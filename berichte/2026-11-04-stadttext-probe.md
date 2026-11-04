# Stadttext-Probestapel + Welle-1-Stichprobe (2026-11-04)

Zwei getrennte Prüfungen in einem Bericht:
- **Teil A:** 10 Welle-1-Beschreibungen aus den breiten Kategorien (Alarm-/Tresorbetriebe) – gehören sie ins Schlüsseldienst-Verzeichnis?
- **Teil B:** Stadttext-Probe über 20 Städte, zwei Modelle (Sonnet, Haiku), Kosten + Unterscheidbarkeit, neue Ähnlichkeitsprüfung.
- **Nebenfund:** 9 Städte ohne Bundesland (ausländische Grenzorte) – eine Gate-4-Entscheidung.

---

## Teil A — Welle-1 aus den breiten Kategorien

Gezielt gezogen (nicht zufällig) aus den Kategorien, über die der breite Nachbestell-Lauf
Betriebe einfing, die keine Türen öffnen: **Security system supplier** (143 angereichert),
**Safe & vault shop** (34), **Security system installation service** (3). Insgesamt **180**
Welle-1-Einträge aus diesen drei Kategorien. Je Eintrag: der volle Text, das Merkmal `kern`
(leistet der Betrieb die Kernarbeit Türöffnung/Schließtechnik?) und worauf die Kernaussage ruht.

**Befund vorweg:** Die sechs Textregeln (keine Preise, Bewertungen, Kontaktdaten usw.) sind in
allen zehn eingehalten – die Texte sind sauber. Aber `kern` trennt sauber zwei Gruppen:

- **Reine Tresor-/Alarmbetriebe** (kern=false oder „not enough info"): Compact Tresore,
  TresorXperten, T&R Tresortechnik, Tresor Technik Jarz, Das Schliesswerk, Reiher
  Sicherheitssysteme. Diese öffnen **keine Wohnungstüren**; ihr Text liest sich als Tresorhandel
  oder Alarmbau. Sie gehören nach der Kern-Logik **nicht** auf eine Schlüsseldienst-Stadtseite.
- **Echte Schlüsseldienste mit Sicherheitstechnik** (kern=true, Beleg für Türöffnung):
  Schlüssel-Reese (HH, seit 1921), Schor Einbruchschutz (hat eigenen Schlüsseldienst),
  Stürmer-Alarm und ast Alstertaler (Grenzfälle – Alarmbauer, die Zylinder/Schließanlagen
  einbauen, aber Türöffnung nicht belegen).

**Das bestätigt die Sorge:** Eine alarmfirmen-lesende Beschreibung verletzt keine der sechs
Regeln und rutscht trotzdem ins Verzeichnis. Der Filter dagegen ist **nicht** der Textlinter,
sondern das Merkmal `kern` in Gate 4 (`04-exclusions.csv`). Empfehlung am Ende von Teil A.

### Die zehn Beschreibungen

**1. Tresor Technik Jarz Frankfurt** — Frankfurt am Main · _Safe & vault shop_ · **kern=not enough info**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Tresore sind das Hauptgeschäft von Tresor Technik Jarz in Frankfurt am Main. Der Inhaber Robert Jarz, ausgebildeter Geräte- und Feinwerktechniker, gründete die Firma 2011; später kamen Niederlassungen in Friedrichsdorf und Bad Vilbel hinzu. Das Angebot reicht vom Verkauf über Transport und Entsorgung bis zu Reparatur, Wartung und Umbau, für private wie gewerbliche Kunden. Tresore werden bei verlorenem Schlüssel oder vergessenem Zahlencode geöffnet, wenn möglich zerstörungsfrei. Die Notöffnung ist an sieben Tagen in der Woche möglich und wird auch bundesweit angeboten. Schon vorab gibt es eine Kosteneinschätzung, und für die Tresoröffnung nennt der Betrieb einen festen Preis. Dazu kommen Ersatzschlüssel, Schlosswechsel, das Nachmachen von Schlüsseln, die Umrüstung auf elektronische Schlösser sowie Einbruchschutz und Sicherheitstechnik. Schlüsseltresore für Hausverwaltungen und Unternehmen gehören ebenfalls zum Sortiment.

**2. Compact Tresore | Tresorverkauf Stuttgart** — Backnang · _Safe & vault shop_ · **kern=false**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Compact Tresore in Backnang bei Stuttgart ist ein Familienunternehmen und nennt sich Tresor-Spezialist, tätig seit 1981. Verkauft und beraten werden Sicherheitstresore, Wertschutztresore, Panikraumsysteme und Tresorräume für Privat- und Gewerbekunden, auch deutschlandweit. Zu den Dienstleistungen zählen Beratung, Lieferung, Montage und Verankerung, Wartung und Prüfung, das Nachmachen von Tresorschlüsseln sowie Notöffnung und Entsorgung. Das Programm führt Tresore nach Widerstandsgraden von 0 bis VI und beschreibt elektronische Tresorschlösser mit Zahlencode. Dazu kommen Sicherheitsschlösser und Sicherheitsschlüssel. Die Beratung berücksichtigt den Einsatzbereich und die Anforderungen der Versicherung. Termine lassen sich buchen. Das Haus liefert diskret und neutral verpackt, plant die Aufstellung vorab und verankert den Tresor am Ort. Neben Wandtresoren und Tresorräumen führt es Verpflegungs- und Vending-Automaten, eine Manufaktur namens LEVEL und Goldtresore. Zu den Zielgruppen zählen Unternehmen wie Privatkunden.

**3. T&R Tresortechnik GmbH** — Kassel · _Safe & vault shop_ · **kern=not enough info**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> T&R Tresortechnik in Kassel ist auf Tresore spezialisiert und bietet ein Komplettangebot rund um den Tresor: Notöffnungen, Reparatur beschädigter Tresore und Geldschränke, Wartung und Umrüstung. Mit Spezialwerkzeug öffnet der Betrieb mechanische Zahlenschlösser, Doppelbartschlösser und elektronische Schlösser, wenn ein Schlüssel oder Code verloren ist oder Gewalt eingewirkt hat. Mechanische Schlösser lassen sich auf ein Elektronikschloss umrüsten. Tresorschlüsselduplikate fertigt er an, bei Tresoren mit Typenschild nur gegen Vorlage des Originalschlüssels. Seit Jahren betreut der Betrieb außerdem die Sicherheitstechnik im Bankenbereich mit Service und Wartung. Das Leistungsfeld gliedert sich in Tresorservice, Notöffnungen, Schlüsselservice, Bankenservice, Beratung und Wartung. Typische Anlässe sind Einbruchschäden, verlorene Schlüssel und vergessene Codes. Der Kundendienst reicht über Deutschland hinaus nach Frankreich und Belgien, und das Team wird erweitert. Der Betrieb sitzt in Kassel.

**4. TresorXperten** — Nürnberg · _Safe & vault shop_ · **kern=false**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> TresorXperten in Nürnberg verkauft Tresore für Privatleute und Unternehmen und berät dazu vor Ort oder telefonisch. Das Sortiment reicht von Datensicherungs-, Deposit- und Dokumententresoren über Luxus-, Möbel-, Wand- und Schlüsseltresore bis zu Tresortüren, Waffenschränken, Wertschutzschränken und Tresorräumen, auch feuerfest und in verschiedenen Sicherheitsstufen. Ein Datensicherungstresor schützt nach der Darstellung des Betriebs neben dem Einbruch auch vor Feuer, Magnetismus und Feuchtigkeit, und Deposittresore nehmen Tageseinnahmen bis zur Abholung durch einen Geldkurier auf. Zu beiden Tresorarten führt der Betrieb eigene Fragen und Antworten. Nach dem Kauf übernimmt er den Service: Wartung, Reparatur, Tresortransport, Tresorentsorgung und die Notöffnung, wenn sich ein Tresor nicht mehr öffnen lässt. Sein Schwerpunkt sind Tresore und Wertbehältnisse, nicht die Öffnung von Wohnungstüren. Weitere Seiten behandeln Sicherheitsstufen, den feuerfesten Tresor und die Tresortür.

**5. ast Alstertaler Sicherheitstechnik GmbH** — Hamburg · _Security system installation service_ · **kern=true**  
Kern-/Türöffnungsbeleg: können wir einen passenden gleichschließenden Zylinder installieren  

> Seit 1991 sichert die ast Alstertaler Sicherheitstechnik GmbH in Hamburg Privathäuser, Geschäfte, Arztpraxen, Büros und Gewerbeobjekte gegen Einbruch und Brand. Der Schwerpunkt liegt auf Alarmanlagen von Ajax, funkbasiert oder verkabelt, und von Telenot für Gewerbe, auf Videoüberwachung, Brandschutz mit Rauchmeldern und Brandmeldeanlagen sowie Zutrittskontrolle mit Sprechanlagen, Türöffnern, Motorschlössern und elektronischen Schließzylindern. Dazu kommt mechanischer Schutz für Fenster und Türen: Fensterschutz, Türschutz, Panzerriegel, Schließzylinder und Zusatzsicherungen, auch von ABUS. Soll ein Panzerriegel mit dem normalen Haustürschlüssel zu öffnen sein, installiert der Betrieb einen passenden gleichschließenden Zylinder; KESO-Zylinder liefert er auch als Schließanlage. Die Konzepte gelten für Privat und Gewerbe. Die Seite nennt auch den Zusammenhang mit der Initiative K-EINBRUCH und einem Merkblatt für Einbruch- und Überfallmeldeanlagen des Landeskriminalamtes Hamburg; zum Sortiment gehören zudem Ajax-Videoüberwachung und Brandwarntechnik.

**6. Das Schliesswerk** — Brilon · _Security system installation service_ · **kern=not enough info**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Das Schliesswerk in Brilon plant, montiert und betreut Schließsysteme, mechanisch, mechatronisch und elektronisch. Partner sind BKS, Assa Abloy und Salto Systems, als SALTO Premium Partner installiert der Betrieb mit einem ständig geschulten Team elektronische Zutrittssysteme. Das Leistungsspektrum umfasst Planung, Montage, Erweiterungen, Wartung und Schulung, außerdem Zutrittskontrolle auf der Grundlage der CLIQ Technologie sowie registrierte Schließungen mit Sicherungskarte. Zu den Kunden zählen nach eigener Angabe Hotels, Speditionen, Caritasverbände, Schulen, Kliniken, mittelständische Unternehmen, Städte und Jugendhilfeeinrichtungen. Auch Lösungen für Fluchttüren, Notausgänge und Rettungswege gehören zum Thema, ebenso die Umstellung einer vorhandenen Anlage auf elektronische Zutrittskontrolle samt Buchungssoftware. Wer eine Anlage nach einem Schlüsselverlust anpassen muss, findet im Betrieb ebenfalls einen Ansprechpartner für neue Schlüssel und Zylinder. Die Zylindersysteme sind patentgeschützt, gibt es in modularer Bauweise und als codierte Einzelschließungen im Normalprofil.

**7. Stürmer-Alarm | Alarmanlagen und Brandmeldetechnik** — Mettmann · _Security system installation service_ · **kern=true**  
Kern-/Türöffnungsbeleg: Wir installieren mechanische Schließsysteme von KESO  

> Seit 1971 sorgt Stürmer-Alarm im Kreis Mettmann, im Großraum Düsseldorf und in Wuppertal für Sicherheit. Der Schwerpunkt liegt auf Alarmanlagen, Funkalarm, Brandmelde- und Rauchwarntechnik, Zutrittskontrolle und Videoüberwachung, die der Betrieb plant und einbaut. Bei den Schließsystemen installiert er mechanische Schließzylinder und Schließanlagen von KESO, auch als elektronische Zylinder, und führt Standtresore, Wandtresore, Möbeltresore und Waffenschränke. Kunden erhalten rund um die Uhr einen technischen Support, bei Bedarf direkt vor Ort. Der Betrieb nennt sich Mitglied der polizeilichen Einbruchschutzkampagne K-EINBRUCH und berät private wie gewerbliche Kunden zu wirksamem Einbruchschutz. Bei den Zylindern nennt er unter anderem den KESO 8000Ω³, der gegen Abbrechen, Herausziehen und Aufbohren geschützt sein soll; Schlüsselkopien sind dort nur mit Sicherungsschein möglich. Die Wartung der Anlagen führt er fachgerecht selbst durch.

**8. Reiher Sicherheitssysteme GmbH** — Ludwigsburg · _Security system supplier_ · **kern=not enough info**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Reiher Sicherheitssysteme im Kreis Ludwigsburg ist ein Fachbetrieb für Sicherheitstechnik mit mehr als fünfzig Jahren Erfahrung. Das Angebot reicht von Tresoren und Waffenschränken über Video und Alarm, Brandschutz und mechanische Absicherung bis zu mechanischen und elektronischen Schließsystemen und elektronischer Zutrittskontrolle. Tresore und Waffenschränke schützen persönliche Werte, wichtige Dokumente und legale Schusswaffen, viele Modelle bieten zusätzlich Feuer- und Wasserschutz. Der Betrieb berät, montiert, wartet und repariert, und Schlüssel und Schließanlagen lassen sich bei ihm nachbestellen. Für Notfälle gibt es eine Nummer für den Schlüssel-Notdienst. Beim Kauf eines Wertschutzschranks oder Tresors setzt der Betrieb auf offene Kommunikation, weil der Kauf vor allem Vertrauenssache gegenüber dem Fachhändler sei. Er legt Wert auf Qualität am Produkt ebenso wie bei der Beratung und führt einen Shop sowie Referenzen.

**9. Schlüssel-Reese GmbH Schließanlagen Einbruchschutz Hamburg** — Hamburg · _Security system supplier_ · **kern=true**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Schlüssel-Reese ist ein Traditionsbetrieb, der nach eigener Angabe seit 1921 als Schlüsseldienst in Hamburg und Lübeck arbeitet. Das Programm umfasst mechanische Schließzylinder von KESO, CES und Winkhaus mit Anbohrschutz, elektronische Schließzylinder sowie mechanische und elektronische Schließanlagen und Einzelschließungen. Schlüssel gibt es vom Ersatzschlüssel bis zum Oldtimerschlüssel, dazu Zylinder-, Tresor-, Auto-, Motorrad-, Möbel- und Truhenschlüssel. Kurzfristige Türöffnungen, Schlossreparaturen, Briefkästen, Tresore, Gravuren und Zusatzsicherungen wie Panzerriegel, Stangenschloss, Fenstersicherung und Kastenzusatzschloss ergänzen das Angebot. Beratung zur Einbruchsicherung für Haus und Wohnung gehört ebenfalls dazu. Bei Fahrzeugschlüsseln sieht sich der Betrieb als Experte, und er steht nach eigener Angabe deutschlandweit zur Verfügung. Der Betrieb stellt Serviceleistungen rund um Schlüssel, Schlösser und Sicherheit zusammen, mit Standorten in Hamburg und Lübeck, und führt seine Produkte nach eigener Angabe in höchster Qualität.

**10. Schor Einbruchschutz** — Dormagen · _Security system supplier_ · **kern=true**  
Kern-/Türöffnungsbeleg: — kein Beleg für Türöffnung/Kern im Stapel —  

> Schor Einbruchschutz in Dormagen führt nach eigener Angabe seit über 75 Jahren Beratung und Montage von Sicherheitstechnik aus. Im Mittelpunkt stehen mechanischer Einbruchschutz, Türsicherheit, Sicherheitszylinder, Scherengitter, Panzerriegel sowie Fenster- und Türschlösser mit Beschlägen. Eingebaut wird Sicherungstechnik nach DIN 18104 Teil 1 und Teil 2, also Aufschraubprodukte und Pilzkopfverriegelungen. Ergänzend gibt es elektronische Zylinder, Funk-Alarmanlagen, Glas-Sicherheitsfolien, Videoüberwachung, Insektenschutz, die Wartung von Fenstern und Fenstertüren sowie die Reparatur von Schäden. Der Schlüsseldienst des Betriebs öffnet Haus- und Wohnungstüren mit möglichst beschädigungsfreien Verfahren, im Notfall auch Tresore. Bei Tresoren steht neben dem klassischen Schloss eine elektronische Verriegelung mit Code oder Fingerprint zur Wahl. Fachvorträge und eine Ausstellung gehören ebenfalls zum Angebot. Als Handwerksbetrieb ist er nach eigener Angabe im Adressennachweis für Errichterunternehmen mechanischer Sicherungseinrichtungen geführt.


### Empfehlung Teil A
`kern=false`/`not enough info` aus diesen drei Kategorien ist ein starkes Ausschluss-Signal.
Vorschlag: die Welle-1-Einträge dieser Kategorien mit `kern≠true` dem Betreiber als Liste
vorlegen (wie die fremden Gewerbe in Gate 4) und per `04-exclusions.csv` droppen, sofern der
Text nicht doch eine Türöffnung belegt. Reine Tresorhändler und Alarmbauer ohne Türöffnung
sind kein Schlüsseldienst.

---

## Nebenfund — 9 Städte ohne Bundesland

Beim Ziehen der Probestädte fielen 9 „Städte" ohne `region` auf (key `x/…`): **ausländische
Grenzorte mit echten Einträgen** und ein PLZ-Zuordnungsfehler.

| Stadt | Einträge | Seite im Verzeichnis? | Art |
|---|---|---|---|
| Basel (CH) | 9 | ja | Schweiz, Grenze zu Weil am Rhein |
| Binningen (CH) | 4 | ja | Schweiz (Basel-Umland) |
| Kreuzlingen (CH) | 3 | ja | Schweiz (Bodensee) |
| Münchenstein (CH) | 3 | ja | Schweiz (Basel-Umland) |
| Słubice (PL) | 2 | ja | Polen (Oder, Frankfurt-Grenze) |
| Forbach (FR) | 1 | nein (Ortsseite) | Frankreich (Saarland-Grenze) |
| Spicheren (FR) | 1 | nein | Frankreich |
| Oberzent (DE) | 1 | nein | **deutsch (Hessen), PLZ-Zuordnung verfehlt** |
| „Unbekannt" | 1 | nein | Sammelrest |

**Entscheidung nötig (Gate-4-artig):** Basel mit 9 Einträgen bekäme sonst eine indexierbare
Schweizer Stadtseite auf einem Deutschland-Verzeichnis. Vorschlag: die vier Schweizer und zwei
französischen Orte per `04-exclusions.csv` droppen (das Verzeichnis ist „in Deutschland");
Oberzents Bundesland von Hand nachtragen (es ist Hessen); „Unbekannt" prüfen. Kein Vorgabewert,
der automatisch löscht.

---

## Teil B — Stadttext-Probe

20 Städte gemischter Größe (2 Groß-, 5 Mittel-, 13 Klein-/Winzigseiten über 16 Bundesländer),
je einmal mit dem **Gate-3-Modell Sonnet** und dem nächstkleineren **Haiku** geschrieben, in
getrennte Ordner (`05-cache/probe-copy-sonnet`, `-haiku`). Faktenblatt vorher mit fünf belegten
Branchenfakten gefüllt (HWK/Handwerksordnung, Verbraucherzentrale, K-EINBRUCH, Stiftung Warentest –
siehe `05-fact-sheet.md`).

### Kosten je Modell und Hochrechnung

| | Städte | Kosten | je Stadt | Token | Laufzeit | 1. Versuch bestanden |
|---|---|---|---|---|---|---|
| **Sonnet** | 20 | 2,94 $ | 14,7 ct | 3,53 Mio | 4:34 min | 4/4 Stapel |
| **Haiku** | 20 | 1,05 $ | 5,3 ct | 6,45 Mio | 5:52 min | 4/4 Stapel |

**Wichtig für die Hochrechnung:** Der Probelauf hat Großstädte überrepräsentiert – 27,6 Einträge je
Seite gegen **5,3 real** über die 729 Seiten. Kosten hängen fast nur an der Paketgröße (Sonnet:
~11 ct Grundpreis je Stadt + 0,15 ct je Eintrag; Haiku: ~3,7 ct + 0,06 ct). Der flache 20er-Schnitt
überschätzt daher. Größengewichtet auf die 729 Seiten (3.868 Einträge):

- **Sonnet: ~86 $** (flacher Schnitt wäre ~107 $)
- **Haiku: ~30 $** (flacher Schnitt wäre ~38 $)

### Unterscheiden sich die zwanzig? (die eigentliche Frage)

**(a) Satzanfänge.** Alle zwanzig Anfänge stehen im Bericht-Anhang untereinander; bei **beiden**
Modellen ist jeder Anfang anders und führt mit einem stadteigenen Zugang („Nürnberger
Schlüsseldienste arbeiten über die Stadtgrenze hinaus …", „Bitburg ist ein Ort, an dem …"). Kein
geteilter Anfang.

**(b) Fast gleiche Sätze (≥3 Städte, Wort-Überlappung ≥75 %).**
- **Sonnet: 0.** Kein Satz kommt in drei Städten fast gleich vor. Erst bei 60 % Überlappung
  erscheint ein einziges Muster (die Bewertungszeile, dort mit verschiedenen Zahlen und Satzbau).
- **Haiku: 4 Cluster über 12 der 20 Städte.** Genau die „gleicher Text, anderer Stadtname"-Gefahr:
  1. `Als Mindestanforderung … Widerstandsklasse RC 2 nach DIN EN 1627` – **ein Faktenblatt-Satz
     fast wörtlich in 4 Städten** (aerzen, dortmund, hamburg, strausberg).
  2. `Die Bewertung liegt bei _ aus _ Bewertungen.` – Bewertungsschablone, 3 Städte.
  3. `Der Betrieb steht bei _ aus _ Bewertungen.` – zweite Bewertungsschablone, 3 Städte.
  4. `Diese Seite zeigt, welche Betriebe in … das anbieten …` – ein **Verzeichnis-Meta-Satz** in 3
     Städten, der nebenbei die Regel „nicht über die Liste schreiben" verletzt.

**(c) Herkunft der Wörter (Paket = stadteigen, Faktenblatt = geteilt, Rest = generisch).**

| | Median Paket% | Median Faktenblatt% | Median generisch% | Städte < 20 % stadteigen |
|---|---|---|---|---|
| Sonnet | **76 %** | 5 % | 19 % | keine (Minimum 48 %) |
| Haiku | 70 % | 6 % | 20 % | keine (Minimum 53 %) |

Beide Modelle schöpfen überwiegend aus den **stadteigenen** Paketdaten, nicht aus dem Faktenblatt
(Median 5–6 %). Kein Text „lebt vom Faktenblatt". Die dünnsten Pakete (Altenburg, Aerzen – zwei
Einträge, teils ohne Website) rutschen am stärksten ins Generische; dort ist die Gefahr am größten.

### Neue Prüfung eingebaut

`check_city_copy.py` prüfte bisher nur **wortgleiche** Sätze – deshalb **bestand Haiku den alten
Check im 1. Versuch**, obwohl 12 Städte Schablonen teilen. Neu eingebaut: ein **Fast-gleich-Durchgang**
(Jaccard der Wortmengen ≥ 0,75, Stadtname entfernt, ab 3 Städten), kalibriert an genau diesem
Probelauf. Verifikation gegen die Probeausgaben:

- **Sonnet: durchgefallen 0** (besteht sauber).
- **Haiku: durchgefallen 12** – die Prüfung nennt je Stadt den Satz zum Umschreiben.

Die Prüfung läuft in jeder Gate-5-Stapelschleife mit; ein Modell, das schablonisiert, kommt nicht
mehr durch.

### Empfehlung Teil B

**Stadttexte auf Sonnet schreiben.** Haiku ist zwar ~3× billiger (~30 $ gegen ~86 $ für 729), fällt
aber bei 12 von 20 Städten durch die neue Prüfung. Mit aktiver Prüfung müsste Haiku jeden Stapel bis
zu dreimal wiederholen und würde dabei kaum konvergieren (ein kleines Modell entschablonisiert
schlecht) – die Ersparnis löst sich in Wiederholungskosten auf, das Ergebnis bleibt austauschbar.
Die ~56 $ Mehrkosten kaufen genau das, worum es bei 729 Seiten geht: dass jede Stadt eigenständig
liest. Empfehlung: **Sonnet, ~86 $, nach Bundesland gestapelt und zwischengespeichert.**


---

## Anhang — Satzanfänge aller 20 Texte

Je Stadt der Anfang des ersten Absatzes. **S** = Sonnet, **H** = Haiku.

**aerzen**  
S: Wer in Aerzen im Weserbergland nach Schlüsseldiensten sucht, findet zwei Betriebe, die weit mehr …  
H: Schlüsseldienste in Aerzen verbinden den Notdienst für Haustüren und Autos mit Sicherheitstechnik für Gebäude …

**ahrensburg**  
S: Die Schlüsseldienste in Ahrensburg arbeiten in einer Umgebung, die sich über mehrere Orte verteilt: …  
H: Die Schlüsseldienste in Ahrensburg in Schleswig-Holstein arbeiten teils mit anderen Gewerken zusammen. Ein Betrieb …

**alsdorf**  
S: Schlüsseldienste in Alsdorf teilen sich auf in einen Einzelunternehmer, der als Notdienst über Kreisgrenzen …  
H: In Alsdorf liegt der Schwerpunkt der Schlüsseldienste auf der Türöffnung und dem Schlosstausch. Ein …

**altenburg**  
S: Bei Schlüsseldiensten in Altenburg im Thüringer Osten fällt zuerst ein Betrieb mit vielen Bewertungen …  
H: Schlüsseldienste in Altenburg reichen von einem Betrieb in der Rechtsform einer Gesellschaft bürgerlichen Rechts …

**andernach**  
S: Schlüsseldienste in Andernach sind zum einen ein Fachbetrieb für Schließtechnik mit langer Geschichte, zum …  
H: Schlüsseldienste in Andernach umfassen hier auch die Planung von Schließanlagen für Gewerbe und Industrie. …

**aschersleben**  
S: Die Schlüsseldienste in Aschersleben haben eine lange Geschichte am selben Ort. Schlüsseldienst Willig Aschersleben …  
H: Seit 1966 arbeitet in Aschersleben in Sachsen-Anhalt der Schlüsseldienst Willig mit Schlössern und Schlüsseln. …

**berlin**  
S: Schlüsseldienste in Berlin arbeiten meist von einem Bezirk aus und fahren trotzdem durch die …  
H: Wer in Berlin ausgesperrt ist, hat die Wahl zwischen Schlüsseldiensten mit eigenem Ladengeschäft in …

**bitburg**  
S: Bitburg ist ein Ort, an dem sich die Schlüsseldienste auf wenige Betriebe stützen und …  
H: Schlüsseldienste in Bitburg teilen sich in zwei Richtungen: den Notdienst für Haus- und Wohnungstüren …

**bremen**  
S: Schlüsseldienste in Bremen sind oft alte Familiengeschäfte, die mit Eisenwaren, Schlosserei oder Schuhreparatur angefangen …  
H: In Bremen reichen die Wurzeln einiger Schlüsseldienste weit zurück. Georg Völz GmbH geht auf …

**dortmund**  
S: Wer in Dortmund einen der Schlüsseldienste braucht, hat die Wahl zwischen mobilen Notdiensten, die …  
H: Schlüsseldienste in Dortmund unterscheiden sich vor allem darin, was neben der Türöffnung angeboten wird. …

**gera**  
S: In Gera ist das Gewerbe der Schlüsseldienste stark vom Handel mit Sicherheitstechnik geprägt: Fachgeschäfte …  
H: Schlüsseldienste in Gera sind häufig an ein Fachgeschäft gebunden. Das Sicherheitsfachgeschäft Peter Böhme besteht …

**hamburg**  
S: Wer in Hamburg einen Schlüsseldienst sucht, findet Fachgeschäfte mit langer Geschichte neben Notdiensten, die …  
H: Die Schlüsseldienste in Hamburg haben zum Teil lange Wurzeln. Hoffmeister Sicherheitstechnik in Volksdorf besteht …

**kassel**  
S: Kassel hat unter den Schlüsseldiensten eine Besonderheit: Neben den Notdiensten für Türöffnungen sitzen hier …  
H: Schlüsseldienste in Kassel haben neben den Notdiensten für Haus- und Wohnungstüren einen eigenen Schwerpunkt: …

**leipzig**  
S: Schlüsseldienste in Leipzig sind häufig Betriebe, die auch Schlosser- oder Metallbauarbeiten machen. Die Schlosserei …  
H: Leipzigs Schlüsseldienste sind zum Teil über Jahrzehnte gewachsen. LSS Leipzig GmbH nennt mehr als …

**nuernberg**  
S: Schlüsseldienste in Nürnberg fahren fast immer auch nach Fürth und Erlangen. Kurt Schlüsseldienst arbeitet …  
H: Nürnberger Schlüsseldienste arbeiten über die Stadtgrenze hinaus. Betriebe mit Sitz in Nürnberg fahren regelmäßig …

**salzgitter**  
S: In Salzgitter stützen sich die Schlüsseldienste auf einen Betrieb mit sehr vielen Bewertungen und …  
H: Schlüsseldienste in Salzgitter haben eine Besonderheit: Hinter dem Schlüsseldienst Salzgitter steht die Betriebs-Instandhaltungs-Technik, die …

**sankt-ingbert**  
S: Die Schlüsseldienste in Sankt Ingbert sind vor allem Fachgeschäfte. Schlüssel, Schlösser und Schließanlagen werden …  
H: Zwei Arten von Betrieb prägen die Schlüsseldienste in Sankt Ingbert im Saarland: das Fachgeschäft …

**strausberg**  
S: Wer in Strausberg einen Schlüsseldienst sucht, landet nicht nur bei Betrieben innerhalb der Stadtgrenze. …  
H: Schlüsseldienste in Strausberg in Brandenburg teilen sich in zwei Arbeitsweisen. Die einen fertigen Schlüssel: …

**villingen-schwenningen**  
S: Villingen-Schwenningen ist ein Ort mit gewachsenen Notdiensten. Die Schlüsseldienste hier sind zum großen Teil …  
H: Wer in Villingen-Schwenningen nachts vor einer verschlossenen Wohnungstür steht, findet hier Schlüsseldienste, die den …

**waren-mueritz**  
S: Die Schlüsseldienste in Waren (Müritz) arbeiten in der Region an der Seenplatte und verbinden …  
H: Die Schlüsseldienste in Waren (Müritz) in Mecklenburg-Vorpommern verbinden Schlüsselarbeit mit Sicherheitstechnik und Hausbetreuung. Schlüsseldienst-SICHERHEITSTECHNIK …
