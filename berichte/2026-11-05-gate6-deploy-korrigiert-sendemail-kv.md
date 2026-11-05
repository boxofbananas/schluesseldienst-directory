---
title: Gate 6, Teil 1 (korrigiert) – KV zuerst, send_email recherchiert, Formular-Bug gefixt
type: bericht
status: fertig
updated: 2026-11-05
---

# Gate 6, erster Teil – korrigierter Ablauf

Ergänzt/ersetzt `berichte/2026-11-05-gate6-deploy-pages-dev.md` um die korrigierte Reihenfolge, die
`send_email`-Recherche und einen gefundenen Formular-Bug.

## Adresse
**https://schluesseldienste-deutschland.pages.dev/** (Produktionszweig `main`).
Noch nicht: eigene Domain, Sitemap-Einreichung, Suchmaschinen-Anmeldung.

## Korrigierte Reihenfolge
1. KV-Namespace `EINSENDUNGEN` angelegt (id `31cfe34f7c08485c8708c642f0fc7781`).
2. Echte id in `wrangler.toml` eingetragen (ersetzt `OFFEN_KV_NAMESPACE_ID`).
3. Projekt `schluesseldienste-deutschland` (Zweig `main`) – bestand bereits.
4. Frischer `npm run build` (4.654 Dateien, Schriftprüfung bestanden), `dist` ausgeliefert.
5. `check_live.py` gegen pages.dev – alle Prüfungen bestanden.

whoami ok (Konto Domholdinggmbh, kein IP-/Rechtefehler), vor jedem Aufruf
`NODE_OPTIONS=--dns-result-order=ipv4first`, Token nie ausgegeben.

## send_email: recherchiert — **Pages Functions unterstützen es NICHT**
Nicht angenommen, nachgeschlagen:
- Offizielle Doku „Bindings – Pages Functions" listet genau **12** Binding-Typen (KV, Durable
  Objects, R2, D1, Vectorize, Workers AI, Service, Queues, Hyperdrive, Analytics Engine,
  Umgebungsvariablen, Secrets) und sagt: „Pages Functions only support a subset of all bindings."
  **Kein E-Mail-Binding darunter.**
- `wrangler` bestätigt es direkt: ein Deploy mit `[[send_email]]` scheitert mit *„Configuration file
  for Pages projects does not support 'send_email'."*
- Community-Berichte: das Binding fehlt auch im Dashboard-Dialog „Add binding" von Pages. `send_email`
  ist ein **Workers**-Merkmal.

**Folge (wie von dir vorgegeben):** Binding **herausgenommen** (in `wrangler.toml` auskommentiert),
**ohne** ausgeliefert. Der Deploy scheitert nicht daran. Einsendungen landen in **KV**, Daniel liest
sie im Dashboard — die Startlösung. Benachrichtigung getrennt (siehe unten).

## KV gebunden — über wrangler, zur Laufzeit bestätigt
`[[kv_namespaces]]` in `wrangler.toml` + `pages deploy` bindet das KV; **kein Dashboard nötig**.
Zur Laufzeit geprüft (temporärer Diagnose-Endpunkt, danach entfernt): `env.EINSENDUNGEN` ist
vorhanden (`object`), die Variablen `NOTIFY_FROM`/`NOTIFY_TO` greifen, `env.SEB` ist erwartungsgemäß
nicht gebunden.

## Gefundener Bug im Formular-Handler — gefixt
Beim Live-Test nahm `/api/claim` **keine** Einsendung an: **HTTP 500 (Cloudflare-Fehler 1101**,
unbehandelte Exception) bei **jedem** POST. Ursache per Stacktrace gefunden:
`functions/api/claim.ts`, Funktion `seite()` rief `Response.redirect(pfad + "?gesendet=1", 303)` mit
einem **relativen** Pfad auf — `Response.redirect` verlangt eine **absolute** URL und wirft sonst
*„Unable to parse URL"*. Das brach die Annahme beider Formulare komplett.
- **Fix:** relativer `Location`-Header statt `Response.redirect` — der Browser löst ihn gegen die
  Anfrage auf, kein URL-Parsing. **Live bestätigt:** POST → `HTTP 303, Location:
  /eintrag-beanspruchen/?gesendet=1`.
