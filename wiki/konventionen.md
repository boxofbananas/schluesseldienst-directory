---
title: Konventionen der deutschen Fassung
type: framework
status: stable
updated: 2026-11-03
---

# Konventionen der deutschen Fassung

Diese Datei ist der verbindliche Vertrag für alle Umbauten des Directory Blueprints auf das
deutsche Projekt. Bei Widerspruch zu einer englischen Wiki-Seite gilt diese Datei.

## Das Projekt

- Verzeichnis: **Die besten Schlüsseldienste** – alle Schlüsseldienste in Deutschland
- Domain: `die-besten-schluesseldienste.de`
- Herausgeber: DOM Holding GmbH, Anton-Bruckner-Straße 8, 90571 Schwaig bei Nürnberg
- Geschäftsführer: Daniel Merz, HRB 43586
- Branche: Schlüsseldienst (Google-Maps-Kategorie `locksmith`)
- Wichtigste Stadt: Mannheim

## Gliederung: drei Ebenen statt zwei

Die englische Fassung kennt einen Bundesstaat mit Städten darunter. Die deutsche Fassung hat
Deutschland als Ganzes, **16 Bundesländer** als Zwischenebene und Städte darunter.

| Ebene | URL | Anzahl |
|---|---|---|
| Startseite | `/` | 1 |
| Blättern (noindex, follow) | `/verzeichnis/` | 1 |
| Bundesland | `/verzeichnis/[bundesland]/` | bis 16 |
| Stadt | `/verzeichnis/[bundesland]/[stadt]/` | je Stadt ab Mindestzahl |
| Eintrag | `/firma/[bundesland]/[stadt]/[slug]/` | je Eintrag |
| Leistung | `/leistungen/[slug]/`, Index `/leistungen/` | je Leistung |
| Eintrag beanspruchen | `/eintrag-beanspruchen/` | 1 |
| Premium / Werbung | `/premium/` | 1 |
| Festpreis-Garantie: Erklärung und Prüfpunkte (indexiert) | `/festpreis-garantie/` | 1 |
| Garantie-Antrag (noindex) | `/festpreis-garantie/antrag/` | 1 |
| Garantie-Nachweis (noindex) | `/auszeichnung/[slug]/`, Bild `/auszeichnung/[slug].svg` | je Betrieb mit Garantie |
| Über uns | `/ueber-uns/` | 1 |
| Kontakt | `/kontakt/` | 1 |
| Impressum | `/impressum/` | 1 |
| Datenschutz | `/datenschutz/` | 1 |
| AGB | `/agb/` | 1 |
| Suche | `/suche/` | 1 |
| Ratgeber | `/ratgeber/[slug]/` | 0 zum Start |

Die Startseite verlinkt alle Bundesländer und die 20 größten Städte. Die Bundesland-Seite
verlinkt jede Stadt des Landes. Alles andere wie in [[site-architecture]].

Bundesland-Slugs (aus `site.json` → `regions`, nicht erraten):
`baden-wuerttemberg`, `bayern`, `berlin`, `brandenburg`, `bremen`, `hamburg`, `hessen`,
`mecklenburg-vorpommern`, `niedersachsen`, `nordrhein-westfalen`, `rheinland-pfalz`,
`saarland`, `sachsen`, `sachsen-anhalt`, `schleswig-holstein`, `thueringen`.

Kürzel: BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH.

## Umlaute

`slugify` muss **vor** dem Entfernen der Sonderzeichen umschreiben:
`ä→ae`, `ö→oe`, `ü→ue`, `Ä→ae`, `Ö→oe`, `Ü→ue`, `ß→ss`.
Sonst wird aus „Nürnberg" `n-rnberg`. Das gilt für Städte, Bundesländer, Firmennamen und
Leistungen. Zwei Städte mit gleichem Namen im gleichen Bundesland: Postleitzahl anhängen.

## Telefonnummern

Deutsche Nummern, nicht US-Format.
- Anzeige: `+49 621 1234567` – Ländervorwahl, Ortsvorwahl, Rest zusammen.
- `tel:`-Link und schema.org: `+49621 1234567` ohne Leerzeichen (E.164: `+496211234567`).
- Nummern, die mit `0` beginnen: führende Null entfernen, `+49` davor.
- Nicht erkennbare Nummern unverändert ausgeben.

## Öffnungszeiten

Google liefert deutsche Tagesnamen und 24-Stunden-Zeiten. Der Parser muss beides verstehen:
- Tage: `Montag` … `Sonntag` **und** `Monday` … `Sunday`
- Zeiten: `08:00–17:00`, `8:00-17:00`, `00:00–24:00`
- `Geschlossen` / `Closed` → geschlossen
- `Durchgehend geöffnet` / `24 Stunden` / `Open 24 hours` → `00:00–23:59`
Für schema.org `openingHoursSpecification` werden die deutschen Tage auf `Mo`…`Su` abgebildet.

