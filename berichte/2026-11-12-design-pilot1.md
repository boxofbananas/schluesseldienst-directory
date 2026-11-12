# Design-Pilot 1 — Startseite und Mannheimer Stadtseite

**Datum:** 2026-11-12
**Auftrag:** `output/schluesseldienste-deutschland/design-pilot1/DBS-WEB-DESIGN-PILOT1-Auftrag-Claude-Code.md`

## Repo, Branch, Commit

- **Repo:** das Verzeichnis-Blueprint-Repo (`~/directory/blueprint`), Build-Ordner
  `output/schluesseldienste-deutschland/site/`. **Nicht** das Henry-Repo (nur Herkunft der Bilder).
- **Ausgangsstand:** `main` = `11f8445`. Der Branch `design/pilot1` zweigt davon ab; seine Basis ist
  `a6caf22` (= `main` + Auftrag und Referenzbilder). `main` war nicht weiter, **kein Merge nötig**.
- **Arbeitskopie:** eigener Worktree `../blueprint-pilot1` auf `design/pilot1` (Hauptbaum unberührt).
  Der Hauptbaum war zu Beginn sauber, keine fremde unversionierte Arbeit.
- **Diese Pilot-Arbeit** ist der Commit auf `design/pilot1` direkt über `a6caf22`.
- **Gesperrt eingehalten:** kein `wrangler`, keine `pages.dev`-Vorschau, kein `verkauf.py`, kein
  `check_live.py`; kein Merge/Commit auf `main`; kein Rückport ins Template; `konventionen.md`
  unverändert; keine Datenänderung (listings.csv, city-copy.json, attributes.json, Garantie-Spalten,
  Hauptbuch, Impressum, Datenschutz, AGB, Preise, Stripe-Links unberührt).

## Ausgangsstand bestätigt

Im Worktree `npm install`, `npm run build`: **4647 Seiten**, Sitemap **2823 Adressen** — entspricht
dem Live-Stand. Aus diesem unveränderten Build wurden die Basisdaten für den Vergleich gesichert
(je Seite Titel, Description, Canonical, robots, H1, JSON-LD; Linkziele für `/` und Mannheim).
Vorher-Screenshots: `design-pilot1/screenshots/vorher-*.png` (Desktop 1440×900, mobil 390×844).

## Änderungen je Datei

- **`site/src/data/site.json`** — vier Marken in `design` (Werte unten). Farben und Schriften
  unverändert.
- **`site/src/layouts/Base.astro`** — neue CSS-Variablen (`--card-radius`, `--card-shadow`,
  `--space-section`); Kopfzeilen-Navigation als **zugängliches CSS-only Checkbox-Menü** (statt
  Wrap), mobil eingeklappt, ab 1024 px inline wie bisher, gleiche Ziele.
- **`site/src/styles/global.css`** — Pilot-1-Block am Dateiende: weiße Karten mit großem Radius und
  weichem Schatten; sichtbarer Fokusring (navy auf hell, Bernstein auf Navy); Suche als Pille mit
  Lupe und sichtbarer Beschriftung; zweispaltiger Hero; zweigeteilter Stadt-Ergebnisbereich mit
  Orientierungsspalte und Zeilenkarten; mobiles Menü; eine Schmalschirm-Korrektur am Premium-Band.
- **`site/src/pages/index.astro`** — Kopfbereich zweispaltig: links der unveränderte Navy-Inhalt
  (Augenbraue, H1, Vorspann, Suche, `heroPoints`), rechts eine helle Übersichtskarte mit echten
  Daten (erste drei Bundesländer aus dem Datenlayer mit Städte- und Eintragszahl, Link auf
  `/verzeichnis/` bzw. die Bundesland-Seiten).
