# DBS-WEB-DESIGN-PILOT1 — Implementierungsauftrag für Claude Code

**Projekt:** Die besten Schlüsseldienste · `die-besten-schluesseldienste.de`
**Repository:** das Verzeichnis-Blueprint-Repo (`~/directory/blueprint`), Build-Ordner
`output/schluesseldienste-deutschland/site/`. **Nicht** das Henry-Repo `boxofbananas/henry-workspace` —
das ist nur die Herkunft der Bildreferenzen, dort wird nichts gelesen und nichts geschrieben.

**Ziel:** Ein sichtbarer, funktionierender Gestaltungs-Pilot für die Startseite und die Mannheimer
Stadtseite, Desktop und mobil, in einem Arbeitsbranch. Du implementierst, du berätst nicht.

---

## 0. Sperren — gelten für den ganzen Auftrag

- **Kein Live-Deployment.** Kein `wrangler` in irgendeiner Form, auch keine Vorschau auf `pages.dev`
  (das wäre eine neue öffentliche Kopie). Kein `scripts/verkauf.py` (liefert aus). Kein `check_live.py`
  als Abnahme — die Live-Seite bleibt, wie sie ist.
- **Kein Merge nach `main`, kein Commit auf `main`.** Den Arbeitsbranch darfst du pushen.
- **Kein Rückport nach `templates/astro/`.** Der Pilot ist nicht freigegeben.
- `wiki/konventionen.md` wird nicht geändert. `CLAUDE.md` gilt unverändert, insbesondere:
  nie eine erzeugte Seite von Hand bearbeiten (nur `src/`), keine externe Schrift, kein externes
  Skript, keine Karte ohne Klick, Tatsachen als sichtbarer Text ohne Auf- und Zuklapper.
- Keine Änderung an Daten: `listings.csv`, `city-copy.json`, `attributes.json`, Garantie-Spalten,
  Hauptbuch, Impressum, Datenschutz, AGB, Preise, Stripe-Links bleiben unberührt.
- Höchstens **zwei** gezielte Korrekturrunden nach dem ersten Stand. Keine endlose Stilfindung.

## 1. Ausgangslage feststellen und Arbeitskopie anlegen

1. `git status`, aktueller Branch und Commit von `main` im Bericht festhalten. Liegt nicht
   committete fremde Arbeit im Baum: nicht anfassen, melden, im Worktree weiterarbeiten.
2. Der Arbeitsbranch `design/pilot1` **existiert bereits auf origin**: Er zweigt vom aktuellen
   `main` ab und enthält nur diesen Ordner `design-pilot1/` (Auftrag, Original-Übergabe, die drei
   Referenzbilder). `git fetch origin`, dann einen **eigenen Worktree** darauf anlegen
   (`git worktree add ../blueprint-pilot1 design/pilot1`), damit der Hauptbaum für Verkäufe und
   Neubauten frei bleibt. Ist `main` inzwischen weiter, `main` in den Branch mergen. Im Worktree
   `npm install`.
3. Bevor du etwas änderst: im Worktree bauen und bestätigen, dass der Ausgangsstand dem Live-Stand
   entspricht (Seitenzahl, Sitemap **2823** Adressen). Weicht er ab, anhalten und melden.
4. Aus diesem unveränderten Build die **Basisdaten für den Vergleich** sichern (Abschnitt 6):
   Liste aller Adressen in `dist/`, je Seite Titel, Meta-Description, Canonical, robots, H1 und der
   JSON-LD-Block, dazu `sitemap`-Adressen.

## 2. Die Referenzen

Die drei PNGs liegen im Branch unter `output/schluesseldienste-deutschland/design-pilot1/referenzen/`.
Sieh sie dir mit dem Read-Werkzeug an, bevor du baust. Die Original-Übergabe liegt daneben als
`uebergabe-original.md`; bei Widerspruch gilt dieser Auftrag.

| Datei | Rolle |
|---|---|
| `02-hero-horizontal.png` | **Wichtigste Richtung.** Dunkler Inhaltsbereich links mit großer Überschrift und Suche, rechts eine helle, ruhige Verzeichnisdarstellung als Karte. |
| `03-verzeichnis-ansicht.png` | Ergebnisbereich: getrennte Orientierungsspalte links, klar gegliederte Eintragskarten rechts. |
| `01-markenmotiv-quadrat.png` | Nur Stimmung: Farben und Schriftkombination. Kein Layout. |

