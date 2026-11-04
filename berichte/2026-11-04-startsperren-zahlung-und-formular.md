# Gate-5-Startsperren: Formularannahme ohne Formspree, offene Zahlungslinks (2026-11-04)

Betrifft die offenen Start-Sperren des Gate-5-Build-Berichts: **`formEndpoint`** und die **drei
`STRIPE_LINK_*`** (`site.json`). Hinweis vorab: Dieser Bericht prüft und legt vor, er baut nichts.

## Ausgangslage
- `site.json → contact.formEndpoint` steht auf `https://formspree.io/f/FORMULAR_ID` – ein
  **Platzhalter**. Beide Formulare (`/eintrag-beanspruchen/`, `/festpreis-garantie/antrag/`)
  posten dorthin.
- Laut [[mail-worker]] ist der **eigentliche** Endpunkt `POST /claim` des Mail-Workers
  (Cloudflare Email Worker, `templates/worker/`), der die Einsendung annimmt, eine feste
  Empfangsbestätigung schickt, durch Claude einordnet und eine Prüfseite mit „Senden"/„Übergehen"
  bereitstellt. Der Worker ist aber „nach dem Start, wahlweise" – zum Start fehlt also ein
  Annahmeweg, und Formspree wäre der Lückenbüßer.

## Vorschlag: Cloudflare Pages Function + KV statt Formspree
Da das Verzeichnis ohnehin auf Cloudflare Pages liegt und Cloudflare in der
Datenschutzerklärung als Hoster/Auftragsverarbeiter steht, nimmt eine **Pages Function** den
POST an und legt die Einsendung in **Cloudflare KV**. Kein zweiter Auftragsverarbeiter, keine
Drittlandübermittlung, kein zusätzlicher AV-Vertrag. Passt zu [[refresh-and-upkeep]]: jede
Einsendung wird von Hand geprüft, bevor sich die CSV ändert.

**Bauteile (neu in Gate 5):**
1. `functions/api/claim.ts` – `onRequestPost`: Felder lesen, einfache Prüfung (Pflichtfelder,
   Honeypot `_gotcha`, Ratelimit je IP), als JSON in KV schreiben (Schlüssel
   `claim:<zeit>:<zufall>`, Wert = Formulardaten + Zeitstempel + Formularart). Antwort: Redirect
   auf eine Dank-Seite **oder** JSON für ein Inline-„eingegangen".
2. **KV-Namespace** `EINSENDUNGEN`, im Pages-Projekt gebunden (`wrangler.toml`/Dashboard).
3. **Prüfseite** – zwei einfache Wege:
   - ohne Bauarbeit: der **KV-Browser im Cloudflare-Dashboard** (Daniel liest die Einsendungen
     direkt), oder
   - mit wenig Bauarbeit: `functions/admin/[[path]].ts` mit **Basic Auth** (ein Passwort als
     Secret), listet die KV-Einträge und zeigt sie einzeln.
4. **Formularänderung**: `formEndpoint` → `/api/claim` (gleiche Domain), Formspree-Platzhalter
   raus; Dank-/Bestätigungsanzeige auf der Seite.

**Aufwand:** klein – eine Function (~40–60 Zeilen), KV-Bindung, wahlweise eine Auth-Prüfseite
(~40 Zeilen). Schätzung ~ ein halber Build-Tag. Deutlich weniger als der volle Mail-Worker.
**Keine neue Abhängigkeit:** KV-Namespace und Pages-Projekt laufen auf Daniels
Cloudflare-Konto, das für das Hosting ohnehin nötig ist.

## Verhältnis zum Mail-Worker ([[mail-worker]])
Die Function **ersetzt den Worker nicht, sie überbrückt die Zeit bis zu ihm** und kann danach
bleiben oder weichen:
- **Zum Start:** Pages Function + KV + Dashboard/Prüfseite. Annahme und manuelle Prüfung stehen,
  ohne Dritten.
- **Später:** Der Mail-Worker ergänzt die E-Mail-Seite (feste Empfangsbestätigung, Einordnung
  durch Claude, Entwurf, Prüfseite mit „Senden"/„Übergehen"). Dann entweder die Function auf den
  Worker-`/claim` umlenken oder sie als reinen KV-Mitschrieb behalten. Beide schließen sich nicht
  aus; der Worker bringt die Automatik, die Function die einfache Annahme.

## Empfangsbestätigung: ja, dafür bräuchte es einen dritten Dienst – hier benannt
Cloudflare Pages Functions / Workers haben **keinen SMTP-Ausgang**; eine Function kann nicht von
sich aus eine Bestätigungsmail an den Absender schicken. Möglichkeiten, ehrlich benannt:
- **Keine Bestätigungsmail, nur Seitenanzeige** („Ihre Einsendung ist eingegangen, ein Mensch
  meldet sich in der Regel innerhalb eines Tages"). **Kein dritter Dienst, DSGVO-sauberste
  Variante.** Empfehlung für den Start.
- **Bestätigung an den Betreiber** (nicht den Absender): über Cloudflare Email Routing bzw. das
  `send_email`-Binding eines Email Workers – aber nur an **verifizierte** Zieladressen, also an
  Daniel, nicht an beliebige Absender. Damit ließe sich „neue Einsendung" an Daniel melden, ohne
  Dritten.
- **Bestätigung an den Absender per Mail** braucht einen **Mailversender als dritten
  Auftragsverarbeiter**: **MailChannels** (seit Mitte 2024 kostenpflichtiges Konto nötig),
  **Resend**, **Postmark** oder **Amazon SES** – jeder ein zusätzlicher Verarbeiter, Resend/
  Postmark/SES mit Drittlandübermittlung und eigenem AV-Vertrag. Das ist derselbe Zielkonflikt
  wie bei Formspree, nur von der Annahme zur Bestätigung verschoben.

Empfehlung: zum Start **Seitenanzeige** (kein Dritter); die automatische Absender-Bestätigung
kommt mit dem Mail-Worker, und erst dann ist zu entscheiden, über welchen Versender sie läuft –
das wäre eine eigene, ausdrückliche Entscheidung, kein stiller Einbau.

## Was offen bleibt (braucht Daniels Konten)
- **`formEndpoint`** ist mit der Pages Function **lösbar ohne Formspree** (KV-Namespace auf
  Daniels Cloudflare-Konto anlegen).
- **Die drei `STRIPE_LINK_*`** (Premium-Eintrag, Stadt-Premium, Top-Platzierung) bleiben offen:
  sie brauchen Daniels Stripe-Konto und die dort erzeugten Zahlungslinks. Die Function ändert
  daran nichts; Stripe ist unabhängig.

## Entscheidung, die ansteht
Function-Weg (empfohlen) oder doch Formspree zum Start? Und für die Prüfseite: Dashboard-KV-Browser
(keine Bauarbeit) oder eine passwortgeschützte Prüfseite (wenig Bauarbeit)?
</content>