## Sprache und Ton

- Alles auf Deutsch, Sie-Anrede, `lang="de"` im HTML.
- Sachlich, keine Werbesprache, keine Superlative über das Verzeichnis selbst.
- Keine Formulierung, die eine amtliche Stelle vortäuscht: nie „Innung", „Verband",
  „Kammer", „amtlich", „offiziell geprüft", „Verbraucherschutz", „getestet".
- Preise in Euro mit Komma: `97 €`, `29 €`, `250 €`.
- Datumsformat `TT.MM.JJJJ`, Dezimaltrennzeichen Komma (Bewertung `4,8`).

## Wortliste (verbindlich)

| Englisch | Deutsch |
|---|---|
| listing | Eintrag |
| featured listing | Premium-Platz |
| premium listing | Premium-Eintrag |
| best-of placement | Top-Platzierung |
| claim your listing | Eintrag beanspruchen |
| claimed | bestätigt |
| verified / vetted | geprüft (intern); sichtbar: Festpreis-Garantie |
| reviews | Bewertungen |
| rating | Bewertung |
| directory | Verzeichnis |
| city page | Stadtseite |
| buyer's guide | Ratgeber |
| resource page | Ratgeberseite |
| services | Leistungen |
| publisher | Herausgeber |
| open now | jetzt geöffnet |
| get directions | Route planen |
| what reviewers mention | Was Kunden hervorheben |
| nearby towns | Orte in der Nähe |
| thin | dünn (intern, nie sichtbar) |

## Festpreis-Garantie (neu gegenüber der englischen Fassung)

Das Programm hieß zunächst „Siegel“. Es wurde am 2026-11-03 zur **Festpreis-Garantie**
umgebaut, weil ein Siegel eine Eigenschaft des Betriebs beschreibt, eine Garantie aber ein
Versprechen an den Kunden ist – und nur das Zweite bringt dem Betrieb Kunden. Das Wort
„Siegel“ kommt in sichtbaren Texten nicht mehr vor; der interne Name des Programms ist
„Garantie-Programm“, die Wiki-Seite heißt weiter `siegel-programm.md`, damit die Wikilinks
halten.

Die Garantie hat drei Teile. Ohne einen davon ist sie nur ein Etikett:

1. **Der Preis steht im Eintrag, bevor der Kunde anruft.** Jeder Betrieb mit Garantie
   veröffentlicht seine drei Standardpreise: Türöffnung tagsüber, Türöffnung nachts (nachts,
   Wochenende, Feiertag) und Anfahrt. Sie stehen im Eintrag, auf der Stadtkarte und im
   Nachweis auf der Website des Betriebs. Spalten: `garantie_tag`, `garantie_nacht`,
   `garantie_anfahrt` – Euro-Beträge als ganze Zahl ohne Einheit; `garantie_anfahrt` = `0`
   heißt „im Preis enthalten“. Spalte `geprueft` = `true` heißt „Garantie aktiv“,
   `geprueft_jahr` = Jahr der Prüfung. Die Spaltennamen bleiben aus Rücksicht auf den Code.
2. **Der Betrieb garantiert: Der genannte Preis ist der Rechnungspreis.** Das ist das
   unterschriebene Serviceversprechen. Die Garantie gibt der Betrieb, nicht der Herausgeber;
   der Herausgeber prüft die Voraussetzungen und überwacht die Einhaltung. Das steht so auf
   `/festpreis-garantie/`.
3. **Verstoß hat Folgen.** Rechnung über dem garantierten Preis → Kunde meldet es mit
   Rechnung → Herausgeber konfrontiert den Betrieb → Garantie entzogen, Preise aus dem
   Eintrag entfernt. Der Weg zur Meldung steht auf `/festpreis-garantie/` und im Eintrag.

Zwei Stufen, beide sichtbar im Eintrag:

1. **Festpreis-Garantie** – kostenlos. Der Betrieb füllt den Antrag auf
   `/festpreis-garantie/antrag/` aus, nennt seine drei Preise verbindlich und gibt das
   Serviceversprechen ab; der Herausgeber prüft die sechs Voraussetzungen an Unterlagen und
   Website.
2. **Premium / Top-Platzierung** – kostenpflichtig, siehe `templates/featured-tiers.md`.

