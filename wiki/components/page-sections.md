---
title: Abschnittsfolgen
type: component
status: current
updated: 2026-11-05
---

# Abschnittsfolgen

Die Folge ist das [[master-template]] und ändert sich nicht. Die Optik ändert sich
([[design-seed]]).

**Kopfzeile:** Wortmarke (der Link zur Startseite) · Schlüsseldienste (auf `/verzeichnis/`) ·
Festpreis-Garantie (auf `/festpreis-garantie/`) · Über uns · Kontakt · Schaltfläche „Eintrag beanspruchen" (auf
`/eintrag-beanspruchen/`).

**Startseite:** Kopfbereich (Augenbraue „Schlüsseldienste in Deutschland"; H1 „Damit die
Rechnung keine Überraschung wird." mit allein „keine Überraschung" in der Aktionsfarbe; die
Unterzeile; die Suchpille, drei Versprechen, der Ratgeberlink, die ruhige Zahlenreihe mit
Zeichen: Einträge, Städte, geprüfte Betriebe, Google-Bewertungen) · **„Schlüsseldienste in Ihrem
Bundesland" als Karten der 16 Bundesländer** · „Schlüsseldienste in Ihrer Stadt" als Karten
der 20 größten Städte mit der Schaltfläche „Alle N Städte ansehen" · Premium-Block ·
Raster der bestbewerteten Betriebe · Hinweis aufs Beanspruchen **mit zwei Schaltflächen
(beanspruchen, Festpreis-Garantie beantragen)** · „Schlüsseldienste nach Leistung" wenn
Leistungsseiten existieren · „Schlüsseldienste nach Stadt" von A bis Z, nach Bundesland
gruppiert · Prüfblock mit vier Schritten und dem Link auf `/festpreis-garantie/` · Ratgeberartikel ohne
Verfasserzeile · Fragenkarten.

**Warum die Startseiten-Überschrift eine Haltung trägt, keinen Notfall-Aufhänger
(entschieden 2026-11-05).** Die Startseite ist nicht der Einstieg für den Notfall: Wer
ausgesperrt ist, sucht „Schlüsseldienst <Stadt>" und landet auf der Stadtseite, nicht hier.
Die Startseite sehen vor allem Besucher über die Marke und die Betriebe, denen Premium-Plätze
und die Festpreis-Garantie verkauft werden. Für dieses Publikum wirkt eine Haltung besser als
ein Notfall-Aufhänger, und „Damit die Rechnung keine Überraschung wird." schließt Vermieter,
Hausverwaltungen und Schließanlagen-Kunden nicht aus. Die Augenbraue „Schlüsseldienste in
Deutschland" trägt die Branche in den ersten Absatz (Textgate) und ist als einzige konkrete
Augenbraue in `design.eyebrows` festgehalten ([[design-seed]]).

**Blättern (`/verzeichnis/`):** Kopfbereich mit Suche · Bundesländer · Städte von A bis Z ·
alle Einträge nach Stadt.

**Bundesland-Seite:** Brotkrumen · H1 „Schlüsseldienst in [Bundesland]" · Kernzahlen als
Pillen · Einleitung · Premium-Block · jede Stadt des Landes mit ihren Zahlen · „Kleinere
Orte" (von `foldMaxKm` freigestellte Ortsseiten, indexiert wie jede Stadtseite, außerhalb der
Navigation) · Fragenkarten (3 bis 5) · Nachbarländer als Karten · Hinweis aufs Beanspruchen.

**Stadtseite:** Brotkrumen · H1 „Schlüsseldienst in [Stadt]" · Kernzahlen als Pillen · erste
Hälfte des Textes · Premium-Block · „Die besten Schlüsseldienste in [Stadt]" als Karten ·
Überlaufliste · zweite Hälfte des Textes · Fragenkarten · „Schlüsseldienste in der Nähe von
[Stadt]" als Karten · Hinweis aufs Beanspruchen.

