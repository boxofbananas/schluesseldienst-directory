# Versand-Export: Mail-Variante, Stand und gerechter Schnitt

**Datum** 2026-11-14 · **Kein Versand, kein Deploy** · `listings.csv` und das Verzeichnis
unverändert. Nur Zahlen in diesem Bericht — keine Namen, keine Adressen. Alle Probeläufe mit
`--probe` oder auf Kopien der Bücher; die Live-Bücher blieben leer.

Erweitert wurde nur `scripts/kontakt.py` (plus `CLAUDE.md`, Bericht, Log).

## Neue Spalten der Export-CSV

Hinter `anrede` zwei Spalten:

- **`variante`** (`platz` oder `telefon`): `platz`, wenn der Eintrag eine Bewertung hat **und**
  die Stadtseite mindestens `PLATZ_HOOK_MIN_ANZAHL` (= 5) Einträge führt; sonst `telefon`. Hat ein
  Eintrag dann kein Telefon, fällt er aus dem Export — neuer Trichter-Grund `keine_variante`, in
  der Zahlenliste ausgewiesen. Die Schwelle steht als eine Konstante oben im Skript.
- **`stand`** (JJJJ-MM-TT): der Exporttag. `exportieren` gibt am Ende den Hinweis aus, dass die
  Plätze für den Stand von heute gelten und nach einem Neubau neu zu exportieren ist.

## Gerechter Schnitt der Obergrenze

Bisher schnitt `--limit` nach der Datei-Reihenfolge (Bundesland, Stadt) ab — späte Städte fielen
ganz weg. Neu: bei `--limit` werden zuerst die Zeilen nach Score absteigend ausgewählt (beste über
alle Städte zuerst), danach wie bisher für die Datei nach Bundesland, Stadt, Score sortiert.
Beleg aus dem Scratch-Lauf (Bayern, `--limit 30`): die 30 Zeilen verteilten sich auf 14 Städte.

## Zahlen (Probeläufe, `--probe`)

| Umfang | versandfertig | mit Namen | Variante platz | Variante telefon | `keine_variante` |
|---|---:|---:|---:|---:|---:|
| national | 639 | 330 | 460 | 179 | 1 |
| Bayern | 91 | 50 | 79 | 12 | 0 |

National fällt gegenüber dem Stand vom 2026-11-14 (640 versandfertig, 331 mit Namen) **ein**
Eintrag weg: er trägt keine Bewertung oder zu wenige Einträge auf der Stadtseite (also Variante
`telefon`) und hat kein Telefon — Grund `keine_variante`. Dieser eine Eintrag hatte einen Namen,
darum 330 statt 331 mit persönlicher Anrede. Variante platz + telefon = versandfertig (460 + 179 =
639; 79 + 12 = 91).

## Prüfung gegen die gebaute Seite

`pruefen` bleibt grün: Seeds 0, 1, 2, je 20 Stichproben, **0 Abweichungen**. Die Werte des Exports
stimmen weiter mit `dist/` überein.

## Offen

Nichts offen. Alle sechs Punkte umgesetzt, `pruefen` grün, Live-Bücher unberührt.
