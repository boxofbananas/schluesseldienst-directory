# Daten: PLZ → Bundesland und Ort

`geonames-de-plz.tsv` ordnet jede deutsche Postleitzahl ihrem Bundesland und ihren Orten zu.
`clean_listings.py` (Gate 2) liest die Datei, um das Bundesland jeder Zeile aus der PLZ
abzuleiten (DataForSEO liefert für Deutschland kein `region`-Feld) und um englische
Exonyme und fehlende Städtenamen auf den deutschen Ortsnamen zu bringen.

## Dateien

- `geonames-de-plz.tsv` — PLZ → Ort, Bundesland, Koordinate (fünf Spalten, siehe unten).
- `de-city-population.tsv` — Einwohnerzahl je Stadt für die Mittelstadt-Regel (drei Spalten:
  `bundesland_kuerzel<TAB>ort_grundform<TAB>einwohner`). Quelle GeoNames `cities5000` (Feature-
  Klasse P), abgerufen am 2026-11-04, CC BY 4.0. Zuordnung über Name + Bundesland, Grundform wie
  in `clean_listings.py:city_base`. `clean_listings.py` und `add_own_listings.py` schreiben die
  Einwohnerzahl in die Spalte `population`; `templates/astro/src/lib/load.mjs` gibt einer Stadt ab
  `site.cityMinPopulation` eine eigene Seite, auch mit nur einem Eintrag.

## Format `geonames-de-plz.tsv`

Tabulatorgetrennt, fünf Spalten, keine Kopfzeile, eine Zeile je PLZ-Ort-Paar:

```
plz<TAB>ort<TAB>bundesland_kuerzel<TAB>lat<TAB>lon
```

(`add_own_listings.py` nutzt lat/lon als Rückfall-Geokodierung, wenn Nominatim nichts findet.)

Eine PLZ kann mehrfach vorkommen (mehrere Orte/Ortsteile). Die Bundesland-Kürzel sind die
16 aus `wiki/konventionen.md` (BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH);
den deutschen Namen bildet das Skript selbst aus dem Kürzel (`NAME_BY_CODE` in
`fetch_dataforseo.py`), weil die Quelle einige Namen englisch führt (Bavaria, Lower Saxony).

## Herkunft und Lizenz

GeoNames Postal Codes, Datei `DE.txt` aus `https://download.geonames.org/export/zip/DE.zip`,
abgerufen am 2026-11-03. Nur die Spalten PLZ, Ort und Bundesland-Kürzel übernommen, auf die
16 gültigen Kürzel gefiltert. GeoNames steht unter **CC BY 4.0**
(`https://creativecommons.org/licenses/by/4.0/`).

Neu beziehen: `DE.zip` laden, entpacken, Spalten 2 (PLZ), 3 (Ort), 5 (Bundesland-Kürzel)
übernehmen, auf fünfstellige PLZ und die 16 Kürzel filtern.
</content>
</invoke>
