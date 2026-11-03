# Verzeichnis-Blueprint für Claude Code

Dieser Ordner ist ein **LLM-gepflegtes Wiki mit Arbeitsablauf**. Sein Zweck: aus einem
Google-Maps-Export ein geordnetes, verkaufsfähiges Branchenverzeichnis bauen. Der Mensch
liefert Material und gibt die Gates frei, du pflegst das Wiki und baust.

**Lies zuerst [[konventionen]], dann `wiki/index.md`.** `wiki/konventionen.md` ist der
verbindliche Vertrag: bei Widerspruch zu einer anderen Wiki-Seite gilt sie.

---

## 1. Was gebaut wird

**Die besten Schlüsseldienste** – ein Verzeichnis aller Schlüsseldienste in Deutschland.
Branche, Land, Domain und Herausgeber sind entschieden und stehen in [[konventionen]]. Frage
sie nicht ab, schlage keine Alternativen vor, bewerte die Branche nicht.

- Domain `die-besten-schluesseldienste.de`
- Herausgeber DOM Holding GmbH, Geschäftsführer Daniel Merz
- Branche Schlüsseldienst (Google-Maps-Kategorie `locksmith`), `niche.schemaType` = `Locksmith`
- Wichtigste Stadt Mannheim
- Build-Ordner `output/schluesseldienste-deutschland/`, kurz `<slug>`; jedes Skript nimmt
  diesen Slug als `--slug` oder in `--out`

**Drei Ebenen** statt der zwei der englischen Fassung: Startseite → bis 16 Bundesland-Seiten →
Stadtseiten → Eintragsseiten. Die URL-Tabelle in [[konventionen]] ist maßgeblich,
[[site-architecture]] führt sie aus.

Statische Astro-Site, Cloudflare Pages, aus einer CSV neu gebaut, sobald sich etwas ändert.

Warum der Betreiber sie baut, in dieser Reihenfolge:
1. Sie stärkt die eigenen Schlüsseldienst-Websites: Verzeichnis, eigene Site und
   Google-Unternehmensprofil belegen dieselbe Trefferliste dreifach.
2. Sie vermietet ihre oberen Plätze (Premium-Eintrag, Stadt-Premium, Top-Platzierung) und
   kann später Anfragen verkaufen.
3. Sie ist der Grund, jeden Schlüsseldienst in Deutschland anzurufen: „Sie haben einen
   Eintrag in meinem Verzeichnis." Der sichtbare Hinweis „Noch nicht geprüft" ist dabei der
   Gesprächsanlass ([[siegel-programm]]).

Werbebanner sind in dieser Größe draußen. **Eigene Websites werden wie jeder andere Betrieb
gelistet**, keine seitenweiten Links, keine Sonderbehandlung ([[footprint-rules]]).

---

## 2. Ordnerkarte

```
verzeichnis-blueprint/
├── CLAUDE.md          diese Datei, das Regelwerk
├── README.md          die Einstiegsseite: entpacken, Claude Code öffnen, „Gate 1 starten"
├── input/             listings-raw.csv (DataForSEO-Abruf oder Outscraper-Export); nie Zugangsdaten
├── scripts/           deterministische Helfer, nach Gate: fetch_dataforseo.py (1),
│                      connect_dataforseo.py (läuft im eigenen Terminal des Betreibers, nie bei dir),
│                      clean_listings.py (2), fetch_sites.py, build_evidence.py, make_batches.py,
│                      merge_enriched.py (3), apply_exclusions.py, add_socials.py,
│                      make_city_packets.py, check_city_copy.py, lint_copy.py (5),
│                      run_batches.py (Stapelläufer für 3 und 5), check_live.py (6),
│                      make_local_preview.py (wahlweise). Nach dem Start: mail_worker.py,
│                      mail_inbox.py, make_worker_listings.py. Die Anweisungsdateien sind
│                      allgemein; die Regeln dieser Branche stehen in output/<slug>/03-attributes.json
├── skills/            seo-content-engine: ihr Linter prüft jeden Textblock in Gate 5, ihr
│                      vollständiger Ablauf schreibt Ratgeberseiten
├── wiki/
│   ├── konventionen.md  DER VERTRAG. Zuerst lesen, nie ändern.
│   ├── index.md         Verzeichnis jeder Wiki-Seite. Danach lesen.
│   ├── log.md           fortgeschriebenes Protokoll
│   ├── framework/       das Regelwerk: Aufbau, Seitentypen, Siegel, Geld, Footprint, Pflege
│   ├── seo/             Seitentechnik, Schema, Sitemap, schlanker Start
│   ├── components/      Abschnittsfolgen der Seitentypen
│   └── references/      die öffentlichen Beispielverzeichnisse (nur Optikvergleich)
├── templates/         Beanspruchungsformular, Preisstufen, astro/ (das vollständige
│                      Astro-Projekt, das Gate 5 kopiert und füllt), master-reference/site/
│                      (der englische Referenzbau als HTML, Maßstab für Aufbau und Optik)
│                      und worker/ (der Mail-Worker, nach dem Start)
└── output/<slug>/     der Build-Ordner dieses Verzeichnisses
```

