#!/usr/bin/env python3
"""Kontaktbuch für die Ansprache der Betriebe — anhängen, nie überschreiben.

Der Rückweg für Anträge beginnt mit dem Anruf: „Sie haben einen Eintrag in meinem Verzeichnis."
Dieses Skript hält jeden Kontakt fest, führt eine Sperrliste und sagt, wer noch nie
angesprochen wurde. Es ändert **keinen** Eintrag und rührt listings.csv nicht an (nur Lesen);
es baut und liefert nichts aus.

Zwei anhängende Bücher neben der Build-CSV:
  output/<slug>/kontakt-hauptbuch.csv   datum, eintrag_slug, weg, ergebnis, notiz
  output/<slug>/kontakt-sperrliste.csv  datum, eintrag_slug, grund

    # einen Kontakt festhalten
    python3 scripts/kontakt.py eintragen --slug <slug> --weg telefon|email|formular \\
        --ergebnis "erreicht, Antrag zugesagt" [--notiz "…"] [--datum JJJJ-MM-TT]

    # einen Eintrag sperren (nie wieder als „noch zu kontaktieren" zeigen)
    python3 scripts/kontakt.py sperren --slug <slug> [--grund "bittet um Ruhe"]

    # wer wurde noch nie kontaktiert (ohne eigene Betriebe, ohne Gesperrte)
    python3 scripts/kontakt.py --offen [--bundesland "Baden-Württemberg"] [--stadt Mannheim] [--alle]

    # Zahlen je Status
    python3 scripts/kontakt.py --stand

Weg-Werte: telefon, email, formular. Beide Bücher werden nur **angehängt** — eine Korrektur ist
eine neue Zeile, nie das Überschreiben einer alten.
"""
import argparse
import csv
import datetime as dt
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)

from verkauf import WURZEL, truthy, fehler, finde_verzeichnis, lade_csv, finde_zeile, _zeige_treffer, heute

csv.field_size_limit(10**9)

HB_FELDER = ["datum", "eintrag_slug", "weg", "ergebnis", "notiz"]
SP_FELDER = ["datum", "eintrag_slug", "grund"]
WEGE = ["telefon", "email", "formular"]


