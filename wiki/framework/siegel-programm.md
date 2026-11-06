---
title: Festpreis-Garantie
type: framework
status: stable
updated: 2026-11-03
---

# Festpreis-Garantie

Diese Datei heißt weiter `siegel-programm.md`, weil das Programm bis zum 2026-11-03 so hieß und
jeder Wikilink `[[siegel-programm]]` halten soll; der Inhalt beschreibt die Festpreis-Garantie.

Die Festpreis-Garantie ist die eigene Auszeichnung des Verzeichnisses. Sie ersetzt die
englische „Verified"-Marke und ist der Grund, aus dem ein Betrieb anruft. Grundlage ist der
Abschnitt „Festpreis-Garantie" in [[konventionen]]; diese Seite ist die Ausführung. Der interne
Name des Programms ist „Garantie-Programm", der Antrag heißt „Garantie-Antrag", der Schnipsel
für die Website des Betriebs „Garantie-Nachweis".

## Warum eine Garantie und kein Zeichen

Ein Prüfzeichen beschreibt eine Eigenschaft des Betriebs. Eine Garantie ist ein Versprechen an
den Kunden, und nur das Zweite bringt dem Betrieb Kunden. Der Unterschied liegt in drei
Dingen, die ein einzelner Betrieb nicht nachbauen kann: Der Preis steht **öffentlich**, **vor
dem Anruf**, **bei einem Dritten**, und dieser Dritte nimmt ihn bei einem Verstoß wieder weg.
Ein Betrieb kann auf seiner eigenen Website jeden Preis nennen und morgen ändern; im
Verzeichnis steht der Preis bei jemandem, der nicht der Betrieb ist, und er verschwindet, sobald
eine Rechnung darüber liegt. Deshalb ist die Festpreis-Garantie das Verkaufsargument des
Betriebs und nicht nur ein Etikett des Verzeichnisses.

## Die drei Teile

Ohne einen davon ist die Garantie nur ein Etikett:

1. **Der Preis steht im Eintrag, bevor der Kunde anruft.** Jeder Betrieb mit Garantie
   veröffentlicht seine Preise, getrennt nach Dienstleistung und Material. Die **Dienstleistung**
   ist die Türöffnung, nicht der Gesamtbetrag: ein **Grundpreis** (werktags 7–20 Uhr) und zwei
   benannte **Zuschläge** – abends/Wochenende/Feiertag (werktags 20–24 Uhr sowie Sa/So/Feiertag
   7–24 Uhr) und nachts (täglich 0–7 Uhr) – dazu die Anfahrt. Die Fenster überschneiden sich
   nicht: **Grundpreis plus höchstens ein Zuschlag, Zuschläge werden nicht addiert.** Sie gelten
   für die zugefallene wie die abgeschlossene Tür. Bei der **abgeschlossenen Tür** kommt das
   **Material** dazu, nach fester Regel: Standardzylinder zu festem Betrag, je 5 mm Mehrlänge ein
   fester Aufschlag. Eine **defekte Tür** hat keinen Festpreis, sondern einen Ab-Preis, der vor
   Arbeitsbeginn beziffert wird. Alle Zahlen stehen im Eintrag, auf der Stadtkarte (nur der
   Grundpreis als Ab-Preis) und im Garantie-Nachweis. Spalten: `garantie_tag` (Grundpreis),
   `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt` (Dienstleistung) und
   `garantie_zylinder`, `garantie_zylinder_5mm` (Material) als Euro-Beträge, ganze Zahl ohne
   Einheit; `garantie_anfahrt` = `0` heißt „im Preis enthalten". Das alte `garantie_nacht` ist
   stillgelegt (der Build bricht bei gefüllter Zelle ab).
   Spalte `geprueft` = `true` heißt „Garantie aktiv", `geprueft_jahr` = Jahr der Prüfung. Die
   Spaltennamen bleiben aus Rücksicht auf den Code.
2. **Der Betrieb garantiert: Der genannte Preis ist der Rechnungspreis.** Das ist das
   unterschriebene Serviceversprechen. Die Garantie gibt der Betrieb, nicht der Herausgeber; der
   Herausgeber prüft die Voraussetzungen und überwacht die Einhaltung. Das steht so auf
   `/festpreis-garantie/`.
3. **Verstoß hat Folgen.** Rechnung über dem garantierten Preis → Kunde meldet es mit Rechnung
   → Herausgeber konfrontiert den Betrieb → Garantie entzogen, Preise aus dem Eintrag entfernt.
   Der Weg zur Meldung steht auf `/festpreis-garantie/` und im Eintrag.

