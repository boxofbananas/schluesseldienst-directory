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
| **Premium-Eintrag** | **97 € im Jahr** | der ausgebaute Eintragszustand: Fotos vom Inhaber, alle Links gefolgt, Karte nach Klick, Öffnungszeiten, dazu das Siegelbild zum Einbinden, wenn der Betrieb geprüft ist | `premium` = `true` | {{STRIPE_LINK_PREMIUM}} |
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
- **Das Siegel ist keine Stufe und nicht kaufbar. Bezahlt wird nur Sichtbarkeit.** Dieser Satz
  steht auf `/premium/` und auf `/siegel/`. Das Siegel ist kostenlos und wird nach den sechs
  veröffentlichten Kriterien erteilt (`wiki/framework/siegel-programm.md`). Ein zahlender
  Betrieb ohne erfüllte Kriterien bekommt kein Siegel; ein geprüfter Betrieb ohne Zahlung
  behält es.

## Das Siegel zum Einbinden

Gate 5 erzeugt das Bild `/auszeichnung/[slug].svg` und die Nachweisseite
`/auszeichnung/[slug]/`, auf der dieses Schnipsel zum Kopieren steht. **Nur für geprüfte
Betriebe**, unabhängig davon, ob sie eine Stufe bezahlt haben.

```html
<a href="https://{{DOMAIN}}/firma/{{BUNDESLAND}}/{{STADT}}/{{SLUG}}/" rel="noopener">
  <img src="https://{{DOMAIN}}/auszeichnung/{{SLUG}}.svg"
       alt="{{FIRMENNAME}} ist bei Die besten Schlüsseldienste geprüft {{JAHR}}"
       width="180" height="60">
</a>
```

Beispiel mit eingesetzten Werten:

```html
<a href="https://die-besten-schluesseldienste.de/firma/baden-wuerttemberg/mannheim/merz-sicherheit-mannheim/" rel="noopener">
  <img src="https://die-besten-schluesseldienste.de/auszeichnung/merz-sicherheit-mannheim.svg"
       alt="Merz Sicherheit ist bei Die besten Schlüsseldienste geprüft 2026"
       width="180" height="60">
</a>
```

**Text auf dem Siegelbild:** `Geprüft 2026` als große Zeile, darunter
`Die besten Schlüsseldienste` als kleine. Die Jahreszahl ist das Jahr aus der Spalte
`geprueft_jahr` und steht immer darauf: das Siegel gilt ein Jahr und wird jährlich erneuert.

**Was nicht auf dem Siegel und nicht im Alternativtext steht:** „lizenziert", „zugelassen",
„zertifiziert", „Meisterbetrieb", „Innung", „Verband", „Kammer", „amtlich",
„Verbraucherschutz", „getestet", „TÜV", „Testsieger". Schlüsseldienst ist in Deutschland kein
zulassungspflichtiges Handwerk, und das Siegel ist die eigene Auszeichnung des Verzeichnisses,
keine Prüfung einer amtlichen Stelle (`wiki/konventionen.md`).

**Als HTML weitergeben, nie als Bilddatei.** Der Zweck ist der Link von der Website des
Betriebs auf seine Eintragsseite. Der Satz, der funktioniert: „Schicken Sie das Ihrem
Webmaster, oder wir bauen es für Sie ein." Den Einbau anbieten. Eine per E-Mail versandte
Bilddatei erzeugt keinen Link.
