# Astro-Vorlage, deutsche Fassung: was Gate 5 kopiert und was es füllt

Dieser Ordner ist ein vollständiges, baubares Astro-5-Projekt für ein **deutsches** Verzeichnis mit
drei Ebenen: Deutschland, Bundesland, Stadt. Gate 5 kopiert ihn nach `output/<slug>/site/` und füllt
die Datendateien. Es schreibt keine Seiten neu. Verbindlich ist `wiki/konventionen.md`; bei
Widerspruch zu einer englischen Wiki-Seite gilt sie.

Probebau am 03.11.2026 mit 17 erfundenen Einträgen in drei Bundesländern
(`/home/claude/build/testdata`): `npm install && DIRECTORY_DATA_DIR=… npm run build` erzeugte
49 Seiten, eine Sitemap mit 35 Adressen (dünne Einträge und die Seiten zur Umwandlung
ausgeschlossen), zwei Siegel-Bilder und robots.txt.

## Diese Dateien füllen (in dieser Reihenfolge)

| Datei | Was hineingehört | Quelle |
|---|---|---|
| `src/data/site.json` | Marke, Domain, Tagline, Branchenwörter, `country` (Deutschland/DE), Startdatum, **Herausgeber** (Name, legalName, Anschrift, Geschäftsführer, Register, URL, E-Mail, Bild, sameAs), Endpunkt des Kontaktformulars (der Formulardienst beim Start oder `/claim` des Mail-Workers nach `scripts/mail_worker.py wire-form`; die Seite „Eintrag beanspruchen“ zeigt ihre Bestätigung auf `/eintrag-beanspruchen/?gesendet=1`), Preise und Stripe-Zahlungslinks, **Gestaltungsmarken**, FAQ der Startseite, `guide` und `aboutWhy` (Absatzlisten, HTML erlaubt). `domain` ist die Domain, die der Betreiber besitzt oder registrieren will; jede Canonical-Adresse, die Sitemap und die Schema-Kennungen werden daraus gebaut | `01-scope.md`, `04-plan.md` |
| `src/data/listings.csv` | das Ergebnis von Gate 3, eine Zeile je Eintrag. **Die Spalte `state` trägt den Namen des Bundeslandes**; daraus leitet `loadRegions()` die Bundesland-Ebene ab | Kopie von `output/<slug>/03-listings-enriched.csv` |
| `src/data/attributes.json` | der Merkmalssatz der Branche: `key` (muss einer CSV-Spalte entsprechen), `label`, `faq`-Vorlage mit `{plural}`, `{singular}`, `{city}`, `{bundesland}`, `{land}`, und bei den Merkmalen, die `04-plan.md` als Leistungsseite nennt, ein `service`-Block (`slug`, `title`, `intro`) | `03-attributes.json` |
| `src/data/city-copy.json` | je Stadtseite, Schlüssel `bundesland-slug/stadt-slug`: `intro` (Absatzliste, 500 bis 800 Wörter echter örtlicher Text; niedrigere Grenzen bei kleinen Städten und 120 Wörter mit 2 bis 6 FAQs auf einer Ortsseite, wiki/framework/page-types.md) und `faqs` (4 bis 6 `{q, a}` aus den Daten). Ein bloßer Stadt-Slug wird weiter akzeptiert. Städte ohne Eintrag bauen mit einem kurzen datengetriebenen Ersatztext, und der Bau nennt sie in einer Warnung | von Claude bei Gate 5 geschrieben |
| `src/pages/impressum/index.astro` | Impressum nach § 5 DDG. Trägt im Auslieferungszustand nur `PLATZHALTER: Inhalt wird separat eingesetzt.` | Betreiber |
| `src/pages/siegel/index.astro` | die Prüfkriterien des Siegels. Diese Seite **muss** stehen, sonst ist das Siegel angreifbar (wiki/konventionen.md). Platzhalter wie oben | Betreiber |
| `src/pages/siegel/antrag/index.astro` | der Fragebogen und das Serviceversprechen. Platzhalter wie oben | Betreiber |
| `public/images/…` | Bilder, die der Betreiber beisteuert; bei beanspruchten Premium-Einträgen gehören die Pfade in die CSV-Spalte `photos`, mit `\|` getrennt | Beanspruchungen und Verkäufe |
| `src/pages/ratgeber/<slug>.md` | optionale Ratgeberseiten (`_example.md` kopieren; Dateien mit `_` am Anfang werden nicht gebaut) | wiki/framework/authority-and-links.md |

