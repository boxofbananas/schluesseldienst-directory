# Verzeichnis-Blueprint: Die besten Schlüsseldienste

Dieser Ordner baut aus einem Google-Maps-Export ein Branchenverzeichnis: **alle
Schlüsseldienste in Deutschland**, auf `die-besten-schluesseldienste.de`, als statische
Astro-Site bei Cloudflare Pages. Sie richten Claude Code darauf, und es baut nach dem
Regelwerk statt zu raten.

**Branche, Land, Domain, Marke und Herausgeber stehen fest** und werden nicht abgefragt:

| | |
|---|---|
| Verzeichnis | Die besten Schlüsseldienste |
| Domain | `die-besten-schluesseldienste.de` |
| Branche | Schlüsseldienst (Google-Maps-Kategorie `locksmith`) |
| Aufbau | Startseite → bis 16 Bundesländer → Städte → Einträge |
| Herausgeber | DOM Holding GmbH, Anton-Bruckner-Straße 8, 90571 Schwaig bei Nürnberg |
| Geschäftsführer | Daniel Merz, HRB 43586 |
| Wichtigste Stadt | Mannheim |

## Was vorher da sein muss

- **Claude Code** installiert und lauffähig (`claude` läuft im Terminal).
- **Node.js 20 oder neuer** (`node -v`), für den Build in Gate 5. Falls der Befehl fehlt:
  nodejs.org.
- **Die Einträge**, auf einem von zwei Wegen: **DataForSEO** (Ihre API-Anmeldung einmal auf
  diesem Rechner gespeichert, siehe unten; Claude nennt die genauen Kosten, bevor es abruft)
  oder ein **Outscraper-Export** der Kategorie, abgelegt als `input/listings-raw.csv`.
- **Die Telefonnummern Ihrer eigenen Schlüsseldienst-Betriebe.** Nur die Nummern. Diese
  Zeilen werden wie jeder andere Betrieb gelistet; die Kennzeichnung dient nur dem Bericht
  (`wiki/framework/footprint-rules.md`).
