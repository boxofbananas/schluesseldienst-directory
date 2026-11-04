# Drei Aufträge: Bewertungszahlen, Slug-Audit, Verhaltens-Ausschlüsse (2026-11-04)

Analyse und Härtung erledigt. **Drei Dinge warten auf deine Freigabe** (unten markiert).

## (1) Bewertungszahlen aus den Stadttexten — der wichtigste

**Befund:** 775 der 792 Texte nennen datenstämmige Zahlen im Fließtext — ~3.133 Sätze, ~7.958
Treffer (Bewertungsschnitte „4,9", Bewertungszahlen „aus 485", „43 Kunden", vereinzelt km). Fast
alle Städte betroffen. Das bricht das Prinzip „bei Datenänderung aus der CSV neu bauen", weil die
Karte auf derselben Seite beim nächsten Lauf die aktuelle Zahl zeigt.

**Dauerhaft abgesichert (erledigt):**
- `scripts/city-copy-instructions.md`: harte Regel ergänzt — keine aus den Daten stammende Zahl im
  Fließtext (Bewertungsschnitt, Zahl der Bewertungen, Eintrags-/Betriebszahl je Stadt, km). Erlaubt:
  qualitative Rangaussagen ohne Ziffer („die größte Bewertungsbasis", „die meisten Stimmen") sowie
  vom Betrieb selbst genannte Jahre/Normen (seit 1991, DIN EN 1627, RC 2). Die früher
  widersprüchlichen Stellen („Nennen Sie Bewertung und Anzahl") sind umgeschrieben.
- `scripts/check_city_copy.py`: neue Prüfung, die an solchen Zahlen scheitert. Verifiziert: meldet
  jetzt **775 Städte durchgefallen** mit der genauen Fundstelle; keine Fehlalarme auf Jahre/Normen.

**Noch nicht ausgeführt — Freigabe + Kosten (GATE A):** Nicht alles neu erzeugen. Geplant ist ein
**gezielter Umschreib-Lauf**: je Stadt den vorhandenen Text lesen und nur die Zahl-Sätze neu
schreiben (Aussage behalten, Ziffer weg). Weil nur der Text gelesen wird (nicht die großen Pakete),
kostet das etwa **ein Zehntel einer Vollerzeugung — Schätzung ~5–12 $ auf Sonnet**. Ich würde das
mit **einem Probestapel (~0,60 $)** genau einmessen, bevor der Rest läuft, und dir die
Probe-Ergebnisse zeigen. Freigabe?

## (1c) Eintragsbeschreibungen — Entwarnung
Nur **4 von 2.963** Eintragsbeschreibungen nennen eine Datenzahl, **alle aus DataForSEO, keine aus
Welle 1**. Die Gate-3-Regel hat bei der eigenen Welle-1-Stapelrunde gehalten. Die 4 (Hartmut Golz /
Ellwangen, Tayfun 2.0 / Fürth, 1.2.3.auf-die-Tür / Pfarrkirchen, Eisenvogel 2.0 / Uslar) hänge ich
an den Umschreib-Lauf an — minimal.

## (2) Slug-Kollision zu Ende geprüft
- **Eintrags-Slugs: eindeutig** (3.809 / 3.809, 0 Dubletten) — sie tragen die Stadt im Slug.
- **Stadtebene:** war die einzige Kollisionsstelle (friedberg, halle, senden). Jetzt überall per
  vollem `key` (region/slug): `make_city_packets.py` erzeugt `### <key>`, Antworten und
  `city-copy.json` sind auf `key` umgeschlüsselt, `load.mjs` liest `cityCopy[c.key]`. 792/792
  decken sich 1:1. Keine zweite Stelle gefunden, die nach Kurz-Slug ohne Bundesland schlüsselt.

## (3) Drei Betriebe wegen Verhaltens ausschließen

**Genaue Einträge (zur Bestätigung vor dem Löschen — GATE B):**

| Name | Ort | Slug |
|---|---|---|
| Schlüsseldienst Herzog | Mannheim | `schluesseldienst-herzog-mannheim` |
| Schlüsseldienst Nürnberg \| Kurt Schlüsseldienst | Nürnberg | `schluesseldienst-nuernberg-kurt-schluesseldienst-nuernberg` |
| Schlüssel One | Erlangen | `schluessel-one-erlangen` |
| Schlüssel One | Fürth | `schluessel-one-fuerth` |

Nicht betroffen (gleicher Name, andere Betriebe, bleiben): Herzog Car Key (Leimen), Schlüsseldienst
Kurt (Kempten), Kurt Schlüsseldienst (Bremen), Kurt Erdal (Wedel) u. a. — alles verschiedene Firmen.

**Textstellen, die nach dem Drop neu geschrieben werden (GATE B, Teil 2):**
- **Mannheim:** 4 Stellen mit Herzog, darunter „Die größte Bewertungsbasis hat Schlüsseldienst
  Herzog …" und die Nennung unter den rund-um-die-Uhr-Betrieben. Der eigene Herzog-Absatz wird
  entfernt, der Text geglättet.
- **Nürnberg:** der „Schlüsseldienst Nürnberg von Kurt" (4 Stellen).
- **Erlangen:** Schlüssel One (4 Stellen). **Fürth:** Schlüssel One (6 Stellen).
- **Nachbarstädte geprüft:** Ludwigshafen/Heidelberg nennen Herzog **nicht**; Fürth/Erlangen nennen
  den Nürnberg-Kurt **nicht**. Kein weiterer Text betroffen.

Diese vier Städte werden nach dem Drop ohnehin voll neu erzeugt (Paket ändert sich), was zugleich
die Bewertungszahlen aus (1) dort erledigt.

**Grund in `04-exclusions.csv`** wird wahrheitsgemäß eingetragen (dokumentiertes Fehlverhalten
gegenüber dem Betreiber), nie als „fremdes Gewerbe" getarnt. Welcher genaue Wortlaut je Betrieb? Ich
schlage vor: „dokumentiertes Fehlverhalten gegenüber dem Betreiber (…)". Sag mir die konkreten
Vorgänge, dann trage ich sie knapp und wahr ein.

**Maßstab festgehalten:** neue Wiki-Seite `framework/conduct-exclusions.md` — wann ein Betrieb wegen
Verhaltens ausgeschlossen wird (Warnung, Presse/Gericht, Bewertungsmuster mit Preisstreit,
dokumentierte eigene Kenntnis), Grund immer wahrheitsgemäß, Maßstab für alle gleich. Begründung
aufgenommen: eigene belegbare Kenntnis wiegt schwerer als die Google-Bewertung.

## Zusammengefasst wartet auf dich
- **GATE A:** Freigabe des gezielten Umschreib-Laufs (~5–12 $, Probe zuerst).
- **GATE B:** Bestätigung der vier Slugs zum Drop **und** die konkreten Vorgänge für den
  Ausschlussgrund.
Danach: droppen → vier Städte neu + Umschreib-Lauf → prüfen (0 Datenzahlen) → `city-copy.json`.
