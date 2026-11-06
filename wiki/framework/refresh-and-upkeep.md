---
title: Pflege: wie ein statisches Verzeichnis lebendig bleibt
type: framework
status: current
updated: 2026-11-03
---

# Pflege: wie ein statisches Verzeichnis lebendig bleibt

Ein Verzeichnis macht nach dem Start mehr Arbeit als eine einzelne Website: Inhaber wollen
ihren Eintrag ändern, und Spam will hinein. Der statische Neubau löst beides ohne Zugänge und
ohne Redaktionssystem. Eintragsdaten ändern sich, wenn eine Beanspruchung, ein Verkauf, ein
geprüfter Garantie-Antrag oder eine Korrektur sie ändert, nicht nach Kalender.

## Keine Zugänge. Zwei Türen.

- Betriebe bekommen **keine Konten** in Fassung 1. Auf gewachsenen Verzeichnissen überholten
  Spam-Anmeldungen die echten, und die Betreiber haben alle Zugänge wieder abgeschaltet.
- Hinein führen genau zwei Formulare:
  - `/eintrag-beanspruchen/` – Daten ändern, Fotos nachliefern
  - `/festpreis-garantie/antrag/` – der Garantie-Antrag mit den Preisen, geprüft gegen die
    sechs Voraussetzungen ([[siegel-programm]])
- **Jede Einsendung wird von Hand geprüft**, bevor sich etwas ändert: ein echter örtlicher
  Betrieb (kein Anfragenvermittler, kein Verzeichnis, kein Callcenter), die E-Mail-Domain
  passt zur Website, die Telefonnummer passt zur Google-Zeile. Dann die CSV ändern und neu
  bauen.
- Jede Selbstanmeldung ist ein warmer Kontakt. Am selben Tag anrufen
  ([[monetization-slots]]).

## Neu bauen bei Änderung

- Beanspruchter Eintrag, verkaufter Platz, korrigierte Telefonnummer, neue Stadt, neu
  erteilte oder entzogene Festpreis-Garantie, geänderte Garantiepreise: CSV ändern, Gate 5 erneut laufen lassen, erneut
  ausliefern. **Nie eine erzeugte Seite von Hand bearbeiten.**
- Die CSV bleibt im Projekt. Die Versionsgeschichte ist der Nachweis, wer wann aufgenommen,
  ausgezeichnet, bezahlt platziert oder entfernt wurde.

## Die Festpreis-Garantie einmal im Jahr erneuern

Die Festpreis-Garantie trägt die Jahreszahl und gilt ein Jahr ([[siegel-programm]]). Daraus
folgt der einzige Termin im Kalender dieses Verzeichnisses, und er ist ein Anrufgrund:

1. Einmal im Jahr alle Zeilen mit `geprueft_jahr` aus dem Vorjahr durchsehen.
2. Jeden dieser Betriebe anrufen: Gelten die Preise (`garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`,
   `garantie_anfahrt` für die Dienstleistung, `garantie_zylinder` und `garantie_zylinder_5mm`
   für das Material) noch, oder haben sie sich geändert? Die sechs Voraussetzungen erneut
   bestätigen, das Serviceversprechen erneut unterschreiben. Beim selben Anruf geht es um
   Sichtbarkeit.
3. Wer bestätigt, bekommt `geprueft_jahr` auf das neue Jahr und gegebenenfalls die neuen
   Preise. Wer nicht antwortet, verliert die Garantie: `geprueft`, `geprueft_jahr` und die drei
   Preisspalten werden geleert, und der Eintrag trägt wieder „Noch keine Festpreis-Garantie".
4. Neu bauen und ausliefern.

**Entzug zwischendurch:** Meldet ein Kunde eine Rechnung über dem garantierten Preis und legt
die Rechnung vor, konfrontiert der Herausgeber den Betrieb damit. Bleibt der Verstoß belegt,
werden `geprueft`, `geprueft_jahr`, `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht` und `garantie_anfahrt`
sofort geleert, neu gebaut und die Nachweisseite `/auszeichnung/[slug]/` entfernt: die Preise
sind aus dem Eintrag heraus. Belegt heißt: eine Rechnung, nicht eine anonyme Zuschrift. Was
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
