#!/usr/bin/env python3
"""Festpreis-Garantie erteilen, ändern, entziehen und auflisten — der Rückweg für Anträge.

Nach einem geprüften Garantie-Antrag setzt Daniel bisher von Hand die Garantie-Spalten in
listings.csv, baut und liefert aus (wiki/framework/siegel-programm.md, [[refresh-and-upkeep]]).
Dieses Skript macht daraus einen Aufruf — nach dem Muster von scripts/verkauf.py, mit dem es die
Infrastruktur (Build-Verzeichnis finden, bauen, ausliefern, check_live.py, Sperre, Testschalter)
teilt.

    # erteilen: alle sechs Preise, Jahr optional (Vorgabe: laufendes Jahr), --bestaetigt nötig
    python3 scripts/garantie.py --slug <slug> --erteilen \\
        --tag 89 --abend 30 --nacht 40 --anfahrt 0 --zylinder 39 --zylinder5mm 3 \\
        [--jahr 2026] --bestaetigt

    # ändern: nur die genannten Preise (der Betrieb muss schon geprueft sein)
    python3 scripts/garantie.py --slug <slug> --aendern --tag 95 --nacht 45

    # entziehen: alle Garantie-Spalten leeren (eine überhöhte Rechnung, abgelaufenes Jahr)
    python3 scripts/garantie.py --slug <slug> --entziehen

    python3 scripts/garantie.py --liste

Es schreibt NUR die Garantie-Spalten (geprueft, geprueft_jahr, garantie_*); featured/premium/
best_of_rank/link_follow rührt es nie an. Vor dem Schreiben läuft die Sperre aus
scripts/_listings_guard.py.

**Die sechs Voraussetzungen** (wiki/framework/siegel-programm.md) prüft das Skript, soweit sie
aus den Daten lesbar sind, und nennt die, die Daniel von Hand bestätigen muss:
  lesbar  (2) Telefonnummer vorhanden — fehlt sie, Abbruch (die Nummer wird vor Erteilung angerufen)
  lesbar  (4) ab 5 Bewertungen Schnitt ≥ 4,0 — sonst Abbruch; bei weniger als 5 Bewertungen
              entscheiden laut Satzung die übrigen Voraussetzungen, kein Abbruch
  gesetzt (3) die sechs Preise — als Pflichtangaben beim Erteilen
  von Hand (1) vollständiges Impressum, (5) kein Callcenter ohne Ortsbezug,
              (6) unterschriebenes Serviceversprechen — mit --bestaetigt zu bestätigen

Die Schalter --kein-deploy und --kein-bauen sind nur zum Testen; im Normalbetrieb läuft die ganze
Kette (bauen, ausliefern, prüfen) mit derselben lauten Schlussmeldung wie verkauf.py.
"""
import argparse
import csv
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)

from _listings_guard import pruefe_kein_verlust
from verkauf import (
    WURZEL, truthy, ganzzahl, fehler, finde_verzeichnis, lade_csv, schreibe_csv,
    finde_zeile, _zeige_treffer, neu_bauen_ausliefern, heute,
)

import datetime as dt
import json

csv.field_size_limit(10**9)

# Die Garantie-Spalten in der Reihenfolge des Datenlayers. NUR diese schreibt das Skript.
G_FLAG = "geprueft"
G_JAHR = "geprueft_jahr"
PREIS_SPALTEN = [
    ("tag", "garantie_tag", "Grundpreis Türöffnung werktags", True),
    ("abend", "garantie_zuschlag_abend", "Zuschlag abends/Wochenende/Feiertag", False),
    ("nacht", "garantie_zuschlag_nacht", "Zuschlag nachts (0–7 Uhr)", False),
    ("anfahrt", "garantie_anfahrt", "Anfahrt", False),
    ("zylinder", "garantie_zylinder", "Standardzylinder (Material)", False),
    ("zylinder5mm", "garantie_zylinder_5mm", "Aufschlag je 5 mm Mehrlänge", False),
]
GARANTIE_SPALTEN = [G_FLAG, G_JAHR] + [s[1] for s in PREIS_SPALTEN]

