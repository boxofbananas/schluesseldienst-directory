#!/usr/bin/env python3
"""Gate 1/2: holt die Einträge einer Google-Maps-Kategorie für Deutschland aus der DataForSEO
Business Listings API und schreibt sie als input/listings-raw.csv in der Outscraper-Spaltenfolge,
damit scripts/clean_listings.py (Gate 2) unverändert darauf läuft.

Deutschland ist für die Kategorie `locksmith` insgesamt nur etwa 8.000 bis 15.000 Einträge und
passt damit in einen Lauf. Der Filter ist deshalb das **Land** (`address_info.country_code`, ISO
z. B. `DE`), nicht ein einzelnes Bundesland. `--region` grenzt einen Lauf freiwillig auf ein Bundesland ein, zum Beispiel
wenn der Dienst bei tiefer Blätterung keine weiteren Seiten mehr liefert.

Aufruf:
  python3 scripts/fetch_dataforseo.py --find-category locksmith      # welche Kategorie-Kennungen es gibt
  python3 scripts/fetch_dataforseo.py --category locksmith --find-regions
  python3 scripts/fetch_dataforseo.py --category locksmith --estimate
  python3 scripts/fetch_dataforseo.py --category locksmith \
      --out input/listings-raw.csv [--region Bayern] [--max-rows 500] [--min-reviews 1] [--yes]

`--country` ist der Pflichtschalter des Laufs und steht auf `Germany`. Die Spalte `state` jeder
Zeile kommt aus `address_info.region` (das Bundesland, wie Google es schreibt), `state_code` aus der
Zuordnungstabelle unten (BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH laut
wiki/konventionen.md). Die Tabelle fängt beide Schreibweisen ab, die deutsche (`Bayern`) und die
englische (`Bavaria`). Ein Bundesland, das die Tabelle nicht kennt, bekommt **kein** geratenes
Kürzel: `state_code` bleibt leer und die Schreibweise steht im Bericht.

Welche Schreibweise der Datenbestand wirklich benutzt, ist nicht vorhersehbar und wird nicht
geraten: `--find-regions` liest sie aus einer echten Antwort und nennt die Anzahl je Bundesland.

Zugangsdaten (werden nie ausgegeben, nie mitgeliefert, nie in diesen Ordner geschrieben): das
Skript liest die Anmeldung aus der DataForSEO-Verbindung, die im eigenen Terminal eingerichtet
wurde, entweder mit `python3 scripts/connect_dataforseo.py` (fragt API-Login und API-Passwort,
prüft und speichert sie) oder mit dem Befehl aus der Gear-Up-Lektion (`claude mcp add -s user
dataforseo -e DATAFORSEO_LOGIN='...' -e DATAFORSEO_PASSWORD='...' -- npx -y
dataforseo-mcp-server@latest`). Beide legen die Anmeldung in den eigenen Einstellungen von Claude
Code ab, ~/.claude.json. Ebenso gelesen werden DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD aus der
Umgebung und ein stdio-Eintrag von Claude Desktop. Eine reine claude.ai-Verbindung (OAuth) enthält
keine Anmeldung, die ein Skript verwenden kann. Den API-Login gibt es unter
https://app.dataforseo.com/api-access (der API-Login ist die Konto-E-Mail, das API-Passwort ist ein
anderes als das Passwort der Website).

Geld: Search kostet 0,012 $ je Anfrage (bis 1.000 Einträge) plus 0,00036 $ je Eintrag
(veröffentlichte Preise, 29.09.2026). `--estimate` und `--find-regions` nennen ihre Kosten im Kopf
der Ausgabe. Ein echter Lauf fragt vorher nach, solange nicht --yes gesetzt ist. --min-reviews 1
(Vorgabe) filtert Zeilen ohne Bewertung schon auf dem Server, die Gate 2 sowieso verwerfen würde.

Aktualität: jede Zeile trägt last_updated_time aus der Datenbank von DataForSEO (in der Stichprobe
vom September 2026 10 bis 18 Tage alt). Das ist eine Datenbank, keine Abfrage von heute. Dieser
Satz gehört in die FAQ.
"""
import argparse, base64, csv, json, math, os, re, sys, time, unicodedata, urllib.request, urllib.error
from collections import Counter

API = "https://api.dataforseo.com/v3/business_data/business_listings/search/live"
CATEGORIES_API = "https://api.dataforseo.com/v3/business_data/business_listings/categories"
PRICE_REQUEST, PRICE_ITEM, PAGE = 0.012, 0.00036, 1000
# Die Schwellen hinter der Warnung "BRANCHEN-WARNUNG". Bewusst niedrig: eine Warnung unterbricht
# jemanden, der sich schon entschieden hat, und soll nur fallen, wenn das Verzeichnis offensichtlich
# dünn würde (Shawn, 01.10.2026). Ein bundesweiter Lauf hat ein Vielfaches der Einträge eines
# US-Bundesstaats, deshalb liegt die Schwelle für einen Lauf über ganz Deutschland zehnmal höher als
# die alte Bundesstaat-Schwelle; mit --region (ein Bundesland) gilt wieder die kleine Schwelle.
FLAG_MIN_PRIMARY_COUNTRY, FLAG_MIN_PRIMARY_REGION, FLAG_MIN_SITE_SHARE = 1000, 100, 0.5
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CLAUDE_CONFIGS = [os.path.expanduser("~/.claude.json"),
                  os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json"),
                  os.path.join(os.environ.get("APPDATA", ""), "Claude", "claude_desktop_config.json")]