Konventionen: Kopfzeilen auf jeder Wiki-Seite (`title`, `type`, `status`, `updated`),
`[[wikilinks]]` im Text, Dateinamen englisch und in Kleinschreibung mit Bindestrichen (damit
die Wikilinks auflösen), ein Gedanke je Seite, nach jeder Änderung `wiki/index.md` ergänzen
und `wiki/log.md` fortschreiben.

---

## 3. Der Ablauf: sechs Gates

Der Reihe nach. **Nach jedem Gate anhalten und auf Freigabe warten.** Das Ergebnis jedes
Gates nach `output/<slug>/` schreiben und eine Zeile in `wiki/log.md` anfügen.

### Gate 1, Umfang

Branche, Land, Domain, Herausgeber und Marke stehen fest ([[konventionen]]). Frage nur noch
die drei Punkte ab, die wirklich offen sind, **eine Frage je Antwortrunde**, und schreibe die
Antworten in `01-umfang.md`, sobald sie eintreffen ([[gate-1-intake]]):

1. **Eigene Websites.** Welche Schlüsseldienst-Websites und -Betriebe gehören dem Betreiber?
   Nur die Telefonnummern, nichts weiter. Sie füllen die Spalte `owned` in Gate 2
   ([[footprint-rules]]).
2. **Optik.** Die mitgelieferte Optik des Referenzbaus, oder eine bis zwei Websites als
   Optikvorlage ([[design-seed]]).
3. **Datenabruf.** Die Kosten des Abrufs nennen und die Freigabe einholen, erst danach
   abrufen.

**Niemals abfragen oder vorschlagen:** die Branche, das Land, das Bundesland, die Domain,
die Marke, den Herausgeber. Kein Bewertungsbogen, kein Nischenfinder, keine Branchenprüfung,
keine Alternativen. Diese Entscheidungen sind gefallen; `scripts/check_vertical.py` wird in
diesem Projekt nicht benutzt.

Mit gespeicherter DataForSEO-Anmeldung (`scripts/connect_dataforseo.py --check`) vor Frage 3
`scripts/fetch_dataforseo.py --estimate` laufen lassen (etwa fünf Cent), die Kosten bei
Frage 3 nennen und erst nach einem Ja abrufen. Ohne gespeicherte Anmeldung lautet die
Anweisung: `python3 scripts/connect_dataforseo.py` im eigenen Terminal des Betreibers. Ein
Connector allein reicht dem Skript nicht. Du führst den Helfer nie selbst aus.

Ergebnis: `01-umfang.md` und, auf dem DataForSEO-Weg, `input/listings-raw.csv` plus
`input/listings-raw-report.md`. Gate 2 beginnt, sobald `01-umfang.md` freigegeben ist.

### Gate 2, Bereinigen

`scripts/clean_listings.py` auf `input/listings-raw.csv`. Die Regeln stehen in
[[listings-cleaning]]: dauerhaft geschlossene Zeilen löschen, DataForSEO-Zeilen ohne
Aktualisierung seit zwölf Monaten löschen, Zeilen ohne Bewertung löschen, Namen mit einem
Branchenwort oder Zeilen mit der Kategorie behalten, auf Telefonnummer plus Adresse
entdoppeln, eigene Betriebe und dünne Einträge kennzeichnen. Das Skript schreibt außerdem
`02-domains.txt`, die Domains der behaltenen Zeilen, und entfernt Googles Tracking-Parameter
aus `website`. `slugify` schreibt Umlaute um, bevor es Sonderzeichen entfernt
([[konventionen]]).

