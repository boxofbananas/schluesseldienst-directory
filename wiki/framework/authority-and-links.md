---
title: Autorität und Links: wie das Verzeichnis stark wird
type: framework
status: current
updated: 2026-11-03
---

# Autorität und Links: wie das Verzeichnis stark wird

Das Verzeichnis soll Stärke an die eigenen Schlüsseldienst-Websites weitergeben, also muss es
selbst erst welche verdienen. Zwei Haltungen, beide richtig:

1. **Die Lücke.** In manchen Branchen und Gebieten gibt es eine Lücke in der Größe eines
   Verzeichnisses. Baue das vollständige, angereicherte, gut aufgebaute Verzeichnis, und es
   rankt ohne Links. Das ist die Annahme, auf der die Gates 2 bis 6 beruhen.
2. **Das SEO-Projekt.** Soll das Verzeichnis Gewicht tragen, wird es wie ein normales
   SEO-Projekt behandelt: entweder kostet es Geld für Links oder Zeit für Ansprache.
   Örtliche Nähe zählt mehr als eine Autoritätskennzahl.

Gebaut wird für Haltung 1, mitgeliefert werden die Haken für Haltung 2. Nichts hier ist ein
Gate; es ist die Arbeit nach dem Start.

## Die fünf Linkquellen, für die die Site gebaut ist

| Quelle | Was der Build mitbringt | Die Arbeit |
|---|---|---|
| **Der Garantie-Nachweis** | Je Betrieb mit Festpreis-Garantie ein HTML-Schnipsel (`templates/featured-tiers.md`) mit Bild von `/auszeichnung/[slug].svg` und Link auf die Eintragsseite, dazu die Nachweisseite `/auszeichnung/[slug]/` zum Kopieren | Das Schnipsel senden, nie eine Bilddatei: „Schicken Sie das Ihrem Webmaster, oder wir bauen es für Sie ein." Den Einbau anbieten. Der Text ist „Festpreis-Garantie [Jahr] · Türöffnung ab [garantie_tag] €"; er nennt **nie** eine Lizenz, eine Zulassung oder eine Zertifizierung, und nie „Innung", „Verband", „Kammer", „amtlich", „Verbraucherschutz" oder „getestet" ([[siegel-programm]]) |
| **Pressemitteilungen** | Die Top-Platzierungen (`best_of_rank`) und je Betrieb eine Eintragsseite | Eine Mitteilung je verkaufter Top-Platzierung, über den Betrieb. Ihre drei Links: Startseite des Betriebs, seine Eintragsseite, die Stadtseite. Der Preis der Stufe deckt die Mitteilung mit ([[monetization-slots]]) |
| **Ratgeberseiten** | `/ratgeber/[slug]/` ([[site-architecture]], [[page-types]]) | Die ausführlichste Seite zu einem Thema an einem Ort schreiben: was bei einer überhöhten Rechnung zu tun ist, was die polizeiliche Kriminalprävention zum Einbruchschutz empfiehlt, welche Stellen in einem Bundesland zuständig sind – **jeweils mit Quelle aus der Liste in [[konventionen]]**. Dann Verbraucherzentralen, Stadtportale und Mietervereine bitten, darauf zu verlinken. Mit der seo-content-engine-Skill geschrieben, wenn DataForSEO verbunden ist, sonst von Hand, und in jedem Fall geprüft ([[copy-gate]]) |
| **Örtliche Inhalte und Ansprache** | Der Ortstextblock der Stadtseite und die Ratgeberseiten | Die Stadt recherchieren, wie ein Einheimischer schreiben, dann den örtlichen Urheber ansprechen: „wir haben etwas veröffentlicht, möchten Sie etwas dazu sagen?" |
| **Der saisonale Anlass** | Nichts zu bauen | Die dunkle Jahreszeit ist die Einbruchszeit, und zu jedem Monat gibt es einen Anlass. Hausverwaltungen, Maklern und Mietervereinen einen Beitrag für ihre Seite anbieten und den Link zurück bekommen. Von Hand, eine echte E-Mail an einen echten Menschen |

Dazu ein Nebeneffekt: Macht der Betreiber SEO für einen Kunden, der gelistet ist, ist dessen
Eintragsseite eine der Seiten, auf die er Links baut. Kundenarbeit stärkt das Verzeichnis.

## Der Garantie-Nachweis ist die wichtigste Quelle

In der englischen Fassung war es ein „Verified"-Zeichen für zahlende Betriebe. Hier ist es
anders herum und deshalb stärker: **die Festpreis-Garantie ist kostenlos und nicht kaufbar**
([[siegel-programm]]). Jeder Betrieb, der die sechs Voraussetzungen erfüllt, bekommt sie, und
jeder, der sie bekommt, hat einen Grund, den Nachweis auf seine Website zu stellen: er zeigt
seinen garantierten Preis bei einem Dritten, und das kann er allein nicht nachbauen. Das sind
Links von echten örtlichen Betriebsseiten, umsonst, ohne Linktausch und ohne etwas zu
versprechen.

Der Ablauf dafür: Garantie-Antrag geprüft → `geprueft`, `geprueft_jahr` und die drei
Preisspalten setzen → neu bauen →
dem Betrieb die Nachweisseite `/auszeichnung/[slug]/` schicken, auf der das Schnipsel zum
Kopieren steht. Nicht: ein Bild per E-Mail. Ein Bild erzeugt keinen Link.

## Regeln

- Links gehen auf Eintragsseiten, Stadtseiten, Bundesland-Seiten und Ratgeberseiten, nicht nur
  auf die Startseite. Ein Verzeichnis hat viele kleine Eingänge.
- Ansprache ist eine echte E-Mail an einen echten Menschen. Keine Serienmails; das
  Verzeichnis ist auch das Kundenwerkzeug des Betreibers, und sein Ruf ist dessen Ruf.
- **Keine Linkgeschäfte zwischen den eigenen Websites und dem Verzeichnis**
  ([[footprint-rules]] gilt weiter). Eigene Betriebe werden wie jeder andere gelistet; ihr
  Website-Link ist über die Spalte `link_follow` freigeschaltet (Betreiberentscheidung vom
  2026-11-13, [[footprint-rules]]), nicht über eine gekaufte Stufe. Je Stadt höchstens ein
  eigener Betrieb auf einem bezahlten Platz.
- Nie einen Link versprechen, auch nicht im Gespräch über eine bezahlte Stufe.
- Festhalten, was wo platziert wurde (`links.md` in `output/<slug>/`), damit ein Neubau keine
  verlinkte Seite verliert. **Eine Adresse mit eingehendem Link wird nie geändert.**

## Siehe auch
[[konventionen]] · [[siegel-programm]] · [[publisher-entity]] · [[monetization-slots]] · [[launch-lean]]
