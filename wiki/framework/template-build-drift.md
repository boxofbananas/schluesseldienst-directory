---
title: Template und Build driften
type: framework
status: current
updated: 2026-11-10
---

# Template und Build driften

Jedes Verzeichnis entsteht so: Gate 5 kopiert `templates/astro/` nach `output/<slug>/site/` und
füllt die Daten ([[master-template]]). Die Kopie ist eine **Momentaufnahme**. Danach passiert alle
echte Arbeit im Build, und nichts davon fließt zurück ins Template. Das Template veraltet ab dem
Moment, in dem nach dem Kopieren weiterentwickelt wird.

**Für dieses Verzeichnis ist der Build die Wahrheit, nicht das Template.** Wer hier etwas ändert,
ändert es im Build (`output/schluesseldienste-deutschland/site/`). Das Template wird erst wieder
angefasst, **wenn ein zweites Verzeichnis entsteht** — dann wird nach der Liste unten zurückportiert.

**Ausnahme, bereits zurückportiert (2026-11-10).** Auf Anweisung vorgezogen, nach den Regeln
dieser Seite (gemischte Dateien hunkweise, branchenspezifisches bleibt im Build):

- `components/FeaturedBand.astro` — nur eine Frei-Karte je Stadt (nicht eine je offenem Platz),
  Frei-Kartentext auf „bis zu drei … in der Reihenfolge der Buchung". **Template == Build.**
- `lib/load.mjs` — neues A-Thema `orderFeaturedBand` samt `featuredSince`-Einlesen und dem Aufruf
  an `city.featured` (hunkweise übernommen; die übrigen Template-Rückstände bleiben offen).
- `pages/premium.astro` — die aktuelle /premium/-Fassung (Stadt-Premium = einer von bis zu drei
  Plätzen nach Buchung, Brutto-/USt-Zeile). Rein generisch, ganz übernommen. **Template == Build.**
- `lib/load.mjs` — die beiden **Fehlerbehebungen** hunkweise: `sanitizeGlyphs` + `GLYPH_OK`
  (Emoji/Fremdschrift aus Freitext, angewandt auf `name`, `address`, `street`, `description`) und
  die Öffnungszeiten-Behandlung in `normalizeHours` (DataForSEO-Array → Text, behebt
  „[object Object]"; ein leerer Tag ergibt „Geschlossen").
- `styles/fonts.css` — die latin-ext-Importe aus demselben Glyph-Thema (europäische Namen wie ẞ,
  Š/š, İ, ş, ů, die der reine Latin-Auszug nicht abdeckt). Damit ist das Glyph-Thema **vollständig**
  zurückportiert. **Template == Build.**

Die neue CSV-Spalte `featured_seit` liest `load.mjs` tolerant (`r.featured_seit || ''`); ein
künftiges Verzeichnis braucht sie erst beim ersten Stadt-Premium, und `scripts/verkauf.py` legt
sie dann selbst an.

**Bewusst nicht portiert (2026-11-10):** das Startseiten-Band **nur aus `featured=state`**
(`homeFeatured` in `lib/load.mjs`). Das ist keine Fehlerbehebung, sondern eine **Entscheidung
dieses Verzeichnisses** ([[footprint-rules]]): national speist nur die oberste Stufe das Band,
damit kein Stadt-/Umland-Platz die Startseite gratis dazubekommt und kein eigener Betrieb ohne
veröffentlichten Preis national oben steht. Ein künftiges Verzeichnis trifft diese Wahl neu;
deshalb bleibt der Template-Stand (alle Stufen speisen das Band) absichtlich erhalten. Ebenfalls
offen und hier nicht angefasst: die BOM-Regex in `parseCsv` und `/danke/` in den `noindexPaths`.

**Design-Pilot 1 — freigegeben, nach `main` gemergt und ins Template zurückportiert (2026-11-12).**
Ein sichtbarer Gestaltungs-Pilot für Startseite und Stadtseite (Auftrag
`output/schluesseldienste-deutschland/design-pilot1/`). Layout- und Komponentenarbeit auf den
bestehenden Marken (Farben/Schriften unverändert), plus vier neue/geänderte Marken (`--card-radius`,
`--card-shadow`, `--space-section`, `buttonRadius`=Pille; siehe `04-plan.md`). Daniel hat den Pilot
freigegeben; `design/pilot1` ist nach `main` gemergt, gebaut, ausgeliefert und live geprüft
(`check_live.py` 2823 grün). Der Branch bleibt stehen.

