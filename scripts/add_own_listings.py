#!/usr/bin/env python3
"""Gate 2 Nachtrag: eigene Betriebe aufnehmen, die im Google-Abruf fehlen.

Der Abruf holt nur Betriebe mit mindestens einer oeffentlichen Bewertung. Betriebe ohne
Unternehmensprofil oder mit gesperrtem Profil tauchen darin nicht auf. Dieses Skript traegt
sie aus einer von Hand gepflegten Datei nach.

Was ein nachgetragener Eintrag bekommt und was nicht:
  - `owned=true`, damit der Bericht ihn zeigt. Die Spalte veraendert die Darstellung nie
    (wiki/framework/footprint-rules.md).
  - **Keine Bewertung und keine Bewertungszahl.** Es gibt keine, also steht da auch keine.
    Eine erfundene Bewertung waere eine Taeuschung des Lesers und wuerde das ganze
    Verzeichnis entwerten.
  - `thin=true`. Der Eintrag ist sichtbar und verlinkt, steht aber zum Start nicht in der
    Sitemap (wiki/seo/launch-lean.md). Sobald der Betrieb ein Profil mit Bewertungen hat,
    holt ihn der naechste Abruf mit echten Daten; dann faellt der Nachtrag weg.
  - **Keine Festpreis-Garantie.** Die bekommt er nur ueber den Antrag und die Pruefung der
    Voraussetzungen, wie jeder andere Betrieb auch (wiki/framework/siegel-programm.md).
  - **Koordinaten** aus Nominatim (Strasse + PLZ + Ort), sonst PLZ-Mittelpunkt aus dem
    GeoNames-Datensatz. Die Spalte `geo_precision` haelt fest, ob exakt oder PLZ-Mittelpunkt;
    PLZ-Mittelpunkte zeigen auf der Eintragsseite die Ortsflaeche statt einer Punktnadel.

Aufruf:
  python3 scripts/add_own_listings.py output/<slug>/02-listings-clean.csv \\
      --eigene input/eigene-betriebe.csv --out output/<slug>/02-listings-clean.csv

Die Eingabedatei `input/eigene-betriebe.csv` hat diese Spalten (Kopfzeile noetig):
  name, strasse, plz, ort, telefon, website         Pflicht (telefon darf leer sein)
  bundesland                                        wenn die PLZ-Tabelle fehlt
  leistungen                                        optional, Freitext fuer Gate 3

Doppelte werden uebersprungen: steht derselbe Betrieb schon ueber Telefonnummer oder Website
in der bereinigten Datei, bleibt die echte Zeile stehen und der Nachtrag entfaellt.
"""
import argparse, csv, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:    # dieselbe Ortsnamen-Normalisierung wie in Gate 2, damit eigene Einträge die
    from clean_listings import city_base, _coord, _hav, load_population   # Scrape-Schreibweise übernehmen
except Exception:   # pragma: no cover
    city_base = None
    def load_population(*_a, **_k): return {}
PLZ_TABELLE = os.path.join(HERE, "data", "geonames-de-plz.tsv")

# Geokodierung über Nominatim (OpenStreetMap). Die Nutzungsregeln verlangen einen eigenen
# User-Agent und höchstens eine Anfrage je Sekunde. Scheitert die Anfrage, fällt das Skript auf
# den PLZ-Mittelpunkt aus dem GeoNames-Datensatz zurück (Spalte `geo_precision` = "plz"); solche
# Einträge zeigen auf der Eintragsseite die Ortsfläche statt einer Punktnadel.
NOMINATIM = "https://nominatim.openstreetmap.org/search"
NOMINATIM_UA = "die-besten-schluesseldienste.de Verzeichnis-Bot (DOM Holding GmbH; Kontakt im Impressum)"
_last_call = [0.0]