- Wahlweise: **eine oder zwei Websites**, deren Optik Sie lieber hätten, gleich welche
  Branche. Ohne sie bekommt das Verzeichnis die fertige Standardoptik, die des Referenzbaus
  (sagen Sie „zeig mir den Referenzbau").
- Für Gate 5 (die Site baut auch ohne, kann aber nicht starten): die Domain registriert, eine
  **Kontakt-E-Mail-Adresse auf der Domain**, die **Umsatzsteuer-Identifikationsnummer** für
  das Impressum, **Lebenslauf und Bild** des Geschäftsführers für „Über uns", und die
  **Stripe-Zahlungslinks** der Stufen, die zum Start verkauft werden sollen.

## DataForSEO verbinden (einmal, im Terminal)

1. In app.dataforseo.com unter **API Access** die API-Anmeldung (Ihre E-Mail-Adresse) und das
   **API-Passwort** holen. Das API-Passwort ist nicht das Passwort, mit dem Sie sich anmelden;
   „Reset API password" schickt ein neues.
2. Das Programm **Terminal** öffnen (unter Windows: PowerShell), `python3 ` mit Leerzeichen
   tippen (Windows: `python `), die Datei `connect_dataforseo.py` aus dem Ordner `scripts`
   hineinziehen und Eingabetaste drücken.
3. Anmeldung tippen, Passwort einfügen (es bleibt verborgen), Eingabetaste. Es prüft die
   Anmeldung bei DataForSEO und speichert sie in den Einstellungen von Claude Code. In diesen
   Ordner wird nichts geschrieben.

Das ist die ganze Einrichtung. Ein DataForSEO-Connector in claude.ai oder in der
Desktop-Anwendung gibt Gesprächen die Datenwerkzeuge, speichert aber keine Anmeldung auf dem
Rechner, also kann der Abruf ihn nicht benutzen.

## Loslegen

1. Ordner entpacken, Dateien darin nicht umbenennen.
2. Entweder DataForSEO verbinden (oben) oder den Outscraper-Export als
   `input/listings-raw.csv` ablegen.
3. Ein Terminal in diesem Ordner öffnen und `claude` starten.
4. Tippen: `Lies CLAUDE.md und starte Gate 1.`
5. Die **drei** Fragen beantworten, die Umfangsdatei freigeben, dann `Gate 2 starten` und so
   weiter bis Gate 6. Claude hält nach jedem Gate an und wartet auf Sie. Alles landet in
   `output/schluesseldienste-deutschland/`.

Was die Gates tun, je eine Zeile:

1. **Umfang:** die drei offenen Punkte – Ihre eigenen Telefonnummern, die Optik, die Freigabe
   des Datenabrufs mit genannten Kosten. Branche, Land, Domain und Herausgeber stehen fest und
   werden nicht gefragt.
2. **Bereinigen:** aus der Rohdatei werden die echten Betriebe mit Bewertungen. Sie lesen den
   Bericht; er zeigt auch, welche fremden Gewerbe über die Kategorie hereinkamen (Schuhmacher,
   Gravurbetriebe, Metallbauer, Baumärkte), welche Namen an vielen Adressen vorkommen und
   welche Einträge keinen Ortsbezug haben. **Gelöscht wird nichts davon** – Sie entscheiden in
   Gate 4.
3. **Anreichern:** Claude schreibt mit Ihnen die Merkmalsliste für Schlüsseldienste, dann
   bekommt jeder Eintrag diese Merkmale (wahr / falsch / keine Angabe) und eine sachliche
   Beschreibung aus den Daten. Trägt Ihr Export keinen Text, liest Claude die eigenen Websites
   der Betriebe, was nichts kostet, und nennt die Kosten des Schreibens vorher.
4. **Planen:** welche Bundesländer und Städte eine Seite bekommen, welche Einträge
   herausfallen und warum, was zum Start in die Sitemap kommt, die Optik. Der Plan endet mit
   einer kurzen Tabelle von Entscheidungen, jede mit Vorschlag, sodass eine Antwort sie
   freigibt.
5. **Bauen:** die Astro-Site entsteht aus `templates/astro/` und Ihren Daten, **Impressum und
   Datenschutzerklärung werden aus den Herausgeberdaten erzeugt und im Fußbereich jeder Seite
   verlinkt**, jeder Textblock besteht das Textgate, `npm run build` läuft durch. Sie bekommen
   einen Bericht, was vor dem Start noch fehlt.
6. **Schlanker Start:** die starken Seiten in die Sitemap (Startseite, alle Bundesländer, alle
   Stadtseiten), dünne Einträge auf noindex, Auslieferung nach Cloudflare Pages, gestaffelte
   Einreichung.

## Die Festpreis-Garantie: der Grund, warum Betriebe anrufen

Jeder Eintrag trägt sichtbar eines von zwei Zeichen: **„Festpreis-Garantie [Jahr]"** mit drei
Preisen (Türöffnung tagsüber, Türöffnung nachts, Anfahrt) oder **„Noch keine
Festpreis-Garantie"**. Das zweite verlinkt auf `/festpreis-garantie/antrag/`, und genau das
ist der Gesprächsanlass: die Prüfung ist **kostenlos**, und beim selben Anruf geht es um
Sichtbarkeit.

Die Garantie hat drei Teile: Der Preis steht im Eintrag, bevor der Kunde anruft. Der Betrieb
garantiert, dass der genannte Preis der Rechnungspreis ist. Und ein Verstoß hat Folgen: Legt
ein Kunde eine Rechnung über dem garantierten Preis vor, konfrontiert der Herausgeber den
Betrieb, entzieht die Garantie und nimmt die Preise aus dem Eintrag. Das kann ein einzelner
Betrieb auf seiner eigenen Website nicht nachbauen, deshalb ist es sein Verkaufsargument.

Die Garantie ist **nicht kaufbar**. Bezahlt wird nur Sichtbarkeit. Die Garantie gibt der
Betrieb; der Herausgeber prüft sechs Voraussetzungen, die auf `/festpreis-garantie/`
veröffentlicht stehen, auf Grundlage von Selbstauskunft und der Prüfung von Unterlagen und
Website. **Es gibt keinen Test vor Ort**, und das steht auf `/festpreis-garantie/`
ausdrücklich. Die Garantie trägt die Jahreszahl, gilt ein Jahr, wird jährlich erneuert und bei
belegten Verstößen entzogen. Alles dazu in `wiki/framework/siegel-programm.md` (die Datei
heißt noch nach dem alten Namen des Programms).

## Was auf dieser Site rechtlich Pflicht ist

- **Impressum** nach § 5 DDG auf `/impressum/`, **Datenschutzerklärung** nach Art. 13 DSGVO
  auf `/datenschutz/`, beide aus den Herausgeberdaten erzeugt und von jeder Seite aus
  verlinkt. Enthält eine der beiden einen Platzhalter, gilt der Build als unfertig und wird
  nicht ausgeliefert.
- **Keine Karte, kein externes Skript, keine externe Schrift ohne Einwilligung.** Google Maps
  erscheint als Platzhalterfläche; erst ein Klick lädt die Karte. Schriften liegen auf dem
  eigenen Server.
- **Kein Google Analytics, keine Search Console** auf dieser Domain. Ausgewertet wird mit
  Cloudflares Statistik ohne Cookies.
- **Schlüsseldienst ist in Deutschland kein zulassungspflichtiges Handwerk.** Es gibt keine
  Lizenz und keine Meisterpflicht. Kein Text auf dieser Site behauptet „lizenziert",
  „zugelassen" oder „zertifiziert", und keiner benutzt „Innung", „Verband", „Kammer",
  „amtlich", „Verbraucherschutz" oder „getestet" – sie würden den Eindruck erwecken, hinter
  dem Verzeichnis stehe eine amtliche Stelle.

Das Wiki nennt, welche Seiten und Angaben Pflicht sind. **Es ist keine Rechtsberatung.** Die
Endfassung von Impressum, Datenschutzerklärung und AGB sollte ein Anwalt prüfen, bevor die
Site online geht.

## Die Site ansehen, bevor sie live ist

In `output/schluesseldienste-deutschland/site/` auf `preview-site.command` (Mac) oder
`preview-site.bat` (Windows) doppelklicken. Der Browser öffnet die Site, von Ihrem Rechner
ausgeliefert, genau wie sie später im Netz steht. Fenster schließen beendet es. Im Terminal
ist dasselbe `npm run preview -- --open`.

Unter macOS weigert sich das System beim ersten Mal, weil die Datei aus einem Download kommt.
Rechtsklick, „Öffnen", bestätigen; ab macOS 15 in den Systemeinstellungen unter „Datenschutz &
Sicherheit" auf „Dennoch öffnen".

**`site/dist/index.html` nicht doppelklicken.** Dieser Ordner ist für die Domain gebaut; als
Datei geöffnet zeigt er keine Gestaltung, und die Links führen ins Leere. Es ist nichts
kaputt.

## Was es an Claude-Nutzung kostet

Die beiden Schreibschritte sind die teuren. **Es gibt dafür noch keine deutschen Messwerte.**
Die Zahlen unten stammen aus dem englischen Pilotprojekt (einem Verzeichnis für Poolbauer in
Florida, 1.848 Einträge, 134 Stadtseiten, als Subagenten auf Sonnet) und sind
Größenordnungen für den Aufwand, keine Zusage:

| Schritt | Je Einheit |
|---|---|
| Gate 3, Merkmale und Beschreibungen | etwa 4.000 Token je Eintrag |
| Gate 5, Stadttexte | etwa 18.000 Token je Stadtseite |

Es läuft über Ihr Claude-Abonnement, es gibt also keine API-Rechnung, aber es zählt gegen Ihr
Nutzungsvolumen. Claude nennt die Schätzung und wartet vor jedem Schritt auf Ihre Freigabe.

## Nach dem Start

- Verkaufter Platz, beanspruchter Eintrag, korrigierte Telefonnummer, neu erteilte oder
  entzogene Festpreis-Garantie, geänderte Garantiepreise: CSV ändern, `Gate 5 starten`, erneut
  ausliefern. **Nie eine erzeugte Seite von Hand bearbeiten.**
- Von Hand verkaufen: Zahlungslink senden, Spalte setzen (`premium`, `featured`,
  `best_of_rank`, `claimed`), neu bauen. Die Garantie wird nicht verkauft: nach geprüftem
  Garantie-Antrag `geprueft`, `geprueft_jahr`, `garantie_tag`, `garantie_nacht` und
  `garantie_anfahrt` setzen, neu bauen. Stufen und der Garantie-Nachweis zum Einbinden stehen
  in `templates/featured-tiers.md`.
- Einmal im Jahr jede Festpreis-Garantie erneuern, mit Anruf, ob die drei Preise noch gelten
  (`wiki/framework/refresh-and-upkeep.md`).
- Wie das Verzeichnis nach dem Start Links und Kunden bekommt:
  `wiki/framework/authority-and-links.md`.

## Nach dem Start, wahlweise: eine echte Adresse mit Einordnung durch Claude

Der Mail-Worker gibt dem Verzeichnis ein funktionierendes `hallo@die-besten-schluesseldienste.de`
ohne Postfachanbieter: jede E-Mail und jede Formulareinsendung bekommt innerhalb einer Minute
eine Bestätigung, Claude ordnet sie ein (Art der Anfrage, welcher Eintrag, ob die
E-Mail-Domain zur Website passt, was fehlt), und Sie bekommen eine Prüf-E-Mail mit einem
Entwurf und einer Seite mit „Senden" und „Übergehen". **Zu einem Betrieb geht nichts, bevor
Sie auf „Senden" drücken.** Es läuft auf Cloudflares Workers-Paid-Tarif (5 $ im Monat) plus
Cent für Claude-Nutzung und braucht die Site live auf Cloudflare Pages mit der DNS derselben
Domain im selben Konto. In Claude Code: `Gib mir die Terminal-Befehle für die Mail-Schlüssel.`,
dann `Richte den Mail-Worker ein. Die Prüf-E-Mails gehen an <Ihre Adresse>.`, dann
`Verbinde die Formulare mit dem Mail-Worker und liefere die Site aus.` Alles dazu in
`wiki/framework/mail-worker.md`.

## Was hier drin ist

```
CLAUDE.md       die Regeln, denen Claude folgt, und die sechs Gates
README.md       diese Seite
input/          listings-raw.csv (DataForSEO-Abruf oder Outscraper-Export)
output/         der Build-Ordner des Verzeichnisses
scripts/        die Helfer, die Claude ausführt: Datenabruf (Gate 1), Bereinigen (Gate 2),
                Websites lesen und Anreicherung prüfen (Gate 3), Stadttextprüfer und Textgate
                (Gate 5), Live-Prüfung (Gate 6), Mail-Worker (nach dem Start)
skills/         seo-content-engine, die SEO-Schreib-Skill (prüft alle Texte, schreibt Ratgeber)
templates/      das Astro-Projekt, der Referenzbau (das fertige Beispiel und die Standardoptik),
                die beiden Formulare, die Preisstufen, der Mail-Worker
wiki/           das Regelwerk. konventionen.md zuerst, dann index.md
```
