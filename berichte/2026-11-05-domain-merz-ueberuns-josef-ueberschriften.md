---
title: WO-5 – Domain angehängt (DNS offen), Merz Premium-Eintrag, „Über uns" neu, Josef raus, drei Überschriften
type: bericht
status: teilweise (Domain wartet auf DNS durch Daniel)
updated: 2026-11-05
---

# Fünf Aufträge

Neuer Build ausgeliefert: `https://30cbc697.schluesseldienste-deutschland.pages.dev`
(Produktionszweig `main`, pages.dev-Adresse unverändert). Inhalte aus 2/3/4 sind dort live.

## 1. Eigene Domain — angehängt, hängt an einem DNS-Eintrag (Daniel)

- `die-besten-schluesseldienste.de` ist ans Pages-Projekt **angehängt**, Status **pending**.
- Cloudflare meldet: **„CNAME record not set"**. Der Apex-CNAME wurde **nicht** automatisch
  angelegt, und nach sechs Minuten löste die Domain nicht auf (durchgehend HTTP 000).
- **Grund:** Der hinterlegte Token ist **Pages-beschränkt** (plus Zone:Read). DNS-Einträge darf
  er **nicht** schreiben (API: „Authentication error"). Ich kann den CNAME also nicht setzen und
  auch keinen www-Eintrag plus Redirect-Regel.
- **Was Daniel tun muss — eines von beiden:**
  1. **Dashboard, ein Klick:** Pages-Projekt → *Custom domains* → bei
     `die-besten-schluesseldienste.de` *Set up DNS / aktivieren*. Da die Zone im selben Konto
     liegt, legt Cloudflare den Apex-CNAME auf `schluesseldienste-deutschland.pages.dev`
     (proxied) selbst an; danach wird die Domain aktiv und das Zertifikat ausgestellt.
  2. **Oder** einen Token mit **Zone DNS:Edit** (für den Redirect zusätzlich **Rules:Edit**)
     geben — dann setze ich CNAME, www und Redirect fertig.
- **www → Apex:** braucht einen proxied DNS-Eintrag `www` und eine Single-Redirect-Regel
  (Host `www…` → 301 auf die Hauptdomain, Pfad/Query erhalten). Dashboard-Vorlage: *Rules →
  Redirect Rules → „Redirect from WWW to Root"*. Mit DNS/Rules-Token übernehme ich das.
- **`check_live.py` gegen die echte Domain: steht aus**, bis die Domain auflöst. (Die
  pages.dev-Prüfung war früher vollständig bestanden.)
- **Weiterhin nicht gemacht (wie gewünscht):** Sitemap einreichen, Suchmaschine anmelden.

## 2. Merz Sicherheit — Premium-Platz Mannheim

- `premium=true` gesetzt (über die angereicherte CSV → `listings.csv`), AES **ohne** Platz.
- Sichtbar als Karten-Kennzeichen **„Premium-Eintrag"** (Bild unten).
- **Prüffrage „auch im Premium-Band der Startseite?": Nein.** Band und Spitzenplatz liest der
  Code ausschließlich aus der Spalte `featured` (Kennzeichen „Premium-Platz"); die Spalte
  `premium` erzeugt **nur** das Karten-Kennzeichen „Premium-Eintrag", kein Band — weder auf der
  Startseite noch auf der Stadtseite.
- **Platz 1 in Mannheim, aber nicht manuell:** Merz steht oben, weil es den besten
  Bewertungs-Score hat (5,0 / 355 Bewertungen → 12,76 gegenüber Key Walter 4,9 / 274 → 11,95).
  Die Sortierung liest `owned`/`premium` **nicht**; das Kennzeichen hat die Position nicht
  verändert. Die Zusage „keine manuelle Höherstellung eigener Betriebe" hält.
- **Stufen-Hinweis für dich:** Willst du Merz als bezahlten Platz **ins Band und an die Spitze**,
  wäre das `featured=city` (Kennzeichen „Premium-Platz"). Du hast `premium` gewählt — das ist die
  schwächere Stufe. Sag Bescheid, falls du die stärkere willst.
- Bild: `scratchpad/merz_card.png`.

## 3. „Über uns" — von der Herausgeberbeschreibung zur Aufgabe

- Herausgeber-Block oben **entfernt**; die Mission steht jetzt zuerst.
- Mission ergänzt um **„unterschriebenes Serviceversprechen"** und eine Quelle: Link zur
  **Verbraucherzentrale** (aus `05-fact-sheet.md`, keine erfundenen Zahlen).
- **DOM Holding** nur noch **ein Satz** am Seitenende, plus das **Organization/Person-Schema** wie
  bisher. Startseite: Holding-Erwähnung **raus**. Fuß: „Herausgegeben von DOM Holding GmbH"
  **bleibt**.
- Textgate **bestanden** (ohne Rechtswörter-Schalter).

## 4. „Schlüsseldienst Josef" (Mannheim)

- `04-exclusions.csv`: `drop`, Grund `verhalten_betreiber` (wie die vier vorherigen).
- Mannheimer Stadttext per Pipeline neu erzeugt (`check_city_copy.py --write`): die Einleitung
  ohne Lücke umgeschrieben, Wortspanne gehalten, alle 787 Stadttexte bestehen weiter.
- Nachbarstädte (Ludwigshafen, Viernheim, Mutterstadt, Frankenthal, Weinheim) geprüft: ohne
  Bezug. (Die drei „Schlüsseldienst Josef"-Treffer, die bleiben, sind **Josef Terporten in
  Nettetal**, ein anderer Betrieb.)

## 5. Drei Überschriften zum Vergleichen

Bild: `scratchpad/hero_abc.png` (oberer Seitenbereich, 1440 px, nebeneinander).

- **C** („Schlüsseldienste, die ihren Preis schriftlich geben.") besteht das Textgate direkt.
- **A** und **B** fielen zuerst durch (Regel `branche_im_ersten_absatz`: „Schlüsseldienste"
  muss im ersten Absatz = in der H1 stehen; A/B tragen es nur in der Unterzeile). Auf deine
  Wahl hin tragen A und B jetzt eine **Branchenzeile über der H1** („Schlüsseldienste in
  Deutschland"); damit **bestehen alle drei**.
- Die **jetzige Fassung ist wiederhergestellt und live** — nichts an der Überschrift geändert,
  bis du entscheidest. Die Einträge-Sortierung ist unberührt.

Die Bilder liegen im Sitzungs-Scratchpad (nicht im Repo):
`/tmp/claude-1001/-home-dan-directory-blueprint/72df4dfc-0040-4439-9280-4c25f376c9fe/scratchpad/`.

---

# Nachtrag (nach deiner Entscheidung): Merz ins Mannheim-Band, Startseite sauber

## Merz Sicherheit jetzt `featured=city` (Stadt-Band Mannheim)

- `featured=city` **zusätzlich** gesetzt (`premium=true` bleibt). Merz steht nun als Karte im
  **Premium-Band der Mannheimer Seite**, Fuß „ab 29 € im Monat". Der veröffentlichte Stadt-Preis
  steht bereits in `tiers.city.price` = „29 € im Monat" und auf `/premium/` („Premium-Platz Stadt").
  Nichts am Preis zu ändern. Bild: `scratchpad/band_mannheim.png`.
- Merz erscheint **nicht** mehr als Rasterkarte (das Band zieht ihn heraus) und trägt im Band die
  „Premium"-Marke. Auf der Eintragskarte selbst gilt jetzt `featured` vor `premium`, also
  „Premium-Platz".

## Konflikt gefunden und behoben: `featured=city` speiste auch das Startseiten-Band

- **Fund:** `homeFeatured` (load.mjs) wurde aus **state + county + city** gebildet. Ein
  `featured=city`-Eintrag wäre damit **auch** im Startseiten-Band erschienen — und da es sonst
  keine featured-Einträge gibt, hätte Merz dort gestanden. Das Band zeigte zudem den
  **Stadt-Preis (29 €)** als Label, obwohl keine Stufe die Startseite verkauft.
- **Behoben:** Das Startseiten-Band wird jetzt **nur von `featured=state`** gespeist (load.mjs);
  der Preis-Prop des Bandes zeigt auf `tiers.state.price` (DirectoryHub). Stadt-/Umland-Plätze
  stehen damit nur im Band ihrer eigenen Seite, nicht national. Ergebnis: Startseiten-Band ohne
  eigenen Betrieb, **ohne Preis-Label** (offener Platz „Dieser Platz ist frei"). Bild:
  `scratchpad/band_startseite.png`.

## Deine Frage: welche Stufe speist das Startseiten-Band, und wie wird ein Preis eingetragen?

- **Nach der Behebung speist `featured=state` (Stufe „Premium-Platz Bundesland") das
  Startseiten-Band.** Diese Stufe hat in `tiers.state` **noch keinen Preis** — deshalb steht dort
  aktuell kein Betrieb, und das Band wirbt ohne Preis.
- **Preis eintragen, wenn Daniel ihn festgelegt hat:**
  1. `src/data/site.json` → `tiers.state`: `"price": "… € im Monat"` und `"link":
     "<Stripe-Zahlungslink>"` setzen (heute beide leer).
  2. `/premium/` zeigt die Zeile **„Premium-Platz Bundesland"** automatisch, sobald ein Preis
     gesetzt ist (die Seite filtert Stufen ohne Preis aus).
  3. Empfehlung: die Beschreibung dieser Stufe in `src/pages/premium.astro` (Zeile „bundesland")
     um die **Startseiten-Sichtbarkeit** ergänzen — heute nennt sie nur Bundesland- und
     Stadtseiten. (Textänderung; mache ich auf Zuruf.)
- Danach kann der Startseiten-Platz regulär besetzt werden — dann gilt auch dort die Regel
  „höchstens ein bezahlter Platz je eigenem Betrieb", und der Preis ist veröffentlicht.
- **Hinweis zur Stufen-Semantik:** „Bundesland" und „Startseite" fallen damit zusammen (die
  oberste Stufe kauft beides). Willst du eine **eigene** nationale Stufe getrennt vom Bundesland,
  wäre das ein zusätzlicher Wert `featured=country` — sag Bescheid, dann lege ich ihn an.

Neuer Build ausgeliefert: `https://8992ce52.schluesseldienste-deutschland.pages.dev`.

---

# Nachtrag 2

## 1. Bildschirmfotos im Repo, Überschriften als Text

Committet unter `berichte/screenshots/`: `hook-a-1440.png`, `hook-b-1440.png`, `hook-c-1440.png`
(oberer Seitenbereich, 1440 px) sowie `band-mannheim.png` und `band-startseite.png`.

Die drei Fassungen vollständig als Text:

**A** — `berichte/screenshots/hook-a-1440.png`
- Branchenzeile (über der H1): SCHLÜSSELDIENSTE IN DEUTSCHLAND
- Überschrift: „Ausgesperrt? Der Preis steht, bevor Sie wählen."
- Unterzeile: „Wer nachts vor einer zugefallenen Tür steht, ruft die erste Nummer an und erfährt
  den Preis, wenn die Arbeit längst läuft. Hier vergleichen Sie Schlüsseldienste in ganz
  Deutschland und sehen vorher, welcher Betrieb sich auf einen Festpreis festlegt."

**B** — `berichte/screenshots/hook-b-1440.png`
- Branchenzeile: SCHLÜSSELDIENSTE IN DEUTSCHLAND
- Überschrift: „Damit die Rechnung keine Überraschung wird."
- Unterzeile: „Bei einem Schlüsseldienst erfährt man den Preis oft erst, wenn die Tür schon offen
  ist. Dieses Verzeichnis zeigt für jede Stadt, welcher Betrieb seinen Festpreis für Türöffnung und
  Anfahrt vorher nennt und welcher nicht."

**C** — `berichte/screenshots/hook-c-1440.png` (ohne Branchenzeile, die Branche steht in der H1)
- Überschrift: „Schlüsseldienste, die ihren Preis schriftlich geben."
- Unterzeile: „Wer vor einer verschlossenen Tür steht, ruft die erste Nummer an und erfährt den
  Preis, wenn die Arbeit längst läuft. Hier sehen Sie vorher, welcher Betrieb sich auf einen
  Festpreis festlegt und welcher nicht."

**Jetzige, live stehende Fassung** (zum Vergleich, nicht geändert):
- Überschrift: „Schlüsseldienste in Deutschland, die ihren Preis vorher nennen"
- Unterzeile: „Wer vor einer verschlossenen Tür steht, ruft die erste Nummer an und erfährt den
  Preis, wenn die Arbeit längst läuft. Hier sehen Sie vorher, welcher Betrieb sich auf einen
  Festpreis festlegt und welcher nicht."

**Band-Bilder als Text:**
- `band-mannheim.png`: Band „Premium-Plätze: Schlüsseldienste in Mannheim". Erste Karte **Merz
  Sicherheit** (Marke PREMIUM, 5,0 bei 355 Bewertungen, Merkmale Schlüsseldienst /
  24-Stunden-Notdienst / Türöffnung, „Eintrag ansehen"). Zweite Karte offen: „Dieser Platz ist
  frei · Ab 29 € im Monat". Fuß: „Was ein Premium-Platz kostet · ab 29 € im Monat".
- `band-startseite.png`: Band „Premium-Plätze: Schlüsseldienste in Deutschland". Nur **ein offener
  Platz** („Dieser Platz ist frei … Ein Betrieb je Stufe und Stadt."), **ohne Preis**. Fuß: „Was
  ein Premium-Platz kostet" (ohne Preis). **Kein eigener Betrieb.**

## 2. Startseiten-Platz: nicht bepreisen (wie entschieden)

`tiers.state` bleibt **ohne Preis**, es wird **keine `country`-Stufe** angelegt. Begründung und die
Warnung, dass „Bundesland" und „Startseite" derzeit **dieselbe** Stufe sind und beim Bepreisen
getrennt werden müssen (sonst bekommt ein Bundesland-Käufer die bundesweite Startseite gratis
dazu), stehen jetzt im Wiki: [[monetization-slots]], Abschnitt „Das Startseiten-Band". **Stadt-
Premium zu 29 € bleibt vorerst die einzige laufende Stufe.** Neu bepreist wird erst, wenn nach der
30-Tage-Prüfung Zugriffszahlen vorliegen.

## 3. Domain — woran ich nach dem DNS-Klick erkenne, dass alles greift

Sobald Daniel im Dashboard den Apex-CNAME gesetzt hat (Pages → Custom domains → *Set up DNS*) und
für www einen proxied DNS-Eintrag plus die Redirect-Regel angelegt hat, prüfe ich:

- **Pages-Domain aktiv:** der Status der Domain im Pages-Projekt springt von `pending` auf
  `active`; die Meldung „CNAME record not set" verschwindet.
- **`check_live.py` gegen die echte Domain.** Ich habe es um genau die drei genannten Prüfungen
  erweitert (laufen nur gegen die echte Domain, gegen pages.dev übersprungen):
  1. **www-Weiterleitung:** `https://www.die-besten-schluesseldienste.de/` antwortet mit **301/308**
     und Location-Host = Hauptdomain — www liefert also keinen eigenen Inhalt aus (kein zweiter
     indexierbarer Host).
  2. **TLS-Zertifikat:** verifizierte TLS-Verbindung zur Hauptdomain (passt zum Hostnamen, von
     anerkannter Stelle, nicht abgelaufen), inklusive Ablaufdatum.
  3. **Sitemap zeigt auf die echte Domain:** alle `<loc>`-Hosts der Sitemap-Teile **und** der
     Adressen sind die Hauptdomain, **kein `pages.dev`** (sonst Doppelinhalt). Bis zum
     Domain-Anschluss zeigte die Sitemap bereits korrekt auf die echte Domain — diese Prüfung
     bestätigt es nach dem Umzug.
- Dazu die bestehenden Prüfungen (Startseite 200/H1/`lang`/canonical/kein `noindex`/keine
  Vorschaukarten, 404 für Unbekanntes, `robots.txt` + Sitemap, Stichproben indexierbar,
  `/verzeichnis/` noindex+follow, Impressum/Datenschutz mit Inhalt und ohne Google-Karte,
  `/premium/` und `/eintrag-beanspruchen/` noindex, pages.dev sendet `X-Robots-Tag: noindex`).
- Aufruf: `python3 scripts/check_live.py https://die-besten-schluesseldienste.de --pages-dev
  https://schluesseldienste-deutschland.pages.dev --expect-urls 2806`.
- Erst nach „Alle Prüfungen bestanden" beginnt die gestaffelte Indexierung. Sitemap einreichen und
  Suchmaschine anmelden bleiben bis dahin bewusst aus.
