# Stadt-Premium: drei Plätze je Stadt, Reihenfolge nach Buchung

**Datum:** 2026-11-10
**Ziel:** Das Stadt-Premium (`featured = city`) bis zu dreimal je Stadt vergeben, die Reihenfolge
im Premium-Band nach dem Buchungsdatum (frühester oben). Footprint schärfen, `/premium/`
umschreiben, die laute „nicht ausgeliefert"-Meldung ergänzen.

## Ausgangslage (vor der Änderung geprüft)

Der `FeaturedBand` rendert bereits `slots = 3` und `items.slice(0, slots)`, füllte aber je Stadt
nur **eine** Frei-Karte, egal wie viele Plätze frei waren. Die Stadtseite speist
`items={city.featured}` = `sorted.filter(isFeaturedIn)`; mehrere `featured=city` ordnete
`sortListings` nach **Bewertung**, nicht nach Buchung. `load.mjs` liest nur aus `src/data/`, nie
das Hauptbuch — das Buchungsdatum musste also als Spalte in die CSV.

## Änderungen

**Datenschicht**
- Neue CSV-Spalte `featured_seit` (Buchungsdatum des Stadt-Premium). `load.mjs` liest sie als
  `featuredSince`.
- `orderFeaturedBand()` ordnet `city.featured` nach `featuredSince` aufsteigend (früheste oben);
  ein `featured=city` ohne Datum wird mit `console.warn` gemeldet, nicht stillschweigend ans Ende
  sortiert.
- `FeaturedBand.astro`: je **freiem** Platz eine „Dieser Platz ist frei"-Karte
  (`slots − shown.length`) statt einer einzigen; die Frei-Karte sagt nicht mehr „Ein Betrieb je
  Stufe und Stadt", sondern „in der Reihenfolge der Buchung", ohne „ganz oben"-Versprechen.

**`scripts/verkauf.py`**
- Stadt-Premium bis zu **dreimal** je Stadt; die Sperre greift erst ab dem **vierten** und nennt
  die drei Halter mit Buchungsdatum.
- Setzt `featured_seit` beim Verkauf (= Buchungstag = Hauptbuch-Datum), leert sie beim Entfernen.
- Footprint unverändert streng: höchstens **ein** eigener Betrieb je Stadt auf einem bezahlten
  Platz; ein zweiter eigener Betrieb bricht ab (die geschärfte Stadt-Regel ist damit umgesetzt).
- Fehlt bei einem `featured=city` das Datum, meldet das Skript es (bei `--liste` und vor jedem
  Build) statt still zu sortieren.
- `--liste` ordnet innerhalb einer Stufe nach Buchungsdatum.
- Bei `--kein-deploy`/`--kein-bauen` schließt ein unübersehbarer Banner: „NICHT AUSGELIEFERT —
  die Live-Seite ist UNVERÄNDERT."

**Hauptbuch**: Merz Sicherheit Mannheim (premium + stadt) mit `2026-11-06` nachgetragen — der Tag,
an dem das Verzeichnis startete. `--liste` zeigt dort jetzt dieses Datum statt „unbekannt".

**`/premium/`**: Stadt-Premium ist „einer von bis zu drei Plätzen oben auf der Stadtseite, die
Reihenfolge richtet sich nach dem Zeitpunkt der Buchung". Keine „nur einer"- oder „sicher ganz
oben"-Aussage mehr (meta description, Hero-Lede, Stufenbeschreibung, Ablauf-Schritt 3). Das
Branchenwort steht jetzt in der H1, damit die Seite das Textgate besteht. **Durch das Textgate
geschickt** (`lint_copy.py … --erlaube-rechtswoerter`): **BESTANDEN**.

**`wiki/framework/footprint-rules.md`**: die geschärfte Regel festgeschrieben — „Von den drei
Plätzen einer Stadt geht höchstens einer an einen owned-Betrieb. `scripts/verkauf.py` bricht ab,
wenn ein zweiter eigener Betrieb einen Stadt-Platz bekäme." Als nicht auslegbar markiert.

## Probelauf (lokal, Scratch-Hauptbuch, ohne Live-Verkauf)

- Footprint: Stadt-Premium an einen **zweiten eigenen** Betrieb (AES Mannheim) → Abbruch.
- Stadt-Premium #2 und #3 an nicht-eigene Betriebe → erlaubt, `featured_seit` gesetzt.
- Stadt-Premium #4 → Abbruch, nennt die **drei** Halter mit Datum.
- Ein `featured=city` ohne Datum → `MELDUNG` des Skripts (nicht still ans Ende).
- `--kein-bauen`/`--kein-deploy` → lauter „NICHT AUSGELIEFERT"-Banner.
- CSV danach zurückgesetzt; einziger bezahlter Platz bleibt Merz.

## Prüfung live

- Build ohne Band-Warnung, `check_live.py … --expect-urls 2823`: **alle Prüfungen bestanden**.
- `https://…/verzeichnis/baden-wuerttemberg/mannheim/`: Merz oben, **zwei Plätze als frei**
  ausgewiesen.
- Eine Stadt ohne bezahlten Platz (Leipzig): drei freie Plätze, nichts kaputt.
- `/premium/` live: „bis zu drei", kein „Ein Betrieb je Stadt" mehr.

## Offen / Hinweis

Die drei Änderungen an `FeaturedBand.astro`, `load.mjs` und `premium.astro` liegen im Build
(`output/<slug>/site/`), der laut [[template-build-drift]] die Wahrheit ist. Für künftige
Verzeichnisse sollten dieselben Diffs nach `templates/astro/` übernommen werden; das ist hier
bewusst nicht geschehen, um den Template-Stand nicht ungefragt zu verändern.
