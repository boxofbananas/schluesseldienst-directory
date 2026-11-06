# Starttag der Staffel auf heute (2026-11-06)

**Datum:** 2026-11-06
**Auslöser:** Daniel — Starttag auf heute. `launchDate` auf 2026-11-06, bauen, ausliefern,
`check_live.py` mit 2823, `datePublished` im gebauten Schema prüfen. Dann `06-launch.md`
angleichen und „Staffel auslösen" als erledigt markieren.

## Änderung

`site.json` `launchDate` von 2026-11-09 auf **2026-11-06** gesetzt (das Schema nutzt den Wert als
`datePublished`).

## Build und Auslieferung

- `npm run build`: 4647 Seiten, Schriftprüfung bestanden.
- Im gebauten Startseiten-Schema: `"datePublished":"2026-11-06"`.
- Ausgeliefert nach Cloudflare Pages.
- Live im ausgelieferten Schema bestätigt: `"datePublished":"2026-11-06"`.
- `check_live.py` mit `--expect-urls 2823`: **alle Prüfungen bestanden**, Sitemap 2823, www-Zeile
  grün.

## 06-launch.md angeglichen

- Kopf: „Start der Staffel **2026-11-06** (ausgelöst)".
- Stellschrauben: `launchDate=2026-11-06`.
- Startsperren: `datePublished`-Punkt auf 2026-11-06, im gebauten und Live-Schema bestätigt; neuer
  Haken **„Staffel ausgelöst am 2026-11-06"**.
- Abschnitt 7: Staffel am **2026-11-06** gestartet, erste **30-Tage-Prüfung am 2026-12-06**.
- Abschnitt 8: Punkt „Staffel auslösen" als **erledigt** markiert; offen beim Betreiber bleibt
  allein der IndexNow-Ping der ersten Stufe im eigenen Cloudflare-Konto.

## Stand

Die Staffel ist mit heutigem Starttag live. Verbleibende Betreiber-Aufgabe: der IndexNow-Ping im
eigenen Cloudflare-Konto. Nächste Prüfung 2026-12-06.
