---
title: Gate 5 – Faktensammlung
type: output
status: in-arbeit
updated: 2026-11-04
---

# Gate 5 – Faktensammlung

Jede Aussage über Recht, Gewerbe, Preise, örtliche Besonderheiten oder Auftragsverarbeiter mit
Quelle und Abrufdatum. Quellenreihenfolge für Branchenfakten ([[konventionen]]): Handwerkskammer,
Stadt-/Gemeindeportale (Gewerbeamt), Verbraucherzentrale, polizei-beratung.de, Stiftung Warentest.
Nicht als Quelle: andere Schlüsseldienst-Websites, Branchenbücher, Presseportale. Ein Punkt mit nur
einer kommerziellen Quelle gilt als unbelegt.

## Auftragsverarbeiter (für Impressum/Datenschutz)

### Zahlungsdienst Stripe
- **Vertragspartei im EWR:** Stripe Payments Europe, Limited, One Wilton Park, Wilton Place,
  Dublin 2, D02 FX04, Irland.
- **Quelle:** Stripe, „Guide for Service of Process, Legal Notices and Law Enforcement Requests"
  (`stripe.com/legal/legal-process-guide`) – nennt diese Gesellschaft als Vertragspartei für den
  Europäischen Wirtschaftsraum. Bestätigt über das LEI-Register / irisches Companies Registration
  Office, **Registernummer 513174**. **Abrufdatum 04.11.2026.**
- **Drittland:** Ja. Die irische Gesellschaft ist Vertragspartei; es findet eine Weiterübermittlung
  an Stripe, Inc. (USA) unter Standardvertragsklauseln statt. In `site.json` als
  `processors.payment` mit `thirdCountry: true` hinterlegt.
- **Status:** belegt (Primärquelle des Anbieters + unabhängiges Register).

### Formulardienst
- **Offen.** Formsprees eigene Unterlagen nennen keine Anschrift, Wirtschaftsdatenbanken
  widersprechen sich (Austin vs. Seattle). Es wird **nichts** eingetragen; `processors.form.company`
  bleibt `OFFEN_` (die Datenschutzerklärung nennt dann nur den Namen des Dienstes). Entfällt ganz,
  wenn die Annahme auf eine Cloudflare Pages Function umgestellt wird (siehe
  `berichte/2026-11-04-startsperren-zahlung-und-formular.md`): dann ist Cloudflare der einzige
  Verarbeiter und steht ohnehin als Hoster in der Datenschutzerklärung.

## Branchen- und Rechtsfakten

Grundsatz, der in keinem Text fehlen darf: Das Schlüsseldienst-Handwerk ist in Deutschland **kein
zulassungspflichtiges Handwerk** nach Anlage A der Handwerksordnung – keine Lizenz, keine
Meisterpflicht. Belegbar und erlaubt: Gewerbeanmeldung, Handelsregistereintrag, freiwillige
Mitgliedschaften, selbst genannte Qualifikationen. Die folgenden fünf Punkte sind die
**geteilten** Fakten, aus denen jeder Stadttext sparsam schöpfen darf (recherchiert 04.11.2026).

### Keine Zulassungspflicht, keine Meisterpflicht
Ein Schlüsseldienst ist in Deutschland kein eigenständiges zulassungspflichtiges Handwerk. In der
Liste der zulassungspflichtigen Handwerke (Anlage A der Handwerksordnung) steht „Schlüsseldienst"
nicht; dort ist nur das Handwerk Metallbauer (Anlage A, Nr. 13) geführt. Für das Öffnen von Türen
und das Anfertigen von Schlüsseln als eigenständiges Gewerbe gibt es daher keine Meisterpflicht und
keine staatliche Zulassung; die Tätigkeit wird je nach Zuschnitt als zulassungsfreies Handwerk oder
handwerksähnliches Gewerbe (Anlage B der Handwerksordnung) geführt, ohne Meisterbrief und ohne
Befähigungsnachweis.
- **Quellen:** Handwerksordnung, Anlage A (Nr. 13 Metallbauer), über den Zentralverband des
  Deutschen Handwerks, `zdh.de/daten-und-fakten/handwerksordnung/gewerbe-der-handwerksordnung-anlage-a/`;
  Handwerkskammer Hamburg, „Eintragung in das Verzeichnis zulassungsfreier Handwerke oder
  handwerksähnlicher Gewerbe", `hamburg.de/service/info/11277392/`. **Abrufdatum 04.11.2026. Status: belegt.**