## Spalten, die die Website aus der CSV liest

Aus Gate 2: `name, phone, website, address, street, city, state, state_code, postal_code, county,
latitude, longitude, type, subtypes, rating, reviews, reviews_tags, description, working_hours,
verified, location_link, area_service, slug, city_slug, thin, featured, featured_cities, claimed`.
`state` ist der **Name des Bundeslandes** („Baden-Württemberg“), `state_code` das Kürzel; fehlt es,
wird es aus der Tabelle `REGION_CODES` in `src/lib/load.mjs` ergänzt.
Aus Gate 3: eine Spalte je Merkmalsschlüssel mit `true` / `false` / leer, dazu `description_enriched`.
Spalten, die der Betreiber von Hand setzt: `featured` (`city` / `county` / `state`),
`featured_cities` (Stadt-Slugs), `premium` (`true`), `best_of_rank` (1 bis 3), `claimed` (`true`),
`photos`, **`geprueft`** (`true`/`false`) und **`geprueft_jahr`** (Jahr der Prüfung, für das Siegel).
`owned` wird von der Website nie gelesen (Footprint-Regel). Als wahr gelten `true`, `wahr`, `ja`, `1`.

## Was die Vorlage bereits tut

- Adressen: `/`, `/verzeichnis/` (Blättern, noindex), `/verzeichnis/<bundesland>/`,
  `/verzeichnis/<bundesland>/<stadt>/`, `/firma/<bundesland>/<stadt>/<slug>/`, `/suche/` (noindex),
  `/eintrag-beanspruchen/`, `/premium/`, `/siegel/`, `/siegel/antrag/`, `/ueber-uns/`, `/kontakt/`,
  `/impressum/`, `/datenschutz/`, `/agb/`, `/ratgeber/`, `/ratgeber/<slug>/`, `/leistungen/` und
  `/leistungen/<slug>/` (nur wenn ein Merkmal einen `service`-Block hat und mindestens die
  Mindestzahl an Einträgen ihn bestätigt), `/favicon.svg`, `/auszeichnung/<slug>/` und
  `/auszeichnung/<slug>.svg` (nur für Betriebe mit `geprueft=true`), `/robots.txt`,
  `/sitemap-index.xml`.
- **Drei Ebenen.** Die Bundesländer werden nicht in `site.json` aufgezählt, sondern von
  `loadRegions()` aus der Spalte `state` abgeleitet (eindeutige Werte, Anzahl Einträge und Anzahl
  Städte je Land). Eine Bundesland-Seite entsteht für jedes Land mit mindestens einer Stadtseite.
  Die Startseite verlinkt alle Bundesländer mit Anzahl und die 20 größten Städte; die
  Bundesland-Seite verlinkt jede Stadt des Landes, kleinere Orte unter „Kleinere Orte“.
  Brotkrumenpfad: Startseite / Schlüsseldienste / Bundesland / Stadt / Betrieb.
- Mindestzahl je Stadt (Standard 3); Orte darunter werden in die nächste Stadt **desselben
  Bundeslandes** gefaltet oder bleiben als indexierte Ortsseite, wenn sie weiter als `foldMaxKm`
  entfernt liegen. Orte in der Nähe nach Entfernung, bundeslandübergreifend. Kartenreihenfolge:
  Premium-Plätze, dann Top-Platzierungen, dann Bewertung x log(Anzahl Bewertungen); Deckel bei
  60 Karten mit einer Liste „N weitere“ darunter.
