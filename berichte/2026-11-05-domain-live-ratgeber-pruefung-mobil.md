---
title: Domain live (Apex), Ratgeber-Prüfung, Mobil-Durchsicht, .gitignore
type: bericht
status: teilweise (www-Weiterleitung wartet auf ein Token-Recht; Ratgeber-Änderungen vorgelegt, nicht ausgeführt)
updated: 2026-11-05
---

# Langer Lauf ohne Rückfragen — vier Punkte

**Selbst entschieden (drei Zeilen):**
1. **www-Weiterleitung nicht gebaut.** Der Token hat DNS:Edit, aber **kein** Rules-Recht; ein
   www-DNS-Eintrag ohne Redirect-Regel hätte 404 geliefert — schlimmer als nichts. Also www
   **gar nicht** angelegt (bleibt sauberes NXDOMAIN) und genau dokumentiert, welches Recht fehlt.
2. **Ratgeber-Preiszahlen als unbelegt eingestuft, aber nichts geändert.** Die fünf Seiten
   nennen viele konkrete Euro-Beträge und Gerichts-/Innungsangaben, die **nicht** in
   `05-fact-sheet.md` stehen. Ich lege sie zur Entscheidung vor (löschen oder Faktenblatt
   nachziehen), wie gewünscht ohne Eingriff.
3. **Mobil bei 390 px gemessen und selbst angesehen.** Kleine Ortsseite = Tuttlingen,
   Leistungsseite = Türöffnung gewählt. Screenshots (10 Vollseiten + 5 lesbare Ausschnitte,
   22 MB) liegen unter `berichte/screenshots/mobil/`.

Kein Seiteninhalt ausgeliefert. Geändert wurde nur Cloudflare-DNS (Punkt 1, ausdrücklich
freigegeben) und `.gitignore` (Punkt 4).

---

## 1. Domain — Apex ist live, www wartet auf ein Token-Recht

**Erledigt:**
- Token geprüft: authentifiziert, Zone `die-besten-schluesseldienste.de` ist `active`
  (Zone-ID `36844d2e…`). DNS:Edit bestätigt (Schreibzugriff funktioniert). Der
  `/user/tokens/verify`-Endpunkt meldet „Invalid API Token" — bekannte Eigenart
  kontoskopierter Token, nicht blockierend, da Zonen- und DNS-Aufrufe durchgehen.
- **Apex-CNAME angelegt:** `die-besten-schluesseldienste.de` → `schluesseldienste-deutschland.pages.dev`,
  **proxied** (CNAME-Flattening am Apex). Record-ID `55756cd6…`.
- **Ergebnis:** Die Domain springt von „CNAME record not set" auf **aktiv**. Apex liefert
  **HTTP 200 über HTTP/2**, **TLS-Zertifikat gültig bis 01.02.2027**, unsere eigenen Header
  (`referrer-policy`, `x-content-type-options`) — also unsere Pages-Site, kein Platzhalter.
- **`check_live.py` gegen die echte Domain gelaufen** (`--pages-dev … --expect-urls 2806`):
  **alle Prüfungen bestanden außer der www-Weiterleitung** — Startseite 200/H1/`lang=de`/canonical/
  nicht-noindex, kein `featuredPreview`, Impressum+Datenschutz im Fuß, 404 für Unbekanntes,
  robots.txt nennt Sitemap, Sitemap-Index mit 1 Teil, **2806 Adressen, alle auf die Hauptdomain
  (kein `pages.dev`)**, Eintrags-/Stadt-/Bundesland-Seite indexierbar, `/verzeichnis/` noindex/follow,
  `/eintrag-beanspruchen/` und `/premium/` noindex, pages.dev sendet `X-Robots-Tag: noindex`.