Die sechs Voraussetzungen, die auf `/festpreis-garantie/` veröffentlicht stehen müssen (sonst
ist die Garantie angreifbar):
- vollständiges Impressum auf der eigenen Website
- eine Telefonnummer, unter der der Betrieb erreichbar ist und bei der Prüfung tatsächlich
  abgehoben hat; die Nummer wird vor der Erteilung angerufen
- die drei Standardpreise verbindlich genannt (Türöffnung tagsüber, nachts, Anfahrt)
- liegen mindestens 5 Google-Bewertungen vor, beträgt der Schnitt mindestens 4,0; liegen weniger
  oder keine vor, entscheiden die übrigen Voraussetzungen (die Garantie sagt etwas über
  Preissicherheit, nicht über Bekanntheit – eine Mindestzahl an Bewertungen schlösse neue und
  profillose Betriebe aus, obwohl sie alle inhaltlichen Voraussetzungen erfüllen; der Riegel nach
  unten bleibt)
- keine Weiterleitung an ein Callcenter ohne Ortsbezug
- unterschriebenes Serviceversprechen: der genannte Preis ist der Rechnungspreis, keine
  Zuschläge, die nicht vorher beziffert wurden, Rechnung mit vollständiger Firmenanschrift,
  zerstörungsfreie Öffnung als Standard

Auf `/festpreis-garantie/` steht außerdem ausdrücklich: Grundlage sind Selbstauskunft und
Prüfung von Unterlagen und Website, **kein** Test vor Ort; die Garantie gibt der Betrieb. Sie
trägt die Jahreszahl, gilt ein Jahr und wird bei belegten Verstößen entzogen.

Die Garantie ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit. Dieser Satz steht wörtlich auf
`/festpreis-garantie/` und auf `/premium/`.

Darstellung im Eintrag: Betriebe mit Garantie tragen „Festpreis-Garantie 2026“ mit den drei
Preisen und Link auf `/festpreis-garantie/`. Betriebe ohne Garantie tragen „Noch keine
Festpreis-Garantie“ mit Link auf `/festpreis-garantie/antrag/` – das ist der Verkaufsanlass
und darf nicht abgeschaltet werden. Keine Formulierung, die dem Betrieb ohne Garantie etwas
unterstellt.

Stadtkarte: Betriebe mit Garantie zeigen eine Zeile „Festpreis-Garantie · Türöffnung ab
<garantie_tag> €“.

**Sortierung der Einträge auf einer Stadtseite** (Gate 5, `load.mjs`), nach den bezahlten
Plätzen in dieser Reihenfolge:
1. bezahlte Plätze (Premium/Top-Platzierung),
2. Einträge mit Festpreis-Garantie (`geprueft` = `true`),
3. Einträge mit einer **Festnetznummer, deren Ortsvorwahl zur PLZ passt** (echter Ortsbezug),
4. alle übrigen.
Innerhalb jeder Gruppe wie bisher nach Bewertung. Eine Mobilnummer oder eine Nummer, die in
mehreren Städten vorkommt, zählt **nicht** als Ortsbezug. Die Festpreis-Garantie verändert damit
die Reihenfolge (anders als zuvor): sie hebt einen Eintrag über die ortsgebundenen und die
übrigen.

Nachweis auf der Website des Betriebs: HTML-Schnipsel mit Bild `/auszeichnung/<slug>.svg`,
Text „Festpreis-Garantie 2026“ mit dem Tagespreis, verlinkt auf die Eintragsseite.

**Reserviert, nicht gebaut: Stufe „Preisschutz“.** Erstattung der Differenz bis 100 € durch
den Herausgeber, Rückgriff auf den Betrieb. Spalte `preisschutz` ist vorgesehen, aber kein
Skript und keine Seite wertet sie aus, bis der Betreiber die Stufe freigibt.

## Vorgaben des Betreibers für Gate 3 und 4 (2026-11-03)

Diese Entscheidungen hat der Betreiber vorab getroffen. Gate 3 und Gate 4 legen sie als
**Vorschlag** vor und holen die Bestätigung ein; sie löschen nichts von selbst (die Regel aus
[[listings-cleaning]] bleibt).