## Warum das Material zwei feste Spalten hat, kein Freitext

Entschieden 2026-11-05: `garantie_zylinder` und `garantie_zylinder_5mm` sind feste Zahlen, keine
Freitext-Staffel. Vergleichbarkeit ist der Zweck des Verzeichnisses; Materialpreise lassen sich
nur vergleichen, wenn alle Betriebe sie gleich ausdrücken. Dass ein Betrieb seine Staffel in das
Format „Standardzylinder + Aufschlag je 5 mm" bringen muss, ist eine Anforderung des Siegels, kein
Mangel. Auf `/festpreis-garantie/antrag/` ist deshalb erklärt, wie die beiden Zahlen gemeint sind.
Zeigen echte Anträge später, dass Betriebe ernsthaft anders staffeln, wird eine Ausnahmespalte
geprüft – nicht jetzt. Die defekte Tür bekommt bewusst keine Spalte: sie ist kein veröffentlichter
Festpreis, sondern der „vor Arbeitsbeginn beziffert"-Fall des Serviceversprechens.

## Zwei Stufen, streng getrennt

| Stufe | Preis | Was sie bedeutet | Spalten in der CSV |
|---|---|---|---|
| **Festpreis-Garantie** | kostenlos | Der Betrieb hat die sechs Voraussetzungen erfüllt, seine Preise verbindlich genannt (Grundpreis, zwei Zuschläge, Anfahrt, zwei Material) und das Serviceversprechen unterschrieben | `geprueft` = `true`, `geprueft_jahr` = Jahr, `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt`, `garantie_zylinder`, `garantie_zylinder_5mm` |
| **Premium / Top-Platzierung** (Premium-Eintrag, Stadt-Premium, Top-Platzierung) | kostenpflichtig, siehe `templates/featured-tiers.md` | bessere Platzierung, Fotos, gefolgte Links | `premium`, `featured`, `best_of_rank` |

**Die Garantie ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit.** Dieser Satz steht wörtlich
auf `/festpreis-garantie/` und auf `/premium/`. Ein zahlender Betrieb ohne erfüllte
Voraussetzungen bekommt keine Garantie, ein Betrieb mit Garantie ohne Zahlung behält sie.

## Die sechs Voraussetzungen

Sie stehen vollständig und wörtlich auf `/festpreis-garantie/`. Eine Garantie, deren
Voraussetzungen nicht veröffentlicht sind, ist angreifbar; deshalb ist die Veröffentlichung
Pflicht und nicht Kür. Wortlaut wie in [[konventionen]]:

- vollständiges Impressum auf der eigenen Website
- eine Telefonnummer, unter der der Betrieb erreichbar ist und bei der Prüfung tatsächlich
  abgehoben hat; die Nummer wird vor der Erteilung angerufen
- die Preise verbindlich genannt: der Grundpreis der Türöffnung (werktags 7–20 Uhr), die beiden
  benannten Zuschläge (abends/Wochenende/Feiertag sowie nachts 0–7 Uhr, nicht kumulativ) und die
  Anfahrt; und – für die abgeschlossene Tür – die beiden Materialpreise (Standardzylinder,
  Aufschlag je 5 mm Mehrlänge)
- liegen mindestens 5 Google-Bewertungen vor, beträgt der Schnitt mindestens 4,0; liegen weniger
  oder keine vor, entscheiden die übrigen Voraussetzungen (die Garantie sagt etwas über
  Preissicherheit, nicht über Bekanntheit; eine Mindestzahl schlösse neue und profillose Betriebe
  aus, der Riegel nach unten bleibt)
- keine Weiterleitung an ein Callcenter ohne Ortsbezug
- unterschriebenes Serviceversprechen (fünf Zusagen): der Grundpreis und die genannten Zuschläge
  sind der Preis auf der Rechnung, höchstens ein Zuschlag je Einsatz und nie addiert (zugefallene
  wie abgeschlossene Tür); außer den genannten Zuschlägen keine weiteren; bei der abgeschlossenen
  Tür kommt nur das genannte Material dazu; defekte Türen werden vor
  Arbeitsbeginn beziffert; Rechnung mit vollständiger Firmenanschrift; zerstörungsfreie Öffnung
  als Standard

## Was die Garantie ausdrücklich nicht ist

Auf `/festpreis-garantie/` steht in eigenen Sätzen:

- Grundlage sind **Selbstauskunft des Betriebs** sowie die Prüfung von **Unterlagen und
  Website** durch den Herausgeber.
- Es gibt **keinen Test vor Ort**, keine Probeöffnung, keinen Testkauf.
- Sie trifft **keine Aussage über Bekanntheit oder Bewertungsmenge**. Ein Betrieb ohne oder mit
  wenigen Google-Bewertungen kann die Garantie führen, wenn er die übrigen Voraussetzungen
  erfüllt; die Garantie bewertet Preissicherheit, nicht Reichweite.
- **Die Garantie gibt der Betrieb**, nicht der Herausgeber. Der Herausgeber prüft die
  Voraussetzungen, veröffentlicht die Preise und entzieht die Garantie bei belegten Verstößen.
- Die Garantie trägt die **Jahreszahl**, gilt **ein Jahr** und muss jährlich erneuert werden.
- Sie wird **entzogen**, wenn ein belegter Verstoß eingeht (siehe unten).
- Sie ist keine Aussage einer amtlichen Stelle. Die Wörter „Innung", „Verband", „Kammer",
  „amtlich", „Verbraucherschutz" und „getestet" kommen in keinem sichtbaren Text vor
  ([[konventionen]], Sprache und Ton): sie würden den Eindruck erwecken, hinter der Garantie
  stehe eine Behörde oder eine Standesorganisation.
- Schlüsseldienst ist in Deutschland kein zulassungspflichtiges Handwerk. Die Garantie sagt
  nichts über eine Lizenz, eine Zulassung oder eine Zertifizierung aus, weil es solche in
  diesem Gewerbe nicht gibt. Die Wörter „lizenziert", „zugelassen" und „zertifiziert" sind
  verboten.

## Arbeitsablauf

1. **Antrag.** Der Betrieb füllt den Garantie-Antrag auf `/festpreis-garantie/antrag/` aus
   (`templates/claim-form.html`): Firmendaten, Website, Impressum, Telefonnummer,
   Google-Profil, **die Preise** – für die Dienstleistung der Grundpreis (werktags 7–20 Uhr), die
   beiden Zuschläge (abends/Wochenende/Feiertag; nachts 0–7 Uhr) und die Anfahrt (`0` = enthalten),
   und zwei für das Material (Standardzylinder, Aufschlag je 5 mm Mehrlänge) – sonstige Zuschläge,
   das Serviceversprechen zum Unterschreiben.
2. **Prüfung.** Der Herausgeber prüft **von Hand** gegen die sechs Voraussetzungen: Impressum
   der Website, Telefonnummer anrufen, Bewertungen zählen, Callcenter-Weiterleitung
   ausschließen, Preise auf Vollständigkeit und Plausibilität lesen, Serviceversprechen
   entgegennehmen. Keine Automatik, kein Skript entscheidet das.
3. **Eintragen.** Bei Erfolg: in `site/src/data/listings.csv` die Spalten `geprueft` = `true`,
   `geprueft_jahr` = Jahr der Prüfung, `garantie_tag`, `garantie_zuschlag_abend`,
   `garantie_zuschlag_nacht`, `garantie_anfahrt` (Dienstleistung) sowie `garantie_zylinder` und
   `garantie_zylinder_5mm` (Material) = die genannten Beträge setzen. Bei Misserfolg: nichts setzen und dem Betrieb schreiben, welche
   Voraussetzung fehlt.
4. **Neu bauen.** Gate 5 erneut laufen lassen ([[master-template]]: nie eine erzeugte Seite
   von Hand bearbeiten).
5. **Ausliefern.** Gate 6 beziehungsweise der Redeploy.

## Entzug

1. **Meldung.** Ein Kunde meldet eine Rechnung über dem garantierten Preis und legt die
   Rechnung bei. Ohne Rechnung gibt es keinen Entzug; eine Behauptung allein reicht nicht.
2. **Konfrontation.** Der Herausgeber legt dem Betrieb die Rechnung vor und hört ihn an.
3. **Entzug.** Bleibt der Verstoß belegt, wird die Garantie entzogen: `geprueft`,
   `geprueft_jahr`, `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`,
   `garantie_anfahrt`, `garantie_zylinder` und `garantie_zylinder_5mm` werden geleert.
4. **Preise raus.** Gate 5 erneut laufen lassen und ausliefern. Der Eintrag trägt wieder „Noch
   keine Festpreis-Garantie".

