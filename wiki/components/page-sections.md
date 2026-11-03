---
title: Abschnittsfolgen
type: component
status: current
updated: 2026-11-03
---

# Abschnittsfolgen

Die Folge ist das [[master-template]] und ändert sich nicht. Die Optik ändert sich
([[design-seed]]).

**Kopfzeile:** Wortmarke (der Link zur Startseite) · Schlüsseldienste (auf `/verzeichnis/`) ·
Siegel (auf `/siegel/`) · Über uns · Kontakt · Schaltfläche „Eintrag beanspruchen" (auf
`/eintrag-beanspruchen/`).

**Startseite:** Kopfbereich (H1 mit „Deutschland" in der Aktionsfarbe, eine Zeile, die
Suchpille, drei Versprechen, der Ratgeberlink, die ruhige Zahlenreihe mit Zeichen:
Einträge, Städte, geprüfte Betriebe, Google-Bewertungen) · **„Schlüsseldienste in Ihrem
Bundesland" als Karten der 16 Bundesländer** · „Schlüsseldienste in Ihrer Stadt" als Karten
der 20 größten Städte mit der Schaltfläche „Alle N Städte ansehen" · Premium-Block ·
Raster der bestbewerteten Betriebe · Hinweis aufs Beanspruchen **mit zwei Schaltflächen
(beanspruchen, Siegel beantragen)** · „Schlüsseldienste nach Leistung" wenn
Leistungsseiten existieren · „Schlüsseldienste nach Stadt" von A bis Z, nach Bundesland
gruppiert · Prüfblock mit vier Schritten und dem Link auf `/siegel/` · Ratgeberartikel ohne
Verfasserzeile · Fragenkarten.

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

**Eintragsseite:** Brotkrumen · Zeichen · H1 · Bewertungszeile · **Siegelzeichen („Geprüft
[Jahr]" oder „Noch nicht geprüft")** · „Schlüsseldienst in [Stadt]" · (Quellreihenfolge) Über
den Betrieb · Leistungen und Angaben (mit Links auf die Leistungsseiten) · Kontakt und
Öffnungszeiten · „Weitere Schlüsseldienste in [Stadt]" · Hinweiszeile; Seitenspalte:
**Kartenplatzhalter mit der Schaltfläche „Karte von Google Maps laden"** · Standort mit „Route
planen" · Beanspruchungskarte · Hinweiskasten.

**Premium-Seite:** Bandkopf · Stufenkarten (Premium-Eintrag, Stadt-Premium, Top-Platzierung) ·
drei Schritte · **der Satz „Das Siegel ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit."** ·
Kontakthinweis.

**Siegel-Seite (`/siegel/`):** Bandkopf · was das Siegel ist · **die sechs Prüfkriterien** ·
was es nicht ist (Selbstauskunft und Unterlagenprüfung, kein Test vor Ort, keine amtliche
Stelle, keine Lizenz) · Jahreszahl, Geltungsdauer, Erneuerung, Entzug · der Satz zur
Nichtkäuflichkeit · Schaltfläche auf `/siegel/antrag/`.

**Siegel-Antrag (`/siegel/antrag/`):** Bandkopf · kurzer Begleittext · Fragebogen zu den sechs
Kriterien · Serviceversprechen zum Unterschreiben · Absenden · Hinweis, dass ein Mensch prüft
und es nichts kostet.

**Siegel-Nachweis (`/auszeichnung/[slug]/`, `noindex`):** Betrieb, Jahr, erfüllte Kriterien ·
Link auf `/siegel/` und auf die Eintragsseite · das HTML-Schnipsel zum Kopieren.

**Leistungsseite:** Brotkrumen · H1 „[Leistung] in Deutschland" · Kernzahlen als Pillen ·
Einleitung · beste Einträge als Karten · die Leistung nach Bundesland · übrige Leistungen ·
Hinweis aufs Beanspruchen.

**Fußbereich:** Über uns mit der Herausgeberzeile · Schnelllinks (Beanspruchen, Premium,
**Siegel**, „Schlüsseldienste nach Leistung" wenn vorhanden) · **die 16 Bundesländer**, endend
mit „Alle N Städte" · Kontakt mit Profilzeichen · **Rechtszeile mit Impressum, Datenschutz und
AGB**.

**Karten:** Eintragskarte (H3 Name, Bewertungszeile, Anschrift, drei Chips, **Siegelzeichen**,
Telefonnummer mit Zeichen am Fuß) · **Bundeslandkarte (Name, Zahl der Einträge, Zahl der
Städte)** · Stadtkarte (Name, Zahl der Einträge, Zahl der geprüften Betriebe) · Premiumkarte
(goldenes Band, marineblauer Reiter, Stadt, Bewertung, Name, Auszug, Chips, Link) · Karte für
einen freien Platz (gleiche Anatomie, gestrichelt).

## Siehe auch
[[konventionen]] · [[master-template]] · [[page-types]] · [[design-seed]] · [[site-architecture]] · [[siegel-programm]]