def geocode_nominatim(strasse, plz, ort):
    """Exakte Koordinate zu Straße + PLZ + Ort oder None. Hält 1 Anfrage/Sekunde ein."""
    q = urllib.parse.urlencode({"street": strasse, "postalcode": plz, "city": ort,
                                "country": "Deutschland", "format": "json", "limit": 1})
    wait = 1.0 - (time.monotonic() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.monotonic()
    try:
        req = urllib.request.Request(f"{NOMINATIM}?{q}",
                                     headers={"User-Agent": NOMINATIM_UA, "Accept-Language": "de"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None
    return None


def lade_plz_koordinaten(pfad):
    """PLZ -> Mittelpunkt (lat, lon) aus dem GeoNames-Datensatz (Spalten 4 und 5), als Rückfall."""
    if not os.path.isfile(pfad):
        return {}
    acc = {}
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            t = zeile.rstrip("\n").split("\t")
            if len(t) < 5:
                continue
            try:
                acc.setdefault(t[0].strip(), []).append((float(t[3]), float(t[4])))
            except ValueError:
                continue
    return {p: (sum(x[0] for x in v) / len(v), sum(x[1] for x in v) / len(v)) for p, v in acc.items()}

BUNDESLAENDER = {
    "baden-wuerttemberg": "BW", "baden-württemberg": "BW", "bayern": "BY", "berlin": "BE",
    "brandenburg": "BB", "bremen": "HB", "hamburg": "HH", "hessen": "HE",
    "mecklenburg-vorpommern": "MV", "niedersachsen": "NI", "nordrhein-westfalen": "NW",
    "rheinland-pfalz": "RP", "saarland": "SL", "sachsen": "SN", "sachsen-anhalt": "ST",
    "schleswig-holstein": "SH", "thueringen": "TH", "thüringen": "TH",
}
CODE_NAME = {"BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg",
             "HB": "Bremen", "HH": "Hamburg", "HE": "Hessen", "MV": "Mecklenburg-Vorpommern",
             "NI": "Niedersachsen", "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz",
             "SL": "Saarland", "SN": "Sachsen", "ST": "Sachsen-Anhalt",
             "SH": "Schleswig-Holstein", "TH": "Thüringen"}
UMLAUTE = [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")]


def slug(s):
    """Wie in clean_listings.py: Umlaute umschreiben, bevor Sonderzeichen entfernt werden."""
    s = s or ""
    for a, b in UMLAUTE:
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "x"


def norm_phone(p):
    d = re.sub(r"\D", "", p or "")
    if d.startswith("0049"):
        d = d[4:]
    elif d.startswith("49") and len(d) > 10:
        d = d[2:]
    d = d.lstrip("0")
    return d[-10:] if len(d) >= 10 else d


def norm_domain(u):
    u = (u or "").strip().lower()
    if not u or u == "none":
        return ""
    u = re.sub(r"^[a-z]+://", "", u)
    u = u.split("/")[0].split("?")[0].split("#")[0].split("@")[-1].split(":")[0]
    return u[4:] if u.startswith("www.") else u


def lade_plz_tabelle(pfad):
    """GeoNames-Auszug: Postleitzahl -> Bundesland-Name. Fehlt die Datei, wird die Spalte
    `bundesland` der Eingabedatei verlangt."""
    if not os.path.isfile(pfad):
        return {}
    tab = {}
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            teile = zeile.rstrip("\n").split("\t")
            if len(teile) < 4:
                continue
            plz = teile[1].strip() if teile[0].strip().upper() == "DE" else teile[0].strip()
            land = next((t for t in teile[2:6] if t.strip() and not t.strip().isdigit()), "")
            if re.fullmatch(r"\d{5}", plz) and land:
                tab.setdefault(plz, land.strip())
    return tab


def bundesland_von(zeile, plz_tab):
    """Bundesland aus der Spalte, sonst aus der Postleitzahl. Gibt (Name, Kuerzel) zurueck."""
    roh = (zeile.get("bundesland") or "").strip()
    if not roh:
        roh = plz_tab.get((zeile.get("plz") or "").strip(), "")
    if not roh:
        return "", ""
    code = BUNDESLAENDER.get(roh.lower()) or (roh.upper() if roh.upper() in CODE_NAME else "")
    return (CODE_NAME.get(code, roh), code)


def main():
    ap = argparse.ArgumentParser(description="Eigene Betriebe in die bereinigte Liste nachtragen.")
    ap.add_argument("clean_csv", help="output/<slug>/02-listings-clean.csv aus Gate 2")
    ap.add_argument("--eigene", required=True, help="input/eigene-betriebe.csv")
    ap.add_argument("--out", required=True, help="Zieldatei; darf dieselbe sein wie clean_csv")
    ap.add_argument("--plz-tabelle", default=PLZ_TABELLE)
    ap.add_argument("--no-geocode", action="store_true",
                    help="Nominatim überspringen und nur den PLZ-Mittelpunkt verwenden (Offline/Test)")
    a = ap.parse_args()

    for pfad in (a.clean_csv, a.eigene):
        if not os.path.isfile(pfad):
            sys.exit(f"FEHLER: {pfad} gibt es nicht.")

    with open(a.clean_csv, encoding="utf-8", newline="") as f:
        leser = csv.DictReader(f)
        spalten = leser.fieldnames or []
        rows = list(leser)
    if not spalten:
        sys.exit(f"FEHLER: {a.clean_csv} hat keine Kopfzeile.")

    # Was schon da ist, wird nicht noch einmal angelegt.
    vorhandene_tel = {norm_phone(r.get("phone")) for r in rows} - {""}
    vorhandene_dom = {norm_domain(r.get("domain") or r.get("website")) for r in rows} - {""}
    vorhandene_slugs = {r.get("slug") for r in rows}

    # Vorhandene Städte je (Bundesland, Grundform) mit Schreibweise, Slug und Koordinate, damit ein
    # eigener Eintrag die Scrape-Schreibweise seiner Stadt übernimmt (Frankenthal -> wie im Scrape).
    stadt_index = defaultdict(list)
    if city_base:
        for r in rows:
            stadt_index[(r.get("state_code") or "", city_base(r.get("city")))].append(
                (r.get("city"), r.get("city_slug"), _coord(r)))

    plz_tab = lade_plz_tabelle(a.plz_tabelle)
    plz_coords = lade_plz_koordinaten(a.plz_tabelle)
    pop_tab = load_population()
    stadt_angeglichen = []
    with open(a.eigene, encoding="utf-8-sig", newline="") as f:
        eigene = list(csv.DictReader(f))
    if not eigene:
        sys.exit(f"FEHLER: {a.eigene} enthält keine Zeilen.")

    pflicht = ("name", "strasse", "plz", "ort", "website")
    neu, uebersprungen, fehler = [], [], []
    for i, e in enumerate(eigene, start=2):
        e = {(k or "").strip().lower(): (v or "").strip() for k, v in e.items()}
        fehlt = [s for s in pflicht if not e.get(s)]
        if fehlt:
            fehler.append(f"Zeile {i}: es fehlt {', '.join(fehlt)}")
            continue
        land_name, land_code = bundesland_von(e, plz_tab)
        if not land_code:
            fehler.append(f"Zeile {i} ({e['name']}): Bundesland nicht bestimmbar. "
                          f"Spalte `bundesland` füllen oder die PLZ-Tabelle bereitstellen.")
            continue
        tel, dom = norm_phone(e.get("telefon")), norm_domain(e.get("website"))
        if (tel and tel in vorhandene_tel) or (dom and dom in vorhandene_dom):
            uebersprungen.append(f"{e['name']} ({e['ort']}) steht bereits mit echten Daten in der Liste")
            continue

        # Koordinate: erst Nominatim (exakt), sonst PLZ-Mittelpunkt (Ortsfläche).
        lat = lon = prec = ""
        g = None if a.no_geocode else geocode_nominatim(e["strasse"], e["plz"], e["ort"])
        if g:
            lat, lon, prec = f"{g[0]:.6f}", f"{g[1]:.6f}", "exact"
        elif e["plz"] in plz_coords:
            c = plz_coords[e["plz"]]
            lat, lon, prec = f"{c[0]:.5f}", f"{c[1]:.5f}", "plz"

        # Stadt an die Scrape-Schreibweise angleichen: gleiche Grundform im selben Bundesland,
        # weniger als 5 km entfernt. Sonst die eigene Schreibweise.
        stadt_name, stadt_slug = e["ort"], slug(e["ort"])
        oc = (float(lat), float(lon)) if lat and lon else None
        if city_base:
            key = (land_code, city_base(e["ort"]))
            treffer = [(cy, cs) for cy, cs, co in stadt_index.get(key, []) if oc and co and _hav(oc, co) < 5]
            if treffer:
                cy, cs = Counter(treffer).most_common(1)[0][0]
                if cy and (cy, cs) != (stadt_name, stadt_slug):
                    stadt_angeglichen.append(f"{e['ort']} → {cy}")
                    stadt_name, stadt_slug = cy, cs

        basis = f"{slug(e['name'])}-{stadt_slug}"
        s = basis if basis not in vorhandene_slugs else f"{basis}-{slug(e['plz'])}"
        vorhandene_slugs.add(s)

        r = {k: "" for k in spalten}
        r.update({
            "name": e["name"], "phone": e.get("telefon", ""), "website": e["website"],
            "domain": dom, "street": e["strasse"], "postal_code": e["plz"], "city": stadt_name,
            "address": f"{e['strasse']}, {e['plz']} {stadt_name}",
            "latitude": lat, "longitude": lon, "geo_precision": prec,
            "population": str(pop_tab.get((land_code, city_base(stadt_name)), "") or "") if city_base else "",
            "state": land_name, "state_code": land_code,
            "country": "Germany", "country_code": "DE",
            "type": "Schlüsseldienst", "category": "Schlüsseldienst",
            "description": e.get("leistungen", ""),
            "business_status": "OPERATIONAL", "verified": "false",
            # Bewusst leer: rating, reviews und jede Bewertungsverteilung. Es gibt keine.
            "rating": "", "reviews": "",
            "source": "eigene-betriebe",
            "slug": s, "city_slug": stadt_slug,
            "owned": "true", "thin": "true",
            "featured": "", "featured_cities": "", "claimed": "",
            "geprueft": "", "geprueft_jahr": "",
            "garantie_tag": "", "garantie_nacht": "", "garantie_anfahrt": "", "preisschutz": "",
        })
        neu.append({k: r.get(k, "") for k in spalten})

    if fehler:
        print("Nicht übernommen:")
        for z in fehler:
            print("  -", z)
        print()
    if not neu:
        sys.exit("Keine Zeile zum Nachtragen übrig. Nichts geschrieben.")

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=spalten)
        w.writeheader()
        w.writerows(rows + neu)

    nach_land = {}
    for r in neu:
        nach_land[r["state"]] = nach_land.get(r["state"], 0) + 1
    print(f"Nachgetragen: {len(neu)} eigene Betriebe in {os.path.relpath(a.out)}")
    for land, n in sorted(nach_land.items(), key=lambda kv: -kv[1]):
        print(f"  {land}: {n}")
    for z in uebersprungen:
        print("  übersprungen:", z)
    exact = sum(1 for r in neu if r.get("geo_precision") == "exact")
    plzc = sum(1 for r in neu if r.get("geo_precision") == "plz")
    ohne = len(neu) - exact - plzc
    print(f"Zeilen gesamt: {len(rows)} + {len(neu)} = {len(rows) + len(neu)}")
    print(f"Koordinaten: {exact} exakt (Nominatim), {plzc} PLZ-Mittelpunkt, {ohne} ohne")
    if stadt_angeglichen:
        print(f"Stadt an Scrape-Schreibweise angeglichen ({len(stadt_angeglichen)}): " + "; ".join(stadt_angeglichen))
    print("Alle nachgetragenen Zeilen: owned=true, thin=true, ohne Bewertung, ohne Garantie.")
    if fehler:
        sys.exit(1)


if __name__ == "__main__":
    main()
