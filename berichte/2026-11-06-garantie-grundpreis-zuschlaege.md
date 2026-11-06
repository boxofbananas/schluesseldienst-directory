# Festpreis-Garantie: Grundpreis + Zuschläge statt zwei Pauschalpreisen

**Datum:** 2026-11-06
**Auslöser:** Daniel — das Preismodell der Festpreis-Garantie soll dem tatsächlichen
Abrechnungsmodell der Branche folgen: ein **Grundpreis** für die Türöffnung plus **benannte
Zuschläge**, nicht ein Tag- und ein Nachtpreis. Mannheimer Beispiel: Türöffnung werktags 89 €,
abends/Wochenende/Feiertag +30 €, nachts 0–7 Uhr +40 €, Zuschläge nicht kumulativ.

## Was sich am Datenmodell ändert

| alt | neu |
|---|---|
| `garantie_tag` (Tagespreis) | `garantie_tag` = **Grundpreis werktags** (Bedeutung bleibt, Sinn geschärft) |
| `garantie_nacht` (Nachtpreis, absolut) | **stillgelegt** — nicht umbenannt |
| — | `garantie_zuschlag_abend` (Zuschlag abends/Wochenende/Feiertag) |
| — | `garantie_zuschlag_nacht` (Zuschlag nachts 0–7 Uhr) |
| `garantie_anfahrt`, `garantie_zylinder`, `garantie_zylinder_5mm` | unverändert |

Die Spaltennamen sind **sprechend** (nicht `_1`/`_2`), damit niemand sie verwechselt.

### Migrations-Riegel
`garantie_nacht` wird **stillgelegt**, nicht entfernt und nicht umbenannt. In beiden `load.mjs`
(Build + Template) bricht der Build jetzt mit Fehler ab, sobald eine **nicht-leere**
`garantie_nacht`-Zelle gefunden wird — ein alter Absolutpreis, der stillschweigend als Zuschlag
gelesen würde, wäre der schlimmste Fehler. Geprüft: leer → ok, Spalte fehlt → ok, gefüllt →
Abbruch mit sprechender Meldung.

## Zeitfenster (lückenlos, überschneidungsfrei)

- **Grundpreis**: Mo–Fr 7–20 Uhr
- **Zuschlag abends/Wochenende/Feiertag**: Mo–Fr 20–24 Uhr sowie Sa, So, Feiertag 7–24 Uhr
- **Zuschlag nachts**: täglich 0–7 Uhr

Jeder Zeitpunkt fällt in genau ein Fenster. Es gilt **Grundpreis plus höchstens ein Zuschlag;
Zuschläge werden nicht addiert.**

## Darstellung im Eintrag

Der Preisblock hat jetzt **drei beschriftete Gruppen** statt zwei:

1. **Dienstleistung (Festpreis)** — Türöffnung (Grundpreis werktags), Anfahrt
2. **Zuschläge (statt des Grundpreises, nicht kumulativ)** — abends/Wochenende/Feiertag, nachts;
   darunter die Zeile „Zuschläge werden nicht addiert: Grundpreis plus höchstens ein Zuschlag."
   Die Gruppe erscheint nur, wenn mindestens ein Zuschlagsfeld gesetzt ist.
3. **Material bei abgeschlossener Tür** — Standardzylinder, Aufschlag je 5 mm

Die Stadtkarte zeigt weiterhin „Festpreis-Garantie · Türöffnung ab `<garantie_tag>` €" — der
Grundpreis ist der richtige Ab-Preis. Der Garantie-Nachweis (HTML-Schnipsel) ebenso.

Bildschirmfoto des vollständigen Blocks (alle drei Gruppen, vorübergehend geflaggter
Fremdeintrag, danach zurückgesetzt): bei 390 und 1440 px geprüft, kein Überlauf, Preise
rechtsbündig, Hinweiszeile kursiv/gedämpft.

## Geänderte Dateien

**Code / Render** (Build + Template gespiegelt):
- `src/lib/load.mjs` — neues `garantie`-Objekt (`zuschlagAbend`, `zuschlagNacht`),
  Migrations-Riegel
