---
title: Eigene Betriebe nachtragen
type: framework
status: stable
updated: 2026-11-03
---

# Eigene Betriebe nachtragen

Der DataForSEO-Abruf holt nur Betriebe mit mindestens einer öffentlichen Bewertung. Betriebe
ohne Unternehmensprofil oder mit gesperrtem Profil sind darin nicht enthalten — nicht
verworfen, sondern gar nicht erst abgerufen. Beim ersten Lauf dieses Projekts betraf das
19 der 21 eigenen Betriebe des Betreibers (2026-11-03).

`scripts/add_own_listings.py` trägt sie nach, zwischen Gate 2 und Gate 3:

```
python3 scripts/add_own_listings.py output/<slug>/02-listings-clean.csv \
    --eigene input/eigene-betriebe.csv --out output/<slug>/02-listings-clean.csv
```

## Was ein nachgetragener Eintrag bekommt, und was nicht

| | |
|---|---|
| `owned` | `true`. Nur für den Bericht; verändert die Darstellung nie ([[footprint-rules]]) |
| Bewertung, Anzahl Bewertungen | **leer**. Es gibt keine, also steht da keine |
| `thin` | `true`. Sichtbar und verlinkt, zum Start nicht in der Sitemap ([[launch-lean]]) |
| Festpreis-Garantie | **keine**. Nur über Antrag und Prüfung der sechs Voraussetzungen, wie bei jedem anderen Betrieb ([[siegel-programm]]) |
| Beschreibung | aus der Spalte `leistungen`, sonst leer; Gate 3 reichert sie wie jeden anderen Eintrag aus der eigenen Website an |

**Eine Bewertung wird nie erfunden.** Ein Verzeichnis, das mit einer Garantie wirbt, verliert
seinen Wert in dem Moment, in dem eine Zahl darin erfunden ist — und am schnellsten bei den
eigenen Einträgen.

## Die Datei

`input/eigene-betriebe.csv`, Kopfzeile nötig:

| Spalte | Pflicht | Bemerkung |
|---|---|---|
| `name` | ja | wie im Impressum des Betriebs |
| `strasse` | ja | mit Hausnummer |
| `plz` | ja | fünfstellig |
| `ort` | ja | deutscher Name |
| `bundesland` | wenn die PLZ-Tabelle fehlt | Name oder Kürzel |
| `telefon` | nein | darf leer bleiben |
| `website` | ja | |
| `leistungen` | nein | Freitext, Startpunkt für Gate 3 |

Das Bundesland kommt aus der Spalte oder aus `scripts/data/geonames-de-plz.tsv`, wenn
vorhanden. Geraten wird nie; eine Zeile ohne bestimmbares Bundesland wird gemeldet und nicht
übernommen.

## Doppelte

Steht ein Betrieb bereits mit echten Daten in der bereinigten Liste — erkannt an
Telefonnummer oder Website —, bleibt die echte Zeile stehen und der Nachtrag entfällt. Die
Datei kann deshalb dauerhaft gepflegt werden: Sobald ein Betrieb ein Profil mit Bewertungen
hat, holt ihn der nächste Abruf mit echten Daten, und der Nachtrag überspringt ihn von selbst.

## Grenze

Nachgetragen wird nur, was es wirklich gibt: angemeldetes Gewerbe, erreichbare Anschrift,
erreichbares Telefon. Ein Eintrag für einen Betrieb, den es an der genannten Adresse nicht
gibt, ist eine Täuschung des Lesers — unabhängig davon, wem der Eintrag gehört. Wurde ein
Unternehmensprofil wegen der Adresse gesperrt, gilt derselbe Einwand auch hier.

## Siehe auch

[[listings-cleaning]] · [[footprint-rules]] · [[siegel-programm]] · [[launch-lean]]
