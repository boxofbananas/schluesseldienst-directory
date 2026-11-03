---
title: Gate 1, Umfang abfragen
type: framework
status: active
updated: 2026-11-03
---

# Gate 1, Umfang abfragen

Gate 1 ist ein festes Gespräch, kein freies. In der englischen Fassung hatte es acht Fragen,
weil dort Branche, Bundesstaat, Domain und Herausgeber noch offen waren. **In diesem Projekt
sind sie entschieden** ([[konventionen]]). Es bleiben drei Fragen.

## Was feststeht und nicht gefragt wird

| Punkt | Festlegung |
|---|---|
| Branche | Schlüsseldienst, Google-Maps-Kategorie `locksmith` |
| Land | Deutschland, bis 16 Bundesländer als Zwischenebene |
| Domain | `die-besten-schluesseldienste.de` |
| Marke | Die besten Schlüsseldienste |
| Herausgeber | DOM Holding GmbH, Anton-Bruckner-Straße 8, 90571 Schwaig bei Nürnberg |
| Geschäftsführer | Daniel Merz, HRB 43586 |
| Wichtigste Stadt | Mannheim |
| Build-Ordner | `output/schluesseldienste-deutschland/` |

**Nie abfragen, nie vorschlagen, nie in Frage stellen:** die Branche, das Land, ein
Bundesland, die Domain, die Marke, den Herausgeber, den Geschäftsführer. Es gibt in diesem
Projekt **keinen Bewertungsbogen, keine Branchenprüfung, keinen Nischenfinder und keine
„VERTICAL FLAG" als Entscheidungsfrage**. `scripts/check_vertical.py` wird nicht benutzt; das
Skript liegt nur noch aus der englischen Fassung im Ordner. Nennt `fetch_dataforseo.py
--estimate` eine ungewöhnlich kleine Zahl, ist das ein Hinweis auf eine falsche
Kategorie-Kennung und wird geprüft, nicht dem Betreiber als Entscheidung vorgelegt.

## Die drei Fragen

**Eine Frage je Antwortrunde**, mit einem Satz Begründung, einem Beispiel und der Form, in
der die Antwort erwartet wird. Keine gestapelten Fragen. Ist eine Antwort unklar, einmal
nachfragen, nicht raten. Jede Antwort geht in `01-umfang.md`, sobald sie eintrifft.

### 1. Eigene Websites und Betriebe

> Welche Schlüsseldienst-Betriebe und -Websites gehören Ihnen? Nennen Sie bitte nur die
> Telefonnummern, je Zeile eine, zum Beispiel `0621 1234567`. Wenn keine, schreiben Sie
> „keine".

Wozu: Diese Zeilen bekommen in Gate 2 die Spalte `owned` und werden **wie jeder andere
Betrieb gelistet** ([[footprint-rules]]). Die Telefonnummer ist die einzige Kennung, die der
Ablauf braucht; sie wird auf dieselbe Weise normalisiert wie jede andere
([[konventionen]], Telefonnummern), damit `0621 1234567` und `+49 621 1234567` dieselbe
Zeile treffen.

Der Betreiber betreibt sehr viele solche Websites. Die Liste darf lang sein; frage sie
einmal vollständig ab und frage nicht nach, ob das alle sind. Merz Sicherheit in Mannheim
gehört dazu und wird im Umfangsdokument eigens vermerkt, weil Mannheim die wichtigste Stadt
ist und dort ein bezahlter Platz vorgesehen ist ([[footprint-rules]]).

### 2. Optik

> Das Verzeichnis bringt eine fertige Optik mit, die des Referenzbaus in diesem Ordner. Sagen
> Sie „zeig sie mir", dann öffne ich sie im Browser. Antworten Sie „Vorgabe", um sie zu
> nehmen. Wenn Sie die Optik einer anderen Website lieber hätten, gleich welche Branche,
> schicken Sie stattdessen eine oder zwei Adressen; übernommen werden Farben, Schrift, Karten
> und Schaltflächen, **nie** Inhalt, Bilder oder Logo.

Wozu: Das [[master-template]] ist Vorgabe und Rückfall. „Vorgabe", „keine", „habe ich nicht"
und keine Antwort bedeuten alle dasselbe: die Marken des Templates unverändert, vermerkt als
„Optik des Templates" in `01-umfang.md`. Biete nichts weiter an. Eine Adresse ist eine
Optikvorlage, aus der Gate 4 Gestaltungsmarken ableitet ([[design-seed]]). Die Beispielseiten
in [[reference-directories]] werden nur gezeigt, wenn ausdrücklich nach anderen Optiken
gefragt wird; sie sind alle englisch und aus anderen Branchen.

