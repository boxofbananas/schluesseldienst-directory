---
title: Einträge bereinigen (Gate 2)
type: framework
status: current
updated: 2026-11-03
---

# Einträge bereinigen (Gate 2)

Das meiste, was ein Scrape zurückbringt, ist unbrauchbar. Die Regeln sind deterministisch und
stehen in `scripts/clean_listings.py`; diese Seite ist die Spezifikation, die das Skript
umsetzt. Die genannten Quoten stammen aus dem **englischen Pilotprojekt** und sind
Größenordnungen, keine Zielwerte für Deutschland.

## Die Regeln, in dieser Reihenfolge

1. **Land und Bundesland.** Zeilen behalten, deren Land Deutschland ist. Das Bundesland wird
   **nicht gefiltert, sondern zugeordnet**: aus `state` beziehungsweise aus der Postleitzahl,
   auf einen der 16 Slugs aus [[konventionen]]. Die englische Fassung filterte hier auf einen
   Bundesstaat; dieses Verzeichnis nimmt alle. Eine Zeile ohne zuordenbares Bundesland geht
   nicht verloren: sie wird gekennzeichnet und in Gate 4 vorgelegt.
2. **Geschlossene löschen.** `business_status` muss `OPERATIONAL` sein.
3. **Ohne Bewertung löschen.** `reviews` muss größer als 0 sein.
4. **Aktualität (nur DataForSEO).** Zeilen löschen, deren `last_updated_time` älter als 365
   Tage ist (`--max-age-days`). Die Datenbank hat kein Merkmal für Geschäftsaufgabe, also
   steht Veralterung dafür ein. Wer die Zeilen zurück will, setzt `--max-age-days 0` und nimmt
   die geschlossenen mit.
5. **Name enthält ein Branchenwort, oder die Zeile trägt die Kategorie.** Die Branchenwörter
   sind die Wörter, die deutsche Betriebe dieses Gewerbes in ihre Namen schreiben:
   `--niche "schlüsseldienst,schluesseldienst,schlüsselnotdienst,aufsperrdienst,türöffnung,tueroeffnung,schlüsselservice,sicherheitstechnik,schließanlagen,schliessanlagen"`
   plus `--category "locksmith"`. **Der Vergleich muss umlautunabhängig sein**: „Schlüsseldienst"
   und „Schluesseldienst" müssen beide treffen, sonst fehlt die Hälfte der Betriebe. Die
   Kategorie als Rückfall behält Markennamen ohne Branchenwort und Zeilen, die die Kategorie
   nur als Nebenkategorie tragen.
6. **Entdoppeln.** Zuerst über die normalisierte `phone`, dann über normalisierte `address`
   plus `postal_code`. Die Zeile mit mehr Bewertungen bleibt.
7. **Eigene kennzeichnen.** Zeilen, deren Telefonnummer in `--owned-phones` oder deren Website
   in `--owned-domains` steht, bekommen `owned=true`. Beide Schalter sind gleichwertig und
   lassen sich mischen; bei `--owned-domains` genügt der Hostname, mit oder ohne `https://` und
   `www.`. Die Zeilen werden **behalten und wie jeder andere Eintrag behandelt**; die
   Kennzeichnung existiert nur, damit der Bericht sie zeigt und niemand sie versehentlich
   bevorzugt ([[footprint-rules]]).
8. **Dünn kennzeichnen.** `reviews < 5` oder kein Beschreibungstext ergibt `thin=true`
   (benutzt von [[launch-lean]], nicht gelöscht). Geprüft wird `description`; ein `about`, das
   sich als JSON einlesen lässt, ist Googles Merkmalsdaten und kein Text
   ([[outscraper-columns]]). Die Kennzeichnung ist vorläufig: Gate 3 nimmt sie einem Eintrag
   mit fünf oder mehr Bewertungen ab, sobald dessen eigene Website echten Text geliefert hat.
9. **Garantiespalten anlegen.** `geprueft`, `geprueft_jahr`, `garantie_tag`, `garantie_nacht`
   und `garantie_anfahrt`, alle leer, dazu `preisschutz` (leer, reservierte Stufe, von nichts
   ausgewertet). Gate 2 setzt sie nie; nur der Herausgeber setzt sie von Hand nach der Prüfung
   eines Garantie-Antrags ([[siegel-programm]], [[outscraper-columns]]). Leer bedeutet „Noch
   keine Festpreis-Garantie", und so wird es auf der Seite angezeigt.

`slugify` schreibt Umlaute um, **bevor** es Sonderzeichen entfernt (`ä→ae`, `ö→oe`, `ü→ue`,
`ß→ss`), sonst wird aus „Nürnberg" `n-rnberg`. Das gilt für `slug`, `city_slug` und den
Bundesland-Slug ([[konventionen]]).

