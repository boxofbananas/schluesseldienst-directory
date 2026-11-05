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
