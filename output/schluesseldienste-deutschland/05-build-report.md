---
title: Gate 5 – Build-Bericht
type: output
status: in-arbeit
updated: 2026-11-04
---

# Gate 5 – Build-Bericht

`npm install && npm run build` läuft durch: **4.629 Seiten in ~26 s, keine Fehler, keine Warnung
über fehlende Daten.** Datenstand abgeschlossen: **3.800 Einträge, 787 Stadtseiten, 16
Bundesländer, 5 Ratgeberseiten**; alle Stadttexte zahlenfrei und bestanden; `04-exclusions.csv`
führt **587** Zeilen (Gate-4-Ausschlüsse, breite Kategorien, Grenzorte, Verhaltens-Drops).

> Stand nach dem Nachtlauf 03./04.11.2026. Was in diesem Lauf ohne Rückfrage entschieden wurde,
> steht als „ENTSCHIEDEN" markiert; es ist jederzeit umkehrbar (CSV ändern, neu bauen).

## Was steht und geprüft ist
- **Build:** 4.629 Seiten, `dist/` mit `404.html`, `_headers`, `robots.txt`, `sitemap-index.xml` +
  `sitemap-0.xml` (**2.807** URLs im schlanken Start).
- **Schema/Technik:** **kein `aggregateRating`** im JSON-LD (0 Treffer), `lang="de"`, genau ein H1
  je Seite.
- **Interne Links (Punkt 4):** vollständiger Linkcheck über alle gebauten Seiten – **0 gebrochene
  interne Ziele, 0 leere `href`, keine Verlinkung auf eine `noindex`-Seite in der Sitemap.**
- **Sitemap-Filter:** Impressum, Datenschutz und `/festpreis-garantie/antrag/` sind **nicht** in der
  Sitemap (noindex greift).
