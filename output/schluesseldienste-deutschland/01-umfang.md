---
title: Gate 1 – Umfang
type: output
status: wartet-auf-freigabe
updated: 2026-11-03
---

# Gate 1 – Umfang

## Feste Angaben (aus [[konventionen]] übernommen, nicht abgefragt)

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

## 1. Eigene Websites und Betriebe

21 eigene Websites, davon 10 mit bekannter Telefonnummer. In Gate 2 füllen sie die Spalte
`owned` und werden **wie jeder andere Betrieb gelistet** ([[footprint-rules]]). Erkennung über
**beide** Schalter von `clean_listings.py` (am 2026-11-03 per `--help` bestätigt: beide
vorhanden):

- `--owned-phones` – die 10 bekannten Nummern
- `--owned-domains` – alle 21 Websites (die 11 ohne Nummer werden nur über die Website erkannt)

**Hauptfirma: Merz Sicherheit in Mannheim (`merz-sicherheit.de`).** Mannheim ist die wichtigste
Stadt. Dort ist **nach dem Start** ein bezahlter Platz (Premium + Top-Platzierung) zum
**öffentlichen Preis** vorgesehen, als normaler Vorgang nach [[footprint-rules]] und erst
nachdem der Betrieb die Festpreis-Garantie beantragt und bestanden hat wie jeder andere.

### `--owned-domains` (alle 21)

```
merz-sicherheit.de,schluesseldienstheidelberg.de,schluesseldienstmannheim.de,schluesseldienstworms.de,schluesseldienstludwigshafen.de,schluesseldienst-weinheim.de,ise-schluesseldienst.de,schluesseldienst-speyer.de,heidelberg-schluesseldienst.de,schluesseldienst-hockenheim.de,schluesseldienstwiesloch.de,schluesseldienstwaghaeusel.de,schluesseldienstviernheim.de,sinsheim-schluesseldienst.de,schluesseldienstschwetzingen.de,schluesseldienstneustadt.de,schluesseldienstleimen.de,schluesseldienstlandau.de,schluesseldienst-lampertheim.de,frankenthal-schluesseldienst.de,schluesseldienst-bensheim.de
```

### `--owned-phones` (10 bekannte)

```
06221-3574913,06205-3029698,01556-3825645,01556-3825820,01556-3825821,0155-63825636,0155-63825819,01556-3825646,0155-63825823,01556-5796853
```

### Zuordnung Website → Ort (für den Gate-2-Bericht)

| Website | Ort | Telefon |
|---|---|---|
| merz-sicherheit.de | Mannheim (Hauptfirma) | über Website |
| schluesseldienstmannheim.de | Mannheim | über Website |
| schluesseldienstheidelberg.de | Heidelberg | über Website |
| heidelberg-schluesseldienst.de | Heidelberg, Czernyring 2 | 06221-3574913 |
| schluesseldienstworms.de | Worms | über Website |
| schluesseldienstludwigshafen.de | Ludwigshafen | über Website |
| schluesseldienst-weinheim.de | Weinheim | über Website |
| ise-schluesseldienst.de | — | über Website |
| schluesseldienst-speyer.de | Speyer | über Website |
| schluesseldienst-hockenheim.de | Hockenheim, Ringstraße 24 | 06205-3029698 |
| schluesseldienstwiesloch.de | Wiesloch, Adelsförsterpfad 5 | 01556-3825645 |
| schluesseldienstwaghaeusel.de | Waghäusel, Goethestraße 61 | 01556-3825820 |
| schluesseldienstviernheim.de | Viernheim, Mannheimer Straße 93 | keine |
| sinsheim-schluesseldienst.de | Sinsheim, Am Leitzelbach 20 | 01556-3825821 |
| schluesseldienstschwetzingen.de | Schwetzingen, Carl-Benz-Straße 9–11 | 0155-63825636 |
| schluesseldienstneustadt.de | Neustadt a. d. Weinstraße, Stangenbrunnengasse 7 | 0155-63825819 |
| schluesseldienstleimen.de | Leimen, Römerstraße 2–4 | keine |
| schluesseldienstlandau.de | Landau i. d. Pfalz, Marktstraße 35 | 01556-3825646 |
| schluesseldienst-lampertheim.de | Lampertheim, Wilhelmstraße 46 | keine |
| frankenthal-schluesseldienst.de | Frankenthal, Johann-Klein-Straße 57 | 0155-63825823 |
| schluesseldienst-bensheim.de | Bensheim, Unteres Grabengässchen 4 | 01556-5796853 |

