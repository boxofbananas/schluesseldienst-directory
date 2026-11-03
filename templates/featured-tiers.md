# Preisstufen

Die Preise dieses Verzeichnisses. Nach einer Zahlung die Spalte setzen, neu bauen, ausliefern
(`wiki/framework/monetization-slots.md`).

**Die Spaltenwerte sind englisch, weil der Code sie englisch liest.** `featured` kennt genau
drei Werte: `city`, `county`, `state` (`templates/astro/src/lib/load.mjs`, `isFeaturedIn`). Ein
deutscher Wert wie `stadt` steht in keiner Abfrage: der bezahlte Platz erscheint dann nirgends,
und das fällt erst dem Kunden auf. Dasselbe gilt für die Namen der Zahlungslinks: maßgeblich ist
`templates/astro/src/data/site.json` → `tiers` mit `STRIPE_LINK_PREMIUM`, `STRIPE_LINK_CITY` und
`STRIPE_LINK_BESTOF`.

**Schreibweise der Stufennamen** (eine, überall): **Premium-Eintrag**, **Stadt-Premium**,
**Top-Platzierung**, dazu **Landkreis-Premium** und **Bundesland-Premium** als später zu
aktivierende Stufen. „Premium-Platz" ist kein Stufenname, sondern die allgemeine Bezeichnung für
einen bezahlten Platz aus der Wortliste in `wiki/konventionen.md` (englisch *featured listing*);
so steht sie auch auf den Schaltflächen der Site.

## Stufen, die verkauft werden

| Stufe | Preis | Platzierung | Spalte | Zahlungslink |
|---|---|---|---|---|
| **Premium-Eintrag** | **97 € im Jahr** | der ausgebaute Eintragszustand: Fotos vom Inhaber, alle Links gefolgt, Karte nach Klick, Öffnungszeiten, dazu nichts aus dem Garantie-Programm: der Garantie-Nachweis gehört zu keiner Stufe | `premium` = `true` | {{STRIPE_LINK_PREMIUM}} |
| **Stadt-Premium** | **29 € im Monat** | oberste Karte auf einer Stadtseite, gefolgter Link, Foto | `featured` = `city` | {{STRIPE_LINK_CITY}} |
| **Top-Platzierung** | **250 € einmalig** | fester Platz in der Liste „Die besten Schlüsseldienste in [Stadt]", dazu eine Pressemitteilung über den Betrieb, deren drei Links auf seine Website, seine Eintragsseite und die Stadtseite gehen | `best_of_rank` = `1` bis `3` | {{STRIPE_LINK_BESTOF}} |

## Stufen, die später zu aktivieren sind

Die Felder stehen im Template, aber diese Stufen werden **nicht verkauft, bevor in mehreren
Städten ein Stadt-Premium verkauft ist**. Ohne verkaufte Stadtplätze gibt es keinen Preis, der
sich begründen lässt, und eine Landkreis-Stufe ohne gefüllte Stadtplätze verkauft Reichweite,
die es noch nicht gibt.

| Stufe | Platzierung | Spalte |
|---|---|---|
| Landkreis-Premium | oberste Karte auf allen Stadtseiten eines Landkreises | `featured` = `county`, dazu `featured_cities` |
| Bundesland-Premium | Block auf der Bundesland-Seite plus alle Stadtseiten des Landes | `featured` = `state` |

Preis für beide: offen. Wird festgelegt, wenn die erste Nachfrage kommt, aus den dann
bekannten Zahlen (Besucher der Bundesland-Seite, Zahl der Städte im Landkreis), nicht vorher
geraten.

## Regeln

- **Je Stadt und Stufe ein Betrieb.**
- **Je Stadt höchstens ein eigener Betrieb auf einem bezahlten Platz**
  (`wiki/framework/footprint-rules.md`). Merz Sicherheit in Mannheim hat Premium-Eintrag und
  Top-Platzierung zum Preis dieser Tabelle; damit ist der Platz in Mannheim belegt.