- **Deutsche Daten.** `slugify` schreibt ä/ö/ü/ß vor dem Entfernen der Sonderzeichen um
  („Nürnberg“ wird `nuernberg`). Telefonnummern werden als `+49 621 1234567` angezeigt und als
  E.164 (`+496211234567`) in `tel:` und im Schema ausgegeben; nicht erkennbare Nummern bleiben
  unverändert. `parseHours` versteht deutsche und englische Tagesnamen, 24-Stunden-Zeiten,
  „Geschlossen“/„Closed“ und „Durchgehend geöffnet“/„24 Stunden“/„Open 24 hours“. Bewertungen
  erscheinen mit Komma (`4,8`), Zahlen mit Punkt als Tausendertrennzeichen (`1.234 Bewertungen`),
  Daten als `TT.MM.JJJJ`. Zwei Städte gleichen Namens im selben Bundesland bekommen die
  Postleitzahl an den Stadt-Slug; erkannt wird das über die Lage (Einfachverkettung bei 25 km),
  nicht über die Postleitzahl, weil eine große Stadt mehrere Leitregionen abdeckt.
- Zwei Zustände je Eintrag: Grundeintrag (keine Bilder; **kein** Website- oder Profil-Link, außer
  der Betrieb hat die Festpreis-Garantie oder ist über `link_follow` freigeschaltet) und
  ausgebauter Eintrag (beanspruchter Premium-Eintrag oder ein Premium-Platz: Bilder, Karte,
  Öffnungszeiten, Siegel-Baustein; der Website-Link kommt mit einem bezahlten Platz als bezahlt
  gekennzeichnet (`rel="sponsored"`) oder mit der Garantie ohne nofollow).
- **Siegel.** Jeder Eintrag trägt eine Siegel-Zeile: „Geprüft <Jahr>“ mit Link auf `/siegel/`, oder
  „Noch nicht geprüft“ mit Link auf `/siegel/antrag/`. Die zweite Zeile ist der Verkaufsanlass und
  darf nicht abgeschaltet werden. `/auszeichnung/<slug>.svg` trägt „Geprüfter Schlüsseldienst
  <Jahr>“ und die Marke und entsteht nur für `geprueft=true`.
- **Keine Karte ohne Klick.** Statt der Google-Maps-Einbettung steht eine Platzhalterfläche mit der
  Schaltfläche „Karte von Google Maps laden“ und dem Hinweis, dass dabei Daten an Google übertragen
  werden; erst der Klick setzt das iframe ein (reines JavaScript, keine fremde Abhängigkeit, kein
  Einwilligungsbanner). Der Link „Route planen“ ist ein gewöhnlicher Link und lädt nichts nach.
  Schriften liegen selbst gehostet in `src/styles/fonts.css`; Google Fonts werden nie geladen.
- Launch lean: dünne Einträge (`thin=true`, oder unter 5 Bewertungen oder ohne Beschreibung), die
  Siegel-Nachweise und die Seiten zu Eintrag, Premium, Siegel-Antrag und Recht tragen `noindex` und
  bleiben aus der Sitemap. Eine Beanspruchung oder eine bezahlte Stufe hebt „dünn“ auf.
- JSON-LD je Seitenart (WebSite, Organization mit Gründer und Herausgeber, der Herausgeber als
  **Organization** statt Person, weil er eine GmbH ist; CollectionPage + ItemList auf Bundesland-,
  Stadt- und Leistungsseiten, der Betriebstyp aus `niche.schemaType` mit Öffnungszeiten auf den
  Eintragsseiten (kein `aggregateRating`: die Bewertungen sind Googles, wiki/seo/schema.md),
  Telefon in E.164, `addressCountry: "DE"`, `inLanguage: "de-DE"`, FAQPage, BreadcrumbList, Article
  auf Ratgeberseiten), `datePublished` aus `launchDate`, `dateModified` aus dem Baudatum.
- Interne Links: jede Eintragsseite führt vier weitere Einträge aus ihrer Stadt und die
  Leistungsseiten, auf denen sie steht; die Startseite hat die Schaltfläche „Alle N Städte ansehen“
  unter den Stadtkarten, der Fußbereich alle Bundesländer sowie Impressum, Datenschutz, AGB und
  Siegel.
- Ein Standard-Favicon (`/favicon.svg`: der erste Buchstabe der Marke auf der Kopfzeilenfarbe).
- Gestaltungsmarken aus `site.json` als CSS-Variablen; keine Etiketten über den Karten, keine
  farbigen Kartenrahmen, die Karten tragen Daten.
