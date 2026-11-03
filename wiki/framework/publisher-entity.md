---
title: Der Herausgeber: eine echte Firma, ein benannter Mensch
type: framework
status: current
updated: 2026-11-03
---

# Der Herausgeber: eine echte Firma, ein benannter Mensch

Ein Verzeichnis ist eine Zeitschrift über eine Branche, und eine Zeitschrift hat einen
Herausgeber. In Deutschland ist das nicht nur eine Vertrauensfrage, sondern Pflicht: § 5 DDG
verlangt ein vollständiges Impressum. Die Leute, die den Herausgeber nachschlagen, sind die
Betriebe, die der Betreiber als nächstes anruft.

## Der Herausgeber steht fest

In der englischen Fassung fragte Gate 1 nach dem Herausgeber. **Hier wird er nicht gefragt.**
Die Angaben stehen in [[konventionen]] und sind:

| Feld | Wert |
|---|---|
| Herausgeber | DOM Holding GmbH |
| Anschrift | Anton-Bruckner-Straße 8, 90571 Schwaig bei Nürnberg |
| Geschäftsführer | Daniel Merz |
| Handelsregister | HRB 43586 |
| Marke | Die besten Schlüsseldienste |
| Domain | `die-besten-schluesseldienste.de` |

Diese Angaben stehen in `site.json` unter `publisher` und sind die **einzige** Quelle für
Impressum, Datenschutzerklärung, Fußbereich, die Seite „Über uns" und das Schema. Sie werden
an keiner Stelle getippt, sondern aus `site.json` erzeugt, damit Impressum und Schema nie
auseinanderlaufen.

Offen bleibt und wird vor Gate 5 gebraucht ([[gate-1-intake]], „Offen vor Gate 5"):
Umsatzsteuer-Identifikationsnummer, Kontakt-E-Mail-Adresse auf der Domain, Telefonnummer für
den Kontakt, Lebenslauf von 60 bis 120 Wörtern und ein Bild des Geschäftsführers.

## Was Gate 5 daraus baut

- **`/impressum/` nach § 5 DDG:** Firma, Rechtsform, Anschrift, Geschäftsführer,
  Handelsregister und -nummer, Umsatzsteuer-Identifikationsnummer falls vorhanden,
  Telefonnummer und E-Mail-Adresse, Verantwortlicher für den Inhalt. Aus `site.json` erzeugt.
  **Ein Platzhalter macht den Build unfertig** ([[page-types]]).
- **`/datenschutz/` nach Art. 13 DSGVO:** Verantwortlicher ist dieselbe Firma. Dazu Zwecke
  und Rechtsgrundlagen, Empfänger (Cloudflare als Hoster), Speicherdauer, Rechte der
  Betroffenen, Beschwerderecht bei der Aufsichtsbehörde, Herkunft der Firmendaten und
  Bewertungen, Widerspruchsrecht und der Weg zur Korrektur oder Löschung
  ([[refresh-and-upkeep]]). Ebenfalls ohne Platzhalter.
- **`/ueber-uns/`:** die Firma und der Geschäftsführer im Mittelpunkt: Bild, Lebenslauf, warum
  es dieses Verzeichnis gibt, wie geprüft wird ([[siegel-programm]]), der Korrektur- und
  Löschweg. Kein allgemeines „Über uns". 300 bis 500 Wörter.
- **Schema:** die `Organization` trägt `legalName`, `address`, die Handelsregisternummer in
  `identifier` und `founder` als `Person`; die Seite „Über uns" gibt beide aus
  ([[schema]]).
- **Fußbereich:** die Zeile „Die besten Schlüsseldienste ist ein Angebot der DOM Holding
  GmbH" mit Link auf „Über uns", und in der Rechtszeile **Impressum, Datenschutz und AGB auf
  jeder Seite**.
- **Verfasserzeile auf Ratgeberseiten:** jede Ratgeberseite nennt den Geschäftsführer als
  Verfasser ([[on-page-rules]]). Der Ratgeberblock der Startseite trägt keine Verfasserzeile;
  dort wird der Herausgeber im Prüfblock, im Fußbereich und auf „Über uns" genannt
  ([[master-template]]).

## Regeln

- Der Sitz des Herausgebers liegt nicht in der wichtigsten Stadt des Verzeichnisses (Nürnberg
  gegen Mannheim), und das ist kein Problem: eine Zeitschrift hat ihren Verlag irgendwo. Ein
  Problem wäre Anonymität. Das Impressum nennt die echte Anschrift, nicht die eines Betriebs.
- Der Mensch muss findbar und über die Jahre derselbe sein: gleicher Name, gleiches Bild,
  gleicher Lebenslauf auf allen Auftritten.
- Keine Kunstfigur. Hier steht eine eingetragene GmbH mit einem benannten Geschäftsführer
  dahinter; etwas anderes wäre bei einer Impressumspflicht auch nicht tragfähig.
- Ein Video („warum ich das gebaut habe", 60 Sekunden) auf „Über uns" ist das stärkste
  Vertrauenszeichen für einen kalt angerufenen Betrieb. Wahlweise, aber es wirkt.
- **Der Herausgeber tritt nie als amtliche Stelle auf.** Nie „Innung", „Verband", „Kammer",
  „amtlich", „Verbraucherschutz", „getestet" ([[konventionen]]). Die DOM Holding GmbH gibt ein
  Verzeichnis heraus und veröffentlicht die Festpreis-Garantie, die der Betrieb gibt; sie ist
  keine Prüfstelle und sagt das auf `/festpreis-garantie/` selbst ([[siegel-programm]]).

## Der Name des Verzeichnisses

Die Marke steht fest: **Die besten Schlüsseldienste**, passend zur Domain
`die-besten-schluesseldienste.de`. Sie liest sich als Publikation, und genau das soll sie.
Daraus folgt eine Pflicht: Wenn das Verzeichnis „die besten" heißt, muss auf `/festpreis-garantie/`
nachlesbar stehen, woran das gemessen wird, und auf `/premium/`, dass Sichtbarkeit kauflich
ist und die Garantie nicht. Eine Behauptung ohne veröffentlichte Voraussetzungen ist
angreifbar.
Kein Vorschlag für einen anderen Namen; die Entscheidung ist gefallen.

## Siehe auch
[[konventionen]] · [[siegel-programm]] · [[authority-and-links]] · [[schema]] · [[page-types]]
