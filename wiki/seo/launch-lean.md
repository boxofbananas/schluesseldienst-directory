---
title: Schlanker Start (Gate 6)
type: seo
status: current
updated: 2026-11-03
---

# Schlanker Start (Gate 6)

Hausregel: alles erzeugen, die starken Seiten zuerst veröffentlichen, Vertrauen aufbauen,
dann erweitern. (Erfahrung aus dem englischen Pilotprojekt: ein Neubau startete mit 4.796
erzeugten Seiten, 1.028 davon in der Sitemap, etwa 1.100 dünne Eintragsseiten auf `noindex`,
und ging in etwa 30 Tagen von 166 auf 887 indexierte Seiten. Für Deutschland liegen keine
Messwerte vor.)

## Was zum Start in die Sitemap kommt

- **Startseite.**
- **Jede Bundesland-Seite**, die mindestens eine Stadtseite trägt. Sie sind die neue
  Zwischenebene und gehören von Anfang an hinein: ohne sie hätte die Startseite bis zu 16
  tote Zweige, und die Stadtseiten hingen an keinem Hub.
- **Jede Stadtseite** über der Mindestzahl von 3 Einträgen.
- **Jede Ortsseite**, die `foldMaxKm` freistellt. Auch sie sind indexiert.
- **Eintragsseiten mit `thin=false`** (5 oder mehr Bewertungen und eine Beschreibung).
- **Die Leistungsseiten und ihr Index**, sobald der Build sie hat ([[page-types]]).
- `/siegel/`, `/siegel/antrag/`, `/eintrag-beanspruchen/`, `/premium/`, `/ueber-uns/`,
  `/kontakt/`, `/impressum/`, `/datenschutz/`, `/agb/`.

Reihenfolge, in der sie eingereicht werden: Startseite, die Bundesland-Seiten, `/ueber-uns/`
und `/siegel/`, dann die Stadtseiten von der größten zur kleinsten (Mannheim zuerst), dann
die Eintragsseiten nach Bewertung und Zahl der Bewertungen.

## Was mit `noindex` startet

- **Eintragsseiten mit `thin=true`.** Sie werden weiter gebaut, verlinken weiter, tragen
  weiter Schema und zeigen weiter „Eintrag beanspruchen" und „Noch nicht geprüft" – eine
  Beanspruchung ist der billigste Weg, eine dünne Seite dick zu machen
  ([[siegel-programm]]).
- **`/verzeichnis/`**, die Blätterseite: `noindex, follow`.
- **`/suche/`**: `noindex`.
- **`/auszeichnung/[slug]/`**, die Siegel-Nachweisseiten: `noindex`. Sie sind Nachweis für den
  Betrieb, keine Inhaltsseite.
- **Zugeschlagene Städte** unter der Mindestzahl (sie bekommen keine Seite; ihre Einträge
  stehen auf der nächsten Stadtseite). Ein Ort jenseits von `foldMaxKm` wird nicht
  zugeschlagen und behält seine indexierte Seite ([[site-architecture]]).
- **Ein Bundesland ohne eine einzige Stadtseite** bekommt keine Seite. Erwartet wird, dass
  alle 16 eine bekommen; der Fall steht hier, damit Gate 5 nicht auf eine leere Hub-Seite
  verlinkt.
- **Der Ratgeber-Index**, solange keine echte Ratgeberseite existiert.

## Erweitern

Alle 30 Tage: indexierte Seiten und Klicks lesen (Bericht des Indexierungsdienstes und
Cloudflare-Auswertung, **keine Search Console auf dieser Domain**, [[footprint-rules]]).
Wachsen die indexierten Seiten, die nächste Stufe dünner Seiten auf indexiert stellen
(beanspruchte zuerst, dann nach Zahl der Bewertungen), neu bauen, neu einreichen.

Reihenfolge der Erweiterung über die Ebenen: zuerst die dünnen Einträge der größten Städte,
dann die der Bundesländer mit dem stärksten Zuwachs. Ein Bundesland, dessen Stadtseiten nicht
indexiert werden, bekommt keine weiteren Einträge dazu, bis das steht.

## Indexierung

Gestaffelt einreichen. Die Adressliste aus der Sitemap ist die Eingabe; 1.000 Seiten laufen 7
bis 10 Tage.

## Aus dem englischen Pilotprojekt gelernt

- **Der Build muss eine `404.html` mitbringen.** Cloudflare Pages behandelt eine Site ohne
  sie als Einzelseitenanwendung und antwortet auf jede unbekannte Adresse mit der Startseite
  und einem 200er. Das Grundgerüst hat `src/pages/404.astro`.
- **Die `pages.dev`-Adresse muss aus der Suche bleiben.** `public/_headers` schickt
  `X-Robots-Tag: noindex` auf `:project.pages.dev` und auf Vorschauadressen. Nach dem
  Ausliefern prüfen, vorher geht es nicht.
- **Ziehen und Ablegen nimmt 1.000 Dateien.** Ein Verzeichnis dieser Größe liegt darüber.
  `npx wrangler pages deploy dist` nimmt 20.000. Bei Cloudflare meldet sich der Betreiber an,
  nie Claude.
- **Von außen prüfen, bevor die Staffel beginnt:** `scripts/check_live.py`.
- **Das Startdatum** in `site.json` füllt `datePublished`. Am Tag des Ausliefern setzen, nicht
  beim Bauen.
- **Ein Gate, das nicht ausliefern kann, erzeugt trotzdem sein Ergebnis.** Fehlt die Domain
  oder die Cloudflare-Anmeldung, steht das oben in `06-launch.md` mit der Liste, was der
  Betreiber tun muss.

## Zusätzlich für diese Fassung zu prüfen

- **Impressum und Datenschutzerklärung sind erreichbar, vollständig und aus dem Fußbereich
  jeder Seite verlinkt.** Enthält eine der beiden einen Platzhalter, wird nicht ausgeliefert
  ([[page-types]]).
- **Keine Karte, kein externes Skript, keine externe Schrift lädt ohne Einwilligung.** Nach
  dem Ausliefern mit leerem Browserprofil prüfen, dass keine Anfrage an Google geht, solange
  niemand „Karte von Google Maps laden" geklickt hat ([[konventionen]]).
- **Kein Google Analytics, keine Search Console** auf dieser Domain.
- Das Verzeichnis liegt auf einem **eigenen Cloudflare-Konto**, getrennt von den
  Schlüsseldienst-Websites des Betreibers ([[footprint-rules]]).

## Die 30-Tage-Prüfung (Termin in `06-launch.md` schreiben)

Indexierte Seiten, Klicks, erste Beanspruchungen, erste Siegel-Anträge, erste Anfrage nach
einem bezahlten Platz.

## Siehe auch
[[konventionen]] · [[on-page-rules]] · [[schema]] · [[site-architecture]]
