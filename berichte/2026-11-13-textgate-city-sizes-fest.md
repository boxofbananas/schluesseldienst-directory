# --city-sizes fest ins Textgate für city-copy.json

**Datum:** 2026-11-13 · **Branch:** `main` · **Kein Deploy** (reine Pipeline-Arbeit, keine Build-Daten berührt)

Folgt auf den Nebenbefund von heute früh: `lint_copy.py` meldete 725 Städte als durchgefallen,
weil es ohne Größenkarte auf die generische Wortspanne zurückfiel. Jetzt ist die Karte Pflicht,
wird frisch erzeugt und ein fehlender Schlüssel bricht ab statt stillzuschweigen.

## Der eigentliche Fehler: die gepflegte Datei war falsch verschlüsselt

`copy-gate.md` schrieb bisher eine zu pflegende `05-city-sizes.json` vor — und ihr Erzeuger
(Zeile 44) verschlüsselte nach dem **bloßen** `slug`:

```
{c['slug']: c['count'] for c in 05-cities.json}      # "mannheim": 17
```

Die Schlüssel von `city-copy.json` sind aber `bundesland/stadt` (`baden-wuerttemberg/mannheim`).
Die Karte traf also **nichts**, jede Stadt fiel auf die generische Spanne zurück, und jede kleine
Stadt fiel zu Unrecht durch. Eine gepflegte Datei kann zudem veralten, sobald sich die
Eintragszahl einer Stadt ändert.

## Geändert

**`scripts/lint_copy.py`**
- Neuer Schalter **`--cities <05-cities.json>`**: baut die Größenkarte bei **jedem Lauf frisch**
  als `regionSlug/slug → count` (neue Funktion `build_city_sizes`). Keine zu pflegende Datei mehr.
- Beim Lauf auf `city-copy.json` ist eine Größenquelle **Pflicht**: fehlt sie, **FEHLER + Abbruch**
  (kein stiller Rückfall auf 500 Wörter / 4 Fragen).
- **Volle Abdeckung erzwungen:** fehlt eine Stadt aus `city-copy.json` in der Karte, **ABBRUCH**,
  der die fehlenden Städte namentlich nennt.
- `--city-sizes` (vorgefertigte Datei) bleibt für Sonderfälle; für `city-copy.json` ist `--cities`
  vorzuziehen. Die Hilfe sagt das.

**`wiki/seo/copy-gate.md`** — Tabellenzeile „Stadtblöcke und Fragen" auf `--cities
output/<slug>/05-cities.json` umgestellt; der Abschnitt zur gepflegten `05-city-sizes.json`
ersetzt durch die Pflicht-/Abbruch-Regel und den Hinweis auf den alten Verschlüsselungsfehler.

**`CLAUDE.md`, Gate 5** — der vollständige Aufruf mit `--cities` festgehalten, samt der Regel, dass
fehlende Quelle oder fehlende Stadt abbricht.

**`wiki/framework/page-types.md`** — Verweis `lint_copy.py --city-sizes` → `--cities` (frisch aus
`05-cities.json`).

## Geprüft

- `--cities` und bloßer `slug`-Schlüssel: `regionSlug/slug` deckt **alle 787** city-copy-Schlüssel.
- **(1)** `city-copy.json` ohne Quelle → `FEHLER … --cities angeben`, echter **exit 1**.
- **(2)** `--cities 05-cities.json` (volle Karte) → Lauf startet, **787 bestanden, 0 durchgefallen**,
  **exit 0**.
- **(3)** `05-cities.json` ohne Mannheim → `ABBRUCH: 1 Stadt(e) … fehlen … baden-wuerttemberg/mannheim`,
  **exit 1**.
- Der in CLAUDE.md/copy-gate dokumentierte Befehl verbatim → exit 0.

## Voller Textgate-Lauf über city-copy.json (das echte Ergebnis)

```
python3 scripts/lint_copy.py output/<slug>/site/src/data/city-copy.json \
    --niche "Schlüsseldienste" --cities output/<slug>/05-cities.json
```

**787 bestanden, 0 durchgefallen.** Die 725 von heute früh waren allesamt Fehlalarme der
generischen Spanne — mit den Größenbändern sind sie weg. **Keine echten Befunde**, nichts zu
ändern. (Beispiel: `thueringen/weimar` 402 Wörter besteht jetzt gegen die Untergrenze 380 seiner
Größenklasse, statt gegen die generischen 500 durchzufallen.) Deckungsgleich mit
`check_city_copy.py` (0 durchgefallen), dem maßgeblichen Prüfer der Bänder.

Kein Deploy.
