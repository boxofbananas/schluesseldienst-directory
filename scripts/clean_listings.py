#!/usr/bin/env python3
"""Gate 2: einen Google-Maps-Export (Outscraper oder die Ausgabe von scripts/fetch_dataforseo.py)
zur Eintragsmenge des Verzeichnisses aufräumen.

Aufruf:
  python3 scripts/clean_listings.py input/listings-raw.csv \
      --category "Schlüsseldienst" \
      --out output/schluesseldienste-deutschland/02-listings-clean.csv \
      [--country Germany] [--bundesland BY] [--owned-phones 062112345,017612345] \
      [--niche "schlüsseldienst,aufsperrdienst"] [--min-reviews 1] [--thin-reviews 5]

Der Ausgabeordner ist `output/schluesseldienste-deutschland/`. Das Verzeichnis umfasst ganz Deutschland,
deshalb filtert dieses Skript auf das **Land** (`--country`, Vorgabe Germany) und nicht auf ein
Bundesland. `--bundesland` grenzt einen Lauf freiwillig auf ein Bundesland ein (Kürzel wie `BY`
oder Name wie `Bayern`/`Bavaria`); das Bundesland jeder Zeile bleibt in der Spalte `state`
erhalten und der Bericht schlüsselt alles danach auf.

`--niche` sind die Wörter, die diese Branche in ihre Firmennamen schreibt. Vorbelegt sind die
deutschen Begriffe (NICHE_DEFAULT unten):
  schlüsseldienst, schluesseldienst, schlüsselnotdienst, aufsperrdienst, schlüsselservice,
  schließanlagen, sicherheitstechnik
Verglichen wird umlauttolerant (ä/ae, ö/oe, ü/ue, ß/ss) und ohne Rücksicht auf Schreibweise,
Bindestriche und Leerzeichen, sonst greift kein Begriff: „Schlüssel-Dienst" und „Schluesseldienst"
zählen wie „Schlüsseldienst". `--category` ist die Bezeichnung der Google-Maps-Kategorie.

Die Regeln stehen in wiki/framework/listings-cleaning.md. Der Bericht geht nach stdout und als
02-clean-report.md neben --out. Keine Zeile wird wegen ihres Gewerbes von selbst entfernt: Zeilen,
die die Kategorie nur als zusätzliche Google-Kategorie tragen, typische Fehlfänge der Kategorie
`locksmith` (Schuhmacher, Gravur und Stickerei, Metallbau und Schlosserei, Baumärkte,
Autowerkstätten) und Namen, die an vielen Adressen vorkommen (Ketten und Callcenter), stehen nur
im Bericht. Darüber entscheidet der Mensch bei Gate 4 (04-exclusions.csv).
"""
import argparse, csv, json, re, sys, os, unicodedata
from collections import Counter, defaultdict
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

KEEP = ["name","phone","website","address","street","city","state","state_code","postal_code","county",
        "latitude","longitude","type","subtypes","category","rating","reviews",
        "reviews_per_score_1","reviews_per_score_2","reviews_per_score_3","reviews_per_score_4","reviews_per_score_5",
        "reviews_tags","about","description","posts","working_hours","business_status","verified",
        "photo","logo","place_id","google_id","cid","location_link","area_service",
        "domain","email_1","email_2","email_3","phone_1","phone_2","phone_3","last_updated_time","source"]
# geprueft und geprueft_jahr gehören zum Siegel-Programm (wiki/konventionen.md) und werden hier
# leer angelegt; gefüllt werden sie erst, wenn der Herausgeber einen Betrieb geprüft hat.
ADDED = ["slug","city_slug","owned","thin","featured","featured_cities","claimed","geprueft","geprueft_jahr"]

NICHE_DEFAULT = ("schlüsseldienst,schluesseldienst,schlüsselnotdienst,aufsperrdienst,"
                 "schlüsselservice,schließanlagen,sicherheitstechnik")

