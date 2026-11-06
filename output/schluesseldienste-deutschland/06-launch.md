# Gate 6 — Schlanker Start

**Verzeichnis:** Die besten Schlüsseldienste · `die-besten-schluesseldienste.de`
**Stand:** 2026-11-06 · Build 4646 Seiten, Sitemap 2806 Adressen · Domain und www-Umleitung live
**Grundlage:** [[launch-lean]], [[footprint-rules]], [[siegel-programm]]

Die Domain ist bereits ausgeliefert und erreichbar; was aussteht, ist die **gestaffelte
Einreichung** (der Dripfeed). Dieses Dokument legt sie fest.

---

## 1. Ist-Stand (erhoben, nichts geändert)

| Ebene | gebaut | in Sitemap | noindex / außerhalb |
|---|---:|---:|---:|
| Startseite | 1 | 1 | – |
| Vertrauensseiten (`/ueber-uns/`, `/festpreis-garantie/`) | 2 | 2 | – |
| Bundesland-Seiten | 16 | 16 | – |
| Stadtseiten | 787 | 577 (≥ 2 Einträge) | 210 (Einzeleintrag, eigenständig) |
| Leistungsseiten (6 + Index) | 7 | 7 | – |
| Ratgeberseiten (5 + Index) | 6 | 6 | – |
| Eintragsseiten | 3799 | 2197 (`thin=false`) | 1602 (`thin=true`) |
| Garantie-Nachweise `/auszeichnung/` | 18 | – | 18 |
| Formular- und Pflichtseiten | ~12 | – | ~11 |
| **Summe** | **4646** | **2806** | **1840** |

**Geprüft:**
- `featuredPreview` im ausgelieferten Build ist **`false`** — 0 Vorschau-Karten (`data-preview="1"`)
  im gesamten `dist`, 804 Seiten mit „Dieser Platz ist frei".
- `dist/404.html` vorhanden (sonst behandelt Cloudflare die Site als Einzelseitenanwendung).
- `dist/_headers` setzt `X-Robots-Tag: noindex` auf `:project.pages.dev` und Vorschauadressen.
- www-Umleitung live (301, Pfad und Query erhalten).
- Stellschrauben: `cityFloor=2`, `foldMaxKm=30`, `cityMinPopulation=20000`, `launchDate=2026-11-03`.

---

## 2. Startsperre: die 18 Garantie-Seiten müssen in die erste Stufe

**Problem.** `load.mjs:550` setzt `thin && !claimed && !optimized` auf `noindex`. 17 der 18
Betriebe mit Festpreis-Garantie sind `thin` (unter 5 Bewertungen) und weder beansprucht noch
bezahlt platziert — sie stehen damit **aktuell auf `noindex`** und fehlen in der Sitemap. Nur Merz
Sicherheit Mannheim (355 Bewertungen, Premium-Platz) ist drin. Die Garantie-Seiten sind aber die
stärksten Seiten des Verzeichnisses und gehören in die erste Stufe.

**Lösung (vor der ersten Einreichung umzusetzen).** Eine geprüfte Seite wird nie wegen `thin` aus
der Sitemap genommen. In `load.mjs` (Build **und** `templates/astro/`):

```
for (const l of listings) if (l.thin && !l.claimed && !l.optimized && !l.geprueft) noindexPaths.add(l.path);
```

Danach neu bauen und ausliefern. Die Sitemap wächst um die 17 Seiten: **2806 → 2823**. Die
`/auszeichnung/`-Nachweisseiten bleiben `noindex` (sie sind Beleg, kein Inhalt). Diese Änderung
ist **noch nicht vorgenommen** — sie wartet auf die Freigabe des Ist-Stands.

---

## 3. Indexierungsplan — ohne Search Console, ohne Analytics

Zwei Projektvorgaben ([[footprint-rules]]): **keine Google Search Console** und **kein Google
Analytics** auf dieser Domain. Der Plan kommt ohne beides aus.

**Wie Seiten gefunden werden:**
1. **Sitemap über `robots.txt`.** `robots.txt` nennt die `sitemap.xml` bereits (von außen
   bestätigt). Google und Bing entdecken darüber den Startbestand ohne angemeldetes Konto.
