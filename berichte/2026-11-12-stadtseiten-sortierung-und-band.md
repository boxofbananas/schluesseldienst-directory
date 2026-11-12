# Stadtseiten: Sortierung nach Konvention und Band-Einträge in der Liste (Teil A)

**Datum:** 2026-11-12 · **Branch:** `main` (live ausgeliefert) · **Projekt:**
`schluesseldienste-deutschland` (Cloudflare Pages, `die-besten-schluesseldienste.de`)

## A1 — Sortierung der Stadtseiten-Liste

### Befund aus dem Git-Verlauf

`sortListings` in `load.mjs` wurde im Erstbau-Commit `feb32b6` genau in der bisherigen Form
angelegt (bezahlte Plätze, `sortAttribute`, Rest) und **seither nie geändert**. Die Gruppen 2
(Festpreis-Garantie) und 3 (Ortsbezug) waren **nie im Code** — sie gingen nicht verloren. Die
Konvention dazu kam am 2026-11-04 hinzu, der Code zog nie nach.

### Gruppe 2 umgesetzt

`geprueft = true` ist jetzt eine eigene Sortierstufe **nach** den bezahlten Plätzen und **vor**
dem Rest. `owned` wird weiterhin nicht gelesen. Reihenfolge jetzt vollständig nach
[[konventionen]]: bezahlte Plätze → Festpreis-Garantie → [Ortsbezug] → Rest, je Gruppe nach
Bewertung (`score = Bewertung × log10(Anzahl+1)`). „Bezahlte Plätze" umfasst Premium-Band
(`featured`), Top-Platzierung (`best_of_rank`) und Premium-Eintrag (`premium`).

### Gruppe 3 ausgelassen — was fehlt

**Festnetznummer mit zur PLZ passender Ortsvorwahl** ist **nicht** umgesetzt. Die Daten reichen
dafür nicht:

- **Vorhanden:** `phone` (E.164) und `postal_code`. Der Code kann die Ortsvorwahl aus der Nummer
  lesen (`nationalDe` + `areaLength`) und Mobilnummern erkennen (`/^1[5-7]/`), also ließen sich
  Mobilnummern ausschließen und mehrfach vorkommende Nummern zählen.
- **Es fehlt:** eine **Vorwahl↔PLZ-Referenz**, die die gelesene Ortsvorwahl (z. B. `341`) einer
  PLZ-Region (z. B. `04275`) zuordnet. Vorwahl und PLZ sind zwei unabhängige Systeme ohne
  rechnerischen Zusammenhang; ohne Nachschlagetabelle lässt sich „passt zur PLZ" nicht bestimmen.
  Im Repo gibt es keine solche Tabelle.

Ich habe **nicht geraten**. Gruppe 3 bleibt leer, bis eine Vorwahl↔PLZ-Tabelle (oder je
Vorwahl→Ort und PLZ→Ort) vorliegt. Der Platz ist im Code als Rang 2 reserviert und kommentiert.

**Wirkung:** Deine Erwartung für Mannheim (Merz, AES, Key Walter) entsteht genau **ohne**
Gruppe 3 — mit Gruppe 3 sprängen ortsgebundene Einträge über Key Walter.

## A2 — Betriebe mit Premium-Platz stehen zusätzlich in der Liste

Bisher nahm die Stadtseite jeden Band-Eintrag aus dem Raster (`gridCards =
cards.filter(!city.featured.includes)`). Dadurch fehlte Merz Sicherheit (5,0 aus 355) in der
Mannheimer Liste. **Jetzt:** Das Band bleibt unverändert als Hervorhebung, und die Band-Einträge
stehen **zusätzlich** in der Liste (`gridCards = cards`) — durch die Sortierung an erster Stelle.
Die Sprungliste „Betriebe in …" nutzt dieselben `gridCards`, enthält sie also mit.

- **Keine doppelten `id`:** Der Sprunganker `b-<slug>` sitzt nur auf der Listenkarte;
  `FeaturedBand` setzt keine `id`. Im Build geprüft: **keine doppelten `id` auf der Mannheim-Seite.**
- **`maxCardsPerCity` zählt die Band-Einträge mit:** `cards = city.listings.slice(0, max)` enthält
  sie, das Raster zeigt jetzt genau `cards`.

### Bundesland-Seiten und Startseite — vor der Änderung geprüft, Ergebnis

- **Bundesland-Seiten:** **unverändert.** Sie zeigen eine **Städte**-Liste, keine Betriebsliste;
  das Band ist dort die einzige Betriebsanzeige — es gibt nichts, aus dem Einträge genommen würden.
