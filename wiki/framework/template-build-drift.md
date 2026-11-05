---
title: Template und Build driften
type: framework
status: current
updated: 2026-11-05
---

# Template und Build driften

Jedes Verzeichnis entsteht so: Gate 5 kopiert `templates/astro/` nach `output/<slug>/site/` und
füllt die Daten ([[master-template]]). Die Kopie ist eine **Momentaufnahme**. Danach passiert alle
echte Arbeit im Build, und nichts davon fließt zurück ins Template. Das Template veraltet ab dem
Moment, in dem nach dem Kopieren weiterentwickelt wird.

**Für dieses Verzeichnis ist der Build die Wahrheit, nicht das Template.** Wer hier etwas ändert,
ändert es im Build (`output/schluesseldienste-deutschland/site/`). Das Template wird erst wieder
angefasst, **wenn ein zweites Verzeichnis entsteht** — dann wird nach der Liste unten zurückportiert.

Gegenstück dazu ist die Sperre in `scripts/init_site.py`: Existiert `output/<slug>/site/` schon,
bricht der Kopierschritt ab und nennt, was verloren ginge (nur mit `--force`, und auch dann wird der
bestehende Ordner nach `site.backup-<Zeitstempel>` beiseitegelegt, nie gelöscht). Gate 5 ruft dieses
Skript, nie ein Hand-`cp`.

## Stand der Messung (2026-11-05)

`templates/astro/src/` gegen `output/schluesseldienste-deutschland/site/src/`, ohne `src/data/`:
**25 Dateien auseinander** (18 inhaltlich verschieden, 7 nur im Build). **Alle Build-voraus, null
Template-voraus** — die gefährliche Klasse (eine Template-Änderung, die den Build nie erreicht hat,
wie es Voraussetzung 2 war) ist leer. Dazu außerhalb von `src/`: der ganze `functions/`-Ordner
(KV-Formularannahme) existiert nur im Build.

## Sorte A — Allgemeine Verbesserungen: beim nächsten Verzeichnis ins Template

Generische Verbesserungen, die aus der Live-Entwicklung stammen und jedem Verzeichnis nützen. Beim
Aufsetzen eines zweiten Verzeichnisses hierher zurückportieren.

| Thema | Dateien |
|---|---|
| **Bewertungsstern als SVG** (statt `★`-Textzeichen) | `components/Star.astro` (neu), `components/Rating.astro`, `components/FeaturedBand.astro`, `components/DirectoryHub.astro`, `pages/firma/[bundesland]/[stadt]/[slug]/index.astro`, `pages/verzeichnis/index.astro`, `pages/verzeichnis/[bundesland]/[stadt]/index.astro`, `styles/global.css` (`.star`) |
| **Häkchen als SVG** (hero-points) | `components/Check.astro` (neu), `pages/index.astro`, `styles/global.css` (hero-points-Icon) |
| **Glyph-Bereinigung + latin-ext** (Emoji/Fremdschrift raus, europäische Namen rein) | `lib/load.mjs` (`sanitizeGlyphs`, `GLYPH_OK`), `styles/fonts.css` (latin-ext-Importe) |
| **Öffnungszeiten-Fix** (DataForSEO-Array → Text, behebt „[object Object]") | `lib/load.mjs` (`normalizeHours`, Array-Zweig) |
| **Merkmalsanzeige: nur bestätigt** (kein „nein", keine „keine-Angabe"-Zeile) | `components/AttributeGrid.astro`, `pages/firma/[bundesland]/[stadt]/[slug]/index.astro` (Abschnitt nur bei vorhandenen Merkmalen) |
| **Sprungliste** auf Stadtseiten | `pages/verzeichnis/[bundesland]/[stadt]/index.astro`, `styles/global.css` (`.jump-list`), `components/Card.astro` (`id`-Prop für Anker) |
| **Startseiten-Band nur aus `featured=state`** | `lib/load.mjs` (`homeFeatured`), `components/DirectoryHub.astro` (Preis-Prop) |
| **Startseite ohne volle Städteliste** (A–Z ausgelagert auf `/verzeichnis/`) | `components/DirectoryHub.astro`, `layouts/Base.astro` (Fußzeile „Alle Städte") |
| **Suchfeld-Platzhalter** (kürzer) | `components/SearchForm.astro` |
| **KV-Formularannahme** (Cloudflare KV + Email Routing, kein externer Formulardienst) | `functions/api/` (ganzer Ordner, nur im Build), gespiegelt in den Datenschutztexten (Sorte B) |

## Sorte B — Projekteigener Inhalt: darf verschieden bleiben

Text und Entscheidungen, die zu diesem Verzeichnis gehören. Ein zweites Verzeichnis bekommt eigene
Fassungen; **nicht** blind zurückportieren.

| Thema | Dateien |
|---|---|
| **„Über uns"** (Mission, Verbraucherzentrale, Herausgeber-Einzeiler + Schema) | `pages/ueber-uns.astro` |
| **Startseiten-Überschrift Fassung B** (Augenbraue + „Damit die Rechnung keine Überraschung wird.") | `pages/index.astro` (Hero), `styles/global.css` (`.eyebrow`) |
| **Ratgeberseiten** | `pages/ratgeber/*.md` (fünf Artikel, nur im Build) |
| **Datenschutz- und Hinweistexte** (KV/Email, DSGVO-Art.-13-Hinweise) | `pages/datenschutz.astro`, `pages/eintrag-beanspruchen.astro` |
| **FAQ-Wortwahl** („steht dafür ein" statt gebanntem „garantiert") | `pages/verzeichnis/[bundesland]/index.astro` |

## Gemischte Dateien

Drei Dateien tragen beide Sorten und müssen beim Rückport **hunkweise** getrennt werden, nicht als
Ganzes übernommen:

- `pages/index.astro` — Häkchen-SVG (A) **und** Überschrift B (B).
- `styles/global.css` — Stern/Sprungliste/Häkchen (A) **und** `.eyebrow` (B).
- `lib/load.mjs` — reine A-Themen (Glyph, Öffnungszeiten, `featured=state`).

## Nicht jetzt (nach dem Start entscheiden)

Der einmalige Rückport ins Template, eine laufende Paritätsprüfung und der Umbau auf geteilten Code
(Build bezieht den Code aus dem Template, nur `src/data/` unterscheidet sich) sind **nicht** gebaut.
Das wird nach dem Start entschieden. Bis dahin hält die Sperre in `scripts/init_site.py` die geladene
Waffe gesichert.

## Siehe auch
[[master-template]] · [[konventionen]]