2. **IndexNow** (Bing, Yandex u. a.) als aktiver Anstoß — kein Google-Dienst, keine Search
   Console, kein Tracking. Cloudflare bietet die IndexNow-Anbindung („Crawler Hints") als
   Schalter im eigenen Konto; sie meldet neue und geänderte Adressen automatisch. Alternativ je
   Stufe ein einzelner IndexNow-Ping mit der Adressliste der Stufe.
3. **Interne Verlinkung.** Jede Eintragsseite hängt an ihrer Stadtseite, jede Stadtseite am
   Bundesland-Hub, jeder Hub an der Startseite; die Vertrauens- und Leistungsseiten sind
   querverlinkt. Der Crawler erreicht jede indexierte Seite in wenigen Klicks.

**Wie der Fortschritt gemessen wird:**
- **Cloudflare-Auswertung** des eigenen Kontos (serverseitige Zugriffe, Crawler-Besuche) —
  ausdrücklich die vorgesehene Quelle ([[launch-lean]]).
- **`site:`-Stichproben** bei Google und Bing, um die Zahl indexierter Seiten grob zu verfolgen.
- **Erste Beanspruchungen, Garantie-Anträge und Anfragen nach bezahlten Plätzen** über den
  Mail-Worker bzw. das Formular — das direkteste Zeichen, dass die starken Seiten greifen.

Kein Zählpixel, kein externes Skript, keine Search-Console-Property. Gemessen wird am Server und
an den Anfragen, die hereinkommen.

---

## 4. Geordnete Adressliste (Reihenfolge der Einreichung)

Die Sitemap ist die maschinenlesbare Eingabe. Eingereicht wird in dieser Reihenfolge
([[launch-lean]]), die **18 Garantie-Seiten vorgezogen**:

1. **Startseite.**
2. **Die 18 Garantie-Eintragsseiten** — die stärksten Seiten, zuerst (nach Umsetzung von
   Abschnitt 2). Mannheim (Merz Sicherheit, AES), dann Heidelberg, Ludwigshafen, Hockenheim,
   Schwetzingen, Worms, Weinheim, Speyer, Wiesloch, Waghäusel, Frankenthal, Bensheim, Sinsheim,
   Neustadt, Landau.
3. **Die 16 Bundesland-Seiten.**
4. **`/ueber-uns/` und `/festpreis-garantie/`** — die beiden Vertrauensseiten.
5. **Die 6 Leistungsseiten und ihr Index**, die 5 Ratgeberseiten und ihr Index.
6. **Die Stadtseiten, von der größten zur kleinsten** — Mannheim zuerst, dann nach Eintragszahl.
   Die Bundesländer nach Bestand: Nordrhein-Westfalen (886), Bayern (542), Baden-Württemberg
   (468), Hessen (305), Niedersachsen (305), Berlin (226), Sachsen (195), Rheinland-Pfalz (165),
   Schleswig-Holstein (132), Brandenburg (113), Thüringen (101), Sachsen-Anhalt (97), Hamburg
   (93), Mecklenburg-Vorpommern (73), Saarland (53), Bremen (45).
7. **Die übrigen Eintragsseiten mit `thin=false`**, nach Bewertung und Zahl der Bewertungen
   (`rating × log10(reviews+1)`), die stärksten zuerst.

1.000 Adressen laufen 7 bis 10 Tage; die Staffel wird entsprechend portioniert.

---

## 5. Erweiterungsstufen

**Stufe 1 (Start, nach Abschnitt 2):** der gesamte Sitemap-Bestand (2823 Adressen) —
Startseite, 18 Garantie-Seiten, 16 Bundesländer, 2 Vertrauensseiten, 7 Leistungsseiten, 6
Ratgeberseiten, 577 Stadtseiten (≥ 2 Einträge), die `thin=false`-Eintragsseiten.

**Alle 30 Tage** (Auswertung aus Cloudflare und `site:`-Stichprobe, **keine Search Console**):
wachsen die indexierten Seiten, die nächste Tranche freischalten, neu bauen, neu einreichen.

- **Stufe 2:** dünne Eintragsseiten der größten Städte — **beanspruchte zuerst**, dann nach Zahl
  der Bewertungen. Reihenfolge der Städte wie Abschnitt 4.6.
- **Stufe 3:** die 210 eigenständigen Einzeleintrag-Stadtseiten in Tranchen (jenseits
  `foldMaxKm`, Mittelstädte ab `cityMinPopulation`).
- **Stufe 4 und weiter:** die übrigen dünnen Einträge nach Bundesländern mit dem stärksten
  Zuwachs. Ein Bundesland, dessen Stadtseiten **nicht** indexiert werden, bekommt keine weiteren
  Einträge dazu, bis das steht.

Eine Beanspruchung ist der billigste Weg, eine dünne Seite stark zu machen; jede neue Garantie,
jede Beanspruchung hebt eine Seite sofort in den indexierten Bestand (neu bauen, neu einreichen).

---

## 6. Vor der ersten Einreichung zu prüfen (aus [[launch-lean]])

- [ ] **Abschnitt 2 umgesetzt** — die 18 Garantie-Seiten sind in der Sitemap (`geprueft`-Ausnahme).
- [x] `featuredPreview = false` im ausgelieferten Build.
- [x] `404.html` und `_headers` (pages.dev-noindex) im Build.
- [x] www-Umleitung live (301, Pfad/Query erhalten).
- [x] Impressum und Datenschutz vollständig, ohne Platzhalter, aus dem Fußbereich jeder Seite
      verlinkt (Gate-5-Bericht, von außen bestätigt).
- [ ] **Mit leerem Browserprofil prüfen**, dass ohne Klick auf „Karte von Google Maps laden" keine
      Anfrage an Google geht (Karten, Schriften selbst gehostet).
- [x] Verzeichnis auf **eigenem Cloudflare-Konto**, getrennt von den Schlüsseldienst-Websites.
- [ ] `datePublished` am Tag des Starts der Staffel setzen (derzeit `launchDate=2026-11-03`).

---

## 7. Termin der 30-Tage-Prüfung

**Starttag der Staffel + 30 Tage.** Beginnt die Einreichung am **2026-11-07**, fällt die erste
Prüfung auf den **2026-12-07**. Zu lesen ([[launch-lean]]):

- indexierte Seiten (Cloudflare-Auswertung, `site:`-Stichprobe) — wächst der Bestand?
- Klicks / Crawler-Zugriffe aus der Cloudflare-Auswertung;
- erste Beanspruchungen, erste Garantie-Anträge, erste Anfrage nach einem bezahlten Platz.

Wachsen die indexierten Seiten, Stufe 2 freischalten. Stagnieren sie, erst die Ursache klären
(interne Verlinkung, Ladezeit, Dubletten), bevor neue Seiten dazukommen.

---

## 8. Was der Betreiber tut (nicht Claude)

- Den IndexNow-Schalter (Crawler Hints) im eigenen Cloudflare-Konto aktivieren oder je Stufe den
  IndexNow-Ping auslösen.
- Den Starttag der Staffel festlegen; danach `datePublished` setzen, neu bauen, ausliefern.
- Die Cloudflare-Auswertung alle 30 Tage lesen.

Claude legt kein Konto an, meldet sich nirgends an und reicht nichts ohne Freigabe ein.