### Überteuerte Notdienste – Festpreis vor Beauftragung
Die Verbraucherzentrale warnt vor überhöhten Rechnungen bei Notöffnungen und rät, schon am Telefon
vor der Beauftragung einen verbindlichen Festpreis einschließlich Anfahrt und etwaiger Zuschläge zu
vereinbaren. Wer dazu keine Auskunft gibt, sollte übergangen werden. Die Verbraucherzentrale Hamburg
nennt als gerade noch angemessenen Rahmen für eine einfache Türöffnung ohne Schlosstausch rund
100 Euro tagsüber und etwa 180 Euro nachts oder am Wochenende.
- **Quellen:** Verbraucherzentrale (Bundesverband), „Schlüsseldienste: So schützen Sie sich vor
  überzogen hohen Rechnungen", `verbraucherzentrale.de/wissen/vertraege-reklamation/abzocke/`;
  Verbraucherzentrale Hamburg, „Ausgesperrt und abgezockt vom Schlüsseldienst", `vzhh.de`.
  **Abrufdatum 04.11.2026. Status: belegt.** Die Euro-Beträge stammen von der VZ Hamburg; der
  Bundesverband nennt selbst keine Zahlen.

### Einbruchschutz – mechanische Nachrüstung zuerst
Die Polizeiliche Kriminalprävention (Kampagne K-EINBRUCH) empfiehlt in erster Linie mechanische
Sicherungen an Türen und Fenstern. Als Mindestanforderung gilt die Widerstandsklasse RC 2 nach
DIN EN 1627 (bei höher gelegenen Fenstern genügt RC 1 N); Nachrüstsysteme sollen der DIN 18104
Teil 1 (aufschraubbar) oder Teil 2 (im Falz) entsprechen. Als staatliche Förderung nennt die
Kampagne KfW-Programme, zuletzt den Kredit „Altersgerecht Umbauen (159)"; der frühere Zuschuss
„Einbruchschutz (455-E)" war mangels Mittel nicht verfügbar. Eine kostenlose Beratung durch die
Polizei wird empfohlen.
- **Quelle:** Polizeiliche Kriminalprävention der Länder und des Bundes, K-EINBRUCH, „Staatliche
  Förderung von Einbruchschutz", `k-einbruch.de/sicherheitstipps/foerderung/`.
  **Abrufdatum 04.11.2026. Status: belegt.**