- Fakten als sichtbarer Text: FAQs, Öffnungszeiten und Merkmale stehen nie in einem Aufklappbereich.

## Optionale Einstellungen in `site.json`

| Schlüssel | Wirkung | Standard |
|---|---|---|
| `design.heading`, `design.headingWeight`, `design.link`, `design.buttonRadius` | Farbe und Stärke der Überschriften, Linkfarbe, Ecken der Schaltflächen | die Grundmarken |
| `design.band`, `design.bandText` | Kopfbereich der Startseite und Fußband | die Flächenfarbe |
| `design.action`, `design.actionText` | das Handlungsband | der Akzent |
| `sortAttribute` | Einträge mit diesem Merkmal sortieren in ihrer Gruppe nach vorn | keines |
| `confirmedLabel` | das kurze Wort nach der Zahl auf der Zahlenreihe und den Stadtkarten | `geprüft` |
| `vettingSteps` | vier `{title, text}`-Schritte als Karten über dem Text zur Aufnahme auf der Startseite | ein allgemeiner Satz von vier Schritten |
| `foldMaxKm` | Orte unter der Mindestzahl, die weiter als dieser Wert von jeder Stadtseite ihres Bundeslandes entfernt liegen, bekommen eine eigene Seite, indexiert und in der Sitemap, stehen auf der Bundesland-Seite unter „Kleinere Orte“ und bleiben aus der Navigation. Sie brauchen wie jede Stadtseite einen Eintrag in `city-copy.json`. `0` heißt kein Deckel | `40` (km) |
| `cityFilter` | ein Filterfeld über der vollständigen Städteliste der Startseite | aus |
| `vetting`, `countryIntro`, `regionIntro` | Absätze für „Wie die Einträge entstehen“, die Blätterseite und die Bundesland-Seiten | die Texte der Vorlage |
| `guide` | der Ratgebertext auf der Startseite, als Absatzliste (HTML erlaubt) | ein sachlicher Standardtext |
| `aboutWhy` | der Abschnitt „Warum es dieses Verzeichnis gibt“ auf `/ueber-uns/` | ein sachlicher Standardtext |
| `heroPoints` | kurze, zutreffende Aussagen mit Haken unter den Schaltflächen im Kopf | keine |
| `footerAbout` | der Absatz in der Spalte „Über …“ im Fußbereich | ein Satz aus Marke, Branche und Land |
| `featuredPreview` | `true` füllt unverkaufte Premium-Plätze mit den besten echten Einträgen, damit die Gestaltung beurteilt werden kann; die Karten tragen `data-preview`. Beim Start `false` | `false` |
| (listings.csv) `socials` | optionale Spalte, `facebook=url\|instagram=url\|…` | keine |
| `niche.schemaType` | der schema.org-Typ jedes gelisteten Betriebs. Für Schlüsseldienste `Locksmith` | `LocalBusiness` |
| `design.favicon` | Pfad einer eigenen Favicon-Datei in `public/` | das erzeugte `/favicon.svg` |
| `design.gold`, `design.goldLight`, `design.goldDeep` | Hervorhebungsfarben auf dunklen Bändern | `#F5B940`, `#FFD86B`, `#D9950F` |
| `disclaimer` | der Hinweis in der Seitenspalte der Eintragsseite | ein Absatz: öffentliche Quellen, selbstständige Betriebe, kein zulassungspflichtiges Handwerk |
| `publisher.sameAs` | Profillinks; der Fußbereich zeigt ein Zeichen je erkanntem Netzwerk | keine |

Die Zahlungslinks in `tiers` sind beim Start Platzhalter (`STRIPE_LINK_…`). Nur Werte, die mit
`http` beginnen, werden verlinkt; sonst führt die Schaltfläche auf die Anfrage
(`payLink()` in `src/lib/load.mjs`).

## Suche

