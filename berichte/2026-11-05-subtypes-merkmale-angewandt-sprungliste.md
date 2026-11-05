---
title: subtypes als Belegquelle angewandt (sicher), Herkunftssatz, Stadtseiten-Sprungliste
type: bericht
status: fertig
updated: 2026-11-05
---

# subtypes-Zuordnung angewandt + Sprungliste

## (1) Sicherheitsprüfung: wirkt `core` in die Ausschlusslogik zurück? **Nein.**
Ausdrücklich geprüft — kein Skript und kein Build-Schritt liest `core`/`schluesseldienst_kern`
für eine Entscheidung über Aufnahme, Ausschluss oder Sichtbarkeit:
- **Build (`site/src`):** `schluesseldienst_kern` kommt nur in `attributes.json` als
  Merkmalsdefinition vor (wird angezeigt, seit gestern nur wenn `true`). Keine `.astro`/`.mjs`
  filtert danach. (Die „Kern"-Treffer in `city-copy.json` sind Fließtext wie „Stadtkern".)
- **`apply_exclusions.py`:** wendet `04-exclusions.csv` **ausschließlich über den `slug`** an
  (Aktionen `drop`/`blank_website`), liest nie ein Merkmal. Ein ausgeschlossener Eintrag bleibt
  ausgeschlossen, egal welche Merkmale er trägt.
- **`core` wird nur** von `make_batches.py` gelesen — ein Hinweis im Gate-3-Anreicherungs-Prompt,
  nicht im Build und nicht in Gate 4.

Die Pipeline ist reproduzierbar: `apply_exclusions.py(03-listings-enriched.csv, 04-exclusions.csv)`
erzeugt die aktuelle `listings.csv` **bit-identisch** (4.387 → 587 drop → 3.800). Deshalb wurde
die Änderung in der **angereicherten CSV** (Quelle) vorgenommen und `listings.csv` neu erzeugt;
`04-exclusions.csv` blieb unberührt.

| | vorher | nachher |
|---|---|---|
| `04-exclusions.csv` (Zeilen) | 587 | **587** |
| Einträge im Build | 3.800 | **3.800** |
| davon gedroppt | 587 | 587 |

**Kein einziger ausgeschlossener Eintrag ist zurückgekommen.**

## (2) Zuordnungstabelle (nur eindeutige), mit Häufigkeit im Build
| Google-subtype | Häufigkeit | → Merkmal |
|---|---|---|
| `Locksmith` | 771 | `schluesseldienst_kern` |
| `Emergency locksmith service` | 627 | `schluesseldienst_kern` (nur Kern — „emergency" ≠ 24h) |
| `Key duplication service` | 621 | `schluessel_nachmachen` |
| `Burglar alarm store` | 179 | `einbruchschutz` |

Nicht zugeordnet, weil sie nur das Umfeld benennen: `Safety equipment supplier`,
`Security system supplier`, `Safe & vault shop`, `Lock Store`/`Locks supplier`, sowie
Schuster/Graveur/Reinigung usw. Einen `Auto locksmith`-subtype gibt es nicht.

## (3) Angewandt — konservativ
Ein subtype hebt ein Merkmal nur von **`keine Angabe` → `wahr`**. Ein von Gate 3 aus der Website
gesetztes **`falsch` wird NICHT überschrieben** (die Website schlägt die Profil-Kategorie):
- **9** `schluesseldienst_kern` und **2** `schluessel_nachmachen` blieben bewusst `falsch`.

Neu auf `wahr` (im Build, 3.800): **+496** `schluesseldienst_kern`, **+313** `schluessel_nachmachen`,
**+60** `einbruchschutz`. **809** Einträge bekamen mindestens ein neu bestätigtes Merkmal; von den
204 indexierten ohne Merkmal haben **125** wieder einen Leistungen-Abschnitt (79 bleiben ohne —
kein verwertbarer subtype).

**Herkunftssatz** im Hinweiskasten der Eintragsseite ergänzt (ein Satz, keine neue Gestaltung,
kein zweites Symbol): *„Bestätigte Leistungen stammen aus der Website des Betriebs oder aus den
Angaben seines Google-Unternehmensprofils und sind keine Prüfung durch das Verzeichnis."*

## (4a) Wirkung auf die Leistungsseiten + Stichprobe
Es gibt sechs Leistungsseiten. Davon bildet die Zuordnung **nur eine** ab — `schluesseldienst_kern`
und `schluessel_nachmachen` haben **keine** eigene Leistungsseite, ändern dort also nichts.

| Leistung | vorher | nachher | neu |
|---|---|---|---|
| Türöffnung | 1.572 | 1.572 | 0 |
| Notdienst | 1.449 | 1.449 | 0 |
| Autoschlüssel | 841 | 841 | 0 |
| Schließanlagen | 1.345 | 1.345 | 0 |
| Tresoröffnung | 345 | 345 | 0 |
| **Einbruchschutz** | 1.261 | **1.321** | **+60** |

Die auf der Startseite genannte Menge „Türöffnung 1.572" bleibt also gleich. **Stichprobe 10 der 60
neu auf Einbruchschutz** — alle tragen `Burglar alarm store` und sind echte Alarm-/Sicherheits­technik-
Betriebe (Focken Sicherheitstechnik, Mattis Sicherheitstechnik, Knödler + Hurler Sicherheitstechnische
Anlagen, Dominico-Service Schlüsseldienst & Einbruchschutz, ISK, SAJAK, WAHLCOM GmbH, MAINHELFER
Elektrotechnik, Key center Barmbek, Wormsbecher Facility Service). **Keiner gehört dort nicht hin.**

## (4b) Stadtseite: Sprungliste statt leerer Fläche
Rechts neben der Einleitung steht jetzt eine klebende Liste **„Betriebe in \<Stadt\>"** mit Name und
Bewertung; jeder Eintrag springt zur Karte weiter unten (Anker `#b-<slug>` an jeder Karte). Nur
interne Links, kein externer Ladevorgang, keine Karte.
- **Mindestzahl:** erst **ab 8 Betrieben** auf der Seite. Geprüft: Mannheim (20) zeigt die Liste
  mit 20 Sprungzielen = 20 Kartenanker; Tuttlingen (2) und Emden (5) zeigen sie **nicht**.
- Auf dem Handy stapelt die Liste unter die Einleitung (geprüft, 390 px).

Screenshots: `stadt-mannheim` und `eintrag-key-walter`, je 1440/390 px.

## Prüfung
Build grün (4.629 Seiten), Schriftprüfung bestanden.
