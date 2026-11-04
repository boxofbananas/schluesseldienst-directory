---
title: Gate 5 – Build-Bericht
type: output
status: in-arbeit
updated: 2026-11-04
---

# Gate 5 – Build-Bericht

`npm install && npm run build` läuft durch: **4634 Seiten in ~23 s, keine Fehler, keine Warnung über
fehlende Daten** (außer der gewollten Pflichtangaben-Warnung, siehe Startsperre 1). Der Datenstand
ist abgeschlossen (3.805 Einträge, 792 Stadtseiten, alle Stadttexte zahlenfrei und bestanden).

## Was steht und geprüft ist
- **Build:** 4634 Seiten, `dist/` mit `404.html`, `_headers`, `robots.txt`, `sitemap-index.xml` +
  `sitemap-0.xml` (**2.802** URLs im schlanken Start).
- **Schema/Technik:** **kein `aggregateRating`** im JSON-LD (0 Treffer), `lang="de"`, genau ein H1
  je Seite (Stichprobe Startseite).
- **Sitemap-Filter:** Impressum, Datenschutz und `/festpreis-garantie/antrag/` sind **nicht** in der
  Sitemap (noindex greift).
- **Schriften:** selbst gehostet über `@fontsource` (Roboto, Roboto Slab), kein Google-Fonts-Abruf.
- **Karte:** Google Maps lädt erst nach Klick („Karte von Google Maps laden"), Einwilligung in
  `firma`-Seite, `datenschutz`, `global.css` umgesetzt.
- **Pflichtseiten erzeugen aus `site.json`:** Impressum (§ 5 DDG) und Datenschutz (Art. 13 DSGVO)
  werden generiert; fehlende Pflichtangaben zeigt die Seite als **sichtbare rote Startsperre** und
  `check_live.py`/`load.mjs` blocken. Aktuell fehlt **keine** Impressum-Pflichtangabe (Firma,
  Anschrift, Geschäftsführer, HRB 43586, Amtsgericht Nürnberg stehen).
- **`featuredPreview: false`** im ausgelieferten Build.
- **Herausgeber:** DOM Holding GmbH, Daniel Merz, Schwaig bei Nürnberg; `Organization`/`Person` in
  „Über uns".
- **Zahlungsdienst:** `processors.payment.company` = Stripe Payments Europe, Limited, Dublin (belegt,
  Drittland, SCC) – in der Datenschutzerklärung nennbar.

## Startsperren (müssen vor dem Launch weg)

1. **`contact.formEndpoint` fehlt (harte PFLICHT-Sperre).** Steht noch auf dem Platzhalter
   `https://formspree.io/f/FORMULAR_ID`. Damit haben das Beanspruchungs- und das Garantie-Formular
   **keinen Empfänger**. `load.mjs` meldet beim Build „1 Angabe fehlt, nicht startbereit". **Deine
   Entscheidung nötig:** entweder eine echte Formspree-Formular-ID eintragen **oder** die Annahme
   auf die Cloudflare Pages Function umstellen (Spezifikation liegt in
   `berichte/2026-11-04-formularannahme-spec.md`; braucht ein KV-Namespace aus Gate 6).

2. **Stripe-Zahlungslinks fehlen.** `tiers.premium/bestOf/city.link` stehen auf `STRIPE_LINK_…`. Die
   `/premium/`-Seite zeigt Platzhalter statt kaufbarer Links. Keine PFLICHT-Sperre (die Seite baut),
   aber **Verkauf nicht möglich**, bis du die drei Zahlungslinks in Stripe anlegst und einträgst.
   Verkauft wird ohnehin von Hand (Spalte setzen, neu bauen), die Links sind nur der Bezahlweg.

3. **Ratgeberseiten sind leer.** `/ratgeber/` baut, zeigt aber „Hier steht noch nichts". Es gibt
   noch keinen Artikel. Die artikelförmigen Seiten entstehen mit der **seo-content-engine**-Skill
   (laut `CLAUDE.md` §7 noch in Prüfung) und brauchen die DataForSEO-Anmeldung. **Entscheidung:** mit
   leerem Ratgeber starten (Fußzeilen-Link führt auf die leere Übersicht) oder vor dem Launch ein, zwei
   Ratgeber schreiben.

4. **Rechtstexte anwaltlich prüfen lassen.** Impressum und Datenschutz sind vollständig generiert,
   aber das Wiki ist keine Rechtsberatung. Offen und bewusst leer gelassen: **USt-IdNr.** (§ 27a UStG
   verlangt sie nur, wenn erteilt) und **Telefonnummer** (§ 5 DDG lässt E-Mail genügen). Beides ist
   **kein** Startblocker; eine Nummer schafft aber Vertrauen. Sag, ob eine USt-IdNr. vorliegt und ob
   eine Telefonnummer ins Impressum soll.

5. **Fünf Schweizer Grenzorte noch im Datenstand – Entscheidung nötig.** Analog zu den von dir
   gedroppten Grenzorten (Basel usw.) stehen noch **Allschwil, Arlesheim, Oberwil, Riehen,
   Siegershausen** (je 1 Eintrag, alle `noindex`-Ortsseiten, nicht in der Start-Sitemap) im Dump. Sie
   waren nicht in deiner genehmigten Liste, deshalb habe ich sie **nicht** von selbst gedroppt. Sollen
   sie unter derselben Regel „Ausland (Schweiz), Verzeichnis ist für Deutschland" raus? (Empfehlung:
   ja.)

## Hinweise, keine Sperren
- **Textgate:** Der maßgebliche Stadttext-Gate ist `check_city_copy.py` (nutzt die stadtgenauen
  Wortspannen) – **792/792 bestanden, 0 Datenzahlen**. `lint_copy.py` direkt auf `city-copy.json`
  meldet nur Scheinfehler, weil ihm ohne `--city-sizes` die Kleinstadt-Spannen fehlen.
- **„ab 49 Euro" auf `/festpreis-garantie/`** ist **gewollt**: der Satz schildert die Lockvogel-Masche
  („…oft ‚ab 49 Euro', und auf der Rechnung stehen 400"). `lint_copy` markiert die Preisfloskel; auf
  dieser Seite (mit `--erlaube-rechtswoerter`) ist sie inhaltlich richtig. Belassen oder umformulieren
  ist deine Wahl.
- **Ansehen:** `preview-site.command` (Mac) / `preview-site.bat` (Windows) in `site/`, nie direkt
  `dist/index.html`.

## Nächste Schritte
Nach deinen Entscheidungen zu 1–5: Werte in `site.json` eintragen, neu bauen, dann Gate 6 (schlanker
Start, Cloudflare Pages, `check_live.py`, gestaffelte Indexierung).