**Eintragsseite:** Brotkrumen · Zeichen · H1 · Bewertungszeile · **Garantie-Zeichen („Festpreis-Garantie
[Jahr]" mit den drei Dienstleistungspreisen Türöffnung tagsüber, nachts, Anfahrt, dem Materialblock bei abgeschlossener Tür und dem Weg zur Meldung einer
Rechnung, oder „Noch keine Festpreis-Garantie")** · „Schlüsseldienst in [Stadt]" · (Quellreihenfolge) Über
den Betrieb · Leistungen und Angaben (mit Links auf die Leistungsseiten) · Kontakt und
Öffnungszeiten · „Weitere Schlüsseldienste in [Stadt]" · Hinweiszeile; Seitenspalte:
**Kartenplatzhalter mit der Schaltfläche „Karte von Google Maps laden"** · Standort mit „Route
planen" · Beanspruchungskarte · Hinweiskasten.

**Premium-Seite:** Bandkopf · Stufenkarten (Premium-Eintrag, Stadt-Premium, Top-Platzierung) ·
drei Schritte · **der Satz „Die Garantie ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit."** ·
Kontakthinweis.

**Garantie-Seite (`/festpreis-garantie/`):** Bandkopf · was die Festpreis-Garantie ist, **die
drei Teile** (Preis vor dem Anruf, der Preis ist der Rechnungspreis, Verstoß hat Folgen) · **die
sechs Voraussetzungen** · was sie nicht ist (Selbstauskunft und Unterlagenprüfung, kein Test vor
Ort, die Garantie gibt der Betrieb, keine amtliche Stelle, keine Lizenz) · Jahreszahl,
Geltungsdauer, Erneuerung, Entzug · der Weg zur Meldung einer Rechnung · der Satz zur
Nichtkäuflichkeit · Schaltfläche auf `/festpreis-garantie/antrag/`.

**Garantie-Antrag (`/festpreis-garantie/antrag/`):** Bandkopf · kurzer Begleittext · Fragebogen
zu den sechs Voraussetzungen mit den Preisen (Dienstleistung und Material) als Pflichtfeldern · Serviceversprechen zum
Unterschreiben · Absenden · Hinweis, dass ein Mensch prüft
und es nichts kostet.

**Garantie-Nachweis (`/auszeichnung/[slug]/`, `noindex`):** Betrieb, Jahr, die Preise,
erfüllte Voraussetzungen · Link auf `/festpreis-garantie/` und auf die Eintragsseite · das
HTML-Schnipsel zum Kopieren.

**Leistungsseite:** Brotkrumen · H1 „[Leistung] in Deutschland" · Kernzahlen als Pillen ·
Einleitung · beste Einträge als Karten · die Leistung nach Bundesland · übrige Leistungen ·
Hinweis aufs Beanspruchen.

**Fußbereich:** Über uns mit der Herausgeberzeile · Schnelllinks (Beanspruchen, Premium,
**Festpreis-Garantie**, „Schlüsseldienste nach Leistung" wenn vorhanden) · **die 16 Bundesländer**, endend
mit „Alle N Städte" · Kontakt mit Profilzeichen · **Rechtszeile mit Impressum, Datenschutz und
AGB**.

**Karten:** Eintragskarte (H3 Name, Bewertungszeile, Anschrift, drei Chips, **Garantie-Zeichen** (bei Garantie die Zeile „Festpreis-Garantie · Türöffnung ab [garantie_tag] €"),
Telefonnummer mit Zeichen am Fuß) · **Bundeslandkarte (Name, Zahl der Einträge, Zahl der
Städte)** · Stadtkarte (Name, Zahl der Einträge, Zahl der geprüften Betriebe) · Premiumkarte
(goldenes Band, marineblauer Reiter, Stadt, Bewertung, Name, Auszug, Chips, Link) · Karte für
einen freien Platz (gleiche Anatomie, gestrichelt).

## Siehe auch
[[konventionen]] · [[master-template]] · [[page-types]] · [[design-seed]] · [[site-architecture]] · [[siegel-programm]]
