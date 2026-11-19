# Versand-Export: drei Anpassungen (Variante-Schwelle, fremde Gewerbe, telefon_national)

**Datum** 2026-11-19 · **Kein Versand, kein Export, nichts vermerkt** · `listings.csv` und das
Verzeichnis unverändert. Alle Probeläufe mit `--probe`; die Live-Bücher blieben unberührt. Nur
Zahlen und öffentliche Firmennamen in diesem Bericht — keine Mail-Adressen von Betrieben.

Geändert wurde nur `scripts/kontakt.py` (plus `CLAUDE.md`, Bericht, Log).

## 1. Variante `platz` nur ab Bewertung 4,0

Neue Konstante **`PLATZ_HOOK_MIN_BEWERTUNG = 4.0`** neben `PLATZ_HOOK_MIN_ANZAHL`. Die Mail-Variante
ist jetzt nur `platz`, wenn der Eintrag eine Bewertung hat **und** die Stadtseite ≥ 5 Einträge führt
**und** die Bewertung ≥ 4,0 ist. Darunter `telefon`. Grund: Ein hoher Platz bei schlechter Bewertung
ist kein guter Aufhänger (der Platz-Text wirbt mit der Reihung, die bei 1,8 Sternen gegen den Betrieb
spricht). Der Rohwert kommt als `ratingRaw` aus `dump-versand.mjs`.

## 2. Fremde Gewerbe — Trichter-Grund `fremdes_gewerbe` (vorbereitet, nicht scharf)

Neue Funktion `ist_fremdes_gewerbe(r)`: erkennt an Name oder Haupt-Kategorie (`type`) ein fremdes
Gewerbe. Zwei Signalgruppen:

- **Starke Signale** (immer fremd, außer der Eintrag ist selbst Schlüsseldienst — Name mit „Schlüssel"
  oder `type` Locksmith/Schlüsseldienst): Schuhmacher/Schuster/Schuhservice/`shoe`/`cobbler`, Gravur,
  Mister Minit, Baumarkt/`hardware store`/`building materials`/`home improvement`/`tool store`,
  Kaufhaus/`department store`/`home goods`, Tischler/Schreiner (`cabinet maker`/`joiner`/`millwork`),
  Reinigung/`dry cleaner`/`cleaners`/`clothing alteration`, Fahrrad/`bicycle`.
- **Metall-Signale** (nur fremd **ohne** Schlüssel-/Kernbezug): Metallbau, Schlosserei,
  `metal construction`/`metal workshop`/`iron ware`. Ein Metallbetrieb mit bestätigter Kernarbeit
  gilt nicht als fremd — das setzt das „ohne Schlüsseldienst" des Auftrags um.

