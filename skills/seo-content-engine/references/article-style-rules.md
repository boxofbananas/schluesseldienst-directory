# Stilregeln für Artikel (deutsche Fassung)

Wie jeder Artikel geschrieben wird: Stimme, Entkitschung, Umgang mit dem Suchbegriff,
Satzbau, Form. Das ist die Untergrenze und gilt auch bei einer eigenen Markenstimme
(eine Stimme ändert Rhythmus und Tonlage, nie diese Regeln). Was **zu bauen** ist,
steht in `references/article-format-guidelines.md`; **wie ein Abschnitt zu schreiben**
ist, in `references/article-template-guidelines.md`. Diese Datei sind die
Schreibregeln.

Alle Texte sind **deutsch, Sie-Anrede**. Englische Textmuster der Skill („TL;DR",
„verdict", „key takeaways") werden nicht übersetzt übernommen, sondern durch deutsche
Formen ersetzt: ein Vorspann, ein Fazit, die Kernpunkte.

## Harte Verbotsliste (vom Linter erzwungen)

Sie steht in `references/forbidden_words.txt`; `scripts/lint_article.py` liest die
Datei und lässt das Gate in Stufe 6 scheitern, sobald eines der Wörter vorkommt.
`scripts/lint_copy.py` liest sie zusätzlich für jeden kurzen Block. Drei Gruppen:

1. **Rechtswörter.** „lizenziert", „zugelassen", „zertifiziert", „Meisterbetrieb",
   „Konzession". Schlüsseldienst ist in Deutschland kein zulassungspflichtiges
   Handwerk; es gibt keine Lizenz und keine Meisterpflicht (`wiki/konventionen.md`).
2. **Wörter, die eine amtliche Stelle vortäuschen.** „Innung", „Verband", „Kammer",
   „amtlich", „Verbraucherschutz", „getestet", „TÜV", „Testsieger".
   Grund: Verwechslungsgefahr. Das Verzeichnis ist ein privates Angebot; seine
   Festpreis-Garantie ist ein Versprechen des Betriebs, das es veröffentlicht
   (`wiki/framework/siegel-programm.md`). Dazu „Garantie" und „garantiert" außer im
   Programmnamen „Festpreis-Garantie"; auf Ratgeberseiten zur Rechtslage mit Schalter
   zugelassen (`wiki/seo/copy-gate.md`, Abschnitt 1b).
3. **Werbefloskeln und KI-Verräter.** „unschlagbar", „erstklassig", „maßgeschneidert",
   „im Herzen von", „Ihr zuverlässiger Partner", „rund um die Uhr für Sie da",
   „schnell und günstig", „Nummer 1 in".

Im Zweifel gilt die Datei, nicht diese Zusammenfassung.

Alles unterhalb der nächsten Überschrift ist die größere **Vermeiden-und-umschreiben**-
Liste. Der Linter lässt sie nicht scheitern: beim Entwerfen vermeiden und zum
einfacheren Wort greifen. Es ist eine Richtschnur, weil manche dieser Wörter
gelegentlich das richtige sind.

---

## Entkitschen: wie ein Mensch klingen

KI-Prosa verrät sich an wenigen Gewohnheiten: aufgeputzte Wörter, gepolsterte
Übergänge, Absicherungen, Modewörter und ein paar Satzbau-Ticks. Wer sie streicht,
liest sich menschlich. Die Prüfung: Könnte ein Leser glauben, das hat ein Chatbot aus
einem Einzeiler erzeugt? Dann ist es nicht fertig.

Unten steht je Gruppe, was zu vermeiden ist und wozu zu greifen. Die Ersatzwörter sind
eine Auswahl, keine Suchen-und-Ersetzen-Liste: tausche kein überbenutztes Wort gegen
ein anderes, das dann zehnmal vorkommt. Ist ein beanstandetes Wort an einer Stelle
wirklich das genaueste, bleibt es; das ist selten, und meist liest sich der Satz
umgebaut besser.