**Die Branchenbesonderheit, die Gate 2 nur sichtbar macht, nie selbst löst:** Die Kategorie
`locksmith` fängt in Deutschland auch Schuhmacher, Gravurbetriebe, Metallbauer und Baumärkte
ein, weil dort Schlüssel nachgemacht werden. Dazu kommen viele Kettenbetriebe mit demselben
Namen an vielen Adressen und viele Callcenter-Einträge ohne Ortsbezug. **Gate 2 löscht keine
Zeile wegen ihres Gewerbes.** Der Bericht schlüsselt die behaltenen Zeilen nach `type`
(Haupt-Kategorie) auf, zählt die Zeilen, die nur über die Kategorie hereinkamen, mit ihren
häufigsten Haupt-Kategorien, nennt Namen, die an mehr als drei Adressen vorkommen, und nennt
Einträge ohne Ortsbezug. **Der Mensch entscheidet in Gate 4.**

Ergebnis: `02-listings-clean.csv`, `02-domains.txt`, `02-clean-report.md` (Zeilen hinein,
Zeilen heraus, Grund).

### Gate 3, Anreichern

Zuerst die **Merkmalsdatei** `output/<slug>/03-attributes.json` für Schlüsseldienste
schreiben: 8 bis 15 Merkmale, jedes mit `key`, `label`, `faq`, `true_when` und `pattern`; die
Form steht in `scripts/examples/README.md`. Kein Merkmal darf eine Lizenz, eine Zulassung
oder eine Zertifizierung behaupten; es gibt sie in diesem Gewerbe nicht ([[konventionen]]).
Zulässig und belegbar: Notdienst rund um die Uhr, zerstörungsfreie Öffnung, Festpreis vor
Anfahrt, Anfahrtspauschale genannt, Einbruchschutz und Nachrüstung, Schließanlagen,
Tresoröffnung, Autoschlüssel, eigene Werkstatt, Gewerbeanmeldung und Handelsregistereintrag.
Ein Merkmal darf `core: true` tragen und festhalten, ob der Betrieb die Kernarbeit überhaupt
leistet (Türöffnung und Schließtechnik); was mit Zeilen geschieht, die darauf `false`
antworten, entscheidet der Mensch in Gate 4.

Dann je behaltenem Eintrag die Merkmale mit `wahr` / `falsch` / `keine Angabe` füllen und eine
Beschreibung in einer Stimme schreiben, aus `reviews_tags`, `about`, `subtypes` und
`description`. Trägt der Export keinen solchen Text, lies die eigene Website des Betriebs:
`fetch_sites.py`, dann `build_evidence.py --patterns 03-attributes.json` (beide kostenlos),
dann `make_batches.py --attributes 03-attributes.json`, jeden Stapel unter
`scripts/enrichment-instructions.md` beantworten, und `merge_enriched.py` schreibt die CSV
erst, wenn jede Antwort besteht. Die Stapel laufen als Subagenten oder mit
`scripts/run_batches.py enrich --slug <slug>`.

**Kosten vorher nennen**, aus der gemessenen Belegmenge. Die Messwerte stammen aus dem
englischen Pilotprojekt und sind nur Größenordnungen: etwa 4.000 Token je Eintrag bei
Subagenten auf Sonnet, etwa 4 Cent je Eintrag über den Stapelläufer auf Sonnet. Dann einen
kleinen Probestapel laufen lassen und lesen, bevor der Rest folgt. Nach Bundesland und Stadt
stapeln, zwischenspeichern. Danach `03-cache/review.md` lesen und die Antwortdateien
nachbessern, bevor das Gate freigegeben wird.

Eine Beschreibung nennt die Tatsachen und nie ihre Quelle: kein „laut Website", kein „die
Seite nennt", kein „auf Google Maps", und kein Satz darüber, was unbekannt ist. Jede Aussage
muss sich auf den Stapel zurückführen lassen. Sie beginnt mit etwas, das nur für diesen
Betrieb gilt; ein Satzanfang, den vier oder mehr Einträge teilen, lässt den Zusammenbau
scheitern.

Ergebnis: `03-listings-enriched.csv`, `03-attributes.json`, `03-enrich-report.md`.

### Gate 4, Planen

Aus der angereicherten CSV, [[site-architecture]] und dem [[master-template]]: Aufbau vom
Template, Optik von der Vorlage, Tatsachen aus den Daten.

