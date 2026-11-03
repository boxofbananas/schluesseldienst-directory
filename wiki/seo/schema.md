---
title: JSON-LD je Seitentyp
type: seo
status: current
updated: 2026-11-03
---

# JSON-LD je Seitentyp

Jede Seite gibt JSON-LD im `<head>` aus, erzeugt aus der CSV. `inLanguage` ist immer `de-DE`.

| Seite | Typen |
|---|---|
| Startseite | `WebSite` (mit `SearchAction`, weil eine Suche existiert), `Organization` (die Marke mit `publisher` = DOM Holding GmbH und `founder` = der Geschäftsführer als `Person`, [[publisher-entity]]), `ItemList` **der 16 Bundesland-Seiten**, `ItemList` der Premium-Plätze, `FAQPage` |
| Blätterseite | `CollectionPage`, `BreadcrumbList`. `noindex, follow`, deshalb keine `ItemList` |
| **Bundesland-Seite** | `CollectionPage`, `ItemList` **der Stadtseiten dieses Landes** (jedes Element eine `WebPage` mit `name` = Stadt und `url` = Stadtseite), `FAQPage` für den Fragenblock, `BreadcrumbList` |
| Stadtseite | `CollectionPage`, `ItemList` deren Elemente der Betriebstyp sind (`@id` des Betriebs auf seiner Eintragsseite, `name`, `address`, `telephone`, `url` = Eintragsseite), `FAQPage` für den Fragenblock, `BreadcrumbList` |
| Leistungsseite | `CollectionPage`, `ItemList` des Betriebstyps (die gezeigten Karten), `BreadcrumbList`; der Leistungs-Index ist eine `CollectionPage` mit einer `ItemList` der Leistungsseiten |
| Eintragsseite | Der Betriebstyp mit `address`, `geo`, `telephone`, `url` (Website des Betriebs), `openingHoursSpecification` aus `working_hours`, `makesOffer` für bestätigte Leistungen, `image` nur bei beanspruchten oder bezahlten Einträgen mit Fotos vom Inhaber ([[page-types]]); `BreadcrumbList` |
| Über uns | `AboutPage`, `Organization` (der Herausgeber mit `address`, `legalName`, Handelsregisternummer in `identifier`), `Person` (der Geschäftsführer, `worksFor` die `Organization`) |
| Impressum, Datenschutz, AGB | `WebPage` |
| Festpreis-Garantie | `WebPage`. **Kein `Rating`, kein `Award`, kein `Certification`**: die Festpreis-Garantie ist ein Versprechen des Betriebs, das das Verzeichnis veröffentlicht, und keine Prüfung durch Dritte ([[siegel-programm]]). Die garantierten Preise stehen als sichtbarer Text im Eintrag, nicht als `priceRange` oder `Offer` im Schema |
| Garantie-Nachweis | `WebPage`, `noindex` |
| Ratgeberseite | `Article` mit `author` = die `Person`, `publisher` = die `Organization`, `datePublished`, `dateModified`, `BreadcrumbList` |
| Beanspruchen, Premium, Suche | nur `WebPage` |

## Regeln

- Jede `WebPage`, `CollectionPage` und jeder Betriebstyp trägt `datePublished` (erster Build)
  und `dateModified` (Datum dieses Builds), damit jeder Neubau eine Auffrischung ist
  ([[refresh-and-upkeep]]).
- **Nirgends `aggregateRating`**, keine `Review`-Objekte. Die Sterne auf der Seite sind
  Googles Bewertung und werden als solche benannt („Bewertungen auf Google"). Googles Regeln
  für Bewertungsauszeichnungen erlauben es nicht, Bewertungen von einer anderen Website
  auszuzeichnen, und ein lokaler Betriebstyp ist für Sterne auf fremd gelieferten Bewertungen
  nicht zugelassen. Bewertungen kommen erst dann ins Schema, wenn das Verzeichnis eigene
  erhebt, was Fassung 1 nicht tut.
- Ein JSON-LD-Block je Typ. Vor Gate 6 je Seitentyp eine Stichprobe mit dem Test für
  strukturierte Daten prüfen.

## Der Betriebstyp

`niche.schemaType` in `site.json` ist der `@type` jedes gelisteten Betriebs und steht in
diesem Projekt fest auf **`Locksmith`**. Schema.org führt diesen Typ als Untertyp von
`LocalBusiness`; er passt genau und wird nicht durch etwas anderes ersetzt. Gate 4 hält ihn in
`04-plan.md` fest, erfindet aber keinen Typ.

## Brotkrumen über fünf Ebenen

Die `BreadcrumbList` einer Eintragsseite hat fünf Positionen:

```
1 Startseite            /
2 Schlüsseldienste      /verzeichnis/
3 [Bundesland]          /verzeichnis/[bundesland]/
4 [Stadt]               /verzeichnis/[bundesland]/[stadt]/
5 [Betrieb]             (aktuelle Seite, ohne item)
```

Die Stadtseite hat vier davon, die Bundesland-Seite drei, die Blätterseite zwei. Position 2
hat ein Ziel, weil `/verzeichnis/` existiert; sie darf nie auf die Startseite zeigen
([[site-architecture]]).

## Telefonnummern

Im Schema in E.164: `+496211234567`, ohne Leerzeichen und ohne führende Null. Die Seite zeigt
die lesbare Form `+49 621 1234567`. Die Umrechnung steht in [[konventionen]].

## Öffnungszeiten

`openingHoursSpecification` bildet die deutschen Tagesnamen auf `Mo` bis `Su` ab.
„Durchgehend geöffnet" und „24 Stunden" werden `00:00` bis `23:59`, „Geschlossen" entfällt
([[konventionen]]).

## Die beiden festen Einheiten

`Organization` und `Person` haben je eine `@id` für die ganze Site
(`https://die-besten-schluesseldienste.de/#herausgeber` und `.../#person`), sodass die
Auszeichnung jeder Seite auf dieselben zwei Einheiten zeigt.

## Siehe auch
[[konventionen]] · [[on-page-rules]] · [[page-types]] · [[publisher-entity]]
