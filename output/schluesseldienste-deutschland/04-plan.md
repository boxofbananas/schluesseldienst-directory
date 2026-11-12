---
title: Gate 4 – Plan
type: output
status: entscheidungen-getroffen
updated: 2026-11-04
---

# Gate 4 – Plan

Aufbau vom [[master-template]], Optik des Templates (Gate 1: „Vorgabe"), Tatsachen aus
`03-listings-enriched.csv`. Alle Zahlen unten sind **nach Ausschluss der fremden Gewerbe**
gerechnet (431 Einträge, siehe Entscheidung 1), also auf **2.493 behaltenen Einträgen**.

## Die zwei Gruppen aus den 507 `schluesseldienst_kern=false`

- **Ausschließen: 431 fremde Gewerbe** (Baumarkt, Metallbau, Schuhmacher, Gravur, Kfz u. ä.) –
  `04-exclusions.csv`, `action=exclude`. Sie machen Schlüssel nach, öffnen aber keine Türen.
- **Behalten: 76** mit Google-Kategorie `locksmith`/`emergency_locksmith_service`, deren Website
  keine Türöffnung beschreibt. Fehlender Beleg ist kein Gegenbeleg; sie bleiben Grundeinträge
  ohne behauptete Merkmale. Liste zur Ausreißer-Durchsicht: `04-keep-locksmith-review.md`.
  **Hinweis:** es sind **76**, nicht 75 – einer trägt `Emergency locksmith service` statt
  `Locksmith`; ich habe ihn zur Gruppe „behalten" gezählt. Sagen Sie, wenn er raus soll.

## Die abgefragten Zahlen

### Stadt-Mindestzahl — **ENTSCHIEDEN: 2**
| Mindestzahl | Stadtseiten | Einträge darauf |
|---|---:|---:|
| **2 ← gewählt** | 380 | 1.755 |
| 3 | 170 | 1.335 |

### `foldMaxKm` — **ENTSCHIEDEN: 30**
Bei Mindestzahl 2 sind die Orte unter der Mindestzahl **1-Eintrag-Orte**. Faltung bei
Mindestzahl 2:
| foldMaxKm | eigenständige Ortsseiten (1 Eintrag) | zugeschlagen |
|---|---:|---:|
| **30 ← gewählt** | **80** | 654 |
| 50 | weniger | mehr |

Dazu 4 Orte ohne Koordinaten (nachgetragene eigene Betriebe) – von Hand zuzuordnen
(Entscheidung 10). **Zur Zahl:** die zuvor genannten **310** galten für Mindestzahl **3**; bei
der gewählten Mindestzahl 2 sind es **80**. Begründung des Betreibers für 30 km: ein Notdienst
fährt realistisch 20–30 km; bei 50 km erschienen Betriebe aus 45 km auf fremden Stadtseiten.

### Bestätigt: jede Stadt ab Mindestzahl 2 bekommt eine eigene Seite
Unabhängig von `foldMaxKm` (das nur 1-Eintrag-Orte betrifft). Die genannten behalten ihre
Seite: **Nürnberg 22, Fürth 8, Mannheim 19, Ludwigshafen am Rhein 5, Heidelberg 7** – je
eigener `(Bundesland, Stadt)`-Schlüssel, getrennt von Namensnachbarn (Bodman-Ludwigshafen BW,
Wipperfürth NW sind andere Seiten).

### Dünn nach Ausschluss und Sitemap zum Start
- **Noch dünn nach Ausschluss: 675** von 2.493 (nicht dünn: 1.818).
- **Sitemap zum Start** (Mindestzahl 2, foldMaxKm 30, die 80 1-Eintrag-Ortsseiten zunächst
  **draußen**): **2.224 Seiten** = 1 Start + 16 Bundesländer + 380 Städte + 1.818 Einträge
  (thin=false) + 7 Leistungen (6 + Index) + 2 Vertrauensseiten.
- **Gate-6-Regel (Betreiber):** die **80 eigenständigen 1-Eintrag-Ortsseiten** kommen zum Start
  nicht in die Sitemap, sondern werden wie dünne Einträge behandelt und nach der 30-Tage-Prüfung
  tranchenweise freigeschaltet (festgehalten in `06-launch.md`).
- Die 675 dünnen Eintragsseiten starten auf `noindex`, dazu die Formular-/Pflichtseiten
  ([[launch-lean]]).

### Mindestzahl/foldMaxKm im Template gesetzt
`templates/astro` liest beide Werte aus `site.json` (`load.mjs`). **Erledigt:**
`templates/astro/src/data/site.json` auf `"cityFloor": 2` und `"foldMaxKm": 30` gesetzt. Gate 5
übernimmt das beim Kopieren.

## Bundesländer (alle 16 bekommen eine Seite), Reihenfolge auf der Startseite nach Einträgen

NW 582 · BY 353 · BW 318 · NI 186 · HE 180 · BE 155 · SN 127 · RP 102 · SH 87 · BB 74 ·
ST 71 · HH 66 · TH 64 · MV 64 · SL 38 · HB 25.

## 20 größte Städte (Startseiten-Raster)

Berlin 155 · Hamburg 66 · München 44 · Köln 43 · Frankfurt am Main 35 · Düsseldorf 34 ·
Essen 30 · Stuttgart 27 · Hannover 23 · Nürnberg 22 · Duisburg 21 · **Mannheim 19** ·
Dortmund 19 · Bremen 18 · Wuppertal 18 · Leipzig 16 · Karlsruhe 15 · Mönchengladbach 15 ·
Bonn 13 · Mülheim an der Ruhr 12.

## Leistungsseiten (sechs, `service`-Block in `03-attributes.json`)

Bestätigte Einträge je Leistung (true): Notdienst 1.166 · Türöffnung 1.259 · Schließanlagen
1.060 · Einbruchschutz 997 · Autoschlüssel 710 · Tresoröffnung 292. Alle weit über jeder
Mindestzahl. **Vorschlag: alle sechs bauen.**

## Bezahlte Plätze / Footprint

Je Stadt höchstens ein eigener Betrieb auf einem bezahlten Platz ([[footprint-rules]]).
**Mannheim** im Vollausbau; **Merz Sicherheit** erhält Premium + Top-Platzierung zum
öffentlichen Preis **erst nach dem Start** und erst nach bestandener Festpreis-Garantie, wie
jeder andere ([[konventionen]]). Keine Garantie ist zum Start gesetzt (`geprueft` überall leer).

## Gestaltungsmarken

Optik des Templates unverändert (Gate 1). Keine Optikvorlage, keine abweichenden Marken
([[design-seed]]).

### Nachtrag — Design-Pilot 1 (Branch `design/pilot1`, 2026-11-12, NICHT freigegeben)

Layout- und Komponentenarbeit auf den bestehenden Marken; Farben und Schriften unverändert
(Navy, Bernstein, Petrol, Tönung; Roboto Slab / Roboto). Nur diese Marken sind **neu bzw.
geändert**, alle **aus den PNG-Referenzen abgeleitet, Pilot 1** (`design-pilot1/`), gesetzt in
`site.json` → `design` und über `Base.astro` als CSS-Variablen:

| Marke (`site.json.design`) | CSS-Variable | Wert | Herkunft |
|---|---|---|---|
| `cardRadius` | `--card-radius` | `22px` | aus PNG abgeleitet, Pilot 1 (große Kartenradien) |
| `cardShadow` | `--card-shadow` | `0 18px 44px -26px rgba(11,37,69,0.30), 0 4px 12px -8px rgba(11,37,69,0.14)` | aus PNG abgeleitet, Pilot 1 (weicher Kartenschatten) |
| `spaceSection` | `--space-section` | `clamp(3.25rem, 6vw, 5.5rem)` | aus PNG abgeleitet, Pilot 1 (großzügige Abschnittsabstände) |
| `buttonRadius` (geändert) | `--button-radius` | `8px` → `999px` | aus PNG abgeleitet, Pilot 1 (Schaltflächen und Suchfeld in Pillenform) |

Farbmarken, Schriften, `radius` (8px, Kleinflächen), `tint`, `gold`, `band` usw. bleiben
unverändert. Der Pilot ist nicht freigegeben und nicht ins Template zurückportiert
([[template-build-drift]]).

## `niche.schemaType`

`Locksmith` ([[schema]]).

## Entscheidungstabelle

| # | Entscheidung | Zahlen | Vorschlag |
|---|---|---|---|
| 1 | Fremde Gewerbe (Baumarkt/Metallbau/Schuhmacher/Gravur/Kfz) | 431 | **ausschließen** (erledigt, `04-exclusions.csv`) |
| 2 | 76 locksmith-Kategorie, `kern=false` | 75 Locksmith → **alle Gruppe B (behalten)**, 0 zur Durchsicht (`04-keep-sorted.md`); der 1 `emergency_locksmith_service` → zur Callcenter-Prüfung, dort ohne Merkmal → bleibt | **erledigt** |
| 3 | Stadt-Mindestzahl | 2 → 380 Seiten / 1.755 · 3 → 170 / 1.335 | **2 (entschieden)** |
| 4 | `foldMaxKm` | bei Mindestzahl 2: 30 → 80 Orte (+4 ohne Koordinaten) | **30 (entschieden)**; die 80 starten außerhalb der Sitemap |
| 5 | Leistungsseiten | 6, je 292–1.259 bestätigt | **alle sechs** |
| 6 | Reihenfolge Bundesländer (Startseite) | nach Einträgen, s. o. | **wie berechnet** |
| 7 | Mannheim / Merz-Platz | Mannheim 19 Einträge | **Vollausbau; Merz-Platz erst nach Start, zum öffentlichen Preis** |
| 8 | Ketten (je Standort) | 42 Gruppen gleichen Namens in ≥2 Städten; **0 Standorte** erfüllen die Ausschlussregel (geteilte Domain+Nummer **und** keine prüfbare Anschrift) | **keine Ausschlüsse**; Gruppen zur Durchsicht in `04-chains.md` |
| 9 | Callcenter ohne Ortsbezug | nach Entfernen des Merkmals „keine Straße" (Service-Area ist Normalfall): **0 Kandidaten** (`04-callcenter.md`) | **keine Ausschlüsse** (entschieden) |
| 10 | Koordinaten der eigenen Betriebe | `add_own_listings.py` geokodiert jetzt (Nominatim, Rückfall PLZ-Mittelpunkt, Spalte `geo_precision`); alle 12 exakt | **erledigt** |
| 11 | Mittelstadt-Regel | Stadt ab **20.000 Einwohnern** bekommt eine eigene Seite, auch mit 1 Eintrag (GeoNames cities5000; Spalte `population`; `load.mjs` + `site.cityMinPopulation`). +180 Seiten gegenüber reiner Faltung | **20.000 (entschieden, umgesetzt)** |

## Ergebnis
`04-plan.md` (dieser Entwurf), `04-exclusions.csv` (431), `04-keep-locksmith-review.md` (76).
**Alle Entscheidungen getroffen (1–11).** Keine Ketten- oder Callcenter-Ausschlüsse; nur die
431 fremden Gewerbe werden entfernt. **Datenstand fix: 431 ausgeschlossen, 2.493 behalten.**
Template auf `cityFloor: 2`, `foldMaxKm: 30`, `cityMinPopulation: 20000`; eigene Betriebe
geokodiert (`geo_precision`), Einwohnerzahl je Stadt in Spalte `population`.

**Seitenbild (simuliert nach `load.mjs`-Logik):** 381 Stadtseiten mit ≥ 2 Einträgen (indexiert),
**260 eigenständige 1-Eintrag-Stadtseiten** (66 Entfernung, 180 Einwohner, 14 beides; zum Start
`noindex`, Tranchen), 475 gefaltete Orte. Start-Sitemap ~2.225; Tranchen-Reserve 260 Stadtseiten
+ 675 dünne Einträge. **Nächstes:** Gate 5 (Bauen und Texten) – dort verifiziert `npm run build`
die `load.mjs`-Änderungen.

### Für Gate 5 vorgemerkt (aus dieser Runde)
- **Stadtseiten-Sortierung** nach den bezahlten Plätzen: Garantie → Festnetz mit passender
  Ortsvorwahl → Rest, je Gruppe nach Bewertung ([[konventionen]]); `load.mjs` umsetzen.
- **Karte je Eintrag:** bei `geo_precision = "plz"` die Ortsfläche statt einer Punktnadel (hier
  aktuell keine, da alle 12 exakt geokodiert).
- **Festpreis-Garantie-Voraussetzung** (Festnetz mit passender Ortsvorwahl, Mobil allein genügt
  nicht) ist in `konventionen`, `siegel-programm`, der `/festpreis-garantie/`-Seite und dem
  Antragsformular bereits ergänzt.
- **Daten-Nachtrag (klein):** die eigenen Einträge Frankenthal (Slug `frankenthal` vs. Scrape
  `frankenthal-pfalz`) und Bensheim (kein Scrape-Bensheim über der Mindestzahl → fällt auf
  Heppenheim) landen über die Faltung auf einer Nachbarseite. Prüfen, ob die Ortsnamen der
  eigenen Betriebe an die Scrape-Schreibweise angeglichen werden sollen.

## Dateien
`04-plan.md`, `04-exclusions.csv` (431), `04-keep-sorted.md` (75 → B), `04-chains.md` (42
Gruppen, 0 Ausschlüsse), `04-callcenter.md` (2 Kandidaten).
</content>
