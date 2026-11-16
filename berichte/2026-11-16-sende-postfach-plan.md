# Sende-Postfach für die Outreach-Mails — Prüfung und Plan

**Datum** 2026-11-16 · **Nur Prüfung und Planung — nichts gesetzt, nichts angelegt, nichts
ausgeliefert.** DNS nur gelesen (Cloudflare-API, Token nur mit DNS-Leserecht). Keine
Schlüsseldienst-Domain kommt als Absender oder Empfänger vor. Das Cloudflare-Token steht nirgends
in diesem Bericht.

## Ziel

- Outreach-Mails gehen von einer persönlichen Adresse auf `die-besten-schluesseldienste.de`
  (Verzeichnis-Domain, kein Schlüsseldienst-Betrieb), versendet über LeadHawk.
- Antworten landen in genau dem Postfach, das LeadHawk per IMAP liest.
- **Was heute läuft, muss weiterlaufen:** (a) `info@` → Gmail über Cloudflare Email Routing;
  (b) Formular-Benachrichtigungen über den Worker `schluesseldienste-claim-notify`
  (`send_email`-Binding, Ziel = Pages-Secret `NOTIFY_TO`).

---

## 1. Heutiger DNS-Stand (mail-relevant)

Zone `die-besten-schluesseldienste.de` (Zone-ID `36844d2e…`), gelesen über
`GET /zones/{id}/dns_records`. Die Email-Routing-Endpunkte lieferten einen Scope-Fehler
(„Authentication error") — das Token darf nur DNS lesen. Der aktive Email-Routing-Betrieb lässt
sich aber eindeutig aus den DNS-Einträgen ablesen.

| Typ | Name | Inhalt | Prio |
|---|---|---|---|
| MX | `die-besten-schluesseldienste.de` | `route1.mx.cloudflare.net` | 94 |
| MX | `die-besten-schluesseldienste.de` | `route2.mx.cloudflare.net` | 100 |
| MX | `die-besten-schluesseldienste.de` | `route3.mx.cloudflare.net` | 50 |
| TXT (SPF) | `die-besten-schluesseldienste.de` | `v=spf1 include:_spf.mx.cloudflare.net ~all` | — |
| TXT (DKIM) | `cf2024-1._domainkey…` | `v=DKIM1; h=sha256; k=rsa; p=…` (Cloudflare) | — |
| TXT | `die-besten-schluesseldienste.de` | `ahrefs-site-verification_…` (nicht mail) | — |
| CNAME | `@` und `www` | `schluesseldienste-deutschland.pages.dev` | — |

**Befunde:**
- MX, SPF und DKIM gehören alle zu **Cloudflare Email Routing** (Empfang/Weiterleitung). Das ist
  die Grundlage von `info@` → Gmail.
- **Kein DMARC-Eintrag** vorhanden (`_dmarc` fehlt).
- **Keine `cf-bounce`-Einträge** vorhanden — also keine Records des neueren Cloudflare-Produkts
  „Email Sending". Daraus folgt: der Worker sendet heute über den **alten** Weg (Versand an eine
  *verifizierte Email-Routing-Zieladresse*), der an ein aktives Email Routing gekoppelt ist — und
  nicht über das separate „Email Sending" mit eigenen `cf-bounce`-Records. Das ist für den Plan
  entscheidend (siehe Punkt 2 und der Konflikt unten).

---

## 2. Was das `send_email`-Binding zwingend braucht

Quellen (Cloudflare, abgerufen 2026-11-16):
- Domain-Konfiguration: <https://developers.cloudflare.com/email-service/configuration/domains/>
- Send-Bindings: <https://developers.cloudflare.com/email-service/configuration/send-bindings/>
- Workers-API: <https://developers.cloudflare.com/email-service/api/send-emails/workers-api/>

