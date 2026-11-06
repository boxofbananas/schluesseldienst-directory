# Benachrichtigung bei Formulareingang

**Datum:** 2026-11-06
**Auslöser:** Daniel — `functions/api/claim.ts` schreibt heute nur in KV; er erfährt nicht, dass
jemand sich gemeldet hat. Kommt eine Beanspruchung oder ein Garantie-Antrag herein, soll er
innerhalb einer Minute eine E-Mail mit dem Inhalt der Einsendung bekommen.

## Weg (vorab in drei Zeilen genannt)

Nicht der volle Blueprint-Mail-Worker (Eingangspost + Claude-Einordnung + Prüfseite, Overkill für
eine reine Benachrichtigung) und **kein Drittanbieter**. Stattdessen ein winziger
**Cloudflare-Worker mit `send_email`-Binding** (`notify-worker/`), den die bestehende
Pages-Function über ein **Service-Binding `MAILER`** aufruft. Kosten **0 €** (Email Routing und
`send_email` im kostenlosen Workers-Kontingent), **kein API-Schlüssel, nichts im Repo**.

Dieser Weg deckt sich mit der bereits veröffentlichten Datenschutzerklärung (Ziffer 5:
Zustellung „über Cloudflare Email Routing an eine von uns verifizierte Adresse und damit ohne einen
weiteren Dienstleister"). Ein Drittanbieter wie Resend hätte dieser Aussage widersprochen und einen
neuen Verarbeiter nötig gemacht — deshalb der Cloudflare-native Weg.

## Was gebaut und ausgeliefert wurde

- **`notify-worker/`**: `src/index.ts` nimmt per Service-Binding `{from, to, raw}` entgegen und
  sendet über `EmailMessage(from, to, raw)` (aktuelle Cloudflare-`send_email`-API, nicht die
  MailChannels-Objekt-API der alten Vorlage). Kein öffentliches Ziel (`workers_dev: false`, keine
  Route) — nur über das Binding erreichbar. Ausgeliefert, Version `a5f83629…`.
- **`functions/api/claim.ts`**: Der frühere, auf Pages wirkungslose `SEB`-`send_email`-Block ist
  ersetzt. Ablauf jetzt: KV-Schreiben **zuerst** (schlägt es fehl, 500, keine Mail); danach, wenn
  `MAILER` und `NOTIFY_TO` vorhanden, Roh-MIME bauen und über `waitUntil(env.MAILER.fetch(...))`
  **im Hintergrund** senden. Der Versand verzögert und blockiert die Antwort nicht; Fehler werden
  geschluckt. Die Function antwortet **immer** mit 303 → `?gesendet=1`.
- **`site/wrangler.toml`**: Service-Binding `[[services]] MAILER → schluesseldienste-claim-notify`
  (an der Produktion per API bestätigt), `NOTIFY_FROM` als Variable. `NOTIFY_TO` bewusst **nicht**
  als Variable (eine Config-Variable überschriebe bei jedem Deploy den Wert) — sondern als Secret.

## Harte Vorgaben eingehalten

- **Kein Zugang im Repo.** Der Weg braucht gar keinen API-Schlüssel. `NOTIFY_TO` (Daniels Adresse)
  ist ein Pages-**Secret**, kein Repo-Eintrag; es überdauert Deploys.
- **Absender/Empfänger nie über eine Schlüsseldienst-Domain.** Absender
  `formular@die-besten-schluesseldienste.de` (Verzeichnis-Domain), Empfänger Daniels gewöhnliche
  Adresse (Secret, zugleich verifizierte Email-Routing-Destination).
- **KV zuerst, Versand darf nicht blockieren.** KV-Schreiben vor dem Versand; scheitert der
  Versand, bleibt die Einsendung in KV und das Formular zeigt trotzdem „gesendet".

## Live-Prüfung über das echte Formular

Echte POST an `https://die-besten-schluesseldienste.de/api/claim` (Formular „Eintrag
beanspruchen", Testmarker im Firmennamen):

- **Formular abgeschickt:** HTTP **303**, kein 500.
- **Weiterleitung korrekt:** `location: /eintrag-beanspruchen/?gesendet=1`.
- **Eintrag in KV:** `beansprucht:2026-11-06T11-00-52:s2c8` mit allen Feldern (remote in KV
  gelesen und bestätigt; Test-Eintrag danach wieder gelöscht).

## Noch offen beim Betreiber (von mir nicht ausführbar — Konto/Postfach)

Die Mail fließt erst nach drei einmaligen Schritten in Daniels Konto; sie brauchen seinen
Postfach-Bestätigungsklick und Email-Routing-Rechte, die das vorhandene Token nicht hat:

1. **Email Routing** auf `die-besten-schluesseldienste.de` aktivieren.
2. Seine **gewöhnliche Adresse** als Destination hinzufügen und per Mail **bestätigen**.
3. `npx wrangler pages secret put NOTIFY_TO --project-name=schluesseldienste-deutschland`
   (= dieselbe Adresse).

**Mail angekommen:** steht noch aus, bis diese drei Schritte erledigt sind — ich bestätige es
unmittelbar danach mit einer erneuten echten Absendung. Alles Übrige (Function, Worker,
Service-Binding, KV-Weg) ist gebaut, ausgeliefert und live geprüft.

## Datenschutz

Keine Änderung nötig: Ziffer 5 beschreibt KV-Ablage (90-Tage-Löschung) und Zustellung per
Cloudflare Email Routing an eine verifizierte Adresse ohne weiteren Dienstleister bereits genau so.