| Frage | Vorgabe |
|---|---|
| Umfang der Anreicherung in Gate 3 | **Alle** behaltenen Einträge, bundesweit. Geändert am 2026-11-03, nachdem der Abruf 3.102 Einträge ergab statt der geschätzten 8.000 bis 15.000: bei dieser Menge ist die vollständige Anreicherung bezahlbar, und jede Stadtseite bekommt echten Inhalt statt dünner Einträge. Die frühere Einschränkung auf Baden-Württemberg, Rheinland-Pfalz, Hessen und die 30 größten Städte gilt nicht mehr. Gate 3 nennt die Kosten trotzdem vor dem Lauf und wartet auf die Freigabe; liegen sie über 150 $, zuerst den Rhein-Neckar-Raum und die größten Städte, den Rest in einer zweiten Tranche. |
| Fremde Gewerbe (Schuhmacher, Gravur, Metallbau, Baumärkte) | Vorschlag: ausschließen, außer das Merkmal `schluesseldienst_kern` ist `true`. |
| Kettenbetriebe (gleicher Name an vielen Adressen) | Vorschlag: je Stadt eine Adresse behalten, die mit den meisten Bewertungen. |
| Callcenter ohne Ortsbezug | Vorschlag: ausschließen. Sie verfehlen Voraussetzung 5 der Festpreis-Garantie. |
| `foldMaxKm` | 30 km. Deutschland ist dichter besiedelt als die US-Vorgabe von 40 km. |
| Mindestzahl Einträge je Stadtseite (`cityFloor`) | Offen, wird in Gate 4 aus dem Gate-2-Bericht entschieden. Bei 3.102 Einträgen auf 1.266 Orte liegt der Schnitt bei 2,4 je Ort; die Vorgabe 3 würde viele Orte zu Nachbarstädten falten. Gate 4 legt dem Betreiber vor, wie viele Stadtseiten bei 3 und bei 2 entstehen, und er entscheidet. |
| Leistungsseiten | Die sechs mit `service`-Block in `attributes.json`: Notdienst, Türöffnung, Schließanlagen, Einbruchschutz, Autoschlüssel, Tresoröffnung. |
| Reihenfolge der Bundesländer auf der Startseite | nach Anzahl Einträge, absteigend. |
| Mannheim | Stadtseite im Vollausbau (oberes Wortband, 6 Fragen). Merz Sicherheit erhält Premium und Top-Platzierung zum öffentlichen Preis, als normaler Vorgang nach [[footprint-rules]], **erst nach dem Start** und erst nachdem der Betrieb die Festpreis-Garantie beantragt und bestanden hat wie jeder andere. |

## Recht

- **Impressum** nach § 5 DDG auf `/impressum/`, aus jeder Seite im Fußbereich verlinkt.
- **Datenschutzerklärung** nach Art. 13 DSGVO auf `/datenschutz/`.
- **Google-Maps-Einbettung erst nach Klick.** Keine Karte, kein Google-Font, kein externes
  Skript lädt ohne Einwilligung. Statt der Karte eine Platzhalterfläche mit Schaltfläche
  „Karte von Google Maps laden" und einem Satz, dass dabei Daten an Google übertragen werden.
  Schriften werden selbst gehostet (`fonts.css`), nie von Google geladen.
- **Keine Einwilligung nötig** und damit erlaubt: Cloudflare-Analytics ohne Cookies.
  Kein Google Analytics, keine Search Console auf dieser Domain (Footprint-Regel).
- **Bewertungen und Firmendaten** stammen aus öffentlichen Quellen; auf jeder Seite mit
  Bewertungen steht, woher die Daten kommen und wie eine Korrektur erbeten wird.
- Keine Fotos bei nicht beanspruchten Einträgen (unverändert aus der englischen Fassung).

## Fakten und Quellen (ersetzt die US-Quellen)

Für die Faktensammlung in Gate 5 gelten in dieser Reihenfolge:
Handwerkskammer des jeweiligen Bezirks, Stadt- und Gemeindeportale (Gewerbeamt),
Verbraucherzentrale des Bundeslandes, Polizeiliche Kriminalprävention der Länder und des
Bundes (`polizei-beratung.de`), Stiftung Warentest.

Nicht als Quelle verwenden: andere Schlüsseldienst-Websites, Branchenbücher, Presseportale.
Ein Punkt, für den nur eine kommerzielle Quelle gefunden wird, gilt als **unbelegt** und darf
in keinem Text auftauchen.

Wichtig für die Texte: Das Schlüsseldienst-Handwerk ist in Deutschland **kein zulassungs-
pflichtiges Handwerk** nach Anlage A der Handwerksordnung. Es gibt keine Lizenz und keine
Meisterpflicht. Texte dürfen deshalb nie von „lizenziert", „zugelassen" oder „zertifiziert"
sprechen. Erlaubt und belegbar: Gewerbeanmeldung, Eintragung im Handelsregister,
freiwillige Mitgliedschaften, Qualifikationen, die der Betrieb selbst nennt.

## Was unverändert bleibt

Struktur, Reihenfolge der Abschnitte, Seitensatz, Schema-Aufbau, die sechs Gates, die
Footprint-Regeln, die Datenhaltung in CSV und der Neubau statt Bearbeitung. Die englische
Referenzseite in `templates/master-reference/site/` bleibt der Maßstab für Aufbau und Optik.