### Aufgeputzte Verben und Substantive
- eruieren → herausfinden, klären
- fokussieren auf → sich kümmern um, achten auf
- implementieren → einbauen, einrichten
- generieren → erzeugen, bringen
- optimieren → verbessern, besser machen
- realisieren → umsetzen, machen
- gewährleisten → dafür sorgen, sicherstellen
- bereitstellen → geben, anbieten
- zielführend → sinnvoll, hilfreich
- Mehrwert → Nutzen, was es bringt
- Thematik → Thema
- Problematik → Problem
- Bereich → Feld, Gebiet, oder streichen
- Lösung (als Produktwort) → sagen, was es ist

### Gepolsterte Übergänge
- darüber hinaus → außerdem, dazu
- des Weiteren → außerdem
- in diesem Zusammenhang → dabei, oder streichen
- im Rahmen von → bei, in
- zum einen zum anderen → einmal, dann
- grundsätzlich → im Grunde, oder streichen
- letztendlich → am Ende, oder streichen
- im Hinblick auf → für, zu

### Absicherungen, die den Punkt schwächen
- in der Regel → meistens
- tendenziell → oft
- gewissermaßen → streichen, oder die Aussage klar treffen
- unter Umständen → manchmal, oder die Bedingung nennen
- durchaus → streichen
Besser noch: die Absicherung streichen und etwas Bestimmtes sagen. Eine Zahl oder eine
genannte Quelle schlägt jedes weiche Wort.

### Modewörter (meist streichen, nicht ersetzen)
- innovativ → zeigen, was neu ist, statt es zu behaupten
- revolutionär → die Veränderung benennen
- zukunftsweisend → streichen
- ganzheitlich → vollständig, oder sagen, was dazugehört
- nachhaltig (wenn nicht Umwelt gemeint ist) → dauerhaft, oder streichen
- synergetisch → streichen
- eine Vielzahl von → viele
- auf das nächste Level → den konkreten Gewinn benennen

### Behördendeutsch
- vorgenannt → der oben genannte, dieser
- diesbezüglich → dazu
- seitens → von
- nach Maßgabe von → nach
- Inanspruchnahme → Nutzung
- zur Verfügung stellen → geben, anbieten
- erfolgt → geschieht, passiert, oder das Verb zurückholen
  („die Öffnung erfolgt" → „der Betrieb öffnet")

### Produkt- und Handwerkswörter, die oft vorkommen
- „umfangreiches Leistungsspektrum" → sagen, welche Leistungen
- „kompetente Beratung" → sagen, worüber beraten wird
- „individuelle Lösungen" → sagen, was gemacht wird
- „höchste Qualität" → streichen; Qualität behauptet man nicht
- „reibungslos" → ohne Schaden, ohne Nacharbeit

---

## Den Text so bauen, dass man ihn herausnehmen kann

- **Antwort zuerst.** Die eigentliche Antwort steht in den ersten Zeilen, nicht nach
  einem Anlauf: die Empfehlung, das Ergebnis, die Begriffsklärung. Suchmaschinen und
  Antwortwerkzeuge nehmen die erste klare Aussage, und wer überfliegt, will sie oben.
  Erst der Schluss, dann die Begründung darunter.
- **Abschnitte stehen für sich.** Jeder Abschnitt muss alleine verständlich sein. Kein
  „wie oben beschrieben", kein „wie wir gesehen haben". Wer einen Abschnitt
  herausnimmt, soll einen vollständigen Gedanken haben.

## Satzbau-Ticks, die wegzulassen sind

