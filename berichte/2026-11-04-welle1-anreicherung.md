# Welle-1-Anreicherung (2026-11-04)

## Lauf
`run_batches.py enrich` auf Sonnet, 27 Stapel:
- **27 Stapel bestanden, 0 durchgefallen, 0 Wiederholungen**, **851 Einträge** beantwortet.
- **39,19 $** von claude -p gemeldet, **45,7 Mio. Token**, **4,6 ct/Eintrag**, **63 min 43 s**.
- Deckt sich mit der Schätzung (~40 $). Abgerechnet über das Claude-Abo.

## Zusammenbau
`merge_enriched.py` über den erweiterten Datensatz:
- `03-listings-enriched.csv`: **4.379 Zeilen**, davon **3.521 angereichert** (2.670 aus Gate 3 +
  851 Welle 1), 858 Grundeinträge. 2 verwaiste Antworten übersprungen (bekannt: Königstein,
  Frankenthal).

## Build nach Ausschluss (`apply_exclusions` → `site/src/data/listings.csv`)
- **3.937 Einträge** (442 gedroppt: 431 fremde Gewerbe + 11 Ketten).
- **nicht dünn (thin=false): 2.268** (vor Welle 1: 1.818) — die Welle-1-Einträge mit ≥ 5
  Bewertungen und Beschreibung sind jetzt startfähig.
- dünn (noindex-Start): 1.669; mit Beschreibung insgesamt: 3.080.

## Start-Sitemap (echte Struktur, nach Welle 1)
1 Start + 16 Bundesländer + **595 Stadtseiten** + **133 indexierbare Einzelseiten** +
**2.268 Eintragsseiten (thin=false)** + 7 Leistungen + 2 Vertrauensseiten ≈ **3.022 Seiten**.
Außerhalb der Start-Sitemap (Tranchen nach 30 Tagen): 77 Einzelseiten ohne Nachbarn, die restlichen
dünnen Einträge, und **Welle 2** (545 Einträge: 246 Stufe A außerhalb der Start-Sitemap + 299
Stufe B), die hinter der 30-Tage-Prüfung angereichert wird.

## Stand
Welle 1 ist live-fähig angereichert. Zwei Bauaufgaben sind jetzt frei (beide waren an „Welle 1
durch + Zahlen vorgelegt" bzw. an die stated-next-Reihenfolge gebunden):
- **Stadttext-Probestapel** (Sonnet vs. kleineres Modell, 20 Städte) — der ursprünglich als
  Nächstes genannte Schritt.
- **Formularannahme-Function** (Pages Function + KV, Spec in
  `berichte/2026-11-04-formularannahme-spec.md`) — Code/Config/Wiki; die Cloudflare-Konto-Teile
  (KV-Namespace, verifizierte Adresse) bleiben für Daniel offen.
</content>
