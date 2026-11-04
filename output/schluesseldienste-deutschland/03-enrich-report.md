---
title: Gate 3 – Anreichern (Bericht)
type: output
status: wartet-auf-freigabe
updated: 2026-11-04
---

# Gate 3 – Anreichern: Bericht

## Umfang (geändert gegenüber der Vorab-Vorgabe)

Statt „nur BW/RP/HE + 30 Städte" (Vorgabe in [[konventionen]]) wurden auf Wunsch des Betreibers
**alle Einträge mit Belegbasis** angereichert.

- Eingang aus Gate 2: **2.912** bereinigte Einträge, dazu **12 eigene Betriebe** nachgetragen
  (`add_own_listings.py`, [[eigene-betriebe]]) → **2.924**.
- **Belegbasis** (Maps-Text oder lesbare eigene Website): **2.672 angereichert**.
- **Ohne jeden Beleg: 252 → Grundeinträge** (Name, Adresse, Telefon, Bewertung; jedes Merkmal
  „keine Angabe", keine Beschreibung). Davon 196 ohne Website, 56 mit geblockter/leerer/toter
  Website.

Ergebnisdatei: `03-listings-enriched.csv` (2.924 Zeilen: 2.672 angereichert, 252 Grundeinträge).

## Merkmalsdatei

`03-attributes.json`, **14 Merkmale**, Kernarbeit = `schluesseldienst_kern` (`core: true`).
Sechs tragen einen `service`-Block (die sechs Leistungsseiten für Gate 4): Notdienst,
Türöffnung, Schließanlagen, Einbruchschutz, Autoschlüssel, Tresoröffnung. Kein Merkmal behauptet
Lizenz/Zulassung/Zertifizierung (gibt es im Gewerbe nicht).

## Website-Abruf (`fetch_sites.py`)

| Zustand | Einträge |
|---|---|
| lesbar (ok) | 1.915 |
| keine Website | 581 |
| gesperrt / Fehler (HTTP 4xx/5xx) | 275 |
| leer / JS-gerendert | 85 |
| nicht erreichbar (SSL/DNS/Timeout) | 44 |
| anderes | 24 |

Mit lesbarem Seitentext: rund **2.000**. Eine Kodierungs- und gzip-Korrektur in `fetch_sites.py`
(siehe unten) hat 48 vorher unbrauchbare (Mojibake/Binär) Seiten auf 1 reduziert.

## Belege und Stapel

`build_evidence.py`: ~**2,23 Mio. Token** Belegmaterial, 761 Token je Eintrag, 2.000 mit
lesbarer Website. `make_batches.py`: 1 Probestapel (20) + **86 Stapel** (2.652) für den vollen
Lauf.

## Läufe (`run_batches.py`, Sonnet, Claude-Abo)

- Probeläufe: 40er (mit Preisen – verworfen), dann 20er mit den geschärften Regeln: 20/20
  bestanden, 0 Verletzungen.
- **Voller Lauf: 86 Stapel bestanden, 0 durchgefallen, 0 Wiederholungen**, 2.652 Einträge.
- Der Betreiber-Auflage (Abbruch bei >5 % durchgefallenen Stapeln) wurde per Monitor überwacht;
  sie griff nicht (0 %).

### Verbrauch gegen die Hochrechnung

| | Hochrechnung | Tatsächlich |
|---|---|---|
| Kosten-Äquivalent | ~130 $ | **123,06 $** (voller Lauf) |
| je Eintrag | ~4,9 ct | **4,6 ct** |
| Token | ~133 Mio. | **131,96 Mio.** (überwiegend Cache-Reads) |
| Laufzeit (3 Läufer) | ~2,5–3 h | **3 h 12 min** |

Mit den zwei Probeläufen zusammen: ~**125,8 $-Äquivalent**, ~135,5 Mio. Token. Abgerechnet
über das Claude-Abo (Wochenkontingent), keine Dollar-Rechnung. Token je Stapel stehen in
`03-cache/runner-replies.log`.

## Merkmalszählung (wahr / falsch / keine Angabe)

| Merkmal | wahr | falsch | keine Angabe |
|---|---:|---:|---:|
| schluesseldienst_kern (Kern) | 1.432 | **507** | 733 |
| notdienst_24h | 1.166 | 17 | 1.489 |
| tueroeffnung | 1.259 | 4 | 1.409 |
| schlossaustausch | 905 | 0 | 1.767 |
| schliessanlagen | 1.060 | 0 | 1.612 |
| einbruchschutz | 997 | 0 | 1.675 |
| autoschluessel | 710 | 6 | 1.956 |
| tresoroeffnung | 292 | 7 | 2.373 |
| schluessel_nachmachen | 1.119 | 15 | 1.538 |
| elektronische_schliesssysteme | 526 | 1 | 2.145 |
| ladengeschaeft | 825 | 28 | 1.819 |
| festpreis_genannt | 647 | 1 | 2.024 |
| anfahrtspauschale_genannt | 168 | 0 | 2.504 |
| gewerblich_objektbetreuung | 683 | 0 | 1.989 |

(Zählung über die 2.672 angereicherten; die 252 Grundeinträge stehen durchweg auf „keine
Angabe".)

## Dünne Einträge

Vor dem Lauf 1.020, **nach dem Lauf 741**: 279 Einträge mit ≥ 5 Bewertungen haben über ihre
Website echten Text bekommen und gelten nicht mehr als dünn. Die 741 (inkl. der 252
Grundeinträge) starten nach [[launch-lean]] auf `noindex`.

## Für Gate 4: die Kernarbeits-Entscheidung

**507 Einträge antworten `schluesseldienst_kern: false`** – sie machen laut eigener Darstellung
keine Türöffnung/Schließtechnik. Nach Haupt-Kategorie:

| Haupt-Kategorie (`type`) | core=false |
|---|---:|
| Home improvement store (Baumarkt) | 181 |
| Locksmith | 75 |
| Metal construction company (Metallbau) | 62 |
| Shoe repair shop (Schuhmacher) | 16 |
| Tool store | 9 |
| Janitorial service | 9 |
| Steel construction company | 8 |
| Car repair and maintenance service | 6 |
| Metal fabricator | 6 |
| übrige | 135 |

Bemerkenswert: **75 Einträge mit primärer Kategorie `Locksmith`** antworten dennoch
`kern: false` – ihre eigene Website beschreibt nur Schlüsselanfertigung, Handel oder ein anderes
Gewerk. Die Vorgabe des Betreibers (ausschließen, außer `kern: true`) trifft in Gate 4 auf
diese 507; der Blueprint löscht nichts von selbst ([[listings-cleaning]]).

## Notizen der Läufer (`03-cache/review.md`, 737 Einzelnotizen)

Wiederkehrende Unsicherheiten, die keine Prüfliste fängt:

- **313 Notizen zur Kernarbeit** – Begründung je Eintrag, warum `false`/`keine Angabe` (fremdes
  Gewerk, nur Handelsware, Schlüsseldienst nur als Banner/Nebenzeile).
- **69 Einträge ohne lesbare Website / nur Maps-Text** – durchweg „keine Angabe", soweit der
  Maps-Text nichts belegt.
- **62 dünne Beschreibungen** an der Wortuntergrenze „etwas gestreckt" (dünne Pakete).
- **22 Einträge mit HTTP 503** – Antworten nur aus dem Maps-Text.
- **5 Vermittler/Vendor-Fälle** (Portal statt ausführendem Betrieb; z. B. ADAC-Reisebüro mit
  Schlüsselnotdienst-Banner, `schluesselfix`).
- Einzelne **Namens-/Slug-Abweichungen**: der Eintragsname aus Google passt nicht zur Firma auf
  der Website (siehe unten).

## Offene Punkte / für Gate 4 vorzulegen

1. **Kernarbeit `false` (507)** – Entscheidung je Gruppe (ausschließen nach `04-exclusions.csv`
   oder behalten), insbesondere die 75 `Locksmith` mit `kern: false`.
2. **Schlechte Eintragsnamen** – keyword-gefüllte Google-Namen, z. B. „Sicherheitsberater für
   Mechanische Nachrüstung von Fenster und Türen" (Goslar), echter Firmenname laut Website
   „Schlüsseldienst Meineke". Gate 4 entscheidet über Umbenennen/Ausschluss.
3. **252 Grundeinträge** bleiben ohne Beschreibung; nach der 30-Tage-Prüfung in Tranchen
   nachziehbar, sobald Websites lesbar werden.
4. **Vermittler/Callcenter** (Gate-2-Listen + die 5 Vendor-Notizen) – Voraussetzung 5 der
   Festpreis-Garantie, Entscheidung in Gate 4.

## Skriptkorrekturen in diesem Gate

1. `fetch_sites.py`: UTF-8-zuerst-Dekoder + gzip/deflate-Entpacken (Mojibake 48 → 1).
2. `make_batches.py`: verträgt Zeilen ohne Bewertung („rating: none" für eigene Betriebe).
3. `run_batches.py`: protokolliert echte Token je Stapel.
4. `merge_enriched.py`: sechs neue Textprüfungen (Preise/Prozent, Bewertung, Kontaktdaten,
   Leseransprache, Karriere/Partner, Google-Ausstattungsmerkmale) + `--basic-unanswered` für
   Läufe, die absichtlich nur Einträge mit Beleg anreichern.
5. `enrichment-instructions.md`: dieselben sechs Regeln geschärft; alte Regeln (Bewertungszeile
   verlangt, Website-Preise erlaubt) entfernt.

## Ergebnis

`03-listings-enriched.csv`, `03-attributes.json`, `03-enrich-report.md`.
**Wartet auf:** Durchsicht von `03-cache/review.md` und Freigabe, dann Gate 4 (Planen).
</content>