Es sind Medienmotive, keine Weblayouts. Übersetzt wird die Qualität: großzügige Abstände, markante
Überschriften, ruhige Flächen, klare Karten, große Radien, weiche Schatten.

**Farben: an den PNGs gemessen, nichts zu ändern.** Die Referenzen wurden erkennbar aus den
vorhandenen Marken gebaut:

| Im Bild gemessen | Vorhandene Marke in `site.json` |
|---|---|
| Navy `#0B2644` | `band` / `heading` / `headerBg` `#0B2545` |
| Bernstein `#F4A81F`–`#F9A529` | `action` `#F5A623` |
| Petrol `#0F6566`–`#146664` | `link` `#126665` |
| helle Tönung `#E7F2F4` | `tint` `#E6F2F4` |
| Fläche `#F5F6F8` | `surface` `#F5F6F8` |

Die Abweichungen sind Renderrauschen. **Die Farbmarken und die Schriften (Roboto Slab, Roboto,
selbst gehostet über `fonts.css`) bleiben, wie sie sind.** Keine neue Schriftdatei. Der Pilot ist
damit Layout- und Komponentenarbeit, keine neue Palette.

**Nicht übernehmen:** graue Platzhalterbalken als Inhalt, beliebige Symbolkacheln (`+`, `○`, `^`),
die Karte mit Stecknadeln, das Rasterlinien-Muster, die zweifarbige Fortschrittslinie, das große
„D". Das „D" ist kein Logoauftrag: `logoText` und Favicon bleiben.

## 3. Vorher-Screenshots

Aus dem unveränderten Build, lokal ausgeliefert (wie bei deinen früheren Prüfungen), **ganze Seite**:

- Seiten: `/` und `/verzeichnis/baden-wuerttemberg/mannheim/`
- Ansichten: Desktop **1440 × 900**, mobil **390 × 844**

Mannheim, weil dort alles vorkommt: ein belegter Premium-Platz mit Garantie-Zeile, die freie Karte,
Einträge mit und ohne Festpreis-Garantie, ein Eintrag ohne Bewertung und der lange Name
„Merz Sicherheit • Einbruchschutz, Schließanlagen & Schlüsseldienst".

Ablage: `output/schluesseldienste-deutschland/design-pilot1/screenshots/vorher-*.png`.

## 4. Umsetzung

Alles im bestehenden System: `src/styles/global.css`, die vorhandenen Komponenten, Marken aus
`site.json` über `Base.astro`. **Kein zweites Stylesheet-System, keine Seitenkopien, kein
CSS-Framework.** Lies vorher [[design-seed]], [[master-template]], [[page-types]] und
[[on-page-rules]]; Abschnitte und ihre Reihenfolge bleiben je Seitentyp, wie sie sind — geändert
wird die Optik.

### 4a. Gemeinsame Gestaltung

- **Neue Marken nur, wo nötig**, in `site.json` → `design` und über `Base.astro` als CSS-Variablen:
  ein großer Kartenradius (Referenz etwa 20–24 px), ein weicher Kartenschatten, eine Abstandsskala
  für Abschnitte. Schaltflächen und Suchfeld in Pillenform (`buttonRadius`). Jede neue oder
  geänderte Marke mit Wert und dem Vermerk **„aus PNG abgeleitet, Pilot 1"** in
  `04-plan.md` (Gestaltungsmarken) festhalten.
- **Kopfzeile:** ruhiger, mehr Luft; Markenname, Navigation und die Schaltfläche „Eintrag
  beanspruchen" bleiben mit denselben Zielen. Mobil darf nichts umbrechen oder überlaufen.
- **Karten** (`Card.astro`, `FeaturedBand.astro`): weiße Fläche, großer Radius, weicher Schatten,
  klare Hierarchie. Keine farbigen Kartenränder ([[design-seed]]).
- **Fokus und Kontrast:** sichtbarer Fokusring auf jedem Link, Feld und Knopf; Kontraste messen
  (AA), Messwerte in den Bericht. Bernstein trägt weiterhin nur dunkle Schrift.
- Zeichen nur als Inline-SVG wie `Star.astro` und `Check.astro`. `check-glyphs.mjs` muss grün
  bleiben.

### 4b. Startseite

Richtung: `02-hero-horizontal.png`.