- **Startseite:** **unverändert gelassen.** Dasselbe Muster besteht (die „Bestbewertete"-Liste
  schließt `homeFeatured` und `l.featured` aus), aber das **nationale Band ist leer**
  (`featured=state` = 0, kein nationaler Platz verkauft) — es gibt keine Band-Einträge, die in die
  Liste gehörten. Der Ausschluss bezahlter Einträge aus der „Bestbewertete"-Liste trennt Redaktion
  von bezahlter Platzierung; das habe ich bewusst **nicht** angetastet. Sobald ein nationaler Platz
  verkauft wird, ist neu zu entscheiden, ob er auch dort erscheint. **Wenn du das jetzt schon
  anders willst, sag Bescheid** — Datenlage und Stelle (DirectoryHub, `spotlight`) sind bekannt.

## A3 — Erste fünf Listeneinträge, vorher/nachher

| # | Mannheim vorher | Mannheim **nachher** |
|---|---|---|
| 1 | Key Walter Mannheim | **Merz Sicherheit** (bezahlt) |
| 2 | Schlüsseldienst-ATILLA | **AES Schlüsseldienst Mannheim** (geprüft) |
| 3 | Autoschlüssel Nachmachen in Mannheim | **Key Walter Mannheim** |
| 4 | Schuh u. Schlüsseldienst Neseli | Schlüsseldienst-ATILLA |
| 5 | SCHLÜSSELDIENST - UHR SERVICE | Autoschlüssel Nachmachen in Mannheim |

Entspricht der Erwartung: **Merz Sicherheit, AES Schlüsseldienst Mannheim, dann Key Walter.**
Merz steht vorn als bezahlter Platz; AES folgt als einziger geprüfter Eintrag (Festpreis-Garantie
hebt ihn über den Rest, auch ohne Bewertung); Key Walter ist der höchstbewertete des Rests
(score 11,96 > Autoschlüssel 11,80, weil 274 Bewertungen gegen 229 zählen). Live bestätigt.

| # | Heidelberg vorher | Heidelberg **nachher** |
|---|---|---|
| 1 | TD Schlüsseldienst | **Heidelberg Schlüsseldienst** (geprüft) |
| 2 | ABC 24 Stunden Schlüsselnotdienst | **Sperber Schlüsseldienst** (geprüft) |
| 3 | Rudis Radladen | TD Schlüsseldienst |
| 4 | Schlüsselnotdienst Metzger | ABC 24 Stunden Schlüsselnotdienst |
| 5 | Schlüsseldienst Gruber | Rudis Radladen |

| # | Hockenheim vorher | Hockenheim **nachher** |
|---|---|---|
| 1 | DIETRICH.expert GmbH | **I-S-E Schlüsseldienst** (geprüft) |
| 2 | Justinger Sicherheitstechnik | **Mein Schlüsseldienst Hockenheim** (geprüft) |
| 3 | I-S-E Schlüsseldienst (geprüft) | DIETRICH.expert GmbH |
| 4 | Mein Schlüsseldienst Hockenheim (geprüft) | Justinger Sicherheitstechnik |

**Abweichung erklärt:** Heidelberg und Hockenheim ändern sich ebenfalls, weil ihre geprüften
Einträge (teils ohne Bewertung) jetzt über den Rest steigen — das ist die Konvention vom
2026-11-04 ausdrücklich so: „Die Festpreis-Garantie hebt einen Eintrag über die übrigen." In
Mannheim fällt das weniger auf, weil dort nur AES geprüft ist.

### Ausgeliefert und live geprüft

`npm run build` (grün, Schriftprüfung grün), `wrangler pages deploy dist` (4647 Dateien),
`check_live.py https://die-besten-schluesseldienste.de --expect-urls 2823`: **alle Prüfungen
bestanden**, Sitemap 2823, Produktionsdomain aktuell, `featuredPreview` = false. Live geprüft:
die Mannheimer Liste zeigt `b-merz-…`, `b-aes-…`, `b-key-walter-…` als erste drei Karten.

## A4 — Rückport ins Template, 04-plan, Protokoll

- **`templates/astro/`**: dieselbe Sortierung in `src/lib/load.mjs` und dieselbe
  Band-in-Liste-Regel in der Stadtseite ([[template-build-drift]]). Das Template ist schlanker
  (keine Sprungliste, keine `id`-Anker), daher dort nur der Inline-Filter → `cards.map(...)`.
- **`04-plan.md`**: Entscheidung A2 festgehalten (Abschnitt „Entscheidung A2") samt Begründung
  für Bundesland-Seiten/Startseite und der Auslassung von Gruppe 3.
- **`wiki/log.md`**: Zeile ergänzt.

## Offen

- **Gruppe 3** wartet auf eine Vorwahl↔PLZ-Referenz.
- **Startseite:** falls ein nationaler Platz verkauft wird oder du bezahlte Einträge doch in der
  „Bestbewertete"-Liste willst, ist das eine kleine, bekannte Änderung in `DirectoryHub`.
