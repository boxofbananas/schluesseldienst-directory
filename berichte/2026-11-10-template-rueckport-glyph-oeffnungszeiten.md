# Rückport ins Template: sanitizeGlyphs und normalizeHours

**Datum:** 2026-11-10
**Ziel:** Die beiden Fehlerbehebungen aus dem Build nach `templates/astro/` zurücktragen, nach den
Regeln aus [[template-build-drift]] (hunkweise, branchenspezifisches bleibt im Build). Das
`featured=state`-Band bleibt draußen — das ist eine Entscheidung dieses Verzeichnisses, keine
Korrektur.

## Genommene Hunks (`templates/astro/src/lib/load.mjs`)

**sanitizeGlyphs (Glyph-Bereinigung)**
- Definition `GLYPH_OK` + `function sanitizeGlyphs(...)` (neuer Block nach `slugify`).
- Angewandt auf `description` sowie `name`, `address`, `street` im Rückgabeobjekt (4 Aufrufe).

**normalizeHours (Öffnungszeiten)**
- Der `Array.isArray(v)`-Zweig: DataForSEO-Array `[{open,close}, …]` → „08:00–17:30"; leeres Array
  → „Geschlossen"; einzelnes 00:00–24:00 → „Durchgehend geöffnet". Behebt „[object Object]".
- `if (!s) return ''` → `return 'Geschlossen'` (ein als `null` geschriebener Ruhetag), mit den
  erklärenden Kommentaren.

## Bewusst draußen gelassen

- **`homeFeatured` / Startseiten-Band nur aus `featured=state`** — keine Fehlerbehebung, sondern
  eine Entscheidung dieses Verzeichnisses ([[footprint-rules]]): national speist nur die oberste
  Stufe das Band. Ein künftiges Verzeichnis trifft die Wahl neu, deshalb bleibt der Template-Stand
  (alle Stufen speisen das Band) erhalten.
- Nicht genannt und darum unangetastet: die BOM-Regex in `parseCsv` und `/danke/` in den
  `noindexPaths`. Ebenfalls noch offen: die `fonts.css`-latin-ext-Importe aus dem Glyph-Thema.

## Prüfung

- Verbleibender Diff `load.mjs` Template↔Build: **nur** die drei bewusst ausgelassenen Hunks
  (BOM, `featured=state`, `/danke/`).
- `node --check` grün (Template und Build).
- Funktionstest der Template-Fassung: `normalizeHours` liefert „08:00–17:30", „Geschlossen",
  „Durchgehend geöffnet", „Geschlossen" (leerer String); `sanitizeGlyphs` definiert und an vier
  Feldern verdrahtet.
- Der Build ist unverändert; die Live-Seite wurde nicht angefasst, kein Deploy nötig.

## Wiki fortgeschrieben

`wiki/framework/template-build-drift.md`:
- Abschnitt „bereits zurückportiert (2026-11-10)" um die zwei Fehlerbehebungen ergänzt
  (`fonts.css`-latin-ext ausdrücklich als noch offen vermerkt).
- `featured=state` ausdrücklich als **bewusst nicht portiert** festgehalten, mit Grund.
- Sorte-A-Tabelle: Glyph- und Öffnungszeiten-Zeile mit „✓ zurückportiert 2026-11-10",
  `featured=state`-Zeile mit „bewusst NICHT portiert".
