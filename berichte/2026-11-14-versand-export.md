# Den Export versandfertig machen

**Datum** 2026-11-14 · **Kein Versand, kein Deploy** · `listings.csv` und das Verzeichnis
unverändert. Nur Zahlen in diesem Bericht — keine Namen, keine Adressen.

Werkzeug: `scripts/kontakt.py` (`exportieren`, `pruefen`, `importieren`, `--stand [--kampagne]`)
und der Datenschicht-Helfer `site/dump-versand.mjs`. Die versandfertige CSV und der MX-Speicher
sind gitignoriert; die Kampagnen-Liste (`kontakt-kampagnen.csv`) enthält nur Slug und Status.

## Adressen säubern und filtern (national, von 3.797 Einträgen)

| Filter | fällt weg |
|---|---:|
| eigene Betriebe | 21 |
| kein bestätigter Kernbetrieb (`schluesseldienst_kern`/`tueroeffnung`) | 1.490 |
| keine E-Mail-Adresse | 1.558 |
| E-Mail formal ungültig | 17 |
| Domain ohne Mail-Server (MX-Prüfung) | 4 |
| Portal-/Zentraladresse (nicht Freemailer, ≥ 5 Einträge) | 23 |
| Mehrfachadresse (nur der bestbewertete Bezug bleibt) | 31 |
| Stadt mit Garantie oder bezahltem Platz | 13 |
| **versandfertig** | **640** |
|   · davon mit persönlicher Anrede („Hallo …") | **331** |
|   · ohne Namen („Guten Tag,") | 309 |

Querprobe zur Impressum-Auswertung vom 2026-11-13: 728 Kernbetriebe mit E-Mail. Davon fallen durch
die Adress-Säuberung 75 (17 + 4 + 23 + 31) und durch den Städte-Filter 13 weg → **640**.

## Säuberung der Adressen (Punkt 1)

Je Eintrag eine Hauptadresse (`email_1`, sonst die nächste gefüllte). Aussortiert mit Grund: formal
ungültig (17), Domain ohne Mail-Server per MX-Prüfung (4; Rückfall auf A/AAAA nach RFC 5321, damit
keine zustellbare Adresse zu Unrecht fällt), Portal-/Zentraladresse (23: eine Nicht-Freemailer-
Adresse an fünf oder mehr Einträgen). Steht dieselbe Adresse bei mehreren Einträgen, bleibt nur der
**bestbewertete** als Bezug (31 Dubletten entfernt). Freemailer bleiben drin. Die Entscheidung ist
bundesweit, damit eine über Ländergrenzen geteilte Adresse einmal fällt.

## Felder für die Mailtexte (Punkt 2)

Je Zeile: `eintrag_url` (vollständige Adresse der Eintragsseite), `platz` und `anzahl` (Rang in der
geltenden Sortierung der Stadtseite und Zahl der Einträge dort), `bewertung` und `bewertungen` im
Format der Website (Komma, Tausenderpunkt), `hat_bewertung` (falsch, wenn keine — dann entfällt der
Halbsatz), `telefon` im Format der Website. Für einen gefalteten Betrieb (geführt auf der Seite der
Nachbarstadt) ist `stadt` die Stadt der Seite, und `platz`/`anzahl` zählen auf dieser Seite. Alle
Werte stammen aus derselben Datenschicht wie der Build und stimmen mit `dist/` überein.

## Nur Städte ohne Garantie und ohne bezahlten Platz (Punkt 3)

Die Pilot-Mail sagt „In Ihrer Stadt hat noch kein Betrieb die Festpreis-Garantie" und „wer sie als
Erster bekommt, steht ganz vorn". Einträge in Städten, in denen schon ein Betrieb die Garantie oder
einen bezahlten Platz hält, kommen nicht in den Export. Dadurch fallen — nach allen anderen Filtern
— **13** sonst versandfertige Einträge weg.

## Werte gegen die gebaute Seite geprüft (Punkt 4)

`pruefen` vergleicht an zufälligen Einträgen `platz`, `anzahl`, Bewertung und Telefon mit `dist/`:
`platz` aus dem JSON-LD `ItemList` der Stadtseite (gerenderte Reihenfolge, erste 60 — ein Eintrag
dahinter wird für den Platz übersprungen), `anzahl` aus der Überschrift, Bewertung und Telefon von
der Eintragsseite. Ergebnis über mehrere Stichproben (Seeds 0, 1, 2, 3, 7; je 20–25 Einträge):
**0 Abweichungen**. Die Werte des Exports stimmen mit der Seite überein.

## Kampagnen, Import, Stand (Punkte 5–7)

- **Kampagne (5):** jeder Export trägt einen Namen und eine Obergrenze (`--limit`), filterbar nach
  Bundesland und Stadt. Exportierte Einträge werden als „vorgesehen" vermerkt und nicht ein zweites
  Mal exportiert (geprüft: zweiter Lauf lässt die bereits vorgesehenen weg).
- **Import (6):** `importieren` liest die Ergebnis-CSV einer Versandplattform (Slug **oder** E-Mail
  — trifft die E-Mail mehrere Einträge, wird die Zeile als unklar gemeldet, nicht geraten; Status
  mit Synonym-Abbildung; Datum deutsch oder ISO). Jede Zeile wird ein Hauptbuch-Eintrag;
  „abgemeldet" und „unzustellbar" kommen zusätzlich auf die Sperrliste. Unbekannte Status- und
  Zeilen werden gemeldet, nicht geraten. Das Spaltenformat steht in `kontakt.py --help`.
- **Stand (7):** `--stand --kampagne <name>` zeigt exportiert, gesendet, geantwortet, abgemeldet,
  unzustellbar und die daraus entstandenen Anträge (Hauptbuch) und Festpreis-Garantien
  (`garantie-hauptbuch.csv`).

## Pilot-Vorschlag (Punkt 8)

Versandfertige Einträge je Bundesland **ohne eigene Betriebe**, nach allen Filtern (Anteil mit
Namen in Klammern):

| Bundesland (ohne eigene Betriebe) | versandfertig | mit Namen |
|---|---:|---:|
| Nordrhein-Westfalen | 161 | 79 |
| Bayern | 91 | 50 |
| Niedersachsen | 57 | 25 |
| Berlin | 47 | 21 |
| Sachsen | 35 | 19 |
| Hamburg | 25 | 18 |

**Drei Regionen für den Pilot:** Nordrhein-Westfalen (Obergrenze 100 → 100, 79 mit Namen),
Bayern (91, 50 mit Namen), Niedersachsen (57, 25 mit Namen). Die Marke „etwa 100 je Region"
erreichen bei Null eigenen Betrieben nur Nordrhein-Westfalen (gedeckelt) und Bayern; die drittgrößte
solche Region ist Niedersachsen mit 57.

## Ein abgefangener Platzhalter

Ein Impressum (`sicherheitstechnik-fries.de`) trägt den Vorlagen-Namen „Max Mustermann", den
`impressum.py` als natürliche Person gelesen hat. Der Export fängt solche Platzhalter am Rand ab
(leeres Namensfeld, Anrede „Guten Tag,") — es würde nie „Hallo Max Mustermann," versendet. Betroffen:
1 Eintrag; darum 331 statt 332 mit persönlicher Anrede.

## Dateien und Schutz

- Neu: `site/dump-versand.mjs` (und `templates/astro/dump-versand.mjs`). Geändert:
  `scripts/kontakt.py` (exportieren/pruefen/importieren/Stand), `CLAUDE.md`, `.gitignore`.
- Anhängende Bücher: `kontakt-hauptbuch.csv`, `kontakt-sperrliste.csv`, `kontakt-kampagnen.csv`
  (Slug + Status, keine Adressen).
- Gitignoriert (Adressen bzw. regenerierbar): `kontakt-export*.csv`, `versand-mx-cache.json`,
  `kontakt-ansprechpartner.csv`, `impressum-cache.json`.
- `listings.csv` nur gelesen; nichts gebaut, nichts ausgeliefert, nichts versendet. Alle Probeläufe
  liefen auf Kopien der Bücher (Scratch), die Live-Bücher blieben leer.
