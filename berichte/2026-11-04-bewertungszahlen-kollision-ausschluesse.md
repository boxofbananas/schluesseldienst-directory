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

**Freigegeben und gestartet (GATE A):** gezielter **Umschreib-Lauf** über den neuen `rewrite`-Modus
von `run_batches.py` — er liest die vorhandene Antwort, nicht das Paket, und schreibt nur die
gemeldeten Zahl-Sätze um (Aussage behalten, Ziffer weg). Zwei Probestapel gemessen: leichte
Kleinstadt-Seite **2,7 ct/Stadt**, schwerer Großstadt-Stapel ~14 ct (mit Retry). Gewichtet über die
775 (weit überwiegend kleine Orte) **~$35–45**. Endkosten im Nachtrag unten.

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
| Name | Ort | Adresse | Telefon | Slug |
|---|---|---|---|---|
| Schlüsseldienst Herzog | Mannheim | Waldpforte 13, 68305 Mannheim | +49 621 43772508 | `schluesseldienst-herzog-mannheim` |
| Schlüsseldienst Nürnberg \| Kurt Schlüsseldienst | Nürnberg | Neustädter Str. 142, 90431 Nürnberg | +49 173 6582728 | `schluesseldienst-nuernberg-kurt-schluesseldienst-nuernberg` |
| Schlüssel One | Erlangen | Friedrichstraße 27, 91054 Erlangen | +49 9131 9334333 | `schluessel-one-erlangen` |
| Schlüssel One | Fürth | Schwabacher Str. 138, 90763 Fürth | +49 911 99967428 | `schluessel-one-fuerth` |

**Verwechslungsprüfung (du wolltest es genau):**
- **„Kurt" im Namen, alle Städte:** 11 Einträge, aber nur **einer in Nürnberg** — der Ziel-Betrieb.
  Die übrigen liegen in Wedel, Berlin (2×), Kempten, Bornheim, Großkarolinenfeld, Siegsdorf, Bremen,
  Rostock, Seiffen — **andere Firmen, bleiben alle**.
- **In Nürnberg** gibt es außerdem „Sos Schluesseldienst" und „Turbo-Schlüsseldienst Nürnberg" —
  **andere Namen, andere Nummern, bleiben** (sie teilen nur den Nürnberg-Stadttext mit dem Ziel).
- **„Schlüssel One", alle Städte:** existiert **nur** in Erlangen und Fürth. Keine weitere Stadt.

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

**Grund in `04-exclusions.csv`:** gemäß deiner Korrektur steht in der Spalte `reason` **nur das
Kürzel `verhalten_betreiber`** — keine Schilderung des Vorgangs, nicht in der CSV, nicht in diesem
Bericht, nicht im Wiki. Das Kürzel verweist auf den Maßstab; die Belege bleiben beim Betreiber
außerhalb des Repositorys. Ich brauche also **keine** Vorgangsbeschreibung von dir — nur das „Ja" zu
den vier Slugs.

**Maßstab festgehalten:** neue Wiki-Seite `framework/conduct-exclusions.md` — wann ein Betrieb wegen
Verhaltens ausgeschlossen wird (Warnung, Presse/Gericht, Bewertungsmuster mit Preisstreit,
dokumentierte eigene Kenntnis), der Grund steht nur als Kürzel, Maßstab für alle gleich. Begründung
aufgenommen: eigene belegbare Kenntnis wiegt schwerer als die Google-Bewertung; und schriftliche
Vorwürfe gegen namentlich genannte Dritte gehören nicht in eine versionierte Datei.

## Stand und was auf dich wartet
- **(A) läuft:** Probe gemessen (leichte Stadt **2,7 ct**, schwere ~9–14 ct); voller Umschreib-Lauf
  auf Sonnet gestartet, Schätzung **~$35–45**. Endkosten im Nachtrag.
- **(B) wartet nur noch auf dein „Ja"** zu den vier Slugs oben (kein Vorgang nötig). Danach: droppen
  (`reason=verhalten_betreiber`) → die vier Städte neu + Textstellen glätten → prüfen → `city-copy.json`.