HB_FELDER = ["datum", "aktion", "eintrag_slug", "jahr",
             "tag", "abend", "nacht", "anfahrt", "zylinder", "zylinder_5mm", "notiz"]


# ---------- Hauptbuch (anhängen, nie überschreiben) ----------
def lade_hauptbuch(pfad):
    if not os.path.isfile(pfad):
        return []
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def haenge_hauptbuch(pfad, zeile):
    neu = not os.path.isfile(pfad)
    with open(pfad, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HB_FELDER)
        if neu:
            w.writeheader()
        w.writerow(zeile)


def seit_wann(hb, slug):
    """Datum der jüngsten Erteilung ohne späteren Entzug, sonst None."""
    letzte = None
    for z in hb:
        if z.get("eintrag_slug") == slug:
            letzte = z
    if letzte and letzte.get("aktion") in ("erteilt", "geaendert"):
        # jüngste Erteilung suchen (nicht geaendert)
        for z in reversed(hb):
            if z.get("eintrag_slug") == slug and z.get("aktion") == "erteilt":
                return z.get("datum")
    return None


# ---------- Preis-Flags ----------
def preis_wert(flagname, roh):
    """'89' / '89,00' -> '89' (ganzzahlig wie im Datenlayer). None bleibt None (nicht gesetzt)."""
    if roh is None:
        return None
    s = str(roh).strip()
    if s == "":
        return None
    try:
        return str(int(round(float(s.replace(",", ".")))))
    except ValueError:
        fehler(f"--{flagname} '{roh}' ist keine Zahl. Preise in Euro, ganzzahlig (z. B. 89).")


# ---------- Vorprüfung der sechs Voraussetzungen ----------
def vorpruefung(r):
    """Gibt (harte_fehler[list], manuell[list], hinweise[list]). Harte Fehler => Abbruch."""
    harte, manuell, hinweise = [], [], []

    # (2) Telefonnummer vorhanden — lesbar
    if (r.get("phone") or "").strip():
        hinweise.append("(2) Telefonnummer vorhanden — vor der Erteilung anrufen, ob tatsächlich abgehoben wird.")
    else:
        harte.append("(2) Keine Telefonnummer im Eintrag. Die Nummer wird vor der Erteilung angerufen; ohne Nummer nicht erteilbar.")

    # (4) Bewertungen — lesbar, aber kein Riegel bei weniger als 5
    reviews = ganzzahl(r.get("reviews"))
    try:
        rating = float(str(r.get("rating") or "").strip().replace(",", ".")) if (r.get("rating") or "").strip() else None
    except ValueError:
        rating = None
    if reviews >= 5:
        if rating is None:
            manuell.append("(4) 5+ Bewertungen, aber kein Schnitt lesbar — Schnitt ≥ 4,0 von Hand prüfen.")
        elif rating < 4.0:
            harte.append(f"(4) {reviews} Bewertungen bei Schnitt {rating:.1f} < 4,0. Ab 5 Bewertungen ist 4,0 Pflicht.")
        else:
            hinweise.append(f"(4) {reviews} Bewertungen, Schnitt {rating:.1f} ≥ 4,0 — erfüllt.")
    else:
        hinweise.append(f"(4) nur {reviews} Bewertung(en): kein Riegel; die übrigen Voraussetzungen entscheiden (Satzung).")

    # (1)(5)(6) nicht aus den Daten lesbar
    manuell.append("(1) Vollständiges Impressum auf der eigenen Website — von Hand prüfen.")
    callcenter_hinweis = ""
    if truthy(r.get("area_service")) or not (r.get("street") or "").strip():
        callcenter_hinweis = " (Hinweis: Eintrag ohne feste Anschrift / Flächenbedienung — besonders auf Callcenter prüfen.)"
    manuell.append("(5) Keine Weiterleitung an ein Callcenter ohne Ortsbezug — von Hand prüfen." + callcenter_hinweis)
    manuell.append("(6) Unterschriebenes Serviceversprechen (fünf Zusagen) — von Hand prüfen.")
    return harte, manuell, hinweise


