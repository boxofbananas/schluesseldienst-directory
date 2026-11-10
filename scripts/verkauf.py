#!/usr/bin/env python3
"""Verkaufte Plätze setzen, entfernen und auflisten — ein Befehl statt Handarbeit.

Nach einer Stripe-Zahlung setzt Daniel bisher von Hand die Spalte in listings.csv, baut und
liefert aus (wiki/framework/monetization-slots.md, templates/featured-tiers.md). Dieses Skript
macht daraus einen Aufruf: Spalte setzen, Verkauf im Hauptbuch festhalten, bauen, ausliefern,
check_live.py.

    python3 scripts/verkauf.py --slug <eintrag-slug> --stufe premium|stadt|top
    python3 scripts/verkauf.py --slug <eintrag-slug> --entfernen [--stufe ...]
    python3 scripts/verkauf.py --liste

Die drei Stufen entsprechen den Stripe-Produkten. WELCHE SPALTE welche Stufe setzt, steht im
Datenlayer (templates/astro/src/lib/load.mjs), nicht in dieser Datei fest verdrahtet — die Werte
hier spiegeln ihn nur:

    premium  Premium-Eintrag   97 € im Jahr     -> Spalte `premium`       = true
    stadt    Stadt-Premium     29 € im Monat    -> Spalte `featured`      = city   (je Stadt einmal)
    top      Top-Platzierung   250 € einmalig   -> Spalte `best_of_rank`  = 1..3

Die Garantie-Spalten (geprueft, geprueft_jahr, garantie_*) rührt das Skript NIE an.

Zwei Prüfungen brechen ab, sie warnen nicht:
  1. Stadt-Premium ist je Stadt nur einmal vergeben. Ist er belegt, Abbruch mit dem Halter.
  2. Höchstens ein eigener (owned) Betrieb je Stadt auf einem bezahlten Platz
     (wiki/framework/footprint-rules.md). Derselbe eigene Betrieb darf mehrere Stufen halten;
     ein ZWEITER eigener Betrieb mit bezahltem Platz in derselben Stadt bricht ab.
Ein Slug, der auf keine oder mehrere Zeilen passt, bricht ab und zeigt die Treffer. Nie raten.

Die Schalter --kein-deploy und --kein-bauen sind nur zum Testen; im Normalbetrieb läuft die
ganze Kette.
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

csv.field_size_limit(10**9)

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)

# Spiegelt load.mjs: truthy akzeptiert genau diese Formen.
_TRUTHY = re.compile(r"^(true|wahr|ja|yes|1|y|j)$", re.I)


def truthy(v):
    return bool(_TRUTHY.match(str(v or "").strip()))


def ganzzahl(v):
    try:
        return int(round(float(str(v).strip().replace(",", "."))))
    except (ValueError, AttributeError):
        return 0


# Stufe -> (Spalte, Setzwert oder None wenn berechnet, Anzeigename, Schlüssel in site.json.tiers)
STUFEN = {
    "premium": ("premium", "true", "Premium-Eintrag", "premium"),
    "stadt": ("featured", "city", "Stadt-Premium", "city"),
    "top": ("best_of_rank", None, "Top-Platzierung", "bestOf"),
}
# Anzeige von featured-Werten, die der Build kennt (county/state sind spätere Stufen).
FEATURED_NAME = {"city": "Stadt-Premium", "county": "Landkreis-Premium", "state": "Bundesland-Premium"}


def fehler(msg):
    print("ABBRUCH: " + msg, file=sys.stderr)
    sys.exit(1)


def finde_verzeichnis(arg):
    if arg:
        d = arg if os.path.isabs(arg) else os.path.join(WURZEL, arg)
        if not os.path.isfile(os.path.join(d, "site", "src", "data", "listings.csv")):
            fehler(f"in {d} liegt keine site/src/data/listings.csv")
        return d
    treffer = sorted(glob.glob(os.path.join(WURZEL, "output", "*", "site", "src", "data", "listings.csv")))
    if len(treffer) == 1:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(treffer[0]))))
    if not treffer:
        fehler("kein Build-Verzeichnis unter output/*/site/ gefunden; --verzeichnis angeben")
    fehler("mehrere Build-Verzeichnisse gefunden, --verzeichnis angeben:\n  " +
           "\n  ".join(os.path.relpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(t)))), WURZEL) for t in treffer))


def lade_csv(pfad):
    with open(pfad, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def schreibe_csv(pfad, felder, rows):
    tmp = pfad + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, pfad)


def finde_zeile(rows, slug):
    """Exakter Slug hat Vorrang; sonst Teiltreffer. Gibt (zeile, treffer_bei_misserfolg)."""
    slug = slug.strip()
    exakt = [r for r in rows if r["slug"] == slug]
    if len(exakt) == 1:
        return exakt[0], None
    low = slug.lower()
    teil = [r for r in rows if low in r["slug"].lower()]
    if len(teil) == 1:
        return teil[0], None
    return None, teil  # 0 oder mehrere


def hat_bezahlten_platz(r):
    return truthy(r.get("premium")) or (r.get("featured") or "").strip() != "" or ganzzahl(r.get("best_of_rank")) > 0


def aktive_stufen(r):
    """Liste (stufen_schluessel_oder_None, anzeigename, spaltenwert) der aktiven bezahlten Plätze."""
    out = []
    if truthy(r.get("premium")):
        out.append(("premium", "Premium-Eintrag", "true"))
    fv = (r.get("featured") or "").strip().lower()
    if fv:
        schluessel = "stadt" if fv == "city" else None
        out.append((schluessel, FEATURED_NAME.get(fv, f"featured={fv}"), fv))
    if ganzzahl(r.get("best_of_rank")) > 0:
        out.append(("top", "Top-Platzierung", str(ganzzahl(r.get("best_of_rank")))))
    return out


# ---------- Hauptbuch ----------
HB_FELDER = ["datum", "aktion", "eintrag_slug", "stufe", "stadt", "preis"]


def lade_hauptbuch(pfad):
    if not os.path.isfile(pfad):
        return []
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def haenge_hauptbuch(pfad, zeilen):
    neu = not os.path.isfile(pfad)
    with open(pfad, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HB_FELDER)
        if neu:
            w.writeheader()
        for z in zeilen:
            w.writerow(z)


def seit_wann(hb, slug, stufe):
    """Datum des jüngsten offenen Verkaufs (kein späteres Ende) für slug+stufe, sonst None."""
    letzte = None
    for z in hb:
        if z.get("eintrag_slug") == slug and z.get("stufe") == stufe:
            letzte = z
    if letzte and letzte.get("aktion") == "verkauf":
        return letzte.get("datum")
    return None


# ---------- Bauen / Ausliefern / Prüfen ----------
def baue(verzeichnis):
    site = os.path.join(verzeichnis, "site")
    print("  bauen (npm run build) ...")
    r = subprocess.run(["npm", "run", "build"], cwd=site, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:], file=sys.stderr)
        fehler("npm run build ist fehlgeschlagen; es wurde nichts ausgeliefert")
    if re.search(r"\b(warn|fehlende Daten|missing)\b", r.stdout, re.I):
        for line in r.stdout.splitlines():
            if re.search(r"\b(warn|fehlende Daten|missing)\b", line, re.I):
                print("  WARNUNG beim Bauen:", line.strip())


def sitemap_zahl(verzeichnis):
    n = 0
    for p in glob.glob(os.path.join(verzeichnis, "site", "dist", "**", "sitemap*.xml"), recursive=True):
        n += open(p, encoding="utf-8").read().count("<url>")
    return n


def liefere_aus(verzeichnis, projekt):
    site = os.path.join(verzeichnis, "site")
    print(f"  ausliefern (wrangler pages deploy, Projekt {projekt}) ...")
    r = subprocess.run(["npx", "wrangler", "pages", "deploy", "dist", f"--project-name={projekt}"],
                       cwd=site, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-2000:], file=sys.stderr)
        fehler("wrangler pages deploy ist fehlgeschlagen")


def pruefe_live(verzeichnis, domain, erwartet):
    print(f"  prüfen (check_live.py {domain}, erwartet {erwartet} Adressen) ...")
    cmd = [sys.executable, os.path.join(HIER, "check_live.py"), f"https://{domain}"]
    if erwartet:
        cmd += ["--expect-urls", str(erwartet)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-2000:], file=sys.stderr)
        fehler("check_live.py meldet einen Fehler an der Live-Seite")


_BANNER = "═" * 70


def banner_nicht_ausgeliefert(grund):
    print("\n" + _BANNER)
    print("  ⚠  NICHT AUSGELIEFERT — die Live-Seite ist UNVERÄNDERT.")
    print(f"     {grund}")
    print("     Die CSV und das Hauptbuch wurden lokal geändert; es ging NICHTS zu")
    print("     Cloudflare, und check_live.py lief nicht. Ohne diese Schalter läuft")
    print("     die ganze Kette (bauen, ausliefern, prüfen).")
    print(_BANNER)


def neu_bauen_ausliefern(a, verzeichnis, domain, projekt):
    if a.kein_bauen:
        banner_nicht_ausgeliefert("--kein-bauen gesetzt: weder gebaut noch ausgeliefert.")
        return
    baue(verzeichnis)
    if a.kein_deploy:
        banner_nicht_ausgeliefert("--kein-deploy gesetzt: lokal gebaut, aber nicht ausgeliefert.")
        return
    liefere_aus(verzeichnis, projekt)
    pruefe_live(verzeichnis, domain, sitemap_zahl(verzeichnis))


# ---------- Unterbefehle ----------
def melde_fehlende_buchungsdaten(rows):
    """Meldet jedes Stadt-Premium ohne featured_seit — nicht stillschweigend ans Ende sortieren."""
    ohne = [r for r in rows if (r.get("featured") or "").strip().lower() == "city"
            and not (r.get("featured_seit") or "").strip()]
    if ohne:
        print("\nMELDUNG: Stadt-Premium ohne Buchungsdatum (featured_seit). Die Reihenfolge im "
              "Band ist für diese Einträge nicht bestimmbar:", file=sys.stderr)
        for r in ohne:
            print(f"  {r['slug']}  ({r['name']}, {r.get('city') or r['city_slug']})", file=sys.stderr)
        print("Das Datum setzt `--slug <...> --stufe stadt` (neue Buchung) oder ein Eintrag von "
              "Hand in die Spalte featured_seit (JJJJ-MM-TT).", file=sys.stderr)
    return ohne


def cmd_liste(rows, hb):
    aktiv = []
    for r in rows:
        for schluessel, name, wert in aktive_stufen(r):
            seit = seit_wann(hb, r["slug"], schluessel) if schluessel else None
            aktiv.append((r.get("city") or r.get("city_slug"), name, r["name"], r["slug"], wert, seit,
                          truthy(r.get("owned"))))
    if not aktiv:
        print("Kein bezahlter Platz gesetzt.")
        return
    aktiv.sort(key=lambda x: (x[0].lower(), x[1], x[5] or "9999-99-99", x[3]))
    print(f"Bezahlte Plätze ({len(aktiv)}):\n")
    print(f"  {'Stadt':<18} {'Stufe':<20} {'Betrieb':<40} {'seit':<11} Eintrag")
    print("  " + "-" * 110)
    for stadt, name, betrieb, slug, wert, seit, owned in aktiv:
        seit_s = seit or "unbekannt"
        marke = " (eigen)" if owned else ""
        wert_s = f" [rang {wert}]" if name == "Top-Platzierung" else ""
        betrieb_disp = (betrieb[:30] + ("…" if len(betrieb) > 30 else "") + marke)
        print(f"  {stadt:<18} {(name+wert_s):<20} {betrieb_disp:<42} {seit_s:<11} {slug}")
    melde_fehlende_buchungsdaten(rows)


def cmd_verkauf(a, rows, felder, csv_pfad, hb, hb_pfad, tiers, verzeichnis, domain, projekt):
    stufe = a.stufe
    spalte, setzwert, name, _ = STUFEN[stufe]
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    stadt = ziel["city_slug"]
    stadt_anzeige = ziel.get("city") or stadt

    # Schon verkauft?
    for schluessel, aname, _ in aktive_stufen(ziel):
        if schluessel == stufe:
            seit = seit_wann(hb, ziel["slug"], stufe)
            print(f"{ziel['name']} hält {name} in {stadt_anzeige} bereits"
                  + (f" (seit {seit})" if seit else "") + ". Nichts zu tun.")
            return

    # Prüfung 1: Stadt-Premium gibt es bis zu dreimal je Stadt. Die Sperre greift erst ab dem
    # vierten und nennt dann die drei Halter.
    if stufe == "stadt":
        halter = [r for r in rows if r["city_slug"] == stadt and r["slug"] != ziel["slug"]
                  and (r.get("featured") or "").strip().lower() == "city"]
        if len(halter) >= 3:
            wer = "; ".join(f"{h['name']} ({h['slug']}, seit {h.get('featured_seit') or '?'})"
                            for h in halter)
            fehler(f"Alle drei Stadt-Premium-Plätze in {stadt_anzeige} sind vergeben an: {wer}. "
                   f"Erst einen entfernen, dann hier verkaufen.")

    # Prüfung 2: höchstens ein eigener Betrieb je Stadt auf bezahltem Platz.
    if truthy(ziel.get("owned")):
        andere = [r for r in rows if r["city_slug"] == stadt and r["slug"] != ziel["slug"]
                  and truthy(r.get("owned")) and hat_bezahlten_platz(r)]
        if andere:
            h = andere[0]
            fehler(f"In {stadt_anzeige} hält schon der eigene Betrieb {h['name']} ({h['slug']}) einen "
                   f"bezahlten Platz. Höchstens ein eigener Betrieb je Stadt (footprint-rules.md). "
                   f"{ziel['name']} ist ebenfalls ein eigener Betrieb — Abbruch.")

    # Top-Platzierung: nächsten freien Rang 1..3 in der Stadt bestimmen.
    if stufe == "top":
        belegt = {ganzzahl(r.get("best_of_rank")) for r in rows
                  if r["city_slug"] == stadt and r["slug"] != ziel["slug"] and ganzzahl(r.get("best_of_rank")) > 0}
        frei = [n for n in (1, 2, 3) if n not in belegt]
        if not frei:
            wer = ", ".join(f"Rang {ganzzahl(r['best_of_rank'])}: {r['name']}" for r in rows
                            if r["city_slug"] == stadt and ganzzahl(r.get("best_of_rank")) > 0)
            fehler(f"Alle drei Top-Plätze in {stadt_anzeige} sind belegt ({wer}). Erst einen entfernen.")
        setzwert = str(frei[0])

    ziel[spalte] = setzwert
    if stufe == "stadt":
        # Buchungsdatum für die Reihenfolge im Band (load.mjs ordnet danach). Es ist derselbe Tag,
        # der ins Hauptbuch geht.
        ziel["featured_seit"] = heute()
    schreibe_csv(csv_pfad, felder, rows)
    preis = (tiers.get(STUFEN[stufe][3], {}) or {}).get("price", "")
    haenge_hauptbuch(hb_pfad, [{"datum": heute(), "aktion": "verkauf", "eintrag_slug": ziel["slug"],
                                "stufe": stufe, "stadt": stadt, "preis": preis}])
    zusatz = f" (Rang {setzwert})" if stufe == "top" else ""
    print(f"Verkauft: {name}{zusatz} an {ziel['name']} in {stadt_anzeige}. Spalte {spalte}={setzwert}, "
          f"im Hauptbuch festgehalten.")
    melde_fehlende_buchungsdaten(rows)
    neu_bauen_ausliefern(a, verzeichnis, domain, projekt)


def cmd_entfernen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    stadt = ziel["city_slug"]
    stadt_anzeige = ziel.get("city") or stadt

    aktiv = aktive_stufen(ziel)
    if a.stufe:
        aktiv = [t for t in aktiv if t[0] == a.stufe]
        if not aktiv:
            print(f"{ziel['name']} hält in {stadt_anzeige} kein {STUFEN[a.stufe][2]}. Nichts zu tun.")
            return
    if not aktiv:
        print(f"{ziel['name']} hat in {stadt_anzeige} keinen bezahlten Platz. Nichts zu tun.")
        return

    hb_neu = []
    entfernt = []
    for schluessel, name, _ in aktiv:
        if schluessel is None:
            # featured county/state (spätere Stufen) — Spalte trotzdem leeren.
            spalte = "featured"
        else:
            spalte = STUFEN[schluessel][0]
        ziel[spalte] = ""
        if spalte == "featured":
            ziel["featured_seit"] = ""
        entfernt.append(name)
        hb_neu.append({"datum": heute(), "aktion": "ende", "eintrag_slug": ziel["slug"],
                       "stufe": schluessel or "featured", "stadt": stadt, "preis": ""})
    schreibe_csv(csv_pfad, felder, rows)
    haenge_hauptbuch(hb_pfad, hb_neu)
    print(f"Entfernt: {', '.join(entfernt)} bei {ziel['name']} in {stadt_anzeige}. "
          f"Ende im Hauptbuch festgehalten.")
    melde_fehlende_buchungsdaten(rows)
    neu_bauen_ausliefern(a, verzeichnis, domain, projekt)


def _zeige_treffer(slug, teil):
    if not teil:
        fehler(f"kein Eintrag mit Slug '{slug}' gefunden. Nie raten — prüf die Schreibweise.")
    print(f"ABBRUCH: '{slug}' passt auf {len(teil)} Einträge:", file=sys.stderr)
    for r in teil[:25]:
        print(f"  {r['slug']}  ({r['name']}, {r.get('city') or r['city_slug']})", file=sys.stderr)
    if len(teil) > 25:
        print(f"  ... und {len(teil) - 25} weitere", file=sys.stderr)
    print("Genaueren Slug angeben. Nie raten.", file=sys.stderr)
    sys.exit(1)


def heute():
    return dt.date.today().isoformat()


def main():
    ap = argparse.ArgumentParser(description="Verkaufte Plätze setzen, entfernen, auflisten.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="Slug des Eintrags (exakt oder eindeutiger Teil)")
    ap.add_argument("--stufe", choices=sorted(STUFEN), help="premium | stadt | top")
    ap.add_argument("--entfernen", action="store_true", help="bezahlte Plätze dieses Eintrags zurücksetzen")
    ap.add_argument("--liste", action="store_true", help="zeigt, was gerade bezahlt ist und seit wann")
    ap.add_argument("--verzeichnis", help="Build-Verzeichnis (Vorgabe: einziges unter output/*/site/)")
    ap.add_argument("--hauptbuch", help="Pfad des Verkaufs-Hauptbuchs (Vorgabe: <verzeichnis>/verkauf-hauptbuch.csv)")
    ap.add_argument("--projekt", help="Cloudflare-Pages-Projekt (Vorgabe: Verzeichnisname)")
    ap.add_argument("--kein-deploy", dest="kein_deploy", action="store_true", help="nur bauen, nicht ausliefern (Test)")
    ap.add_argument("--kein-bauen", dest="kein_bauen", action="store_true", help="nur CSV/Hauptbuch, nicht bauen (Test)")
    a = ap.parse_args()

    if not (a.liste or a.entfernen or a.stufe):
        ap.error("eine Aktion wählen: --liste, --stufe premium|stadt|top, oder --entfernen")
    if a.liste and (a.entfernen or a.stufe or a.slug):
        ap.error("--liste steht für sich allein")

    verzeichnis = finde_verzeichnis(a.verzeichnis)
    csv_pfad = os.path.join(verzeichnis, "site", "src", "data", "listings.csv")
    hb_pfad = a.hauptbuch if a.hauptbuch else os.path.join(verzeichnis, "verkauf-hauptbuch.csv")
    if a.hauptbuch and not os.path.isabs(hb_pfad):
        hb_pfad = os.path.join(WURZEL, hb_pfad)
    site_json = json.load(open(os.path.join(verzeichnis, "site", "src", "data", "site.json"), encoding="utf-8"))
    domain = site_json.get("domain", "")
    tiers = site_json.get("tiers", {})
    projekt = a.projekt or os.path.basename(verzeichnis)

    felder, rows = lade_csv(csv_pfad)
    if "featured_seit" not in felder:
        felder = felder + ["featured_seit"]
        for r in rows:
            r.setdefault("featured_seit", "")
    hb = lade_hauptbuch(hb_pfad)

    if a.liste:
        cmd_liste(rows, hb)
        return
    if not a.slug:
        ap.error("--slug ist nötig für --stufe und --entfernen")
    if a.entfernen:
        cmd_entfernen(a, rows, felder, csv_pfad, hb, hb_pfad, verzeichnis, domain, projekt)
        return
    if not a.stufe:
        ap.error("--stufe premium|stadt|top angeben (oder --entfernen, oder --liste)")
    cmd_verkauf(a, rows, felder, csv_pfad, hb, hb_pfad, tiers, verzeichnis, domain, projekt)


if __name__ == "__main__":
    main()
