# Design-Pilot 1: Freigabe, Merge, Ausliefern, Template-Rückport (Teil B)

**Datum:** 2026-11-12 · **Branch:** `design/pilot1` → `main` (gemergt, live) · **Projekt:**
`schluesseldienste-deutschland`

Teil B begann erst, nachdem Teil A live und grün war.

## 1. `main` in `design/pilot1` geholt, Konflikte von Hand gelöst

`main` (Teil A) in `design/pilot1` gemergt. Die Stadtseite war in beiden Zweigen geändert; der
Merge löste sie **automatisch korrekt** auf — ich habe das geprüft, nicht blind übernommen:
`gridCards = cards` (A2, aus `main`) steht im Pilot-Zweispalten-Layout (`city-results-main` zuerst,
dann `city-orient`). Mannheim-Raster im Branch-Build: **Merz, AES, Key Walter**, keine doppelten
`id`. `load.mjs` kam mit der neuen Sortierung sauber herüber. Von Hand gelöst:

- `wiki/log.md` — beide Einträge behalten.
- `04-plan.md` — der Auto-Merge hatte eine **doppelte** „## Gestaltungsmarken"-Überschrift erzeugt;
  zusammengeführt, Entscheidung A2 und Pilot-Nachtrag beide erhalten.

Build grün, Glyph-Prüfung grün. Merge-Commit auf dem Branch.

## 2. Screenshot-Prüfung im Branch (vor dem Merge nach `main`)

Desktop 1440 und mobil 390 von acht Seitentypen: Mannheim (mit Merz/AES oben), Bundesland-Seite,
Eintrag **mit** Garantie (Merz Sicherheit), Eintrag **ohne** Garantie (Key Walter), eine
Ratgeberseite, `/premium/`, `/festpreis-garantie/antrag/`, `/suche/` mit einem Treffer. Je Seite:
Kopfzeile, mobiles Menü auf/zu, Knöpfe, Karten, Überlauf 320–1440.

**Ergebnis: keine Pilot-bedingten Brüche.** Alle acht Seiten ohne Überlauf bei 320/390/768/1024/1440,
mobiles Menü klappt überall auf und zu (`none→flex→none`), je genau ein H1. Die Pilot-Marken
(Karten-Radius/-Schatten, Pillen-Knöpfe, Fokusring, Pillen-Suche mit Lupe, zugängliches Menü) greifen
auf allen Seitentypen, auch den im Pilot nicht eigens gestalteten (Eintrag, Formulare, Ratgeber,
Premium) — sie erben sie über die Marken und `global.css`.

**Ein Befund, vorbestehend, nicht Pilot:** In den Ergebniskarten von `/suche/` erscheinen die
Bewertungssterne als leere Kästchen (Tofu). Ursache: `public/search.js` baut die Bewertung mit den
**Textzeichen** `★`/`☆` (`★`/`☆`), die der selbst gehostete Schrift-Auszug bewusst nicht
enthält (dafür gibt es `components/Star.astro` als SVG). Das ist **nicht** vom Pilot verursacht —
`search.js` ist im Pilot-Branch unverändert und auf `main` zeichengleich (zwei Vorkommen in
`public/search.js:30` und `:70`). Auf Geräten mit System-Symbolschrift erscheinen echte Sterne, nur
wo keine vorhanden ist, das Kästchen. Ich habe den Merge deshalb **nicht blockiert** und die Datei
nicht im Zuge des Pilots angefasst. **Vorschlag:** als eigener kleiner Fix (wie Teil A) die beiden
Stellen in `public/search.js` auf dasselbe Inline-SVG wie `Star.astro` umstellen; sag Bescheid, dann
mache ich das separat.

## 3. `design/pilot1` → `main`, ausgeliefert, live geprüft

Fast-Forward-Merge nach `main` (der Branch enthielt `main` bereits). Gebaut (grün, Glyph-Prüfung
grün, Sitemap 2823), mit `wrangler pages deploy` ausgeliefert (4648 Dateien),
`check_live.py … --expect-urls 2823`: **alle Prüfungen bestanden**.

Live gegen `die-besten-schluesseldienste.de` geprüft (Playwright):

- **Startseite** lädt, H1 vorhanden, **keine** Fremd-Host-Anfrage.
- **Mannheim**: erste drei Listenkarten `b-merz-…`, `b-aes-…`, `b-key-walter-…` (A2 + Sortierung
  live), keine Fremd-Hosts.
- **Eintrag mit Garantie (Merz)**: Karten-Platzhalter „Karte von Google Maps" da, **keine
  Fremd-Host-Anfrage vor dem Klick** (Einwilligung greift).
- **Beide Formulare** liefern Felder (`/eintrag-beanspruchen/` 12, `/festpreis-garantie/antrag/` 33).
- **Suche** `/suche/?s=Key Walter Mannheim`: **1 Treffer**, Key Walter sichtbar.
- **Keine Anfrage an einen fremden Host ohne Klick** über alle geprüften Seiten (Schriften selbst
  gehostet, kein Google).

## 4. Rückport der Gestaltung ins Template (`templates/astro/`)

Nach den Regeln in [[template-build-drift]]: **hunkweise**, nur die pilot-eigenen Hunks (isoliert als
Diff Fork `11f8445` → `2c1e118`), aufgeschobene Vor-Pilot-Drift blieb außen vor. Portiert:
`site.json` (vier Marken), `Base.astro` (CSS-Variablen + Checkbox-Menü), `global.css` (Pilot-Block +
`select`-Regel), `index.astro` (Hero zweispaltig + Übersichtskarte, Überschrift A bleibt),
Stadtseite (zweigeteilter Ergebnisbereich, `cards.map` ohne `id`/Text-Stern bleibt), `SearchForm.astro`
(Lupe + Label, langer Platzhalter bleibt), `Card.astro` (Kartenfußzeile).

**Nebenbefund, dabei behoben:** Das Template war seit dem FeaturedBand-Rückport (2026-11-10) **nicht
mehr eigenständig baubar** — `FeaturedBand.astro` importiert `./Star.astro`, das nie mitportiert
wurde. Da eine bereits portierte Datei die Komponente voraussetzt, ist `Star.astro` jetzt mit
dabei (die `.star`-CSS steckt im Pilot-Block). Danach baut `templates/astro` wieder durch
(`npm run build` → „[build] Complete!"; die „Pflichtangaben"-Zeile zum fehlenden `formEndpoint` ist
die erwartete Platzhalter-Warnung). Die Startseite des Template-Builds rendert die Pilot-Struktur
(hero-split, Übersichtskarte, Checkbox-Menü, `--card-radius:22px`). Stadtseiten entstehen im
Template-Build nicht, weil die mitgelieferten Platzhalterdaten keine Städte enthalten; die Stadtseite
ist strukturgleich zum live geprüften Build.

Der [[template-build-drift]]-Eintrag „Design-Pilot 1" steht auf dem neuen Stand (freigegeben,
gemergt, portiert; Star.astro-Nebenbefund dokumentiert).

## 5. Aufräumen

Worktree `blueprint-pilot1` entfernt, Branch `design/pilot1` steht. 

## Offen / zur Entscheidung

- **`public/search.js`-Sterne** (Tofu in Suchergebnissen) — vorbestehend, als eigener kleiner Fix auf
  Abruf.
- **Voller Stern-SVG-Umbau** im Template (`.rt i` → `.rt .star` an den übrigen Stellen) bleibt
  aufgeschoben (Sorte A); bis dahin tragen jene Stellen den Text-Stern.
