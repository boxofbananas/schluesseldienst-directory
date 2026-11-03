---
title: Optik: damit das Verzeichnis nicht wie von einer KI gebaut aussieht
type: framework
status: current
updated: 2026-11-03
---

# Optik: damit das Verzeichnis nicht wie von einer KI gebaut aussieht

Jede KI hat eine Handschrift. Hundert Verzeichnisse mit derselben Optik sind ein erkennbares
Muster und ein Vertrauensproblem. Deshalb liefert der Betreiber die Abweichung.

## Was Gate 1 fragt

Frage 2 in [[gate-1-intake]] bietet die Optik des Referenzbaus als Vorgabe an und nimmt eine
bis zwei Websites von einem Betreiber, der eine andere Optik lieber hätte, gleich welche
Branche. Das sind **Optikvorlagen**: sie leihen ein Aussehen, nie einen Aufbau
([[master-template]]). In `01-umfang.md` steht entweder „Optik des Templates" oder die
Adressen.

Gibt es Vorlagen, leitet Gate 4 daraus ab und schreibt in `04-plan.md`:

- eine Farbpalette (Hintergrund, Fläche, Schrift, ein Akzent, die Aktionsfarbe für
  Schaltflächen, die Bandfarbe für Kopfbereich und Fußbereich, der Akzent im Kopfbereich) als
  CSS-Variablen, ausgehend von den Marken des Templates, **jede Änderung festgehalten**
- die Schriftpaarung (eine Überschriftenschrift, eine Textschrift, Systemschriften erlaubt)
- den Kartenstil (flach oder mit Schatten, Radius), den Schaltflächenstil, die Abstandsskala
- das Muster für Kopf- und Fußbereich

Übernommen wird das Aussehen, **nie** Inhalt, Bilder oder Logo. Der Plan nennt die
abgeleiteten Marken; der Betreiber gibt sie frei, bevor Gate 5 baut.

**Lässt sich eine Vorlage nicht per Skript lesen** (Botschutz antwortet mit 403): Gate 4
bittet um zwei oder drei Bildschirmfotos im Chat (Startseite, eine Listenseite, eine
Detailseite) und leitet die Marken daraus ab, mit Kontrastmessung wie bei jeder anderen
Vorlage. Kommen keine, bleiben die Marken des Templates, `04-plan.md` hält fest, dass die
Vorlage nicht lesbar war, und es geht weiter.

## Vorgabe und Rückfall: die Optik des Templates

Ein Betreiber ohne Optikvorlage bekommt die Optik des Templates wie geliefert: die Marken in
`templates/astro/src/data/site.json`, die die Optik des Referenzbaus in
`templates/master-reference/site/` sind. „Vorgabe", „keine" und „habe ich nicht" bedeuten
alle dies, und Gate 4 vermerkt „Optik des Templates, keine Änderungen". **Nichts weiter wird
angeboten.** Der Referenzbau ist die erste und schwerste Referenz in jedem Build, und das
gilt auch, wenn eine Vorlage nicht lesbar ist oder die Bildschirmfotos nie kommen.

(Im englischen Pilotprojekt antwortete der erste Durchlauf auf „habe ich keine" mit einer
Tabelle von sieben anderen Verzeichnissen, und der Betreiber musste zweimal sagen, dass er
die Vorgabe will. Daraus wurde diese Regel.)

Die sieben Seiten in [[reference-directories]] werden nur gezeigt, wenn ausdrücklich nach
anderen Optiken oder Beispielen gefragt wird. Dann: eine Zeile je Seite, der Betreiber wählt
eine oder zwei, niemals für ihn wählen. **Sie sind alle englisch und aus anderen Branchen**;
ihre Branche ist nie ein Vorschlag, und ihre Texte sind nie eine Vorlage für deutsche Texte.

## Augenbrauen und Zeichen: erlaubt, wenn übernommen, verboten, wenn beliebig

Eine Augenbraue ist die kleine Zeile über einer Überschrift. Augenbrauen und Zeichen sind
gewollt, solange sie nicht wie von einer KI gemacht aussehen.