def lade(pfad, felder):
    if not os.path.isfile(pfad):
        return []
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def haenge(pfad, felder, zeile):
    neu = not os.path.isfile(pfad)
    with open(pfad, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        if neu:
            w.writeheader()
        w.writerow(zeile)


def norm_bundesland(s):
    return (s or "").strip().lower()


def cmd_eintragen(a, rows, hb_pfad):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    if a.weg not in WEGE:
        fehler("--weg muss telefon, email oder formular sein.")
    if not (a.ergebnis or "").strip():
        fehler("--ergebnis angeben (was bei dem Kontakt herauskam).")
    datum = a.datum or heute()
    try:
        dt.date.fromisoformat(datum)
    except ValueError:
        fehler(f"--datum '{datum}' ist kein Datum im Format JJJJ-MM-TT.")
    haenge(hb_pfad, HB_FELDER, {"datum": datum, "eintrag_slug": ziel["slug"], "weg": a.weg,
                                "ergebnis": a.ergebnis.strip(), "notiz": (a.notiz or "").strip()})
    print(f"Festgehalten: {datum} · {ziel['name']} ({ziel['slug']}) · {a.weg} · {a.ergebnis.strip()}")


def cmd_sperren(a, rows, sp_pfad, sperr):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    if ziel["slug"] in sperr:
        print(f"{ziel['name']} ({ziel['slug']}) ist bereits gesperrt. Nichts zu tun.")
        return
    haenge(sp_pfad, SP_FELDER, {"datum": heute(), "eintrag_slug": ziel["slug"], "grund": (a.grund or "").strip()})
    print(f"Gesperrt: {ziel['name']} ({ziel['slug']})"
          + (f" — {a.grund.strip()}" if (a.grund or '').strip() else "")
          + ". Erscheint in keiner Liste 'noch zu kontaktieren' mehr.")


def cmd_offen(a, rows, kontaktiert, sperr):
    offen = []
    for r in rows:
        if truthy(r.get("owned")):
            continue
        if r["slug"] in sperr:
            continue
        if r["slug"] in kontaktiert:
            continue
        if a.bundesland and norm_bundesland(r.get("state")) != norm_bundesland(a.bundesland):
            continue
        if a.stadt and (r.get("city") or "").strip().lower() != a.stadt.strip().lower():
            continue
        offen.append(r)
    offen.sort(key=lambda r: ((r.get("state") or "").lower(), (r.get("city") or "").lower(), r["slug"]))

    filterhinweis = ""
    if a.bundesland:
        filterhinweis += f" · Bundesland {a.bundesland}"
    if a.stadt:
        filterhinweis += f" · Stadt {a.stadt}"
    print(f"Noch nie kontaktiert: {len(offen)} Einträge (ohne eigene, ohne gesperrte){filterhinweis}.\n")
    if not offen:
        return
    gefiltert = bool(a.bundesland or a.stadt)
    if len(offen) > 200 and not gefiltert and not a.alle:
        print("  Viele offene Einträge — Verteilung je Bundesland (mit --bundesland/--stadt einschränken,")
        print("  oder --alle zum vollständigen Auflisten):\n")
        je = {}
        for r in offen:
            je[r.get("state") or "?"] = je.get(r.get("state") or "?", 0) + 1
        for bl in sorted(je, key=lambda b: -je[b]):
            print(f"    {je[bl]:>5}  {bl}")
        return
    print(f"  {'Bundesland':<22} {'Stadt':<18} {'Betrieb':<34} {'Tel':<3} {'Mail':<4} Eintrag")
    print("  " + "-" * 110)
    for r in offen:
        tel = "ja" if (r.get("phone") or "").strip() else "—"
        mail = "ja" if any((r.get(c) or "").strip() for c in ("email_1", "email_2", "email_3")) else "—"
        print(f"  {(r.get('state') or '')[:21]:<22} {(r.get('city') or '')[:17]:<18} "
              f"{r['name'][:33]:<34} {tel:<3} {mail:<4} {r['slug']}")


def cmd_stand(rows, hb, kontaktiert, sperr):
    gesamt = len(rows)
    eigen = sum(1 for r in rows if truthy(r.get("owned")))
    gesperrt = sum(1 for r in rows if r["slug"] in sperr)
    # „offen" = nicht eigen, nicht gesperrt, nie kontaktiert
    offen = sum(1 for r in rows if not truthy(r.get("owned")) and r["slug"] not in sperr and r["slug"] not in kontaktiert)
    kontaktiert_n = sum(1 for r in rows if r["slug"] in kontaktiert)
    print("Kontakt-Stand:\n")
    print(f"  Einträge gesamt          {gesamt:>6}")
    print(f"  davon eigene Betriebe    {eigen:>6}  (nie in 'noch zu kontaktieren')")
    print(f"  gesperrt                 {gesperrt:>6}")
    print(f"  schon kontaktiert        {kontaktiert_n:>6}  (eindeutige Einträge im Hauptbuch)")
    print(f"  noch offen               {offen:>6}  (nicht eigen, nicht gesperrt, nie kontaktiert)")
    if hb:
        print(f"\n  Kontakte im Hauptbuch gesamt: {len(hb)}")
        je_weg = {}
        je_erg = {}
        for z in hb:
            je_weg[z.get("weg") or "?"] = je_weg.get(z.get("weg") or "?", 0) + 1
            je_erg[(z.get("ergebnis") or "?").strip() or "?"] = je_erg.get((z.get("ergebnis") or "?").strip() or "?", 0) + 1
        print("  je Weg:    " + ", ".join(f"{w}: {n}" for w, n in sorted(je_weg.items(), key=lambda x: -x[1])))
        print("  je Ergebnis:")
        for e, n in sorted(je_erg.items(), key=lambda x: -x[1]):
            print(f"    {n:>5}  {e}")


def main():
    ap = argparse.ArgumentParser(description="Kontaktbuch: eintragen, sperren, offene Einträge, Stand.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aktion", nargs="?", choices=["eintragen", "sperren"],
                    help="eintragen = Kontakt festhalten; sperren = Eintrag sperren")
    ap.add_argument("--slug", help="Slug des Eintrags (exakt oder eindeutiger Teil)")
    ap.add_argument("--weg", choices=WEGE, help="telefon | email | formular (bei eintragen)")
    ap.add_argument("--ergebnis", help="was bei dem Kontakt herauskam (bei eintragen)")
    ap.add_argument("--grund", help="Grund der Sperre (bei sperren)")
    ap.add_argument("--notiz", help="Freitext-Notiz")
    ap.add_argument("--datum", help="Datum JJJJ-MM-TT (Vorgabe: heute)")
    ap.add_argument("--offen", action="store_true", help="Einträge, die noch nie kontaktiert wurden")
    ap.add_argument("--stand", action="store_true", help="Zahlen je Status")
    ap.add_argument("--bundesland", help="--offen auf ein Bundesland einschränken (Spalte state)")
    ap.add_argument("--stadt", help="--offen auf eine Stadt einschränken")
    ap.add_argument("--alle", action="store_true", help="--offen vollständig auflisten, auch bei vielen")
    ap.add_argument("--verzeichnis", help="Build-Verzeichnis (Vorgabe: einziges unter output/*/site/)")
    ap.add_argument("--hauptbuch", help="Pfad des Kontaktbuchs (Vorgabe: <verzeichnis>/kontakt-hauptbuch.csv)")
    ap.add_argument("--sperrliste", help="Pfad der Sperrliste (Vorgabe: <verzeichnis>/kontakt-sperrliste.csv)")
    a = ap.parse_args()

    aktionen = [bool(a.aktion), a.offen, a.stand]
    if sum(aktionen) != 1:
        ap.error("genau eine Aktion: eintragen, sperren, --offen oder --stand")

    verzeichnis = finde_verzeichnis(a.verzeichnis)
    csv_pfad = os.path.join(verzeichnis, "site", "src", "data", "listings.csv")
    hb_pfad = a.hauptbuch or os.path.join(verzeichnis, "kontakt-hauptbuch.csv")
    sp_pfad = a.sperrliste or os.path.join(verzeichnis, "kontakt-sperrliste.csv")
    if a.hauptbuch and not os.path.isabs(hb_pfad):
        hb_pfad = os.path.join(WURZEL, hb_pfad)
    if a.sperrliste and not os.path.isabs(sp_pfad):
        sp_pfad = os.path.join(WURZEL, sp_pfad)

    _, rows = lade_csv(csv_pfad)
    hb = lade(hb_pfad, HB_FELDER)
    sp = lade(sp_pfad, SP_FELDER)
    kontaktiert = {z.get("eintrag_slug") for z in hb}
    sperr = {z.get("eintrag_slug") for z in sp}

    if a.aktion == "eintragen":
        if not a.slug:
            ap.error("eintragen braucht --slug")
        cmd_eintragen(a, rows, hb_pfad)
    elif a.aktion == "sperren":
        if not a.slug:
            ap.error("sperren braucht --slug")
        cmd_sperren(a, rows, sp_pfad, sperr)
    elif a.offen:
        cmd_offen(a, rows, kontaktiert, sperr)
    elif a.stand:
        cmd_stand(rows, hb, kontaktiert, sperr)


if __name__ == "__main__":
    main()