### Stiftung Warentest zu Schlüsseldiensten
Stiftung Warentest hat Schlüsseldienste untersucht (14 Anbieter: zehn lokale Betriebe vor Ort, vier
überregionale Vermittlungsportale) und das Ergebnis mit „Pfusch, Abzocke" überschrieben. Die Preise
für eine einfache Türöffnung reichten von 65 bis 415 Euro; kritisiert wurden überhöhte Preise vor
allem der Vermittlungsportale (drei von vier „mangelhaft") und der Verkauf unnötig teurer Zylinder.
Lokale Betriebe schnitten überwiegend besser ab.
- **Quelle:** Stiftung Warentest, „Schlüsseldienste im Test: Pfusch, Abzocke und ein naheliegender
  Geheimtipp" (2019), `test.de`. **Abrufdatum 04.11.2026. Status: belegt.** Eckdaten aus der frei
  zugänglichen Testbeschreibung; der vollständige Test ist kostenpflichtig.

### Gewerbeanmeldung und Handwerksrolle
Wer einen Schlüsseldienst selbstständig betreibt, meldet das Gewerbe beim Gewerbeamt an und lässt
die Tätigkeit bei der Handwerkskammer in das Verzeichnis der zulassungsfreien Handwerke bzw.
handwerksähnlichen Gewerbe eintragen (Gewerbekarte). Anders als bei zulassungspflichtigen Handwerken
ist dafür kein Qualifikations- oder Meisterbrief nötig. Eine Eintragung ins Handelsregister hängt
von Rechtsform und Geschäftsumfang ab (etwa bei Kapitalgesellschaften) und ist keine allgemeine
Pflicht jedes Schlüsseldienstes.
- **Quellen:** Handwerkskammer Hamburg, `hamburg.de/service/info/11277392/`; Serviceportal
  Baden-Württemberg (Handwerkskammer), „Verzeichnis der zulassungsfreien Handwerke …",
  `service-bw.de/zufi/leistungen/987`. **Abrufdatum 04.11.2026. Status: belegt.** Handelsregister
  nicht pauschal als Pflicht formulieren.
</content>

---

## Ratgeberseiten (Gate 5, Punkt 7)

Fünf Ratgeberseiten, geschrieben am 04.11.2026 aus den im Regelwerk zugelassenen Quellen
(Verbraucherzentrale, Stiftung Warentest, Polizeiliche Kriminalprävention / k-einbruch.de,
Handwerkskammer, kommunale Notrufseite). Keine anderen Schlüsseldienst-Websites, keine Branchenbücher,
keine Presseportale. Jede Quelle mit Abrufdatum; alle als **belegt** eingestuft. Seite „Unseriöse
Schlüsseldienste erkennen" nennt bewusst keinen einzelnen Betrieb.

### /ratgeber/was-kostet-ein-schluesseldienst/ — Was kostet ein Schlüsseldienst?
- Verbraucherzentrale: https://www.verbraucherzentrale.de/wissen/vertraege-reklamation/abzocke/schluesseldienste-so-schuetzen-sie-sich-vor-ueberzogen-hohen-rechnungen-6687 (Abruf 2026-11-04)
- Verbraucherzentrale: https://www.verbraucherzentrale.de/infothek/schluesseldienste (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienst-Abzocke-So-wehren-Sie-sich-gegen-teure-Tueroeffner-5154674-0/ (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienste-im-Test-Pfusch-Abzocke-und-ein-naheliegender-Geheimtipp-1152279-0/ (Abruf 2026-11-04)
- Verbraucherzentrale: https://www.verbraucherzentrale.de/wissen/geld-versicherungen/weitere-versicherungen/generalschluessel-verloren-drohende-kosten-bis-zum-preis-eines-kleinwagens-10679 (Abruf 2026-11-04)
- Zentralverband des Deutschen Handwerks (Handwerksordnung): https://www.zdh.de/daten-und-fakten/handwerksordnung/ (Abruf 2026-11-04)

### /ratgeber/ausgesperrt-was-tun/ — Ausgesperrt: Was Sie jetzt tun sollten
- Verbraucherzentrale: https://www.verbraucherzentrale.de/wissen/vertraege-reklamation/abzocke/schluesseldienste-so-schuetzen-sie-sich-vor-ueberzogen-hohen-rechnungen-6687 (Abruf 2026-11-04)
- Verbraucherzentrale: https://www.verbraucherzentrale.de/infothek/schluesseldienste (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienst-Abzocke-So-wehren-Sie-sich-gegen-teure-Tueroeffner-5154674-0/ (Abruf 2026-11-04)
- Stadt München (Notrufseite): https://stadt.muenchen.de/infos/notruf.html (Abruf 2026-11-04)
- Polizeiliche Kriminalprävention: https://www.polizei-beratung.de/themen-und-tipps/einbruch/technische-sicherheit/ (Abruf 2026-11-04)

### /ratgeber/unserioese-schluesseldienste-erkennen/ — Unseriöse Schlüsseldienste erkennen
- Verbraucherzentrale: https://www.verbraucherzentrale.de/wissen/vertraege-reklamation/abzocke/schluesseldienste-so-schuetzen-sie-sich-vor-ueberzogen-hohen-rechnungen-6687 (Abruf 2026-11-04)
- Verbraucherzentrale Niedersachsen: https://www.verbraucherzentrale-niedersachsen.de/themen/handwerker-notdienste/so-vermeiden-sie-aerger-unserioesen-schluesselnotdiensten (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienst-Abzocke-So-wehren-Sie-sich-gegen-teure-Tueroeffner-5154674-0/ (Abruf 2026-11-04)
- Handwerkskammer Rhein-Main: https://www.hwk-rhein-main.de/downloads/Beratung/Rechtsberatung/Schl%C3%BCsselnotdienste.pdf (Abruf 2026-11-04)
- Polizeiliche Kriminalprävention: https://www.polizei-dein-partner.de/themen/diebstahl-betrug/detailansicht-diebstahl-betrug/artikel/unserioese-schluesseldienste.html (Abruf 2026-11-04)

### /ratgeber/schloss-austauschen/ — Schloss austauschen: Anlässe, Ablauf, Kosten
- Stiftung Warentest: https://www.test.de/Test-Tuerschloesser-und-Schliesszylinder-5243517-5243523/ (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienst-Abzocke-So-wehren-Sie-sich-gegen-teure-Tueroeffner-5154674-0/ (Abruf 2026-11-04)
- Stiftung Warentest: https://www.test.de/Schluesseldienste-im-Test-Pfusch-Abzocke-und-ein-naheliegender-Geheimtipp-1152279-5520609/ (Abruf 2026-11-04)
- Verbraucherzentrale: https://www.verbraucherzentrale.de/infothek/schluesseldienste (Abruf 2026-11-04)
- Verbraucherzentrale: https://www.verbraucherzentrale.de/wissen/vertraege-reklamation/abzocke/schluesseldienste-so-schuetzen-sie-sich-vor-ueberzogen-hohen-rechnungen-6687 (Abruf 2026-11-04)
- Polizeiliche Kriminalprävention (k-einbruch.de): http://www.k-einbruch.de/tueren (Abruf 2026-11-04)

### /ratgeber/tueren-nachruesten-einbruchschutz/ — Türen nachrüsten: Einbruchschutz ohne Umbau
- Polizeiliche Kriminalprävention der Länder und des Bundes: https://www.polizei-beratung.de/themen-und-tipps/einbruch/technische-sicherheit/ (Abruf 2026-11-04)
- K-EINBRUCH (Polizeiliche Kriminalprävention): https://www.k-einbruch.de/sicherheitstipps/tueren/ (Abruf 2026-11-04)
- K-EINBRUCH (Polizeiliche Kriminalprävention): https://www.k-einbruch.de/sicherheitstipps/fenster/ (Abruf 2026-11-04)
- K-EINBRUCH (Polizeiliche Kriminalprävention, zur KfW-Förderung): https://www.k-einbruch.de/sicherheitstipps/foerderung/ (Abruf 2026-11-04)
