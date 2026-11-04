---
title: Morgenbericht – Nachtlauf 03./04.11.2026
type: bericht
status: fertig
updated: 2026-11-04
---

# Morgenbericht

**Selbst entschieden (1):** Die fünf Ratgeberseiten **nicht** mit der seo-content-engine-Skill
geschrieben, sondern aus den im Regelwerk vorgeschriebenen Quellen – ihr Skill-Ablauf stützt sich
auf eine Wettbewerbs-/SERP-Analyse, also auf andere Schlüsseldienst-Websites, die Gate 5 als Quelle
ausschließt. Die Skill hat nur geprüft (Linter), nicht geschrieben.
**Selbst entschieden (2):** Alle fünf Seiten geschrieben – der Probelauf lag weit unter 10 $/Seite,
externe Kosten blieben bei **0 $** (keine bezahlte API), also keine Rückfrage nötig.
**Selbst entschieden (3):** Die von den Schreib-Agenten falsch auf **2026-11-05** (morgen) gesetzten
Abruf- und Veröffentlichungsdaten auf das echte Datum **2026-11-04** korrigiert.

Alle sieben Punkte sind erledigt. Nichts kostet Geld über der Grenze, nichts ist unumkehrbar; jede
Entscheidung lässt sich durch Ändern der CSV bzw. der Dateien und einen Neubau zurücknehmen.

---

## 1. Schweizer Grenzorte
**Erledigt.** Allschwil, Arlesheim, Oberwil, Riehen, Siegershausen unter derselben Regel wie Basel
nach `04-exclusions.csv` gedroppt (Grund: „Ausland (Schweiz); Verzeichnis ist für Deutschland").
Gegenprobe gemacht: **kein** weiterer Ort außerhalb eines deutschen Bundeslands blieb übrig.
Betroffene Stadttexte neu erzeugt. Datenstand jetzt **3.800 Einträge / 787 Stadtseiten / 16
Bundesländer**.

## 2. Impressum (USt-IdNr., Telefon)
**Erledigt, als entschieden festgehalten – kein offener Blocker mehr.** Beide Felder bleiben leer
(keine USt-IdNr. erteilt; § 5 DDG lässt die E-Mail als Kontakt genügen), die Seite lässt die Zeilen
weg. Im Build-Bericht steht das jetzt als entschiedene Sache, nicht als Startsperre.

## 3. Formularannahme
**Erledigt.** Cloudflare Pages Function `site/functions/api/claim.ts` nach deiner Spezifikation:
Honeypot + IP-Ratelimit, Feld-Whitelist, KV-Ablage mit 90 Tagen TTL und lesbarem Schlüssel,
Benachrichtigung ans Betreiber-Postfach, Art.-13-Hinweis auf beiden Formularen,
Wiedervorlage-Zeile, 303-Weiterleitung. `contact.formEndpoint` steht auf `/api/claim` – die harte
PFLICHT-Sperre ist damit weg. **Deine Cloudflare-Klicks** (KV-Namespace `EINSENDUNGEN` anlegen +
binden, Email-Routing-Zieladresse `info@die-besten-schluesseldienste.de` verifizieren +
`send_email`-Bindung `SEB`) stehen im Build-Bericht unter „Was du in Cloudflare tun musst".

## 4. Linkcheck
**Erledigt, sauber.** Vollständiger Lauf über alle gebauten Seiten: **0 gebrochene interne Ziele,
0 leere `href`, keine Verlinkung auf eine `noindex`-Seite in der Sitemap.**

## 5. Screenshots
**Erledigt (das Wichtigste für den Morgen).** 12 Seiten je in **1440 px und 390 px** (Playwright +
System-Chrome, kein Browser-Download) unter `berichte/screenshots/`: Startseite, Bundesland
(Baden-Württemberg), Mannheim, kleine Ortsseite (Tuttlingen), Eintrag **mit** und **ohne**
Festpreis-Garantie, Leistungsseite (Einbruchschutz), `/festpreis-garantie/`, `/premium/`, Impressum,
Datenschutz, 404. Schau am besten zuerst `startseite-1440.png`, `stadt-mannheim-1440.png` und
`eintrag-mit-garantie-1440.png` an.

## 6. Textgate
**Erledigt, bestanden.** `lint_copy.py` auf Startseite, alle Bundesland-Seiten und „Über uns" –
alle bestanden. Stadttext-Gate `check_city_copy.py`: 787/787 bestanden, 0 Datenzahlen.

## 7. Ratgeberseiten
**Erledigt, alle fünf durch das Textgate** (`--erlaube-rechtswoerter`, da sie die Rechtslage und
Preise behandeln):

| Seite | Wörter | Quellen |
|---|---|---|
| Was kostet ein Schlüsseldienst? | ≈ 990 | Verbraucherzentrale, Stiftung Warentest, ZDH |
| Ausgesperrt: Was Sie jetzt tun sollten | ≈ 970 | Verbraucherzentrale, Stiftung Warentest, Polizei, Stadt München |
| Unseriöse Schlüsseldienste erkennen | ≈ 1.094 | Verbraucherzentrale, Stiftung Warentest, Handwerkskammer, Polizei |
| Schloss austauschen | ≈ 886 | Stiftung Warentest, Verbraucherzentrale, k-einbruch |
| Türen nachrüsten: Einbruchschutz ohne Umbau | ≈ 995 | Polizei / k-einbruch |

Nur zugelassene Quellen (Verbraucherzentrale, Stiftung Warentest, Polizeiliche Kriminalprävention /
k-einbruch.de, Handwerkskammer, kommunale Notrufseite). Keine anderen Schlüsseldienst-Websites,
keine Branchenbücher, keine Presseportale. „Unseriöse erkennen" nennt bewusst keinen einzelnen
Betrieb, nur Muster. Alle Quellen mit Abrufdatum in `05-fact-sheet.md` und je Seite unter „Quellen".
Kosten: **0 $** extern, weit unter der 40-$-Grenze.

Kleine handwerkliche Entscheidung: der Türen-nachrüsten-Seite habe ich einen Einleitungsabsatz
vorangestellt, der den Bezug zum Schlüsseldienst herstellt – sonst wäre sie am Textgate-Check
„Branche im ersten Absatz" gescheitert.

---

## Nicht angefasst (wie angewiesen)
Stripe-Zahlungslinks (brauchen dein Konto), die anwaltliche Prüfung, Welle 2, die
Cloudflare-Auslieferung.

## Stand
Build grün: **4.629 Seiten**, keine Fehler. Vollständiger Stand in `output/schluesseldienste-
deutschland/05-build-report.md`.
