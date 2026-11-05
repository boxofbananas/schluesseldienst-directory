# Ratgeber-Zahlen bereinigt, Zahlenprüfung gebaut, Mobil-Befunde behoben

**2026-11-05**

## Drei Zeilen, was ich selbst entschieden habe

1. **www bleibt NXDOMAIN, kein nacktes Record.** Das Token hat weiterhin kein
   Dynamic-Redirect-Recht (Rulesets-Endpunkt `403`, DNS-Aufrufe gehen). Ein www-Record
   ohne Weiterleitung erzeugte nur Doppelinhalt – schlechter als gar keins. Also nicht
   angelegt; der eine fehlende Dashboard-Klick steht unten.
2. **Mobil-Fixes gebaut und geprüft, aber noch nicht ausgeliefert.** Rein gestalterisch
   (CSS), kein Textinhalt. Nach der stehenden Regel „erst im Bericht nennen" liegen sie
   startbereit, aber ausgeliefert wird erst auf dein Wort (ein `wrangler`-Lauf).
3. **Erwartungswert 2807 war mein Fehler, nicht ein Fehler der Seite.** Die Live-Sitemap
   führt korrekt 2806 Seitenadressen; ich hatte den Selbstverweis der `sitemap-index.xml`
   mitgezählt. Alles andere in `check_live.py` ist grün.

---

## 1. Unbelegte Zahlen aus den Ratgeberseiten (erledigt, Commit ff4e70e)

Jede Zahl, die nicht mit Quelle und Abrufdatum in `05-fact-sheet.md` steht, ist raus. Die
betroffenen Stellen sind so umgeschrieben, dass sie mit den belegten Angaben auskommen –
keine vage Formulierung, die dieselbe Behauptung verschwommen weiterträgt, sondern der Satz
gestrichen oder auf das Belegte zurückgeführt.

**Belegt und geblieben** (die einzigen Geldzahlen, die noch vorkommen):
- Verbraucherzentrale: rund **100 €** tagsüber, rund **180 €** nachts/Wochenende/Feiertag,
  jeweils reines Öffnen ohne Schlosstausch.
- Stiftung Warentest: Spanne **65 bis 415 €** für eine einfache Türöffnung.

**Entfernt** (ohne belegte Quelle): die frei gegriffenen Einzelpreise (60/150/50/70/250 €,
83,30/88,50/125,70 €, 30/77/36/500 € u. a.), die Gerichts-Aktenzeichen (AG Lingen, AG Essen),
die „100 %"-Angabe, die Innungs-/Verbands-Einzelwerte und die als Prozent gekleideten
Behauptungen.

### Der Widerspruch „167,60–209,50" gegen „167,60/177,00", aufgeklärt

Beide Zahlenreihen waren **Innungs- bzw. Verbandsempfehlungen zu Sonn- und Feiertagspreisen**
– also eine Preisliste einer Handwerksinnung. Zwei Dinge dazu:

- **Keine zulässige Quelle.** Die Faktenregel in `wiki/konventionen.md` lässt nur
  Handwerkskammer, Stadt-/Gemeindeportale, Verbraucherzentrale, Polizeiliche
  Kriminalprävention und Stiftung Warentest zu. Innungs-Preislisten zählen ausdrücklich
  **nicht** dazu (sie stehen den ausgeschlossenen Branchenbüchern und
  Schlüsseldienst-Websites näher als einer amtlichen oder verbrauchernahen Quelle). Damit
  wäre die Angabe selbst dann draußen, wenn sie in sich stimmig wäre.
- **Die Unstimmigkeit beweist die Erfindung.** Für denselben Posten – Türöffnung am
  Sonntag – standen in zwei Ratgebertexten zwei verschiedene Werte (einmal eine Spanne
  167,60–209,50 €, einmal zwei feste 167,60/177,00 €). Eine echte, abgeschriebene Preisliste
  liefert für denselben Posten denselben Wert. Zwei verschiedene heißt: generiert, nicht
  belegt.

**Woher die Zahlen hätten stammen sollen:** aus einer belegten Quelle für Sonntagspreise –
die es in den zulässigen Quellen nicht gibt. Die Verbraucherzentrale nennt nur den groben
Rahmen (rund 180 € nachts/Wochenende/Feiertag), keine auf den Cent genauen Sonntagstarife.
Es gibt also keine belegte Zahl, die an diese Stelle gehört; richtig ist die Streichung und
der Rückgriff auf den VZ-Rahmen. Genau das steht jetzt dort.

Alle fünf Seiten bestehen das Textgate, auch die neue Zahlenprüfung (Punkt 2).

## 2. Zahlenprüfung gegen die Faktensammlung (erledigt, Commit ff4e70e)

Die Lehre aus dem Nachtlauf: **das Textgate prüft Wörter, nicht Tatsachen.** Eine erfundene
Zahl in flüssigem, floskelfreiem Deutsch kam ungehindert durch.

Gebaut, analog zur Stadttext-Prüfung, in `scripts/lint_copy.py` als Gate `zahlen_im_faktenblatt`:

- Jeder **Euro-Betrag, jede Prozentzahl, jede Jahreszahl und jedes Gerichts-/Aktenzeichen**
  einer Ratgeberseite muss sich als Zahl-Token in `05-fact-sheet.md` wiederfinden, sonst
  fällt die Seite durch. Spannen („65 bis 415") werden ganz aufgelöst, jede Zahl einzeln
  geprüft.
- **Kennungen sind ausgenommen**, weil sie keine Tatsachenbehauptung über Geld/Zeit sind:
  DIN-/EN-/RC-Normnummern, mm-Maße, die Notrufnummern 112/110, KfW-Programmnummern.
- Aufruf: `lint_copy.py … --facts output/<slug>/05-fact-sheet.md`. Nur für Ratgeberseiten;
  Stadttexte, Eintragsbeschreibungen und Startseite laufen ohne `--facts` (Abschnitt 2b in
  `wiki/seo/copy-gate.md`).

Gegen die korrigierten Seiten gelaufen: alle fünf **bestanden**. CLAUDE.md (Gate 5) und
`copy-gate.md` sind entsprechend ergänzt.

## 3. Die vier Mobil-Befunde (gebaut und geprüft, nicht ausgeliefert)

Alle in `output/schluesseldienste-deutschland/site/src/styles/global.css`. Bei 390 px neu
gemessen (Playwright, Chrome, `isMobile`), danach Screenshots.

| # | Befund | Fix | Nachgemessen |
|---|--------|-----|--------------|
| 1 | Tippflächen unter 44 px (Navigation, Fußzeile, Checkbox) | Logo/Nav/Breadcrumb/Fuß-Listenlinks `min-height:44px` über `inline-flex`; Rechtslinks über Innenabstand; Checkbox-Label füllt die Zeile, Kästchen 22 px statt 13 px | logo 44, nav 44, crumb 44, Fuß-Liste 44, Rechtslinks 48, Checkbox-Label 355×59 |
| 2 | Ratgeber-Überlauf durch nackte Quell-URLs | `.prose a { overflow-wrap: anywhere }` – die URL bricht um, die Seite dehnt sich nicht | Ratgeber scrollWidth 510 → **390** |
| 3 | Startseiten-Band rechts abgeschnitten (28 px über) | `white-space:nowrap` vom Band-Listenpunkt entfernt, der lange Satz bricht jetzt um | Startseite scrollWidth 418 → **390** |
| 4 | Premium-Preiskarte, rechter Rand fehlt | Button ist gestreckter Flex-Child; `max-width:calc(100% - 3rem)` deckelt ihn auf die Breite zwischen den 1,5-rem-Rändern | Premium scrollWidth 390, Button symmetrisch im Kartenkörper |

**Kein horizontaler Überlauf mehr** auf Startseite, Premium, Antrag, Ratgeber, Mannheim
(alle scrollWidth = 390). Die Schrift ist nirgends gewachsen, nur die Trefferfläche.

Inline-Textlinks im Fließtext (Byline „DOM Holding GmbH", E-Mail in einem Satz) bleiben unter
44 px – WCAG 2.5.5 nimmt Links im laufenden Text ausdrücklich aus; sie 44 px hoch zu machen
würde den Textfluss zerreißen.

Neue Aufnahmen in `berichte/screenshots/mobil/`: `nach-01-startseite.png`,
`nach-02-antragsformular.png`, `nach-03-premium.png`, `nach-04-ratgeber.png` (ganze Seite)
sowie `foldn-*.png` (erster Bildschirm).

`npm run build` läuft ohne Warnung durch (4628 Seiten, Glyph-Prüfung bestanden).

## Domain / www

Unverändert zum Lauf vom 05.11.: Apex lebt (CNAME → pages.dev, proxied), TLS gültig bis
03.02.2027, pages.dev sendet `noindex`. www fehlt weiterhin, und zwar bewusst: die dauerhafte
Weiterleitung www → Hauptdomain braucht **Zone → Dynamic Redirect → Edit** auf dem Token,
das der Token nicht hat (`http_request_dynamic_redirect`-Endpunkt: `403`). Sobald du das
Recht setzt, lege ich www-Record und 308-Weiterleitung an und prüfe erneut vollständig.

## check_live.py (Live-Domain)

Bis auf die zwei oben erklärten Zeilen (mein Erwartungswert 2807 statt 2806; www-Weiterleitung)
alles **BESTANDEN**: 200 + H1 + `lang="de"` + canonical auf der Startseite, Impressum und
Datenschutz vollständig und im Fuß verlinkt, Datenschutz lädt keine Google-Karte, `/verzeichnis/`
`noindex, follow`, Eintrags-/Stadt-/Bundesland-Seite indexierbar, `/premium/` und
`/eintrag-beanspruchen/` `noindex`, robots.txt mit Sitemap, alle Sitemap-Adressen auf die
Hauptdomain, unbekannte Adresse 404, `featuredPreview` false.

## Nicht angefasst

Sitemap nicht eingereicht, keine Suchmaschine angemeldet, keine Indexierung gestartet;
Garantie-Daten der eigenen Betriebe, Stripe, Sortierung, Rückport ins Template – alles
unberührt. Mobil-Fixes gebaut, aber nicht ausgeliefert.

## Offen für dich

- **Mobil-Fixes ausliefern?** Ein Wort, dann `npx wrangler pages deploy dist`.
- **Token-Recht Dynamic Redirect** setzen, dann hole ich www nach.