COLUMNS = ["name","phone","website","domain","address","street","city","state","state_code","postal_code","county",
           "country","country_code",
           "latitude","longitude","type","subtypes","category","rating","reviews",
           "reviews_per_score_1","reviews_per_score_2","reviews_per_score_3","reviews_per_score_4","reviews_per_score_5",
           "reviews_tags","about","description","posts","working_hours","business_status","verified",
           "photos_count","photo","logo","place_id","google_id","cid","location_link","area_service",
           "email_1","email_2","email_3","phone_1","phone_2","phone_3","last_updated_time","source"]

# DataForSEO filtert das Land über address_info.country_code (ISO 3166-1 alpha-2, z. B. "DE"),
# nicht über den von Google geschriebenen Ländernamen. Steht in --country ein Name (Vorgabe
# "Germany"), nimmt base_task() den Code aus dieser Tabelle; ein schon zweistelliger Wert wird
# groß geschrieben unverändert durchgereicht. Ohne die Umsetzung lehnt der Dienst das ganze
# Feld "filters" ab (40501 Invalid Field: 'filters').
COUNTRY_CODES = {"germany": "DE", "deutschland": "DE", "de": "DE",
                 "österreich": "AT", "austria": "AT", "schweiz": "CH", "switzerland": "CH"}

def country_code(name):
    n = (name or "").strip()
    return n.upper() if len(n) == 2 else COUNTRY_CODES.get(n.lower(), n)

# Bundesland -> Kürzel laut wiki/konventionen.md. Beide Schreibweisen, die deutsche und die
# englische, zeigen auf dasselbe Kürzel. Die Schlüssel werden mit fold() verglichen, deshalb sind
# Umlaute, Bindestriche und Groß- und Kleinschreibung hier ohne Bedeutung.
BUNDESLAENDER = {
    "BW": ["Baden-Württemberg", "Baden-Wuerttemberg", "Baden Wurttemberg", "Baden-Wurttemberg"],
    "BY": ["Bayern", "Freistaat Bayern", "Bavaria"],
    "BE": ["Berlin"],
    "BB": ["Brandenburg"],
    "HB": ["Bremen", "Freie Hansestadt Bremen"],
    "HH": ["Hamburg", "Freie und Hansestadt Hamburg"],
    "HE": ["Hessen", "Hesse"],
    "MV": ["Mecklenburg-Vorpommern", "Mecklenburg-Western Pomerania", "Mecklenburg Western Pomerania"],
    "NI": ["Niedersachsen", "Lower Saxony"],
    "NW": ["Nordrhein-Westfalen", "North Rhine-Westphalia", "North Rhine Westphalia"],
    "RP": ["Rheinland-Pfalz", "Rhineland-Palatinate"],
    "SL": ["Saarland"],
    "SN": ["Sachsen", "Freistaat Sachsen", "Saxony"],
    "ST": ["Sachsen-Anhalt", "Saxony-Anhalt"],
    "SH": ["Schleswig-Holstein"],
    "TH": ["Thüringen", "Thueringen", "Freistaat Thüringen", "Thuringia"],
}
# Der deutsche Name je Kürzel, für Bericht und Ausgabe: die erste Schreibweise der Liste.
NAME_BY_CODE = {code: names[0] for code, names in BUNDESLAENDER.items()}


def fmt(x):
    """Eine Zahl mit Punkt als Tausendertrennzeichen, wie im Deutschen: 12345 -> 12.345."""
    return f"{x:,}".replace(",", ".")


