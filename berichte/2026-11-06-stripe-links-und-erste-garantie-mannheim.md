# Stripe-Links eingetragen · erste Festpreis-Garantie (zwei Mannheimer Betriebe)

**Datum:** 2026-11-06
**Auslöser:** Daniel — die Zuordnung der drei Zahlungslinks steht fest, und die beiden
Mannheimer Betriebe bekommen die Festpreis-Garantie.

## 1. Stripe-Zahlungslinks in `site.json`

| Stufe (site.json) | Produkt | Preis | Link |
|---|---|---|---|
| `premium` | Premium-Eintrag | 97 € im Jahr | `https://buy.stripe.com/aFa5kE2lg1k85Nw7fm1VK02` |
| `bestOf` | Top-Platzierung | 250 € einmalig | `https://buy.stripe.com/00w5kEaRM8MA0tcary1VK00` |
| `city` | Stadt-Premium | 29 € im Monat | `https://buy.stripe.com/4gM8wQbVQe6U7VE6bi1VK01` |

Auf `/premium/` geprüft, Preis für Preis — kein vertauschter Link: 97 € → …1VK02, 250 €
→ …1VK00, 29 € → …1VK01. Live bestätigt.

### Für Daniel: die Weiterleitung auf `/danke/` setzt du in Stripe selbst
Pro Zahlungslink im Stripe-Dashboard:
**Payment Links → den Link öffnen → „After payment" (Nach der Zahlung) → „Confirmation page"
→ „Redirect customers to your website" wählen → URL eintragen:**
`https://die-besten-schluesseldienste.de/danke/`

Das ist eine Einstellung **am Zahlungslink**, nicht im Code und nicht an der Domain. Sie muss an
**allen drei** Links gesetzt werden. Die `/danke/`-Seite steht (noindex, nicht im Fuß verlinkt)
und ist als Ziel bereit.

## 2. Festpreis-Garantie für zwei Mannheimer Betriebe

`geprueft = true`, `geprueft_jahr = 2026`, für beide dieselben Preise:

| Feld | Wert |
|---|---|
| `garantie_tag` (Grundpreis werktags) | 89 € |
| `garantie_zuschlag_abend` | +30 € |
| `garantie_zuschlag_nacht` | +40 € |
| `garantie_anfahrt` | 0 € (im Preis enthalten) |
| `garantie_zylinder` | 39 € |
| `garantie_zylinder_5mm` | +3 € |

- **Merz Sicherheit** (owned, 5,0 aus 355 Bewertungen, Premium-Platz Stadt) — Voraussetzung 4
  über Bewertungen erfüllt.
- **AES Schlüsseldienst Mannheim** (owned, keine Bewertungen) — nach Voraussetzung 4
  entscheiden die übrigen Voraussetzungen; alle erfüllt.

Beide Eintragsseiten zeigen den vollständigen Preisblock (drei Gruppen, „Zuschläge werden nicht
addiert"). Beide Stadtkarten tragen „Festpreis-Garantie 2026 · Türöffnung ab 89 €" — live
geprüft (zweimal auf der Mannheimer Stadtseite).

### Nebenbefund behoben: der Premium-Band zeigte keine Garantie-Zeile
Merz ist der erste Betrieb, der zugleich einen **bezahlten Premium-Platz** (oben im Band) und
eine **Garantie** hat. Der `FeaturedBand` rendert die Garantie-Zeile bislang nicht — damit hätte
Merz die Garantie auf seiner Stadtkarte **nicht** angezeigt, obwohl die Regel sie „auf jeder
Stadtkarte eines Betriebs mit Garantie" verlangt (CLAUDE.md, `siegel-programm.md`). Behoben:
`<Garantie listing={l} mode="card" />` in `FeaturedBand.astro` eingefügt, wie in `Card.astro`.

Dabei fiel eine **Template-Drift** auf: die Template-Kopie des `FeaturedBand` war bei der
Brutto-Umstellung (Aufgabe B, 2026-11-05) nicht mitgezogen worden — ihr fehlten `vatNote` und
der `Star`-Glyph-Fix. Die Build-Fassung ist durchweg die neuere, allgemeine; ich habe das
Template auf sie gesetzt, sodass künftige Verzeichnisse `vatNote`, Stern-Glyph und Garantie-Zeile
mitbekommen.

## 3. Die Mannheimer Reihenfolge — folgt der Regel, nicht `owned`

Die Sortierregel (`sortListings` in `load.mjs`): **Rang 0** bezahlter Premium-Platz dieser Stadt
(`featured`), **Rang 1** bezahlte Top-Platzierung (`bestOfRank`), **Rang 2** Sortiermerkmal,
**Rang 3** Rest; innerhalb der Gruppe `score = rating × log10(reviews+1)`. `owned` wird
**nicht gelesen** (Kommentar in `load.mjs:426`), `geprueft` ist **kein** Sortierfaktor.

Mannheim, wie es jetzt steht:

- **Ganz oben im Premium-Band:** Merz Sicherheit (Abzeichen „Premium"). Oben, **weil es den
  bezahlten Stadt-Premium-Platz hält** — nicht weil es owned ist. Der Band nimmt die featured
  Einträge aus dem Raster heraus und zeigt sie zuvor.
- **Hauptraster, streng nach score absteigend:** Key Walter (11,95) → Schlüsseldienst-ATILLA
  (11,89) → Autoschlüssel Nachmachen (11,81) → … → **AES Schlüsseldienst Mannheim ganz unten
  (#18, score 0,00)**.

**AES ist owned und jetzt garantie-geprüft — und steht trotzdem letzter**, weil es keine
Bewertungen hat (score 0). Das ist der Beleg: weder `owned` noch die Garantie heben einen Eintrag;
Merz steht oben allein über den bezahlten Platz.

## Stand

Gebaut (4629 Seiten, Riegel grün), ausgeliefert, live geprüft: Premium-Links in richtiger
Zuordnung, Garantie-Block und -Zeile auf beiden Mannheimer Betrieben, `check_live.py` bestanden
**außer der www-Umleitung** (Token hat weiter kein Dynamic-Redirect-Recht — dein Schritt).

**Offen bei dir:** die `/danke/`-Weiterleitung an den drei Stripe-Links setzen (oben beschrieben),
und die www-Weiterleitung.
