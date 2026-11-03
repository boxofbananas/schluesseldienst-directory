---
title: Aufbau und Adressen
type: framework
status: current
updated: 2026-11-03
---

# Aufbau und Adressen

Eine Branche, ein Land, **drei Ortsebenen**: Deutschland → bis 16 Bundesländer → Städte →
Einträge. Die englische Fassung kannte nur einen Bundesstaat mit Städten darunter; diese
Zwischenebene ist neu und tragend.

Die URL-Tabelle in [[konventionen]] ist maßgeblich. Unten steht, was jede Ebene leistet.

## Die Ebenen

| Ebene | Adresse | Anzahl | Rankt für |
|---|---|---|---|
| Startseite | `/` | 1 | „Schlüsseldienst", „Schlüsseldienst in meiner Nähe" bundesweit |
| Blättern | `/verzeichnis/` | 1 | nichts, `noindex, follow`: Suchfeld, alle Bundesländer, alle Städte von A bis Z |
| Bundesland | `/verzeichnis/[bundesland]/` | bis 16 | „Schlüsseldienst [Bundesland]"; verlinkt jede Stadt des Landes |
| Stadt | `/verzeichnis/[bundesland]/[stadt]/` | je Stadt ab Mindestzahl | „Schlüsseldienst [Stadt]", „Schlüsseldienst [Stadt] Notdienst" – die Geldseite |
| Eintrag | `/firma/[bundesland]/[stadt]/[slug]/` | je behaltenem Eintrag | Firmenname plus Leistung, der lange Schwanz |
| Leistung | `/leistungen/[slug]/`, Index `/leistungen/` | je Leistung aus dem Plan | „[Leistung] Schlüsseldienst": alle bestätigten Einträge, die besten als Karten, dann jedes Bundesland mit seiner Zahl |
| Eintrag beanspruchen | `/eintrag-beanspruchen/` | 1 | Umwandlung, nicht Ranking |
| Premium / Werbung | `/premium/` | 1 | Umwandlung, nicht Ranking |
| Festpreis-Garantie | `/festpreis-garantie/` | 1 | Vertrauen, Pflichtveröffentlichung ([[siegel-programm]]) |
| Garantie-Antrag | `/festpreis-garantie/antrag/` | 1 | Umwandlung; Ziel jedes „Noch keine Festpreis-Garantie" |
| Garantie-Nachweis | `/auszeichnung/[slug]/`, Bild `/auszeichnung/[slug].svg` | je Betrieb mit Garantie | nichts, `noindex` |
| Über uns | `/ueber-uns/` | 1 | der Herausgeber, Vertrauen für den Anruf ([[publisher-entity]]) |
| Kontakt | `/kontakt/` | 1 | Korrektur- und Löschweg ([[refresh-and-upkeep]]) |
| Impressum | `/impressum/` | 1 | Pflicht nach § 5 DDG |
| Datenschutz | `/datenschutz/` | 1 | Pflicht nach Art. 13 DSGVO |
| AGB | `/agb/` | 1 | Pflicht für die bezahlten Stufen |
| Suche | `/suche/` | 1 | nichts, `noindex` |
| Ratgeber | `/ratgeber/[slug]/` | 0 zum Start | verlinkbare Nachschlageseiten ([[authority-and-links]]) |

## Seitenzahlen

Die Zahl der Seiten ergibt sich aus den Daten und steht in `04-plan.md`. Die Rechnung:

```
1 Startseite
+ 1 Blätterseite
+ Zahl der Bundesländer mit mindestens einer Stadtseite       (bis 16)
+ Zahl der Städte über der Mindestzahl
+ Zahl der Ortsseiten, die foldMaxKm freistellt
+ Zahl der behaltenen Einträge
+ Zahl der Leistungsseiten + 1 Index
+ 1 Nachweisseite je Betrieb mit Garantie                     (noindex)
+ 12 feste Seiten (Beanspruchen, Premium, Festpreis-Garantie, Garantie-Antrag, Über uns,
  Kontakt, Impressum, Datenschutz, AGB, Suche, Ratgeber-Index, 404)
```