- **`site/src/pages/verzeichnis/[bundesland]/[stadt]/index.astro`** — Ergebnisbereich zweigeteilt:
  links eine schmale, klebende Orientierungsspalte auf getönter Fläche (vorhandene Suche + Verweise
  auf Bundesland und Nachbarorte), rechts die Einträge. **Abschnittsfolge unverändert**; die
  Sprungliste bleibt an ihrem Dokumentplatz oben.
- **`site/src/components/SearchForm.astro`** — Lupe als Inline-SVG; optionale sichtbare
  Beschriftung über eine Eigenschaft (`label`), nur auf Startseite und Stadtseite gesetzt. **Ziel
  (`/suche/`), Feldnamen (`s`, `near`, `f`) und Verhalten exakt unverändert.**
- **`site/src/components/Card.astro`** — Kartenfußzeile mit Telefon-`tel:`-Link und ruhiger
  „Eintrag ansehen"-Pille (gleiches Ziel wie der Namenslink).
- **`04-plan.md`** — Gestaltungsmarken-Nachtrag (die vier Marken, „aus PNG abgeleitet, Pilot 1").
- **`wiki/framework/template-build-drift.md`** — Eintrag „Design-Pilot 1 — nicht freigegeben, nicht
  portiert" mit den betroffenen Dateien. **`wiki/log.md`** — Log-Zeile.

## Bewusst erhaltene Funktionen und Inhalte

- H1 je Seite genau einmal, `lang="de"`; Titel, Descriptions, Canonicals, robots, JSON-LD, Sitemap
  und `noindex`-Regeln **unverändert** (Vergleich unten).
- Die bestehende H1 „Damit die Rechnung keine Überraschung wird." samt Vorspann und `heroPoints`;
  kein generischer Ersatztext, der Markenname wird nicht zur Hauptüberschrift.
- Suche, Sortierung der Einträge, Premium-Band (Merz oben + genau eine freie Karte, Abzeichen,
  Logik aus `load.mjs` unangetastet), Garantie-Zeilen, Formular `/api/claim`, Einwilligungs-Klick
  für Google Maps, Fußbereich mit Impressum/Datenschutz, interne Links und ihre Ziele.
- Nur SVG-Zeichen (`check-glyphs` grün); keine farbigen Kartenränder (Trennung über Fläche,
  Schatten, Abstand).

## Neue/geänderte Marken (aus den PNG-Referenzen abgeleitet, Pilot 1)

| `site.json.design` | CSS-Variable | Wert |
|---|---|---|
| `cardRadius` | `--card-radius` | `22px` |
| `cardShadow` | `--card-shadow` | `0 18px 44px -26px rgba(11,37,69,0.30), 0 4px 12px -8px rgba(11,37,69,0.14)` |
| `spaceSection` | `--space-section` | `clamp(3.25rem, 6vw, 5.5rem)` |
| `buttonRadius` (geändert von `8px`) | `--button-radius` | `999px` (Pillenform) |

Farbmarken (Navy `#0B2545`, Bernstein `#F5A623`, Petrol `#126665`, Tönung `#E6F2F4`, Fläche
`#F5F6F8`) und Schriften (Roboto Slab / Roboto, selbst gehostet) **unverändert**. Keine neue
Schriftdatei.

## Prüfergebnisse

1. **Build:** `npm run build` ohne Datenwarnung, `check-glyphs` grün. 4647 Seiten, Sitemap **2823**.
2. **Vergleich gegen die Basisdaten (alle 4647 Seiten):** 0 Seiten dazu/weg; **0 Abweichungen** bei
   Titel, Description, Canonical, robots, H1 und JSON-LD; jede Seite genau eine H1. Interne Linkziele
   für `/` (64) und Mannheim (56): **nichts weggefallen, nichts neu** — einzige Differenz ist der
   Dateiname des gebündelten Stylesheets (`/_astro/index.*.css`), der sich zwangsläufig ändert, weil
   `global.css` geändert wurde; das ist kein navigierbares Linkziel.
3. **Funktion (lokaler Build, Chromium):** Suchformular Ziel/Feldnamen unverändert, `search-index.json`
   3799 Einträge unverändert; **keine externe Anfrage beim Laden** (ohne Klick) auf Start- und
   Stadtseite; Telefon-`tel:`-Link 44 px hoch; mit Tab erreicht man auf dem Desktop Markenname und
   **alle** Nav-Links mit sichtbarem Fokusring; das mobile Menü klappt per Tastatur/Klick auf und zu.
4. **Darstellung:** kein horizontaler Überlauf bei **320, 390, 768, 1024, 1440 px** auf Startseite,
   Mannheim, **Leipzig (ohne bezahlten Platz)** und **Neunkirchen (Saar) (nur zwei Einträge)**. Der
   lange Name „Merz Sicherheit …" und der Eintrag ohne Bewertung („AES …") sitzen sauber. Mobil:
   Kopf eine Zeile (84 px, kein Umbruch), Suche im ersten Bildschirm (390×844), Orientierung kompakt
   über den Einträgen.