# Länder-Schreibweisen, die als dasselbe Land gelten. Google schreibt das Land englisch, ein
# Outscraper-Export trägt zusätzlich country_code. Jede Schreibweise der Gruppe darf in --country
# stehen und erkennt alle anderen mit.
COUNTRY_GROUPS = [["germany", "deutschland", "de", "deu", "brd"]]

# Typische Fehlfänge der Google-Kategorie `locksmith` in Deutschland. Sie werden nur gezählt und im
# Bericht gezeigt, damit der Mensch bei Gate 4 entscheiden kann. Verglichen wird die umlauttolerante
# Form von Name, type, subtypes und category.
MISFITS = {
    "Schuhmacher und Schuhreparatur": r"schuhmach|schuhrepar|schuster|schuhservic|misterminit|schuhwerkstatt",
    "Gravur und Stickerei": r"gravur|graveur|stickerei|bestick|textildruck|schilderherstell|schildermach|stempel",
    "Metallbau und Schlosserei": r"metallbau|schlosserei|metallwerkstatt|stahlbau|schweisstechnik|zaunbau|tore?undzaun",
    "Baumarkt und Eisenwaren": r"baumarkt|bauhaus|hornbach|hagebau|toombaumarkt|eisenwaren|haushaltswaren|werkzeughandel",
    "Autowerkstatt und Kfz": r"autowerkstatt|kfzwerkstatt|kfzservice|autoservice|autohaus|reifen|autoglas|abschleppdienst",
}
MISFIT_RE = {k: re.compile(v) for k, v in MISFITS.items()}

try:    # eine einzige Zuordnungstabelle für die Bundesländer, damit nichts doppelt gepflegt wird
    from fetch_dataforseo import code_for as bundesland_code, NAME_BY_CODE
except Exception:     # pragma: no cover - nur, wenn die Datei fehlt
    def bundesland_code(_): return ""
    NAME_BY_CODE = {}

UMLAUTE = (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"))


def fold(s):
    """Vergleichsform: Kleinbuchstaben, Umlaute umgeschrieben (ä/ae, ö/oe, ü/ue, ß/ss), alles
    andere als Buchstaben und Ziffern entfernt. Damit greifen die Begriffe unabhängig von
    Schreibweise, Bindestrich und Leerzeichen."""
    s = (s or "").lower()
    for a, b in UMLAUTE:
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", s)


def slug(s):
    """Kleinbuchstaben, ASCII, Bindestriche zwischen allem anderen. Umlaute werden **vor** dem
    Entfernen der Sonderzeichen umgeschrieben (ä->ae, ö->oe, ü->ue, ß->ss, wiki/konventionen.md),
    sonst wird aus „Nürnberg" n-rnberg. Danach fallen übrige Akzente weg (NFKD), damit auch
    „Besançon" zu besancon wird. Gilt für `slug` und `city_slug`."""
    s = (s or "")
    for a, b in UMLAUTE:
        s = s.replace(a, b).replace(a.upper(), b)
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def norm_phone(p):
    """Vergleichsform einer Telefonnummer: nur Ziffern, Ländervorwahl 0049/+49 abgeschnitten und
    die führende 0 der Ortsvorwahl entfernt, damit +49 621 123456 und 0621 123456 dieselbe Nummer
    sind. Übrig bleiben die letzten 10 Stellen wie bisher, kurze Nummern unverändert."""
    d = re.sub(r"\D", "", p or "")
    if d.startswith("0049"):
        d = d[4:]
    elif d.startswith("49") and len(d) > 10:
        d = d[2:]
    d = d.lstrip("0")
    return d[-10:] if len(d) >= 10 else d


def norm_addr(r):
    return slug((r.get("street") or r.get("address") or "") + " " + (r.get("postal_code") or ""))


def site_domain(u):
    u = (u or "").strip().lower()
    if not u: return ""
    u = re.sub(r"^https?://", "", u).split("/")[0].split("?")[0]
    return u[4:] if u.startswith("www.") else u
TRACKING = re.compile(r"^(utm_|se_|y_source|gclid|fbclid|msclkid|gad_|ref$|source$|campaign$)", re.I)


def clean_url(u):
    """Outscraper behält die Tracking-Parameter von Maps, oft prozentkodiert im Pfad
    (https://site.de/%3Futm_source%3Dgoogle), was einen 404 ergibt. Dekodieren und Tracking entfernen."""
    u = (u or "").strip()
    if not u or u.lower() == "none": return ""
    if re.search(r"%3F|%26|%3D", u, re.I):
        u = re.sub(r"%3F", "?", re.sub(r"%26", "&", re.sub(r"%3D", "=", u, flags=re.I), flags=re.I), flags=re.I)
    try:
        s = urlsplit(u)
        q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True) if not TRACKING.search(k)]
        return urlunsplit((s.scheme, s.netloc, s.path or "/", urlencode(q), s.fragment))
    except ValueError:
        return u


