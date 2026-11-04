# Bau-Spezifikation Formularannahme (Cloudflare Pages Function + KV) — 2026-11-04

Entschieden: **Pages Function + KV statt Formspree**, Prüfung zum Start über den
**Dashboard-KV-Browser** (keine Admin-Seite). Gebaut wird erst nach Welle 1 und den
Anreicherungszahlen; hier die vollständige Spezifikation.

## Datenfluss
1. Formular (`/eintrag-beanspruchen/`, `/festpreis-garantie/antrag/`) postet an
   `functions/api/claim.ts` (gleiche Domain).
2. Function prüft (Pflichtfelder, Honeypot `_gotcha`, Ratelimit je IP), **verwirft unerwartete
   Felder** und **begrenzt die Größe** (max. 8 KB je Einsendung; längere Felder abgeschnitten).
3. Function schreibt die Einsendung als JSON in **KV** (Namespace `EINSENDUNGEN`).
4. Function schickt die Einsendung **zusätzlich als vollständige Mail an die verifizierte
   Betreiberadresse** (Pflicht, siehe (1)).
5. Antwort an den Absender: **Seitenanzeige** „Ihre Einsendung ist eingegangen; ein Mensch meldet
   sich in der Regel innerhalb eines Werktags." Keine automatische Bestätigungsmail an den
   Absender.

## (1) Email-Routing-Meldung an den Betreiber — Pflicht, kein Drittverarbeiter
Jede Einsendung geht zusätzlich als vollständige Mail (alle Felder im Klartext) an die
verifizierte Adresse des Betreibers, über das `send_email`-Binding eines Cloudflare Email Workers
(Versand nur an **verifizierte** Zieladresse = Betreiber, daher ohne dritten Verarbeiter). Drei
Gründe (so ins Wiki):
- Sie ist die **Sicherung von KV** — KV hat keine Sicherung und keine Versionierung; das Postfach
  hält jede Einsendung dauerhaft vor.
- Sie **startet das Verkaufsgespräch beim Garantie-Antrag persönlich** statt automatisch.
- Sie **braucht keinen dritten Verarbeiter** (Versand nur an die eigene verifizierte Adresse).

Absender-Bestätigung bleibt Seitenanzeige; eine automatische Mail an den Absender (und damit ein
Mailversender als dritter Dienst) wird erst mit dem [[mail-worker]] entschieden, nicht hier.

## (2) Datenschutz an der Erhebungsstelle (Art. 13 DSGVO)
Über der Absendeschaltfläche beider Formulare ein kurzer Hinweis: Verantwortlicher (DOM Holding
GmbH, Daniel Merz), **Zweck** (Prüfung des Garantie-Antrags bzw. der Beanspruchung), **Rechts-
grundlage** (Art. 6 Abs. 1 lit. b DSGVO – vorvertragliche Maßnahmen auf Anfrage des Betriebs),
**Speicherdauer** (siehe Löschfrist), **Link zur vollständigen Datenschutzerklärung**.

**Vorgeschlagene Löschfrist: 90 Tage** für abgelehnte und unbeantwortete Einsendungen, technisch
als KV-`expirationTtl` beim Schreiben (KV löscht den Schlüssel dann von selbst).
Begründung: 90 Tage decken die Bearbeitung plus einen Rückfrage-/Nachfasszyklus ab und sind kurz
genug, um keine Vorratsdaten anzuhäufen. Angenommene Einsendungen, die zu einer Eintragsänderung
führen, sind ohnehin über die CSV und die Git-Historie dokumentiert; ihr KV-Eintrag darf
mitablaufen. (Alternative, falls gewünscht: 180 Tage — mehr Puffer, aber mehr Vorrat.)
Datenschutzerklärung ergänzen: **KV als Speicherort, Zweck, 90-Tage-Frist**.

## (3) KV-Schlüssel und Hygiene
- Schlüssel enthält die **Formularart**: `garantie:2026-11-04T13-55:ab12` bzw.
  `beansprucht:2026-11-04T13-55:cd34` (Art : ISO-Zeit mit Bindestrichen : 4-Zeichen-Zufall). Im
  Dashboard auf einen Blick erkennbar.
- **Größenobergrenze** 8 KB je Einsendung, **Feld-Whitelist** (nur die bekannten Formularfelder;
  alles andere verworfen), damit KV nicht zur Mülldeponie wird.
- Honeypot (`_gotcha`) und einfaches Ratelimit je IP wie vorgeschlagen.

## (4) `site.json` und Datenschutz kürzen
- `processors.form` **ganz entfernen** (nicht auf `OFFEN_`): mit der Function ist Cloudflare der
  einzige Verarbeiter und steht als Hoster bereits in der Datenschutzerklärung.
- `contact.formEndpoint` → `/api/claim` (gleiche Domain), Formspree-Platzhalter raus.
- Datenschutzerklärung: Formulardienst-Absatz streichen; Absatz zu **KV als Speicherort** mit
  Zweck und 90-Tage-Frist aufnehmen.

## Verhältnis zum Mail-Worker ([[mail-worker]])
Die Function ist die Startlösung (Annahme + KV + Betreiber-Mail + Dashboard-Prüfung). Der
Mail-Worker ergänzt später die Automatik (Einordnung durch Claude, Entwurf, Prüfseite mit
„Senden"/„Übergehen", und die Entscheidung über eine Absender-Bestätigung samt Versender).

## Bauaufwand (in Gate 5, nach Welle 1)
- `functions/api/claim.ts` (~60–80 Zeilen inkl. Validierung, KV-Write mit TTL, Betreiber-Mail),
- KV-Namespace-Bindung + `send_email`-Binding in der Pages-/Worker-Konfiguration (braucht Daniels
  Cloudflare-Konto und eine verifizierte Absende-/Zieladresse),
- Formulare umstellen (Endpoint, Seitenanzeige), Datenschutz + `site.json` wie unter (4).
Schätzung: ~ ein halber bis ein Build-Tag. Kein Formspree, kein dritter Verarbeiter.

## Offen (Daniels Konten)
- Verifizierte Absende-/Zieladresse für die Betreiber-Mail (Cloudflare Email Routing).
- Die drei `STRIPE_LINK_*` (unabhängig von der Function).

## Zu bestätigen
Löschfrist **90 Tage** (oder 180)? Danach baue ich nach Welle 1.
</content>
