# Zwei Mannheimer Einträge entfernt (Betreiberentscheidung)

**Datum:** 2026-11-12 · **Branch:** `main` (live) · **Deploy:** `9f0ec5a5` · **Projekt:** `schluesseldienste-deutschland`

Betreiberentscheidung. Ausschluss nach [[conduct-exclusions]] mit dem dort vorgesehenen Code, wie bei
den früheren Betreiberausschlüssen. Kein Vorfall, kein Grund — weder in der CSV noch hier, im Log oder
in der Commit-Nachricht.

## Ausschluss

Beide Slugs trafen vorab **genau eine Zeile** (geprüft in `03-listings-enriched.csv` und in der
Build-`listings.csv`). In `04-exclusions.csv` angefügt, nur mit Code:

```
tuerengel-schluesseldienst-mannheim-mannheim,drop,verhalten_betreiber
schluesseldienst-vetter-schliess-und-sicherheitstechnik-mannheim,drop,verhalten_betreiber
```

Danach die zwei Zeilen CSV-sicher aus `site/src/data/listings.csv` entfernt (Mehrzeilenfelder, daher
mit CSV-Parser; `git diff` zeigt `0 insertions, 8 deletions`, keine Umformatierung, alle
Garantie-/Verkaufsdaten intakt). `apply_exclusions.py` validiert jeden Ausschluss-Slug gegen die
Eingabe und läuft nur auf der enriched-CSV; da die Build-CSV die Garantie-Daten trägt und von enriched
abweicht, wurde chirurgisch entfernt — der Eintrag in `04-exclusions.csv` sichert die Provenienz für
einen vollständigen Neulauf.

## Alle Fundstellen (vor dem Bauen gesucht)

**Handgeschriebener Text, der die beiden nannte — bereinigt:**
- `city-copy.json`, Stadttext **Mannheim** (`baden-wuerttemberg/mannheim`): Intro-Absatz 2 (Türengel),
  Intro-Absatz 3 (Vetter) und zwei FAQ-Antworten (Vetter in „über den Rhein", Türengel in „nachts und
  am Wochenende"). Neu geschrieben, siehe unten.

**Automatisch erzeugt aus `listings.csv` — bereinigt sich beim Neubau, kein Handgriff nötig:**
- Die zwei Eintragsseiten `/firma/baden-wuerttemberg/mannheim/<slug>/` und ihre Anker.
- Die Mannheimer Stadtseite (Kartenliste, „weitere Betriebe"-Sprungliste, Kopf-Kennzahlen).
- Der Suchindex (`search-index.json.ts` → `dist/search-index.json`).
- Leistungsseiten, Bundesland-Seite, Sitemap.

**Geprüft, nicht betroffen:**
- **Ein anderer Betrieb mit ähnlichem Namen bleibt:** `tuerengel-schluesseldienst-24-7-essen`
  („Türengel Schlüsseldienst 24/7", Essen, Nordrhein-Westfalen) ist ein eigener Betrieb. Der
  Essen-Stadttext (`nordrhein-westfalen/essen`) nennt ihn — **unangetastet**. Essen ist kein Nachbarort
  von Mannheim.
- Nachbarorte (Ludwigshafen, Viernheim, Mutterstadt, Frankenthal, Weinheim u. a.): kein Stadttext nennt
  die beiden.
- `site.json` (Bundesland-Text, Startseiten-FAQ), `attributes.json` (Leistungs-Intros), Ratgeber: keine
  Nennung.

## Stadttext Mannheim neu (vorgesehener Weg)

Aus den **verbleibenden 17 Einträgen**: `node dump-cities.mjs` auf der bereinigten CSV, frisches
Mannheim-Stadtpaket mit `make_city_packets.py` (17 Einträge, 1.593 Bewertungen, Schnitt 4,8), Antwort
nach `scripts/city-copy-instructions.md` neu gefasst (Intro-Absätze 2 und 3, zwei FAQ-Antworten),
`check_city_copy.py --only` gegen das frische Paket **bestanden**, dann `--write` → `city-copy.json`.
Die Regenerierung ändert **nur** Mannheim; die 786 anderen Städte bleiben byte-identisch (geprüft).
Kein Satz nennt die beiden mehr, keine Aussage stammt nur aus ihren Daten (Türengels Stadtteile
Lindenhof/Sandhofen, Vetters Gebiet Limburgerhof/Mutterstadt entfernt). **Textgate** (`lint_copy.py`
auf `city-copy.json`, ohne `--erlaube-rechtswoerter`): Mannheim **BESTANDEN** (518 Wörter, 5 FAQs); die
725 vorbestehenden Durchfaller kleiner Städte sind vor und nach der Änderung identisch (generische
Wortspanne von `lint_copy` gegen die Größenbänder — betrifft Mannheim nicht).

## Neu gebaut — Erwartung erfüllt

- **Mannheim 17 Einträge**, Kopf neu berechnet: **17 eingetragen · 2 geprüft · 4,8 Durchschnitt aus
  1.593 Bewertungen** (vorher 19 / 1.757).
- Spitze der Stadtseite: **Merz, AES, Key Walter** (dann ATILLA …).
- Beide Eintragsseiten weg, ihre Anker weg, **kein interner Link** mehr auf sie (0 Treffer in `dist`).
- **Neue Sitemap-Zahl: 2.821** (vorher 2.823, −2).
- Eintragsseiten (`/firma/…`): 3.797 (vorher 3.799). Gebaute HTML-Seiten gesamt: 4.644.

## Ausgeliefert und live geprüft

- `wrangler pages deploy` → Deploy `9f0ec5a5`.
- `check_live.py … --expect-urls 2821` → **alle Prüfungen bestanden**.
- Beide Adressen liefern **HTTP 404**.
- Mannheim zeigt live **Merz, AES, Key Walter** an der Spitze, kein Türengel/Vetter.
- Suche: die beiden Mannheimer Namen sind aus dem Index verschwunden; nur der Essener „Türengel
  Schlüsseldienst 24/7" bleibt (eigener Betrieb).

## Sollwert nachgezogen

- `06-launch.md`: Start-Sollwert auf **2821** nachgezogen (Historie 2823 am Start erhalten).
- `CLAUDE.md`: enthält keine 2823, nichts zu ändern.
- Zwei weitere, **historisch/narrativ** (nicht geändert): `design-pilot1/DBS-WEB-DESIGN-PILOT1-…md`
  (abgeschlossener Pilot-Auftrag) und `wiki/framework/template-build-drift.md:54` (Beispiel im Fließtext
  eines zurückliegenden Vorgangs). Beide nennen 2823 als Beschreibung eines vergangenen Laufs, nicht als
  laufenden Sollwert — auf Zuruf angleichbar.