def to_int(v):
    try: return int(float(str(v).replace(",", ".")))
    except Exception: return 0


def fmt(x):
    return f"{x:,}".replace(",", ".")


def has_text(r):
    """Fließtext über den Betrieb, für das Merkmal „dünn": eine nicht leere description oder ein
    about, das keine Attribut-JSON ist. Beide Quellen schreiben die Google-Attribute als JSON in
    about (die DataForSEO-Abholung in jeder Zeile), ein JSON-about ist also Daten, kein Text."""
    if (r.get("description") or "").strip(): return True
    ab = (r.get("about") or "").strip()
    if not ab: return False
    try:
        json.loads(ab); return False
    except ValueError:
        return True


def country_match(r, accepted, has_cols):
    """Gehört die Zeile zum Zielland? Geprüft werden country und country_code. Fehlen beide Spalten
    im Export, bleibt die Zeile drin (und der Bericht sagt, dass nicht gefiltert wurde)."""
    if not has_cols:
        return True
    return fold(r.get("country")) in accepted or fold(r.get("country_code")) in accepted


def bundesland_of(r):
    """Das Bundesland der Zeile als Klartext: die Schreibweise aus `state`, sonst der Name zum
    Kürzel, sonst „(ohne Angabe)"."""
    st = (r.get("state") or "").strip()
    if st: return st
    return NAME_BY_CODE.get((r.get("state_code") or "").upper().strip(), "") or "(ohne Angabe)"


