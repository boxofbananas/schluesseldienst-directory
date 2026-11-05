# Stripe-Vorbereitung: /danke/-Seite und Brutto-Preise mit USt.-Ausweis

**2026-11-05**

## Drei Zeilen

1. **/danke/** gebaut: noindex, nicht in Sitemap, nicht im Fuß verlinkt — bereit als
   Stripe-Weiterleitungsziel.
2. **Preise sind jetzt Brutto:** „inkl. 19 % USt." steht überall, wo ein Stufenpreis erscheint;
   zwei alte Netto-Sätze auf Brutto gedreht; B2B-Verkaufsbeschränkung in den AGB ausdrücklich.
3. **Ausgeliefert** (Daniel hatte das Ausliefern in dieser Runde freigegeben), live bei 1440 und
   390 px geprüft. Die drei Stripe-Zahlungslinks und ihre Eintragung kommen später von Daniel —
   nichts davon vorbereitet.

## 1. Dankeseite /danke/

`src/pages/danke.astro`: kurz und freundlich, bestätigt den Zahlungseingang und kündigt an, dass
sich DOM Holding GmbH innerhalb eines Werktags per E-Mail meldet, um den Platz freizuschalten und
den Eintrag umzustellen. `noindex`, **nicht** im Fußbereich verlinkt. Zur Sitemap-Ausnahme musste
`/danke/` in `src/lib/load.mjs` zu `noindexPaths` — sonst setzt die Seite zwar das `noindex`-Meta,
bleibt aber in der Sitemap (das Meta und der Sitemap-Filter sind zwei getrennte Wege). Danach:
nicht in der Sitemap (2806 unverändert), kein Überlauf bei 390 px. Screenshot
`berichte/screenshots/mobil/danke-390.png`.

Später, mit den Stripe-Links: `/danke/` als `success_url` der Zahlungen eintragen.

## 2. Brutto-Preise mit „inkl. 19 % USt."

**Eine Preisquelle.** Der USt.-Hinweis liegt als Datenfeld `tiers.vatNote` in `site.json`
(„inkl. 19 % USt.") und wird von dort gerendert:
- **/premium/** — gedämpfte Unterzeile `.price-vat` unter jedem der drei Preise (auch lesbar auf
  dem goldenen Kopf der Stadt-Stufe).
- **Premium-Band** — gedämpfte Zeile `.slot-vat` in der freien Karte; die Fußzeile zeigt
  „… · ab 29 € im Monat · inkl. 19 % USt." und darf auf dem Handy umbrechen (Fußnote, in Ordnung).

**Zwei Netto-Stellen auf Brutto gedreht** (sie widersprachen der Entscheidung, waren also mehr als
eine Ergänzung):
- `/premium/`, Abschnitt „Preise und Vertragspartner".
- AGB **B3**.

Neuer Satz an beiden: „Alle Preise sind Bruttopreise und enthalten die gesetzliche Umsatzsteuer
von 19 %." Das alte „zuzüglich der gesetzlichen Umsatzsteuer" kommt nirgends mehr vor.

**AGB — B2B-Vorbehalt ausdrücklich.** Nicht neu erfunden; der bestehende Satz in Teil B lautet
jetzt: „Die bezahlten Einträge und Werbeplätze werden ausschließlich an Unternehmer verkauft; ein
Angebot an Verbraucher oder ein Vertragsschluss mit ihnen besteht nicht."

**Eintragsseiten — bewusst kein Preis** (deine Entscheidung, Option 1). Sie nennen keinen
Stufenpreis, nur das Abzeichen und den Kasten „Ist das Ihr Betrieb?" mit Link auf /premium/. Die
Begründung steht im Wiki (`monetization-slots.md`, neue Sektion „Preise stehen nur auf /premium/"):
eine Preisquelle; die Eintragsseite wendet sich an Suchende, nicht an Käufer; weniger Preisstellen
veralten weniger. (Die Garantie-Preise auf der Eintragsseite sind die Türöffnungs-Preise des
Betriebs, kein Stufenpreis, von der USt.-Frage nicht berührt.)

## Geprüft

`npm run build` ohne Warnung (4629 Seiten). Live bei 1440 und 390 px: kein horizontaler Überlauf,
drei USt.-Zeilen je Ansicht, Brutto-Satz und B2B-Satz vorhanden. Screenshots
`berichte/screenshots/premium-live-1440.png` und `berichte/screenshots/mobil/premium-live-390.png`.

## Offen für Daniel

- **Drei Stripe-Zahlungslinks.** Sobald sie da sind: in `site.json` bei `tiers.premium/bestOf/city`
  statt der `STRIPE_LINK_*`-Platzhalter eintragen, `/danke/` als Weiterleitungsziel setzen, neu
  bauen und ausliefern. Nicht vorbereitet, wie gewünscht.
- **www-Weiterleitung** weiter offen (Token ohne Dynamic-Redirect-Recht), unverändert.