## Die Branchenbesonderheit: Gate 2 macht sie sichtbar, Gate 4 entscheidet

**Gate 2 löscht keine Zeile wegen ihres Gewerbes.** Das ist die Regel, und sie gilt in diesem
Projekt besonders, weil die Kategorie `locksmith` in Deutschland drei Gruppen einfängt, die
kein Schlüsseldienst im gemeinten Sinn sind:

1. **Fremde Gewerbe.** Schuhmacher, Gravurbetriebe, Metallbauer und Baumärkte tragen die
   Kategorie, weil sie Schlüssel nachmachen. Türen öffnen sie nicht. Sie sind nicht falsch
   erfasst, sie sind nur etwas anderes.
2. **Kettenbetriebe.** Derselbe Firmenname an vielen Adressen in vielen Städten. Oft ist nur
   eine Adresse ein Betrieb und der Rest eine Eintragung.
3. **Callcenter ohne Ortsbezug.** Einträge mit einer ortsfremden Nummer, ohne erreichbare
   Anschrift, oft an mehreren Orten gleichzeitig. Sie verfehlen Voraussetzung 5 der
   Festpreis-Garantie ([[siegel-programm]]).

Was das Skript dafür tut: **berichten, nicht löschen.** Der Bericht führt zusätzlich

- die behaltenen Zeilen nach `type` (Haupt-Kategorie), damit die fremden Gewerbe als Gruppe
  sichtbar werden
- die Zeilen, die **nur** über den Kategorie-Rückfall hereinkamen (Name und Haupt-Kategorie
  trafen nicht), mit ihren häufigsten Haupt-Kategorien
- **Namen, die an mehr als drei Adressen vorkommen**, mit Zahl der Adressen und Zahl der
  Städte, als Kettenverdacht
- **Zeilen ohne Ortsbezug**: Ortsvorwahl der Telefonnummer passt nicht zur Postleitzahl, oder
  es gibt keine Straßenanschrift, als Callcenter-Verdacht

Diese vier Listen sind die Vorlage für Gate 4. **Der Mensch entscheidet je Gruppe**, und jede
Entscheidung, die eine Zeile entfernt, geht nach `04-exclusions.csv`, nie in die bereinigte
CSV. Der Blueprint hat für keine der Gruppen einen Vorgabewert, der löscht.

## Der Bericht (`02-clean-report.md`)

Zeilen hinein, Zeilen nach jeder Regel, Behaltequote, **Zahl der Bundesländer mit mindestens
einer Stadtseite und Zahl der Einträge je Bundesland**, wie viele Städte die Mindestzahl von 3
erreichen und wie viele behaltene Zeilen diese Städte halten, gefundene eigene Zeilen, dünne
Zeilen, geschriebene Domains, dann die vier Listen oben und die Städte mit ihren Zahlen.
Mannheim wird eigens ausgewiesen, weil es die wichtigste Stadt ist. Zeilen ohne zuordenbares
Bundesland werden mit Grund aufgeführt.

## Ausgabespalten

Die Spalten aus [[outscraper-columns]] unter „Von der Verarbeitung benutzt", dazu `slug`,
`city_slug`, `owned`, `thin`, `featured` (leer), `featured_cities` (leer), `claimed` (leer),
`geprueft` (leer), `geprueft_jahr` (leer).

Das Bundesland bleibt in `state` und `state_code` stehen; Spalten `bundesland` oder
`bundesland_slug` gibt es nicht, und der Build würde sie auch nicht lesen (er leitet Name,
Slug und Kürzel aus `state` und `state_code` ab). `premium` und `best_of_rank` legt Gate 2
nicht an: sie kommen beim ersten Verkauf dazu ([[monetization-slots]]).

## Die Domainliste (`02-domains.txt`)

Eine Website-Domain je Zeile für jede behaltene Zeile. Sie existiert für den
Outscraper-Weg, wo der Rohexport keine E-Mail-Adressen trägt: der Betreiber lädt diese Datei
in Outscrapers Kontakt-Scraper, statt für jede unbrauchbare Zeile des Rohexports zu zahlen.
Der DataForSEO-Weg bringt Adressen schon mit. In jedem Fall wird eine Adresse auf ihre Domain
geprüft und ein Zustellversuch gemacht, bevor der Beanspruchungsablauf etwas sendet
([[refresh-and-upkeep]]). **E-Mail-Adressen erscheinen nie auf einer Seite.**

## Siehe auch
[[konventionen]] · [[outscraper-columns]] · [[enrichment]] · [[siegel-programm]]
