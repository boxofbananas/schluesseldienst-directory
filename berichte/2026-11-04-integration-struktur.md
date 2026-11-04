# Integration der Nachbestellung + echte Struktur (2026-11-04)

## Integriert
- Neue behaltene Einträge (Stufe A + B + Grundeintrag, **ohne** Ketten) an `02-listings-clean.csv`
  angehängt: **+1.455** → 02 hat jetzt **4.379** Zeilen. Städte an die Scrape-Schreibweise des
  Bestands angeglichen, Slugs entdoppelt, owned-Flag gesetzt.
- Ausschlüsse (`04-exclusions.csv`, `action=drop`): **442** = 431 fremde Gewerbe + **11 Ketten**
  im Bestand (BZN Hagebau, OBI Ratingen, Mister Minit ×3, „… im Globus"-Stände, DaBastler Baumarkt
  u. a.). Die **9 neuen Ketten** wurden gar nicht erst aufgenommen. Die Marke „Globus
  Schlüsseldienst® Nürnberg" bleibt (eigenständig, kein Globus-Markt-Stand).
- Korrektur am Mechanismus: Exklusions-`action` heißt `drop` (nicht `exclude`); `04-exclusions.csv`
  entsprechend korrigiert. `clean_listings.py` hat jetzt `--no-category-filter` (breiter Abruf,
  Branchenprüfung folgt am Website-Rohtext).
- Zusammenbau: `03-listings-enriched.csv` = **4.379** (2.670 angereichert aus Gate 3 unverändert,
  1.709 Grundeinträge). Bestehende Anreicherung blieb erhalten.

## Echte Struktur (aus `load.mjs` via `node dump-cities.mjs`, nicht simuliert)
Build-CSV nach `apply_exclusions`: **3.937 Einträge**, 16 Bundesländer.

| | echter Build | (Simulation vorher) |
|---|--:|--:|
| Stadtseiten ≥ 2 Einträge (indexiert) | **595** | 599 |
| Einzelseiten (1 Eintrag) | **210** | 191 |
|   davon über Entfernung (>30 km) | 46 | 46 |
|   davon über Einwohner (≥ 20.000) | 141 | 139 |
|   davon beides | 6 | 6 |
|   indexierbar über „Betriebe in der Umgebung" (≥1 Nachbar < 10 km) | **133** | 125 |
|   bleiben noindex | 77 | 66 |
| gefaltete Orte (keine Seite) | 742 | 761 |
| Stadt-/Ortsseiten gesamt (= Gate-5-Texte) | **805** | 790 |
| **Start-Sitemap-Stadtseiten (indexiert)** | **595 + 133 = 728** | |

(Die leichten Abweichungen zur Simulation kommen aus `load.mjs`’ eigener Städte-Aufteilung nach
`CITY_SPLIT_KM` und der regionweisen Faltung; der Build ist maßgeblich.)

## Anreicherung in zwei Wellen
- Neue Stufe A im Build: **1.097** (9 Ketten gedroppt), Stufe B: **299**.
- **Welle 1** — Stufe A auf Start-Sitemap-Stadtseiten: **851 Einträge → ~39 $** (live).
- **Welle 2** — Stufe A außerhalb (246) + alle Stufe B (299) = **545 → ~25 $** (dünn/noindex,
  nach der 30-Tage-Prüfung).

## Nächste Schritte
Welle 1 anreichern (~39 $), dann der Stadttext-Probestapel (Sonnet vs. kleineres Modell).
Welle 2 bleibt hinter der 30-Tage-Prüfung.
</content>
