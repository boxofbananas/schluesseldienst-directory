---
title: Bezahlte Plätze
type: framework
status: current
updated: 2026-11-03
---

# Bezahlte Plätze

Was das Verzeichnis verkauft, und was der Build dafür mitbringen muss. Preise und
Zahlungslinks stehen in `templates/featured-tiers.md`.

| Stufe | In Fassung 1? | Was die Site braucht |
|---|---|---|
| Werbebanner | Nein (Vermarkter wollen etwa 250.000 Besucher im Monat) | nichts |
| **Premium-Eintrag, 97 € im Jahr** (der leichteste Verkauf) | **Ja** | der ausgebaute Eintragszustand (Fotos, alle Links gefolgt, Karte nach Klick), das Siegelbild zum Einbinden, eine Spalte `premium` |
| **Stadt-Premium, 29 € im Monat** | **Ja** | Premium-Plätze auf jeder Stadtseite und der Startseite, die Seite `/premium/` mit Stufen und Zahlungslinks, eine Spalte `featured`, die Gate 5 liest |
| **Top-Platzierung, 250 € einmalig** | **Ja** | die Stadtseite **ist** die Liste „Die besten Schlüsseldienste in [Stadt]"; eine Spalte `best_of_rank` heftet den bezahlten Platz fest |
| Landkreis-Stufe, Bundesland-Stufe | Später zu aktivieren | die Felder stehen im Template, werden aber erst verkauft, wenn ein Stadt-Platz verkauft ist |
| Eigene Dienstleistungen (SEO, Profilpflege, Website) | **Ja, für den Betreiber der wichtigste Punkt** | nichts auf der Site; der Eintrag ist der Anlass für den Anruf |
| Anfragen verkaufen | Ja, später | ein Formular oder eine getrackte Nummer je Stadt, sobald die Seiten ranken |

**Das Siegel ist keine Stufe.** Es ist kostenlos und nicht kaufbar; bezahlt wird nur
Sichtbarkeit ([[siegel-programm]]). Dieser Satz steht auf `/siegel/` und auf `/premium/`. Ein
zahlender Betrieb ohne erfüllte Kriterien bekommt kein Siegel.

## Der Siegel-Antrag ist der Verkaufsanlass

Jeder nicht geprüfte Eintrag trägt sichtbar **„Noch nicht geprüft"** mit Link auf
`/siegel/antrag/`. Das ist der Grund, aus dem ein Betrieb anruft oder schreibt, und der
Einstieg in jedes Gespräch: er kann das Zeichen kostenlos loswerden, und beim selben Anruf
geht es um Sichtbarkeit. **Das Zeichen wird nie abgeschaltet** – kein Gate, keine Einstellung
und kein Wunsch eines Betriebs entfernt es ([[siegel-programm]]).

Der Ablauf hat damit zwei Türen, und das ist Absicht:

| Tür | Adresse | Was sie auslöst |
|---|---|---|
| **Eintrag beanspruchen** | `/eintrag-beanspruchen/` | Daten ändern, Fotos nachliefern, kostenlos; danach das Gespräch über Sichtbarkeit |
| **Siegel beantragen** | `/siegel/antrag/` | die Prüfung gegen die sechs Kriterien, kostenlos; danach dasselbe Gespräch |

Beide Formulare fragen am Ende, ob über Premium gesprochen werden soll. Beide Anfragen sind
warme Kontakte und werden am selben Tag beantwortet.

## Beanspruchen

Jede Eintragsseite trägt „Ist das Ihr Betrieb? Eintrag beanspruchen". Das Formular
(`templates/claim-form.html`, ohne eigenen Server) erfasst Betrieb, Ansprechpartner, Nachweis
(E-Mail-Adresse auf der Domain der Website oder ein Anruf auf der Nummer des
Google-Eintrags) und die Wunschliste. Beanspruchen ist kostenlos. Ein beanspruchter Eintrag
bekommt `claimed=true` und das Zeichen „Bestätigt".

**Erst prüfen, dann ändern.** Keine Zugänge für Betriebe in Fassung 1 (auf gewachsenen
Verzeichnissen überholten Spam-Anmeldungen die echten). Jede Beanspruchung wird von Hand
geprüft: ein echter örtlicher Betrieb, kein Anfragenvermittler und kein Callcenter; die
E-Mail-Domain passt zur Website; die Telefonnummer passt zur Google-Zeile. Dann die CSV
ändern und neu bauen ([[refresh-and-upkeep]]).

## Die beiden Eintragszustände