Der Plan legt fest:
- welche **Bundesländer** eine Seite bekommen (jedes mit mindestens einer Stadtseite) und in
  welcher Reihenfolge sie auf der Startseite stehen
- welche **Städte** eine Seite bekommen, Mindestzahl Einträge je Stadt
- die **Seitenzahl** je Ebene und den schlanken Start: welche Seiten zum Start in die Sitemap
  kommen ([[launch-lean]])
- URL-Slugs nach der Tabelle in [[konventionen]], Umlaute umgeschrieben
- die Anordnung der bezahlten Plätze ([[monetization-slots]]) und, je Stadt, höchstens **ein**
  bezahlter Platz für einen eigenen Betrieb ([[footprint-rules]])
- die **Gestaltungsmarken** aus der Optikvorlage, ausgehend von den Marken des Templates, jede
  Änderung festgehalten ([[design-seed]])
- `foldMaxKm` (Vorgabe 40 km) und wie viele Ortsseiten daraus entstehen
- die **Leistungsseiten**: Merkmale, nach denen Menschen als Leistung suchen (nie ein
  Vertrauenszeichen, nie eine Lizenz), jede mit Slug, Titel und Zahl bestätigter Einträge

**Die Branchenbesonderheit entscheidet der Mensch, hier:** Der Plan legt dem Betreiber die
Listen aus dem Gate-2-Bericht vor und fragt je Gruppe nach einer Entscheidung:
1. **Fremde Gewerbe** – Schuhmacher, Gravurbetriebe, Metallbauer, Baumärkte, die über die
   Kategorie `locksmith` hereinkamen. Sie machen Schlüssel nach, öffnen aber keine Türen.
   Vorschlag zur Entscheidung, kein Vorgabewert.
2. **Kettenbetriebe** – derselbe Name an vielen Adressen. Vorschlag: je Stadt eine Zeile
   behalten, die übrigen Adressen derselben Stadt zusammenführen.
3. **Callcenter ohne Ortsbezug** – Einträge, deren Nummer ortsfremd ist und die keine
   erreichbare Adresse haben. Sie verfehlen Kriterium 5 des Siegels ([[siegel-programm]]);
   ob sie im Verzeichnis bleiben, entscheidet der Betreiber.

Der Blueprint hat für keine dieser Gruppen einen Vorgabewert, der eine Zeile löscht. Jede
Entscheidung, die einen Eintrag entfernt oder verändert, geht nach `04-exclusions.csv`
(`slug, action, reason`), nie in die angereicherte CSV.

Der Plan setzt `niche.schemaType` auf `Locksmith` ([[schema]]) und endet mit einer
nummerierten Tabelle der Entscheidungen, jede mit einem Vorschlag.

Ergebnis: `04-plan.md` und `04-exclusions.csv`.

### Gate 5, Bauen

`templates/astro/` nach `output/<slug>/site/` kopieren und füllen, kein Astro-Projekt von
Hand schreiben. Das Grundgerüst setzt [[site-architecture]], [[page-types]],
[[on-page-rules]], [[schema]] und den Sitemap-Filter des schlanken Starts schon um. Zu füllen
sind: `src/data/site.json` (Marke, Domain, Herausgeber, Kontakt, Bundesländer, Preisstufen,
Gestaltungsmarken aus `04-plan.md`), `src/styles/fonts.css` (selbst gehostete Schriften),
`src/data/listings.csv`, `src/data/attributes.json`, `src/data/city-copy.json`, die Texte der
Seite „Über uns" und angeforderte Ratgeberseiten.

**Vor jedem Text die Faktensammlung `05-fact-sheet.md` bauen.** Jede Aussage über Recht,
Gewerbe, Preise oder örtliche Besonderheiten mit Quelle, dazu was die Texte nicht behaupten
dürfen. Quellen in dieser Reihenfolge ([[konventionen]]): Handwerkskammer des Bezirks,
Stadt- und Gemeindeportale (Gewerbeamt), Verbraucherzentrale des Bundeslandes, Polizeiliche
Kriminalprävention (`polizei-beratung.de`), Stiftung Warentest. Nicht als Quelle: andere
Schlüsseldienst-Websites, Branchenbücher, Presseportale. Ein Punkt mit nur einer
kommerziellen Quelle gilt als **unbelegt** und darf in keinem Text auftauchen. Jeder Punkt
hält Adresse und Abrufdatum fest. Der Verfasser der Faktensammlung darf dafür das Netz
abrufen und suchen (die Stadttext-Läufer nicht).