Gate 4 füllt diese Rechnung mit echten Zahlen und nennt sie im Plan. Es gibt noch keine
deutschen Erfahrungswerte; der englische Pilot (ein Verzeichnis für Poolbauer in Florida)
hatte 1.557 Einträge und 1.719 Seiten mit zwei Ortsebenen, was für die Größenordnung nichts
hergibt, weil Deutschland eine Ebene mehr und ein anderes Städtebild hat.

## Adressregeln

- Ortsseiten liegen unter `/verzeichnis/`, Firmenseiten unter `/firma/`, beide gefolgt vom
  Bundesland-Slug und der Stadt. Die Bundesland-Slugs stehen in [[konventionen]] und kommen
  aus `site.json` → `regions`; sie werden nie geraten.
- `/verzeichnis/` ist die Blätterseite (Suche, alle Bundesländer, alle Städte, alle Einträge),
  `noindex, follow`, damit die Brotkrumenebene „Schlüsseldienste" ein Ziel hat
  (Startseite / Schlüsseldienste / Bayern / Nürnberg / Betrieb) ohne eine zweite Kopie der
  Startseite. Sie trägt keinen Text der Startseite, damit die beiden nie konkurrieren.
- `/firma/`, `/firma/[bundesland]/` und `/firma/[bundesland]/[stadt]/` leiten über
  `dist/_redirects` auf die passende Verzeichnisseite.
- Kleinschreibung, Bindestriche, Schrägstrich am Ende, kein `.html`, keine Abfrageparameter
  für Filter. Jede Filterkombination, die ranken soll, ist eine **echte Seite**.
- **Umlaute vor dem Entfernen der Sonderzeichen umschreiben** (`ä→ae`, `ö→oe`, `ü→ue`,
  `ß→ss`), sonst wird aus „Nürnberg" `n-rnberg` ([[konventionen]]). Zwei Städte gleichen
  Namens im gleichen Bundesland: Postleitzahl anhängen.
- `slug` eines Eintrags = `[name]-[stadt]`, umgeschrieben; bei Kollision die Postleitzahl
  anhängen.
- Leistungsseiten sind bundesweit. Leistung je Stadt (`/leistungen/[leistung]/[stadt]/`) wird
  nicht gebaut: die meisten solchen Seiten hielten einen oder zwei Einträge. Die
  Leistungsseite verlinkt stattdessen jedes Bundesland mit seiner Zahl, und die Stadtseite
  beantwortet die Leistungsfrage für ihren Ort in den häufigen Fragen.
- Keine Eintragsseite ist eine Sackgasse: jede verlinkt vier weitere Einträge ihrer Stadt (die
  nächsten vier in der Reihenfolge der Stadt, umlaufend, sodass jeder Eintrag von vier anderen
  verlinkt wird), ihre Stadtseite und die Leistungsseiten, auf denen sie vorkommt.
- Kanonische absolute Adresse auf jeder Seite.

## Interne Verlinkung über drei Ebenen

- **Startseite** verlinkt **alle Bundesländer** (eine Karte je Bundesland mit Zahl der
  Einträge und Zahl der Städte) und die **20 größten Städte** direkt. Beides, damit die
  Zwischenebene nicht die großen Städte verschluckt.
- **Bundesland-Seite** verlinkt **jede Stadt des Landes** mit ihrer Zahl, dazu die
  „Kleineren Orte" (Ortsseiten unter der Mindestzahl, die `foldMaxKm` freistellt), die
  Startseite und die Nachbar-Bundesländer.
- **Stadtseite** verlinkt jeden Eintrag der Stadt (bezahlte Plätze zuerst), die nächsten fünf
  Städte nach Koordinaten – **auch über die Landesgrenze hinweg**, weil ein Leser in
  Mannheim nach Ludwigshafen schaut und nicht auf das Bundesland achtet – und hinauf zur
  Bundesland-Seite.
