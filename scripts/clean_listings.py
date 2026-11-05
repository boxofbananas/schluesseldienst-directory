#!/usr/bin/env python3
"""Gate 2: einen Google-Maps-Export (Outscraper oder die Ausgabe von scripts/fetch_dataforseo.py)
zur Eintragsmenge des Verzeichnisses aufräumen.

Aufruf:
  python3 scripts/clean_listings.py input/listings-raw.csv \
      --category "Schlüsseldienst" \
      --out output/schluesseldienste-deutschland/02-listings-clean.csv \
      [--country Germany] [--bundesland BY] [--owned-phones 062112345,017612345] [--owned-domains meine-seite.de,andere.de] \
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
# geprueft, geprueft_jahr, garantie_tag, garantie_nacht und garantie_anfahrt gehören zur
# Festpreis-Garantie (wiki/konventionen.md, Abschnitt „Festpreis-Garantie") und werden hier leer
# angelegt; gefüllt werden sie erst, wenn der Herausgeber den Garantie-Antrag eines Betriebs
# geprüft hat. preisschutz ist die reservierte Stufe „Preisschutz": angelegt, von keinem Skript
# und keiner Seite ausgewertet, bis der Betreiber sie freigibt.
GARANTIE = ["geprueft","geprueft_jahr","garantie_tag","garantie_nacht","garantie_anfahrt","garantie_zylinder","garantie_zylinder_5mm","preisschutz"]
ADDED = ["slug","city_slug","owned","thin","featured","featured_cities","claimed","geo_precision","population"] + GARANTIE
POP_TABELLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "de-city-population.tsv")

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


# Amtliche Namenszusätze, die beim Städtevergleich wegfallen: „Frankenthal (Pfalz)",
# „Frankfurt am Main", „Neustadt an der Weinstraße", „Landau in der Pfalz", „Bergen auf Rügen",
# „Halle (Saale)", „Lindau (Bodensee)", Abkürzungen wie „a. M.", „a. d. B.", „i. OB" sowie
# nachgestellte Gebietskürzel „Westf.", „Holstein". Dient nur dem Vergleich, nicht der Anzeige.
CITY_SUFFIX = re.compile(
    r"\s*\(.*?\)\s*$"
    r"|\s+(?:a\.?\s*d\.?|an\s+der|an\s+dem|am|a\.|auf|ob|im|in\s+der|in|i\.?\s*(?:d\.?|ob|bay\.?)?)\s+\S.*$"
    r"|\s*[,/]\s*\S.*$"
    r"|\s+(?:westf|holst|holstein|oldb|rhld|thuer|saale|pfalz|bodensee)\.?\s*$", re.I)


def city_base(name):
    """Vergleichsform eines Ortsnamens ohne amtliche Zusätze und ohne Sonderzeichen."""
    s = (name or "").strip()
    for a, b in UMLAUTE:
        s = s.replace(a, b)
    prev = None
    while prev != s:
        prev = s
        s = CITY_SUFFIX.sub("", s).strip()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def load_population(path=POP_TABELLE):
    """(Bundesland-Kürzel, Ort-Grundform) -> Einwohnerzahl, aus GeoNames cities5000 (Feature P).
    Für die Mittelstadt-Regel in Gate 4/5: eine Stadt ab `cityMinPopulation` bekommt eine eigene
    Seite, auch mit nur einem Eintrag ([[site-architecture]])."""
    tab = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                t = line.rstrip("\n").split("\t")
                if len(t) >= 3 and t[2].isdigit():
                    tab[(t[0], t[1])] = int(t[2])
    except FileNotFoundError:
        return {}
    return tab


def _coord(r):
    try:
        return (float(r["latitude"]), float(r["longitude"]))
    except (TypeError, ValueError, KeyError):
        return None


def _hav(a, b):
    import math
    R = 6371
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))


def canonicalize_cities(rows, max_km=5.0):
    """Varianten derselben Stadt vereinheitlichen: gleiche Grundform (city_base) im selben
    Bundesland, die weniger als max_km auseinanderliegen, bekommen die häufigste volle
    Schreibweise. Namensnachbarn (Fürth/Wipperfürth: verschiedene Grundform) und gleichnamige
    Orte über max_km bleiben getrennt. Gibt die Zusammenführungen zurück (für den Bericht)."""
    groups = defaultdict(list)
    for r in rows:
        groups[(r.get("state_code") or "", city_base(r.get("city")))].append(r)
    merges = []
    for (code, base), rs in groups.items():
        if not base:
            continue
        clusters = []
        for r in rs:
            c = _coord(r)
            for cl in clusters:
                if c and cl["cent"] and _hav(c, cl["cent"]) < max_km:
                    cl["rows"].append(r); cl["pts"].append(c)
                    cl["cent"] = (sum(p[0] for p in cl["pts"]) / len(cl["pts"]),
                                  sum(p[1] for p in cl["pts"]) / len(cl["pts"]))
                    break
            else:
                clusters.append({"pts": [c] if c else [], "cent": c, "rows": [r]})
        for cl in clusters:
            spellings = Counter((r.get("city") or "").strip() for r in cl["rows"])
            canon = spellings.most_common(1)[0][0]
            if len(spellings) > 1:
                merges.append((code, canon, dict(spellings)))
            for r in cl["rows"]:
                r["city"] = canon
    return merges


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


def norm_domain(u):
    """Vergleichsform einer Website: nur der Hostname, klein, ohne Protokoll, ohne www und ohne
    Pfad. https://www.Schluesseldienst-Mannheim.de/kontakt -> schluesseldienst-mannheim.de, damit
    der Betreiber seine eigenen Seiten als Adresse nennen kann statt als Telefonnummer."""
    u = (u or "").strip().lower()
    if not u or u == "none":
        return ""
    u = re.sub(r"^[a-z]+://", "", u)
    u = u.split("/")[0].split("?")[0].split("#")[0].split("@")[-1].split(":")[0]
    return u[4:] if u.startswith("www.") else u


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


# --- PLZ -> Bundesland und Ort --------------------------------------------------
# DataForSEO liefert für Deutschland kein `region`-Feld; das Bundesland wird deshalb aus der
# PLZ abgeleitet (wiki/framework/listings-cleaning.md, Regel 1: „aus `state` beziehungsweise aus
# der Postleitzahl"). Dieselbe Quelle bringt den deutschen Ortsnamen und räumt damit die
# englischen Exonyme der city-Spalte (Munich, Cologne) und die leeren Städtenamen weg. Quelle:
# scripts/data/geonames-de-plz.tsv (GeoNames, CC BY 4.0; siehe scripts/data/README.md).
PLZ_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "geonames-de-plz.tsv")
CITY_FROM_ADDR = re.compile(r",\s*\d{5}\s+(.+?)\s*$")
PLZ_IN_ADDR = re.compile(r"\b(\d{5})\b")
# Stadtstaaten mit nur einer Gemeinde: ihre Ortsteile (GeoNames führt „Berlin Kreuzberg" als
# eigenen Ort) werden auf die Stadt zusammengezogen. Bremen (HB) steht NICHT hier – das Land hat
# zwei Städte, Bremen und Bremerhaven.
STADTSTAAT = {"BE": "Berlin", "HH": "Hamburg"}


def load_plz_index(path=PLZ_DATA):
    """PLZ -> Liste von (Ort, Bundesland-Kürzel) in Dateireihenfolge. None, wenn die Datei fehlt."""
    idx = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 3 and p[0]:
                    idx.setdefault(p[0], []).append((p[1], p[2]))
    except FileNotFoundError:
        return None
    return idx


def _addr_city(r):
    """Der deutsche Ortsname aus dem address-Feld (Teil nach ', PLZ '). DataForSEO schreibt die
    city-Spalte englisch (Munich), das address-Feld aber deutsch (München, …)."""
    m = CITY_FROM_ADDR.search((r.get("address") or "").strip())
    return m.group(1).split(",")[0].strip() if m else ""


def _pick_city(town, orte):
    """Der kanonische deutsche Ortsname aus den GeoNames-Orten einer PLZ, gesteuert vom Ort, den
    die Zeile mitbringt (`town`): genaue Übereinstimmung, sonst der Oberbegriff eines Ortsteils
    („Hamburg-Nord" -> „Hamburg"), sonst der häufigste bzw. kürzeste Ort der PLZ."""
    if not orte:
        return ""
    ft = fold(town)
    if ft:
        for o in orte:
            if fold(o) == ft:
                return o
        cands = [o for o in orte if fold(o) and ft.startswith(fold(o))]
        if cands:
            return max(cands, key=lambda o: len(fold(o)))
        cands = [o for o in orte if fold(o).startswith(ft)]
        if cands:
            return min(cands, key=lambda o: len(fold(o)))
    cnt = Counter(orte)
    return max(cnt, key=lambda o: (cnt[o], -len(o)))


def assign_from_plz(rows, idx):
    """Setzt state_code, state (deutscher Name aus dem Kürzel) und normalisiert city aus der PLZ.
    Eine PLZ ohne eindeutiges Bundesland (sie liegt auf einer Landesgrenze) wird über den Ort
    aufgelöst; gelingt auch das nicht, bleibt das Bundesland leer und steht im Bericht. Gibt die
    Zählung für den Bericht zurück."""
    s = {"land_set": 0, "land_resolved": 0, "land_unassigned": 0,
         "city_fixed": 0, "city_filled": 0, "plz_from_addr": 0}
    for r in rows:
        plz = (r.get("postal_code") or "").strip()
        entries = idx.get(plz, []) if idx else []
        # Fehlt die PLZ-Spalte oder kennt die Tabelle sie nicht, die erste PLZ aus dem address-Feld
        # nehmen, die die Tabelle kennt (Outscraper lässt postal_code mitunter leer).
        if not entries and idx:
            for cand in PLZ_IN_ADDR.findall(r.get("address") or ""):
                if cand in idx:
                    plz, entries = cand, idx[cand]
                    if not (r.get("postal_code") or "").strip():
                        r["postal_code"] = cand
                    s["plz_from_addr"] += 1
                    break
        orte = [o for o, _ in entries]
        town = _addr_city(r) or (r.get("city") or "").strip()
        chosen = _pick_city(town, orte)
        codes = {c for _, c in entries}
        code = ""
        if len(codes) == 1:
            code = next(iter(codes)); s["land_set"] += 1
        elif len(codes) > 1:
            for o, c in entries:
                if chosen and fold(o) == fold(chosen):
                    code = c; break
            s["land_resolved" if code else "land_unassigned"] += 1
        else:
            s["land_unassigned"] += 1
        if code:
            r["state_code"] = code
            r["state"] = NAME_BY_CODE.get(code, "")
            if code in STADTSTAAT:     # Ortsteile auf die eine Stadt des Stadtstaats ziehen
                chosen = STADTSTAAT[code]
        if chosen:
            old = (r.get("city") or "").strip()
            r["city"] = chosen
            if not old:
                s["city_filled"] += 1
            elif fold(old) != fold(chosen):
                s["city_fixed"] += 1
    return s


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
    ap.add_argument("--no-category-filter", action="store_true",
                    help="Regel 5 aussetzen: alle Zeilen behalten (der Abruf hat schon nach Kategorien "
                         "gefiltert; die Branchenprüfung folgt am Website-Rohtext, z. B. für eine breite Nachbestellung)")
    ap.add_argument("--owned-phones", default="", help="eigene Nummern, mit Komma getrennt; die Zeilen werden nur markiert")
    ap.add_argument("--owned-domains", default="",
                    help="eigene Websites, mit Komma getrennt (mit oder ohne https:// und www.); "
                         "wirkt wie --owned-phones, die Zeilen werden nur markiert")
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
    owned = {norm_phone(p) for p in a.owned_phones.split(",") if p.strip()} - {""}
    owned_domains = {norm_domain(d) for d in a.owned_domains.split(",") if d.strip()} - {""}
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

    # Bundesland aus der PLZ ableiten und die Städtenamen auf Deutsch bringen (siehe oben).
    plz_idx = load_plz_index()
    if plz_idx is None:
        notes.append(f"Die PLZ-Tabelle `{os.path.relpath(PLZ_DATA)}` fehlt, deshalb wurde das Bundesland "
                     "**nicht** aus der PLZ abgeleitet und die Städtenamen blieben unverändert (siehe "
                     "scripts/data/README.md, wie die Datei neu bezogen wird).")
        plz_stats = None
    else:
        plz_stats = assign_from_plz(rows, plz_idx)

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
        elif a.no_category_filter:
            r["_match"] = "keep-all"; kept.append(r)
    rows = kept
    steps.append(("Treffer über Name oder Kategorie" if not a.no_category_filter
                  else "ohne Kategorie-Filter (alle Kategorien behalten, Filter folgt per fetch_sites)", len(rows)))

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

    # Ortsnamen vereinheitlichen (amtliche Zusätze, Varianten derselben Stadt unter 5 km).
    city_merges = canonicalize_cities(rows)
    pop_tab = load_population()
    if city_merges:
        bsp = "; ".join(f"{canon} ← {', '.join(k for k in sp if k != canon)}" for _, canon, sp in city_merges[:12])
        notes.append(f"Ortsnamen vereinheitlicht: {len(city_merges)} Städte mit mehreren Schreibweisen "
                     f"zusammengeführt (gleiche Grundform, unter 5 km). {bsp}" + (" …" if len(city_merges) > 12 else ""))

    slugs = Counter()
    for r in rows:
        r["city_slug"] = slug(r.get("city"))
        base = f"{slug(r.get('name'))}-{r['city_slug']}"
        slugs[base] += 1
        r["slug"] = base if slugs[base] == 1 else f"{base}-{slug(r.get('postal_code'))}"
        # Eigener Betrieb, wenn die Telefonnummer oder die Website passt. Die Spalte dient nur
        # dem Bericht und darf die Darstellung nie veraendern (wiki/framework/footprint-rules.md).
        eigene_nummer = bool(owned) and norm_phone(r.get("phone")) in owned
        host = norm_domain(r.get("domain") or r.get("website"))
        eigene_domain = bool(owned_domains) and host in owned_domains
        r["owned"] = "true" if (eigene_nummer or eigene_domain) else "false"
        r["thin"] = "true" if (to_int(r.get("reviews")) < a.thin_reviews or not has_text(r)) else "false"
        r["website"] = clean_url(r.get("website"))
        r["featured"] = ""; r["featured_cities"] = ""; r["claimed"] = ""
        # Herkunft/Güte der Koordinate: DataForSEO-Zeilen tragen den echten Geopunkt des Betriebs.
        # Nachgetragene eigene Betriebe setzen das in add_own_listings.py auf "exact" (geokodiert)
        # oder "plz" (PLZ-Mittelpunkt → auf der Eintragsseite Ortsfläche statt Nadel).
        r["geo_precision"] = "exact" if ((r.get("latitude") or "").strip() and (r.get("longitude") or "").strip()) else ""
        # Einwohnerzahl der Stadt (GeoNames) für die Mittelstadt-Regel; leer, wenn nicht gematcht.
        r["population"] = str(pop_tab.get((r.get("state_code") or "", city_base(r.get("city"))), "") or "")
        for c in GARANTIE: r[c] = ""

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KEEP + ADDED, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

    # Website-Domains der behaltenen Zeilen, eine je Zeile, für den Emails-&-Contacts-Scraper von
    # Outscraper (nur auf der aufgeräumten Liste laufen lassen).
    domains = sorted({d for d in (site_domain(r.get("website")) for r in rows) if d})
    dom_path = os.path.join(os.path.dirname(a.out) or ".", "02-domains.txt")
    with open(dom_path, "w", encoding="utf-8") as f:
        f.write("\n".join(domains) + ("\n" if domains else ""))

    if plz_stats is not None:
        zugeordnet = sum(1 for r in rows if (r.get("state_code") or "").strip())
        notes.append(
            f"Bundesland aus der PLZ abgeleitet (`{os.path.relpath(PLZ_DATA)}`, GeoNames): "
            f"{fmt(zugeordnet)} der {fmt(len(rows))} behaltenen Zeilen haben ein Bundesland, "
            f"{fmt(len(rows) - zugeordnet)} bleiben „(ohne Angabe)“ und stehen in der Bundesland-Tabelle. "
            f"Städtenamen auf Deutsch normalisiert: {fmt(plz_stats['city_fixed'])} Exonyme ersetzt "
            f"(Munich -> München), {fmt(plz_stats['city_filled'])} leere city gefüllt; "
            f"{fmt(plz_stats['land_resolved'])} PLZ auf einer Landesgrenze über den Ort aufgelöst, "
            f"{fmt(plz_stats['plz_from_addr'])} PLZ aus dem address-Feld nachgezogen (postal_code war leer) "
            f"(Zählung über alle Zeilen mit PLZ vor dem Entdoppeln).")

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
              f"**Neue, leere Spalten:** `geprueft`, `geprueft_jahr`, `garantie_tag`, `garantie_nacht`, `garantie_anfahrt` "
              "(Dienstleistungspreise der Festpreis-Garantie), `garantie_zylinder`, `garantie_zylinder_5mm` "
              "(Materialpreis bei abgeschlossener Tür, wiki/konventionen.md) und `preisschutz` (reservierte Stufe, nicht ausgewertet)",
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