Die Faktensammlung hält außerdem fest: **Schlüsseldienst ist in Deutschland kein
zulassungspflichtiges Handwerk nach Anlage A der Handwerksordnung. Es gibt keine Lizenz und
keine Meisterpflicht.** Kein Text darf „lizenziert", „zugelassen" oder „zertifiziert"
behaupten. Erlaubt und belegbar: Gewerbeanmeldung, Eintragung im Handelsregister, freiwillige
Mitgliedschaften, Qualifikationen, die der Betrieb selbst nennt.

**Gate 5 erzeugt außerdem zwei Pflichtseiten aus den Herausgeberdaten in `site.json`:**
- `/impressum/` nach § 5 DDG: Firma, Rechtsform, Anschrift, Geschäftsführer,
  Handelsregister und -nummer, Umsatzsteuer-Identifikationsnummer falls vorhanden,
  Telefonnummer und E-Mail-Adresse, Verantwortlicher für den Inhalt.
- `/datenschutz/` nach Art. 13 DSGVO: Verantwortlicher, Zwecke und Rechtsgrundlagen,
  Empfänger (Cloudflare als Hoster), Speicherdauer, Rechte der Betroffenen, Beschwerderecht
  bei der Aufsichtsbehörde, Herkunft der Firmendaten und der Bewertungen, Widerspruchsrecht
  und der Weg zur Korrektur oder Löschung eines Eintrags.

Beide Seiten sind im **Fußbereich jeder Seite** verlinkt. **Der Build gilt als unfertig,
solange eine der beiden Seiten einen Platzhalter enthält**; `05-build-report.md` führt das als
Startsperre. Das Wiki sagt, welche Seiten und Angaben Pflicht sind – es ist keine
Rechtsberatung. Die Endfassung beider Seiten sollte ein Anwalt prüfen; das steht im
Build-Bericht.

**Keine Einwilligung, keine externe Ladung.** Keine Karte, kein externes Skript und keine
externe Schrift lädt ohne Einwilligung. Google Maps erscheint erst nach Klick: an der Stelle
der Karte eine Platzhalterfläche mit der Schaltfläche „Karte von Google Maps laden" und einem
Satz, dass dabei Daten an Google übertragen werden. Schriften werden selbst gehostet
(`fonts.css`), nie von Google geladen. Kein Google Analytics, keine Search Console auf dieser
Domain ([[footprint-rules]]).

Stadttexte entstehen aus Paketen (`node dump-cities.mjs`, dann
`scripts/make_city_packets.py`) unter `scripts/city-copy-instructions.md`, und nur
`scripts/check_city_copy.py --write` erzeugt `city-copy.json`. Wortuntergrenzen je Stadtgröße
in [[page-types]]. Danach das **Textgate** ([[copy-gate]]): `scripts/lint_copy.py` auf
`city-copy.json`, auf die gebauten Seiten Startseite, Bundesland und „Über uns" in `dist/`
und auf jede Ratgeberseite; nachbessern und erneut prüfen, bis jeder Block besteht.
Ratgeberseiten und der Ratgeberblock der Startseite entstehen mit der
**seo-content-engine**-Skill, wenn sie verfügbar ist. Stadtblöcke und Stadt-Fragen werden nie
mit der Skill erzeugt, nur von ihr geprüft.

Die gebauten Seiten mit denselben Seiten in `templates/master-reference/site/` vergleichen
(gleiche Abschnitte in gleicher Reihenfolge; aus ihrem Inhalt wird nie etwas übernommen,
schon weil er englisch und aus einer anderen Branche ist), dann die Merkmalsliste aus
[[design-seed]] durchgehen. `npm install && npm run build` muss ohne Warnung über fehlende
Daten durchlaufen.

Dann die gebauten Seiten prüfen: je Seite ein H1 und ein Titel, `lang="de"`, JSON-LD das
sich einlesen lässt und kein `aggregateRating` trägt, kein gebrochener interner Link, keine
`noindex`-Seite in der Sitemap, kein Platzhaltertext, Impressum und Datenschutz vollständig
und im Fußbereich verlinkt, Telefonnummern im deutschen Format ([[konventionen]]),
„Geprüft 2026" beziehungsweise „Noch nicht geprüft" auf jedem Eintrag
([[siegel-programm]]). `featuredPreview` muss im ausgelieferten Build `false` sein.

