---
title: Das Master-Template
type: framework
status: verbindlich
updated: 2026-11-03
---

# Das Master-Template

`templates/astro/` **ist** das Verzeichnis. Sein Aufbau, sein Seitensatz, seine
Abschnittsfolge und seine Bedienmuster sind die Vorgabe und wiegen in jedem Build am
schwersten. Websites, die in Gate 1 genannt werden, sind **Optikvorlagen**: sie leihen eine
Farbpalette, eine Schriftpaarung, einen Karten- und Schaltflächenstil, eine Bildrichtung und
höchstens ein oder zwei Seitenmuster. Den Aufbau ersetzen sie nie. Widersprechen sich Vorlage
und Template im Aufbau, gewinnt das Template; im Aussehen gewinnt die Vorlage, im Rahmen der
Merkmale aus [[design-seed]] und der Kontrastprüfung.

## Wo es liegt

- **Das Template:** `templates/astro/`. Seine `src/data/site.json`, `src/styles/fonts.css`
  und `package.json` bringen die Optik des Referenzbaus als Vorgabe mit (Marineblau `#0B2545`,
  Bernstein `#F5A623` mit marineblauer Schrift, Roboto Slab 800 und Roboto, 8 px Radius).
- **Der Referenzbau:** `templates/master-reference/site/` ist ein vollständiger Build als
  HTML, 1.719 Seiten. Er ist das **englische Pilotprojekt** (ein Verzeichnis für Poolbauer in
  Florida, 1.557 Einträge, 145 Stadt- und Ortsseiten) und damit der Maßstab für **Aufbau und
  Optik**, nicht für Inhalt, Sprache oder Branche. Seine Seiten direkt lesen:
  `site/index.html` (Startseite), `site/directory/index.html` (Blättern),
  `site/directory/florida/index.html` (die Ebene, die hier Bundesland heißt),
  `site/directory/florida/naples/index.html` (eine Stadt),
  `site/directory/florida/vernon/index.html` (eine kleine Stadt),
  `site/company/florida/naples/classic-pools-of-naples-naples/index.html` (ein Eintrag),
  `site/featured/index.html`, `site/claim/index.html`, `site/about/index.html`, und
  `site/_astro/*.css` für das Stylesheet. Die Bildschirmfotos daneben (`home.png`,
  `city.png` und so weiter) zeigen dieselben Seiten bei 1280 px.
