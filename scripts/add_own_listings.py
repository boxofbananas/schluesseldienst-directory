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
    sechs Voraussetzungen, wie jeder andere Betrieb auch (wiki/framework/siegel-programm.md).

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
import argparse, csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PLZ_TABELLE = os.path.join(HERE, "data", "geonames-de-plz.tsv")

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

    plz_tab = lade_plz_tabelle(a.plz_tabelle)
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

        stadt_slug = slug(e["ort"])
        basis = f"{slug(e['name'])}-{stadt_slug}"
        s = basis if basis not in vorhandene_slugs else f"{basis}-{slug(e['plz'])}"
        vorhandene_slugs.add(s)

        r = {k: "" for k in spalten}
        r.update({
            "name": e["name"], "phone": e.get("telefon", ""), "website": e["website"],
            "domain": dom, "street": e["strasse"], "postal_code": e["plz"], "city": e["ort"],
            "address": f"{e['strasse']}, {e['plz']} {e['ort']}",
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
    print(f"Zeilen gesamt: {len(rows)} + {len(neu)} = {len(rows) + len(neu)}")
    print("Alle nachgetragenen Zeilen: owned=true, thin=true, ohne Bewertung, ohne Garantie.")
    if fehler:
        sys.exit(1)


if __name__ == "__main__":
    main()