def main():
    ap = argparse.ArgumentParser(description="Gate 2: Google-Maps-Export zur Eintragsmenge aufräumen.")
    ap.add_argument("csv")
    ap.add_argument("--niche", default=NICHE_DEFAULT,
                    help="Namensbegriffe, mit Komma getrennt; vorbelegt mit den deutschen Schlüsseldienst-Begriffen")
    ap.add_argument("--country", default="Germany", help="Land, auf das gefiltert wird (Vorgabe: Germany; Deutschland und DE gelten als dasselbe)")
    ap.add_argument("--bundesland", "--state", default="",
                    help="optional: nur dieses Bundesland behalten, als Kürzel (BY) oder Name (Bayern, Bavaria)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--category", default="", help="Bezeichnung der Google-Maps-Kategorie (in type/subtypes/category gesucht)")
    ap.add_argument("--owned-phones", default="", help="eigene Nummern, mit Komma getrennt; die Zeilen werden nur markiert")
    ap.add_argument("--min-reviews", type=int, default=1)
    ap.add_argument("--thin-reviews", type=int, default=5)
    ap.add_argument("--city-floor", type=int, default=3, help="Mindestzahl an Einträgen, ab der eine Stadt eine eigene Seite bekommt")
    ap.add_argument("--chain-addresses", type=int, default=5,
                    help="ab wie vielen Adressen ein gleicher Name im Bericht als Kette oder Callcenter auftaucht")
    ap.add_argument("--max-age-days", type=int, default=365,
                    help="nur DataForSEO-Zeilen: Zeilen verwerfen, deren last_updated_time älter ist (0 = alle behalten)")
    a = ap.parse_args()
    terms = [t.strip() for t in a.niche.split(",") if t.strip()]
    folded_terms = sorted({fold(t) for t in terms} - {""})
    if not folded_terms and not a.category.strip():
        ap.error("geben Sie --niche, --category oder beides an")
    cat = fold(a.category)
    owned = {norm_phone(p) for p in a.owned_phones.split(",") if p.strip()}
    accepted_country = {fold(a.country)}
    for group in COUNTRY_GROUPS:
        folded = {fold(x) for x in group}
        if accepted_country & folded:
            accepted_country |= folded
    want_code = (a.bundesland or "").strip()
    want_code = want_code.upper() if len(want_code) <= 3 else (bundesland_code(want_code) or "")
    if a.bundesland and not want_code:
        ap.error(f"--bundesland \"{a.bundesland}\" ist weder ein Kürzel noch ein bekannter Bundesland-Name "
                 "(die Tabelle steht in scripts/fetch_dataforseo.py, BUNDESLAENDER)")

    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        cols_in = rd.fieldnames or []
        rows = list(rd)
    steps = [("Zeilen gelesen", len(rows))]
    notes = []

    has_country_cols = bool({"country", "country_code"} & set(cols_in))
    rows = [r for r in rows if country_match(r, accepted_country, has_country_cols)]
    steps.append((f"Land {a.country}", len(rows)))
    if not has_country_cols:
        notes.append(f"Der Export hat keine Spalte `country` und keine Spalte `country_code`, deshalb wurde **nicht** auf das Land "
                     f"gefiltert; alle {fmt(steps[0][1])} Zeilen gingen in die nächste Regel. Prüfen Sie beim Abholen, dass das Land "
                     "mitgeschrieben wird (scripts/fetch_dataforseo.py schreibt es).")
    if want_code:
        rows = [r for r in rows if (r.get("state_code") or "").upper() == want_code
                or bundesland_code(r.get("state")) == want_code]
        steps.append((f"Bundesland {want_code}", len(rows)))

    rows = [r for r in rows if (r.get("business_status") or "OPERATIONAL").upper() == "OPERATIONAL"]
    steps.append(("dauerhaft oder vorübergehend geschlossen verworfen", len(rows)))
    if a.max_age_days and rows and rows[0].get("source") == "dataforseo":
        # Die Listings-Datenbank kennt kein Schließungs-Merkmal; das Alter ist der Ersatz dafür.
        import datetime
        cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=a.max_age_days)).strftime("%Y-%m-%d")
        rows = [r for r in rows if (r.get("last_updated_time") or "9999")[:10] >= cutoff]
        steps.append((f"seit {a.max_age_days} Tagen nicht aktualisiert verworfen", len(rows)))
    rows = [r for r in rows if to_int(r.get("reviews")) >= a.min_reviews]
    steps.append((f"weniger als {a.min_reviews} Bewertung(en) verworfen", len(rows)))

    def match_kind(r):
        """Wie eine Zeile Regel 4 besteht: „name" (ein Begriff steckt im Namen), „type" (die
        Kategorie ist die primäre Google-Kategorie), „secondary" (die Kategorie steht nur in
        subtypes/category) oder None. Verglichen wird umlauttolerant."""
        n = fold(r.get("name"))
        if any(t in n for t in folded_terms): return "name"
        if cat:
            if cat in fold(r.get("type")): return "type"
            if cat in fold(" ".join((r.get(k) or "") for k in ("subtypes", "category"))): return "secondary"
        return None

    kept = []
    for r in rows:
        k = match_kind(r)
        if k:
            r["_match"] = k; kept.append(r)   # _match steht nicht in KEEP und kommt nie in die CSV
    rows = kept
    steps.append(("Treffer über Name oder Kategorie", len(rows)))

    rows.sort(key=lambda r: -to_int(r.get("reviews")))
    seen_p, seen_a, out, dropped_dupes = set(), set(), [], 0
    for r in rows:
        p, ad = norm_phone(r.get("phone")), norm_addr(r)
        if p and p in seen_p: dropped_dupes += 1; continue
        if ad and ad in seen_a: dropped_dupes += 1; continue
        if p: seen_p.add(p)
        if ad: seen_a.add(ad)
        out.append(r)
    rows = out
    steps.append(("Dubletten über Telefon und Adresse verworfen", len(rows)))

    slugs = Counter()
    for r in rows:
        r["city_slug"] = slug(r.get("city"))
        base = f"{slug(r.get('name'))}-{r['city_slug']}"
        slugs[base] += 1
        r["slug"] = base if slugs[base] == 1 else f"{base}-{slug(r.get('postal_code'))}"
        r["owned"] = "true" if norm_phone(r.get("phone")) in owned else "false"
        r["thin"] = "true" if (to_int(r.get("reviews")) < a.thin_reviews or not has_text(r)) else "false"
        r["website"] = clean_url(r.get("website"))
        r["featured"] = ""; r["featured_cities"] = ""; r["claimed"] = ""
        r["geprueft"] = ""; r["geprueft_jahr"] = ""

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KEEP + ADDED, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

    # Website-Domains der behaltenen Zeilen, eine je Zeile, für den Emails-&-Contacts-Scraper von
    # Outscraper (nur auf der aufgeräumten Liste laufen lassen).
    domains = sorted({d for d in (site_domain(r.get("website")) for r in rows) if d})
    dom_path = os.path.join(os.path.dirname(a.out) or ".", "02-domains.txt")
    with open(dom_path, "w", encoding="utf-8") as f:
        f.write("\n".join(domains) + ("\n" if domains else ""))

    # --- Bericht ---------------------------------------------------------------
    cities = Counter(r.get("city") for r in rows)
    floor_cities = {c: n for c, n in cities.items() if n >= a.city_floor}
    types = Counter((r.get("type") or "").strip() or "(ohne Typ)" for r in rows)
    secondary = [r for r in rows if r.get("_match") == "secondary"]
    sec_types = Counter((r.get("type") or "").strip() or "(ohne Typ)" for r in secondary)

    # Aufschlüsselung nach Bundesland: Einträge, Städte, Städte über der Mindestzahl. Gruppiert wird
    # nach Kürzel, damit die deutsche und die englische Schreibweise desselben Landes eine Zeile sind;
    # ein Bundesland ohne Kürzel steht unter seiner Schreibweise.
    per_land = defaultdict(lambda: {"rows": 0, "cities": Counter(), "spellings": Counter()})
    for r in rows:
        land = bundesland_of(r)
        code = bundesland_code(land)
        d = per_land[code or f"?{land}"]
        d["rows"] += 1
        d["cities"][r.get("city") or "(ohne Stadt)"] += 1
        d["spellings"][land] += 1
    land_lines = []
    for key, d in sorted(per_land.items(), key=lambda kv: -kv[1]["rows"]):
        over = {c: n for c, n in d["cities"].items() if n >= a.city_floor}
        code = "" if key.startswith("?") else key
        name = NAME_BY_CODE.get(code) or key[1:]
        spellings = ", ".join(s for s, _ in d["spellings"].most_common())
        land_lines.append(f"| {name} | {code or '(unbekannt)'} | {fmt(d['rows'])} | "
                          f"{fmt(len(d['cities']))} | {fmt(len(over))} | {fmt(sum(over.values()))} | {spellings} |")
    ohne_code = sorted({s for key, d in per_land.items() if key.startswith("?") for s in d["spellings"]})

    # Typische Fehlfänge der Kategorie: nur zählen, nie löschen.
    misfit_hits = defaultdict(list)
    for r in rows:
        blob = fold(r.get("name")) + "|" + fold(" ".join((r.get(k) or "") for k in ("type", "subtypes", "category")))
        for label, rx in MISFIT_RE.items():
            if rx.search(blob):
                misfit_hits[label].append(f"{(r.get('name') or '').strip()} ({(r.get('city') or '').strip()})")

    # Ketten und Callcenter: gleicher Name an mehr als --chain-addresses Adressen.
    by_name = defaultdict(lambda: {"name": "", "addr": set(), "cities": set(), "rows": 0})
    for r in rows:
        k = fold(r.get("name"))
        if not k: continue
        e = by_name[k]
        e["name"] = e["name"] or (r.get("name") or "").strip()
        e["addr"].add(norm_addr(r) or f"zeile-{id(r)}")
        e["cities"].add((r.get("city") or "").strip())
        e["rows"] += 1
    chains = sorted([e for e in by_name.values() if len(e["addr"]) > a.chain_addresses],
                    key=lambda e: -len(e["addr"]))

    n_in = steps[0][1]; rate = (len(rows) / n_in * 100) if n_in else 0
    dfs = bool(rows) and (rows[0].get("source") == "dataforseo")
    rate_note = ("  (eine DataForSEO-Abholung ist schon vor dem Eintreffen nach Kategorie gefiltert, deshalb besteht der größte Teil "
                 "der Zeilen; Zeilen, die die Kategorie nur als zusätzliche tragen, kommen mit und stehen unten für die Entscheidung bei Gate 4)" if dfs
                 else ("  (ein breiter Scrape behält 2 bis 15 %, ein gezielter Kategorie-Export etwa 20 bis 25 %; außerhalb beider "
                       "Spannen prüfen Sie die Namensbegriffe)" if not 2 <= rate <= 25 else ""))

    lines = ["# Bericht Gate 2 (Aufräumen)", "",
             f"Quelle: `{os.path.relpath(a.csv, os.path.dirname(HERE)) if a.csv.startswith(os.path.dirname(HERE)) else a.csv}`  ",
             f"Land: {a.country}" + (f"  ·  Bundesland: {want_code}" if want_code else "  ·  ganz Deutschland") +
             f"  ·  Kategorie: {a.category or '(keine)'}  ·  Namensbegriffe: {', '.join(terms) or '(keine)'}", "",
             "| Schritt | Zeilen |", "|---|---|"] + [f"| {k} | {fmt(v)} |" for k, v in steps]
    lines += ["", f"**Behalten:** {rate:.1f} %".replace(".", ",") + rate_note,   # Dezimaltrennzeichen Komma (konventionen.md)
              f"**Städte:** {fmt(len(cities))}, davon über der Mindestzahl von {a.city_floor} Einträgen: {fmt(len(floor_cities))}; "
              f"diese halten {fmt(sum(floor_cities.values()))} der {fmt(len(rows))} behaltenen Zeilen",
              f"**Eigene Zeilen gefunden:** {fmt(sum(1 for r in rows if r['owned'] == 'true'))} (werden wie jeder andere Eintrag "
              "geführt, siehe footprint-rules)",
              f"**Dünne Zeilen (zum Start noindex):** {fmt(sum(1 for r in rows if r['thin'] == 'true'))} (unter {a.thin_reviews} "
              "Bewertungen oder ohne Beschreibungstext; Attribut-JSON in `about` gilt nicht als Text)",
              f"**Als Dublette verworfen:** {fmt(dropped_dupes)} (gleiche Telefonnummer oder gleiche Adresse; behalten wurde die "
              "Zeile mit mehr Bewertungen)",
              f"**Neue, leere Spalten:** `geprueft`, `geprueft_jahr` (Siegel-Programm, wiki/konventionen.md)",
              f"**Website-Domains in 02-domains.txt:** {fmt(len(domains))}"]
    if notes:
        lines += ["", "## Hinweise zum Lauf", ""] + [f"- {x}" for x in notes]
    lines += ["", "## Einträge je Bundesland", "",
              "`state` bleibt in jeder Zeile erhalten, `state_code` ist das Kürzel laut wiki/konventionen.md.", "",
              "| Bundesland | Kürzel | Einträge | Städte | Städte ab " + str(a.city_floor) +
              " Einträgen | Einträge in diesen Städten | Schreibweisen im Export |",
              "|---|---|---|---|---|---|---|"] + land_lines
    if ohne_code:
        lines += ["", "**Ohne Kürzel:** " + ", ".join(ohne_code) + ". Diese Schreibweisen kennt die Zuordnungstabelle in "
                  "`scripts/fetch_dataforseo.py` (BUNDESLAENDER) nicht. Tragen Sie sie dort nach, statt ein Kürzel zu raten."]
    lines += ["", "## Behaltene Zeilen nach primärem Typ", "",
              "Die Spalte `type` ist die primäre Google-Kategorie. Jeder andere Typ kam über die Namensbegriffe oder über die "
              "Kategorie als zusätzliche Kategorie herein.", ""]
    lines += [f"- {t}: {fmt(n)}" for t, n in types.most_common()]
    lines += ["", "## Nur über die Kategorie behalten", ""]
    if not cat:
        lines += ["Kein `--category` angegeben, also hat jede behaltene Zeile über ihren Namen gepasst."]
    else:
        lines += [f"{fmt(len(secondary))} Zeilen tragen \"{a.category.strip()}\" nur als zusätzliche Kategorie: weder die "
                  "Namensbegriffe noch der primäre Typ haben gepasst. Sie bleiben drin und stehen hier, sie werden nicht "
                  "verworfen; ob sie bleiben, entscheidet der Mensch bei Gate 4 (04-exclusions.csv)."]
        if secondary:
            lines += ["", "Häufigste primäre Typen darunter:", ""] + [f"- {t}: {fmt(n)}" for t, n in sec_types.most_common(10)]
    lines += ["", "## Typische Fehlfänge der Kategorie `locksmith`", "",
              "Die Google-Kategorie führt in Deutschland regelmäßig Betriebe mit, die kein Schlüsseldienst sind. **Nichts davon ist "
              "entfernt worden** – die Regel des Baukastens lautet, dass keine Zeile wegen ihres Gewerbes von selbst entfernt wird. "
              "Entscheiden Sie bei Gate 4, welche Zeilen in 04-exclusions.csv wandern.", ""]
    if not misfit_hits:
        lines += ["Keine Treffer in den geprüften Gruppen (Schuhmacher, Gravur und Stickerei, Metallbau und Schlosserei, Baumärkte, "
                  "Autowerkstätten)."]
    else:
        for label in MISFITS:
            hits = misfit_hits.get(label) or []
            if not hits: continue
            lines += [f"- **{label}:** {fmt(len(hits))} {'Zeile' if len(hits) == 1 else 'Zeilen'}. Beispiele: " + "; ".join(sorted(hits)[:8]) +
                      (" ..." if len(hits) > 8 else "")]
        lines += ["", "Ein Treffer ist ein Verdacht, kein Urteil: ein Schlüsseldienst mit Schlosserei im Namen steht hier zu Recht "
                  "im Verzeichnis. Sehen Sie sich die Namen an."]
    lines += ["", f"## Namen an mehr als {a.chain_addresses} Adressen", "",
              "In dieser Branche gibt es viele Kettenbetriebe mit identischem Namen an vielen Adressen und viele Callcenter-Einträge. "
              "Die Dublettenregel (Telefon und Adresse) hat hier nichts verworfen, weil sich Adresse und Nummer unterscheiden. "
              "**Auch das ist nur ein Bericht, es wurde nichts gelöscht.**", ""]
    if not chains:
        lines += [f"Kein Name kommt an mehr als {a.chain_addresses} Adressen vor."]
    else:
        lines += ["| Name | Adressen | Städte | Zeilen |", "|---|---|---|---|"]
        lines += [f"| {e['name']} | {fmt(len(e['addr']))} | {fmt(len(e['cities']))} | {fmt(e['rows'])} |" for e in chains[:40]]
        if len(chains) > 40:
            lines += ["", f"... und {fmt(len(chains) - 40)} weitere Namen."]
    lines += ["", "## Städte nach Anzahl", ""]
    lines += [f"- {c}: {fmt(n)}" for c, n in cities.most_common()]
    rep = "\n".join(lines) + "\n"
    with open(os.path.join(os.path.dirname(a.out) or ".", "02-clean-report.md"), "w", encoding="utf-8") as f:
        f.write(rep)
    print(rep)


if __name__ == "__main__":
    main()
