# Sende-Postfach setzen (Variante A, Subdomain `post`)

**Datum** 2026-11-16 · Freigabe: Variante A aus `berichte/2026-11-16-sende-postfach-plan.md`,
Label **`post`** statt `send`. Absender `daniel@post.die-besten-schluesseldienste.de`,
Anbieter mailbox.org (Tarif Standard, Konto angelegt). **Die Wurzel der Zone bleibt unangetastet.**

Ablauf in zwei Etappen: zuerst nur der Nachweis-TXT (Schritt 1–2), dann nach der „verifiziert"-
Meldung des Betreibers die restlichen Einträge und der Funktionstest (Schritt 3–5). Beide Etappen
sind unten festgehalten; **alle fünf Schritte sind erledigt.**

---

## Schritt 1 — Darf das Token DNS schreiben?

**Ja.** Geprüft, ohne etwas zu umgehen:

- `/user/tokens/verify` meldet `Invalid API Token` (Code 1000) — das ist der bekannte Effekt
  eines **zonen-gebundenen** Tokens, der auf den `/user/*`-Namensraum keinen Zugriff hat, und
  **kein** Zeichen für einen ungültigen Token.
- Der echte Beleg: ein **DNS-Read** der Zone (`GET …/dns_records`) läuft mit `success: true`.
  Der Token wird also erkannt.
- Der **DNS-Write** in Schritt 2 (Anlegen des Nachweis-TXT) wurde mit `success: true`
  angenommen. Damit ist die Schreibberechtigung (DNS:Edit) nachgewiesen — es gibt bei Cloudflare
  keinen Probelauf, der spezifizierte, reversible TXT-Eintrag ist der Test selbst.

Keine fehlende Berechtigung; nichts wurde umgangen.

## Wurzel der Zone — Zustand **vorher** (und unverändert)

Diese Einträge bleiben bei allen folgenden Schritten unberührt:

| Typ | Name | Prio | Inhalt (gekürzt) |
|---|---|---|---|
| CNAME | `die-besten-schluesseldienste.de` | – | `schluesseldienste-deutschland.pages.dev` (proxied) |
| CNAME | `www` | – | `schluesseldienste-deutschland.pages.dev` (proxied) |
| MX | `die-besten-schluesseldienste.de` | 94 | `route1.mx.cloudflare.net` |
| MX | `die-besten-schluesseldienste.de` | 50 | `route3.mx.cloudflare.net` |
| MX | `die-besten-schluesseldienste.de` | 100 | `route2.mx.cloudflare.net` |
| TXT (SPF) | `die-besten-schluesseldienste.de` | – | `v=spf1 include:_spf.mx.cloudflare.net ~all` |
| TXT (DKIM) | `cf2024-1._domainkey` | – | `v=DKIM1; … p=…` (Cloudflare Email Routing) |
| TXT | `die-besten-schluesseldienste.de` | – | `ahrefs-site-verification_…` |

Kein `_dmarc` auf der Wurzel vorhanden — bestätigt den im Plan beschriebenen Weg (Worker-Versand
über das Email-Routing-gekoppelte Legacy-Sending, abhängig von den Wurzel-MX). Unter `post.` lag
vorher **nichts**.

## Schritt 2 — Nachweis-TXT gesetzt (DNS-only, TTL Auto)

```
Typ:  TXT
Name: 378adbc96caa4222432e51447fec7706b0c5cdd1.post.die-besten-schluesseldienste.de
Wert: 461552dcccfe01279e8352fe06e17edd8c339b92
TTL:  Auto    proxied: nein (graue Wolke)
```

Angelegt, `success: true`. **Von außen geprüft**, löst auf beiden öffentlichen Resolvern auf:

- `@1.1.1.1` → `"461552dcccfe01279e8352fe06e17edd8c339b92"`
- `@8.8.8.8` → `"461552dcccfe01279e8352fe06e17edd8c339b92"`

Danach hat der Betreiber bei mailbox.org auf „Prüfen" geklickt und **„verifiziert"** gemeldet —
daraufhin Schritt 3.

---

## Schritt 3 — MX, SPF, DKIM, DMARC für `post.` gesetzt (nach „verifiziert")

Prioritäten und DKIM-Ziele vorher gegen die mailbox.org-Doku geprüft
(kb.mailbox.org/en/private/custom-domains/spf-dkim-and-dmarc/): vier MX je **Prio 10**
(Cloudflare erlaubt gleiche Prioritäten; 10/20/30/40 nur, wenn ein Provider Duplikate ablehnt),
vier DKIM-CNAMEs, SPF `include:mailbox.org`, DMARC mit Pflicht-`p=none`. Alle Einträge **DNS-only
(grau)**, TTL Auto. Jeweils `success: true`:

1. **MX** `post` → `mxext1.mailbox.org` (Prio 10)
2. **MX** `post` → `mxext2.mailbox.org` (Prio 10)
3. **MX** `post` → `mxext3.mailbox.org` (Prio 10)
4. **MX** `post` → `mxext4.mailbox.org` (Prio 10)
5. **TXT (SPF)** `post` → `v=spf1 include:mailbox.org ~all`
6. **CNAME** `MBO0001._domainkey.post` → `MBO0001._domainkey.mailbox.org`
7. **CNAME** `MBO0002._domainkey.post` → `MBO0002._domainkey.mailbox.org`
8. **CNAME** `MBO0003._domainkey.post` → `MBO0003._domainkey.mailbox.org`
9. **CNAME** `MBO0004._domainkey.post` → `MBO0004._domainkey.mailbox.org`
10. **TXT (DMARC)** `_dmarc.post` → `v=DMARC1; p=none; rua=mailto:dmarc@post.die-besten-schluesseldienste.de`

Cloudflare schreibt die CNAME-Hostnamen klein (`mbo0001…`); DNS ist Groß-/Kleinschreibungs-
unabhängig, der DKIM-Selektor wird davon nicht berührt.

## Schritt 4 — dig-Kontrolle von außen (1.1.1.1 und 8.8.8.8)

**`post.`-Einträge — alle aufgelöst (auf beiden Resolvern identisch):**

| Abfrage | Antwort |
|---|---|
| `MX post` | `10 mxext1` · `10 mxext2` · `10 mxext3` · `10 mxext4 .mailbox.org` |
| `TXT post` | `"v=spf1 include:mailbox.org ~all"` |
| `TXT _dmarc.post` | `"v=DMARC1; p=none; rua=mailto:dmarc@post.die-besten-schluesseldienste.de"` |
| `CNAME MBO0001–0004._domainkey.post` | → `mbo000N._domainkey.mailbox.org`, folgt weiter zum echten DKIM-Schlüssel (2× RSA, 2× ed25519) |

**Wurzel der Zone — Vorher = Nachher (unverändert):**

| Typ | Name | Vorher | Nachher |
|---|---|---|---|
| MX | `@` | `route1(94)`, `route3(50)`, `route2(100)` .mx.cloudflare.net | **gleich** |
| TXT (SPF) | `@` | `v=spf1 include:_spf.mx.cloudflare.net ~all` | **gleich** |
| TXT (DKIM) | `cf2024-1._domainkey` | `v=DKIM1; … p=…` | **gleich** |
| TXT | `@` | `ahrefs-site-verification_…` | **gleich** |
| TXT | `_dmarc` (Wurzel) | — (nicht vorhanden) | — (weiter nicht vorhanden) |

Es wurde nur unterhalb von `post.` (und `_dmarc.post`) angelegt; an der Wurzel nichts.

## Schritt 5 — Test der Formular-Benachrichtigung (kommt noch an)

Wie bei der Ersteinrichtung: echte Absendung an die Produktion `POST …/api/claim`, währenddessen
`wrangler tail` auf dem Benachrichtigungs-Worker `schluesseldienste-claim-notify`.

- Function-Antwort: **HTTP 303 → `/eintrag-beanspruchen/?gesendet=1`** (Annahme-Pfad).
- Worker-Tail (der maßgebliche Beweis, weil der 303 unabhängig vom Hintergrund-Versand feuert):
  `POST https://mailer.internal/send - Ok` und `(log) notify: EMAIL.send ok`.

Das `send_email`-Binding hat die Nachricht also angenommen und Cloudflare Email Routing zur
Zustellung übernommen — **genau wie bei der Ersteinrichtung**. Der Versandweg des Formulars ist
nach dem Setzen der `post.`-Subdomain unverändert intakt (die Wurzel-MX und Email Routing, von
denen er abhängt, sind unberührt). Die letzte Ankunft im Posteingang bestätigt der Betreiber wie
beim ersten Mal.

*Aufräumen:* Der Testlauf erzeugte Probe-Einsendungen in KV (Marker „TEST post-Subdomain …
bitte ignorieren"); sie werden wieder gelöscht und laufen andernfalls über die 90-Tage-TTL von
selbst ab. Absender war die Verzeichnis-Domain, Empfänger das `NOTIFY_TO`-Postfach — keine
Betriebsadresse, keine Schlüsseldienst-Domain beteiligt.

## Ergebnis

- **Alle Schritte 1–5 erledigt.** Variante A auf der Subdomain `post.` steht: Nachweis +
  MX/SPF/DKIM/DMARC, von außen aufgelöst. Die Wurzel (info@-Routing und Worker-Versand) ist
  nachweislich unberührt, die Formular-Benachrichtigung kommt weiter durch.
- **Noch beim Betreiber:** in der mailbox Suite das Postfach `daniel@post.…` endgültig anlegen/
  freischalten und in LeadHawk IMAP/SMTP von mailbox.org hinterlegen (Schritt 6 des Plans). Das
  liegt außerhalb der DNS-Arbeit.
- **Hinweis zur Umgebung:** Die Festplatte war zu Beginn zu 100 % voll (0 Byte frei). Für Bericht
  und Commit wurde nur der regenerierbare npm-Download-Cache (`~/.npm/_cacache`) geleert; am
  Projekt oder an den Daten wurde nichts entfernt. (Die größere Aufräumung folgt getrennt.)
