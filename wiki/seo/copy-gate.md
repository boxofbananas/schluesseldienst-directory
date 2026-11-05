---
title: Textgate (Gate 5)
type: seo
status: active
updated: 2026-11-03
---

# Textgate

Die Merkmalsliste in [[design-seed]] fängt die optischen Verräter einer KI-gebauten Site. Dieses
Gate fängt die sprachlichen, und es läuft in Gate 5: auf `city-copy.json` und die
Ratgeberseiten **vor** `npm run build`, und auf die gebauten Seiten Startseite, Bundesland und
„Über uns" in `dist/` **danach**, weil die ihren Text aus `site.json` ziehen. Es benutzt die
**seo-content-engine**-Skill aus `skills/seo-content-engine/` auf zwei Weisen.

## 1. Jeden kurzen Block prüfen (kein Zugang nötig)

`scripts/lint_copy.py` liest die Verbotsliste der Skill
(`skills/seo-content-engine/references/forbidden_words.txt`) plus die eigenen Zusätze des
Blueprints (`scripts/copy-bans.txt`). Beide Listen haben vier Blöcke: `[WORDS]` und `[PHRASES]`
für die **Werbefloskeln**, `[RECHTSWOERTER]` und `[RECHTSWENDUNGEN]` für die **Rechts- und
Amtswörter** (Abschnitt 1a). Ein Eintrag, der auf `*` endet, ist ein **Wortstamm** und trifft
jede gebeugte Form: `lizenzier*` fängt „lizenziert“, „lizenzierte“ und „Lizenzierung“.
Verglichen wird umlauttolerant („zuverlaessig“ gilt wie „zuverlässig“). Nur
Standardbibliothek, Rückgabewert 1 bei jedem Fehler, also läuft es als Schleife: laufen lassen,
nachbessern, erneut laufen lassen.

| Text | Befehl | Was geprüft wird |
|---|---|---|
| Stadtblöcke und Fragen | `python3 scripts/lint_copy.py output/<slug>/site/src/data/city-copy.json --niche "schlüsseldienste" --city-sizes output/<slug>/05-city-sizes.json` | Wort- und Fragenband der Größenklasse ([[page-types]]), jede Antwort 20 bis 120 Wörter, Branchenwort im ersten Absatz, keine verbotenen Wörter, keine Gedankenstriche |
| Bundesland-Seite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/verzeichnis/<bundesland>/index.html --min-words 300 --max-words 500` | Seitenband, Verbote, Gedankenstriche. **Das Band greift erst, wenn Gate 5 den Einleitungstext geschrieben hat** (siehe unten) |
| „Über uns" (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/ueber-uns/index.html --min-words 300 --max-words 500` | Seitenband, Verbote, Gedankenstriche |
| Startseite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/index.html --min-words 800 --max-words 1500 --niche "schlüsseldienste"` | Seitenband, Branchenwort früh, Verbote, Gedankenstriche. Der Ratgeberblock darin bleibt bei 400 bis 600 Wörtern und die Fragen bei 5 bis 8 |
| Garantie-Seite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/festpreis-garantie/index.html --min-words 700 --max-words 1200 --erlaube-rechtswoerter` | Seitenband, Floskelverbote. Die Rechtswörter und „Garantie"/„garantiert" sind hier zugelassen (siehe unten). **Zusätzlich von Hand prüfen:** alle sechs Voraussetzungen stehen da, die drei Teile der Garantie stehen da, der Satz „kein Test vor Ort" steht da, der Satz „die Garantie gibt der Betrieb" steht da, der Satz zur Nichtkäuflichkeit steht da, der Weg zur Meldung einer Rechnung steht da ([[siegel-programm]]) |
| Premium-Seite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/premium/index.html --max-words 400 --erlaube-rechtswoerter` | Floskelverbote, Gedankenstriche. Der Schalter nur wegen des Satzes „Die Garantie ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit." ([[page-types]]) |
| AGB (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/agb/index.html --erlaube-rechtswoerter` | Floskelverbote, Gedankenstriche; kein Wortband (eine Rechtsseite wird nicht auf Länge geschrieben) |
| Ratgeberseite | `python3 scripts/lint_copy.py output/<slug>/site/src/pages/ratgeber/<slug>.md --min-words 1200 --niche "<thema>" --facts output/<slug>/05-fact-sheet.md` | 1.200 Wörter oder mehr, Thema früh, Verbote, Gedankenstriche. **`--facts` ist bei Ratgeberseiten Pflicht:** jede Zahl (Euro, Prozent, Jahre, Gerichts-/Aktenzeichen) muss in der Faktensammlung belegt sein, sonst scheitert die Prüfung (Abschnitt 2b). Klärt die Seite über die Rechtslage auf, dann zusätzlich `--erlaube-rechtswoerter` |