- Verkauft wird von Hand: Zahlungslink senden, nach der Zahlung die Spalte setzen, Gate 5
  erneut laufen lassen, ausliefern. Kündigung heißt Spalte leeren und neu bauen.
- Preise in Euro mit Komma und Euro-Zeichen dahinter: `97 €`, `29 €`, `250 €`. Auf `/premium/`
  steht, ob brutto oder netto, und dieselbe Angabe steht in den AGB.
- **Die Festpreis-Garantie ist keine Stufe und nicht kaufbar. Bezahlt wird nur Sichtbarkeit.**
  Dieser Satz steht auf `/premium/` und auf `/festpreis-garantie/`. Die Garantie ist kostenlos
  und wird nach den sechs veröffentlichten Voraussetzungen erteilt
  (`wiki/framework/siegel-programm.md`). Ein zahlender Betrieb ohne erfüllte Voraussetzungen
  bekommt keine Garantie; ein Betrieb mit Garantie ohne Zahlung behält sie.

## Der Garantie-Nachweis zum Einbinden

**Der Garantie-Nachweis ist kostenlos und gehört zu keiner Stufe.** Er steht jedem Betrieb mit
Festpreis-Garantie zu, ob er eine Stufe bezahlt hat oder nicht, und keine Stufe bringt ihn mit.
Gate 5 erzeugt das Bild `/auszeichnung/[slug].svg` und die Nachweisseite
`/auszeichnung/[slug]/`, auf der dieses Schnipsel zum Kopieren steht. **Nur für Betriebe mit
Garantie** (`geprueft` = `true` und die drei Preise gesetzt).

```html
<a href="https://{{DOMAIN}}/firma/{{BUNDESLAND}}/{{STADT}}/{{SLUG}}/" rel="noopener">
  <img src="https://{{DOMAIN}}/auszeichnung/{{SLUG}}.svg"
       alt="{{FIRMENNAME}}: Festpreis-Garantie {{JAHR}} bei Die besten Schlüsseldienste, Türöffnung ab {{GARANTIE_TAG}} €"
       width="180" height="60">
</a>
```

Beispiel mit eingesetzten Werten:

```html
<a href="https://die-besten-schluesseldienste.de/firma/baden-wuerttemberg/mannheim/merz-sicherheit-mannheim/" rel="noopener">
  <img src="https://die-besten-schluesseldienste.de/auszeichnung/merz-sicherheit-mannheim.svg"
       alt="Merz Sicherheit: Festpreis-Garantie 2026 bei Die besten Schlüsseldienste, Türöffnung ab 89 €"
       width="180" height="60">
</a>
```

**Text auf dem Bild:** `Festpreis-Garantie {{JAHR}} · Türöffnung ab {{GARANTIE_TAG}} €` als
große Zeile, darunter `Die besten Schlüsseldienste` als kleine. Die Jahreszahl ist das Jahr aus
der Spalte `geprueft_jahr`, der Betrag ist die Spalte `garantie_tag`; beides steht immer
darauf: die Garantie gilt ein Jahr und wird jährlich erneuert, und der Preis ist der Kern der
Garantie. Der Link führt auf die Eintragsseite, wo alle drei Preise stehen.

**Was nicht auf dem Bild und nicht im Alternativtext steht:** „lizenziert", „zugelassen",
„zertifiziert", „Meisterbetrieb", „Innung", „Verband", „Kammer", „amtlich",
„Verbraucherschutz", „getestet", „TÜV", „Testsieger", „geprüft". Schlüsseldienst ist in
Deutschland kein zulassungspflichtiges Handwerk, und die Festpreis-Garantie ist ein Versprechen
des Betriebs, das der Herausgeber veröffentlicht und überwacht, keine Prüfung einer amtlichen
Stelle (`wiki/konventionen.md`).

**Als HTML weitergeben, nie als Bilddatei.** Der Zweck ist der Link von der Website des
Betriebs auf seine Eintragsseite. Der Satz, der funktioniert: „Schicken Sie das Ihrem
Webmaster, oder wir bauen es für Sie ein." Den Einbau anbieten. Eine per E-Mail versandte
Bilddatei erzeugt keinen Link.
