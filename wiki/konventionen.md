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
| Siegel-Kriterien | `/siegel/` | 1 |
| Siegel-Antrag | `/siegel/antrag/` | 1 |
| Siegel-Nachweis (noindex) | `/auszeichnung/[slug]/`, Bild `/auszeichnung/[slug].svg` | je ausgezeichneter Betrieb |
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
| verified / vetted | geprüft |
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

## Siegel-Programm (neu gegenüber der englischen Fassung)

Zwei Stufen, beide sichtbar im Eintrag:

1. **Geprüft** – kostenlos. Der Betrieb füllt den Fragebogen auf `/siegel/antrag/` aus und gibt
   das Serviceversprechen ab; der Herausgeber prüft die Angaben an Unterlagen und Website.
   Spalte `geprueft` = `true`, Spalte `geprueft_jahr` = Jahr der Prüfung.
2. **Premium / Top-Platzierung** – kostenpflichtig, siehe `templates/featured-tiers.md`.

Prüfkriterien, die auf `/siegel/` veröffentlicht stehen müssen (sonst ist das Siegel
angreifbar):
- vollständiges Impressum auf der eigenen Website
- erreichbare Festnetz- oder Mobilnummer
- Preisangabe oder Anfahrtspauschale auf der Website genannt
- mindestens 10 Google-Bewertungen bei einem Schnitt von mindestens 4,0
- keine Weiterleitung an ein Callcenter ohne Ortsbezug
- unterschriebenes Serviceversprechen: Festpreis vor Arbeitsbeginn, keine versteckten
  Zuschläge, Rechnung mit vollständiger Firmenanschrift, zerstörungsfreie Öffnung als Standard

Auf `/siegel/` steht außerdem ausdrücklich: Grundlage sind Selbstauskunft und Prüfung von
Unterlagen und Website, **kein** Test vor Ort. Das Siegel trägt die Jahreszahl, gilt ein Jahr
und wird bei belegten Beschwerden entzogen.

Das Siegel ist nicht kaufbar. Bezahlt wird nur Sichtbarkeit. Dieser Satz steht auf `/siegel/`
und auf `/premium/`.

Darstellung im Eintrag: geprüfte Betriebe tragen „Geprüft 2026" mit Link auf `/siegel/`.
Nicht geprüfte Betriebe tragen „Noch nicht geprüft" mit Link auf `/siegel/antrag/` – das ist
der Verkaufsanlass und darf nicht abgeschaltet werden.

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