**Nicht gebaut — www-Weiterleitung (fehlt ein Token-Recht):**
- Eine dauerhafte Umleitung `www → Apex` braucht eine **Single-Redirect-Regel** (Rulesets-Phase
  `http_request_dynamic_redirect`). Der Token darf Rulesets **nicht** lesen/schreiben
  („Authentication error" bei der Rechteprobe). DNS allein kann nicht 301 umleiten.
- Einen www-DNS-Eintrag **ohne** Regel habe ich bewusst **nicht** angelegt: www würde dann auf
  die Pages-Fläche zeigen, die für `www…` keinen Custom-Domain-Eintrag hat → **404**. Der jetzige
  Zustand (www = NXDOMAIN, löst gar nicht auf) ist sauberer als ein 404. `check_live.py` meldet
  hier folgerichtig „DURCHGEFALLEN: www leitet dauerhaft um" — das ist der einzige offene Punkt.
- **Was Daniel braucht — eines von beiden:**
  1. **Token erweitern** um **Zone → Dynamic Redirect → Bearbeiten** (für die Redirect-Regel).
     Dann lege ich in einem Zug den proxied www-Eintrag **und** die 301/308-Regel an und
     `check_live.py` ist vollständig grün. (Mehr braucht es nicht; DNS:Edit habe ich schon.)
  2. **Oder ein Dashboard-Klick:** *Rules → Redirect Rules → Create rule → Vorlage „Redirect
     from WWW to Root"*; dazu unter *DNS* einen **proxied** `www`-Eintrag (CNAME `www` →
     `die-besten-schluesseldienste.de`, Orange-Cloud). Die Regel sendet 301 auf die Hauptdomain,
     Pfad und Query bleiben erhalten.

**Wie gewünscht nicht gemacht:** Sitemap einreichen, Suchmaschinen anmelden, Indexierung
starten. Das entscheidet Daniel nach der Anwaltsdurchsicht — auch wenn (bis auf www) alle
Prüfungen bestehen.

---

## 2. Die fünf Ratgeberseiten — gelesen, bewertet, Änderungen vorgelegt (nichts geändert)

**Der durchgehende Befund zuerst:** Die Seiten sind sprachlich gut und lesen sich menschlich,
aber sie **laufen dem Faktenblatt davon**. `05-fact-sheet.md` hält nur fünf Faktenblöcke fest
(keine Zulassung/Meisterpflicht; VZ Hamburg ~100 €/180 €; Einbruchschutz RC 2 / DIN EN 1627 /
DIN 18104 / KfW 159; Warentest-Spanne 65–415 €; Gewerbe/Handwerksrolle). Die Seiten nennen
**dutzende** weitere konkrete Zahlen und Rechtsangaben, die **dort nicht stehen** und sich
damit nicht gegen das Faktenblatt prüfen lassen. Nach der Projektregel („jede Aussage über
Recht, Gewerbe, Preise … mit Quelle und Abrufdatum im Faktenblatt") gelten sie als **unbelegt**,
auch wenn die Seiten im Fuß zulässige Quellen (VZ, Warentest, Polizei, HWK) nennen. Zwei Wege:
das Faktenblatt um **jede** Zahl mit Quelle+Datum ergänzen (und dabei jede Zahl an der Quelle
nachprüfen) — oder die nicht nachgeprüften Zahlen streichen/weicher fassen.

**Lizenz/Zulassung/Zertifizierung/Meisterpflicht:** Keine Seite behauptet so etwas. Seite 1
erklärt sogar ausdrücklich und korrekt, dass es **keine** Lizenz/Meisterpflicht gibt. (Eine
Nuance dort unten.) **Firmennamen:** keine Seite nennt einen Betrieb; Seite „Unseriöse …" sagt
das sogar ausdrücklich. **Bilder:** keine. **Gut.**

### Seite für Seite

**a) `was-kostet-ein-schluesseldienst` — am stärksten belastet.**
Bewertung: flüssig und praktisch, aber die preislich dichteste Seite. Nicht im Faktenblatt
belegt und zu prüfen/streichen: „60 bis 150 Euro je nach Bundesland" (VZ), „werktags 150 Euro
nicht überschreiten", RLP-Beispiel „50–100 / 70–250 Euro", „rund 112 Euro / Amtsgericht Lingen",
Innungssätze „83,30 / 88,50 Euro" und nachts „125,70 / 167,60 / 167,60–209,50 Euro", „Zuschläge
max. 100 %", „Sofort-/Bereitschafts-/Spezialwerkzeug-Zuschläge unzulässig", Zylinder „36 Euro
Zuschlag / 30 Euro Material / 300 statt 30 Euro", der ganze Versicherungsabschnitt (Hausrat,
Haftpflicht, Wohnungsschutzbrief). Nur „65 bis 415 Euro" steht im Faktenblatt.
Zusätzlich inhaltlich zu prüfen: Satz „gilt … **nicht als Handwerk** im Sinne der HwO" —
das Faktenblatt sagt, es sei ein **zulassungsfreies Handwerk bzw. handwerksähnliches Gewerbe
(Anlage B)**. Das ist ein feiner Widerspruch; die „Abgrenzungsleitfaden"-Aussage ist plausibel,
steht aber nicht im Faktenblatt.