def zeige_vorpruefung(r, harte, manuell, hinweise):
    print(f"\nVorprüfung {r['name']} ({r['slug']}, {r.get('city') or r.get('city_slug')}):")
    for h in hinweise:
        print("  ok     " + h)
    for m in manuell:
        print("  HAND   " + m)
    for h in harte:
        print("  FEHLER " + h)


# ---------- Unterbefehle ----------
def cmd_liste(rows, hb):
    g = [r for r in rows if truthy(r.get(G_FLAG))]
    if not g:
        print("Keine Festpreis-Garantie gesetzt.")
        return
    g.sort(key=lambda r: ((r.get("city") or r.get("city_slug") or "").lower(), r["slug"]))
    print(f"Festpreis-Garantie ({len(g)}):\n")
    print(f"  {'Stadt':<16} {'Betrieb':<34} {'Jahr':<5} {'Tag':>4} {'Ab':>4} {'Na':>4} {'Anf':>4} {'Zyl':>4} {'5mm':>4}  seit")
    print("  " + "-" * 104)
    for r in g:
        stadt = (r.get("city") or r.get("city_slug") or "")[:15]
        betrieb = r["name"][:33]
        seit = seit_wann(hb, r["slug"]) or "unbekannt"
        print(f"  {stadt:<16} {betrieb:<34} {(r.get(G_JAHR) or ''):<5} "
              f"{(r.get('garantie_tag') or ''):>4} {(r.get('garantie_zuschlag_abend') or ''):>4} "
              f"{(r.get('garantie_zuschlag_nacht') or ''):>4} {(r.get('garantie_anfahrt') or ''):>4} "
              f"{(r.get('garantie_zylinder') or ''):>4} {(r.get('garantie_zylinder_5mm') or ''):>4}  {seit}")


def cmd_erteilen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    stadt = ziel.get("city") or ziel.get("city_slug")

    if truthy(ziel.get(G_FLAG)):
        fehler(f"{ziel['name']} hat in {stadt} schon die Festpreis-Garantie (Jahr {ziel.get(G_JAHR)}). "
               f"Preise ändern mit --aendern, zurücknehmen mit --entziehen.")

    # Alle sechs Preise sind beim Erteilen Pflicht (Voraussetzung 3).
    werte = {}
    fehlend = []
    for flag, spalte, _, _ in PREIS_SPALTEN:
        w = preis_wert(flag, getattr(a, flag))
        if w is None:
            fehlend.append("--" + flag)
        werte[spalte] = w
    if fehlend:
        fehler("Beim Erteilen sind alle sechs Preise Pflicht (Voraussetzung 3). Es fehlen: "
               + ", ".join(fehlend) + ".")
    if ganzzahl(werte["garantie_tag"]) <= 0:
        fehler("Der Grundpreis (--tag) muss größer als 0 sein.")

    harte, manuell, hinweise = vorpruefung(ziel)
    zeige_vorpruefung(ziel, harte, manuell, hinweise)
    if harte:
        fehler("Eine lesbare Voraussetzung ist nicht erfüllt (siehe FEHLER oben). Es wurde nichts geschrieben.")
    if not a.bestaetigt:
        fehler("Die mit HAND markierten Voraussetzungen (1, 5, 6) sind nicht aus den Daten lesbar. "
               "Bestätige sie nach der Prüfung mit --bestaetigt und ruf den Befehl erneut auf. "
               "Es wurde nichts geschrieben.")

    jahr = a.jahr or dt.date.today().year
    ziel[G_FLAG] = "true"
    ziel[G_JAHR] = str(jahr)
    for spalte, w in werte.items():
        ziel[spalte] = w
    pruefe_kein_verlust(rows, csv_pfad, erlaubt={ziel["slug"]: set(GARANTIE_SPALTEN)}, etikett=csv_pfad)
    schreibe_csv(csv_pfad, felder, rows)
    haenge_hauptbuch(hb_pfad, _hb_zeile("erteilt", ziel, jahr, a.notiz))
    print(f"\nErteilt: Festpreis-Garantie {jahr} an {ziel['name']} in {stadt}. "
          f"Türöffnung ab {werte['garantie_tag']} €. Im Hauptbuch festgehalten.")
    neu_bauen_ausliefern(a, verzeichnis, domain, projekt)