Der Trichter-Grund ist **vorbereitet, aber standardmäßig nicht scharf**: `exportieren` zählt die
erkannten Zeilen unter den versandfertigen aus („darunter mutmaßl. fremdes Gewerbe: N — nur erkannt,
nicht entfernt"), **entfernt sie aber nicht**. Erst `FREMDES_GEWERBE_AUSSCHLIESSEN = True` schaltet den
Schritt scharf (Grund `fremdes_gewerbe`, vor der Obergrenze). Der Betreiber entscheidet anhand der
Liste unten.

**Bundesweit versandfertig: 638, davon mutmaßlich fremd: 28** (Name · Bundesland · Stadt · `type` ·
`schluesseldienst_kern` · `tueroeffnung`):

| Name | Bundesland | Stadt | type | kern | tür |
|---|---|---|---|---|---|
| MasterXPress Laufenburg | Baden-Württemberg | Laufenburg | Shoe repair shop | true | true |
| Schreinerei & Industriekletterer Schäfer Gmbh | Baden-Württemberg | Reutlingen | Millwork shop | true | — |
| Schulz & Pfahl - Haus & Rad GmbH | Baden-Württemberg | Öhringen | Home goods store | true | — |
| Schreinerei Anton J. Kiesl | Bayern | Ebersberg | Cabinet maker | true | — |
| Mittermeier | Bayern | Moosburg | Joiner | true | — |
| Schuhmacher Lehel | Bayern | München | Shoe repair shop | true | — |
| Picobello | Berlin | Berlin | Shoe repair shop | true | true |
| Schuhmacher Ei | Berlin | Berlin | Shoe repair shop | true | — |
| Tischlerei Götze GmbH | Brandenburg | Strausberg | Cabinet maker | true | — |
| Bernd's Heel Mending | Hamburg | Hamburg | Shoe repair shop | true | — |
| Janssen + Kruse GmbH & Co. KG | Niedersachsen | Emden | Building materials store | true | — |
| Tischlerei Steffen Lichtenstein | Niedersachsen | Herzberg am Harz | Joiner | true | true |
| MUTLU'S WERKSTATT - Schusterei & Reparatur | Niedersachsen | Wilhelmshaven | Shoe repair shop | true | — |
| Quadflieg | Nordrhein-Westfalen | Arnsberg | Bicycle store | true | — |
| Schröter Markus | Nordrhein-Westfalen | Dinslaken | Joiner | true | — |
| Steinrück GmbH & Co. KG | Nordrhein-Westfalen | Düsseldorf | Building materials supplier | true | — |
| M&B Gebäudeservice/Tatortreinigung GmbH | Nordrhein-Westfalen | Gelsenkirchen | Cleaners | true | true |
| Friedrich Vollmer e.K. Inh. Bergfrede GmbH & Co. KG | Nordrhein-Westfalen | Solingen | Home improvement store | true | — |
| Jann Wolfgang Inh. A. Drywa Haushaltswaren | Nordrhein-Westfalen | Steinheim | Home goods store | true | — |
| Friedrich Wilh. Waldhausen GmbH & Co. KG | Nordrhein-Westfalen | Übach-Palenberg | Hardware store | true | — |
| Robert Schmidt e. K. | Rheinland-Pfalz | Betzdorf | Tool store | true | — |
| Ralf Staudt Schreinermeister | Rheinland-Pfalz | Bingen am Rhein | Joiner | true | — |
| TB Textilreinigung - Wäscherei Annahmestelle | Rheinland-Pfalz | Neuwied | Dry cleaner | true | — |
| Dienstleistungsservice by Rossi Inh. Steffen Rosse | Sachsen | Dresden | Shoe repair shop | true | — |
| Zweiradhaus Thomas Röhricht | Sachsen | Zittau | Bicycle store | true | — |
| Tischlerei Wilhelm Piening Inh. Bernd Piening | Schleswig-Holstein | Hanerau-Hademarschen | Millwork shop | true | — |
| Tischlerei Schlüter | Schleswig-Holstein | Neumünster | Cabinet maker | true | true |
| Tischlerei Witter | Thüringen | Schleusingen | Cabinet maker | true | — |

(„tür" = `tueroeffnung`; „—" = `not enough info`. Alle 28 haben `schluesseldienst_kern = true`, kamen
also über die Kernarbeit in den Versand — darum lohnt die Handprüfung. Ein echter Mischbetrieb wie
„Shoe & Locksmiths Laim", München, `type` Locksmith, wird **nicht** gelistet.)

## 3. Neue Spalte `telefon_national`

`exportieren` schreibt zusätzlich **`telefon_national`** (`+49 177 3977646` → `0177 3977646`,
`+49 89 221747` → `089 221747`). `telefon` bleibt unverändert im Website-Format. Umsetzung: Helfer
`zu_national` ersetzt führendes `+49`/`0049` durch `0`, Reststruktur bleibt; nicht deutsche Formate
bleiben unangetastet.

## Probe Bayern (erneut, `--probe`)

| | vorher | nachher |
|---|---:|---:|
| versandfertig | 91 | 91 |
| davon Variante `platz` | 79 | **76** |
| davon Variante `telefon` | 12 | **15** |
| darunter mutmaßl. fremdes Gewerbe | — | 4 |

Drei Zeilen wechselten von `platz` zu `telefon`, weil ihre Bewertung unter 4,0 liegt (darunter
„Schuhmacher Lehel", München, 1,8). `versandfertig` bleibt 91 — es wurde nichts entfernt.

## Fünf Beispielzeilen Bayern (mit neuer Spalte)

| anrede | name | city | platz | anzahl | bew. | bew.-zahl | telefon | telefon_national | variante |
|---|---|---|---:|---:|---|---|---|---|---|
| Hallo Andreas Dries, | Aschaffenburger Schlüsseldienst | Aschaffenburg | 1 | 11 | 5,0 | 130 | +49 6021 4566630 | 06021 4566630 | platz |
| Guten Tag, | Schlüsseldienst Korb | Fürth | 4 | 10 | 4,8 | 71 | +49 911 771379 | 0911 771379 | platz |
| Guten Tag, | Schuhmacher Lehel | München | 74 | 78 | 1,8 | 5 | +49 89 221747 | 089 221747 | telefon |
| Guten Tag, | KA Service Schlüsseldienst | Dachau | 1 | 4 | 5,0 | 131 | +49 177 3977646 | 0177 3977646 | telefon |
| Guten Tag, | Schlüsseldienst Müller Erlangen | Erlangen | 4 | 4 | 5,0 | 19 | +49 151 26959850 | 0151 26959850 | telefon |

„Schuhmacher Lehel" ist jetzt `telefon` (Bewertung 1,8 < 4,0) und steht zugleich auf der
fremde-Gewerbe-Liste. Dachau und Erlangen sind `telefon`, weil ihre Stadtseite nur 4 Einträge führt
(< 5).

## Offen beim Betreiber

Anhand der 28er-Liste entscheiden, welche fremden Gewerbe raus sollen (per `kontakt.py sperren`), und
ob der Trichter-Schritt künftig scharf geschaltet wird (`FREMDES_GEWERBE_AUSSCHLIESSEN = True`).