- Zusätzlich defensiv: `cloudflare:email` nur noch als **Typ** importiert und sonst **dynamisch** nur
  wenn ein `SEB`-Binding vorhanden ist (auf Pages nie) — so hängt die Function nicht an einem Modul,
  das die Pages-Laufzeit nicht bereitstellt.

Das war ein echter Fehler, der die Startlösung („Einsendungen landen in KV") unmöglich machte; ohne
den Fix hätte **kein** Formular funktioniert. (Test-Schlüssel wieder aus KV gelöscht; der
Rate-Limit-Zähler meiner Test-IP läuft binnen einer Stunde von selbst ab.)

## Benachrichtigung – welche Wege es gäbe (getrennt, später)
`send_email` steht auf Pages nicht zur Verfügung. Optionen, wenn Daniel über neue Einsendungen
benachrichtigt werden soll:
1. **Nur KV + Dashboard (jetzt):** keine automatische Mail, Daniel sieht Einsendungen unter
   Workers & Pages → KV → `EINSENDUNGEN`. TTL 90 Tage.
2. **Transaktions-Mail-Dienst per `fetch()`** aus der Pages Function (Resend, Postmark, Mailgun,
   Brevo …), API-Schlüssel als Pages-Secret. Läuft aus Pages heraus, kein eigener Worker nötig.
3. **Eigenständiger Cloudflare Worker** (nicht Pages Function) mit `send_email`-Binding über Email
   Routing — angestoßen von der Pages Function (Service-Binding) oder per Cron, der KV liest.
4. **Cloudflare Email Sending REST API** per `fetch()` (abhängig vom Plan).

**Zur Zieladresse (deine Frage):** Email Routing verschickt nur an eine **verifizierte
Destination**. Verifiziert ist Daniels **eigenes Postfach**, auf das `info@die-besten-
schluesseldienste.de` weitergeleitet wird — **nicht** die `info@`-Adresse selbst. Für Weg 3/4 müsste
deshalb als Ziel Daniels echtes Postfach eingetragen werden (heute steht in `wrangler.toml` als
`NOTIFY_TO` die `info@`-Weiterleitungsadresse; die ist als Routing-Adresse richtig, als
send_email-**Destination** aber nicht verifiziert). Für Weg 2 ist das egal — ein Mail-Dienst sendet an
jede Adresse.

## check_live.py (gegen pages.dev)
**Alle Prüfungen bestanden.** U. a. Startseite 200/H1/`lang="de"`/canonical auf die echte Domain,
keine Vorschau-Premium-Karten, Impressum+Datenschutz im Fuß verlinkt, unbekannte Adresse → 404,
`robots.txt` mit Sitemap, Sitemap mit **2.807 Adressen** (schlanker Start), Eintrags-/Stadt-/
Bundesland-Seite indexierbar, `/verzeichnis/` noindex+follow, `/eintrag-beanspruchen/` und `/premium/`
noindex, Datenschutz ohne Google-Karte, pages.dev sendet `X-Robots-Tag: noindex`.

## Indexierung auf pages.dev — kein Problem
`_headers` setzt `X-Robots-Tag: noindex` für `*.pages.dev` (Produktions- und Versions-Subdomain),
**live per curl bestätigt** auf Start-, Unterseite und Versions-Subdomain. `robots.txt` erlaubt das
Crawlen (`Allow: /`) — richtig so, nur so sehen Crawler den noindex-Header; ein `Disallow` würde ihn
verstecken. Sitemap zeigt auf die echte Domain. Kein Doppelinhalt bei späterem Domain-Anschluss.

## Was Daniel im Cloudflare-Dashboard noch selbst tun muss
- **Jetzt für die pages.dev-Ansicht:** nichts.
- **Einsendungen lesen:** Workers & Pages → `schluesseldienste-deutschland` → KV / „KV namespace
  viewer" → `EINSENDUNGEN` → Schlüssel ansehen (`beansprucht:…`, `garantie:…`).
- **Benachrichtigung (später, eigener Schritt):** einen der Wege 2–4 oben wählen; bei Email Routing
  zuerst die Zieladresse (eigenes Postfach) in Email Routing als Destination verifizieren.
- **Vor dem Index-Start (später):** eigene Domain verbinden, dann Sitemap/Suchmaschinen — bewusst
  noch nicht.

Nächster Schritt bei dir: die Seite unter der pages.dev-Adresse ansehen.
