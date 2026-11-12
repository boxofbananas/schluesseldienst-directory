# Sortierung offenlegen, Premium aus Stufe 0, Sterne auf /suche/ (Nacharbeiten)

**Datum:** 2026-11-12 · **Branch:** `main` (live) · **Projekt:** `schluesseldienste-deutschland`

## 1. Die Sortierregel offengelegt

Seit heute stehen Einträge mit Festpreis-Garantie vor den übrigen; die Seite sagte das nirgends,
und `/premium/` behauptete noch, die Stadtseiten ordneten nur nach Bewertung. Berichtigt:

- **Stadtseite**, sichtbare Zeile direkt unter „Die besten … in …": „Zuerst die Premium-Plätze und
  bezahlten Top-Platzierungen, dann Betriebe mit Festpreis-Garantie, danach alle übrigen nach
  Bewertung und Anzahl der Bewertungen." (`<p class="sort-note meta">`). Live bestätigt.
- **Stadtseite**, Ersatz-Vorspann (Städte ohne eigenen Stadttext): um die Festpreis-Garantie-Stufe
  ergänzt.
- **/festpreis-garantie/**: ein Absatz, dass ein Betrieb mit Festpreis-Garantie auf seiner Stadtseite
  vor den Betrieben ohne steht (hinter den bezahlten Plätzen, vor der übrigen Liste), dass die
  Platzierung kostenlos und nicht kaufbar ist und innerhalb der Gruppe die Bewertung entscheidet.
- **/premium/**: der Satz zur Ordnung der Stadtseiten (lede) berichtigt; zusätzlich die
  Stadt-Premium-Beschreibung („über der übrigen Liste (Betriebe mit Festpreis-Garantie, dann nach
  Bewertung)").

**Textgate:** Alle drei Seiten geprüft — **meine Zusätze führen keinen neuen Verstoß ein** (Vergleich
gegen HEAD identisch). Die Stadtseite besteht die Wort- und Rechtswort-Prüfung **ohne**
`--erlaube-rechtswoerter`; der Programmname „Festpreis-Garantie" ist frei, kein „garantiert"/„Garantie"
allein. Die als „durchgefallen" gemeldeten Punkte sind **vorbestehend** und nicht von diesen Edits:
`branche_im_ersten_absatz` (Artefakt beim Linten einer `.astro` — die Branche steht als Variable
`{site.niche.plural}`, die der gebaute HTML-Text sehr wohl im ersten Absatz trägt), das Betrugszitat
„ab 49 Euro" auf `/festpreis-garantie/` und die 11 Gedankenstriche derselben Seite (ich hatte dort
versehentlich einen zwölften gesetzt und wieder entfernt).

### Weitere Stellen, die die alte Reihenfolge behaupten — zur Entscheidung

Gesucht in Über uns, Fragen, Ratgeber und darüber hinaus. Gefunden, **noch nicht geändert** (du
wolltest sie genannt bekommen):

1. **Bundesland-Seite**, lede (`verzeichnis/[bundesland]/index.astro:50`): „Jede Stadtseite ordnet die
   Betriebe nach Bewertung und Anzahl der Bewertungen; bezahlte Platzierungen sind gekennzeichnet."
   → **klar betroffen**, sollte die Festpreis-Garantie-Stufe nennen. Empfehlung: berichtigen.
2. **Premium-Band** (`components/FeaturedBand.astro:37`): „… im Premium-Band über der nach Bewertung
   sortierten Liste …" → beschreibt die Liste als „nach Bewertung sortiert"; nur noch halb richtig.
   Klein.
3. **Stadtseite, Meta-Description** (`[stadt]/index.astro:25`): „geordnet nach Bewertung und Anzahl
   der Bewertungen" → SEO-Kurzfassung, nicht sichtbarer Fließtext. Klein.

**Geprüft und korrekt (kein Fix):**
- **Über uns** (`ueber-uns.astro:30`): „ordnet … nach Bundesland und Stadt" — geografische Ordnung,
  keine Aussage über die Reihenfolge innerhalb einer Stadt.
- **Startseite, Bestbewertete-Liste** (`DirectoryHub.astro:48`): „Geordnet nach der Google-Bewertung…"
  — diese kuratierte Liste ist tatsächlich rein nach Bewertung (bezahlte und geprüfte Einträge sind
  ausgeschlossen), die Aussage stimmt.
- **Leistungsseiten** (`leistungen/[…slug].astro`): „nach der Google-Bewertung geordnet" — die Liste
  wird dort rein nach `score` sortiert (`load.mjs:519`), nicht über `sortListings`; geprüfte Einträge
  steigen hier nicht auf. Stimmt.
- **FAQ** (attributeFaqs) und **Ratgeber**: keine Aussage zur Reihenfolge gefunden.

## 2. `premium` aus der obersten Sortierstufe genommen

`sortListings`: `isFeaturedIn(…) || l.bestOfRank > 0 || l.premium ? 0 : …` → `|| l.premium` entfernt.
Stufe 0 sind jetzt nur **Stadt-Premium** (`featured`, über `isFeaturedIn`) und **Top-Platzierung**
(`bestOfRank`). Der Premium-Eintrag wird als Bilder, Links und Karte verkauft, nicht als Platzierung,
und ordnet sich nach seiner Bewertung ein. Im Build **und** im Template, mit erneuertem Kommentar.

**Mannheim unverändert:** Merz hält das Stadt-Premium über `featured='city'` (nicht über `premium`),
`isFeaturedIn(Merz, mannheim)` bleibt wahr → Stufe 0. Erste drei Karten weiter Merz, AES, Key Walter,
Merz weiter im Premium-Band. In der ganzen CSV gibt es **keinen** Eintrag, der nur `premium=true`
trägt (ohne `featured`/`best_of_rank`), also verschiebt die Änderung in den aktuellen Daten nichts;
sie greift erst, falls künftig ein reiner Premium-Eintrag verkauft wird.

## 3. Sterne auf /suche/

`public/search.js` zeichnete die Bewertung mit den Textzeichen `★`/`☆` (`★`/`☆`), die der
selbst gehostete Schrift-Auszug nicht enthält (Tofu, wo keine System-Symbolschrift da ist). Beide
Render-Pfade (`stars()` für die Ergebniskarte, `ratingHtml()` für die Vorschlagsliste) stellen jetzt
dasselbe Inline-SVG wie `components/Star.astro` dar, an Schriftgröße (`1em`) und -farbe (umgebende
`.rating .stars` / `.suggest .rt .star`) gekoppelt. Im Build **und** im Template.

**Live geprüft** (`/suche/?s=Key Walter Mannheim`): 1 Treffer, Key Walter sichtbar, **fünf goldene
SVG-Sterne** in der Ergebniskarte, kein Textzeichen mehr.

## Bauen, Ausliefern, Prüfen

`npm run build` grün (Glyph-Prüfung grün, Sitemap 2823), `wrangler pages deploy`,
`check_live.py … --expect-urls 2823` **alle Prüfungen bestanden**. Template baut eigenständig durch.
Live bestätigt: Mannheim-Sortierzeile, `/premium/`-lede, `/festpreis-garantie/`-Absatz, SVG-Sterne in
der Suche.

## Offen

- Die drei genannten „weiteren Stellen" (Bundesland-lede, FeaturedBand, Meta-Description) auf Zuruf.
- Gruppe 3 der Sortierung (Ortsvorwahl↔PLZ) weiter ausgelassen bis zur Referenztabelle.
