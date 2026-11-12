# Offenlegung abgeschlossen: die drei Reststellen + Template-Nachtrag

**Datum:** 2026-11-12 · **Branch:** `main` (live) · **Deploy:** `cfbc517b` · **Projekt:** `schluesseldienste-deutschland`

Folgt auf `berichte/2026-11-12-sortierung-offenlegen.md`. Dort waren drei weitere Stellen genannt,
aber nicht geändert; hier werden sie berichtigt, und die Copy-Änderungen werden ins Template
nachgetragen.

## 1. Die drei genannten Stellen berichtigt — überall dieselbe Reihenfolge

Reihenfolge wie in der Sortierzeile: **bezahlte Plätze → Festpreis-Garantie → die übrigen nach
Bewertung.**

- **Bundesland-Seite**, lede (`verzeichnis/[bundesland]/index.astro:50`): „Jede Stadtseite führt
  zuerst die bezahlten Plätze, dann die Betriebe mit Festpreis-Garantie und danach alle übrigen nach
  Bewertung und Anzahl der Bewertungen."
- **FeaturedBand** (`components/FeaturedBand.astro:37`), Frei-Karte: „… im Premium-Band [für X], über
  der übrigen Liste (zuerst die Betriebe mit Festpreis-Garantie, dann nach Bewertung), in der
  Reihenfolge der Buchung." (`{place}` vor die Klammer gezogen, damit der Satz sauber läuft.)
- **Stadtseiten-Meta-Description** (`[stadt]/index.astro:25`): neu gefasst, Reihenfolge statt
  „geordnet nach Bewertung".

### Meta-Description: vorher / nachher am Beispiel Mannheim

| | Wortlaut | Zeichen |
|---|---|---|
| **vorher** | 19 Schlüsseldienste in Mannheim, Baden-Württemberg, geordnet nach Bewertung und Anzahl der Bewertungen. Am besten bewertet: Merz Sicherheit • Einbruchschutz, Schließanlagen & Schlüsseldienst (5,0 aus 355 Bewertungen). Telefonnummern und Leistungen zu jedem Eintrag. | **265** |
| **nachher** | 19 Schlüsseldienste in Mannheim, Baden-Württemberg: bezahlte Plätze, dann Festpreis-Garantie, dann nach Bewertung. Mit Telefonnummer und Leistungen. | **148** |

**Zur Längenvorgabe:** `wiki/seo/on-page-rules.md` nennt **keine** Zeichenzahl für Beschreibungen —
die einzige Längenregel dort gilt dem **Titel** („über 60 Zeichen kürzt Google", Abschnitt „Titel").
Für Beschreibungen gibt es nur die inhaltliche Vorgabe (Abschnitt „Beschreibungen": Anzahl,
bestbewertete Betriebe, Zahl der geprüften). Die alte Fassung war mit 265 Zeichen weit über Googles
praktischer Anzeigegrenze (~160); der lange Firmenname des bestbewerteten Betriebs trieb sie. Die neue
Fassung bleibt mit **148 Zeichen** darunter. Dafür entfällt die Nennung des bestbewerteten Betriebs
(sonst nicht unter 160 zu halten, weil Firmennamen hier bis ~65 Zeichen lang sind). Mannheim ist nahe
dem ungünstigsten Fall (langer Bundeslandname), die meisten Städte werden kürzer. **Falls die Nennung
des Spitzenbetriebs wichtiger ist als die 160-Grenze, sag Bescheid** — dann nehme ich sie wieder auf
und lasse die Länge laufen.

### Textgate an den gebauten `dist/`-Seiten (echtes Ergebnis)

| Seite (aus `dist/`) | Flag | Ergebnis |
|---|---|---|
| Stadtseite Mannheim | **ohne** `--erlaube-rechtswoerter` | **BESTANDEN** (1427 Wörter) |
| Bundesland Baden-Württemberg | **ohne** `--erlaube-rechtswoerter` | **BESTANDEN** (258 Wörter) |
| /premium/ | mit `--erlaube-rechtswoerter` | **BESTANDEN** (361 Wörter) |
| /festpreis-garantie/ | mit `--erlaube-rechtswoerter` | **DURCHGEFALLEN** — nur vorbestehende Punkte |

Das /festpreis-garantie/-DURCHGEFALLEN ist **unverändert zur Live-Fassung**: Diese Seite hat in diesem
Task **keine** Build-Änderung bekommen (der Reihenfolge-Absatz kam in der vorigen Runde, Build-Datei ==
HEAD, kein Diff). Die drei Punkte sind der Natur der Seite geschuldet: das Betrugszitat „ab 49 Euro"
(muss stehen, um das Problem zu zeigen), 11 Gedankenstriche (mein Absatz fügt **0** hinzu — belegt) und
`branche_im_ersten_absatz` (die Seite eröffnet mit dem Problem, nicht mit dem Branchenwort). Der
Programmname „Festpreis-Garantie" ist frei; kein freistehendes „Garantie"/„garantiert".

## 2. Template-Nachtrag

Geprüft, ob die Copy-Änderungen der vorigen Runde schon im Template standen — **sie fehlten alle**.
Nachgetragen, zusammen mit den drei Stellen aus Punkt 1. Im Template stehen jetzt (Quelle bestätigt,
`npm run build` grün, in der Template-`dist` gerendert):

| Element | Template vorher | jetzt |
|---|---|---|
| Stadtseite: Sortierzeile unter „Die besten …" | fehlte | **da** |
| Stadtseite: Ersatz-Vorspann (ohne Stadttext) | alt | **berichtigt** |
| Stadtseite: Meta-Description | alt (265-Form) | **neu (Reihenfolge)** |
| /festpreis-garantie/: Reihenfolge-Absatz | fehlte | **da** |
| /premium/: lede + Stadt-Premium-Satz | alt | **berichtigt** |
| Bundesland-lede | alt | **berichtigt** |
| FeaturedBand-Frei-Karte | alt | **berichtigt** |

Build und Template tragen damit denselben Stand.

## 3. Bauen, Ausliefern, Prüfen

- `npm run build` (Build) grün, Schriftprüfung grün, Sitemap 2823.
- `npm run build` (Template) grün.
- `wrangler pages deploy` → Deploy `cfbc517b`.
- `check_live.py … --expect-urls 2823` → **alle Prüfungen bestanden**.
- Live-Stichprobe auf `die-besten-schluesseldienste.de`: Mannheim-Sortierzeile ✓, Mannheim-Meta
  148 Zeichen ✓, BW-lede ✓, /premium/-lede ✓, /festpreis-garantie/-Absatz ✓.

## Offen

- Entscheidung, ob die Meta-Description den Spitzenbetrieb wieder nennen soll (dann > 160 Zeichen).
- Interne Notiz: `on-page-rules.md:85` beschreibt die Kartenabschneidung bei 60 Einträgen als
  „geordnet nach bezahltem Platz, dann Bewertung" — nennt die Festpreis-Garantie-Stufe nicht. Das ist
  eine Wiki-Regel, keine ausgelieferte Seite; auf Zuruf angleichen.
- Gruppe 3 der Sortierung (Ortsvorwahl ↔ PLZ) weiter ausgelassen bis zur Referenztabelle.
