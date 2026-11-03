---
title: Pflege: wie ein statisches Verzeichnis lebendig bleibt
type: framework
status: current
updated: 2026-11-03
---

# Pflege: wie ein statisches Verzeichnis lebendig bleibt

Ein Verzeichnis macht nach dem Start mehr Arbeit als eine einzelne Website: Inhaber wollen
ihren Eintrag ändern, und Spam will hinein. Der statische Neubau löst beides ohne Zugänge und
ohne Redaktionssystem. Eintragsdaten ändern sich, wenn eine Beanspruchung, ein Verkauf, eine
Siegelprüfung oder eine Korrektur sie ändert, nicht nach Kalender.

## Keine Zugänge. Zwei Türen.

- Betriebe bekommen **keine Konten** in Fassung 1. Auf gewachsenen Verzeichnissen überholten
  Spam-Anmeldungen die echten, und die Betreiber haben alle Zugänge wieder abgeschaltet.
- Hinein führen genau zwei Formulare:
  - `/eintrag-beanspruchen/` – Daten ändern, Fotos nachliefern
  - `/siegel/antrag/` – die Prüfung gegen die sechs Kriterien ([[siegel-programm]])
- **Jede Einsendung wird von Hand geprüft**, bevor sich etwas ändert: ein echter örtlicher
  Betrieb (kein Anfragenvermittler, kein Verzeichnis, kein Callcenter), die E-Mail-Domain
  passt zur Website, die Telefonnummer passt zur Google-Zeile. Dann die CSV ändern und neu
  bauen.
- Jede Selbstanmeldung ist ein warmer Kontakt. Am selben Tag anrufen
  ([[monetization-slots]]).

## Neu bauen bei Änderung

- Beanspruchter Eintrag, verkaufter Platz, korrigierte Telefonnummer, neue Stadt, neu
  erteiltes oder entzogenes Siegel: CSV ändern, Gate 5 erneut laufen lassen, erneut
  ausliefern. **Nie eine erzeugte Seite von Hand bearbeiten.**
- Die CSV bleibt im Projekt. Die Versionsgeschichte ist der Nachweis, wer wann aufgenommen,
  ausgezeichnet, bezahlt platziert oder entfernt wurde.

## Das Siegel einmal im Jahr erneuern

Das Siegel trägt die Jahreszahl und gilt ein Jahr ([[siegel-programm]]). Daraus folgt der
einzige Termin im Kalender dieses Verzeichnisses:

1. Einmal im Jahr alle Zeilen mit `geprueft_jahr` aus dem Vorjahr durchsehen.
2. Jeden dieser Betriebe anschreiben: die sechs Kriterien erneut bestätigen, das
   Serviceversprechen erneut unterschreiben.
3. Wer bestätigt, bekommt `geprueft_jahr` auf das neue Jahr. Wer nicht antwortet, verliert das
   Siegel: `geprueft` und `geprueft_jahr` werden geleert, und der Eintrag trägt wieder
   „Noch nicht geprüft".
4. Neu bauen und ausliefern.

**Entzug zwischendurch:** Gehen belegte Beschwerden über einen Betrieb ein, werden `geprueft`
und `geprueft_jahr` sofort geleert, neu gebaut und die Nachweisseite `/auszeichnung/[slug]/`
entfernt. Belegt heißt: ein nachvollziehbarer Vorgang, nicht eine anonyme Zuschrift. Was
geprüft wurde und wie entschieden wurde, wird notiert, damit der Entzug begründbar bleibt.

## Geldseiten folgen dem allgemeinen Auffrischungsrat

Startseite, Bundesland-Seiten und Stadtseiten sind Geldseiten und werden wie solche behandelt:
Bilder tauschen, `dateModified` anheben, Tatsachen nicht in Aufklappern verstecken. Das ist
allgemeiner SEO-Rat für Geldseiten und keine Regel für Eintragsdaten. Eintragsseiten und die
Eintragsdaten stehen nicht in einem Auffrischungskalender. Ein erneuter Datenabruf ist eine
Entscheidung des Betreibers, wenn die Daten gealtert sind; er läuft als Gate 2 und 3 erneut,
und der Unterschied wird vor dem Neubau gelesen.

Was Gate 5 in jedem Fall tut: `datePublished` beim ersten Build setzen und `dateModified` bei
jedem Neubau, und Fragen, Öffnungszeiten und Merkmale als sichtbaren Text halten.

## Korrektur und Löschung

Das Verzeichnis veröffentlicht die Betriebe anderer Leute. Darum:

- Auf `/kontakt/` und in der Datenschutzerklärung steht der **Weg für Korrektur und
  Löschung**, mit einer echten E-Mail-Adresse.
- Beantwortet wird innerhalb einer Woche.
- Eine Löschung wird befolgt: die Zeile wird geleert und neu gebaut. Das ist kein Gefallen,
  sondern die Antwort auf einen Widerspruch nach Art. 21 DSGVO; die Datenschutzerklärung nennt
  dieses Recht ausdrücklich ([[page-types]]).
- Auf jeder Eintragsseite steht eine Zeile Hinweis: die Angaben sind aus öffentlichen Quellen
  zusammengetragen und keine Empfehlung. **Kein Hinweis darauf, eine Lizenz oder Zulassung zu
  prüfen** – in diesem Gewerbe gibt es keine ([[konventionen]]).
- Auf jeder Seite mit Bewertungen steht, woher die Daten kommen und wie eine Korrektur erbeten
  wird.

Das Wiki nennt die Pflichtangaben und die Pflichtwege. Es ist **keine Rechtsberatung**; die
Endfassung der Rechtstexte sollte ein Anwalt prüfen.

## Siehe auch
[[konventionen]] · [[siegel-programm]] · [[monetization-slots]] · [[launch-lean]] · [[schema]]
