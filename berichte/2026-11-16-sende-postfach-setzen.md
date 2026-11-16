# Sende-Postfach setzen (Variante A, Subdomain `post`) — Schritt 1–2

**Datum** 2026-11-16 · Freigabe: Variante A aus `berichte/2026-11-16-sende-postfach-plan.md`,
Label **`post`** statt `send`. Absender später `daniel@post.die-besten-schluesseldienste.de`,
Anbieter mailbox.org (Tarif Standard, Konto angelegt). **Die Wurzel der Zone bleibt unangetastet.**

Dieser Bericht hält Schritt 1 und 2 fest. **Schritt 3–5 stehen noch aus** und werden erst
ausgeführt, wenn der Betreiber „verifiziert" meldet (mailbox.org-Prüfung bestanden). Es wurde
bisher **genau ein** DNS-Eintrag gesetzt: der Nachweis-TXT.

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

**→ Jetzt bei mailbox.org erneut auf „Prüfen" klicken.** Sobald mailbox.org die Domain als
verifiziert zeigt und du „verifiziert" meldest, folgt Schritt 3.

---

## Schritt 3 — vorbereitet, **noch NICHT gesetzt**

Erst nach „verifiziert". Für `post.die-besten-schluesseldienste.de`, alle **DNS-only (grau)**,
Host **ohne** Zonen-Suffix eintragen. Werte aus dem Plan, Label `send`→`post`:

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

Prioritäten/Ziele vor dem Setzen gegen die mailbox.org-Doku gegenprüfen. Danach Schritt 4
(dig-Kontrolle aller Einträge + Vorher/Nachher der Wurzel) und Schritt 5 (Test der
Formular-Benachrichtigung).

## Offen

- Warte auf „verifiziert" vom Betreiber (mailbox.org-Prüfung). Dann Schritt 3–5.
- Nichts außer dem Nachweis-TXT wurde gesetzt. Die Wurzel ist unberührt.
- **Hinweis zur Umgebung:** Die Festplatte war zu Beginn zu 100 % voll (0 Byte frei). Für Bericht
  und Commit wurde nur der regenerierbare npm-Download-Cache (`~/.npm/_cacache`) geleert; am
  Projekt oder an den Daten wurde nichts entfernt.
