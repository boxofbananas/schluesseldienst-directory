# Günstigeres Sende-Postfach? Spacemail und lima-city vs. mailbox.org

**Datum** 2026-11-16 · **Nur Prüfung — nichts gekauft, keine DNS-Änderung.** Vergleich für das
Sende-/Antwort-Postfach aus dem Plan vom 2026-11-16 (Variante A, Subdomain
`post.die-besten-schluesseldienste.de`; Domain bleibt bei Namecheap registriert, DNS bei Cloudflare,
**Wurzel der Zone unangetastet**). Keine Schlüsseldienst-Domain als Absender/Empfänger.

## Vergleich

| Kriterium | **Spacemail** (Spaceship) | **lima-city** (Tarif „Mini") | **mailbox.org** (Variante A, Bericht 2026-11-16) |
|---|---|---|---|
| **1. Subdomain mit externer DNS (Cloudflare), Wurzel unberührt** | **Ja** (Third-party-Domain). Nötig: Nachweis-TXT (Wert aus dem Konto) + 2× MX `mx1.spacemail.com`/`mx2.spacemail.com` (Prio 0) + SPF-TXT `v=spf1 include:spf.spacemail.com ~all`. *Subdomain nicht ausdrücklich dokumentiert → im Panel bestätigen.* | **Ja** („externe Domain aufschalten", **keine** NS-Umstellung) — **aber nur mit kostenpflichtigem Webhosting-Tarif**. Nötig: Nachweis-TXT `_lima-verification.post…` = `lima-verification=<Token>` + MX (im Panel; live `mail.lima-city.de` Prio 10). **Offen:** ob eine **reine Mail-Subdomain ohne A-Records auf lima-city** geht → vor Kauf beim Support bestätigen. | **Ja** (external alias). Nötig: Nachweis-TXT (Security-Key, zweiteilig) + 4× MX `mxext1–4.mailbox.org` (Prio 10). |
| **2. IMAP / SMTP** | `mail.spacemail.com` — IMAP **993** (SSL), SMTP **465** (SSL) | `mail.lima-city.de` — IMAP **993** (SSL), SMTP **465** (SSL) | `imap.mailbox.org` **993** (SSL) / `smtp.mailbox.org` **465** (SSL) bzw. 587 (STARTTLS) |
| **3. DKIM mit eigener Domain** | **Ja** — TXT `spacemail._domainkey` (Wert aus dem Konto) | **Ja** — von lima-city erzeugt, in Cloudflare eintragen. SPF: `v=spf1 include:_all-out.lima-city.de ~all` | **Ja** — 4× CNAME `MBO0001–4._domainkey` → `…mailbox.org` |
| **4. Versandgrenze (Bedarf ≤ 20/Tag)** | Bezahlt **500/Stunde** je Postfach (Testphase 20/Std.) → reicht weit | **Nicht dokumentiert**; 20/Tag unkritisch | Im Bericht 2026-11-16 nicht erfasst; regulärer Versand, 20/Tag unkritisch |
| **5. Geschäftliche Einzelmails erlaubt (kein Massenversand)?** | **Strengste der drei.** AUP verbietet „mass unsolicited email" und wertet Nicht-Opt-in als „unsolicited"; Null-Toleranz, pauschalierter Schadenersatz **$500 je Spam-Mail**. Niedrigvolumige Einzel-B2B = Graubereich → **Risiko** | **AGB schweigt** — weder erlaubt noch verboten; nur allgemeine Sperrklausel §5.2 (Netzintegrität) | Im Bericht 2026-11-16 nicht geprüft |
| **6. Preis 1. Jahr / danach (inkl. MwSt falls angegeben)** | ~**$0,98/Monat** jährlich (≈ **$11,76/Jahr** 1. Jahr; Aktionen günstiger), Verlängerung ähnlich/höher. **USD; MwSt für die EU vermutlich zusätzlich** (nicht als inkl. ausgewiesen) | **Mini:** Aktion **1,00 €/Mon.** erste 3 Monate, danach **3,50 €/Mon.** (= 42 €/Jahr laufend); **1. Jahr ≈ 34,50 €**. **inkl. 19 % MwSt.** 1 Domain + 10 GB Mail inkl. | **~3 €/Monat** (≈ 36 €/Jahr), deutscher Anbieter → inkl. MwSt |

*Zu Punkt 1/Subdomain: Bei allen drei Anbietern liegen die Einträge auf der Subdomain; die Wurzel
(Email Routing, Worker-Versand) bleibt unberührt. Spacemail und lima-city dokumentieren den
Subdomain-Fall nicht ausdrücklich — vor dem Kauf im Panel bzw. beim Support bestätigen.*

## Empfehlung

Der **günstigste Kandidat, der die Punkte 1–3 erfüllt, ist Spacemail** (~11–14 €/Jahr inkl. etwaiger
MwSt, gegenüber ~34–42 €/Jahr bei lima-city und ~36 €/Jahr bei mailbox.org). Technisch erfüllt es
1–3 vollständig (Third-party-Domain, IMAP/SMTP, DKIM) und die Versandgrenze locker.

**Zwei Vorbehalte, die vor einer Entscheidung zählen:**
1. **Punkt 5 ist bei Spacemail das Risiko.** Die AUP hat Null-Toleranz gegen unaufgeforderten
   Versand und $500 pauschalierten Schadenersatz je Spam-Mail. Unsere Mails sind einzeln und
   niedrigvolumig (≤ 20/Tag), aber „unsolicited" im Sinne der AUP. Wer den Vertragsrahmen über den
   Preis stellt, fährt mit **lima-city Mini** ruhiger (AGB schweigt zum Versand, deutscher Anbieter,
   inkl. MwSt) — dort ist aber die **Support-Rückfrage zur reinen Mail-Subdomain** (Punkt 1) vor dem
   Kauf nötig.
2. **Subdomain-Nutzung** bei Spacemail vor dem Kauf im Konto bestätigen (nicht ausdrücklich
   dokumentiert).

Kurz: **nach dem gestellten Kriterium (günstigster, der 1–3 erfüllt) → Spacemail.** Als
risikoärmere Alternative bei strengerer Gewichtung von Punkt 5 → lima-city Mini. mailbox.org bleibt
die teuerste, aber am besten belegte Option (Punkte 4/5 dort noch zu prüfen).

## Quellen

Spacemail/Spaceship:
- Third-party-Domain-DNS: <https://www.spaceship.com/knowledgebase/spacemail-dns-records-third-party-domain/>
- DKIM: <https://www.spaceship.com/knowledgebase/setup-dkim-record-spacemail/>
- IMAP/SMTP: <https://www.spaceship.com/knowledgebase/connect-spacemail-to-email-client/>
- Versandgrenzen: <https://www.spaceship.com/knowledgebase/spacemail-email-limits/>
- Preis: <https://www.spaceship.com/business-email/> · AUP/ToS: <https://www.spaceship.com/legal/spacemail/>, <https://www.spaceship.com/en-GB/legal/hosting-aup/>
  *(spaceship.com beantwortet automatische Abrufe mit HTTP 403; Werte aus dem Suchindex der obigen Seiten.)*

lima-city:
- Externe Domain aufschalten: <https://www.lima-city.de/hilfe/wie-kann-ich-die-domain-eines-anderen-anbieters-mit-lima-city-webspace-nutzen>
- E-Mail einrichten (IMAP/SMTP): <https://www.lima-city.de/hilfe/wie-kann-ich-meine-e-mail-adressen-einrichten>
- SPF/Diagnose: <https://www.lima-city.de/hilfe/e-mail-zustellung-und-diagnose> · DKIM/DMARC: <https://www.lima-city.de/hilfe/einen-dmarc-eintrag-anlegen>
- Tarif/Preis: <https://www.lima-city.de/webhosting> · AGB: <https://www.lima-city.de/juristisches#agb>

mailbox.org: Werte aus `berichte/2026-11-16-sende-postfach-plan.md`.

## Offene Punkte / was zu klären ist

- **lima-city:** vor Kauf per Support klären, ob eine **reine Mail-Subdomain ohne A-Records auf
  lima-city** aufgeschaltet werden kann (das Aufschalten ist webspace-orientiert).
- **Spacemail:** Subdomain-Nutzung im Panel bestätigen; die genaue MX-Priorität und der
  Nachweis-TXT-Wert stehen im Konto. **Die AUP ist streng** — vor einer Kalt-Outreach-Nutzung
  bewusst entscheiden.
- **mailbox.org:** Versandgrenze (4) und AGB zum Einzelversand (5) wurden am 2026-11-16 nicht
  erhoben; bei Bedarf nachtragen.
- Es wurde **nichts gekauft, nichts gesetzt, nichts ausgeliefert.**
