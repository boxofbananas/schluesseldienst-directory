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

---

# Nachtrag (2026-11-04) — vier Ergänzungen, ersetzt die flache 90-Tage-Frist oben

## (1) Löschfrist gestaffelt nach Zweck
- **Erteilte Garantie / bearbeitete Beanspruchung:** KV-Eintrag **sofort löschen**, sobald das
  Ergebnis in der CSV steht (keine zweite Kopie ohne zweiten Zweck). Explizites `KV.delete` im
  Pflegeablauf, in [[refresh-and-upkeep]] aufgenommen.
- **Abgelehnt / unbeantwortet / abgebrochen:** **90 Tage**, technisch über `expirationTtl` beim
  Schreiben (kein vergessbarer Aufräumlauf).
- **Begründung (Wiki):** Nach einer Ablehnung trägt kein Zweck die längere Aufbewahrung fremder
  Gewerbedaten, und der Garantie-Antrag enthält eine Unterschrift. 180 Tage wären nicht begründbar.

## (2) Zwei Speicherorte, zwei zutreffende Fristen — meine Empfehlung: volle Mail + Postfachregel
Die Benachrichtigungsmail enthält die vollständige Einsendung. Eine „90 Tage in KV"-Zusage wäre
unzutreffend, solange dieselben Daten unbefristet im Postfach liegen. Regelung:
- **Datenschutzerklärung nennt beide Orte:** Cloudflare KV (90 Tage bzw. sofort bei Abschluss)
  **und** das E-Mail-Postfach des Verantwortlichen mit eigener Frist.
- **Empfehlung: Variante (a) — volle Mail behalten, Postfachfrist per Regel.** Gründe: die volle
  Mail ist die **Sicherung** von KV, trägt den **persönlichen Verkaufsanlass** und enthält bei
  angenommenen Garantie-Anträgen die **unterschriebene Serviceversprechen-Zusage** (ein Beleg, den
  der Betreiber zu Recht behält). Variante (b) (nur Formularart + KV-Schlüssel in der Mail) löste
  den Konflikt, nähme aber Sicherung **und** Unterschriftsbeleg und zwänge, für jeden Lead KV zu
  öffnen — schlechter für den Verkaufsanlass. Postfach-Frist: **abgelehnte/unbeantwortete
  Einsendungsmails nach 90 Tagen löschen** (Filter/Label im Postfach, deckungsgleich mit KV);
  **angenommene Garantie-Anträge** als Geschäftsbeleg für die Laufzeit der Garantie plus
  gesetzliche Aufbewahrung behalten. **Abhängigkeit, die in der Erklärung ehrlich stehen muss:**
  die Postfach-Frist wird durch eine einmalig eingerichtete Filterregel in Daniels Postfach
  eingehalten — ohne sie wäre die Zusage unzutreffend.

## (3) Wiedervorlage statt Totalverlust
Beim Löschen bleibt **nur eine Wiedervorlage-Zeile**: Firmenname, Ort, Datum, Formularart,
Ablehnungsgrund in Kurzform. **Kein Formularinhalt, keine Preise, keine Unterschrift.** Zweck:
Nachfassen, wenn der Betrieb die fehlende Voraussetzung erfüllt.
- **Ort (Empfehlung): eine Datei `output/<slug>/wiedervorlage.csv`** — außerhalb von `site/`,
  per `.gitignore` aus dem Repo, nie in Site-Daten, nie in einen Build. Geschrieben **beim
  manuellen Ablehnen** (Pflegeablauf), nicht von der Function. Besser als eine KV-Liste ohne
  Ablauf, weil die Daten dann nicht unbefristet bei Cloudflare lägen und der Betreiber sie in der
  Hand hat.
- **Frist (Vorschlag): 12 Monate** — ein Jahr genügt, damit der Betrieb die fehlende
  Voraussetzung erfüllen kann (Bewertungen sammeln, Festnetz einrichten) und der Betreiber einmal
  nachfasst. Rechtsgrundlage Art. 6 Abs. 1 lit. f (B2B-Nachfassen).
- Datenschutzerklärung nennt die Wiedervorlage als **eigene Verarbeitung** mit eigenem Zweck und
  eigener Frist.
- **Wiki-Regel (ausdrücklich):** Preise aus einem abgelehnten Antrag erscheinen **nie** auf einer
  Eintragsseite. Ein ungeprüfter Preis liest sich als Zusage des Verzeichnisses und entwertet die
  Festpreis-Garantie. Die drei Preise erscheinen ausschließlich mit erteilter Garantie, aus der CSV.

## (4) Eigene Adresse, maschinelle Vorprüfung, keine automatische Erteilung
- `contact.email` → **info@die-besten-schluesseldienste.de** (Cloudflare Email Routing auf Daniels
  Postfach); die Function-Benachrichtigung geht an dieselbe verifizierte Zieladresse.
  `publisher.email` bleibt **info@domholdinggmbh.de** (Impressum = Herausgeberin).
- **Wiki ([[footprint-rules]]):** Antworten gehen nie von einer der eigenen
  Schlüsseldienst-Domains (sichtbarer Zusammenhang); bis es ein sendefähiges Postfach gibt, wird
  von der Holding-Adresse geantwortet.
- **Neues Skript `scripts/pruefe_antrag.py`** (nach Welle 1): prüft maschinell, was prüfbar ist —
  Impressum unter der angegebenen Domain erreichbar, Festnetz mit zur PLZ passender Ortsvorwahl,
  alle drei Preise ausgefüllt und plausibel, Bewertungslage gegen „ab 5 Bewertungen Schnitt ≥ 4,0".
  Ausgabe: eine Zeile je Voraussetzung (bestanden / offen / durchgefallen) **und** ausdrücklich,
  was **nicht** maschinell prüfbar ist (Unterschrift, Callcenter-Weiterleitung, telefonische
  Preisbestätigung). Ergebnis gehört in die Benachrichtigungsmail. **Die Function bleibt dumm**
  (annehmen, speichern, melden), damit Regeländerungen kein Ausliefern brauchen.
- **Wiki-Regel:** Die **Erteilung** der Festpreis-Garantie wird **nie** automatisiert; kein Skript
  setzt `geprueft` ohne menschliche Entscheidung. Der Wert liegt in der telefonischen Bestätigung
  der drei Preise.
- **Für nach dem Start, in `06-launch.md` vormerken (nicht jetzt bauen):** ein Skript, das aus einer
  angenommenen Einsendung die CSV-Zeile setzt; automatischer Neubau + Ausliefern bei CSV-Änderung;
  Erinnerung an fällige Jahreserneuerungen 30 Tage vorher.
</content>