Ansehen: `preview-site.command` (Mac) oder `preview-site.bat` (Windows) in `site/`
doppelklicken. Nie auf `dist/index.html` verweisen, das zeigt ohne Server keine Gestaltung.

Ergebnis: `output/<slug>/site/` und `05-build-report.md` mit allem, was offen ist und was den
Start sperrt.

### Gate 6, Schlanker Start

[[launch-lean]] anwenden: starke Seiten in die Sitemap, dünne Einträge auf `noindex`, dann
nach Cloudflare Pages ausliefern und die Adressen gestaffelt einreichen. Prüfen, dass der
Build `404.html` und `_headers` mitbringt. Mit Wrangler ausliefern
(`npx wrangler pages deploy dist`); Ziehen und Ablegen bricht bei 1.000 Dateien ab. Das
Projekt einmal anlegen (`npx wrangler pages project create <name> --production-branch main
--force`), danach ohne `--force` ausliefern. Die Domain registriert der Betreiber, bei
Cloudflare melde sich der Betreiber an; du legst kein Konto an und gibst keine Zugangsdaten
ein. Das Verzeichnis liegt auf einem **eigenen Cloudflare-Konto**, getrennt von den
Schlüsseldienst-Websites ([[footprint-rules]]). Nach dem Ausliefern `scripts/check_live.py`,
und erst nach bestandener Prüfung die Staffel starten.

Ergebnis: `06-launch.md` mit dem Indexierungsplan, der geordneten Adressliste, den
Erweiterungsstufen und dem Termin der 30-Tage-Prüfung.

### Neu bauen bei Änderung

Verkaufter Platz, bestätigter Eintrag, neu erteiltes Siegel, neue Stadt: CSV ändern, Gate 5
erneut laufen lassen, erneut ausliefern. **Nie eine erzeugte Seite von Hand bearbeiten.**

### Nach dem Start: der Mail-Worker

[[mail-worker]], wahlweise, auf Wunsch des Betreibers, nie Teil eines Gates. Ein Cloudflare
Email Worker gibt dem Verzeichnis eine echte Adresse: feste Empfangsbestätigung innerhalb
einer Minute, Einordnung durch Claude, eine Prüfseite mit „Senden" und „Übergehen". Er ändert
nie einen Eintrag und sendet nie von sich aus. Anfragen zum Siegel verweist er auf
`/siegel/antrag/`. Die Texte stehen in `output/<slug>/worker/src/templates.ts`.

### Pflege

[[refresh-and-upkeep]]: keine Zugänge für Betriebe, jede Beanspruchung und jede Siegelprüfung
von Hand, bevor sich die CSV ändert. Einmal im Jahr die Siegel erneuern
([[siegel-programm]]).

---

## 4. Technik

- **Astro, statische Ausgabe, Cloudflare Pages.** Kein Server, keine Datenbank in Fassung 1.
- Ein Projekt je Verzeichnis, `npm run build` erzeugt `dist/`.
- Jede Seite trägt vollständige Seitentechnik und JSON-LD nach [[schema]], echte
  `sitemap.xml`.
- Kein Google Analytics, keine Search Console auf dieser Domain ([[footprint-rules]]).
- `lang="de"`, Preise in Euro, Datum `TT.MM.JJJJ`, Komma als Dezimaltrennzeichen.
- Das Beanspruchungsformular geht an einen Formulardienst ohne eigenen Server oder, sobald
  eingerichtet, an `/claim` des Mail-Workers. Die Preisstufen sind **Stripe-Zahlungslinks**,
  eingetragen in `templates/featured-tiers.md`. Verkauft wird von Hand: Spalte `premium`,
  `featured` oder `best_of_rank` setzen, neu bauen.
- Einträge ohne Beanspruchung tragen keine Fotos. Fotos kommen vom Inhaber, mit der
  Beanspruchung oder einer bezahlten Stufe ([[page-types]]).
- Tatsachen stehen als sichtbarer Text. Keine Auf- und Zuklapper, keine Reiter für Fragen,
  Öffnungszeiten oder Merkmale.
- Jedes Verzeichnis ist das [[master-template]]: Aufbau, Seitensatz, Adressen, Navigation und
  Abschnittsfolge kommen aus `templates/astro/`. Genannte Websites sind nur Optikvorlagen
  ([[design-seed]]).