Die **Gestaltung** ist nach den Regeln dieser Seite **hunkweise** ins Template zurückportiert — nur
die pilot-eigenen Hunks (Fork `11f8445` → `2c1e118`), die aufgeschobene Vor-Pilot-Drift (Star-SVG an
den Text-Stern-Stellen, Sprungliste, `Check.astro`, Augenbraue, Überschrift-B, kürzerer
Such-Platzhalter, „Alle Städte", entfernte Herausgeber-Zeile) blieb außen vor. **Template == Build**
für die Pilot-Gestaltung. Portierte Dateien:

- `templates/astro/src/data/site.json` (vier Marken in `design`: `buttonRadius`=999px, `cardRadius`,
  `cardShadow`, `spaceSection`)
- `templates/astro/src/layouts/Base.astro` (die drei neuen CSS-Variablen; Kopfzeilen-Navigation als
  zugängliches Checkbox-Menü). Die aufgeschobene Drift derselben Datei (Herausgeber-Zeile, „Alle
  Städte") blieb unangetastet.
- `templates/astro/src/styles/global.css` (Pilot-1-Block angehängt: Karten, Fokusring, Suche,
  Hero-Zweispalt, Stadt-Ergebnisbereich/Zeilenkarten, mobiles Menü; dazu `select` in der
  Formularregel)
- `templates/astro/src/pages/index.astro` (Hero zweispaltig + Übersichtskarte; **Template-Überschrift
  A bleibt**, keine Augenbraue, kein `Check`)
- `templates/astro/src/pages/verzeichnis/[bundesland]/[stadt]/index.astro` (zweigeteilter
  Ergebnisbereich mit Orientierungsspalte; **Template behält** `cards.map` ohne `id` und den
  Text-Stern der „weiteren"-Liste)
- `templates/astro/src/components/SearchForm.astro` (Lupe als SVG, optionale sichtbare Beschriftung;
  **Template behält** den längeren Platzhalter)
- `templates/astro/src/components/Card.astro` (Kartenfußzeile mit „Eintrag ansehen")

**Nebenbefund, dabei behoben:** Das Template war seit dem FeaturedBand-Rückport (2026-11-10)
**nicht mehr baubar** — `components/FeaturedBand.astro` importiert `./Star.astro`, das nie mitportiert
wurde (Sorte A, „Bewertungsstern als SVG", bis dahin aufgeschoben). Da `FeaturedBand` die Komponente
bereits voraussetzt, ist `components/Star.astro` jetzt mitportiert (die `.star`-CSS steckt im
Pilot-Block). Der breitere Stern-Umbau (`.rt i` → `.rt .star` an den übrigen Stellen, `Rating.astro`
usw.) bleibt weiter aufgeschoben; jene Stellen tragen bis dahin den Text-Stern. Danach baut
`templates/astro` wieder eigenständig durch (`npm run build`, „[build] Complete!"; die
„Pflichtangaben"-Zeile zum fehlenden `formEndpoint` ist die erwartete Platzhalter-Warnung).

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
| **Glyph-Bereinigung + latin-ext** (Emoji/Fremdschrift raus, europäische Namen rein) **✓ vollständig zurückportiert 2026-11-10** | `lib/load.mjs` (`sanitizeGlyphs`, `GLYPH_OK`) und `styles/fonts.css` (latin-ext-Importe) — **Template == Build** |
| **Öffnungszeiten-Fix** (DataForSEO-Array → Text, behebt „[object Object]") | `lib/load.mjs` (`normalizeHours`, Array-Zweig) **✓ zurückportiert 2026-11-10** |
| **Merkmalsanzeige: nur bestätigt** (kein „nein", keine „keine-Angabe"-Zeile) | `components/AttributeGrid.astro`, `pages/firma/[bundesland]/[stadt]/[slug]/index.astro` (Abschnitt nur bei vorhandenen Merkmalen) |
| **Sprungliste** auf Stadtseiten | `pages/verzeichnis/[bundesland]/[stadt]/index.astro`, `styles/global.css` (`.jump-list`), `components/Card.astro` (`id`-Prop für Anker) |
| **Startseiten-Band nur aus `featured=state`** | `lib/load.mjs` (`homeFeatured`), `components/DirectoryHub.astro` (Preis-Prop) — **bewusst NICHT portiert (2026-11-10):** Entscheidung dieses Verzeichnisses, keine Korrektur (siehe oben, [[footprint-rules]]) |
| **Startseite ohne volle Städteliste** (A–Z ausgelagert auf `/verzeichnis/`) | `components/DirectoryHub.astro`, `layouts/Base.astro` (Fußzeile „Alle Städte") |
| **Suchfeld-Platzhalter** (kürzer) | `components/SearchForm.astro` |
| **KV-Formularannahme** (Cloudflare KV + Email Routing, kein externer Formulardienst) | `functions/api/` (ganzer Ordner, nur im Build), gespiegelt in den Datenschutztexten (Sorte B) |
| **Stadt-Premium: bis zu drei Plätze, Buchungsreihenfolge** (✓ zurückportiert 2026-11-10) | `components/FeaturedBand.astro`, `lib/load.mjs` (`orderFeaturedBand`, `featuredSince`), `pages/premium.astro`, CSV-Spalte `featured_seit` (von `scripts/verkauf.py` gepflegt) |

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
