---
title: Siegel-Programm
type: framework
status: stable
updated: 2026-11-03
---

# Siegel-Programm

Das Siegel ist die eigene Auszeichnung des Verzeichnisses. Es ersetzt die englische
„Verified"-Marke und ist der Grund, aus dem ein Betrieb anruft. Grundlage ist der Abschnitt
„Siegel-Programm" in [[konventionen]]; diese Seite ist die Ausführung.

## Zwei Stufen, streng getrennt

| Stufe | Preis | Was sie bedeutet | Spalte in der CSV |
|---|---|---|---|
| **Geprüft** | kostenlos | Der Betrieb hat die sechs Kriterien erfüllt und das Serviceversprechen unterschrieben | `geprueft` = `true`, `geprueft_jahr` = Jahr |
| **Sichtbarkeit** (Premium-Eintrag, Stadt-Premium, Top-Platzierung) | kostenpflichtig, siehe `templates/featured-tiers.md` | bessere Platzierung, Fotos, gefolgte Links | `premium`, `featured`, `best_of_rank` |

**Das Siegel ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit.** Dieser Satz steht wörtlich auf
`/siegel/` und auf `/premium/`. Ein zahlender Betrieb ohne erfüllte Kriterien bekommt kein
Siegel, ein geprüfter Betrieb ohne Zahlung behält es.

## Die sechs Prüfkriterien

Sie stehen vollständig und wörtlich auf `/siegel/`. Ein Siegel, dessen Kriterien nicht
veröffentlicht sind, ist angreifbar; deshalb ist die Veröffentlichung Pflicht und nicht
Kür.

1. vollständiges Impressum auf der eigenen Website des Betriebs
2. erreichbare Festnetz- oder Mobilnummer
3. Preisangabe oder Anfahrtspauschale auf der Website genannt
4. mindestens 10 Google-Bewertungen bei einem Schnitt von mindestens 4,0
5. keine Weiterleitung an ein Callcenter ohne Ortsbezug
6. unterschriebenes Serviceversprechen: Festpreis vor Arbeitsbeginn, keine versteckten
   Zuschläge, Rechnung mit vollständiger Firmenanschrift, zerstörungsfreie Öffnung als
   Standard

## Was das Siegel ausdrücklich nicht ist

Auf `/siegel/` steht in eigenen Sätzen:

- Grundlage sind **Selbstauskunft des Betriebs** sowie die Prüfung von **Unterlagen und
  Website** durch den Herausgeber.
- Es gibt **keinen Test vor Ort**, keine Probeöffnung, keinen Testkauf.
- Das Siegel trägt die **Jahreszahl**, gilt **ein Jahr** und muss jährlich erneuert werden.
- Es wird **entzogen**, wenn belegte Beschwerden über den Betrieb eingehen.
- Es ist keine Aussage einer amtlichen Stelle. Die Wörter „Innung", „Verband", „Kammer",
  „amtlich", „Verbraucherschutz" und „getestet" kommen in keinem sichtbaren Text vor
  ([[konventionen]], Sprache und Ton): sie würden den Eindruck erwecken, hinter dem Siegel
  stehe eine Behörde oder eine Standesorganisation.
- Schlüsseldienst ist in Deutschland kein zulassungspflichtiges Handwerk. Das Siegel sagt
  nichts über eine Lizenz, eine Zulassung oder eine Zertifizierung aus, weil es solche in
  diesem Gewerbe nicht gibt. Die Wörter „lizenziert", „zugelassen" und „zertifiziert" sind
  verboten.

## Arbeitsablauf

1. **Antrag.** Der Betrieb füllt den Fragebogen auf `/siegel/antrag/` aus: Firmendaten,
   Website, Telefonnummer, Preisangabe, Serviceversprechen zum Unterschreiben.
2. **Prüfung.** Der Herausgeber prüft **von Hand** gegen die sechs Kriterien: Impressum der
   Website, Telefonnummer anrufen, Preisangabe suchen, Bewertungen zählen, Callcenter-Weiter-
   leitung ausschließen, Serviceversprechen entgegennehmen. Keine Automatik, kein Skript
   entscheidet das.
3. **Eintragen.** Bei Erfolg: in `site/src/data/listings.csv` die Spalte `geprueft` auf
   `true` und `geprueft_jahr` auf das Jahr der Prüfung setzen. Bei Misserfolg: nichts setzen
   und dem Betrieb schreiben, welches Kriterium fehlt.
4. **Neu bauen.** Gate 5 erneut laufen lassen ([[master-template]]: nie eine erzeugte Seite
   von Hand bearbeiten).
5. **Ausliefern.** Gate 6 beziehungsweise der Redeploy.

Jährliche Erneuerung: einmal im Jahr werden alle Zeilen mit `geprueft_jahr` aus dem Vorjahr
durchgesehen. Wer nicht erneuert, verliert das Siegel; die Spalten werden geleert und das
Verzeichnis neu gebaut ([[refresh-and-upkeep]]).

## Der Verkaufsanlass

Jeder Eintrag zeigt eines von zwei Zeichen, immer, auf jeder Eintragsseite und auf jeder
Karte in der Stadtliste:

- geprüft: **„Geprüft 2026"**, verlinkt auf `/siegel/`
- nicht geprüft: **„Noch nicht geprüft"**, verlinkt auf `/siegel/antrag/`

„Noch nicht geprüft" ist der Grund für den Anruf und **darf nicht abgeschaltet werden**. Kein
Gate, keine Einstellung und kein Wunsch eines Betriebs entfernt dieses Zeichen. Es ist sachlich
richtig (der Betrieb hat keinen Antrag gestellt) und es ist der Einstieg in jedes Gespräch:
der Betrieb kann es kostenlos loswerden, indem er den Antrag stellt, und beim selben Anruf
wird über Sichtbarkeit gesprochen.

## Seiten und Adressen

| Seite | Adresse | Robots |
|---|---|---|
| Kriterien und was das Siegel nicht ist | `/siegel/` | indexiert |
| Antragsformular | `/siegel/antrag/` | `noindex` |
| Nachweisseite je ausgezeichneter Betrieb | `/auszeichnung/[slug]/` | `noindex` |
| Siegelbild zum Einbinden | `/auszeichnung/[slug].svg` | – |

`/siegel/` ist die indexierte Seite des Programms: dort stehen die Kriterien, und dorthin
verlinkt jedes Siegel. Das Antragsformular ist eine Formularseite und startet wie alle
Formular- und Pflichtseiten mit `noindex`, aus der Sitemap heraus ([[launch-lean]]); erreichbar
ist es über jeden Eintrag mit „Noch nicht geprüft" und über `/siegel/`.

Das Siegel wird als HTML-Schnipsel weitergegeben, nie als Bilddatei, damit der Link auf die
Eintragsseite entsteht ([[authority-and-links]], `templates/featured-tiers.md`).

## Siehe auch
[[konventionen]] · [[monetization-slots]] · [[page-types]] · [[refresh-and-upkeep]] · [[authority-and-links]]