- **Gedankenstriche.** Ein schweres Verräterzeichen. Stattdessen Komma, Doppelpunkt,
  Punkt oder Klammer. Einer oder zwei im ganzen Artikel sind erträglich, wenn ein Satz
  ihn wirklich braucht; mehr liest sich maschinell. (Bindestriche in Zahlbereichen wie
  „10–15 €" sind in Ordnung.)
- **Satzanfänge mit Bindewörtern.** Kein Satz beginnt mit „Darüber hinaus",
  „Zudem", „Des Weiteren", „Außerdem" als Einstieg. Frisch anfangen, oder mit etwas
  Konkretem überbrücken („Der Grund dafür ist …").
- **Dreierreihen als Polster.** Nicht reflexhaft dreifach („schneller, günstiger,
  einfacher"). Das eine nennen, auf das es ankommt.
- **Wiederholte Satzmuster.** Haben mehrere Sätze hintereinander dasselbe Gerüst, das
  Muster brechen: Anfänge und Längen wechseln.
- **Rhetorische Fragen.** Höchstens eine je Artikel, und nur wenn sie etwas trägt.
- **Den Artikel erzählen.** Nicht ankündigen, was ein Abschnitt tun wird, und nicht
  zusammenfassen, was vorher kam. Einfach das Nächste schreiben.
- **Substantivketten.** „Die Durchführung der Türöffnung" → „die Tür öffnen".
  Deutsche KI-Prosa verrät sich daran stärker als englische.

---

## Stimme

- Den Leser mit **„Sie"** anreden, durchgehend, nie „man" als Ersatz dafür und nie
  „Nutzer" oder „Kunden" als Anrede.
- Keine Verkürzungen wie im Englischen; deutsche Umgangsformen wie „gibt's" bleiben
  draußen. Sachlich, aber nicht steif.
- „Ich" ist in Ordnung, wenn der Text einen klaren Standpunkt hat und eine
  Verfasserzeile trägt. „Wir" nur, wo wirklich der Herausgeber spricht.
- Aktiv schreiben. Passiv nur, wenn es ehrlich besser liest. Deutsche Texte rutschen
  leicht ins Passiv; das ist der häufigste Grund, warum ein Absatz tot klingt.

---

## Lesbarkeit

Für das in Stufe 1 festgelegte Publikum schreiben. Bei diesem Verzeichnis ist das
jemand, der nachts vor der eigenen Tür steht und das Telefon in der Hand hat:

- Kurze Sätze. Jeden Satz über etwa 20 Wörter teilen (deutsche Wörter sind länger als
  englische, die englische Grenze von 25 trägt hier nicht).
- Einfache, konkrete Wörter vor abstrakten.
- Ein Gedanke je Satz.
- Zusammengesetzte Wörter aufbrechen, wenn sie über drei Glieder gehen:
  „Schließanlagenaustauschkosten" → „was der Austausch einer Schließanlage kostet".

`lint_article.py` meldet einen Lesbarkeitswert, damit ein zu dicht geratener Abschnitt
auffällt, lässt den Lauf aber nicht daran scheitern. **Die englischen Stufenwerte sind
auf deutsche Sätze nicht übertragbar**; der Wert ist ein Hinweis, kein Maß.

---

## Absätze und Aufbau

- Absätze kurz halten, ein paar Sätze, selten mehr als fünf. Längen wechseln, damit die
  Seite Rhythmus hat.
- Etwa alle 250 bis 300 Wörter eine Überschrift, damit keine Textwand entsteht.
- Aufzählungen ab drei gleichartigen Punkten.
- Tabellen sind erlaubt, wo sie einen Vergleich wirklich tragen. Keine Prosa in eine
  Tabelle zwingen.
- **Die Beschriftung fett setzen** bei jedem beschrifteten Punkt: Schrittnamen, Pro und
  Contra, „Nehmen Sie X, wenn …", Hinweise auf Fehler. Eine Beschriftung ohne Fettung
  liest sich wie unbearbeitete Chatbot-Ausgabe.

---

## Überschriften

- Ein H1 (der Titel). H2 für Hauptabschnitte, H3 für Unterpunkte.
- Höchstens zwei Ebenen (H2 → H3). Kein H4.
- Jedes inhaltliche H2 trägt mindestens einen konkreten Begriff aus der Liste aus
  Stufe 1, damit kein Abschnitt Füllmasse ist.

---

## Umgang mit dem Suchbegriff

**Platzierung (Pflicht):**
- **Titel:** der genaue Suchbegriff, vorne, wo er natürlich liest.
- **Erste etwa 100 Wörter** des Vorspanns.
- **Mindestens zwei H2:** in einem der genaue Begriff, in einem anderen eine nahe
  Abwandlung, wo es natürlich liest. Geht das nur gezwungen, ist eines die
  Untergrenze.
- **Letzter Abschnitt** (das Fazit), einmal.

`lint_article.py --keyword "<Suchbegriff>"` prüft Vorspann, ein H2 und den Schluss.

**Gebrauch (Platzierung vor Menge):**
- Den **genauen Wortlaut** an diesen Stellen benutzen. Genau darauf soll die Seite
  ranken, also nicht mit einem Synonym verwässern, wo der echte Begriff hingehört.
- Die Dichte leicht und ungezwungen halten (etwa 0,5 bis 2 % des Textes). Den Begriff
  oder nahe Abwandlungen zu häufen ist Überfüllung.
- **Deutsche Besonderheit:** Der Begriff kommt in Beugung und Zusammensetzung vor
  („Schlüsseldienst", „Schlüsseldienste", „Schlüsseldienst Mannheim"). Das sind
  natürliche Formen und keine Abwandlungen, die den genauen Begriff ersetzen. Die
  Umlautschreibung im sichtbaren Text ist immer die richtige („Schlüsseldienst", nie
  „Schluesseldienst"); die umgeschriebene Form gehört nur in Adressen
  (`wiki/konventionen.md`).
- **Die Themenabdeckung wiegt schwerer als die Begriffszahl.** Die Unterthemen
  abdecken, die die oberen Treffer abdecken; den genauen Begriff dort setzen, wo er
  hingehört; nicht jedes Ziel um seiner selbst willen hineinpressen.

---

## Konkret statt allgemein

Das gilt für **Behauptungen**, also Aussagen, zu denen ein Leser nach einem Belegen
fragen könnte, nicht für jeden Satz. Wird eine allgemeine Behauptung aufgestellt
(„viele Betriebe arbeiten so"), dann mit einer Zahl, einem Namen, einem Datum oder
einem konkreten Beispiel unterlegen, oder streichen.

**In dieser Fassung zusätzlich verbindlich:** Eine Aussage über Recht, Gewerbe, Preise
oder örtliche Besonderheiten braucht eine Quelle aus der Liste in
`wiki/konventionen.md`: Handwerkskammer des Bezirks, Stadt- und Gemeindeportale
(Gewerbeamt), Verbraucherzentrale des Bundeslandes, polizei-beratung.de, Stiftung
Warentest. **Nicht als Quelle:** andere Schlüsseldienst-Websites, Branchenbücher,
Presseportale. Ein Punkt, für den nur eine kommerzielle Quelle gefunden wird, gilt als
**unbelegt** und darf nicht im Text auftauchen. Jeder Punkt hält Adresse und
Abrufdatum fest.

**Preise:** kein Preis und keine Preisspanne in Euro, außer eine amtliche Quelle belegt
sie und der Text nennt sie als deren Angabe. Überhöhte Rechnungen sind in diesem
Gewerbe das Hauptthema der Verbraucherzentralen; eine selbst geschätzte Zahl ist hier
nicht nur ungenau, sondern schädlich.

---

## Saubere Ausgabe

- Nie Platzhalter: kein `[Bild hier einfügen]`, kein `[TODO]`, kein `[Link]`, keine
  Marker in Klammern. Alles, was ausgegeben wird, ist veröffentlichungsreif.
- Keine Bildplatzhalter und keine Notizen wie „hier ein Bildschirmfoto einfügen".
- Echter, beschreibender Linktext, nie „hier klicken".
- Links selbst sind willkommen: interne Links aus Stufe 2 und belegte Quellen aus
  Stufe 6. Nur keine Platzhalter-Schreibweise.

---

## Die letzte Prüfung

Den fertigen Text noch einmal lesen und fragen: Klingt irgendein Teil wie ein Chatbot
auf einen einfachen Auftrag? Wenn ja, ist das der schwächste Teil, und er wird neu
geschrieben. Der Maßstab: Prosa, die ein sachkundiger Mensch gerne unter seinem Namen
veröffentlicht.

Dann drei Fragen, die nur in dieser Fassung gestellt werden:
1. Steht irgendwo „lizenziert", „zugelassen", „zertifiziert", „Innung", „Verband",
   „Kammer", „amtlich", „Verbraucherschutz" oder „getestet"? Dann streichen.
2. Steht irgendwo ein Preis in Euro ohne amtliche Quelle? Dann streichen.
3. Ist eine Aussage über Recht oder Gewerbe ohne Quelle aus der Liste? Dann streichen.