5. **Textgate:** die neuen sichtbaren Textblöcke („…oder Ort suchen", „Standort wählen",
   „Verzeichnisübersicht", „Orientierung", „Anderen Ort suchen", „Alle Städte in …", „Eintrag
   ansehen", „Menü") bestehen `lint_copy.py` (Startseite ohne `--erlaube-rechtswoerter`) und enthalten
   keine gebannten Begriffe.

### Kontrastmessung (AA)

- Navy `#0B2545` auf Weiß `#FFFFFF`: 15,5:1 (AA/AAA).
- Bernstein-Schaltfläche: Text Navy `#0B2545` auf Bernstein `#F5A623`: 6,5:1 (AA). Bernstein trägt
  weiterhin nur dunkle Schrift.
- Gedämpfter Text `#4F6B74` auf Weiß: 4,9:1 (AA für Fließtext).
- Petrol-Link `#126665` auf Weiß: 5,2:1 (AA).
- **Fokusring (Nicht-Text, ≥ 3:1):** Navy auf Weiß/Tönung ≫ 3:1; Bernstein auf Navy 6,5:1 — beide
  bestehen.

### Grenzen (nicht geprüft)

Echte Geräte, Screenreader-Durchlauf und andere Browser als Chromium wurden **nicht** getestet;
geprüft wurde im lokalen Build mit Chromium. Keine Behauptung vollständiger Barrierefreiheit — die
Tastatur- und Kontrastprüfungen oben sind, was tatsächlich gemessen wurde. Die sichtbare, aber in der
Tab-Reihenfolge liegende verborgene Leistungs-Checkbox-Gruppe im Suchformular ist ein vorbestehendes
Verhalten und wurde nicht angefasst.

## So kannst du den Stand ansehen

**Screenshots (im Branch committet):** `output/schluesseldienste-deutschland/design-pilot1/screenshots/`
— `vorher-*.png` und `nachher-*.png`, je `home`/`mannheim` × `desktop`/`mobil`. Per SFTP direkt unter
`/home/dan/directory/blueprint-pilot1/output/schluesseldienste-deutschland/design-pilot1/screenshots/`,
oder nach `git fetch && git checkout design/pilot1` unter demselben Pfad im Hauptrepo.

**Lokale Vorschau (echte, bedienbare Seite, keine Live-Adresse):**

```
git fetch origin && git checkout design/pilot1
cd output/schluesseldienste-deutschland/site
npm install
npm run build
npm run preview        # astro preview, Standard http://localhost:4321/
```

Dann im Browser `http://localhost:4321/` und `http://localhost:4321/verzeichnis/baden-wuerttemberg/mannheim/`.
Alternativ `preview-site.command` (Mac) bzw. `preview-site.bat` (Windows) im Ordner `site/`.

## Abschluss

Zusammenführen nach `main` und Ausliefern geschehen erst nach deiner Freigabe in einem eigenen
Auftrag. Höchstens zwei gezielte Korrekturrunden sind noch offen.