- **Nur von der Optikvorlage übernehmen.** Hat die Vorlage eine Augenbraue, hält Gate 4 ihre
  Behandlung in `design.eyebrows` fest (Schreibweise, Größe, Farbe, wo sie vorkommt), und
  Gate 5 setzt sie an genau diesen Stellen ein. Hat die Vorlage Zeichen, hält
  `design.icons` den Stil fest (gefüllt oder Linie, eine Farbe, Größe). Hat die Vorlage
  nichts davon, hat das Verzeichnis nichts davon (`none`).
- **Die KI-Fassung ist das Verräterische, nicht das Element.** Von einer KI: dieselbe
  beliebige Zeile über jeder Überschrift („Unsere Leistungen", „Warum wir", „Empfohlen"), eine
  dreispaltige Reihe beliebiger Linienzeichen mit einem Titel und einem Satz, der nichts sagt,
  Zeichen als Schmuck neben Überschriften. Von einem Menschen: eine Augenbraue dort, wo die
  Vorlage eine hat, die etwas über dieses Verzeichnis sagt; eine Aktionsreihe, in der jede
  Karte ein echtes Ziel auf der Site ist (nach Bundesland suchen, nach Stadt suchen, Festpreis-Garantie
  beantragen, Eintrag beanspruchen) mit einem Zeichen, das die Handlung benennt, in einem
  einheitlichen Stil.
- **Jede Augenbraue und jede Karte muss konkret sein.** Prüfung: Könnte die Zeile unverändert
  auf einem anderen Verzeichnis stehen? Dann streichen. Keine Augenbraue über den H2 der
  Eintragsblöcke, der Fragen oder des Handlungsbandes, es sei denn die Vorlage macht genau
  das.
- **Keine Kundenstimmen.** Ein Verzeichnis hat zum Start keine Kunden zu zitieren, und
  erfundene Zitate sind ein Vertrauens- und ein Rechtsproblem. In diesem Gewerbe zusätzlich:
  eine erfundene Stimme über einen genannten Betrieb ist eine Behauptung über einen echten
  Dritten.
- Im Grundgerüst: das Template bringt keine Augenbraue und keine Aktionsreihe mit. Hat eine
  Vorlage eine, schreibt Gate 4 `design.eyebrows` oder `design.icons` mit der Behandlung,
  entwirft die Zeile oder die Karten in `04-plan.md` zur Freigabe, und Gate 5 fügt sie als
  übernommenes Seitenmuster hinzu, **ohne einen Abschnitt zu entfernen**
  ([[master-template]]).

## Die Grundoptik ist das Template

Was das Grundgerüst zeigt, bevor Gate 4 etwas anfasst: marineblauer Kopfbereich,
Suchpille, drei Versprechen, die ruhige Zahlenreihe, bernsteinfarbene Schaltflächen mit
marineblauer Schrift (7,6 zu 1), Roboto Slab 800 für Überschriften und Roboto für den Text,
8-px-Karten. Es ist eine fertige Optik, kein Entwurf: wer keine Seite nennt, liefert sie
unverändert aus. Wer eine nennt, bekommt Farben und Schriften daraus abgeleitet, im Rahmen der
Kontrastregel, und `04-plan.md` hält fest, was sich gegenüber den Marken des Templates
geändert hat. Der Aufbau ändert sich in keinem Fall ([[master-template]]).

## Die Merkmale, die wegzugestalten sind

- **Keine farbigen Kartenränder.** Karten durch Flächenfarbe, Schatten oder Abstand trennen.
- **Kontrast:** jede Schaltfläche und jeder Link erfüllt WCAG AA gegen seinen Hintergrund.
  Besonders das Handlungsband prüfen.
- **Ein echtes Logo** (geliefert, oder eine Wortmarke in der Überschriftenschrift) und echte
  Bilder, wo Bilder benutzt werden. Keine Platzhalterverläufe.
- Die Aufgabe der Startseite bleiben Bundesländer, Städte, Premium-Plätze und der Ratgeber;
  eine Aktionsreihe sitzt unter dem Kopfbereich und zeigt dorthin, sie ersetzt nichts.
- **Karten zeigen Daten** (Bewertung, Zahl der Bewertungen, Merkmale, Telefonnummer,
  Garantie-Zeichen). Eine Karte mit nichts als einem Namen und einer Schaltfläche liest sich wie
  erzeugt.
- **Zwei Optiken bringen KI-Werkzeuge von selbst hervor**, und eine Vorlage kann eine davon
  tragen: creme-farbenes Papier mit Serifenüberschriften und Terrakotta-Akzent, und Inter mit
  Tailwind-Blau. Nennt der Betreiber eine Seite mit einer dieser Optiken, liest sich das
  Verzeichnis trotzdem wie KI-gebaut. In Gate 4 sagen und eine andere Richtung anbieten. Die
  Marken des Templates (Marineblau und Bernstein) sind keine von beiden.
- **Kontrast der Vorlage messen, bevor ihre Farben übernommen werden.** Im englischen
  Pilotprojekt erfüllten sechs von acht genannten Seiten WCAG AA irgendwo nicht, meist weiße
  Schrift auf einem hellen Akzent. Den Farbton übernehmen, die Paarung richten, die Änderung
  in `04-plan.md` festhalten.
- **Mehr als zwei Vorlagen sind keine Vorlage.** Nennt der Betreiber mehr, alle lesen, die
  zwei oder drei auswählen, die ein ganzes Verzeichnis tragen können, sie als Richtungen
  vorstellen und aus den übrigen höchstens Seitenmuster nehmen.
- **Gekaufte Schriften lassen sich nicht übernehmen.** Prüfen, dass die Paarung frei
  lizenziert ist, und **selbst hosten** (`src/styles/fonts.css`). Keine Schrift von Google
  laden, auch nicht die freien: das ist in dieser Fassung eine Rechtsfrage, keine
  Geschmacksfrage ([[konventionen]]).

## Was deutsche Texte an der Optik ändern

- **Deutsche Wörter sind länger.** „Eintrag beanspruchen" statt „Claim", „Schlüsseldienste in
  Baden-Württemberg" statt „Pool Builders in Florida". Schaltflächen, Chips, Kartenüberschriften
  und die Navigation müssen den längeren Text tragen, ohne zu brechen. Gate 5 prüft die
  Kopfzeile, die Stufenkarten und die Eintragskarten bei 360 px Breite.
- **Die Bundeslandnamen sind lang.** „Mecklenburg-Vorpommern" und „Nordrhein-Westfalen"
  bestimmen die Breite der Bundeslandkarten. Nie abkürzen; die Kürzel aus [[konventionen]]
  sind für Datenfelder, nicht für sichtbare Überschriften.
- **Komma als Dezimaltrennzeichen** in jeder Bewertung („4,8"), Preise mit Euro-Zeichen
  dahinter („97 €") ([[konventionen]]).
- **Das Garantie-Zeichen braucht Platz** auf jeder Eintragskarte und in jedem Eintragskopf,
  in beiden Zuständen („Festpreis-Garantie 2026" mit der Zeile „Türöffnung ab [garantie_tag] €"
  und „Noch keine Festpreis-Garantie"). Es wird nicht gekürzt, nicht zu einem Zeichen
  zusammengezogen und nicht ausgeblendet, wenn es eng wird
  ([[siegel-programm]]).

## Was jedes Verzeichnis ohnehin teilt

Das [[master-template]] ist der Aufbau: Seitensatz, Adressen, Navigation, jeder Abschnitt in
seiner Folge, die Suche, der Premium-Block, der Eintragsaufbau. Er wiegt in jedem Build am
schwersten. Eine genannte Seite ist eine Optikvorlage für das Aussehen und höchstens ein oder
zwei Seitenmuster; den Aufbau ändert sie nie.

## Siehe auch
[[konventionen]] · [[master-template]] · [[page-sections]] · [[page-types]] · [[footprint-rules]] · [[reference-directories]]
