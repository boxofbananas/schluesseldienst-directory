# Stadttexte auf Sonnet erzeugt — 792 Seiten (2026-11-04)

Ausschlüsse angewandt, neu gebaut, Dump, Stadttexte auf Sonnet. Jetzt vollständig.

## Daten
- `04-exclusions.csv` (578 Drops) angewandt → **3.809 Einträge**, **792 Stadtseiten** (577 mit ≥2
  Einträgen, 215 kleine Ortsseiten). Oberzent jetzt unter Hessen.
- `site/src/data/city-copy.json`: **792 Städte, 0 Durchfaller**, 1:1 zu den Seiten.

## Kosten (Sonnet, claude -p)
- Hauptlauf: **69,99 $**, 66,3 Mio Token, **8,9 ct/Stadt**, 85 min, 111/112 Stapel im 1. Versuch.
- Nachläufe (16 + 1 Städte neu): ~2,2 $. **Gesamt rund 72 $** — unter der Schätzung (~86 $).

## Zwei Befunde beim Zusammenbau
1. **Slug-Kollision (behoben).** Drei Städtepaare teilen einen Kurz-Slug: `friedberg` (Bayern/
   Hessen), `halle` (Halle-Saale/Halle-Westf.), `senden` (Bayern/NRW). Pakete und Antworten
   schlüsselten nach Kurz-Slug → sie hätten sich im `city-copy.json` überschrieben (eine Seite
   bekäme den Text der anderen). **`make_city_packets.py` schlüsselt jetzt nach vollem `key`
   (region/slug)**; vorhandene Pakete und Antworten wurden umgeschlüsselt. `load.mjs` las schon
   `cityCopy[c.key]` zuerst, passt also.
2. **Near-Dup-Prüfung: 16 + 1 Schablonen gefunden und neu geschrieben.** Erst im vollständigen Satz
   (nicht in den parallelen Stapelprüfungen, die noch nicht alle anderen sahen) zeigten sich
   fast gleiche Sätze über ≥3 Städte: Bewertungszeilen, Faktenblatt-Satz der Verbraucherzentrale,
   „Nachbarorte"-/„Eigene Seiten gibt es für …"-Listen benachbarter Orte. Die 16 betroffenen Städte
   auf Sonnet neu geschrieben; eine letzte (Pinneberg, FAQ-Nachbarliste) von Hand umformuliert.
   Die Prüfung selbst wurde für 800 Städte **subquadratisch** gemacht (invertierter Index auf die
   seltensten Tokens je Satz, Prefix-Filter — findet dieselben Treffer, läuft in ~18 s statt Timeout).

## Offen für den vollständigen Gate-5-Bau (nicht Teil dieses Auftrags)
`npm run build`, `site.json` vollständig, selbst gehostete Schriften, Pflichtseiten Impressum
(§ 5 DDG) und Datenschutz (Art. 13 DSGVO), „Über uns", Ratgeberseiten, Textgate auf die gebauten
Seiten. Die Stadttexte stehen bereit.