**b) `ausgesperrt-was-tun` — stark, wenige Zahlen.**
Bewertung: der beste Ratgeber-Ton, klarer Ablauf (112 nur bei Gefahr, Zweitschlüssel zuerst).
Zu prüfen/belegen: „150 Euro werktags", „100 % Zuschlaggrenze", „Sofort-/Bereitschafts-/
Spezialwerkzeug unzulässig", „Amtsgericht Lingen ~112 Euro (76 + 36)", „Wucher = das Doppelte,
100 → 200 nichtig", „örtliche Vorwahl → nur Anfahrt im Ort". Die 112/Stadt-München-Angaben sind
über die gelistete Quelle gedeckt.

**c) `unserioese-schluesseldienste-erkennen` — gut, aber viele Fremdzahlen.**
Bewertung: sauber, nennt bewusst keine Firma. Zu prüfen/belegen: VZ-Umfrage „600 Dienste,
59,40–83,61 Euro", „nachts/Wochenende 75–100 Euro", „Praxisfall ~800 Euro", Innungssätze
„83,30 / 88,50 / 167,60 / 177,00 Euro", „89–119 / 235–415 Euro", „Amtsgericht Essen", „100 %",
„0800-Warnung". **Interner Widerspruch zu Seite a:** Sonntagssatz hier „167,60 bzw. 177,00",
auf Seite a „167,60–209,50" — ein Zeichen, dass diese Zahlen nicht aus einer festgehaltenen
Quelle transkribiert wurden.

**d) `schloss-austauschen` — solide, DIN-lastig.**
Bewertung: gut gegliederter Ablauf (Ausmessen, Normprofil, Tausch). Zu prüfen/belegen:
„30 Euro / Testsieger 77 Euro", „36 Euro Zuschlag", „Berliner Fall ~500 Euro Material",
„150 Euro werktags"; DIN 18252/18257/18251 (Klassen) stehen **nicht** im Faktenblatt (dort nur
DIN EN 1627 / DIN 18104).

**e) `tueren-nachruesten-einbruchschutz` — am besten belegt.**
Bewertung: durchgehend an Polizei/K-EINBRUCH gebunden, **keine Preise**. DIN EN 1627 (RC 2),
DIN 18104 Teil 1/2, KfW 159 und 455-E stehen im Faktenblatt. Zusätzlich DIN 18252/18257/18251
und „3 mm Schließblech / Errichterverzeichnis" — Standard-K-EINBRUCH-Inhalt, aber nicht im
Faktenblatt notiert. Kein Lizenz-/Zertifizierungs-Anklang (das Errichterverzeichnis ist ein
Hinweis an Leser, keine Aussage über unsere Einträge).