**Laut Dokumentation** (Produkt heißt inzwischen „Email Service", es vereint „Email Routing" =
Empfang und „Email Sending" = Versand):
- Versand und Empfang sind **getrennt**: „Email Sending and Email Routing have separate DNS
  records and separate settings pages" und „Email Sending and Email Routing are managed separately.
  Removing one does not affect the other."
- „Email Sending" legt eigene Records auf der **`cf-bounce.`-Subdomain** an (MX, SPF, DKIM) plus ein
  `_dmarc` auf der Wurzel; der Wurzel-MX gehört nur zum **Empfang** (Routing).
- Der Absender muss zu einer für den Versand **onboardeten/verifizierten** Domain gehören
  (`E_SENDER_DOMAIN_NOT_AVAILABLE` = „Domain not onboarded", `E_SENDER_NOT_VERIFIED`). Der
  Standard-Binding darf an **jede verifizierte Zieladresse** senden; mit `allowed_destination_addresses`
  lässt sich das auf eine Liste einschränken. Grenzen: ≤ 50 Empfänger/Mail, ≤ 25 MiB.

**In diesem Konto konkret:** Es gibt **keine** `cf-bounce`-Records. Der Worker nutzt also den
**legacy-Weg** (Versand an die verifizierte Routing-Zieladresse `NOTIFY_TO`). Dieser Weg **hängt am
aktiven Email Routing** und damit daran, dass der **Wurzel-MX auf Cloudflare** zeigt.

> **Antwort auf die Frage:** Im **heutigen** Zustand ja — Email Routing muss aktiv bleiben und der
> Wurzel-MX muss auf Cloudflare zeigen, sonst steht der Worker-Versand auf der Kippe. Laut Doku
> *ließe* sich der Versand über „Email Sending" (cf-bounce) vom Empfang entkoppeln, aber das ist
> hier nicht eingerichtet und wäre eine Migration. Der empfohlene Plan (Punkt 4) lässt den
> Wurzel-MX in Ruhe, damit sich diese Frage gar nicht stellt.

---

## 3. Was mailbox.org für eine eigene Domain verlangt

Quellen (mailbox.org, abgerufen 2026-11-16):
- Eigene Domain: <https://kb.mailbox.org/en/private/custom-domains/using-emails-with-a-custom-domain>
- SPF/DKIM/DMARC: <https://kb.mailbox.org/en/private/custom-domains/spf-dkim-and-dmarc/>

- **Empfangen** (Antworten sollen im Postfach landen): **MX muss auf mailbox.org zeigen.** Die MX
  sind `mxext1.mailbox.org` … `mxext4.mailbox.org` (alle Priorität 10; falls der Anbieter gleiche
  Prioritäten verbietet: 10/20/30/40). „Check whether your DNS records contain MX records that do
  not point to the mailbox servers. Remove these records." Ohne MX auf mailbox.org kommt keine
  eingehende Antwort an — und ohne das kann LeadHawk nichts per IMAP lesen.
- **Nachweis**: ein **TXT-Eintrag** mit einem „mailbox security key" (zweigeteilt: Host = erster
  Teil, Ziel = zweiter Teil), erzeugt beim Anlegen der Adresse als „external alias" in der mailbox
  Suite. Sync bis zu 48 h.
- **Nur senden**: Die Doku sagt dazu nichts Belastbares. Technisch genügt zum **Senden** über die
  mailbox-SMTP die Alias-Einrichtung + SPF/DKIM; **Empfangen** verlangt aber MX. Da hier Antworten
  ankommen **müssen**, ist der Fall „nur senden" für uns ohnehin nicht einschlägig — MX auf
  mailbox.org ist für das Sende-/Antwort-Postfach nötig.
- **SPF**: genau **ein** TXT `v=spf1 include:mailbox.org ~all` („Multiple SPF entries are not
  allowed!").
- **DKIM**: vier **CNAMEs** `MBO0001…MBO0004._domainkey.<domain>` → `MBO000N._domainkey.mailbox.org`.
- **DMARC**: TXT `_dmarc.<domain>` = `v=DMARC1; p=none; rua=mailto:…` (mit p=none beginnen).
- **Reihenfolge**: Key holen (Alias anlegen) → TXT-Nachweis → Alias/Adresse in mailbox speichern →
  **erst dann** MX umstellen.

---

## Der Konflikt (und warum es einen gibt)

Der **Wurzel-MX kann nur auf einen Anbieter zeigen.**
- Cloudflare Email Routing (und damit `info@` → Gmail **und** der heutige Worker-Versand) braucht
  den **Wurzel-MX auf Cloudflare**. „Cannot use Email Routing with external mail servers."
- mailbox.org-Empfang (für die Antworten) braucht **MX auf mailbox.org** — für die Domain bzw.
  Subdomain, die das Sende-Postfach trägt.

Beides auf der **nackten Wurzel** geht nicht gleichzeitig. Die Lösung ist, das Sende-/Antwort-
Postfach auf eine **Subdomain** zu legen, deren MX getrennt auf mailbox.org zeigt, während die
Wurzel bei Cloudflare bleibt.

---

## 4. Vorschlag

### Variante A — Subdomain bei mailbox.org  ·  **empfohlen**

Sende-Adresse z. B. **`vorname@send.die-besten-schluesseldienste.de`** (Label `send`, `post` oder
`mail` frei wählbar). Die **Wurzel bleibt komplett unverändert** bei Cloudflare.

- `info@` → Gmail (Email Routing): **läuft weiter**, unangetastet.
- Worker `schluesseldienste-claim-notify` (`send_email` → `NOTIFY_TO`): **läuft weiter**, weil der
  Wurzel-MX und Email Routing bleiben.
- Antworten an `…@send.…` landen bei mailbox.org (Subdomain-MX), LeadHawk liest sie per IMAP.
- **Bonus:** eine getrennte Sende-Subdomain schützt den Ruf der Haupt-/Markendomain — für
  Kalt-Outreach ohnehin die saubere Praxis.
- **Kosten:** mailbox.org ~3 €/Monat. **Bruch: keiner.**

### Variante B — nackte Wurzel bei mailbox.org

Sende-Adresse `vorname@die-besten-schluesseldienste.de`. Dafür müsste der **Wurzel-MX** von
Cloudflare auf mailbox.org wechseln. Folgen:
- **Email Routing bricht** → `info@` → Gmail muss als **mailbox.org-Alias/Weiterleitung**
  neu gebaut werden (geht, aber Handarbeit).
- **Worker-Versand bricht sehr wahrscheinlich** → der heutige legacy-Weg hängt an Email Routing.
  Rettung nur über eine **Migration** auf Cloudflare „Email Sending" (Domain onboarden,
  `cf-bounce`-Records setzen) **oder** Umbau des Workers auf einen anderen Versandweg. Das ist
  echte Arbeit und ein Ausfallrisiko für die Formular-Benachrichtigungen.
- **Kosten:** mailbox.org ~3 €/Monat **plus** Migrationsaufwand und Risiko.

**Empfehlung: Variante A.** Sie erfüllt alle Ziele, bricht nichts und spart die Worker-Migration.
Der einzige „Preis" ist die Subdomain im Absender — bei Outreach ein Vorteil, kein Nachteil.

**Anbieter:** mailbox.org passt (eigene Domain, IMAP/SMTP, ~3 €/Monat) und bleibt die Empfehlung.
Gleichwertige Alternativen wären Fastmail oder Migadu (Migadu rechnet pauschal je Domain, angenehm
für Subdomains) — aber kein Grund zu wechseln; die Entscheidung ist **Subdomain statt Wurzel**,
nicht der Anbieter.

---

## 5. Die genauen DNS-Einträge (Variante A) — **noch NICHT setzen**

Für die Subdomain `send.die-besten-schluesseldienste.de`. In Cloudflare den Host **ohne**
Zonen-Suffix eintragen (Cloudflare hängt die Zone an; ein bekannter Fallstrick ist, dass Cloudflare
den Domainteil sonst abschneidet). **Alle Einträge DNS-only (graue Wolke), nicht proxied.**

1. **Nachweis (TXT)** — Wert wird beim Anlegen der Adresse in der mailbox Suite erzeugt (security
   key, zweigeteilt). Name = erster Key-Teil (relativ zur Subdomain, wie mailbox ihn zeigt),
   Inhalt = zweiter Key-Teil. *Platzhalter, echten Wert bei der Einrichtung einsetzen.*
2. **MX** `send` → `mxext1.mailbox.org` (Prio 10)
3. **MX** `send` → `mxext2.mailbox.org` (Prio 10)
4. **MX** `send` → `mxext3.mailbox.org` (Prio 10)
5. **MX** `send` → `mxext4.mailbox.org` (Prio 10)
6. **TXT (SPF)** `send` → `v=spf1 include:mailbox.org ~all`
   *(nur falls LeadHawk über eigene Relay-IPs sendet statt über die mailbox-SMTP: dessen
   SPF-include **vor** `~all` ergänzen — siehe Punkt 6, Schritt LeadHawk.)*
7. **CNAME** `MBO0001._domainkey.send` → `MBO0001._domainkey.mailbox.org`
8. **CNAME** `MBO0002._domainkey.send` → `MBO0002._domainkey.mailbox.org`
9. **CNAME** `MBO0003._domainkey.send` → `MBO0003._domainkey.mailbox.org`
10. **CNAME** `MBO0004._domainkey.send` → `MBO0004._domainkey.mailbox.org`
11. **TXT (DMARC)** `_dmarc.send` → `v=DMARC1; p=none; rua=mailto:dmarc@send.die-besten-schluesseldienste.de`
    *(Berichtsadresse liegt bewusst **auf derselben Subdomain** und wird dort als Alias empfangen —
    so ist kein externer DMARC-Autorisierungs-Eintrag nötig. p=none zum Mitlesen, später
    verschärfbar.)*

**Wurzel-Einträge bleiben unverändert** (MX→Cloudflare, SPF `_spf.mx.cloudflare.net`, Cloudflare-
DKIM). Nichts davon wird angefasst.

---

## 6. Was du selbst klickst

### Bei mailbox.org
1. Konto/Tarif anlegen bzw. einloggen: <https://login.mailbox.org> (Tarif ab ~3 €/Monat, eigene
   Domain inklusive).