**Die Datei `05-city-sizes.json`** erzeugt kein Gate von sich aus; sie ist die Größentabelle für
den Lauf auf `city-copy.json` und wird in Gate 5 **unmittelbar nach `node dump-cities.mjs`** aus
`05-cities.json` geschrieben, in einer Zeile:

```
python3 -c "import json;print(json.dumps({c['slug']:c['count'] for c in json.load(open('output/<slug>/05-cities.json'))}))" > output/<slug>/05-city-sizes.json
```

Ohne diese Datei gilt für jede Stadt 500 Wörter und 4 Fragen, also fällt jede kleine Stadt zu
Unrecht durch. Maßgeblich für die Größenklassen bleibt ohnehin `scripts/check_city_copy.py`: es
liest die Spanne jeder Stadt aus der Zeile `intro band:` ihres Pakets.

Die Lesbarkeitsstufe wird berichtet, nicht erzwungen. Für deutsche Texte über ein
Handwerksthema taugt eine Stufe, die ein Laie im Notfall am Telefon versteht; sehr lange
Sätze kürzen. Die englischen Stufenwerte der Skill sind auf deutsche Sätze nicht
übertragbar, weil deutsche Wörter länger sind; sie sind ein Hinweis, kein Maß.

`.astro`-Seiten werden als Ganzes geprüft, feste Absätze eingeschlossen, also gilt das
Seitenband und nicht das Blockband. **Die Startseite nie aus `index.astro` prüfen:** sie zählt
zu wenig, und ihr erster Absatz nach dem Entfernen des Auszeichnungscodes ist die
H1-Formulierung, sodass die Branchenprüfung aus dem falschen Grund scheitert.

**Warum das Band der gebauten Startseite 800 bis 1.500 ist.** Der Aufbau des Templates
(Länderkarten, Städtekarten, Zahlenreihe, Suchfeldbeschriftungen, die drei Versprechen, die
vier Prüfschritte) ergibt im gebauten Zustand etwa 350 Wörter Text, bevor ein Satz geschrieben
ist – in dieser Fassung mehr als in der englischen, weil die Bundeslandkarten dazukommen und
deutsche Beschriftungen länger sind. Mit dem Ratgeber bei 400 bis 600 und den Fragen bei 5 bis
8 muss die Obergrenze 1.500 sein, damit beide Bänder zugleich halten. Der geschriebene Text
sind etwa 800 bis 1.200 Wörter.

**Warum das Band der Garantie-Seite 700 bis 1.200 ist.** `/festpreis-garantie/` muss die drei
Teile der Garantie, alle sechs Voraussetzungen, das vollständige Serviceversprechen **und** die
Aufklärung über die Rechtslage tragen ([[siegel-programm]], [[konventionen]]); das sind
Pflichtteile, die zusammen unter 700 Wörtern nicht ohne Auslassung hineinpassen (der Probebau
der Vorgängerseite vom 03.11.2026 kam auf 784 Wörter und war vollständig, fiel aber am alten
Band 400 bis 700 durch).

**Warum das Band der Bundesland-Seite erst später greift.** Die Vorlage
(`templates/astro/src/pages/verzeichnis/[bundesland]/index.astro`) setzt den Einleitungstext aus
`site.regionIntro`; im ausgelieferten Template ist dieses Feld leer (`[]`), und ohne es trägt die
Seite nur Seitenkopf, Städteliste und Fragen, im Probebau 227 Wörter. **Das Band ist richtig, die
Seite war noch nicht geschrieben:** 300 bis 500 Wörter gelten erst, wenn Gate 5 den
Einleitungstext je Bundesland geschrieben hat. Bis dahin wird die Bundesland-Seite ohne
`--min-words` geprüft (Verbote und Gedankenstriche genügen), und `05-build-report.md` führt den
fehlenden Einleitungstext als offenen Punkt.

**Offener Punkt am Template:** `site.regionIntro` ist **ein** Textfeld für alle 16
Bundesland-Seiten. Derselbe Text auf jeder von ihnen wäre doppelter Inhalt auf der ganzen
Zwischenebene. Ein Einleitungstext je Bundesland braucht deshalb ein nach Bundesland
geschlüsseltes Feld in der Vorlage; solange es das nicht gibt, bleibt `regionIntro` leer und die
Bundesland-Seiten laufen ohne Einleitung, mit ausgesetztem Band.