### Schablonen über die fünf Seiten hinweg?
Einzeln lesen sie sich menschlich. **Über die Menge fällt Wiederholung auf:** der
Festpreis-Absatz („Vereinbaren Sie schon am Telefon einen Festpreis, der Anfahrt und mögliche
Zuschläge enthält") steht fast wörtlich auf a, b, c, d; der „zugefallene Tür / Druck /
erstbeste Nummer"-Einstieg auf a und c; „150 Euro werktags" auf a, b, d. Wer zwei Seiten liest,
erkennt dieselben Sätze. Mild, aber vor dem Start glätten.

### Empfehlung (zur Entscheidung, nicht ausgeführt)
Vor dem Scharfschalten der Ratgeber: entweder die Zahlen pro Seite an der jeweils genannten
Quelle nachprüfen und **mit Quelle+Datum ins Faktenblatt** heben — oder die nicht nachprüfbaren
Zahlen entfernen und auf die im Faktenblatt belegten Spannen zurückführen. Der interne
Sonntagssatz-Widerspruch (c vs a) zeigt, dass mindestens eine Zahl falsch transkribiert ist.

---

## 3. Mobil (390 px) — selbst angesehen

Methode: Alle zehn Seiten bei 390 px gerendert (`berichte/screenshots/mobil/01–10…png`,
Vollseite) und zusätzlich per DOM geprüft, *was* überläuft und welche Tippflächen zu klein sind;
die kritischen Stellen in lesbaren Ausschnitten (`f01/f05/f07/f08/f10…png`) nachgesehen.

**Echte Probleme:**
1. **Alle fünf Ratgeberseiten: horizontaler Überlauf (~120 px).** Die „Quellen"-Liste zeigt
   **nackte URLs als Links**, die nicht umbrechen (`https://www.verbraucherzentrale.de/…`, 388 px
   breit); sie schieben die Seite auf **510 px** → die ganze Seite lässt sich seitlich scrollen.
   Fix: `overflow-wrap: anywhere` / `word-break: break-word` auf `.prose a` bzw. die Quellen-Liste,
   oder Quellen als Linktext statt nackter URL. Datei: `10-ratgeber-kosten.png` (gilt für alle fünf).
2. **Startseite: horizontaler Überlauf (~28 px)** mit sichtbarem Symptom — der Band-Satz unter
   dem Hero („Festpreis-Garantie: Preise stehen im Eintrag, bevor Sie **anr**…") ist **rechts
   abgeschnitten**. Datei: `01-startseite.png`, `f01-startseite.png`.
3. **Premium: Preiskarten asymmetrisch/zu breit.** Linke Kante mit Rand, **rechte Kante bündig
   bzw. ~6 px über den Viewport**; `.card.tier` ist 403 px breit bei 355 px Inhalt, der Button
   „Verfügbarkeit anfragen" sitzt rechts bündig am Rand. Datei: `08-premium.png`, `f08-premium.png`.
4. **Tippflächen unter der Empfehlung (44–48 px).** Navigationslinks ~25 px hoch;
   Fußzeilen-/Rechtslinks (Impressum, Premium, AGB, Garantie-Antrag) ~17–19 px; die „ja"-Checkbox
   auf `/eintrag-beanspruchen/` nur **13×13 px**. Auf allen Seiten.

**Was gut aussieht (keine Probleme):**
- **Eintragsseite:** SVG-Sterne sauber (4,4), „Noch keine Festpreis-Garantie", Telefon im
  deutschen Format (`+49 7361 8096607`, bricht nicht um), Adresse umbricht sauber.
- **Festpreis-Garantie:** lesbar, kein Überlauf, Preisblock passt in 390 px.
- **Bundesland / Mannheim / Kleinort (Tuttlingen):** kein Überlauf; Breadcrumbs und Karten
  umbrechen sauber.
- **Keine quellenden Bilder** (kein `img` breiter als der Viewport — Einträge ohne Beanspruchung
  tragen keine Fotos). **Keine umbrechenden Zahlen** (Preise, Telefon, Bewertungen bleiben ganz).
- **Hinweis, kein Bug:** `/leistungen/tueroeffnung/` ist bei 390 px **~44.000 px hoch** (sehr
  viele Einträge auf einer Seite). Kein Überlauf, aber ein sehr langer Scroll — vielleicht später
  eine Kürzung/Blätterung erwägen.

Keine dieser Stellen wurde geändert (keine Inhalts-/Build-Änderung ohne Vorlage).

---

## 4. `.gitignore` — site.backup-* ausgenommen

`output/*/site.backup-*/` und `site.backup-*/` ergänzt, damit `init_site.py --force` im Ernstfall
keine Vollkopie des Builds ins Repo zieht. Erledigt und committet.

---

## Offen / wartet auf Daniel
- **www-Weiterleitung:** Token um *Zone → Dynamic Redirect → Bearbeiten* erweitern (dann baue ich
  www-Eintrag + 301-Regel), oder den Dashboard-Weg aus Punkt 1 gehen.
- **Ratgeber:** entscheiden, ob die unbelegten Zahlen ins Faktenblatt nachgezogen (und geprüft)
  oder gestrichen werden; dann baue ich um.
- **Mobil:** vier Fixes freigeben (URL-Umbruch Ratgeber, Hero-Band-Überlauf Startseite,
  Premium-Kartenrand, Tippflächen) — alles Stil/CSS, nichts an den Daten.
- Unverändert nicht angefasst: Garantie-Daten eigener Betriebe, Stripe, Sortierung, Rückport.
- Nicht gestartet (nach Anwaltsdurchsicht): Sitemap/Indexierung.
