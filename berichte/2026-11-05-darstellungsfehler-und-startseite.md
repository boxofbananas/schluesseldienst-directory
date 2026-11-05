---
title: Darstellungsfehler (Kästchen), Startseite gekürzt, Öffnungszeiten repariert
type: bericht
status: fertig
updated: 2026-11-05
---

# Darstellungsfehler, Startseite, Öffnungszeiten

## Sicherheitsprüfung nach der vollen Platte (03:29)
`npm run build` läuft durch: **4.629 Seiten, keine Fehler.** `listings.csv` **3.800 Zeilen**,
`city-copy.json` valides JSON (**788 Keys**), die **fünf Ratgeberseiten** vollständig (jede endet mit
ihrem `## Quellen`-Block). **Nichts abgeschnitten**, nichts beschädigt.

## (1) Bewertungssterne: Schriftzeichen → Inline-SVG
Die Sterne ★/☆ (und das Häkchen ✓, Punkt 2) sind **Zeichen außerhalb des selbst gehosteten
Schrift-Auszugs**; der Browser fiel auf eine Systemschrift zurück und zeigte dort, wo sie fehlt, ein
leeres Kästchen. Ersetzt durch zwei kleine Inline-SVG-Komponenten:
- `components/Star.astro` (voll/leer), hängt über `currentColor` an der Farbe und über `1em` an der
  Schriftgröße, `aria-hidden`. Eingesetzt in `Rating.astro`, `DirectoryHub.astro`, `FeaturedBand.astro`,
  `verzeichnis/index.astro`, `verzeichnis/[bundesland]/[stadt]/index.astro`,
  `firma/.../[slug]/index.astro`.
- CSS: die `.rt i`-Regeln heißen jetzt `.rt .star`, die Farbe (`#b7791f`) bleibt.

## (2) Häkchen unter dem Suchfeld: CSS-content → Inline-SVG
Das Kästchen unter dem Suchfeld war `content: "\2713"` in `global.css` (`.hero-points li::before`).
Ersetzt durch `components/Check.astro` (Inline-SVG) im Markup der drei Vertrauenszeilen; die
`::before`-Regel ist raus, das Häkchen steht in der Handlungsfarbe.

## Alle weiteren Zeichen außerhalb des Auszugs + Build-Prüfung
Ein erster Scan fand **53.732** solcher Zeichen. Neben ★/☆/✓ steckten viele in den **Daten**
(Google-Maps-Beschreibungen, Namen, Adressen): Emoji (🔑🔥👍📞✅➤ …), Dingbats, arabische und
kyrillische Schriftfragmente, und – wichtig – **europäische Buchstaben, die der reine „latin"-Auszug
nicht enthält** (ẞ, Š/š, İ, ş …). Drei Klassen, drei Behandlungen:
1. **Europäische Buchstaben sollen erscheinen** → zusätzlich den Auszug **`latin-ext`** eingebunden
   (`fonts.css`, vier Gewichte). Damit rendern Namen wie „İşçi" oder „Straße/ẞ" korrekt.
2. **Emoji, Dingbats, fremde Schriften** → beim Laden aus dem Freitext entfernt
   (`load.mjs`, `sanitizeGlyphs`, angewandt auf `name`, `description`, `address`, `street`; danach
   doppelte Leerzeichen zusammengezogen).
3. **Build-Prüfung** `scripts/check-glyphs.mjs`, als **`postbuild`** in `package.json`: scannt alle
   gebauten `.html` und `.css` und **lässt `npm run build` scheitern**, falls ein Zeichen außerhalb
   von latin + latin-ext auftaucht (auch in CSS-content). Endstand: **bestanden, 0 Treffer**.

## (3) Startseite gekürzt
Die vollständige Liste aller Städte (city-pills, A–Z) ist von der Startseite **entfernt**. Es bleiben
die 16 Bundesländer und „Die größten Städte" (20); an ihre Stelle tritt der Verweis **„Alle Städte"
auf `/verzeichnis/`** (die A–Z-Liste steht dort unverändert). Die Startseite ist danach noch
**8.430 px hoch bei 1440 px Breite** (15.718 px bei 390 px, mobil gestapelt) – vorher lief sie allein
durch die 787er-Liste um rund 5.000 px länger.

## Kleinigkeiten
- **Suchfeld-Platzhalter** gekürzt auf „Firmenname oder Leistung" (vorher abgeschnitten).
- **U+FEFF in `load.mjs`**: steht **nicht am Dateianfang**, sondern in Zeile 93 **innerhalb einer
  Regex** `/^﻿/`, die ein BOM aus CSV-Kopfzeilen entfernt – also **gewollt**, nur als
  unsichtbares Zeichen geschrieben. Zur Sicherheit auf die explizite Escape-Form `﻿` umgestellt;
  kein weiteres literales U+FEFF in der Datei.

## Dabei gefunden und mitrepariert: „[object Object]" bei den Öffnungszeiten
Auf **jeder Eintragsseite** stand unter „Öffnungszeiten" siebenmal **„[object Object]"**. Ursache:
`working_hours` kommt von DataForSEO als **Array von Intervallen**
(`[{open:{hour,minute},close:{hour,minute}}]`), `normalizeHours` behandelte aber nur Strings und gab
`String(Array)` aus. `normalizeHours` versteht jetzt das Array: leeres Array → „Geschlossen", ein
00:00–24:00 → „Durchgehend geöffnet", sonst „HH:MM–HH:MM" (mehrere Intervalle mit Komma). Das
Schema-JSON-LD bleibt korrekt (die Zeiten werden daraus weiter erzeugt). Nicht in deiner Liste, aber
ein sichtbarer Fehler auf allen 3.800 Eintragsseiten – deshalb gleich behoben; sag Bescheid, wenn du
es anders willst.

## Screenshots (neu, berichte/screenshots/)
Startseite, Mannheim und ein **Eintrag mit Festpreis-Garantie**, je 1440 px und 390 px.
Hinweis: **derzeit hat kein Betrieb eine Festpreis-Garantie** (geprueft = 0). Für das Garantie-Foto
habe ich einen Mannheimer Eintrag (Key Walter) **nur für die Aufnahme** temporär mit Garantie
geflaggt, danach die Daten zurückgesetzt; der ausgelieferte Stand ist unverändert ohne Garantie.

## Prüfung
Build grün, Schriftprüfung bestanden, kein „[object Object]" mehr in `dist`, Startseite ohne 787er-
Liste, Verzeichnis mit vollständiger A–Z-Liste.