- **Eintragsseite** verlinkt ihre Stadtseite, die Seite zum Beanspruchen und, je nach Garantie,
  `/festpreis-garantie/` oder `/festpreis-garantie/antrag/` ([[siegel-programm]]). Links auf die Website des Betriebs
  tragen **`rel="nofollow"`**; bezahlte Stufen bekommen einen gefolgten Link (das ist Teil
  dessen, was die Stufe kauft, [[monetization-slots]]).
- **Brotkrumen auf jeder Seite**, fünf Ebenen auf einer Eintragsseite, auch als
  `BreadcrumbList` ([[schema]]).
- Ratgeberseiten verlinken die Stadtseiten, um die es geht, und werden von dort und aus dem
  Fußbereich verlinkt. Eine Adresse mit eingehendem Link wird nie geändert
  ([[authority-and-links]]).
- **Eigene Websites werden genauso behandelt wie jeder andere Eintrag** ([[footprint-rules]]).

## Mindestzahl, Zusammenlegen und `foldMaxKm`

- Eine Stadt bekommt eine Seite ab **3 Einträgen**. Städte darunter werden der nächsten Stadt
  mit Seite zugeschlagen.
- `foldMaxKm` in `site.json`: ein Ort unter der Mindestzahl, der weiter als dieser Wert von
  jeder Stadt mit Seite entfernt liegt, wird **nicht** zugeschlagen. Er bekommt eine eigene
  Seite, indexiert und in der Sitemap wie jede Stadtseite, steht auf der Bundesland-Seite
  unter „Kleinere Orte" und bleibt aus Navigation und Startseitenraster heraus. Er braucht
  einen Eintrag in `city-copy.json` mit der Untergrenze von 120 Wörtern ([[page-types]]).
- **Vorgabe: 40 km**, der Wert aus dem englischen Pilotprojekt. Gate 4 darf ihn ändern und
  nennt dabei die Zahl der Ortsseiten, die daraus entstehen. Für Deutschland ist 40 km eher
  großzügig: die Siedlungsdichte ist höher als in Florida oder Colorado, ein Leser 40 km von
  der nächsten Stadtseite nennt diese Seite nicht „in meiner Nähe". Gate 4 prüft das an den
  Daten, bevor es den Wert übernimmt.
- `sortAttribute` in `site.json`: Einträge, bei denen dieses Merkmal wahr ist, stehen vor den
  übrigen, hinter den bezahlten Plätzen. Wahlweise.
- Entscheidungen aus Gate 4, die Einträge entfernen oder verändern, stehen in
  `04-exclusions.csv` und werden von `scripts/apply_exclusions.py` angewandt, wenn die
  Einträge in die Site kopiert werden. Die angereicherte CSV wird nie bearbeitet. Jede Zeile
  ist eine Entscheidung des Menschen; der Blueprint hat keinen Vorgabewert, der eine Gruppe
  von Einträgen löscht ([[listings-cleaning]]).

## Navigation

Kopfzeile: Wortmarke links (der Link zur Startseite, kein eigener Punkt „Startseite"), dann
„Schlüsseldienste" (auf `/verzeichnis/`), „Festpreis-Garantie" (auf `/festpreis-garantie/`),
„Über uns", „Kontakt"
und eine Schaltfläche „Eintrag beanspruchen". Die größten Städte und alle Bundesländer stehen
im Fußbereich, nicht in der Navigation.

Fußbereich, vier Spalten: Über uns mit der Herausgeberzeile, Schnelllinks (Beanspruchen,
Premium, Festpreis-Garantie, Leistungen wenn vorhanden), die 16 Bundesländer, Kontakt. Darunter die
Rechtszeile mit **Impressum**, **Datenschutz** und **AGB** – auf jeder Seite, ohne Ausnahme
([[konventionen]], Recht).

## Siehe auch
[[konventionen]] · [[page-types]] · [[page-sections]] · [[on-page-rules]] · [[siegel-programm]]
