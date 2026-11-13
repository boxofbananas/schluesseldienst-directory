#!/usr/bin/env python3
"""Schutz der operativen Spalten von site/src/data/listings.csv gegen Datenverlust.

Die Build-CSV ist die **alleinige Wahrheit** fuer die operativen Spalten (Festpreis-Garantie,
Premium, Buchung). 03-listings-enriched.csv traegt sie nie: dort stehen die beschreibenden
Spalten (Beschreibung, Merkmale, Bewertungen, Scrape-Felder). Setzt also verkauf.py einen
Platz oder wird eine Garantie von Hand erteilt, geschieht das in listings.csv und nirgends
sonst. Ein Lauf, der listings.csv aus enriched neu schreibt, wuerde diese Werte loeschen,
weil enriched sie leer hat (so beim Mannheimer Ausschluss aufgefallen).

Zwei Bausteine, die jedes Skript nutzt, das listings.csv ueberschreibt:

  merge_protected(rows, fieldnames, existing_path) -> fieldnames
      Traegt die operativen Spalten per Slug aus der bestehenden listings.csv in die neuen
      Zeilen zurueck und ergaenzt fehlende Spaltennamen. So FOLGT die neu gebaute CSV der
      alten: enriched liefert Text und Merkmale, listings.csv die operativen Werte.

  pruefe_kein_verlust(rows, existing_path, erlaubt=None, etikett="") -> None
      Die SPERRE. Bricht ab (sys.exit 1), wenn eine Zeile, die bleibt, einen gefuellten
      operativen Wert verloere (gefuellt -> leer), und nennt die betroffenen Eintraege.
      `erlaubt` = {slug: {spalten}} fuer gewollte Aenderungen (verkauf.py setzt/leert seine
      eine Zelle selbst). Ein geaenderter, aber nicht geleerter Wert (z. B. neuer
      Garantiepreis) ist KEIN Verlust und loest nichts aus.

Nur der Uebergang gefuellt -> leer zaehlt. leer -> gefuellt und gefuellt -> anderer Wert sind
erlaubt. Eine per Ausschluss ganz entfernte Zeile ist kein "leer werden" und wird hier nicht
geprueft; ihr Verlust meldet apply_exclusions.py als Warnung.
"""
import csv
import sys

csv.field_size_limit(10**9)

# Die operativen Spalten: Festpreis-Garantie, Premium, Buchung, reservierter Preisschutz.
# Reihenfolge wie im Datenlayer; neue operative Spalten hier eintragen.
PROTECTED = [
    "geprueft", "geprueft_jahr",
    "garantie_tag", "garantie_zuschlag_abend", "garantie_zuschlag_nacht",
    "garantie_anfahrt", "garantie_zylinder", "garantie_zylinder_5mm",
    "featured", "featured_cities", "featured_seit", "premium", "best_of_rank",
    "preisschutz",
]


def _leer(v):
    return not (str(v or "").strip())


def _lade_geschuetzt(pfad):
    """{slug: {spalte: wert}} der GEFUELLTEN operativen Zellen der bestehenden CSV.
    Fehlt die Datei, ist die Abbildung leer (erster Lauf, nichts zu schuetzen)."""
    import os
    if not pfad or not os.path.isfile(pfad):
        return {}
    with open(pfad, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        karte = {}
        for r in rd:
            gefuellt = {c: r[c] for c in PROTECTED if c in r and not _leer(r.get(c))}
            if gefuellt:
                karte[r["slug"]] = gefuellt
    return karte


def merge_protected(rows, fieldnames, existing_path):
    """Traegt die operativen Werte der bestehenden listings.csv per Slug in `rows` zurueck
    und ergaenzt fehlende operative Spalten. Gibt die (ggf. erweiterte) Spaltenliste zurueck.
    listings.csv ist die Wahrheit fuer diese Spalten, also gewinnt ihr gefuellter Wert."""
    karte = _lade_geschuetzt(existing_path)
    felder = list(fieldnames)
    # Operative Spalten, die in der bestehenden CSV vorkommen, aber der neuen Quelle fehlen,
    # anlegen (Schema-Divergenz: enriched kennt z. B. featured_seit nicht).
    noetig = set()
    for g in karte.values():
        noetig.update(g.keys())
    for c in PROTECTED:
        if c in noetig and c not in felder:
            felder.append(c)
    for r in rows:
        for c in felder:
            r.setdefault(c, "")
        g = karte.get(r.get("slug"))
        if not g:
            continue
        for c, v in g.items():
            r[c] = v  # bestehender gefuellter Wert gewinnt; leert nie
    return felder


def pruefe_kein_verlust(rows, existing_path, erlaubt=None, etikett="listings.csv"):
    """Bricht ab, wenn eine bleibende Zeile einen gefuellten operativen Wert verloere."""
    karte = _lade_geschuetzt(existing_path)
    if not karte:
        return
    erlaubt = erlaubt or {}
    neu = {r.get("slug"): r for r in rows}
    verluste = []  # (slug, spalte, alter_wert)
    for slug, g in karte.items():
        r = neu.get(slug)
        if r is None:
            continue  # Zeile ganz entfernt (Ausschluss) -> hier nicht geprueft
        erlaubte_spalten = erlaubt.get(slug, set())
        for c, alt in g.items():
            if c in erlaubte_spalten:
                continue
            if _leer(r.get(c)):
                verluste.append((slug, c, alt))
    if verluste:
        print(f"ABBRUCH: Schreiben von {etikett} wuerde gefuellte Garantie-/Premium-/"
              f"Buchungsspalten leeren. {len(verluste)} Zelle(n) betroffen:", file=sys.stderr)
        proben = {}
        for slug, c, alt in verluste:
            proben.setdefault(slug, []).append(f"{c}={alt}")
        for slug in sorted(proben):
            print(f"  {slug}: {', '.join(proben[slug])}", file=sys.stderr)
        print("Die operativen Spalten stehen nur in listings.csv (nicht in enriched). Vor dem "
              "Schreiben mit merge_protected() aus der bestehenden listings.csv zuruecktragen "
              "oder von Hand sichern. Es wurde nichts geschrieben.", file=sys.stderr)
        sys.exit(1)