Kann eine genannte Seite nicht per Skript gelesen werden (Botschutz antwortet mit 403), sage,
dass Gate 4 die Marken aus zwei oder drei Bildschirmfotos ableitet, und bitte darum, sie bei
Beginn von Gate 4 in den Chat zu stellen. Kommen keine, bleiben die Marken des Templates, und
`04-plan.md` hält das fest.

### 3. Datenabruf und Kosten

> Die Einträge kommen auf einem von zwei Wegen:
> 1. **DataForSEO** (Vorgabe): Ich rufe sie mit der auf diesem Rechner gespeicherten
>    API-Anmeldung ab und nenne vorher die genauen Kosten. Für die Kategorie
>    `locksmith` in Deutschland rechne ich mit **[Zahl] Einträgen für etwa [Betrag] €**.
> 2. **Outscraper-Export**: Sie scrapen selbst und legen die CSV als
>    `input/listings-raw.csv` ab.
>
> Antworten Sie „1, abrufen" oder „2".

Wozu: Gate 2 braucht eine Rohdatei. Es gibt keinen dritten Weg und keine Beispieldaten.

**Vor dieser Frage** `scripts/connect_dataforseo.py --check` laufen lassen (kostenlos, nennt
nur ja oder nein, nie die Anmeldung). Ist eine Anmeldung gespeichert, zuerst
`scripts/fetch_dataforseo.py --estimate` laufen lassen (etwa fünf Cent) und die Zahl und den
Betrag in die Frage einsetzen. **Die Kosten müssen in der Frage stehen; abgerufen wird erst
nach einem ausdrücklichen Ja.**

Ist keine Anmeldung gespeichert, lautet die Anweisung, in einer Nachricht:

> Der Abruf braucht Ihre DataForSEO-API-Anmeldung, einmalig auf diesem Rechner gespeichert.
> Öffnen Sie das Programm „Terminal" (nicht dieses Fenster) und fügen Sie diese Zeile ein:
> `python3 "<absoluter Pfad zu diesem Ordner>/scripts/connect_dataforseo.py"`
> (unter Windows beginnt die Zeile mit `python`, nicht `python3`)
> Es fragt nach API-Anmeldung und API-Passwort von app.dataforseo.com/api-access (das
> API-Passwort ist nicht das Anmeldepasswort), prüft beides und speichert es in den
> Einstellungen von Claude Code. Antworten Sie „fertig", wenn „saved" erscheint.

Die Zeile mit dem echten absoluten Pfad ausgeben. **Den Helfer nie selbst ausführen** (er
wartet auf getippte Eingaben), die Anmeldung nie im Gespräch abfragen, und einen Connector
nicht als Weg für den Abruf anbieten: ein Connector allein gibt dem Skript nichts. Auf
„fertig" erst `--check`, dann die Schätzung. Scheitert es wiederholt, ist der
Outscraper-Export der Weg.

## Was `01-umfang.md` enthält

Nichts, was nicht gefragt oder in [[konventionen]] festgelegt ist:

- die festen Angaben aus der Tabelle oben, als Kopfabschnitt übernommen, nicht abgefragt
- die eigenen Telefonnummern, mit dem Vermerk zu Merz Sicherheit in Mannheim
- die Optik („Optik des Templates", oder die Optikvorlagen mit Vermerk, wenn eine Seite
  Skripte blockt)
- die Datenquelle und, bei DataForSEO, die Schätzzeile oder, wenn der Abruf gelaufen ist, die
  Kostenzeile aus `input/listings-raw-report.md`
- eine Liste „Offen vor Gate 5" für die Angaben, die erst dort gebraucht werden: Lebenslauf
  und Bild des Geschäftsführers, die Kontakt-E-Mail-Adresse auf der Domain, die
  Umsatzsteuer-Identifikationsnummer für das Impressum, die Stripe-Zahlungslinks der Stufen

Gate 2 läuft, sobald `01-umfang.md` freigegeben ist, in derselben Sitzung, wenn der Betreiber
das sagt. Nie vorher.

## Siehe auch
[[konventionen]] · [[directory-overview]] · [[design-seed]] · [[publisher-entity]] · [[footprint-rules]] · [[outscraper-columns]]