- Der Herausgeber steht auf „Über uns" mit `Organization`-Schema; der Geschäftsführer mit
  `Person`-Schema ([[publisher-entity]], [[authority-and-links]]).
- Das Siegel wird als HTML-Schnipsel weitergegeben, der auf die Eintragsseite verlinkt, nie
  als Bilddatei ([[siegel-programm]]).

---

## 5. Datenquellen

Zwei Wege in `input/listings-raw.csv`, gleiche Spalten ([[outscraper-columns]]), gleiches
Gate 2.

- **DataForSEO Business Listings API** (`scripts/fetch_dataforseo.py`, Vorgabe bei
  gespeicherter Anmeldung). Kategoriegenau: eine Kategorie in einem Gebiet kommt als die
  bewerteten Betriebe zurück. Die Anmeldung ist die DataForSEO-API-Anmeldung, einmal im
  eigenen Terminal gespeichert: `python3 scripts/connect_dataforseo.py`. Das Skript liest sie
  aus `~/.claude.json`, aus der Umgebung oder aus einem Claude-Desktop-Eintrag, nie aus einer
  Datei in diesem Ordner, und fragt sie nie im Gespräch ab. Es nennt die Kosten immer vor dem
  Abruf. `--find-category <wort>` listet die Kategorie-Kennungen, kostenlos. `--estimate`
  kostet etwa fünf Cent. Zu nennende Einschränkungen: die Datenbank hat kein Merkmal für
  Geschäftsaufgabe (Gate 2 löscht Zeilen ohne Aktualisierung seit zwölf Monaten), etwa ein
  offener Betrieb von zwanzig fehlt, ein Betrieb kann über eine Nebenkategorie erscheinen
  (Gate 2 behält diese Zeilen und berichtet sie, Gate 4 entscheidet), und E-Mail-Adressen
  brauchen eine Domainprüfung und einen Zustellversuch.
- **Outscraper-Export**: der Betreiber scrapt die Kategorie selbst und legt die CSV als
  `input/listings-raw.csv` ab.
- Die **DataForSEO-MCP-Werkzeuge** im Gespräch sind für Recherche und für die
  seo-content-engine-Skill, nicht für den Abruf.
- Kein Weg über erfundene oder Beispieldaten. Ein Build beginnt mit echten Einträgen oder
  wartet darauf.

---

## 6. Textwerkzeuge

- **`skills/seo-content-engine/`** wird in Gate 5 auf zwei Weisen gebraucht
  ([[copy-gate]]): ihr `scripts/lint_article.py` prüft jeden kurzen Block über
  `scripts/lint_copy.py`, ohne Zugang; ihr vollständiger achtstufiger Ablauf schreibt die
  artikelförmigen Seiten (Ratgeberseiten, der Ratgeberblock der Startseite) und braucht die
  DataForSEO-Anmeldung. Die Skill erkennt die Verbindung am Werkzeugnamen, also wird nie ein
  Zugang in diesen Ordner geschrieben; `references/credentials.md` bleibt leer.
- Die Skill nie auf Stadtblöcke anwenden. Sie schreibt je Lauf einen langen Artikel; sechzig
  Stadtseiten wären sechzig Läufe in der falschen Form. Der Stadtblock sind 500 bis 800 Wörter
  aus den Daten, von dir geschrieben, vom Gate geprüft.
- Die Wortliste der verbotenen Werbefloskeln liegt in
  `skills/seo-content-engine/references/forbidden_words.txt` und ist deutsch.

---

## 7. Stand

Deutsche Fassung vom 2026-11-03, aus der englischen Fassung vom 2026-10-05 übertragen. Dieses
Verzeichnis ist noch nicht gebaut: es gibt keine deutschen Messwerte. Alle Zahlen in diesem
Wiki, die aus einem echten Lauf stammen, kommen aus dem **englischen Pilotprojekt** (einem
Verzeichnis für Poolbauer in Florida und einem Testlauf für Zaunbauer in Colorado) und sind
als solche gekennzeichnet. Sie sind Größenordnungen, keine Zielwerte, und über den deutschen
Markt sagen sie nichts.

Bekannte Lücken: gesperrte und per Skript aufgebaute Websites werden nicht mit einem Browser
nachgeholt; keine Qualifikation eines Betriebs wird je überprüft (in diesem Gewerbe gibt es
auch keine Lizenz, die zu prüfen wäre); die seo-content-engine-Skill ist noch in Prüfung.
