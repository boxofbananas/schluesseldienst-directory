# Premium-Band: eine Frei-Karte je Stadt, und Rückport ins Template

**Datum:** 2026-11-10
**Zwei Nacharbeiten** zum Stadt-Premium (drei Plätze, Buchungsreihenfolge).

## 1. Nur eine „Dieser Platz ist frei"-Karte je Stadt

Verkaufte Plätze werden alle gezeigt; dahinter höchstens **eine** Frei-Karte, auch wenn zwei oder
drei offen sind. Grund: auf fast allen 787 Stadtseiten ist kein Platz verkauft — drei leere
Werbekarten über den Einträgen machen aus einer Verzeichnisseite eine Anzeigenseite, für Besucher
wie für Google.

- `FeaturedBand.astro`: statt `slots − shown.length` Frei-Karten wieder **eine**
  (`{shown.length < slots && …}`). Der Text sagt weiterhin, dass es bis zu drei Plätze gibt und
  die Reihenfolge der Buchung folgt; nur der Platz wird nicht mehr mehrfach freigehalten.

### Drei Fälle geprüft
- **Live Mannheim** (ein Platz verkauft): Merz oben + **eine** Frei-Karte.
- **Live Leipzig** (kein Verkauf): **eine** Frei-Karte.
- **Lokal drei verkauft** (Mannheim, zwei Testplätze dazu, Build ohne Deploy): drei Karten,
  **null** Frei-Karten. CSV danach zurückgesetzt (die Spalte `featured_seit` ist jetzt committet,
  `git checkout` stellt den Merz-Stand sauber wieder her).
- `check_live.py … --expect-urls 2823`: alle Prüfungen bestanden; danach sauber ausgeliefert.

## 2. Rückport ins Template (nach [[template-build-drift]])

Vorgezogen auf Anweisung, nach den Regeln der Seite (gemischte Dateien hunkweise,
branchenspezifisches bleibt im Build):

- `components/FeaturedBand.astro` — die Template-Fassung unterschied sich nur in der
  Frei-Kartentextzeile (Slot-Logik und `Star`-SVG waren schon gleich). Textzeile übernommen →
  **Template == Build**.
- `lib/load.mjs` — als gemischte/rein-A-Datei **hunkweise**: `featuredSince`-Einlesen,
  `orderFeaturedBand()` und der Aufruf an `city.featured`. Die übrigen Template-Rückstände
  (Glyph, Öffnungszeiten, `featured=state`) bleiben wie gehabt offen und werden erst beim
  nächsten Verzeichnis gesammelt portiert.
- `pages/premium.astro` — rein generisch (alles über `site.*`), die aktuelle /premium/-Fassung
  ganz übernommen → **Template == Build**.

Die CSV-Spalte `featured_seit` liest `load.mjs` tolerant; ein künftiges Verzeichnis braucht sie
erst beim ersten Stadt-Premium, und `scripts/verkauf.py` legt sie dann selbst an.

`templates/astro/src/lib/load.mjs` syntaktisch geprüft (`node --check`). FeaturedBand und
premium.astro sind zwischen Template und Build jetzt bytegleich.

### Wiki fortgeschrieben
`wiki/framework/template-build-drift.md`: `updated` auf 2026-11-10, Abschnitt „Ausnahme, bereits
zurückportiert (2026-11-10)" ergänzt, neue Sorte-A-Zeile „Stadt-Premium: bis zu drei Plätze,
Buchungsreihenfolge (✓ zurückportiert)".
