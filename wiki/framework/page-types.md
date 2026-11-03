---
title: Seitentypen und Pflichtinhalte
type: framework
status: current
updated: 2026-11-03
---

# Seitentypen und Pflichtinhalte

| Seite | Zweck | Pflichtinhalte und Untergrenzen |
|---|---|---|
| **Startseite** | Bundesweite Antwort auf „Schlüsseldienst" | **800 bis 1.500 Wörter wie gebaut** (geprüft an `dist/index.html`, [[copy-gate]]): was das Verzeichnis ist, wie geprüft wird, **Raster aller Bundesländer** mit Zahl der Einträge und Städte, Raster der 20 größten Städte, Block der Premium-Plätze, „So erkennen Sie einen seriösen Schlüsseldienst" (der Ratgeberblock, 400 bis 600 Wörter), Fragenblock (5 bis 8), Hinweise auf Beanspruchen, Premium und Siegel. Der Aufbau des Templates allein (Länderkarten, Städtekarten, Zahlenreihe, Suchfeldbeschriftungen, Prüfschritte) ergibt im gebauten Zustand etwa 350 Wörter; der geschriebene Text sind etwa 800 bis 1.200. |
| **Blätterseite** | Alles auf einer Seite | `/verzeichnis/`, `noindex, follow`. Suchfeld, alle Bundesländer, alle Städte von A bis Z, alle Einträge nach Stadt. **Kein Text der Startseite**, damit die beiden nicht konkurrieren. Keine Wortuntergrenze. |
| **Bundesland-Seite** | Vollständiger Städte-Index eines Landes, Antwort auf „Schlüsseldienst [Bundesland]" | **300 bis 500 Wörter** Einleitung über das Land in Bezug auf das Gewerbe (Ballungsräume und Flächenkreise, was die Betriebe dort nach ihren eigenen Angaben schwerpunktmäßig machen, die Handwerkskammerbezirke wenn die Faktensammlung sie nennt), dann **jede Stadt des Landes mit ihrer Zahl**, „Kleinere Orte" (die von `foldMaxKm` freigestellten Ortsseiten), Block der Premium-Plätze, Fragenblock (**3 bis 5**), Hinweis aufs Beanspruchen, Links auf die Nachbar-Bundesländer. Ein Bundesland bekommt eine Seite, sobald es mindestens eine Stadtseite trägt. Das Wortband gilt erst, wenn Gate 5 den Einleitungstext geschrieben hat: ohne ihn trägt die Seite nur Kopf, Städteliste und Fragen ([[copy-gate]]). |
| **Stadtseite** | Die Geldseite: „Schlüsseldienst [Stadt]" | **500 bis 800 Wörter** echter Ortstext (keine Schablone mit getauschtem Stadtnamen): was bei einer Türöffnung in **dieser** Stadt zählt, dann die Einträge als Karten (Premium-Plätze zuerst, dann die bezahlten Top-Platzierungen, dann nach Bewertung × Zahl der Bewertungen; die Stadtseite **ist** die Liste „Die besten Schlüsseldienste in [Stadt]", [[monetization-slots]]), dann ein **Fragenblock von 4 bis 6 Fragen** aus den Merkmalsdaten, als sichtbarer Text, nie zum Aufklappen, dann die Nachbarstädte und der Hinweis aufs Beanspruchen. Mindestens **3 Einträge** für eine eigene Seite. |
| **Eintragsseite** | Ein Betrieb | Name, Anschrift, Telefonnummer im deutschen Format, Öffnungszeiten, Bewertung und Zahl der Bewertungen, das Merkmalsraster (wahr und falsch als Felder, die „keine Angabe" zu einer gedämpften Zeile zusammengefasst), die angereicherte Beschreibung (120 bis 200 Wörter), **das Siegelzeichen: „Geprüft [Jahr]" mit Link auf `/siegel/` oder „Noch nicht geprüft" mit Link auf `/siegel/antrag/`** ([[siegel-programm]], nicht abschaltbar), Kartenplatzhalter (lädt erst nach Klick), Website-Link (`nofollow`, außer bei bezahlter Stufe), Links auf die Leistungsseiten, „Weitere Schlüsseldienste in [Stadt]" mit vier Einträgen derselben Stadt, „Ist das Ihr Betrieb? Eintrag beanspruchen", eine Zeile Hinweis: Daten aus öffentlichen Quellen, keine Empfehlung, **kein Hinweis auf eine zu prüfende Lizenz** – es gibt keine. Zwei Zustände: **einfach** (nicht beansprucht: keine Fotos, keine Profillinks) und **ausgebaut** (beansprucht mit Premium oder bezahlter Stufe: Fotos vom Inhaber, alle Links gefolgt, Karte nach Klick, Öffnungszeiten, Siegelbild). Seiten mit weniger als 5 Bewertungen **oder** ohne Beschreibung sind **dünn** und starten mit `noindex` ([[launch-lean]]). |
| **Leistungsseite** | Bundesweite Antwort auf „[Leistung] Schlüsseldienst" | `/leistungen/[slug]/`, gebaut je Merkmal mit `service`-Block in `attributes.json`, das mindestens so viele Einträge bestätigen wie die Stadt-Mindestzahl. H1 „[Leistung] in Deutschland", Kernzahlen (Anzahl, Städte, Datum), Einleitung von **80 bis 200 Wörtern** aus den Daten und der Faktensammlung (geprüft an der gebauten Seite mit 140 bis 270 Wörtern, weil der Aufbau allein etwa 60 ergibt), die besten Einträge als Karten, dann **jedes Bundesland mit seiner bestätigten Zahl**, verlinkt auf die Bundesland-Seite, dann die übrigen Leistungen. Welche Merkmale eine Seite bekommen, entscheidet der Mensch in Gate 4: nur etwas, wonach als Leistung gesucht wird, **nie ein Vertrauenszeichen und nie eine Lizenz**. |
| **Eintrag beanspruchen** | Umwandlung | Unter 300 Wörtern. Das Formular aus `templates/claim-form.html`. Was das Beanspruchen bringt (Daten ändern, Fotos hinzufügen), was es kostet (nichts), und der Hinweis auf das kostenlose Siegel. |
| **Premium / Werbung** | Umwandlung | Unter 400 Wörtern. Die Stufen aus `templates/featured-tiers.md` mit Preisen in Euro, was jede Stufe bringt, Stripe-Schaltflächen, die Knappheitsregel („je Stadt und Stufe ein Betrieb") und **der Satz „Das Siegel ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit."** ([[siegel-programm]]). |
| **Siegel-Kriterien** | Vertrauen, Pflichtveröffentlichung | `/siegel/`. Die sechs Prüfkriterien vollständig, was das Siegel **nicht** ist (Selbstauskunft und Unterlagenprüfung, kein Test vor Ort), Jahreszahl und jährliche Erneuerung, Entzug bei belegten Beschwerden, der Satz zur Nichtkäuflichkeit, der Weg zum Antrag. **700 bis 1.200 Wörter**: sechs Kriterien, vollständiges Serviceversprechen und Aufklärung über die Rechtslage sind drei Pflichtteile, die zusammen unter 700 Wörtern nur mit Auslassung hineinpassen ([[copy-gate]]). Wortlaut und Umfang: [[siegel-programm]]. |
| **Siegel-Antrag** | Umwandlung | `/siegel/antrag/`. Der Fragebogen zu den sechs Kriterien und das Serviceversprechen zum Unterschreiben. Unter 300 Wörtern Begleittext. Ziel jedes „Noch nicht geprüft". |
| **Siegel-Nachweis** | Nachweis für den Betrieb | `/auszeichnung/[slug]/`, `noindex`. Welcher Betrieb, welches Jahr, welche Kriterien erfüllt, Link auf `/siegel/` und auf die Eintragsseite, dazu das HTML-Schnipsel zum Kopieren. |
| **Über uns** | Vertrauen für den Anruf | Der Herausgeber im Mittelpunkt: DOM Holding GmbH und der Geschäftsführer mit Bild und Lebenslauf, warum es dieses Verzeichnis gibt, wie geprüft wird, der Korrektur- und Löschweg ([[publisher-entity]], [[refresh-and-upkeep]]). 300 bis 500 Wörter. Gibt `Organization` und `Person` als Schema aus. |
| **Kontakt** | Erreichbarkeit | Echte E-Mail-Adresse und der Weg für Korrektur und Löschung ([[refresh-and-upkeep]]). |
| **Impressum** | **Pflicht, § 5 DDG** | Firma, Rechtsform, Anschrift, Geschäftsführer, Handelsregister und -nummer, Umsatzsteuer-Identifikationsnummer falls vorhanden, Telefonnummer und E-Mail-Adresse, Verantwortlicher für den Inhalt. Aus den Herausgeberdaten in `site.json` erzeugt. **Ein Platzhalter macht den Build unfertig.** |
| **Datenschutz** | **Pflicht, Art. 13 DSGVO** | Verantwortlicher, Zwecke und Rechtsgrundlagen, Empfänger (Cloudflare als Hoster), Speicherdauer, Rechte der Betroffenen, Beschwerderecht bei der Aufsichtsbehörde, Herkunft der Firmendaten und Bewertungen, Widerspruchsrecht, der Weg zur Korrektur oder Löschung eines Eintrags, der Hinweis auf die Karte erst nach Klick. **Ein Platzhalter macht den Build unfertig.** |
| **AGB** | Pflicht für die bezahlten Stufen | Leistungsbeschreibung der Stufen, Laufzeit, Kündigung, Preise in Euro, Widerrufsrecht. |
| **Ratgeberseite** | Links | `/ratgeber/[slug]/`. Die ausführlichste Seite zu einem Thema: Notfallnummern, was die Verbraucherzentrale zu überhöhten Rechnungen sagt, was die polizeiliche Kriminalprävention zum Einbruchschutz empfiehlt, jeweils mit Quelle. 1.200 Wörter oder mehr, mit Verfasserzeile und Datum. Wird nur gebaut, wenn der Betreiber das Thema nennt ([[authority-and-links]]). |

Das Wiki sagt, welche Seiten und Angaben Pflicht sind. Es ist **keine Rechtsberatung**; die
Endfassung von Impressum, Datenschutzerklärung und AGB sollte ein Anwalt prüfen, und
`05-build-report.md` schreibt das hin.

## Wortuntergrenze der Stadtseite nach Größe

Eine Seite mit drei Einträgen trägt keine 500 ehrlichen Wörter. Die Klassen (aus dem
englischen Pilotprojekt übernommen, von beiden Prüfern angewandt: `lint_copy.py --city-sizes`
aus den Eintragszahlen, `check_city_copy.py` aus der Bandzeile des Pakets, beide über
`lint_copy.faq_band`):

| Einträge auf der Seite | Wörter | Fragen |
|---|---|---|
| 10 oder mehr | 500 bis 800 | 4 bis 6 |
| 5 bis 9 | 380 bis 800 | 4 bis 6 |
| 3 oder 4 | 250 bis 800 | 4 bis 6 |
| 1 oder 2 (Ortsseite, von `foldMaxKm` freigestellt) | 120 bis 800 | 2 bis 6 |

Die Obergrenze bleibt 800. `lint_copy.py` kennzeichnet jede kleine Stadt im Bericht,
`make_city_packets.py` schreibt das Band auf jedes Paket.

## Stadttext handelt vom Ort

- **Thema: die Stadt in Bezug auf das Gewerbe.** Schreibe darüber, wie man sich in *diesem*
  Ort ausgeschlossen findet und wieder hineinkommt: welche Stadtteile die Betriebe bedienen,
  welche Arbeiten das örtliche Gewerbe schwerpunktmäßig anbietet (Türöffnung, Schließanlagen,
  Einbruchschutz, Autoschlüssel), welche Nachbarorte die Seite mitträgt, der Landkreis und
  sein Gewerbeamt wenn die Faktensammlung ihn nennt, der Gebäudebestand (Altbau mit
  Buntbartschlössern, Neubaugebiete mit Schließanlagen) wenn eine belegte Tatsache das sagt.
  Ein Leser aus dieser Stadt soll sie erkennen; ein Leser aus der Nachbarstadt soll den
  Unterschied merken.
- **Einmalig für den Ort.** Kein Satz darf mit getauschtem Stadtnamen auch stimmen. Die
  Prüfung auf geteilte Sätze in `check_city_copy.py` setzt den Buchstaben dieser Regel durch,
  der Schreiber ihren Sinn.
- **Nur mit Quelle.** Jede Ortsaussage kommt aus dem Paket (Einsatzgebiete, Orte, Landkreise
  und Schwerpunkte, die die Betriebe selbst nennen) oder aus einer belegten Faktensammlung
  (`05-fact-sheet.md`, bei vielen Städten `05-city-facts.json`). Quellen und ihre Reihenfolge
  in [[konventionen]]. Ohne Quelle wird eine Ortstatsache nicht geschrieben. Ein kurzer
  ehrlicher Text schlägt einen erfundenen; dafür sind die Untergrenzen nach Größe da.
- **Preise niemals.** Der Export trägt keine Preise, und überhöhte Rechnungen sind in diesem
  Gewerbe das Hauptthema der Verbraucherzentralen. Kein Stadttext nennt einen Preis, eine
  Preisspanne oder eine Anfahrtspauschale in Euro, auch keine Spanne „ab", es sei denn die
  Faktensammlung belegt sie mit einer amtlichen Quelle und nennt sie als deren Angabe. Eine
  Stadt benutzt höchstens einen Punkt aus der Faktensammlung.
- **Nie „lizenziert", „zugelassen", „zertifiziert", „geprüfter Meisterbetrieb".** Das Gewerbe
  ist nicht zulassungspflichtig, es gibt keine Lizenz und keine Meisterpflicht
  ([[konventionen]]). Ebenso nie „Innung", „Verband", „Kammer", „amtlich",
  „Verbraucherschutz", „getestet": sie erwecken den Eindruck, hinter dem Verzeichnis stehe
  eine amtliche Stelle oder eine Standesorganisation.
- **Der Leser erfährt nie, wie das Verzeichnis gemacht wurde.** Kein „das Paket", kein
  „Merkmal", keine Fehlercodes einer Website, nichts über Suchmaschinen. Beide Prüfer lassen
  das scheitern.
- **Nie geschrieben:** Zählungen dessen, was Einträge „angeben", „nennen" oder „erwähnen";
  Zahlen von Einträgen „ohne Angabe"; ob eine Website geladen hat; „das Verzeichnis hat das
  nicht geprüft"; wie die Seite geordnet ist; die Wörter „Eintrag" und „Einträge" als Subjekt
  eines Satzes. Betriebe werden dafür genannt, was sie in der Stadt tun.
- **Zahlen sparsam.** Die Zahl auf der Seite, die Bewertung und Bewertungszahl eines genannten
  Betriebs wo sie dem Leser etwas sagt, die Nachbarorte. Keine Volkszählung der Merkmale.
- **Häufige Fragen** folgen derselben Regel: Fragen, die jemand aus diesem Ort stellt (wer
  macht hier nachts auf, wer fährt in die Außenbezirke, wer baut auch Schließanlagen ein,
  welche Nachbarorte haben eine eigene Seite), beantwortet aus Paket und Faktensammlung, nie
  „wie viele Einträge nennen X".

## Textregeln

- Sachlich, auf Augenhöhe, Sie-Anrede, keine Werbesprache, **keine Gedankenstriche**
  (Hausregel).
- Jede Zahl auf einer Seite kommt aus den Daten. Keine erfundenen Kundenstimmen, keine
  erfundenen Siegel. „Keine Angabe" ist ein zulässiger Merkmalswert und wird so angezeigt.
- Ein H1 je Seite. H1 der Stadtseite: „Schlüsseldienst in [Stadt]". H1 der Bundesland-Seite:
  „Schlüsseldienst in [Bundesland]".
- Tatsachen stehen als sichtbarer Text. Keine Auf- und Zuklapper, keine Reiter, kein
  „mehr lesen" für Fragen, Öffnungszeiten oder Merkmale.

## Bilder

- Einträge ohne Beanspruchung tragen **keine Fotos**. Google-Fotos dürfen nicht eingebunden
  werden, und ein Foto vom Profil eines Betriebs zu übernehmen ist ein urheberrechtliches
  Risiko, das der Betreiber trägt.
- Fotos kommen mit der Beanspruchung oder einer bezahlten Stufe, vom Inhaber geliefert. Diese
  Lücke ist Teil des Verkaufsgesprächs.
- Startseite, Bundesland- und Stadtseiten verwenden eigene oder lizenzierte Bilder, nie
  Eintragsfotos.
- Keine externe Schrift und kein externes Bild ohne Einwilligung ([[konventionen]]).

## Siehe auch
[[konventionen]] · [[site-architecture]] · [[siegel-programm]] · [[enrichment]] · [[page-sections]] · [[monetization-slots]]
