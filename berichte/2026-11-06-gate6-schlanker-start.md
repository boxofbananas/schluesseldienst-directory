# Gate 6 — schlanker Start: Ist-Stand und Startplan

**Datum:** 2026-11-06
**Auslöser:** Daniel — Gate 6 beginnen: Ist-Stand erheben (noindex, Sitemap, Seitenzahlen je
Ebene), `featuredPreview` prüfen, `06-launch.md` schreiben. **Noch nichts an der Sitemap ändern.**

Ergebnis: `output/schluesseldienste-deutschland/06-launch.md`. Dieser Bericht fasst den Ist-Stand
und den einen Befund zusammen, der eine Entscheidung braucht.

## Ist-Stand (nichts geändert)

Build 4646 Seiten, Sitemap 2806 Adressen.

| Ebene | gebaut | Sitemap | noindex |
|---|---:|---:|---:|
| Startseite | 1 | 1 | – |
| Vertrauensseiten (`/ueber-uns/`, `/festpreis-garantie/`) | 2 | 2 | – |
| Bundesland-Seiten | 16 | 16 | – |
| Stadtseiten | 787 | 577 (≥ 2 Einträge) | 210 (Einzeleintrag) |
| Leistungsseiten (6 + Index) | 7 | 7 | – |
| Ratgeber (5 + Index) | 6 | 6 | – |
| Eintragsseiten | 3799 | 2197 (`thin=false`) | 1602 (`thin=true`) |
| Garantie-Nachweise `/auszeichnung/` | 18 | – | 18 |
| Formular-/Pflichtseiten | ~12 | – | ~11 |
| **Summe** | **4646** | **2806** | **1840** |

**`featuredPreview` im ausgelieferten Build: `false`** — 0 Vorschau-Karten (`data-preview="1"`)
im gesamten `dist`, 804 Seiten mit „Dieser Platz ist frei". Zusätzlich bestätigt: `404.html` und
`_headers` (pages.dev-`noindex`) im Build, www-Umleitung live.

## Der Befund: 17 der 18 Garantie-Seiten stehen auf `noindex`

`load.mjs:550` setzt `thin && !claimed && !optimized` auf `noindex`. 17 der 18 geprüften Betriebe
sind `thin` (unter 5 Bewertungen) und weder beansprucht noch bezahlt platziert — sie fallen damit
aus der Sitemap. Nur Merz Sicherheit Mannheim (355 Bewertungen, Premium-Platz) ist drin. Das
widerspricht der Vorgabe „die 18 gehören in die erste Stufe".

**Vorgeschlagene Lösung** (im Plan als den Start sperrende Vorbedingung, **noch nicht umgesetzt**):
eine geprüfte Seite wird nie wegen `thin` auf `noindex` gesetzt — Ergänzung `&& !l.geprueft` in
`load.mjs:550`, gespiegelt ins Template. Sitemap danach 2806 → 2823. Die `/auszeichnung/`-Seiten
bleiben `noindex`.

## Der Plan (`06-launch.md`)

- **Indexierungsplan ohne Search Console und ohne Analytics:** Sitemap über `robots.txt`,
  **IndexNow** (Bing/Yandex, kein Google-Dienst; Cloudflare „Crawler Hints"), interne
  Verlinkung. Messung über die **Cloudflare-Auswertung** des eigenen Kontos und `site:`-Stichproben
  — kein Zählpixel, keine GSC-Property.
- **Geordnete Adressliste:** Startseite → 18 Garantie-Seiten → 16 Bundesländer → Vertrauensseiten
  → Leistungs-/Ratgeberseiten → Stadtseiten größte→kleinste (Mannheim zuerst) → übrige
  `thin=false`-Einträge nach Bewertung.
- **Erweiterungsstufen:** Stufe 1 der ganze Sitemap-Bestand; dann alle 30 Tage dünne Einträge der
  größten Städte (beanspruchte zuerst), die 210 Einzeleintrag-Stadtseiten in Tranchen, danach nach
  Bundesländern mit dem stärksten Zuwachs.
- **30-Tage-Prüfung:** Starttag der Staffel + 30 Tage; bei Start am 2026-11-07 Prüfung am
  2026-12-07.

## Offen (Betreiber / Freigabe)

- Freigabe des Ist-Stands, dann die `geprueft`-Ausnahme umsetzen, neu bauen, ausliefern.
- IndexNow im eigenen Cloudflare-Konto aktivieren; Starttag der Staffel festlegen; `datePublished`
  an dem Tag setzen.
- Mit leerem Browserprofil prüfen, dass ohne Klick keine Anfrage an Google geht.

Keine Sitemap-Änderung in diesem Schritt vorgenommen.