Der Weg zur Meldung steht auf `/festpreis-garantie/` und in jedem Eintrag mit Garantie.

## Jährliche Erneuerung

Die Garantie trägt die Jahreszahl und gilt ein Jahr. Einmal im Jahr werden alle Zeilen mit
`geprueft_jahr` aus dem Vorjahr durchgesehen, und jeder Betrieb wird angerufen: Gelten die drei
Preise noch, gilt das Serviceversprechen noch? Das ist ein Anrufgrund mit einem echten Anlass,
und im selben Gespräch geht es um Sichtbarkeit. Wer erneuert, bekommt das neue Jahr und
gegebenenfalls neue Preise eingetragen; wer nicht erneuert, verliert die Garantie, die sieben
Garantiespalten (`geprueft`, `geprueft_jahr`, die vier Dienstleistungsspalten – Grundpreis, zwei
Zuschläge, Anfahrt – und die zwei Materialspalten) werden geleert und das Verzeichnis neu gebaut
([[refresh-and-upkeep]]).

## Der Verkaufsanlass

Jeder Eintrag zeigt eines von zwei Zeichen, immer, auf jeder Eintragsseite und auf jeder Karte
in der Stadtliste:

- mit Garantie: **„Festpreis-Garantie 2026"** mit ihren Preisen (Grundpreis, Zuschläge, Material), verlinkt auf
  `/festpreis-garantie/`; auf der Stadtkarte als Zeile „Festpreis-Garantie · Türöffnung ab
  <garantie_tag> €"
- ohne Garantie: **„Noch keine Festpreis-Garantie"**, verlinkt auf
  `/festpreis-garantie/antrag/`

„Noch keine Festpreis-Garantie" ist der Grund für den Anruf und **darf nicht abgeschaltet
werden**. Kein Gate, keine Einstellung und kein Wunsch eines Betriebs entfernt dieses Zeichen.
Es ist sachlich richtig (der Betrieb hat keinen Antrag gestellt), es unterstellt dem Betrieb
nichts, und es ist der Einstieg in jedes Gespräch: der Betrieb kann es kostenlos loswerden,
indem er den Antrag stellt, und beim selben Anruf wird über Sichtbarkeit gesprochen.

Die Garantie verändert die Reihenfolge nicht: Sortierung bleibt bezahlte Plätze, dann
Bewertung ([[monetization-slots]]).

## Seiten und Adressen

| Seite | Adresse | Robots |
|---|---|---|
| Erklärung, Voraussetzungen und was die Garantie nicht ist | `/festpreis-garantie/` | indexiert |
| Garantie-Antrag | `/festpreis-garantie/antrag/` | `noindex` |
| Nachweisseite je Betrieb mit Garantie | `/auszeichnung/[slug]/` | `noindex` |
| Bild des Garantie-Nachweises zum Einbinden | `/auszeichnung/[slug].svg` | – |

`/festpreis-garantie/` ist die indexierte Seite des Programms: dort stehen die
Voraussetzungen, und dorthin verlinkt jedes Garantie-Zeichen. Das Antragsformular ist eine
Formularseite und startet wie alle Formular- und Pflichtseiten mit `noindex`, aus der Sitemap
heraus ([[launch-lean]]); erreichbar ist es über jeden Eintrag mit „Noch keine
Festpreis-Garantie" und über `/festpreis-garantie/`.

Der Garantie-Nachweis wird als HTML-Schnipsel weitergegeben, nie als Bilddatei, damit der Link
auf die Eintragsseite entsteht: Bild `/auszeichnung/[slug].svg`, Text „Festpreis-Garantie
2026 · Türöffnung ab <garantie_tag> €" ([[authority-and-links]], `templates/featured-tiers.md`).
Er ist kostenlos und gehört zu keiner Stufe.

## Reserviert, nicht gebaut: Stufe „Preisschutz"

Erstattung der Differenz bis 100 € durch den Herausgeber, Rückgriff auf den Betrieb. Die
Spalte `preisschutz` wird von `scripts/clean_listings.py` leer angelegt und von
`scripts/merge_enriched.py` durchgereicht, aber **kein Skript und keine Seite wertet sie aus**,
bis der Betreiber die Stufe freigibt. Bis dahin steht sie weder auf `/festpreis-garantie/`
noch auf `/premium/` noch in einem Entwurf des Mail-Workers.

## Siehe auch
[[konventionen]] · [[monetization-slots]] · [[page-types]] · [[refresh-and-upkeep]] · [[authority-and-links]]