- **Schriften:** selbst gehostet über `@fontsource` (Roboto, Roboto Slab), kein Google-Fonts-Abruf.
- **Karte:** Google Maps lädt erst nach Klick („Karte von Google Maps laden"), Einwilligung
  umgesetzt.
- **Pflichtseiten aus `site.json`:** Impressum (§ 5 DDG) und Datenschutz (Art. 13 DSGVO) werden
  generiert, **ohne Platzhalter**, im Fußbereich jeder Seite verlinkt. Keine Pflichtangabe fehlt.
- **`featuredPreview: false`** im ausgelieferten Build.
- **Herausgeber:** DOM Holding GmbH, Daniel Merz, Schwaig bei Nürnberg, HRB 43586, Amtsgericht
  Nürnberg; `Organization`/`Person` in „Über uns".
- **Zahlungsdienst:** `processors.payment.company` = Stripe Payments Europe, Limited, Dublin
  (belegt, Drittland, SCC) – in der Datenschutzerklärung genannt.
- **Screenshots (Punkt 5):** 12 Seiten je in **1440 px und 390 px** (Playwright + System-Chrome)
  unter `berichte/screenshots/`: Startseite, Bundesland (Baden-Württemberg), Mannheim, kleine
  Ortsseite (Tuttlingen), Eintrag mit und ohne Festpreis-Garantie, Leistungsseite
  (Einbruchschutz), `/festpreis-garantie/`, `/premium/`, Impressum, Datenschutz, 404.
- **Textgate (Punkt 6):** `lint_copy.py` auf Startseite, alle Bundesland-Seiten und „Über uns"
  **bestanden**. Stadttext-Gate `check_city_copy.py`: **787/787 bestanden, 0 Datenzahlen.**

## In diesem Lauf erledigt (vormals Startsperren)

1. **Formularannahme gebaut – PFLICHT-Sperre weg (ENTSCHIEDEN).** `contact.formEndpoint` steht jetzt
   auf `/api/claim`. Umgesetzt als **Cloudflare Pages Function** (`site/functions/api/claim.ts`)
   nach der Spezifikation in `berichte/2026-11-04-formularannahme-spec.md`: Honeypot und
   IP-Ratelimit, Feld-Whitelist, Ablage in KV mit **90 Tagen TTL** und lesbarem Schlüssel,
   Benachrichtigung an den Betreiber über die Email-Routing-Bindung, 303-Weiterleitung mit
   Bestätigung. Beide Formulare (Beanspruchung und Garantie-Antrag) tragen den **Art.-13-Hinweis**
   über der Datenschutz-Checkbox; die Datenschutzerklärung beschreibt KV-Speicherung,
   Betreiber-Postfach und Wiedervorlage. **Baut und läuft ohne externen Formulardienst.**
   → Deine Cloudflare-Klicks dafür stehen unten unter „Was du in Cloudflare tun musst".

2. **Impressum: beide offenen Punkte entschieden (ENTSCHIEDEN, kein Startblocker).** **Keine
   USt-IdNr.** (§ 27a UStG verlangt sie nur, wenn erteilt – es ist keine erteilt) und **keine
   Telefonnummer** für die DOM Holding GmbH. Beide Felder in `site.json` bleiben leer; die Seite
   lässt die betreffenden Zeilen weg. § 5 DDG lässt die E-Mail-Adresse als erreichbaren Kontakt
   genügen. Das ist damit **erledigt und kein offener Blocker mehr** – nicht mehr abzufragen.

3. **Fünf Schweizer Grenzorte gedroppt (ENTSCHIEDEN).** **Allschwil, Arlesheim, Oberwil, Riehen,
   Siegershausen** unter derselben Regel wie Basel entfernt (Grund in `04-exclusions.csv`:
   „Ausland (Schweiz); Verzeichnis ist für Deutschland"). Gegenprobe: **kein** weiterer Ort außerhalb
   eines deutschen Bundeslands verblieb im Datenstand. Betroffene Stadttexte neu erzeugt. Datenstand
   damit 3.800 Einträge / 787 Stadtseiten.

4. **Fünf Ratgeberseiten geschrieben und durch das Textgate (ENTSCHIEDEN, Punkt 7).**
   `/ratgeber/` ist nicht mehr leer. Fünf Artikel, alle aus den im Regelwerk zugelassenen Quellen
   (Verbraucherzentrale, Stiftung Warentest, Polizeiliche Kriminalprävention / k-einbruch.de,
   Handwerkskammer, kommunale Notrufseite) – **keine anderen Schlüsseldienst-Websites, keine
   Branchenbücher, keine Presseportale**. Quellen mit Abrufdatum in `05-fact-sheet.md` und je Seite
   unter „Quellen". Alle fünf durch `lint_copy.py --erlaube-rechtswoerter` **bestanden**.
   - `/ratgeber/was-kostet-ein-schluesseldienst/` (≈ 990 Wörter)
   - `/ratgeber/ausgesperrt-was-tun/` (≈ 970 Wörter)
   - `/ratgeber/unserioese-schluesseldienste-erkennen/` (≈ 1.094 Wörter) – nennt **bewusst keinen
     einzelnen Betrieb**, nur wiederkehrende Muster.
   - `/ratgeber/schloss-austauschen/` (≈ 886 Wörter)
   - `/ratgeber/tueren-nachruesten-einbruchschutz/` (≈ 995 Wörter)

   **Warum nicht mit der seo-content-engine-Skill:** ihr Ablauf stützt sich auf eine SERP-/
   Wettbewerbsanalyse, also auf andere Schlüsseldienst-Websites – genau die Quellen, die das
   Regelwerk für Gate 5 ausschließt. Deshalb aus den vorgeschriebenen Quellen geschrieben und nur
   durch den Linter der Skill geprüft. **Kostengrenze:** keine bezahlte externe API verwendet, somit
   **0 $** externe Kosten, weit unter der Grenze von 40 $. Die eine-Seite-zuerst-Messung lag deutlich
   unter 10 $/Seite, daher wurden alle fünf geschrieben.

## Noch offen (bewusst nicht angefasst)

- **Stripe-Zahlungslinks.** `tiers.premium/bestOf/city.link` stehen weiter auf `STRIPE_LINK_…`.
  Keine PFLICHT-Sperre (die `/premium/`-Seite baut), aber **Verkauf erst möglich**, wenn du die drei
  Links in deinem Stripe-Konto anlegst und einträgst. Verkauft wird ohnehin von Hand (Spalte setzen,
  neu bauen).
- **Anwaltliche Prüfung von Impressum und Datenschutz.** Beide Seiten sind vollständig und
  platzhalterfrei, aber das Wiki ist keine Rechtsberatung; die Endfassung sollte ein Anwalt prüfen.
- **Welle 2 / Cloudflare-Auslieferung.** Nicht Teil dieses Laufs (Gate 6).

## Was du in Cloudflare tun musst (für die Benachrichtigung bei Formulareingang)

KV-Namespace `EINSENDUNGEN` ist angelegt und gebunden; die Formulare nehmen live an und schreiben
nach KV (bestätigt durch eine echte Live-Absendung). Pages Functions können aber **nicht selbst
mailen** (kein `send_email`-Binding). Der Versand läuft deshalb über den Worker `notify-worker/`
(`send_email`-Binding), den die Function per Service-Binding `MAILER` aufruft. Worker und
Service-Binding sind ausgeliefert (`MAILER` an der Produktion bestätigt). Es fehlen noch **drei
einmalige Schritte in deinem eigenen** Cloudflare-Konto des Verzeichnisses (getrennt von den
Schlüsseldienst-Websites) — nur diese drei, danach kommt die Mail:

1. **Email Routing** auf `die-besten-schluesseldienste.de` aktivieren (legt die MX/DNS selbst an).
2. Deine **gewöhnliche Adresse** (nicht die Verzeichnis-Domain, nicht eine Schlüsseldienst-Domain)
   als **Destination** in Email Routing hinzufügen und den **Bestätigungsklick** in der Mail an
   diese Adresse ausführen.
3. Im eigenen Terminal:
   `npx wrangler pages secret put NOTIFY_TO --project-name=schluesseldienste-deutschland`,
   Wert = dieselbe gewöhnliche Adresse. Als **Secret** (nicht als Variable), damit es Deploys
   überdauert und nie im Repo steht. Absender `NOTIFY_FROM` steht schon in `wrangler.toml`.

Erst danach geht bei jedem Formulareingang innerhalb einer Minute eine Mail mit dem Inhalt der
Einsendung an deine Adresse. Scheitert der Versand, bleibt die Einsendung in KV und das Formular
zeigt dem Absender trotzdem „gesendet". Siehe `berichte/2026-11-06-formular-benachrichtigung.md`.

## Ansehen
`preview-site.command` (Mac) / `preview-site.bat` (Windows) in `site/`, nie direkt
`dist/index.html`. Screenshots unter `berichte/screenshots/`.

## Nächste Schritte
Gate 6 (schlanker Start): Cloudflare-Bindungen oben setzen, optional Stripe-Links, dann
`npx wrangler pages deploy dist`, `check_live.py`, gestaffelte Indexierung. Vor dem Scharfschalten
Impressum und Datenschutz anwaltlich prüfen lassen.
