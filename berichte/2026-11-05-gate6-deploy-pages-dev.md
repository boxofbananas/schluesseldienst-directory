---
title: Gate 6, Teil 1 – Deploy auf Cloudflare Pages (pages.dev)
type: bericht
status: fertig
updated: 2026-11-05
---

# Gate 6, erster Teil: ausgeliefert auf pages.dev

## Adresse
**https://schluesseldienste-deutschland.pages.dev/**
(Produktionszweig `main`; letzter Build-Deploy `a0eef6bb.schluesseldienste-deutschland.pages.dev`.)

Noch **nicht** gemacht (wie gewünscht): eigene Domain verbinden, Sitemap einreichen, bei
Suchmaschinen anmelden.

## Konto / Token
`npx wrangler whoami` zeigt das Konto **Domholdinggmbh@gmail.com's Account** — kein Rechte- oder
Anmeldefehler, die IP-Beschränkung greift also nicht. Vor jedem Aufruf `NODE_OPTIONS=
--dns-result-order=ipv4first` gesetzt (IPv4). Der Token wurde nie ausgegeben. (Zwei technische
Randnotizen: die Token-Datei hat CRLF-Zeilenenden, daher den Token-Wert beim Einlesen von Leerzeichen
befreit; `CLOUDFLARE_ACCOUNT_ID` wird nicht gesetzt — der Token ist auf genau ein Konto beschränkt,
wrangler wählt es selbst.)

## Ablauf
1. `whoami` – Konto bestätigt.
2. Frischer `npm run build` – 4.654 Dateien, Schriftprüfung bestanden.
3. Pages-Projekt `schluesseldienste-deutschland` angelegt (einmalig, Produktionszweig `main`).
4. `dist` ausgeliefert (4.652 Dateien).
5. KV-Namespace `EINSENDUNGEN` angelegt und gebunden (siehe unten).
6. `check_live.py` gegen pages.dev – alles bestanden.

**Zur `wrangler.toml`:** Sie trug eine Platzhalter-KV-ID und ein `send_email`-Binding. Für den
ersten, reinen Static-Deploy habe ich sie kurz beiseitegelegt und mit expliziten Flags ausgeliefert,
danach wiederhergestellt und die echte KV-ID eingetragen.

## KV-Binding: geht über wrangler — erledigt
- KV-Namespace `EINSENDUNGEN` angelegt, ID `31cfe34f7c08485c8708c642f0fc7781`, in `wrangler.toml`
  eingetragen (ersetzt den Platzhalter).
- **Die Bindung geht über wrangler** (`[[kv_namespaces]]` in `wrangler.toml` + `pages deploy`); beim
  Redeploy angewandt, **kein Dashboard nötig**. Daniel muss für KV nichts klicken.

## `send_email`: NICHT über die Pages-Konfig — Dashboard (erst für den Mail-Worker)
Der erste Redeploy mit vollständiger `wrangler.toml` scheiterte mit:
*„Configuration file for Pages projects does not support 'send_email'".* Pages unterstützt
`send_email` also **gar nicht** in der Konfigurationsdatei. Ich habe den Block deshalb in
`wrangler.toml` auskommentiert (sonst scheitert jeder Deploy) und mit nur dem KV-Binding ausgeliefert.
- `send_email` wird **erst für den Mail-Worker nach dem Start** gebraucht, **nicht für Gate 6**. Dann
  muss es im Dashboard gesetzt werden (Pages-Projekt → Settings → Functions → Bindings), und die
  Zieladresse muss vorher in **Email Routing** als „Destination address" verifiziert sein.
- **Offen zu prüfen beim Worker-Schritt:** ob das Pages-Dashboard überhaupt einen
  `send_email`/Email-Binding-Typ anbietet. Falls nicht, läuft der Mail-/Formular-Handler nicht als
  Pages Function, sondern muss ein eigenständiger Worker werden. Das klären wir, wenn der Worker dran
  ist. Die statische Seite und das Verzeichnis sind davon unberührt.

Hinweis: Das Beanspruchungs-Formular (`/api/claim`) braucht KV **und** `send_email`. KV ist gebunden,
`send_email` fehlt noch, also nimmt das Formular noch keine Einsendungen an. Für „die Seite ansehen"
ist das ohne Belang.

## check_live.py (gegen pages.dev)
**Alle 22 Prüfungen bestanden.** Darunter: Startseite 200/H1/`lang="de"`/canonical auf die echte
Domain, keine Vorschau-Premium-Karten, Impressum und Datenschutz im Fußbereich verlinkt und mit
Inhalt, unbekannte Adresse → 404, `robots.txt` mit Sitemap, Sitemap mit **2.807 Adressen** (schlanker
Start), je eine Eintrags-, Stadt- und Bundesland-Seite indexierbar, `/verzeichnis/` noindex+follow,
`/eintrag-beanspruchen/` und `/premium/` noindex, Datenschutz lädt keine Google-Karte, und: die
pages.dev-Adresse sendet `X-Robots-Tag: noindex`.

## Indexierung auf pages.dev — kein Problem
Geprüft, ob die öffentlich erreichbare pages.dev-Adresse versehentlich indexierbar wäre. **Nein:**
`_headers` setzt `X-Robots-Tag: noindex` für `*.pages.dev` (Produktions- und Versions-Subdomain),
**live bestätigt** per `curl` auf Start-, Unterseite und Versions-Subdomain. `robots.txt` erlaubt zwar
das Crawlen (`Allow: /`) — das ist **richtig so**: nur wenn Crawler die Seite laden dürfen, sehen sie
den noindex-Header; ein `Disallow` würde ihn verstecken. Die Sitemap in `robots.txt` zeigt bereits auf
die echte Domain. Damit entsteht **kein Doppelinhalt**, wenn später die eigene Domain dazukommt.

## Was bei Cloudflare noch von Hand zu tun ist
- **Jetzt nichts Zwingendes** für die pages.dev-Ansicht.
- **Vor dem Index-Start (später, eigener Schritt):** eigene Domain `die-besten-schluesseldienste.de`
  mit dem Pages-Projekt verbinden (du meldest dich bei Cloudflare an), danach Sitemap einreichen und
  die Adressen gestaffelt einreichen.
- **Für den Mail-Worker (nach dem Start):** Email Routing einrichten + `send_email`/„SEB" binden
  (Dashboard), siehe oben.

Nächster Schritt liegt bei dir: die Seite unter der pages.dev-Adresse ansehen.
