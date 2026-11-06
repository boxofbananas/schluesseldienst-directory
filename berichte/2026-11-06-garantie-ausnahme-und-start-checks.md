# Garantie-Ausnahme mit Inhaltsschranke, Startdatum, Einwilligungs-Check

**Datum:** 2026-11-06
**Auslöser:** Daniel — die `geprueft`-Ausnahme umsetzen, aber erst nach einer Inhaltsprüfung der 18
Garantie-Seiten; leere Seiten aus der Ausnahme nehmen. Dazu zwei offene Prüflistenpunkte:
`datePublished` auf den Staffel-Starttag 2026-11-09, und der Karten-Einwilligungs-Check.

## Inhaltsprüfung der 18 Garantie-Betriebe

Gemessen je Eintragsseite: Länge der Beschreibung (`description_enriched`) und Zahl der belegten
Merkmale (`true`).

**9 Seiten sind praktisch leer** (0 Wörter, 0 Merkmale — nur Stammdaten und Garantie-Block):

| Betrieb | Ort |
|---|---|
| AES Schlüsseldienst Mannheim | Mannheim |
| I-S-E Schlüsseldienst | Hockenheim |
| Mein Schlüsseldienst Weinheim | Weinheim |
| Merz Schlüsseldienst Ludwigshafen | Ludwigshafen |
| Merz Schlüsseldienst Speyer | Speyer |
| Merz Schlüsseldienst Worms | Worms |
| Rheinpfalz Schlüsseldienst Frankenthal | Frankenthal (Pfalz) |
| Riegelklar Schlüsseldienst Schwetzingen | Schwetzingen |
| Sperber Schlüsseldienst | Heidelberg |

**9 Seiten tragen Inhalt** (120–134 Wörter, 7–14 Merkmale): Merz Sicherheit Mannheim (355 Bew.),
Heidelberg Schlüsseldienst, Mein Schlüsseldienst Hockenheim, Kraichgau Sinsheim, Pälzer Neustadt,
Hardt Waghäusel, Südpfalz Landau, Odenwald Bensheim, Kurpfalz Wiesloch.

Die 9 leeren gehören trotz `geprueft` nicht in die erste Stufe — dort misst `thin` das Richtige.

## Die Codeänderung (Build + Template)

`load.mjs`, `noindexPaths`-Schleife: eine geprüfte Seite wird nur dann aus der `thin`-Sperre
genommen, wenn sie eine Beschreibung trägt.

```
for (const l of listings) if (l.thin && !l.claimed && !l.optimized && !(l.geprueft && l.description)) noindexPaths.add(l.path);
```

Gespiegelt nach `templates/astro/src/lib/load.mjs`.

## Sitemap vorher / nachher

- **Vorher:** 2806 Adressen, 17 der 18 Garantie-Seiten auf `noindex`.
- **Nachher:** **2814** Adressen (+8; Merz Sicherheit Mannheim war schon drin). **9 Garantie-Seiten
  indexiert**, **9 leere bleiben `noindex`**.

**Live bestätigt** (`die-besten-schluesseldienste.de`):
- Sitemap führt 2814 Adressen.
- Kraichgau Sinsheim, Kurpfalz Wiesloch, Südpfalz Landau: `index, follow`, in der Sitemap.
- Sperber Heidelberg, AES Mannheim: `noindex, follow`, nicht in der Sitemap.
- `check_live.py`: alle Prüfungen bestanden (mit `--expect-urls 2814`), www-Zeile grün.

## Startdatum

`site.json` `launchDate` (vom Schema als `datePublished` genutzt) von 2026-11-03 auf **2026-11-09**
gesetzt — der Staffel-Starttag, vor dem die 30-Tage-Prüfung (2026-12-09) liegt. Im gebauten Schema
der Startseite bestätigt (`"datePublished":"2026-11-09"`).

## Einwilligungs-Check (Karten, Schriften) — der letzte rechtliche Haken

Mit leerem Browserprofil (frischer Kontext je Seite, alle Netzanfragen protokolliert):

| Seite | externe Hosts vor Klick | Google vor Klick |
|---|---|---|
| Startseite | **keine** | **keine** |
| Stadtseite Mannheim | **keine** | **keine** |
| Eintragsseite mit Karte (Merz) | **keine** | **keine** |

Auf der Eintragsseite lädt die Karte **erst nach Klick** auf „Karte von Google Maps laden" —
danach erscheinen `www.google.com`, `maps.gstatic.com`, `maps.googleapis.com`. Schriften sind
selbst gehostet (kein externer Font-Host). Ohne Einwilligung geht nichts an Google.

## Stand

Garantie-Ausnahme umgesetzt und ausgeliefert, Sitemap 2814, Startdatum gesetzt, Einwilligung
geprüft. Die Startsperren in `06-launch.md` sind abgehakt. Offen beim Betreiber: IndexNow im
eigenen Cloudflare-Konto aktivieren und die Staffel am 2026-11-09 auslösen. Die 9 leeren
Garantie-Seiten ziehen in die Sitemap nach, sobald sie eine Beschreibung bekommen (Beanspruchung
oder Anreicherung).