- `src/components/Garantie.astro` — Zuschläge-Gruppe + Hinweiszeile
- `src/styles/global.css` — `.garantie-hinweis`
- `src/data/listings.csv` — Spaltenmigration (`garantie_nacht` → zwei Zuschlagsspalten, leer)
- `src/pages/festpreis-garantie/index.astro` — Prosa (Kurzfassung, „Die drei Teile",
  Voraussetzung 3, Serviceversprechen)
- `src/pages/festpreis-garantie/antrag/index.astro` — Felder + Serviceversprechen-Zusagen
- `functions/api/claim.ts` — Garantie-Feldliste

**Pipeline-Skripte:** `clean_listings.py` (GARANTIE-Liste + Bericht), `add_own_listings.py`,
`merge_enriched.py`.

**Wiki / Doku:** `konventionen.md` (Preissemantik, Voraussetzung 3, Serviceversprechen,
Darstellung, Nachweis), `siegel-programm.md` (alle Parallelstellen), `page-types.md`,
`page-sections.md`, `footprint-rules.md`, `outscraper-columns.md`, `listings-cleaning.md`,
`refresh-and-upkeep.md`, `copy-gate.md`, `index.md`, `enrichment-instructions.md`,
`CLAUDE.md`, `README.md`, `astro-skeleton.md`. Historische Berichte, `log.md` und Gate-Caches
bleiben als Zeitdokument unverändert.

## Die vollständige Voraussetzungsliste (sechs)

1. Vollständiges Impressum auf der eigenen Website.
2. Eine erreichbare Telefonnummer, bei der Prüfung tatsächlich abgehoben; wird vor der Erteilung
   angerufen.
3. **Die Preise verbindlich genannt:** der Grundpreis der Türöffnung (werktags 7–20 Uhr), die
   beiden benannten Zuschläge (abends/Wochenende/Feiertag sowie nachts 0–7 Uhr, nicht kumulativ)
   und die Anfahrt; und — für die abgeschlossene Tür — die beiden Materialpreise (Standardzylinder,
   Aufschlag je 5 mm Mehrlänge).
4. Liegen mindestens fünf Google-Bewertungen vor, beträgt der Schnitt mindestens 4,0; liegen
   weniger oder keine vor, entscheiden die übrigen Voraussetzungen.
5. Kein Callcenter ohne Ortsbezug.
6. Unterschriebenes Serviceversprechen.

## Das Serviceversprechen (fünf Zusagen)

1. **Der Grundpreis der Türöffnung und die genannten Zuschläge sind verbindlich und stehen auf
   der Rechnung.** Es wird höchstens ein Zuschlag berechnet; Zuschläge werden nicht addiert. Der
   Preis gilt für die zugefallene wie die abgeschlossene Tür und wird vor Arbeitsbeginn bestätigt.
2. **Bei einer abgeschlossenen Tür kommt nur das Material dazu**, zu den genannten Beträgen
   (Standardzylinder, Aufschlag je 5 mm). Außer den genannten Zuschlägen keine weiteren.
3. **Defekte Türen und Sonderfälle werden vor Arbeitsbeginn beziffert**; gearbeitet wird erst nach
   Zustimmung.
4. **Rechnung mit vollständiger Firmenanschrift.**
5. **Zerstörungsfreie Öffnung**, wo technisch möglich.

## Stand

Schema steht, Build grün (4629 Seiten, Riegel grün, Schriftprüfung bestanden), ausgeliefert,
live geprüft (`check_live.py`: alles bestanden außer der bekannten www-Umleitung, die am fehlenden
Dynamic-Redirect-Recht des Tokens hängt — Daniels Schritt). Es ist **noch kein Preis eingetragen**;
jeder Eintrag zeigt „Noch keine Festpreis-Garantie". Daniels Zahlen kommen, wenn das Schema steht —
es steht jetzt.

**Stripe:** Die drei Zahlungslinks liegen vor, aber noch ohne Zuordnung zur Stufe. Ich trage sie
erst ein, wenn Daniel bestätigt, welcher Link zu welcher Stufe gehört; dann in `site.json` bei den
Stufen und `/danke/` als Weiterleitungsziel. Nicht vorbereitet.