## 1a. Der Schalter für die Rechtswörter

`forbidden_words.txt` verbietet die Rechts- und Amtswörter („lizenziert", „zugelassen",
„zertifiziert", „Meisterpflicht", „Kammer", „amtlich", „Testsieger", „staatlich", „getestet")
ausdrücklich **auch in Verneinungen**. Für die Seiten, die nach [[konventionen]] genau darüber
aufklären müssen („Der Schlüsseldienst ist kein zulassungspflichtiges Handwerk … wer mit
‚lizenziert‘ wirbt, sagt nichts aus"), ist das ein Widerspruch, der sich nicht durch Umschreiben
auflösen lässt: die Aufklärung braucht das Wort, das sie bestreitet.

Deshalb stehen diese Einträge in beiden Verbotslisten in einem eigenen, benannten Block
(`[RECHTSWOERTER]` und `[RECHTSWENDUNGEN]`), und `scripts/lint_copy.py --erlaube-rechtswoerter`
(englische Zweitform `--allow-legal-words`) lässt genau diesen Block für **eine einzelne Seite**
zu. Die Werbefloskeln aus `[WORDS]` und `[PHRASES]` bleiben dabei verboten, und der Bericht
schreibt eine Hinweiszeile, dass der Schalter an war.

**Der Schalter gilt ausschließlich für:**

- `/festpreis-garantie/` – die drei Teile, die sechs Voraussetzungen und die Aufklärung, was die
  Garantie nicht ist
- `/premium/` – wegen des Satzes zur Nichtkäuflichkeit der Garantie
- `/agb/` – die Rechtsseite zu den bezahlten Stufen und zur Garantie
- Ratgeberseiten, die über die Rechtslage aufklären (kein zulassungspflichtiges Handwerk, keine
  Lizenz, keine Meisterpflicht)

**Nie für Stadttexte, Eintragsbeschreibungen oder die Startseite.** Dort gibt es keinen Grund,
diese Wörter zu schreiben, und dort wäre jede Verwendung genau der Rechtsverstoß, den die Liste
verhindert. Auch mit Schalter gilt: kein Satz behauptet eine Lizenz, eine Zulassung oder eine
amtliche Rolle; die Wörter stehen nur in der Verneinung oder als Zitat der Werbung anderer.
`scripts/check_city_copy.py` kennt den Schalter nicht und wird ihn nie bekommen: Stadttexte
werden immer gegen die vollständige Liste geprüft.

### 1b. „Garantie" und „garantiert"

Seit das Programm Festpreis-Garantie heißt (2026-11-03), ist das Wort in zwei Rollen unterwegs:
als Name des Programms und als Werbeversprechen eines Betriebs. Die Regel:

- **Der Programmname „Festpreis-Garantie"**, genau so, mit Bindestrich, ist **überall**
  erlaubt: auf jedem Eintrag („Festpreis-Garantie 2026" oder „Noch keine Festpreis-Garantie"),
  auf jeder Stadtkarte, auf der Startseite, auf „Über uns". `scripts/lint_copy.py` nimmt ihn vor
  dem Vergleich aus dem Text (`PROGRAMMNAME`), damit die Startseite ohne Schalter besteht.
- **Jede andere Form** – „Garantie", „garantiert", „garantieren", „Festpreisgarantie" ohne
  Bindestrich, „Zufriedenheitsgarantie", „kostenlose Anfahrt garantiert" – steht als Stamm
  `garantie*` und als Wendungen im Rechtsblock von `forbidden_words.txt`: ohne Schalter ein
  Treffer, mit `--erlaube-rechtswoerter` zugelassen. Zugelassen ist das Wort damit auf
  `/festpreis-garantie/` (die Seite erklärt, was der Betrieb garantiert), auf `/premium/` (der
  Satz zur Nichtkäuflichkeit) und in den AGB.
- **Im Eintrag** steht das Wort nur in dem Block, den die Seite aus den Spalten `geprueft`,
  `geprueft_jahr`, `garantie_tag`, `garantie_nacht`, `garantie_anfahrt`, `garantie_zylinder` und
  `garantie_zylinder_5mm` baut: „Festpreis-
  Garantie 2026", die Preise, der Satz, dass der Betrieb den genannten Preis als
  Rechnungspreis garantiert. Dieser Block kommt aus dem Template und wird nicht gelintet.
- **Ein Betrieb ohne Garantie darf in seiner Beschreibung nicht „garantiert" sagen**, und ein
  Betrieb mit Garantie auch nicht: die Garantie zeigt die Seite, nicht sein Text. Die
  Beschreibungen prüft `scripts/merge_enriched.py` in Gate 3 gegen die vollständige Liste, ohne
  Schalter und ohne die Ausnahme für den Programmnamen; dort ist auch „Festpreis-Garantie" ein
  Treffer, weil eine Beschreibung das Programm nie erwähnt (`scripts/enrichment-instructions.md`).
- Stadttexte: wie Beschreibungen, vollständige Liste, nie der Schalter. Wer in einem Stadttext
  auf das Programm hinweisen will, schreibt den Programmnamen und sonst nichts mit diesem Stamm.

## 2. Was der Prüfer zusätzlich fängt

`scripts/check_city_copy.py` läuft das Textgate und prüft vier Dinge mehr: jede Zahl muss in
den Daten der Stadt oder auf der Faktensammlung stehen, **keine Prozentangabe und kein
Eurobetrag**, keine interne Wortwahl, und kein Satz und kein Anfang, den drei oder mehr Städte
teilen.

Der vollständige Aufruf (er schreibt `city-copy.json` erst, wenn jede Stadt beantwortet ist und
nichts durchfällt; `--write` erwartet den Pfad der Datei, es ist kein Schalter ohne Wert):

```
python3 scripts/check_city_copy.py --copy output/<slug>/05-cache/city-copy \
    --batches output/<slug>/05-cache/city-batches --facts output/<slug>/05-fact-sheet.md \
    --niche "Schlüsseldienste" --write output/<slug>/site/src/data/city-copy.json
```

Für diese Fassung kommt dazu, was in keinem sichtbaren Text vorkommen darf und von Hand oder
über `scripts/copy-bans.txt` geprüft wird (zu den beiden Rechtsblöcken siehe Abschnitt 1a: nur
`/festpreis-garantie/`, `/premium/`, `/agb/` und Ratgeberseiten zur Rechtslage dürfen sie
bestreiten):

- **„lizenziert", „zugelassen", „zertifiziert", „Meisterbetrieb" als Gütezeichen,
  „Konzession".** Schlüsseldienst ist kein zulassungspflichtiges Handwerk; es gibt keine
  Lizenz und keine Meisterpflicht ([[konventionen]]).
- **„Innung", „Verband", „Kammer", „amtlich", „offiziell geprüft", „Verbraucherschutz",
  „getestet".** Grund: Verwechslungsgefahr mit einer amtlichen Stelle. Das Verzeichnis ist
  ein privates Angebot der DOM Holding GmbH, und seine Festpreis-Garantie ist ein Versprechen
  des Betriebs, das der Herausgeber veröffentlicht und überwacht ([[siegel-programm]]).
- **„geprüft"** nie als allgemeines Lob für einen Betrieb; sichtbar heißt der Zustand
  „Festpreis-Garantie [Jahr]", nicht „geprüft".
- **„Garantie", „garantiert"** nach Abschnitt 1b: nur der Programmname „Festpreis-Garantie" ist
  frei, alles andere nur mit Schalter auf den dort genannten Seiten.
- **Jeder Preis und jede Preisspanne in Euro** in Stadt-, Bundesland- und Eintragstexten.
  Erlaubt sind Preise nur auf `/premium/` und in den AGB (die eigenen Stufen) und in einer
  Ratgeberseite, wenn die Zahl in der Faktensammlung belegt ist (siehe 2b) ([[page-types]]).

## 2b. Zahlen einer Ratgeberseite gegen die Faktensammlung

Die Lehre aus dem Nachtlauf vom 2026-11-04: Das Textgate prüft **Wörter, nicht Tatsachen**. Fünf
Ratgeberseiten entstanden über Nacht mit dutzenden konkreten Euro-Beträgen, Gerichtsurteilen und
Innungssätzen, die in `05-fact-sheet.md` **nicht** standen — sprachlich sauber, aber unbelegt.
Deshalb trägt `lint_copy.py` jetzt `--facts <pfad>`: Für eine Ratgeberseite muss **jede Zahl der
vier Kategorien — Euro-Beträge, Prozente, Jahreszahlen, Gerichts-/Aktenzeichen — als eigenständiges
Token in der Faktensammlung vorkommen**, sonst scheitert das Gate (`zahlen_im_faktenblatt`) und nennt
die Fundstellen. Spannen wie „65 bis 415 Euro" werden ganz geprüft, beide Zahlen.

Nicht geprüft werden **Bezeichner**, keine Tatsachenzahlen: Normkennungen (DIN, EN, RC), Maße (mm),
Notruf- und Förderprogrammnummern (112, 110, KfW 159). Sie sind Namen, keine belegpflichtigen
Angaben. Eine Zahl kommt also nur auf eine Ratgeberseite, wenn sie zuvor mit Quelle und Abrufdatum
ins Faktenblatt eingetragen wurde — nie umgekehrt. Belegt oder raus; keine vage Ersatzformulierung,
die dieselbe Behauptung nur unscharf macht.

**Eine Zahl aus einer nicht zugelassenen Quelle ist auch dann unzulässig, wenn sie stimmt.** Das
Gate prüft, ob eine Zahl im Faktenblatt steht; der Mensch prüft davor, ob sie überhaupt hineindurfte.
Ins Faktenblatt kommt nur, was aus den Quellen von [[konventionen]] belegt ist (Handwerkskammer,
Stadt-/Gemeindeportale, Verbraucherzentrale, Polizeiliche Kriminalprävention, Stiftung Warentest).
Innungs- und Verbandspreislisten, Branchenbücher, Presseportale und andere
Schlüsseldienst-Websites zählen nicht dazu — eine von dort übernommene Zahl bleibt draußen, auch
wenn sie zufällig korrekt wäre. Beispiel aus dem Lauf vom 2026-11-05: die Sonntagspreise
„167,60–209,50 €" bzw. „167,60/177,00 €" waren Innungsempfehlungen (unzulässige Quelle) **und** in
sich widersprüchlich (zwei Werte für denselben Posten beweisen die Erfindung). Entscheidend war
aber schon das Erste: die Quelle war nicht zugelassen. Die Richtigkeit einer Zahl ersetzt den Beleg
nicht.
- **Werbefloskeln** aus `forbidden_words.txt`: „schnell und günstig", „rund um die Uhr für
  Sie da", „unschlagbar", „führend", „Nummer 1", „seriös und zuverlässig" als Behauptung über
  einen Betrieb, den das Verzeichnis nicht geprüft hat.
- **Erfundene Ortsangaben.** Eine Stadttatsache ohne Quelle aus der Liste in
  [[konventionen]] wird nicht geschrieben.

## 3. Die artikelförmigen Seiten mit der Skill schreiben

Ratgeberseiten und der Ratgeberblock der Startseite sind der Text, der wirklich
artikelförmig ist: ein Thema, eine Seite, gebaut um verlinkt zu werden
([[authority-and-links]]). Dafür den vollständigen Ablauf der Skill benutzen. Stufe 1 holt die
aktuellen Treffer zum Thema über die DataForSEO-Anmeldung des Betreibers, die späteren Stufen
entwerfen, glätten, prüfen die Tatsachen und geben aus.

- DataForSEO ist **wahlweise**. Der Start (Gates 1 bis 6) braucht nichts davon. Ohne
  Verbindung diese Seiten von Hand aus der Faktensammlung schreiben und mit der Tabelle oben
  prüfen.
- Die Skill findet die Verbindung am Werkzeugnamen; sie fragt nie einen Zugang im Gespräch ab,
  und `references/credentials.md` bleibt leer.
- **Die Tatsachenprüfung der Skill ersetzt die Faktensammlung nicht.** Was die Skill findet,
  wird gegen die Quellen aus [[konventionen]] gehalten: Handwerkskammer, Gewerbeamt,
  Verbraucherzentrale, polizei-beratung.de, Stiftung Warentest. Ein Punkt, für den nur eine
  kommerzielle Quelle oder ein anderes Branchenbuch gefunden wird, gilt als **unbelegt** und
  darf in keinem Text auftauchen.
- Was die Skill schreibt, ist auf Deutsch zu schreiben. Englische Textmuster der Skill
  („TL;DR", „verdict") werden nicht übersetzt übernommen, sondern durch deutsche Formen
  ersetzt: ein Vorspann und ein Fazit.

## Wofür die Skill nicht da ist

Der Stadtblock. Die Skill schreibt je Lauf einen langen Artikel; Stadtseiten wären so viele
Läufe in der falschen Form. Ein Stadtblock sind 500 bis 800 Wörter Ortstext über den Karten,
aus den angereicherten Daten geschrieben. **Prüfen, nicht erzeugen.**

## Siehe auch
[[konventionen]] · [[page-types]] · [[design-seed]] · [[siegel-programm]]
