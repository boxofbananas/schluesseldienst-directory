# Anreicherung der neun leeren Garantie-Seiten (Gate-3-Weg)

**Datum:** 2026-11-06
**Auslöser:** Daniel — die neun Garantie-Betriebe ohne Beschreibung anreichern. Sie kamen über
`eigene-betriebe.csv` nach und haben Gate 3 nie durchlaufen. Alle neun haben eine eigene Website.
Dieselben Gate-3-Regeln ohne Ausnahme, kein werblicher Ton, weil es eigene Betriebe sind.

## Die neun

AES Mannheim · I-S-E Hockenheim · Mein Schlüsseldienst Weinheim · Merz Ludwigshafen ·
Merz Speyer · Merz Worms · Rheinpfalz Frankenthal · Riegelklar Schwetzingen · Sperber Heidelberg.

## Weg und Kosten

Scratch-Ordner `output/schluesseldienste-deutschland/03-own9/`. Kein Export-Text vorhanden
(`about`, `reviews_tags`, `description`, `subtypes` je 0 Zeichen), also Belege allein aus den
Websites.

- `fetch_sites.py` → 9/9 gelesen (kostenlos).
- `build_evidence.py --patterns 03-attributes.json` → 9 Belegpakete (kostenlos).
- `make_batches.py --attributes 03-attributes.json` → 1 Stapel, 9 Einträge, ~14.800 Token (kostenlos).
- **Beantwortung inline** durch mich, kein zusätzlicher API-Aufwand (statt ~36 Cent über
  `run_batches.py` auf Sonnet). Kosten vor der Anreicherung genannt.

## Regeln eingehalten

Dritte Person, keine Leseransprache, keine Quellenangabe (kein „laut Website"; „nach eigener
Angabe" für Selbstauskünfte ist zulässig, „nach eigener Darstellung" lehnt der Linter ab),
keine Preise/Beträge/Prozente, keine Kontaktdaten im Text, keine Lizenz- oder
Zertifizierungsbehauptung (IHK-Mitgliedschaft und ELOCK2-Arbeit als Selbstauskunft erlaubt),
keine Gedankenstriche. **Kein freundlicherer Ton**, obwohl es eigene Betriebe sind: dieselbe
nüchterne Stimme wie bei den 3.790 fremden Einträgen.

Satzanfänge geprüft: alle neun Anfänge kommen bei den bestehenden 2.197 angereicherten
Beschreibungen **0-mal** vor (Schwelle: 4 teilen scheitert).

## Prüfung (`merge_enriched.py`)

Erster Lauf: 9/9 scheiterten (Texte 100–122 Wörter unter der Spanne 120–200; „nach eigener
Darstellung" als Quellenangabe; „am Telefon" als Kontaktdatum; Sperber `anfahrtspauschale_genannt`
und Ludwigshafen `gewerblich_objektbetreuung` ohne belegten Beleg). Nachgebessert: Texte mit
echten Paketfakten auf 121–139 Wörter, „Telefon"/„Darstellung" entfernt, Sperber-Anfahrt mit
Beleg-Trace (`zum Festpreis von nur 89 € inkl. Anfahrt an`) gestützt, Ludwigshafen-Gewerbe auf
„keine Angabe" gesetzt. Zweiter Lauf: **9/9 bestanden, 0 Fehler.**

Merkmalsverteilung (true/false/keine Angabe): kern 9/0/0, notdienst 9/0/0, tueroeffnung 9/0/0,
schlossaustausch 8/0/1, schliessanlagen 9/0/0, einbruchschutz 9/0/0, autoschluessel 5/0/4,
tresoroeffnung 0/0/9, schluessel_nachmachen 0/0/9, elektronische_schliesssysteme 3/0/6,
ladengeschaeft 0/0/9, festpreis_genannt 9/0/0, anfahrtspauschale_genannt 5/0/4,
gewerblich_objektbetreuung 6/0/3.

## Übertragung und Build

`description_enriched` und die 14 Merkmalsspalten je Slug in
`site/src/data/listings.csv` und in `03-listings-enriched.csv` übertragen; Garantie-Spalten
(`geprueft`, `garantie_tag`, Zuschläge, Material) unverändert. `npm run build` ohne Warnung,
Schriftprüfung bestanden.

## Sitemap und Live

Die Bedingung `geprueft && description` greift ohne weitere Codeänderung: die neun rutschen von
selbst aus der `thin`-Sperre in die Sitemap.

- **Sitemap 2814 → 2823**, Differenz sind genau die neun Eintragsseiten (Set-Vergleich lokal gegen
  Live bestätigt).
- `check_live.py` mit `--expect-urls 2823`: **alle Prüfungen bestanden**, www-Zeile grün.
- Jede der neun Seiten live: `index, follow`, in der Sitemap, mit Beschreibung und Garantie-Zeile
  „Türöffnung ab <garantie_tag> €" (89/99 €). Kein `aggregateRating`, `featuredPreview` false.

## Stand

Alle 18 Garantie-Betriebe tragen jetzt Inhalt und stehen indexiert in der ersten Stufe. Die in
`06-launch.md` vermerkte Lücke („9 leere Garantie-Seiten ziehen nach, sobald sie eine Beschreibung
bekommen") ist geschlossen.