def cmd_aendern(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    stadt = ziel.get("city") or ziel.get("city_slug")
    if not truthy(ziel.get(G_FLAG)):
        fehler(f"{ziel['name']} hat in {stadt} keine Festpreis-Garantie. Zuerst --erteilen.")

    geaendert = []
    for flag, spalte, label, _ in PREIS_SPALTEN:
        w = preis_wert(flag, getattr(a, flag))
        if w is not None and w != (ziel.get(spalte) or ""):
            geaendert.append(f"{label}: {ziel.get(spalte) or '—'} → {w} €")
            ziel[spalte] = w
    if a.jahr and str(a.jahr) != (ziel.get(G_JAHR) or ""):
        geaendert.append(f"Jahr: {ziel.get(G_JAHR) or '—'} → {a.jahr}")
        ziel[G_JAHR] = str(a.jahr)
    if ganzzahl(ziel["garantie_tag"]) <= 0:
        fehler("Der Grundpreis (garantie_tag) muss größer als 0 bleiben.")
    if not geaendert:
        print(f"{ziel['name']} in {stadt}: keine Preise geändert (nichts angegeben oder gleich geblieben).")
        return
    # Ändern leert keine Spalte (nur gefüllt -> anderer Wert), die Sperre löst nicht aus; der
    # erlaubte Satz deckt es dennoch ab.
    pruefe_kein_verlust(rows, csv_pfad, erlaubt={ziel["slug"]: set(GARANTIE_SPALTEN)}, etikett=csv_pfad)
    schreibe_csv(csv_pfad, felder, rows)
    haenge_hauptbuch(hb_pfad, _hb_zeile("geaendert", ziel, ganzzahl(ziel.get(G_JAHR)), a.notiz))
    print(f"Geändert bei {ziel['name']} in {stadt}:\n  " + "\n  ".join(geaendert))
    neu_bauen_ausliefern(a, verzeichnis, domain, projekt)


def cmd_entziehen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    stadt = ziel.get("city") or ziel.get("city_slug")
    if not truthy(ziel.get(G_FLAG)):
        print(f"{ziel['name']} in {stadt} hat keine Festpreis-Garantie. Nichts zu tun.")
        return
    jahr = ganzzahl(ziel.get(G_JAHR))
    for spalte in GARANTIE_SPALTEN:
        ziel[spalte] = ""
    # Entziehen leert absichtlich die Garantie-Spalten DIESES Eintrags; alles andere (Premium,
    # Buchung, link_follow, jede fremde Garantie) muss unverändert bleiben.
    pruefe_kein_verlust(rows, csv_pfad, erlaubt={ziel["slug"]: set(GARANTIE_SPALTEN)}, etikett=csv_pfad)
    schreibe_csv(csv_pfad, felder, rows)
    haenge_hauptbuch(hb_pfad, _hb_zeile("entzogen", ziel, jahr, a.notiz))
    print(f"Entzogen: Festpreis-Garantie bei {ziel['name']} in {stadt}. "
          f"Alle Garantie-Spalten geleert, im Hauptbuch festgehalten.")
    neu_bauen_ausliefern(a, verzeichnis, domain, projekt)


def _hb_zeile(aktion, r, jahr, notiz):
    return {"datum": heute(), "aktion": aktion, "eintrag_slug": r["slug"], "jahr": str(jahr or ""),
            "tag": r.get("garantie_tag") or "", "abend": r.get("garantie_zuschlag_abend") or "",
            "nacht": r.get("garantie_zuschlag_nacht") or "", "anfahrt": r.get("garantie_anfahrt") or "",
            "zylinder": r.get("garantie_zylinder") or "", "zylinder_5mm": r.get("garantie_zylinder_5mm") or "",
            "notiz": notiz or ""}


def main():
    ap = argparse.ArgumentParser(description="Festpreis-Garantie erteilen, ändern, entziehen, auflisten.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="Slug des Eintrags (exakt oder eindeutiger Teil)")
    ap.add_argument("--erteilen", action="store_true", help="Garantie neu erteilen (alle sechs Preise, --bestaetigt)")
    ap.add_argument("--aendern", action="store_true", help="Preise einer bestehenden Garantie ändern")
    ap.add_argument("--entziehen", action="store_true", help="Garantie zurücknehmen (alle Garantie-Spalten leeren)")
    ap.add_argument("--liste", action="store_true", help="zeigt alle Betriebe mit Festpreis-Garantie und ihre Preise")
    ap.add_argument("--tag", help="Grundpreis Türöffnung werktags (€, ganzzahlig)")
    ap.add_argument("--abend", help="Zuschlag abends/Wochenende/Feiertag (€)")
    ap.add_argument("--nacht", help="Zuschlag nachts 0–7 Uhr (€)")
    ap.add_argument("--anfahrt", help="Anfahrt (€, 0 erlaubt)")
    ap.add_argument("--zylinder", help="Standardzylinder, Material (€)")
    ap.add_argument("--zylinder5mm", dest="zylinder5mm", help="Aufschlag je 5 mm Mehrlänge (€)")
    ap.add_argument("--jahr", type=int, help="Prüfjahr (Vorgabe: laufendes Jahr)")
    ap.add_argument("--bestaetigt", action="store_true",
                    help="bestätigt die von Hand geprüften Voraussetzungen (1 Impressum, 5 kein Callcenter, 6 Serviceversprechen)")
    ap.add_argument("--notiz", help="Notiz fürs Hauptbuch")
    ap.add_argument("--verzeichnis", help="Build-Verzeichnis (Vorgabe: einziges unter output/*/site/)")
    ap.add_argument("--hauptbuch", help="Pfad des Garantie-Hauptbuchs (Vorgabe: <verzeichnis>/garantie-hauptbuch.csv)")
    ap.add_argument("--projekt", help="Cloudflare-Pages-Projekt (Vorgabe: Verzeichnisname)")
    ap.add_argument("--kein-deploy", dest="kein_deploy", action="store_true", help="nur bauen, nicht ausliefern (Test)")
    ap.add_argument("--kein-bauen", dest="kein_bauen", action="store_true", help="nur CSV/Hauptbuch, nicht bauen (Test)")
    a = ap.parse_args()

    aktionen = [a.erteilen, a.aendern, a.entziehen, a.liste]
    if sum(bool(x) for x in aktionen) != 1:
        ap.error("genau eine Aktion wählen: --erteilen, --aendern, --entziehen oder --liste")
    if a.liste and a.slug:
        ap.error("--liste steht für sich allein")

    verzeichnis = finde_verzeichnis(a.verzeichnis)
    csv_pfad = os.path.join(verzeichnis, "site", "src", "data", "listings.csv")
    hb_pfad = a.hauptbuch if a.hauptbuch else os.path.join(verzeichnis, "garantie-hauptbuch.csv")
    if a.hauptbuch and not os.path.isabs(hb_pfad):
        hb_pfad = os.path.join(WURZEL, hb_pfad)
    site_json = json.load(open(os.path.join(verzeichnis, "site", "src", "data", "site.json"), encoding="utf-8"))
    domain = site_json.get("domain", "")
    projekt = a.projekt or os.path.basename(verzeichnis)

    felder, rows = lade_csv(csv_pfad)
    # Fehlende Garantie-Spalten ergänzen (Schema-Sicherheit), damit DictWriter nicht scheitert.
    for c in GARANTIE_SPALTEN:
        if c not in felder:
            felder = felder + [c]
            for r in rows:
                r.setdefault(c, "")
    hb = lade_hauptbuch(hb_pfad)

    if a.liste:
        cmd_liste(rows, hb)
        return
    if not a.slug:
        ap.error("--slug ist nötig für --erteilen, --aendern und --entziehen")
    if a.erteilen:
        cmd_erteilen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt)
    elif a.aendern:
        cmd_aendern(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt)
    elif a.entziehen:
        cmd_entziehen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt)


if __name__ == "__main__":
    main()
