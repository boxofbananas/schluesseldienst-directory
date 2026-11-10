# Ein Befehl für verkaufte Plätze: scripts/verkauf.py

**Datum:** 2026-11-10
**Ziel:** Nach einer Stripe-Zahlung nicht mehr von Hand die CSV ändern, bauen und ausliefern,
sondern ein Befehl: Spalte setzen, Verkauf im Hauptbuch festhalten, bauen, ausliefern,
`check_live.py`.

## Aufruf

```
python3 scripts/verkauf.py --slug <eintrag-slug> --stufe premium|stadt|top
python3 scripts/verkauf.py --slug <eintrag-slug> --entfernen [--stufe ...]
python3 scripts/verkauf.py --liste
```

## Stufen → Spalten (aus dem Datenlayer gelesen, nicht fest verdrahtet)

`templates/astro/src/lib/load.mjs` und `templates/featured-tiers.md` sind maßgeblich:

| Stufe | Stripe-Produkt | Spalte | Wert |
|---|---|---|---|
| `premium` | Premium-Eintrag, 97 €/Jahr | `premium` | `true` |
| `stadt` | Stadt-Premium, 29 €/Monat | `featured` | `city` (je Stadt einmal) |
| `top` | Top-Platzierung, 250 € einmalig | `best_of_rank` | nächster freier Rang 1–3 der Stadt |

Das Skript liest `truthy` genau wie der Build (`/^(true|wahr|ja|yes|1|y|j)$/i`) und die Preise aus
`site.json → tiers`. **Die Garantie-Spalten (`geprueft`, `geprueft_jahr`, `garantie_*`) rührt es
nie an.**

## Was es tut

- **Spalte setzen → bauen → ausliefern → check_live.py.** `check_live.py` bekommt die
  Adresszahl aus der frisch gebauten Sitemap, prüft also die Live-Seite gegen genau den Build.
- **Hauptbuch** `output/<slug>/verkauf-hauptbuch.csv` (Datum, Aktion, Slug, Stufe, Stadt, Preis).
  Jeder Verkauf und jedes Ende wird als Zeile angehängt — ohne Aufzeichnung wüsste niemand bei
  einer Kündigung in acht Monaten, welcher Eintrag gemeint war.
- **`--liste`** zeigt aus der CSV, was gerade bezahlt ist, mit dem „seit"-Datum aus dem Hauptbuch
  (`unbekannt`, solange ein Platz vor Einführung des Hauptbuchs gesetzt wurde).
- **`--entfernen`** leert die Spalte(n), trägt das Ende ins Hauptbuch ein und baut neu. Ohne
  `--stufe` werden alle bezahlten Plätze des Eintrags entfernt, mit `--stufe` nur der eine.

## Zwei Prüfungen, die abbrechen (nicht warnen)

1. **Stadt-Premium je Stadt nur einmal.** Ist `featured=city` in der Stadt schon vergeben,
   Abbruch mit Nennung des Halters.
2. **Höchstens ein eigener Betrieb je Stadt auf einem bezahlten Platz** ([[footprint-rules]]).
   Derselbe eigene Betrieb darf mehrere Stufen halten (Beispiel Merz Sicherheit: Premium +
   Top); ein **zweiter** eigener Betrieb mit bezahltem Platz in derselben Stadt bricht ab.

Ein Slug, der auf keine oder mehrere Zeilen passt, bricht ab und zeigt die Treffer. Exakter Slug
hat Vorrang, sonst eindeutiger Teiltreffer — nie geraten.

## Probelauf (nichts an der Live-Seite verändert)

- `--liste`: zeigt den Ist-Zustand — nur Merz Sicherheit Mannheim hält Premium-Eintrag +
  Stadt-Premium (seit „unbekannt", da vor dem Hauptbuch gesetzt).
- Abbruch A: Stadt-Premium an einen anderen Mannheimer Betrieb → bricht ab, nennt Merz Sicherheit.
- Abbruch B: Premium an `aes-schluesseldienst-mannheim-mannheim` (zweiter eigener Betrieb in
  Mannheim) → bricht ab (footprint-rules).
- Abbruch: `--slug merz` → mehrdeutig, zeigt 6 Treffer; unbekannter Slug → Abbruch.
- `--entfernen` auf einem Testwert (`leipziger-…-leipzig`, premium) mit Demo-Hauptbuch im
  Scratch und `--kein-bauen`: Verkauf gesetzt und protokolliert, `--liste` zeigt ihn mit
  „seit = 2026-11-10", dann entfernt und protokolliert, `--liste` wieder ohne ihn. Danach die
  CSV mit `git checkout` zurückgesetzt — `git status` sauber. **Es wurde nichts ausgeliefert und
  nichts an der Live-Seite verkauft, was niemand gekauft hat.**

Die Schalter `--kein-deploy` (nur bauen) und `--kein-bauen` (nur CSV/Hauptbuch) sind nur zum
Testen; im Normalbetrieb läuft die ganze Kette.

## Dateien

- `scripts/verkauf.py` (neu)
- `output/schluesseldienste-deutschland/verkauf-hauptbuch.csv` (neu, nur Kopfzeile — füllt sich
  bei realen Verkäufen)
- `CLAUDE.md` → Abschnitt „Neu bauen bei Änderung": Aufruf eingetragen.