## 2. Optik

**Optik des Templates** (Vorgabe). Die Gestaltungsmarken des Referenzbaus
(`templates/master-reference/site/` bzw. `templates/astro/`) werden unverändert übernommen;
keine fremde Optikvorlage. Gate 4 leitet daraus keine abweichenden Marken ab
([[design-seed]]).

## 3. Datenquelle

**Weg 1, DataForSEO — abgerufen am 03.11.2026.** Freigabe „1, abrufen" erteilt.

Ergebnis (`input/listings-raw.csv`, Bericht `input/listings-raw-report.md`):
- **3.102 Zeilen** geschrieben, gemeldete Kosten **1,1771 $**.
- 1.266 Städte; 861 Zeilen mit mindestens einer E-Mail-Adresse.
- `last_updated_time` von 2023-05-24 bis 2026-10-07 (Alter des Bestands, keine Tagesabfrage).
- 1.843 Zeilen tragen `locksmith` als primäre Kategorie; die übrigen als Nebenkategorie —
  Gate 2 behält sie und berichtet nach primärem Typ, Gate 4 entscheidet.
- Bundesland im Rohdatenfeld leer (siehe Auffälligkeit unten); Gate 2 ordnet zu.

Vorarbeit:
- DataForSEO-Anmeldung auf diesem Rechner gespeichert (`connect_dataforseo.py --check`: ja).
- Kategorie-Kennung: `locksmith` (108.803 Betriebe weltweit). Nebenkennung
  `emergency_locksmith_service` existiert, wird aber nicht benutzt – die Branche steht
  vertraglich auf `locksmith` ([[konventionen]]).
- **Schätzung (`fetch_dataforseo.py --estimate --category locksmith --country Germany`):**
  **3.102 Einträge** (Bewertungen ≥ 1), Abruf in 4 Anfragen, voraussichtliche Kosten
  **etwa 1,16 $ (≈ 1 €)**; mindestens 456 Städte in der 1.000er-Stichprobe; 59 % tragen
  `locksmith` als primäre Kategorie, 79 % haben eine Website; keine Branchen-Warnung. Die
  Schätzanfrage selbst hat 0,40 $ gekostet.

Datenauffälligkeit für Gate 2/4: DataForSEO füllt `address_info.region` für die deutschen
Zeilen nicht (die ganze 1.000er-Stichprobe ist leer). Die Zuordnung zum **Bundesland**
übernimmt deshalb Gate 2 (`clean_listings.py`, [[listings-cleaning]]), nicht der Abruf; ein
`--region`-Filter auf das Rohdaten-Feld brächte nichts. Der bundesweite Lauf braucht ihn auch
nicht (4 Anfragen genügen).

**Scriptkorrektur am 2026-11-03:** `fetch_dataforseo.py` filterte das Land über das
ungültige Feld `address_info.country` und lief auf `40501 Invalid Field: 'filters'`. Gültig
ist `address_info.country_code` mit ISO-Code (`DE`). Behoben (Tabelle `COUNTRY_CODES` +
Funktion `country_code`), mit `locksmith`/`Germany` verifiziert. Siehe `wiki/log.md`.

## Offen vor Gate 5

- Lebenslauf und Bild des Geschäftsführers (für „Über uns")
- Kontakt-E-Mail-Adresse auf der Domain
- Umsatzsteuer-Identifikationsnummer für das Impressum
- Stripe-Zahlungslinks der Stufen
</content>
</invoke>