Der Kopf der Startseite und die Seite `/suche/` tragen dasselbe Formular
(`src/components/SearchForm.astro`): zwei Felder (was, und wo) mit Vorschlägen während der Eingabe.
Das erste Feld bietet zuerst die passenden Leistungen (eine Wahl wird zu einem Schildchen im Feld,
die Rücktaste im leeren Feld entfernt das letzte) und danach die Betriebe (eine Wahl öffnet den
Eintrag). Es gibt keinen Server: `src/pages/search-index.json.ts` schreibt beim Bau
`search-index.json` (jeder Eintrag und jede Stadtseite, kleine Felder, dazu das Siegel-Kennzeichen
und das Bundesland), und `public/search.js` holt die Datei, sobald ein Besucher das erste Mal ein
Feld berührt. `norm()` in `search.js` schreibt Umlaute um, damit „Nurnberg“ und „Nürnberg“ dieselben
Treffer finden. Gesucht wird erst beim Klick auf Suchen (oder mit der Eingabetaste): das öffnet
`/suche/?s=&near=&f=` (noindex, nicht in der Sitemap). Filter werden mit UND verknüpft.
„In meiner Nähe“ nutzt den Standort des Browsers mit acht Sekunden Zeitgrenze. Ohne JavaScript
verweist die Suchseite auf die Blätterseite.

Webschriften: selbst gehostete `@fontsource`-Importe in `src/styles/fonts.css`, die Pakete stehen in
`package.json`. Die Vorlage liefert das Paar der Mustervorlage, Roboto Slab 800 für Überschriften und
Roboto für den Text.

`dump-cities.mjs` (im Website-Ordner, bei Gate 5 ausgeführt) schreibt die Städtestruktur genau so,
wie die Website sie baut, Faltungen eingeschlossen, für `scripts/make_city_packets.py`:
`node dump-cities.mjs [plz-kreis.json] ../05-cities.json`. Jede Stadt trägt dort ihr Bundesland.

## Bauen und veröffentlichen

```
npm install
npm run build        # -> dist/
```
Mit einem Datenordner außerhalb des Projekts:
`DIRECTORY_DATA_DIR=/pfad/zu/daten npm run build`.
Unter npm 11 gibt `npm install` eine Warnung zu Installationsskripten von esbuild und sharp aus. Das
ist eine Warnung, kein Fehler; der Bau läuft trotzdem durch.
Cloudflare Pages: Repository verbinden, Voreinstellung Astro, Baubefehl `npm run build`, Ausgabe
`dist`. Oder `dist/` von Hand hochladen. Nach jeder Änderung der CSV neu bauen und veröffentlichen.
`astro.config.mjs` schreibt bei jedem Bau `public/_redirects`: `/firma/`, `/firma/<bundesland>/` und
`/firma/<bundesland>/<stadt>/` leiten auf die passende Verzeichnisseite, dazu die alten englischen
Adressen der Vorlage (`/directory/`, `/company/`, `/services/`, `/badge/`, `/claim/`, `/featured/`,
`/about/`, `/contact/`, `/privacy/`, `/terms/`, `/search/`, `/resources/`).

## Den Bau auf dem eigenen Rechner ansehen
`dist/` nutzt Pfade, die am Wurzelverzeichnis der Domain beginnen (`/_astro/…`,
`/verzeichnis/bayern/nuernberg/`). Von einem Webserver ausgeliefert ist das richtig. Als Datei
geöffnet hat es keine Gestaltung und toten Links.

- **Standard:** `preview-site.command` (Mac) oder `preview-site.bat` (Windows) doppelklicken.
- **Um jemandem einen Ordner zu geben:** `python3 scripts/make_local_preview.py <site>/dist <out>/preview`
  schreibt eine Kopie mit relativen Pfaden. Veröffentlicht wird `dist/`, nie die Kopie.

## Zwei Eigenheiten des Astro-Compilers beim Bearbeiten von Seiten
- `set:html` wirkt nicht auf einem Element innerhalb eines `.map()`-Ausdrucks. Den HTML-String zuerst
  bauen und `set:html` auf den Rahmen setzen (siehe `paragraphs()` in `src/lib/load.mjs` und
  `JsonLd.astro`).
- `<p>`-Elemente innerhalb eines `.map()`-Ausdrucks lassen sich nicht übersetzen. Für Absatzlisten
  `paragraphs()` nutzen.
