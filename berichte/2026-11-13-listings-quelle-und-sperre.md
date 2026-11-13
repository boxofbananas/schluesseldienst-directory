# Garantie- und Verkaufsdaten gegen Überschreiben gesichert

**Datum:** 2026-11-13 · **Branch:** `main` · **Kein Deploy** (reine Pipeline-Arbeit, die Build-`listings.csv` ist unberührt)

Beim Mannheimer Ausschluss fiel auf: die Build-`listings.csv` trägt die operativen Spalten,
`03-listings-enriched.csv` nicht. Ein Vollneulauf aus der angereicherten CSV hätte sie gelöscht.
Dieser Vorgang legt eine Quelle fest, trägt die Werte beim Neulauf zurück und sperrt jedes
Überschreiben, das sie verlöre.

## 1. Das volle Ausmaß des Unterschieds

Verglichen `03-listings-enriched.csv` (4.387 Zeilen, 80 Spalten) gegen
`site/src/data/listings.csv` (3.797 Zeilen, 82 Spalten). 3.797 gemeinsame Slugs, 590 nur in
enriched (die Gate-4-Ausschlüsse), keiner nur im Build.

**Spalten-Divergenz (Schema):**
- Nur im Build: `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `featured_seit`
- Nur in enriched: `garantie_nacht` (alter Einzelzuschlag, vom Build durch abend/nacht abgelöst)

**Werte-Divergenz — gefüllt im Build, leer in enriched:**

| Spalte | gefüllte Zeilen im Build |
|---|---|
| `geprueft`, `geprueft_jahr` | 18 |
| `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt`, `garantie_zylinder`, `garantie_zylinder_5mm` | je 18 |
| `featured` (= `city`) | 1 (Merz) |
| `featured_seit` (= `2026-11-06`) | 1 (Merz) |
| `premium` (= `true`) | 1 (Merz) |
| `best_of_rank`, `featured_cities`, `preisschutz` | 0 |

Also **18 vollständige Festpreis-Garantien** (geprüft + sechs Preisspalten) und **ein
Mannheimer Platz** (Merz: Stadt-Premium + Premium-Eintrag mit Buchungsdatum), die enriched
nicht kennt.

**Skripte, die die Build-`listings.csv` überschreiben:**
1. `apply_exclusions.py` — schreibt sie **aus enriched** (`--out …/listings.csv`). Der eigentliche
   Verlust-Vektor: enriched hat die operativen Spalten leer.
2. `verkauf.py` — in-place, setzt/leert eine Verkaufsspalte, rührt die Garantie nie an.
3. `add_socials.py` — in-place, setzt nur die Spalte `socials`.

(`add_own_listings.py` schreibt die Gate-2-CSV `02-listings-clean.csv`, nicht die Build-CSV —
außerhalb der Sperre.)

## 2. Eine Quelle (Vorschlag, umgesetzt)

> 1. Die Build-`site/src/data/listings.csv` ist die **alleinige Wahrheit** für die operativen
>    Spalten (geprueft, geprueft_jahr, die sechs `garantie_*`, featured, featured_cities,
>    featured_seit, premium, best_of_rank, preisschutz). Nur dorthin schreiben `verkauf.py` und
>    die Garantie-Vergabe von Hand.
> 2. `03-listings-enriched.csv` bleibt die Wahrheit für die **beschreibenden** Spalten
>    (Beschreibung, Merkmale, Bewertungen, Scrape-Felder) und trägt die operativen Spalten nie.
> 3. Baut die Kette `listings.csv` neu aus enriched, **folgt** sie der bestehenden Datei:
>    `apply_exclusions.py` trägt die operativen Spalten per Slug zurück (`merge_protected`) und
>    ergänzt fehlende Spaltennamen, bevor es schreibt.

In CLAUDE.md unter „Neu bauen bei Änderung" festgehalten.

## 3. Die Sperre

Neues gemeinsames Modul `scripts/_listings_guard.py`:
- `PROTECTED` — die Liste der operativen Spalten (eine Stelle; neue Spalten hier eintragen).
- `merge_protected(rows, fieldnames, existing_path)` — trägt die operativen Werte per Slug aus
  der bestehenden CSV zurück und ergänzt fehlende Spaltennamen (löst die Schema-Divergenz).
- `pruefe_kein_verlust(rows, existing_path, erlaubt=…)` — **bricht ab** (exit 1), wenn eine
  **bleibende** Zeile einen gefüllten operativen Wert verlöre (gefüllt → leer), und nennt
  Eintrag und Spalte. Ein geänderter, nicht geleerter Wert (neuer Garantiepreis) und ein ganz
  entfernter Eintrag lösen nichts aus; `erlaubt={slug:{spalten}}` lässt die eine gewollte
  Änderung durch.

Verdrahtet in alle drei Überschreiber:
- `apply_exclusions.py`: erst `merge_protected` (Rücktrag), dann `pruefe_kein_verlust` als
  Backstop; ein ausgeschlossener Eintrag mit Garantie/Buchung wird zusätzlich als Warnung gemeldet.
- `verkauf.py`: `pruefe_kein_verlust` vor jedem Schreiben, `erlaubt` nur für die eine gesetzte/
  geleerte Buchungsspalte des Ziels — jede Garantie und jeder fremde Platz bleibt geschützt.
- `add_socials.py`: `pruefe_kein_verlust` ohne Ausnahme (es rührt nur `socials` an).

## 4. Probe (Vollneulauf in eine Kopie)

Die bestehende Build-CSV in eine Scratch-Kopie gelegt (im echten Lauf ist sie selbst das
`--out`-Ziel), dann `apply_exclusions.py` aus enriched darüber laufen lassen:

```
listings in: 4387, written: 3797   (dropped: 590)
```

Nachprüfung der Kopie gegen die Live-CSV:
- Zeilen **3.797 = 3.797**.
- **18 geprüft**, dieselben Slugs wie live.
- **0** abweichende Garantie-Preiszellen (alle acht Spalten × 18 identisch).
- Merz: `featured=city`, `premium=true`, `featured_seit=2026-11-06` — **erhalten**.
- Beide Mannheimer Ausschlüsse **nicht mehr** in der Kopie.

**Gegenbeweis, dass die Sperre greift:** enriched-Zeilen (Garantie leer) ohne Rücktrag gegen die
Live-CSV geprüft → `ABBRUCH … 145 Zelle(n) betroffen`, **18 Einträge namentlich** genannt
(Garantiepreise + Merz' Platz). Es wurde nichts geschrieben.

**Backstop-Live-Test:** `verkauf.py --stufe top` auf einer Scratch-Kopie (geprüfter
Heidelberg-Eintrag, `--kein-bauen`) → Buchung gesetzt (`best_of_rank=1`), Garantie erhalten
(`garantie_tag=89`), weiterhin 18 geprüft. Die Sperre lässt die gewollte Änderung durch.

## 5. Nebenbefund: `lint_copy.py` auf `city-copy.json` (nichts geändert)

**Ja, ein Schalter behebt es: `--city-sizes`.** Die 725 Durchfaller entstehen, weil das Textgate
ohne ihn eine generische Wortspanne (≥10-Einträge-Band) auf jede Stadt anwendet; kleine Städte
fallen dann an `in_der_wortspanne` durch. Mit `--city-sizes` nimmt es die Bänder nach Stadtgröße
(≥10: 500–800 & 4–6 FAQs; 5–9: 380–800; 3–4: 250–800; 1–2: 120–800 & 2–6 FAQs) — dieselben, die
`check_city_copy.py` kennt (0 Durchfaller).

**Haken:** die Größenkarte muss mit den **city-copy-Schlüsseln** verschlüsselt sein,
`<bundesland-slug>/<stadt-slug>` (z. B. `thueringen/weimar`), nicht mit dem bloßen `city_slug`.
Eine falsch verschlüsselte Karte matcht nichts und lässt alle 725 stehen (selbst erlebt). Mit
korrekt verschlüsselter Karte treffen **alle 787 Schlüssel** und die Durchfaller fallen auf
**0** — read-only in Scratch bestätigt, nichts geändert.

Die Karte ist billig: `05-cities.json` trägt je Stadt `count`, `regionSlug` und `slug`, also
`{regionSlug + '/' + slug: count}`. **Vorschlag (auf Rückmeldung):** beim Textgate für
`city-copy.json` immer `--city-sizes` mit dieser Karte mitgeben und den Schritt in
[[copy-gate]] festhalten, damit ein echter Fehler nicht länger in 725 Fehlalarmen untergeht.
`check_city_copy.py` bleibt der maßgebliche Wortzahl-Prüfer (kennt die Größen aus den Paketen).

## Geändert

- neu: `scripts/_listings_guard.py`
- `scripts/apply_exclusions.py`, `scripts/verkauf.py`, `scripts/add_socials.py` — Sperre/Rücktrag
- `CLAUDE.md` — „Neu bauen bei Änderung": Quelle und Sperre
- Keine Build-Daten, kein Deploy.