- **Einfach (nicht beansprucht):** Name, Anschrift, Telefonnummer, Bewertung, Zahl der
  Bewertungen, Merkmale, Beschreibung, Kartenplatzhalter, Website-Link mit `nofollow`. Keine
  Fotos, keine Profillinks. Dazu „Noch nicht geprüft", solange kein Siegel vorliegt.
- **Ausgebaut (beansprucht mit Premium oder bezahlter Stufe):** Fotos vom Inhaber, alle Links
  gefolgt (Website und Profile), die Karte nach Klick, Öffnungszeiten, das Siegelbild wenn
  geprüft. Diese Lücke ist das Verkaufsargument: „Sie haben einen Eintrag, und er ist nicht
  ausgebaut."

## Die Stufen

Preise, Zahlungslinks und das Siegelschnipsel stehen in `templates/featured-tiers.md`.
Kurzfassung:

- **Premium-Eintrag, 97 € im Jahr:** der ausgebaute Zustand plus das Siegelbild zum Einbinden.
- **Stadt-Premium, 29 € im Monat:** oberste Karte auf einer Stadtseite, gefolgter Link, Foto
  (`featured` = `city`).
- **Top-Platzierung, 250 € einmalig:** fester Platz in der Liste „Die besten Schlüsseldienste
  in [Stadt]" (`best_of_rank` 1 bis 3), dazu eine Pressemitteilung über den Betrieb.
- Landkreis- und Bundesland-Stufe: **später zu aktivieren**, nicht verkaufen, bevor ein
  Stadt-Platz verkauft ist.

**Die Spalte `featured` kennt genau drei Werte, und sie sind englisch:** `city`, `county`,
`state`. Nur diese drei liest der Build (`templates/astro/src/lib/load.mjs`); ein deutscher
Wert wie `stadt` erzeugt einen bezahlten Platz, der auf keiner Seite erscheint.

**Je Stadt und Stufe ein Betrieb.** Verkauft wird von Hand: Zahlungslink senden, Spalte
setzen, neu bauen. Kündigung heißt Spalte leeren und neu bauen. **Und je Stadt höchstens ein
eigener Betrieb auf einem bezahlten Platz** ([[footprint-rules]]).

## Das Siegelbild ist ein Link, deshalb HTML

Das Schnipsel in `templates/featured-tiers.md` ist HTML, nie eine Bilddatei. Der Satz, der
funktioniert: „Schicken Sie das Ihrem Webmaster, oder wir bauen es für Sie ein." Biete den
Einbau an, denn der Zweck ist der Link von der Website des Inhabers auf seine Eintragsseite
([[authority-and-links]]). Der Text auf dem Siegel trägt die Jahreszahl und nennt nie eine
Lizenz, eine Zulassung oder eine Zertifizierung ([[siegel-programm]]).

## Die Top-Platzierung

Die Stadtseite ordnet die Einträge, also ist jede Stadtseite eine Liste „Die besten
Schlüsseldienste in [Stadt]". Die Betriebe darauf anrufen und gratulieren, das öffnet das
Gespräch. Ein halbes Jahr später die anrufen, die nicht darauf stehen: „wir aktualisieren
unsere Liste." Die Spalte `best_of_rank` steuert die festen Plätze; die unbezahlten bleiben
nach Daten geordnet.

**Die Pressemitteilung** handelt vom Betrieb, nicht vom Verzeichnis. Ihre drei Links gehen auf
die Startseite des Betriebs, auf seine Eintragsseite und auf die Stadtseite. Eine Mitteilung
stärkt drei Teile des Verzeichnisses ([[authority-and-links]]).

## Die Ansprache, die das Verzeichnis ermöglicht

- Der warme Einstieg: „Sie haben einen Eintrag in Die besten Schlüsseldienste, dem
  Verzeichnis aller Schlüsseldienste in Deutschland. Dort steht bei Ihnen noch ‚Noch nicht
  geprüft'. Die Prüfung kostet nichts, soll ich Ihnen den Fragebogen schicken?"
- Danach das Gespräch über den ausgebauten Eintrag, danach das Einstiegsangebot für SEO oder
  Profilpflege. Für Betreiber solcher Verzeichnisse sind sie die wichtigste Quelle für
  SEO-Kunden.
- Selbstanmeldungen auf einem gewachsenen Verzeichnis sind die wärmsten Kontakte überhaupt.

Nichts in diesen Gesprächen und in keinem Text verspricht einen Link, eine Aufnahme, eine
Änderung oder eine Platzierung, bevor sie entschieden ist, und nichts stellt das Siegel als
käuflich dar.

## Siehe auch
[[konventionen]] · [[siegel-programm]] · [[page-types]] · [[footprint-rules]] · [[refresh-and-upkeep]] · [[authority-and-links]]
