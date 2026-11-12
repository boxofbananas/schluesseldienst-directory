# Gate 6 — Schlanker Start

**Verzeichnis:** Die besten Schlüsseldienste · `die-besten-schluesseldienste.de`
**Stand:** 2026-11-06 · Build 4646 Seiten, Sitemap **2814** Adressen (Garantie-Ausnahme umgesetzt)
· Domain und www-Umleitung live · Start der Staffel 2026-11-06 (ausgelöst)
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
- Stellschrauben: `cityFloor=2`, `foldMaxKm=30`, `cityMinPopulation=20000`, `launchDate=2026-11-06`.

---

## 2. Die Garantie-Ausnahme — umgesetzt, mit Inhaltsschranke

**Ausgangslage.** `load.mjs` setzte `thin && !claimed && !optimized` auf `noindex`. 17 der 18
Betriebe mit Festpreis-Garantie waren `thin` (unter 5 Bewertungen) und fielen damit aus der
Sitemap; nur Merz Sicherheit Mannheim war drin.

**Inhaltsprüfung (vor der Umsetzung).** Nicht jede geprüfte Seite trägt eigenen Inhalt. Von den 18
sind **9 praktisch leer** (0 Wörter Beschreibung, 0 belegte Merkmale — nur Stammdaten und
Garantie-Block): AES Schlüsseldienst Mannheim, I-S-E Schlüsseldienst (Hockenheim), Mein
Schlüsseldienst Weinheim, Merz Schlüsseldienst Ludwigshafen, Merz Schlüsseldienst Speyer, Merz
Schlüsseldienst Worms, Rheinpfalz Schlüsseldienst Frankenthal, Riegelklar Schlüsseldienst
Schwetzingen, Sperber Schlüsseldienst (Heidelberg). Die übrigen **9 tragen Inhalt** (120–134
Wörter, 7–14 Merkmale). Eine leere Seite gehört trotz `geprueft` nicht in die erste Stufe — dort
misst `thin` das Richtige.

**Umgesetzt.** Eine geprüfte Seite wird nur dann nicht wegen `thin` ausgenommen, wenn sie eine
Beschreibung trägt. In `load.mjs` (Build **und** `templates/astro/`):

```
for (const l of listings) if (l.thin && !l.claimed && !l.optimized && !(l.geprueft && l.description)) noindexPaths.add(l.path);
```

Gebaut und ausgeliefert. Sitemap **2806 → 2814** (+8; Merz Sicherheit war schon drin). Jetzt sind
**9 Garantie-Seiten indexiert** (mit Inhalt), **9 bleiben `noindex`** (leer) und werden erst
indexiert, wenn sie eine Beschreibung bekommen — über eine Beanspruchung oder eine Anreicherung.
Die `/auszeichnung/`-Nachweisseiten bleiben `noindex` (Beleg, kein Inhalt). Live bestätigt: die 9
inhaltsstarken Seiten senden `index, follow` und stehen in der Sitemap, die 9 leeren senden
`noindex, follow` und fehlen in ihr.

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
2. **Die 9 indexierten Garantie-Eintragsseiten** — die stärksten Seiten, zuerst: Merz Sicherheit
   Mannheim, Heidelberg Schlüsseldienst, Mein Schlüsseldienst Hockenheim, Kraichgau Sinsheim,
   Pälzer Neustadt, Hardt Waghäusel, Südpfalz Landau, Odenwald Bensheim, Kurpfalz Wiesloch. Die 9
   leeren Garantie-Seiten (Abschnitt 2) bleiben vorerst `noindex` und ziehen nach, sobald sie eine
   Beschreibung bekommen.
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

**Stufe 1 (Start):** der gesamte Sitemap-Bestand (2814 Adressen) — Startseite, 9 indexierte
Garantie-Seiten, 16 Bundesländer, 2 Vertrauensseiten, 7 Leistungsseiten, 6 Ratgeberseiten, 577
Stadtseiten (≥ 2 Einträge), die `thin=false`-Eintragsseiten.

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

- [x] **Abschnitt 2 umgesetzt** — die 9 inhaltsstarken Garantie-Seiten sind in der Sitemap, die 9
      leeren bleiben `noindex` (`geprueft && description`-Ausnahme), live bestätigt.
- [x] `featuredPreview = false` im ausgelieferten Build.
- [x] `404.html` und `_headers` (pages.dev-noindex) im Build.
- [x] www-Umleitung live (301, Pfad/Query erhalten).
- [x] Impressum und Datenschutz vollständig, ohne Platzhalter, aus dem Fußbereich jeder Seite
      verlinkt (Gate-5-Bericht, von außen bestätigt).
- [x] **Mit leerem Browserprofil geprüft**: Startseite, Stadtseite und Eintragsseite laden ohne
      Klick **keine** externe Anfrage und **nichts** von Google; erst nach Klick auf „Karte von
      Google Maps laden" lädt die Karte (`maps.googleapis.com` u. a.). Schriften selbst gehostet.
- [x] Verzeichnis auf **eigenem Cloudflare-Konto**, getrennt von den Schlüsseldienst-Websites.
- [x] `datePublished` auf den Staffel-Starttag **2026-11-06** gesetzt (`site.json` `launchDate`),
      im gebauten und im Live-Schema bestätigt.
- [x] **Staffel ausgelöst** am **2026-11-06**: Build und Auslieferung mit dem Starttag als
      `datePublished` live, `check_live.py` grün. Sitemap am Start 2823 Adressen; seit der
      Entfernung zweier Einträge am **2026-11-12** **2821** (laufender Sollwert für `check_live.py`).

---

## 7. Termin der 30-Tage-Prüfung

**Starttag der Staffel + 30 Tage.** Die Staffel ist am **2026-11-06** gestartet (= `datePublished`);
die erste Prüfung fällt auf den **2026-12-06**. Zu lesen ([[launch-lean]]):

- indexierte Seiten (Cloudflare-Auswertung, `site:`-Stichprobe) — wächst der Bestand?
- Klicks / Crawler-Zugriffe aus der Cloudflare-Auswertung;
- erste Beanspruchungen, erste Garantie-Anträge, erste Anfrage nach einem bezahlten Platz.

Wachsen die indexierten Seiten, Stufe 2 freischalten. Stagnieren sie, erst die Ursache klären
(interne Verlinkung, Ladezeit, Dubletten), bevor neue Seiten dazukommen.

---

## 8. Was der Betreiber tut (nicht Claude)

- Den IndexNow-Schalter (Crawler Hints) im eigenen Cloudflare-Konto aktivieren oder je Stufe den
  IndexNow-Ping auslösen.
- [x] Die Staffel ist am Starttag **2026-11-06** ausgelöst (Build und Auslieferung mit diesem Tag
  als `datePublished`). Noch offen beim Betreiber: den IndexNow-Ping der ersten Stufe im eigenen
  Cloudflare-Konto absetzen.
- Die Cloudflare-Auswertung alle 30 Tage lesen.

Claude legt kein Konto an, meldet sich nirgends an und reicht nichts ohne Freigabe ein.