2. In der mailbox Suite: Zahnrad (oben rechts) → **All settings** → **Email addresses** →
   **Email aliases** → **Add external alias**. Adresse `vorname@send.die-besten-schluesseldienste.de`
   eingeben → **Save**. mailbox zeigt den **security key** (zweigeteilt) für den TXT-Nachweis.
3. Den TXT-Nachweis (Schritt 1 der DNS-Liste) in Cloudflare DNS setzen; bis zu 48 h Sync abwarten,
   bis mailbox die Domain als verifiziert führt.
4. Das eigentliche Postfach/die Adresse in mailbox anlegen **bevor** du die MX umstellst (sonst
   „User unknown").
5. Danach die MX (Schritte 2–5), SPF (6), DKIM-CNAMEs (7–10) und DMARC (11) in Cloudflare setzen —
   **erst nach deiner Freigabe.**
6. Prüfen: `nslookup -type=MX send.die-besten-schluesseldienste.de` und `-type=TXT` für SPF/DMARC;
   eine Testmail an die Adresse schicken und im mailbox-Posteingang ankommen sehen.

### In LeadHawk
7. Postfach verbinden: **IMAP + SMTP** auf mailbox.org:
   - IMAP `imap.mailbox.org`, Port **993** (SSL) — damit liest LeadHawk die **Antworten**.
   - SMTP `smtp.mailbox.org`, Port **465** (SSL) oder **587** (STARTTLS) — damit **sendet** LeadHawk.
   - Benutzer = die volle Adresse, Passwort = mailbox-Passwort (bei aktiver 2FA ein App-Passwort in
     mailbox anlegen).
8. In LeadHawk prüfen/entscheiden, **wie** LeadHawk sendet:
   - Sendet LeadHawk **über die verbundene mailbox-SMTP** (der Normalfall bei „bring your own
     mailbox"), ist SPF `include:mailbox.org` ausreichend — nichts weiter.
   - Sendet LeadHawk über **eigene Relay-IPs**, nennt LeadHawk dafür einen **SPF-include**; den dann
     in Schritt 6 der DNS-Liste vor `~all` ergänzen. (In der LeadHawk-Doku/Einstellungen prüfen.)
9. Als Absenderadresse in der Kampagne `vorname@send.die-besten-schluesseldienste.de` setzen,
   Antwort-Adresse identisch, damit Antworten ins IMAP-Postfach zurücklaufen.
10. Eine Testkampagne an eine eigene Zweitadresse senden, antworten, und in LeadHawk die
    **Antworterkennung** prüfen.

---

## Quellen

- Cloudflare Email Service — Domains: <https://developers.cloudflare.com/email-service/configuration/domains/>
- Cloudflare Email Service — Send bindings: <https://developers.cloudflare.com/email-service/configuration/send-bindings/>
- Cloudflare Email Service — Workers API: <https://developers.cloudflare.com/email-service/api/send-emails/workers-api/>
- mailbox.org — eigene Domain: <https://kb.mailbox.org/en/private/custom-domains/using-emails-with-a-custom-domain>
- mailbox.org — SPF/DKIM/DMARC: <https://kb.mailbox.org/en/private/custom-domains/spf-dkim-and-dmarc/>

## Was bricht / offene Punkte

- **Bei Variante A bricht nichts.** `info@`→Gmail und der Worker-Versand bleiben unberührt, weil der
  Wurzel-MX bei Cloudflare bleibt.
- **Nur bei Variante B** brächen `info@`-Weiterleitung und Worker-Versand (Letzterer bräuchte eine
  Migration auf „Email Sending"/cf-bounce oder einen anderen Versandweg).
- **Offen, vor dem Setzen zu klären:** (1) Label der Subdomain (`send`/`post`/`mail`); (2) ob
  LeadHawk über die mailbox-SMTP oder eigene Relay-IPs sendet (entscheidet, ob ein zweiter
  SPF-include nötig ist); (3) der DKIM-Weg bei mailbox.org ist CNAME auf feste `MBO0001–4`-Schlüssel
  — kein per-Domain-Schlüssel.
- **Token:** nur DNS-Leserecht; Email-Routing-Status wurde aus den DNS-Einträgen abgeleitet, nicht
  aus dem Routing-Endpunkt.
- Es wurde **nichts** gesetzt, angelegt oder ausgeliefert.
