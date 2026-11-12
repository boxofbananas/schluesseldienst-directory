---
title: Regeln für die Seitentechnik
type: seo
status: current
updated: 2026-11-03
---

# Regeln für die Seitentechnik

## Titel

Der senkrechte Strich trennt Seitentitel und Marke.

- **Startseite:** `Schlüsseldienst in Deutschland | Die besten Schlüsseldienste`
- **Bundesland:** `Schlüsseldienst [Bundesland]: alle Städte | Die besten Schlüsseldienste`
- **Stadt:** `Schlüsseldienst [Stadt] ([N] Einträge) | Die besten Schlüsseldienste`
- **Eintrag:** `[Betrieb] | Schlüsseldienst in [Stadt]`
- **Leistung:** `[Leistung] in Deutschland | Die besten Schlüsseldienste`

Der Bundeslandname wird nie abgekürzt; die Kürzel aus [[konventionen]] sind für Datenfelder.
Deutsche Titel werden länger als englische: über 60 Zeichen kürzt Google. Fällt ein Titel zu
lang aus, zuerst die Marke kürzen, nie den Ortsnamen.

## Beschreibungen

Für Startseite, Bundesland- und Stadtseiten aus den Daten geschrieben (Anzahl, bestbewertete
Betriebe, Zahl der geprüften). Eintragsseiten: der erste Satz der Beschreibung. **Nie ein
Preis**, auch keine Spanne ([[page-types]]).

## Überschriften

Ein H1 je Seite. H2 für Abschnitte, H3 für Karten; Eintragskarten sind H3. Das Garantie-Zeichen
ist keine Überschrift, sondern ein Element mit Link.

## Verfasserzeile

Verfasserzeile (Name, Link auf „Über uns", Daten) auf **jeder Ratgeberseite**. Der
Ratgeberblock der Startseite trägt keine; dort wird der Herausgeber im Prüfblock („Ein
Angebot der DOM Holding GmbH", verlinkt auf „Über uns"), in der Fußzeile und auf „Über uns"
genannt ([[master-template]], [[publisher-entity]]). Eintrags-, Stadt- und
Bundesland-Seiten tragen die Zeile mit `dateModified`, keine Verfasserzeile.

## Sprache und Format

- `lang="de"` im `<html>`, `inLanguage` `de-DE` im Schema.
- Datum `TT.MM.JJJJ`, Dezimaltrennzeichen Komma (`4,8`), Preise `97 €`.
- Telefonnummern sichtbar als `+49 621 1234567`, im `tel:`-Link und im Schema als E.164
  ([[konventionen]]).
- Umlaute in Adressen umgeschrieben, in sichtbarem Text natürlich geschrieben
  ([[konventionen]]).

## Links

- Interne Links nach [[site-architecture]]: Startseite auf alle Bundesländer und die 20
  größten Städte, Bundesland auf jede seiner Städte, Stadt auf jeden Eintrag und die fünf
  nächsten Städte, Eintrag auf vier weitere seiner Stadt.
- **Brotkrumen auf jeder Seite**, fünf Ebenen auf einer Eintragsseite ([[schema]]).
- Links auf die Website eines Betriebs tragen `rel="nofollow"`, außer bei bezahlter Stufe
  ([[monetization-slots]]).
- Im Fußbereich jeder Seite: **Impressum, Datenschutz, AGB** ([[konventionen]]).
- Jeder Eintrag verlinkt `/festpreis-garantie/` oder `/festpreis-garantie/antrag/` über sein
  Garantie-Zeichen
  ([[siegel-programm]]).

## Bilder, Schriften, externe Einbindungen

- Bilder als `.webp`, unterhalb des ersten Bildschirms verzögert geladen, `alt` =
  Betriebsname plus „Schlüsseldienst" plus Stadt. **Google-Fotos werden nicht eingebunden.**
- **Schriften selbst gehostet** (`src/styles/fonts.css`), nie von Google geladen.
- **Keine Karte, kein externes Skript, keine externe Schrift ohne Einwilligung.** Google Maps
  erscheint als Platzhalterfläche mit der Schaltfläche „Karte von Google Maps laden" und einem
  Satz zur Datenübertragung; erst der Klick lädt. Das gilt auf jeder Eintragsseite, auch bei
  bezahlten Stufen ([[konventionen]]).
- Kein Google Analytics, keine Search Console auf dieser Domain
  ([[footprint-rules]]).

## Kopfbereich jeder Seite

Kanonische absolute Adresse, `robots` nach [[launch-lean]] (indexiert oder `noindex`),
`theme-color`, Open Graph und Twitter-Karte. Kein Vorabladen von einer fremden Domain.

## Seitenumbruch

Keiner in Fassung 1. Eine Stadt mit mehr als 60 Einträgen teilt nur dann nach Stadtteilen,
wenn die Daten es tragen; sonst die Karten bei 60 abschneiden (geordnet nach bezahltem Platz,
dann Festpreis-Garantie, dann Bewertung × Zahl der Bewertungen) und den Rest über einen Block
„Alle [N] Schlüsseldienste in [Stadt]" erreichbar halten. Große deutsche Städte erreichen
diese Zahl leicht, also wird der Block gebaut und nicht als Ausnahme behandelt.

## Geschwindigkeit

Statisch, kein Browser-Skript außer der Formularprüfung, der Suche auf `/suche/` und dem
Klick, der die Karte lädt. Keine eingebundene Schrift, keine eingebundene Karte beim Laden:
das ist hier zugleich die Rechtslage und der Grund, warum die Seiten schnell sind.

## Siehe auch
[[konventionen]] · [[schema]] · [[launch-lean]] · [[page-types]]