- **Was der Referenzbau nicht ist:** eine Inhaltsquelle. Seine Einträge, Beschreibungen,
  Stadttexte, Fragen, Ratgebertexte, sein Herausgeber, seine Kontaktdaten und seine Domain
  gehören jenem Verzeichnis und werden **nie** übernommen, zitiert oder weiterverwendet. Er
  ist englisch und aus einer anderen Branche; jede Tatsache in diesem Build kommt aus den
  eigenen Daten und den Quellen aus [[konventionen]]. Sein Text liegt außerdem vor zwei
  Regeln, und die Regeln gewinnen: seine Beschreibungen nennen mitunter ihre Quelle („its site
  says"), was [[enrichment]] verbietet, und seine fünf Ortsseiten tragen kein Textband und
  keine Fragen, was [[page-types]] verlangt. Eine Ortsseite wird deshalb nach der kleinen
  Stadtseite plus den Ortsregeln aus [[page-types]] gebaut, nie nach diesen fünf. Sein
  Beanspruchungsformular zeigt einen Platzhalter.

## Die Gewichtungsregel in einer Zeile

**Aufbau vom Template, Optik von der Vorlage, Tatsachen aus den Daten.** Ein Plan aus Gate 4
führt auf, was die Vorlage ändert (Marken, Schriften, Bilder, ein oder zwei Muster), und
nichts weiter; alles Nichtaufgeführte ist das Template wie geliefert.

## Aufbau der Site

Der Referenzbau hat zwei Ortsebenen, diese Fassung hat **drei**. Das ist der eine Punkt, an
dem das Template erweitert wird, und er steht in [[site-architecture]] und in
[[konventionen]].

| Ebene | Adresse | Aufgabe |
|---|---|---|
| Startseite | `/` | Die rankende Seite für „Schlüsseldienst": Kopfbereich mit Suche, Zahlenreihe, **Karten aller Bundesländer**, Karten der 20 größten Städte, Premium-Block, Raster der bestbewerteten Betriebe, Hinweis aufs Beanspruchen, Städteindex, Prüfblock, Ratgeberblock, Fragen |
| Blättern | `/verzeichnis/` | Suche, alle Bundesländer, alle Städte von A bis Z, alle Einträge nach Stadt. `noindex, follow` |
| **Bundesland** | `/verzeichnis/[bundesland]/` | **Neu.** Die Seite nach Städten: Einleitung, Premium-Block, jede Stadt mit ihren Zahlen, „Kleinere Orte", Fragen, Hinweis aufs Beanspruchen, Nachbarländer |
| Stadtseite | `/verzeichnis/[bundesland]/[stadt]/` | Die Geldseite: Kernzahlen, Ortstext um die Karten herum geteilt, Premium-Block, Karten, Überlaufliste, Fragen, Nachbarstädte, Hinweis aufs Beanspruchen |
| Eintrag | `/firma/[bundesland]/[stadt]/[slug]/` | Ein Betrieb: Kopf mit Bewertung und Garantie-Zeichen, zwei Spalten |
| Suche | `/suche/` | Ergebnisse im Browser aus `search-index.json`. `noindex` |
| Premium | `/premium/` | Stufenkarten, drei Schritte, Kontakthinweis, der Satz zur Nichtkäuflichkeit der Festpreis-Garantie |
| **Festpreis-Garantie** | `/festpreis-garantie/`, `/festpreis-garantie/antrag/`, `/auszeichnung/[slug]/` | **Neu.** Die drei Teile und die Voraussetzungen, Garantie-Antrag, Garantie-Nachweis ([[siegel-programm]]) |
| Beanspruchen, Über uns, Kontakt, **Impressum**, **Datenschutz**, AGB | Wurzel | wie das Template sie liefert; Impressum und Datenschutz neu und Pflicht |

**Brotkrumen über fünf Ebenen** auf jeder Orts- und Firmenseite: Startseite › Schlüsseldienste
› [Bundesland] › [Stadt] › [Betrieb], mit Winkeln, und die passende `BreadcrumbList`
([[schema]]). Der Referenzbau hat hier vier Ebenen; die fünfte ist die Bundesland-Ebene.

## Navigation

Wortmarke links (der Link zur Startseite, es gibt keinen Punkt „Startseite"), dann
„Schlüsseldienste" (auf `/verzeichnis/`), **„Festpreis-Garantie"** (auf `/festpreis-garantie/`), „Über uns",
„Kontakt" und eine bernsteinfarbene Schaltfläche „Eintrag beanspruchen". Marineblaue Leiste,
weiße Schrift. Die 16 Bundesländer und die größten Städte stehen im Fußbereich, nicht in der
Navigation.

Der Fußbereich hat vier Spalten plus Rechtszeile. Die Rechtszeile trägt **Impressum,
Datenschutz und AGB auf jeder Seite** ([[konventionen]]).

## Startseite, Abschnitt für Abschnitt

1. **Kopfbereich.** Marineblaues Band. H1 „Schlüsseldienste in Deutschland" mit „Deutschland"
   in der Aktionsfarbe. Eine Zeile: „Bewertungen, Leistungen und eine Telefonnummer für jeden
   Schlüsseldienst in Deutschland." Die Suchleiste: eine weiße Pille mit Was-Feld, Ort-Feld
   und bernsteinfarbener Schaltfläche „Suchen". Darunter eine Reihe mit drei kurzen Versprechen
   mit Häkchen (`heroPoints`, drei bis vier Wörter). Ein kleiner unterstrichener Textlink zum
   Ratgeber. Am Fuß vier Zahlen als ruhige Reihe mit Linienzeichen: Einträge, Städte,
   **geprüfte Betriebe**, Google-Bewertungen. Keine Schaltflächen im Kopfbereich, kein Foto,
   solange keines geliefert wird.
2. **„Schlüsseldienste in Ihrem Bundesland."** Getöntes Band, zentrierte Überschrift, **die 16
   Bundesländer als weiße Karten**: Name (H3), Zahl der Einträge, Zahl der Städte. Keine
   farbigen Kartenränder. Dieser Abschnitt ist neu und steht **vor** den Städten, weil die
   Bundesländer die Zwischenebene tragen.
3. **„Schlüsseldienste in Ihrer Stadt."** Die 20 größten Städte als Karten: Name (H3), Zahl
   der Einträge, Zahl der geprüften Betriebe. Darunter eine Schaltfläche
   „Alle N Städte ansehen", die auf Abschnitt 8 zeigt.
4. **Premium-Block.** Marineblau über die ganze Breite, goldene Überschrift, bis zu drei Karten
   mit goldenem Verlaufsband und marineblauem Reiter, dazu eine gestrichelte Karte
   „Dieser Platz ist frei", solange Plätze unverkauft sind. `featuredPreview` füllt unverkaufte
   Plätze zur Durchsicht mit den besten echten Einträgen der Seite und **muss zum Start aus
   sein**. Der Preislink steht unter den Karten. Derselbe Block erscheint auf der
   Bundesland-Seite und auf jeder Stadtseite.
5. **Bestbewertete Schlüsseldienste.** Sechs Karten, Bewertung mit der Zahl der Bewertungen
   gewichtet, Untergrenze 4,5 und 25 Bewertungen.
6. **Hinweis aufs Beanspruchen.** Das bernsteinfarbene Band: „Betreiben Sie einen
   Schlüsseldienst?" mit „Eintrag beanspruchen" und „Festpreis-Garantie beantragen". **Zwei Türen, nicht
   eine** ([[monetization-slots]]).
7. **„Schlüsseldienste nach Leistung."** Nur wenn der Build Leistungsseiten hat
   ([[page-types]]): jeder Leistungstitel mit seiner Zahl, verlinkt auf seine Seite.
8. **„Schlüsseldienste nach Stadt."** Jede Stadtseite als vierspaltige Liste von A bis Z,
   Name links, Zahl rechts, Buchstabenüberschriften als schlichter Text, **nach Bundesland
   gruppiert**.
9. **„So prüfen wir."** Getöntes Band, zentrierte Überschrift, vier nummerierte Schritte
   (`vettingSteps`), der Prüftext in schmalem Satz. Hier wird auf `/festpreis-garantie/` verlinkt, und
   hier wird der Herausgeber genannt („Ein Angebot der DOM Holding GmbH", verlinkt auf
   „Über uns").
10. **„So erkennen Sie einen seriösen Schlüsseldienst."** Der Ratgeber als Artikel:
    zentrierter Titel, Vorspann, nummerierte H3, **keine Verfasserzeile** (die steht nur auf
    Ratgeberseiten, [[on-page-rules]], [[publisher-entity]]).
11. **Häufige Fragen.** Frage-und-Antwort-Karten in drei Spalten mit Fragezeichen, jede
    Antwort sichtbar.

## Bundesland-Seite

Getönter Kopf mit Brotkrumen, H1 „Schlüsseldienst in [Bundesland]", die Kernzahlen als Pillen
(Einträge, Städte, geprüfte Betriebe), die Einleitung von 300 bis 500 Wörtern, der
Premium-Block, **jede Stadt des Landes mit ihren Zahlen** als Karten oder als Liste von A bis
Z (je nach Zahl), „Kleinere Orte" als schlichte Liste, Fragenkarten (3 bis 5), die
Nachbarländer als Karten, der Hinweis aufs Beanspruchen. Dieselbe Anatomie wie die
Bundesstaat-Seite des Referenzbaus, eine Ebene tiefer eingehängt.

## Stadtseite

Getönter Kopf mit Brotkrumen, H1 „Schlüsseldienst in [Stadt]" und die Kernzahlen als Pillen.
Erste Hälfte des Textes, dann der Premium-Block, dann „Die besten Schlüsseldienste in [Stadt]"
als Karten, dann der Überlauf über `maxCardsPerCity` als „N weitere Schlüsseldienste in
[Stadt]" in einer knappen Liste, dann die zweite Hälfte des Textes, Fragenkarten,
„Schlüsseldienste in der Nähe von [Stadt]" als Stadtkarten mit H3 (auch über die
Landesgrenze, [[site-architecture]]), der Hinweis aufs Beanspruchen. Der Text folgt der
Ortsregel aus [[page-types]].

## Eintragsseite

Kopf: Brotkrumen, Zeichen, H1, Bewertungszeile (Sterne, Wert mit Komma, Zahl), **das
Garantie-Zeichen** („Festpreis-Garantie 2026" mit den Dienstleistungspreisen, falls hinterlegt dem Materialblock, und Link auf
`/festpreis-garantie/`, oder „Noch keine Festpreis-Garantie" mit Link auf
`/festpreis-garantie/antrag/`; [[siegel-programm]], nicht abschaltbar), „Schlüsseldienst in [Stadt]".
Quellreihenfolge darunter: Über den Betrieb, Leistungen und Angaben (bestätigte Leistungen als
Felder mit Häkchen und je einem H3, ein ausdrückliches Nein als Feld mit Kreuz, die
Unbekannten zu einer gedämpften Zeile gefaltet, dann die Leistungsseiten als Chips), Kontakt
und Öffnungszeiten, dann „Weitere Schlüsseldienste in [Stadt]": vier Einträge derselben Stadt
mit Bewertung und ein Link auf die Stadtseite. Am Bildschirm steht der Kontaktkasten zuerst.
Seitenspalte: **Kartenplatzhalter** mit der Schaltfläche „Karte von Google Maps laden" und
dem Satz zur Datenübertragung – **die Karte lädt erst nach Klick, auf jedem Eintrag, auch bei
bezahlten Stufen** ([[konventionen]]), Standort mit „Route planen", Telefon, Website und
Maps-Link, die Beanspruchungskarte, der Hinweiskasten. Profilzeichen unter Kontakt, wenn die
Website sie verlinkt. Schema: der Betriebstyp `Locksmith` mit `makesOffer` für bestätigte
Leistungen und `sameAs` für Profile, **keine Bewertungsauszeichnung** ([[schema]]).

## Leistungsseite

Getönter Kopf mit Brotkrumen (Startseite, Leistungen, die Leistung), H1 „[Leistung] in
Deutschland" und die Kernzahlen als Pillen. Die Einleitung, die besten Einträge als Karten,
„[Leistung] nach Bundesland" als Länderliste mit Zahlen, die übrigen Leistungen, der Hinweis
aufs Beanspruchen. Nur für die Merkmale gebaut, die der Plan nennt ([[page-types]]).

## Karten

Eintragskarte: H3 Name, Bewertungszeile, Anschrift, bis zu drei Chips, **das Garantie-Zeichen** (bei Garantie die
Zeile „Festpreis-Garantie · Türöffnung ab [garantie_tag] €"),
Telefonnummer mit Hörerzeichen am Fuß der Karte. Bundeslandkarte: Name, Zahl der Einträge,
Zahl der Städte. Stadtkarte: Name, Zahl der Einträge, Zahl der geprüften Betriebe.
Premiumkarte: goldenes Band mit marineblauem Reiter, Stadt, Bewertung, Name, Auszug, Chips,
Link.

## Einstellungen, die die Optik tragen

Die `design.*`-Marken (bg, surface, text, heading, headerBg, band, tint, accent, action mit
7,6 zu 1 gegen marineblaue Schrift, gold, goldLight, goldDeep, radius, shadow),
`src/styles/fonts.css` für **selbst gehostete** Schriften (nie von Google geladen,
[[konventionen]]), `heroImage` wenn ein Bild geliefert wird. Alles andere ist Aufbau und
bleibt.

## Was eine Optikvorlage ändern darf

- Farben, im Rahmen der Kontrastregel, mit Messwerten in `04-plan.md` festgehalten.
- Schriftpaarung, frei lizenziert und selbst gehostet.
- Kartenradius und Schatten, Schaltflächenradius.
- Bilder im Kopfbereich, eigene oder lizenzierte.
- Höchstens ein oder zwei Seitenmuster, im Plan benannt, die keinen Abschnitt oben entfernen.

## Was eine Optikvorlage nicht ändern darf

Den Seitensatz und die Adressen, die Navigation, die Abschnittsfolge auf irgendeiner Seite,
die Suche, den Premium-Block und seinen Vorschaumodus, das Merkmalsraster, die Seitenspalte
der Eintragsseite, die Brotkrumen, die vier Fußspalten, die Rechtszeile mit Impressum und
Datenschutz, **das Garantie-Zeichen auf jedem Eintrag**, **den Kartenplatzhalter**, oder eine
Regel aus [[konventionen]], [[page-types]], [[on-page-rules]], [[schema]] und
[[launch-lean]].

## Siehe auch
[[konventionen]] · [[design-seed]] · [[page-sections]] · [[page-types]] · [[site-architecture]] · [[siegel-programm]]
