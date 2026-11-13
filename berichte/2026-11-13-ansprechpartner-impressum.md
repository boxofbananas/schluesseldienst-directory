# Ansprechpartner aus dem Impressum lesen

**Datum** 2026-11-13 · **Kein Versand, kein Deploy** · `listings.csv` und das Verzeichnis
unverändert. Nur Zahlen in diesem Bericht — keine Namen, keine Adressen.

Namen und Fundstellen stehen ausschließlich in der gitignorierten Datei
`output/<slug>/kontakt-ansprechpartner.csv`; der Zwischenspeicher `impressum-cache.json` erlaubt
Fortsetzen und erneutes Auslesen ohne neuen Abruf. Werkzeug: `scripts/impressum.py`.

## Umfang

Anschreibbar = Website vorhanden, nicht eigener Betrieb **und E-Mail-Adresse** (ohne E-Mail kein
Zweck). Das sind **1.144 Einträge** auf **1.073 Domains**. Ein Abruf je Domain, höflich (üblich
`/impressum`, sonst ein Startseiten-Abruf + Fußlink; Pause 1,2 s; neutraler Client-Name; keine
Verbindung zu den Schlüsseldienst-Websites). **60 geteilte Domains** (mehrere Einträge auf einer
Domain = Portal/Kette) wurden gar nicht erst abgerufen.

## Ergebnis des Abrufs (je anschreibbarem Eintrag)

| | Zahl |
|---|---:|
| Name **gefunden** | **558** |
| **nicht gefunden** | **554** |
|   · davon fremdes Impressum (Agentur/Portal/anderer Firmenname) | 23 |
|   · davon geteilte Domain (nicht abgerufen) | 131 |
|   · davon erreichbar, aber keine Person im Impressum lesbar | 400 |
| Domain **nicht abrufbar** | **32** |
| **Summe** | **1.144** |

Kein Name wurde geraten: keiner aus E-Mail-Adresse, Firmenname oder Bewertung. Firmen-only-Impressen
(„Vertreten durch: … GmbH") und Fremdimpressen liefern kein Feld. Eine erste, zu großzügige Fassung
griff Straßennamen, Überschriften und EU-Boilerplate ab; strengere Regeln verwerfen das jetzt
(lieber leer als falsch).

## Versandfilter: nur bestätigte Kernbetriebe

Nur Einträge mit dem Merkmal **`schluesseldienst_kern`** oder **`tueroeffnung`** als bestätigt
kommen in den Export (`kontakt.py --offen --export`). Fremde Gewerbe, die nur über die Kategorie
`locksmith` hereinkamen, fallen aus dem Versand.

Von den **1.144** anschreibbaren Einträgen:

| | Zahl |
|---|---:|
| Kernbetrieb bestätigt (**bleiben im Versand**) | **728** |
| **fallen weg** (kein Kernmerkmal bestätigt) | **416** |

**Haupt-Kategorien der 416 Wegfallenden** (`type`):

| Haupt-Kategorie | Anzahl |
|---|---:|
| Locksmith (ohne bestätigte Kernarbeit, beide Merkmale „not enough info") | 127 |
| Security system supplier | 104 |
| Safe & vault shop | 38 |
| Key duplication service | 31 |
| Safety equipment supplier | 24 |
| Shoe repair shop | 7 |
| Metal construction company | 5 |
| Cabinet maker | 5 |
| Security system installation service | 5 |
| Window supplier | 4 |
| Burglar alarm store | 4 |
| Electrician | 3 |
| Tool store | 3 |
| Emergency locksmith service | 3 |
| Security guard service | 3 |
| übrige (Bicycle store, Hardware store, Iron ware dealer, Shoe store, Auto tune up service u. a.) | 42 |

## Versandliste, zusammengeführt

| | Zahl |
|---|---:|
| Versand (Kernbetrieb mit E-Mail) | **728** |
|   · mit persönlichem Namen → Anrede „Hallo Vorname Nachname," | **348** |
|   · ohne Namen → Anrede „Guten Tag," | 380 |

Über das ganze Verzeichnis (alle offenen Einträge, Kernfilter, alle Kanäle) umfasst der Export
**2.286 Zeilen**, davon **728 mit E-Mail** und **348 mit persönlichem Namen**.

## Drei Ergänzungen (umgesetzt)

1. **Fremde Impressen ausgesperrt.** Ein Name wird nur übernommen, wenn das Impressum erkennbar
   zum gelisteten Betrieb gehört (unterscheidender Namensteil in der Domain; mindestens zwei
   Namensteile in der Domain; Nachname in Domain oder Firmenname; unterscheidender Namensteil
   **ohne Ort** im Impressum-Kopf). Geteilte Domains bekommen nie einen Namen.
   - **Anmerkung zu `1a-schreinerei.de`:** Der *gelistete Betrieb heißt dort selbst „Schreinerei
     Kober GmbH & Co. KG"*, und das Impressum nennt dieselbe Firma — es ist also **kein**
     Fremdimpressum; Patrick Kober betreibt genau diesen Eintrag (eine Schreinerei, über die
     Kategorie `locksmith` hereingekommen). Die Regel behält ihn zu Recht; echte Fremdfälle wie
     `weblocator.de` werden ausgesperrt. Diese Schreinerei fällt ohnehin über den Versandfilter
     oben weg, wenn ihr Kernmerkmal nicht bestätigt ist — das ist eine Gewerbe-, keine
     Namensfrage.
2. **Einzelbuchstaben weg.** „Klaus D Mapara" wird zu „Klaus Mapara" (im gespeicherten Namen und
   in der Anrede).
3. **Anrede.** Mit Namen „Hallo Vorname Nachname,", ohne Namen „Guten Tag,".

## Dateien und Schutz

- Neu: `scripts/impressum.py`. Geändert: `scripts/kontakt.py` (Export mit `vorname`/`nachname`/
  `anrede` und Kernbetrieb-Filter), `CLAUDE.md`, `.gitignore`.
- Gitignoriert (personenbezogen): `kontakt-ansprechpartner.csv`, `impressum-cache.json`,
  `kontakt-export*.csv`.
- `listings.csv` nur gelesen; nichts gebaut, nichts ausgeliefert, nichts versendet.