- **Kopfbereich zweispaltig ab etwa 1024 px.** Links auf Navy, linksbündig statt zentriert:
  die eine Augenbraue („Schlüsseldienste in Deutschland"), die **bestehende H1 „Damit die Rechnung
  keine Überraschung wird."** samt Hervorhebung, der bestehende Vorspann, die bestehende Suche und
  die bestehenden `heroPoints`. Kein Wort davon wird ersetzt. Der Markenname wird **nicht** zur
  Hauptüberschrift, und „Online-Branchenverzeichnis für Deutschland" kommt nicht als Ersatztext.
- **Suche:** `SearchForm.astro` behält Ziel, Feldnamen und Verhalten exakt. Sie wird groß und
  eindeutig (Pillenform, Lupe als SVG, Schaltfläche in Bernstein) und bekommt eine **sichtbare
  Beschriftung**. Keine neue Suchlogik, kein zweites Feld, das nichts tut.
- **Rechts eine helle Übersichtskarte** auf heller Fläche, mit klarer Trennung zum Navy-Bereich
  (schräge oder gerade Kante, höchstens **ein** weicher Kreis als Zierde, alles in CSS). Die Karte
  zeigt **echte Daten statt grauer Balken**: oben ein Block „Standort wählen — Stadt oder
  Bundesland" als Link auf `/verzeichnis/`, darunter unter der Zwischenzeile „Verzeichnisübersicht"
  drei Zeilen mit den ersten drei Bundesländern in der Reihenfolge, die die Startseite schon
  verwendet, je mit Zahl der Städte und Einträge **aus dem Datenlayer** und Link auf die
  Bundesland-Seite. Keine Zahl von Hand, kein Firmenname, kein erfundener Eintrag. Jede Zeile ist
  ein echter Link; nichts sieht bedienbar aus, das es nicht ist.
- **Darunter** bleiben Zählkarten, `DirectoryHub`, Premium-Band, Ratgeberblock, Fragen und alles
  Übrige inhaltlich und in ihrer Reihenfolge erhalten; sie bekommen die gemeinsamen Karten,
  Abstände und Flächen. Der Übergang vom Kopfbereich in die getönte Fläche muss sauber bleiben
  (die Zählkarten liegen heute über der Farbkante — das darf nicht brechen).
- **Mobil:** einspaltig in der Reihenfolge Augenbraue, H1, Vorspann, **Suche**, Punkte — erst
  danach die Übersichtskarte. Die Suche steht auf 390 × 844 im ersten Bildschirm.

### 4c. Stadtseite

Richtung: `03-verzeichnis-ansicht.png`. Gebaut in der Vorlage
`pages/verzeichnis/[bundesland]/[stadt]/index.astro`, gilt also für alle Stadtseiten; abgenommen
wird an Mannheim.

- **Abschnittsfolge unverändert.** Stadttext, Fragen, Sprungliste, Premium-Band, Einträge, Liste
  der weiteren Einträge: nichts fällt weg, nichts wechselt den Platz in der Dokumentreihenfolge.
- **Ergebnisbereich zweigeteilt ab etwa 1024 px:** links eine schmale Orientierungsspalte auf
  getönter Fläche (`tint`) mit dem, was die Seite **heute schon** zur Orientierung hat — Suche,
  Sprungliste, vorhandene Verweise auf Bundesland und Nachbarorte —, rechts die Einträge. Die
  Spalte darf beim Scrollen stehen bleiben. **Keine Karte, kein Filter, den es nicht gibt.**
- **Eintragskarten** als klar gegliederte Zeilenkarten statt enger Kacheln: Name als Überschrift
  (bricht um, wird nie abgeschnitten), Bewertung mit Stern und Anzahl, Ort, die Zeile
  „Festpreis-Garantie · Türöffnung ab … €" beziehungsweise „Noch keine Festpreis-Garantie" wie
  bisher, die belegten Merkmale, Telefon als `tel:`-Link im deutschen Format, „Eintrag ansehen" als
  ruhige Pille rechts. **Jede Angabe, die heute auf der Karte steht, steht danach auch dort.**
  Fehlt ein Wert (keine Bewertung, kein Telefon), entfällt die Zeile sauber — nichts wird gefüllt.
  Keine Fotos, keine Symbolkacheln für Einträge ohne Beanspruchung.
- **Premium-Band:** Merz oben, dahinter genau **eine** freie Karte, Garantie-Zeile sichtbar,
  Abzeichen „Premium" bleibt. Reihenfolge und Logik aus `load.mjs` werden nicht angefasst.
- **Mobil:** Orientierung kompakt über den Einträgen, Karten einspaltig, Telefonlink gut treffbar
  (mindestens 44 px hoch).

### 4d. Texte

Neuer sichtbarer Wortlaut nur, wo die Gestaltung ihn braucht (Feldbeschriftung, „Standort wählen",
„Verzeichnisübersicht"). Keine neuen Werbezeilen, keine neuen Aussagen über Preise, Prüfung oder
Qualität, kein „garantiert". Jeder neue oder geänderte Textblock geht durch `scripts/lint_copy.py`
— die Startseite **ohne** `--erlaube-rechtswoerter`.

## 5. Ausdrücklich unverändert

Adressen und Routen · Titel, Descriptions, Canonicals, robots · JSON-LD (kein neuer Typ, kein
`aggregateRating`) · Sitemap und `noindex`-Regeln · interne Links und ihre Ziele · Sortierung der
Einträge · Formulare und `/api/claim` · Einwilligungs-Klick für Google Maps · Fußbereich mit
Impressum und Datenschutz · H1 je Seite genau einmal, `lang="de"`.

## 6. Prüfungen (Ergebnisse in den Bericht, auch die roten)

1. `npm run build` ohne Warnung, `check-glyphs` grün.
2. **Vergleich gegen die Basisdaten aus Abschnitt 1**, über alle Seiten: gleiche Adressliste,
   gleiche Sitemap (2823), je Seite identische Titel, Descriptions, Canonicals, robots und H1,
   JSON-LD inhaltsgleich. Auf Startseite und Mannheim zusätzlich: Menge der internen Linkziele
   vorher gegen nachher; jeder weggefallene Link wird begründet oder zurückgeholt.
3. **Funktion im lokalen Build, im Browser:** Suche von der Startseite und von der Stadtseite
   liefert dieselben Treffer wie vorher · Navigation und Sprungliste springen richtig ·
   `tel:`-Links und „Eintrag ansehen" führen zum richtigen Eintrag · Tastatur: mit Tab durch
   Kopfzeile, Suche und die ersten Karten, Fokus immer sichtbar · ohne Klick keine Anfrage an einen
   fremden Host.
4. **Darstellung:** kein horizontaler Überlauf bei 320, 390, 768, 1024 und 1440 px · der lange
   Merz-Name und der Eintrag ohne Bewertung sitzen sauber · zusätzlich eine Stadt ohne bezahlten
   Platz (Leipzig) und eine kleine Stadt mit zwei Einträgen ansehen, dass die Vorlage dort nicht
   bricht.
5. Textgate für geänderte Blöcke bestanden.
6. Was du **nicht** prüfen konntest (echte Geräte, Screenreader, andere Browser), steht als Grenze
   im Bericht. Keine Behauptung vollständiger Barrierefreiheit.

## 7. Nachher-Screenshots und Übergabe

- Nachher-Screenshots derselben zwei Seiten in denselben zwei Größen mit denselben Daten:
  `design-pilot1/screenshots/nachher-*.png`. Sieh sie dir selbst an und vergleiche mit den
  Referenzen, bevor du abschließt.
- `berichte/2026-11-12-design-pilot1.md` mit: Repo, Ausgangscommit, Arbeitsbranch und Commit ·
  Liste der Änderungen je Datei · bewusst erhaltene Funktionen · neue Marken mit Werten ·
  Prüfergebnisse und Grenzen · **der Weg, auf dem Daniel den Stand wirklich ansehen kann** (die
  Screenshot-Dateien mit Pfad für den SFTP-Abruf und der genaue Befehl für die lokale Vorschau;
  keine erfundene Adresse).
- `design-pilot1/rueckgabe-henry.md`, höchstens eine Seite: wiederverwendbare Layoutentscheidungen,
  konkrete Problemfälle der Referenzen im echten Layout, Markenwerte nur **als Vorschlag**. Nichts
  wird ins Henry-Repo, in Skills oder in eine Learning-Registry geschrieben.
- In [[template-build-drift]] ein Eintrag „Design-Pilot 1 — nicht freigegeben, nicht portiert"
  mit den betroffenen Dateien. Log-Zeile in `wiki/log.md`. Commit auf `design/pilot1`, Branch
  pushen.

Dann **anhalten**. Zusammenführen und Ausliefern geschehen erst nach Daniels Freigabe in einem
eigenen Auftrag.