def fold(v):
    """Vergleichsform eines Namens: Umlaute umgeschrieben, Kleinbuchstaben, nur Buchstaben und
    Ziffern. Damit sind "Baden-Württemberg", "baden wuerttemberg" und "BADEN-WURTTEMBERG" gleich."""
    v = (v or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        v = v.replace(a, b)
    v = unicodedata.normalize("NFKD", v)
    v = "".join(ch for ch in v if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", v)


CODE_BY_FOLD = {fold(n): code for code, names in BUNDESLAENDER.items() for n in names}


def code_for(region):
    """Das Kürzel zu einer Bundesland-Schreibweise, oder "" wenn die Tabelle sie nicht kennt.
    Es wird nie geraten: ein unbekanntes Bundesland bekommt ein leeres Kürzel und steht im Bericht."""
    return CODE_BY_FOLD.get(fold(region), "")


def _basic(login, password):
    return "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode()


def _clean(v):
    """Ein Wert, der in einer Shell mit Anführungszeichen getippt wurde, die sie behält (cmd.exe),
    kommt als 'wert' an. Ein passendes Paar wird entfernt."""
    v = (v or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
    return v


PY = "python" if os.name == "nt" else "python3"   # was getippt wird; python3 ist unter Windows ein Store-Platzhalter
NO_LOGIN = ("Auf diesem Rechner ist keine DataForSEO-Anmeldung zu finden. Öffnen Sie ein eigenes Terminal (nicht diesen Chat) und führen Sie aus:\n"
            f'  {PY} "{os.path.join(HERE, "connect_dataforseo.py")}"\n'
            "Das Skript fragt API-Login und API-Passwort von app.dataforseo.com/api-access, prüft sie und speichert sie in den "
            "Einstellungen von Claude Code. Oder führen Sie den Befehl aus der Gear-Up-Lektion selbst aus, mit einfachen Anführungszeichen um beide Werte:\n"
            "  claude mcp add -s user dataforseo -e DATAFORSEO_LOGIN='<api login>' -e DATAFORSEO_PASSWORD='<api passwort>' -- npx -y dataforseo-mcp-server@latest\n"
            "(sagt das Terminal, claude sei nicht gefunden, beginnen Sie die Zeile mit ~/.local/bin/claude). "
            "Eine reine claude.ai-Verbindung ist eine OAuth-Verknüpfung und enthält keine Anmeldung, die dieses Skript lesen kann. "
            "Die Anmeldung nie in den Chat einfügen.")
REJECTED = ("DataForSEO hat die gespeicherte Anmeldung abgelehnt (401). Das API-Passwort ist nicht das Passwort zum Anmelden auf der Website: "
            "kopieren Sie beide Werte von app.dataforseo.com/api-access (Reset API password schickt ein neues per E-Mail) und führen Sie dann in einem eigenen Terminal aus:\n"
            f'  {PY} "{os.path.join(HERE, "connect_dataforseo.py")}"\n'
            "Das ersetzt den gespeicherten Eintrag. Die Anmeldung nie in den Chat einfügen.")
FILTER_HINT = ("\nHinweis: Lehnt der Dienst das Filterfeld ab, prüfen Sie die Schreibweise von --country "
               "(`Germany`, wie Google das Land schreibt) und grenzen Sie den Lauf notfalls mit "
               "--region auf ein Bundesland ein.")


def _auth_from_server(cfg):
    """Ein mcpServers-Eintrag: stdio mit der Anmeldung in env, oder http mit Basic-Header. OAuth-Einträge enthalten nichts."""
    if not isinstance(cfg, dict):
        return None
    env = cfg.get("env") or {}
    login = _clean(env.get("DATAFORSEO_LOGIN") or env.get("DATAFORSEO_USERNAME")); password = _clean(env.get("DATAFORSEO_PASSWORD"))
    if login and password:
        return _basic(login, password)
    hdr = (cfg.get("headers") or {}).get("Authorization") or ""
    if hdr.lower().startswith("basic ") and "dataforseo" in json.dumps(cfg).lower():
        return hdr
    return None


def load_credentials():
    """Die gespeicherte Anmeldung, in dieser Reihenfolge: der Eintrag namens dataforseo im
    Benutzerbereich (den connect_dataforseo.py und der Befehl der Lektion schreiben), die Umgebung,
    dann jeder andere Eintrag mit einer Anmeldung. Der Eintrag des Helfers kommt zuerst, damit ein
    älterer Eintrag oder ein Platzhalter in einem Shell-Profil ihn nicht verdeckt."""
    named, others = [], []
    for path in CLAUDE_CONFIGS:
        if not os.path.isfile(path):
            continue
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        top = d.get("mcpServers") or {}
        if "dataforseo" in top:
            named.append(top["dataforseo"])
        others += [cfg for name, cfg in top.items() if name != "dataforseo"]
        for proj in (d.get("projects") or {}).values():
            others += list(((proj or {}).get("mcpServers") or {}).values())
    for cfg in named:
        auth = _auth_from_server(cfg)
        if auth:
            return auth
    login = _clean(os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME"))
    password = _clean(os.environ.get("DATAFORSEO_PASSWORD"))
    if login and password:
        return _basic(login, password)
    for cfg in others:
        auth = _auth_from_server(cfg)
        if auth:
            return auth
    sys.exit(NO_LOGIN)


def post(auth, task, retries=3, url=API):
    body = json.dumps([task]).encode()
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "Authorization": auth})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            if e.code == 401:
                sys.exit(REJECTED)
            if e.code == 402:
                sys.exit("DataForSEO meldet ein zu geringes Guthaben (402). Laden Sie das Konto auf app.dataforseo.com auf und starten Sie den Lauf erneut.")
            if attempt == retries - 1:
                sys.exit(f"DataForSEO hat dreimal mit {e.code} geantwortet. Versuchen Sie es in einigen Minuten erneut.")
            time.sleep(3 * (attempt + 1))
        except (urllib.error.URLError, OSError) as e:
            if attempt == retries - 1:
                sys.exit(f"DataForSEO war nicht erreichbar ({getattr(e, 'reason', e)}). Prüfen Sie die Internetverbindung und starten Sie den Lauf erneut.")
            time.sleep(3 * (attempt + 1))
    if data.get("status_code") != 20000:
        sys.exit(f"Fehler von DataForSEO {data.get('status_code')}: {data.get('status_message')}" + FILTER_HINT)
    t = data["tasks"][0]
    if t.get("status_code") != 20000:
        sys.exit(f"Fehler in der Anfrage an DataForSEO {t.get('status_code')}: {t.get('status_message')}" + FILTER_HINT)
    res = (t.get("result") or [{}])[0]
    return res, float(t.get("cost") or 0)


def _area(a):
    """Land und Region des Aufrufers. `region` heißt bei einem Lauf dieses Skripts das Bundesland;
    scripts/check_vertical.py ruft base_task() mit seinem eigenen Namensraum auf und kennt nur
    --state, deshalb wird beides mit getattr gelesen."""
    return (getattr(a, "country", "") or "").strip(), (getattr(a, "region", "") or getattr(a, "state", "") or "").strip()


def base_task(a):
    """Der Filter des Laufs: das Land, wahlweise zusätzlich ein Bundesland, wahlweise eine
    Mindestzahl an Bewertungen."""
    country, region = _area(a)
    filters = []
    if country:
        filters.append(["address_info.country_code", "=", country_code(country)])
    if region:
        filters += (["and"] if filters else []) + [["address_info.region", "=", region]]
    if getattr(a, "min_reviews", 0) > 0:
        filters += (["and"] if filters else []) + [["rating.votes_count", ">=", a.min_reviews]]
    return {"categories": a.category, "filters": filters,
            "order_by": ["rating.votes_count,desc"]}


def scope(a):
    """Der Umfang des Laufs als Text, für Meldungen und Bericht."""
    country, region = _area(a)
    return (country or "ohne Länderfilter") + (f", Bundesland {region}" if region else "")


def count(auth, a, extra):
    """Zeilen, die die Filter des Laufs und eine weitere Bedingung erfüllen. Eine Anfrage, keine Einträge."""
    task = dict(base_task(a), limit=1)
    task["filters"] = task["filters"] + ["and", extra]
    res, cost = post(auth, task)
    return int(res.get("total_count") or 0), cost


def health(auth, a, sample):
    """Wie viele Zeilen die Kategorie als ihre primäre tragen und wie viele eine Website haben.
    Die primäre Kategorie ist eine Bezeichnung ("Schlüsseldienst"), der Lauf arbeitet aber mit
    Kennungen (locksmith), und die Bezeichnung lässt sich aus der Kennung nicht herleiten
    (Bindestriche, Apostrophe, zwei Schreibweisen derselben Bezeichnung). Deshalb werden die
    Bezeichnungen aus einer Stichprobe der Zeilen selbst gelesen. primary=None heißt: nicht
    gemessen, weil keine Zeile der Stichprobe die Kategorie als primäre trägt. Das ist nie eine Warnung."""
    wanted = {c.lower() for c in a.category}
    labels = sorted({it.get("category") for it in sample
                     if it.get("category") and re.sub(r"[^a-z0-9]+", "_", it["category"].lower()).strip("_") in wanted})
    primary, c1 = None, 0.0
    if labels:
        primary, c1 = count(auth, a, ["category", "in", labels])
    sites, c2 = count(auth, a, ["domain", "<>", None])
    return primary, sites, c1 + c2


def vertical_flags(total, primary, sites, a):
    """Die Gründe, aus denen diese Kategorie in diesem Gebiet offensichtlich nicht passt. Bei fast
    jeder echten Branche bleibt die Liste leer."""
    out = []
    floor = FLAG_MIN_PRIMARY_REGION if a.region else FLAG_MIN_PRIMARY_COUNTRY
    if total == 0:
        return [f"kein bewerteter Betrieb ist unter {', '.join(a.category)} in {scope(a)} eingetragen. Das ist fast immer eine "
                "Schreibweise: prüfen Sie die Kategorie-Kennung (--find-category), die Schreibweise des Landes und, falls gesetzt, "
                "die des Bundeslandes (--find-regions), korrigieren Sie sie und schätzen Sie erneut."]
    if primary is not None and primary < floor:
        out.append(f"nur {fmt(primary)} {'Betrieb trägt' if primary == 1 else 'Betriebe tragen'} in {scope(a)} diese Kategorie als primäre "
                   f"(unter {fmt(floor)}), damit erreichen zu wenige Städte die Mindestzahl an Einträgen und das Verzeichnis bliebe dünn.")
    if sites / total < FLAG_MIN_SITE_SHARE:
        out.append(f"nur {sites / total:.0%} von ihnen haben eine Website (unter der Hälfte), und der Baukasten füllt jeden Eintrag "
                   "aus der Website des Betriebs, also wären die meisten Seiten ein Name und eine Telefonnummer.")
    return out


def s(v):
    return "" if v is None else str(v)


def own_domain_first(mails, domain):
    d = (domain or "").lower().replace("www.", "")
    own = [m for m in mails if d and m.lower().endswith("@" + d)]
    return own + [m for m in mails if m not in own]


def to_row(it, country_name=""):
    """Eine Zeile in der Outscraper-Spaltenfolge. `state` ist das Bundesland, wie Google es schreibt,
    `state_code` das Kürzel aus der Zuordnungstabelle (leer, wenn die Tabelle es nicht kennt).
    `country_name` ist das Land des Laufs und füllt die Spalte `country`, wenn die Antwort selbst
    keinen Landesnamen trägt."""
    ai = it.get("address_info") or {}
    rating = it.get("rating") or {}
    dist = it.get("rating_distribution") or {}
    topics = it.get("place_topics") or {}
    ci = it.get("contact_info") or []
    mails = own_domain_first([c["value"] for c in ci if c.get("type") == "mail"], it.get("domain"))
    main_phone = re.sub(r"\D", "", s(it.get("phone")))
    phones = [c["value"] for c in ci if c.get("type") == "telephone" and re.sub(r"\D", "", c["value"])[-10:] != main_phone[-10:]]
    phones = list(dict.fromkeys(phones))
    wt = (it.get("work_time") or {}).get("work_hours") or {}
    region = s(ai.get("region"))
    row = {
        "name": s(it.get("title")), "phone": s(it.get("phone")), "website": s(it.get("url")), "domain": s(it.get("domain")),
        "address": s(it.get("address")), "street": s(ai.get("address")), "city": s(ai.get("city")), "state": region,
        "state_code": code_for(region), "postal_code": s(ai.get("zip")), "county": "",
        # Das Land wird mitgeschrieben, damit Gate 2 darauf filtern kann (clean_listings.py --country).
        "country": s(ai.get("country")) or s(country_name), "country_code": s(ai.get("country_code")),
        "latitude": s(it.get("latitude")), "longitude": s(it.get("longitude")),
        "type": s(it.get("category")), "subtypes": ", ".join(it.get("additional_categories") or []), "category": s(it.get("category")),
        "rating": s(rating.get("value")), "reviews": s(rating.get("votes_count") or 0),
        "reviews_tags": ", ".join(f"{k} ({v})" for k, v in sorted(topics.items(), key=lambda kv: -kv[1])),
        "about": json.dumps(it.get("attributes") or {}, ensure_ascii=False),
        "description": s(it.get("description")), "posts": "",
        "working_hours": json.dumps(wt.get("timetable") or {}, ensure_ascii=False),
        "business_status": "OPERATIONAL",  # die Listings-Datenbank kennt kein Schließungs-Merkmal; Gate 2 behält diese Zeilen
        "verified": "true" if it.get("is_claimed") else "false",
        "photos_count": s(it.get("total_photos")), "photo": s(it.get("main_image")), "logo": s(it.get("logo")),
        "place_id": s(it.get("place_id")), "google_id": s(it.get("feature_id")), "cid": s(it.get("cid")),
        "location_link": s(it.get("check_url")), "area_service": "",
        "last_updated_time": s(it.get("last_updated_time")), "source": "dataforseo",
    }
    for i in range(1, 6):
        row[f"reviews_per_score_{i}"] = s(dist.get(str(i), 0))
    for i in range(3):
        row[f"email_{i+1}"] = mails[i] if i < len(mails) else ""
        row[f"phone_{i+1}"] = phones[i] if i < len(phones) else ""
    return row


def sample_page(auth, a, limit):
    """Eine echte Seite Einträge, aus der Schreibweisen gelesen werden. Eine Anfrage."""
    res, cost = post(auth, dict(base_task(a), limit=max(1, min(PAGE, limit))))
    return res.get("items") or [], int(res.get("total_count") or 0), cost


def region_report(auth, a, items):
    """Die Bundesland-Schreibweisen aus einer echten Antwort, je Schreibweise mit der genauen Anzahl
    aus einer eigenen Zählanfrage. Rückgabe: (Zeilen für die Ausgabe, Kosten, unbekannte Schreibweisen).
    Die Schreibweisen stammen aus der Stichprobe; eine Schreibweise, die in der Stichprobe nicht
    vorkommt, fehlt hier. Deshalb wird die Stichprobengröße in der Ausgabe genannt."""
    seen = Counter(s((it.get("address_info") or {}).get("region")) or "(leer)" for it in items)
    lines, cost, unknown = [], 0.0, []
    for name, in_sample in seen.most_common():
        if name == "(leer)":
            lines.append((name, None, in_sample, ""))
            unknown.append(name)
            continue
        exact, c = count(auth, a, ["address_info.region", "=", name])
        cost += c
        code = code_for(name)
        if not code:
            unknown.append(name)
        lines.append((name, exact, in_sample, code))
    lines.sort(key=lambda x: -(x[1] or 0))
    return lines, cost, unknown


def print_region_lines(lines):
    print(f"{'Schreibweise in address_info.region':40s} {'Einträge':>10s} {'Stichprobe':>11s}  Kürzel")
    for name, exact, in_sample, code in lines:
        print(f"{name[:40]:40s} {('?' if exact is None else fmt(exact)):>10s} {fmt(in_sample):>11s}  "
              f"{code or 'unbekannt, Kürzel bleibt leer'}")


def main():
    ap = argparse.ArgumentParser(description="Einträge einer Google-Maps-Kategorie für ein Land aus DataForSEO Business Listings holen.")
    ap.add_argument("--find-category", metavar="WORT",
                    help='Kategorie-Kennungen von DataForSEO auflisten, die WORT enthalten (z. B. "locksmith"), und beenden; kostenlose Anfrage')
    ap.add_argument("--category", action="append", default=[],
                    help="Kategorie-Kennung von DataForSEO, mehrfach möglich (höchstens 10), z. B. locksmith")
    ap.add_argument("--country", default="Germany",
                    help='Land, wie Google es schreibt; der Pflichtfilter des Laufs (Vorgabe: Germany)')
    ap.add_argument("--region", default="",
                    help='optional: Lauf auf ein Bundesland eingrenzen, Schreibweise wie in address_info.region (siehe --find-regions)')
    ap.add_argument("--find-regions", action="store_true",
                    help="aus einer echten Antwort lesen, welche Schreibweisen für address_info.region im Datenbestand vorkommen, mit Anzahl je Bundesland; kein Lauf")
    ap.add_argument("--sample", type=int, default=1000,
                    help="wie viele Zeilen --estimate und --find-regions als Stichprobe lesen (höchstens 1000)")
    ap.add_argument("--out", default=os.path.join(ROOT, "input", "listings-raw.csv"))
    ap.add_argument("--estimate", action="store_true", help="schätzt ohne Lauf: Zeilenzahl und Kosten, Verteilung über die Bundesländer, Zahl der Städte, Anteil mit primärer Kategorie, Anteil mit Website, und eine BRANCHEN-WARNUNG, wenn die Branche offensichtlich nicht passt")
    ap.add_argument("--max-rows", type=int, default=0, help="nach so vielen Zeilen aufhören (Tests)")
    ap.add_argument("--min-reviews", type=int, default=1, help="Filter auf dem Server; 0 holt alles")
    ap.add_argument("--allow-partial", action="store_true",
                    help="eine unvollständige Menge trotzdem schreiben, wenn der Dienst keine weiteren Seiten liefert (Vorgabe: abbrechen und nach Bundesländern aufteilen)")
    ap.add_argument("--yes", action="store_true", help="die Rückfrage überspringen")
    a = ap.parse_args()
    auth = load_credentials()

    if a.find_category:
        req = urllib.request.Request(CATEGORIES_API, headers={"Authorization": auth})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 401:
                sys.exit(REJECTED)
            raise
        result = (data.get("tasks") or [{}])[0].get("result") or []
        # Der Endpunkt gibt die Kategorien als Ergebnisliste selbst zurück (kostenlos, GET)
        # und liefert [{category_name, business_count}, ...]; category_name ist die Kennung für --category
        items = result if (result and "category_name" in result[0]) else ((result[0] if result else {}) or {}).get("items") or []
        word = a.find_category.lower().replace(" ", "_")
        hits = sorted([it for it in items if word in (it.get("category_name") or "").lower()],
                      key=lambda it: -(it.get("business_count") or 0))
        print(f"Kategorie-Kennungen mit '{a.find_category}' ({len(hits)}), mit Betrieben weltweit; eine oder mehrere als --category übergeben:")
        for it in hits:
            print(f"  {it.get('category_name'):45s} {fmt(it.get('business_count') or 0):>12s}")
        return

    if not a.category:
        sys.exit("--category wird für --find-regions, --estimate und jeden Lauf gebraucht (Kennung suchen: --find-category).")
    if not a.country.strip():
        sys.exit("--country darf nicht leer sein; der Lauf filtert auf das Land (Vorgabe: Germany).")
    if len(a.category) > 10:
        sys.exit("Höchstens 10 Kategorien je Lauf.")

    if a.find_regions:
        items, total, cost = sample_page(auth, a, a.sample)
        lines, rcost, unknown = region_report(auth, a, items)
        cost += rcost
        print(f"Schreibweisen der Bundesländer für {', '.join(a.category)} in {scope(a)}.")
        print(f"Kosten dieser Abfrage, von DataForSEO gemeldet: {cost:.4f} $ "
              f"({1 + len(lines)} Anfragen, Stichprobe {fmt(len(items))} Zeilen von {fmt(total)} insgesamt)")
        print("Die Schreibweisen stammen aus dieser Stichprobe, die Anzahl je Schreibweise aus einer eigenen Zählanfrage. "
              "Eine Schreibweise, die in der Stichprobe nicht vorkam, fehlt hier; mit einer größeren --sample erneut prüfen.\n")
        print_region_lines(lines)
        if unknown:
            print("\nNicht in der Zuordnungstabelle und deshalb ohne Kürzel: " + ", ".join(unknown) +
                  ".\nDiese Zeilen bekommen ein leeres state_code. Tragen Sie die Schreibweise in BUNDESLAENDER in diesem Skript nach, "
                  "statt ein Kürzel zu raten.")
        print(f"\nAls Filter für einen Lauf über ein Bundesland: --region \"<Schreibweise aus der ersten Spalte>\"")
        return

    probe_limit = a.sample if a.estimate else 1
    items, total, cost = sample_page(auth, a, probe_limit)
    target = min(total, a.max_rows) if a.max_rows else total
    requests_needed = max(1, math.ceil(target / PAGE))
    projected = requests_needed * PRICE_REQUEST + target * PRICE_ITEM
    print(f"Kategorien: {', '.join(a.category)} | Gebiet: {scope(a)}")
    print(f"Zeilen in der Datenbank von DataForSEO (Bewertungen >= {a.min_reviews}): {fmt(total)}")
    print(f"Zu holende Zeilen: {fmt(target)} in {requests_needed} Anfrage(n); voraussichtliche Kosten etwa {projected:.2f} $ "
          f"(veröffentlichte Preise; abgerechnet wird der tatsächliche Betrag). Kosten der Probeanfrage: {cost:.4f} $")
    if a.estimate:
        if total == 0:
            print("BRANCHEN-WARNUNG: " + vertical_flags(0, 0, 0, a)[0])
            return
        lines, rcost, unknown = region_report(auth, a, items)
        primary, sites, hcost = health(auth, a, items)
        spent = cost + rcost + hcost
        cities = {s((it.get("address_info") or {}).get("city")) for it in items if (it.get("address_info") or {}).get("city")}
        print(f"Kosten dieser Schätzung insgesamt, von DataForSEO gemeldet: {spent:.4f} $ "
              f"({2 + len(lines) + (1 if primary is not None else 0)} Anfragen, Stichprobe {fmt(len(items))} Zeilen)")
        print(f"\nVerteilung über die Bundesländer (Anzahl aus je einer Zählanfrage, Schreibweisen aus der Stichprobe von {fmt(len(items))} Zeilen):")
        print_region_lines(lines)
        covered = sum(x[1] or 0 for x in lines)
        if covered < total:
            print(f"Summe der gefundenen Bundesländer: {fmt(covered)} von {fmt(total)}. Die Differenz sind Schreibweisen, die in der "
                  "Stichprobe nicht vorkamen; mit --find-regions und größerer --sample nachsehen.")
        if unknown:
            print("Ohne Kürzel, weil nicht in der Zuordnungstabelle: " + ", ".join(unknown) + " (state_code bleibt leer, nichts wird geraten).")
        print(f"\nStädte: mindestens {fmt(len(cities))} verschiedene Städte in der Stichprobe von {fmt(len(items))} Zeilen "
              "(eine Untergrenze; die genaue Zahl steht nach Gate 2 im Bericht von clean_listings.py).")
        ptext = (f"{fmt(primary)} von {fmt(total)} ({primary / total:.0%}) tragen sie als primäre" if primary is not None
                 else "nicht gemessen (keine Zeile der Stichprobe trägt sie als primäre)")
        print(f"\nPrimäre Kategorie: {ptext}. Mit Website: {fmt(sites)} ({sites / total:.0%}).")
        flags = vertical_flags(total, primary, sites, a)
        for fl in flags:
            print("BRANCHEN-WARNUNG: " + fl)
        if not flags:
            print("Branchen-Warnungen: keine.")
        print(f"\nFür Gate 1: {fmt(total)} Einträge in {scope(a)}, {len(lines)} Bundesländer, mindestens {fmt(len(cities))} Städte.")
        return
    if total == 0:
        sys.exit("Es gibt nichts zu holen. Prüfen Sie die Kategorie-Kennung (--find-category), die Schreibweise des Landes und, falls gesetzt, "
                 "die des Bundeslandes (--find-regions).")
    if not a.yes:
        try:
            ans = input("Jetzt holen? Zum Fortfahren yes eingeben: ").strip().lower()
        except EOFError:
            sys.exit("Kein Terminal für die Rückfrage. Nach dem Ja führen Sie denselben Befehl mit --yes aus.")
        if ans not in ("yes", "ja", "j"):
            print("Vor dem Holen abgebrochen."); return

    rows, spent, offset, token, seen = [], cost, 0, None, set()
    stalled = ""
    while len(rows) < target:
        task = dict(base_task(a), limit=min(PAGE, target - len(rows)))
        if token:
            task["offset_token"] = token
        else:
            task["offset"] = offset
        res, c = post(auth, task); spent += c
        items = res.get("items") or []
        if not items:
            stalled = "der Dienst hat eine leere Seite geliefert"
            break
        before = len(rows)
        for it in items:
            key = it.get("cid") or it.get("place_id") or (it.get("title"), it.get("address"))
            if key in seen:
                continue
            seen.add(key); rows.append(to_row(it, a.country))
        new_token = res.get("offset_token")
        offset += len(items)
        print(f"  geholt: {fmt(len(rows))} / {fmt(target)}", file=sys.stderr)
        if len(items) < task["limit"]:
            # Kürzere Seite als angefragt: bei DataForSEO das Ende der Treffermenge.
            break
        # Abbruchsicherung für tiefe Blätterung: bei großen Mengen kann der Dienst irgendwann keine
        # weitere Seite mehr liefern (kein offset_token mehr, oder dasselbe Token, oder nur schon
        # gesehene Zeilen). Dann wird nichts stillschweigend Unvollständiges geschrieben.
        if len(rows) == before:
            stalled = "eine ganze Seite enthielt nur Zeilen, die schon geholt waren"
            break
        if not new_token:
            stalled = "der Dienst hat kein offset_token für die nächste Seite mehr geliefert"
            break
        if new_token == token:
            stalled = "der Dienst hat dasselbe offset_token noch einmal geliefert, die Blätterung kommt nicht weiter"
            break
        token = new_token

    split_hint = (f"Lauf nach Bundesländern aufteilen: {fmt(len(rows))} von {fmt(target)} Zeilen geholt, dann {stalled}. "
                  "Die Blätterung des Dienstes reicht für diese Menge nicht. Starten Sie je Bundesland einen Lauf, zum Beispiel\n"
                  f"  {PY} scripts/fetch_dataforseo.py --category {' --category '.join(a.category)} --region \"Bayern\" "
                  "--out input/listings-raw-by.csv --yes\n"
                  "und hängen Sie die Dateien danach aneinander (die Kopfzeile nur einmal). Die Schreibweisen der Bundesländer "
                  "nennt --find-regions.")
    if stalled and len(rows) < target and not a.allow_partial:
        sys.exit("ABBRUCH, es wurde nichts geschrieben. " + split_hint)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS); w.writeheader(); w.writerows(rows)

    with_email = sum(1 for r in rows if r["email_1"])
    by_state = Counter(r["state"] or "(leer)" for r in rows)
    no_code = sorted({r["state"] or "(leer)" for r in rows if not r["state_code"]})
    primary = sum(1 for r in rows if r["type"].lower().replace(" ", "_") in [c.lower() for c in a.category])
    cities = {(r["state_code"] or r["state"], r["city"]) for r in rows if r["city"]}
    ages = [r["last_updated_time"][:10] for r in rows if r["last_updated_time"]]
    report = [
        "# Abholbericht (DataForSEO Business Listings)", "",
        f"- Geholt: {time.strftime('%d.%m.%Y %H:%M %Z (UTC%z)')} (Ortszeit)",
        f"- Kategorien: {', '.join(a.category)}; Land: {a.country}" + (f"; Bundesland: {a.region}" if a.region else "") +
        f"; Mindestbewertungen: {a.min_reviews}",
        f"- Zeilen in der Datenbank: {fmt(total)}; geschriebene Zeilen: {fmt(len(rows))} nach `{os.path.relpath(a.out, ROOT)}`",
        f"- Von DataForSEO gemeldete Kosten dieses Laufs: {spent:.4f} $",
        f"- Städte: {fmt(len(cities))}; Bundesländer: {len(by_state)}",
        f"- Zeilen, deren primäre Kategorie eine der gesuchten ist: {fmt(primary)} (die übrigen tragen sie als zusätzliche Kategorie; "
        "Gate 2 behält sie und listet sie in 02-clean-report.md nach primärem Typ, die Entscheidung fällt bei Gate 4)",
        f"- Zeilen mit mindestens einer E-Mail-Adresse: {fmt(with_email)} (eigene Domain zuerst; vor einer Ansprache Domain prüfen und Zustellbarkeit testen)",
        f"- Zeitraum von last_updated_time: {min(ages) if ages else 'nicht vorhanden'} bis {max(ages) if ages else 'nicht vorhanden'} "
        "(Alter der Datenbank, keine Abfrage von heute)",
        "", "## Einträge je Bundesland", "",
        "| Bundesland (Schreibweise von Google) | Kürzel | Einträge |", "|---|---|---|",
    ]
    report += [f"| {name} | {code_for(name) or '(unbekannt)'} | {fmt(n)} |" for name, n in by_state.most_common()]
    if no_code:
        report += ["", "**Ohne Kürzel:** " + ", ".join(no_code) + ". Diese Schreibweisen kennt die Zuordnungstabelle in "
                   "`scripts/fetch_dataforseo.py` nicht; `state_code` bleibt leer, es wurde nichts geraten. Tragen Sie sie dort nach "
                   "und holen Sie erneut, oder setzen Sie das Kürzel in der CSV von Hand."]
    if stalled:
        report += ["", "**Unvollständig:** " + split_hint.replace("\n", " ")]
    report += ["", f"Weiter: `{PY} scripts/clean_listings.py input/listings-raw.csv --country \"{a.country}\" "
               "--out output/schluesseldienste-deutschland/02-listings-clean.csv --category \"Schlüsseldienst\"`"]
    rep_path = os.path.join(os.path.dirname(a.out) or ".", "listings-raw-report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
