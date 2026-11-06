---
title: Spalten der Eintrags-CSV (Outscraper-Layout)
type: framework
status: stable
updated: 2026-11-03
---

# Spalten der Eintrags-CSV

Die Spaltennamen sind englisch und bleiben es: beide Datenquellen liefern sie so, und die
Skripte lesen sie so. Nur die neuen Spalten dieser Fassung sind deutsch benannt. Geprüft gegen
outscraper.com/google-maps-scraper (Datenverzeichnis).

## Standardspalten

name, name_for_emails, subtypes, type, category, phone, website, address, street, county,
city, state, state_code, postal_code, country, country_code, latitude, longitude, h3,
time_zone, plus_code, area_service, rating, reviews, reviews_link, reviews_tags,
reviews_per_score, reviews_per_score_1 bis _5, photos_count, photo, street_view, logo,
located_in, located_google_id, business_status, working_hours, working_hours_csv_compatible,
other_hours, popular_times, typical_time_spent, range, prices, reservation_links,
booking_appointment_link, menu_link, order_links, about, description, posts, verified,
owner_id, owner_title, owner_link, location_link, location_reviews_link, place_id, google_id,
cid, kgmid, reviews_id

## Spalten der Anreicherungs-Erweiterung

domain, email_1 bis email_3, Facebook, Instagram, Twitter, Linkedin, Youtube, phone_1 bis
phone_3, website_title, website_generator, website_description, website_keywords,
website_has_fb_pixel, website_has_gtm

## Der DataForSEO-Weg schreibt dasselbe Layout

`scripts/fetch_dataforseo.py` bildet die Felder der Business Listings API auf diese
Spaltennamen ab, damit Gate 2 unverändert läuft: `title` auf name, `url` auf website,
`address_info` auf street, city, state, postal_code, `category` auf type und category,
`additional_categories` auf subtypes, `rating` auf rating und reviews,
`rating_distribution` auf reviews_per_score_1 bis _5, `place_topics` auf reviews_tags als
„Stichwort (Anzahl)", `attributes` (JSON) auf about, `work_time` auf working_hours,
`is_claimed` auf verified, `main_image` auf photo, `total_photos` auf photos_count,
`feature_id` auf google_id, `check_url` auf location_link. Zusätzliche Spalten: domain,
email_1 bis email_3, phone_1 bis phone_3, last_updated_time, source (`dataforseo`). Immer
leer: county, posts, area_service. `business_status` ist immer `OPERATIONAL`, weil die
Datenbank kein Merkmal für Geschäftsaufgabe trägt.

## Von der Verarbeitung benutzt

| Spalte | Wofür |
|---|---|
| name, phone, website, address, street, city, state, state_code, postal_code, latitude, longitude | Firmendaten, Slugs, Zuordnung zum Bundesland, Entfernungsrechnung für Nachbarstädte |
| type, subtypes, category | Branchenabgleich als Rückfall, Merkmalshinweise, **Aufschlüsselung der fremden Gewerbe im Gate-2-Bericht** |
| rating, reviews, reviews_per_score_* | Reihenfolge innerhalb einer Stadt, Kennzeichnung dünner Einträge, **Voraussetzung 4 der Festpreis-Garantie** (mindestens 10 Bewertungen bei mindestens 4,0) |
| reviews_tags, about, description, posts | Eingaben für das Anreichern; `description` ist der Text, den die Dünn-Kennzeichnung in Gate 2 liest |
| working_hours | Öffnungszeitenblock, `openingHoursSpecification` im Schema |
| business_status, verified | Bereinigen, Hinweis „auf Google bestätigt" |
| photo, logo | Eintragsbild (Einbinden ist nicht erlaubt: herunterladen oder weglassen) |
| place_id, google_id, cid, location_link | Entdoppelungsschlüssel, Kartenlink |
| area_service | Betriebe ohne Ladenanschrift (keine Straßenanschrift anzeigen) |

## Spalten, die diese Fassung hinzufügt

| Spalte | Von | Bedeutung |
|---|---|---|
| `slug`, `city_slug` | Gate 2 | Adressteile, Umlaute umgeschrieben ([[konventionen]]) |
| `state`, `state_code` | aus dem Abruf, von Gate 2 gefüllt | **die Zwischenebene Bundesland.** Spalten mit deutschem Namen gibt es nicht: `templates/astro/src/lib/load.mjs` leitet Name, Slug und Kürzel des Bundeslandes aus `state` und `state_code` ab (Slugs und Kürzel: [[konventionen]]) |
| `owned` | Gate 2 | eigener Betrieb des Betreibers. **Verändert die Darstellung nie** ([[footprint-rules]]) |
| `thin` | Gate 2, von Gate 3 aufgehoben | dünner Eintrag, startet mit `noindex` ([[launch-lean]]) |
| `claimed` | von Hand | Eintrag beansprucht und geprüft ([[refresh-and-upkeep]]) |
| `featured`, `featured_cities` | von Gate 2 leer angelegt, von Hand nach Zahlung | bezahlte Sichtbarkeit. `featured` kennt genau die drei **englischen** Werte `city`, `county`, `state`, die der Code liest; ein deutscher Wert erscheint nirgends (`templates/featured-tiers.md`, [[monetization-slots]]) |
| `premium`, `best_of_rank` | von Hand nach Zahlung | bezahlte Sichtbarkeit. Gate 2 legt diese beiden Spalten **nicht** an; beim ersten Verkauf werden sie der CSV hinzugefügt (`premium` = `true`, `best_of_rank` = `1` bis `3`). Fehlen sie, liest der Build sie als leer |
| `geprueft` | von Hand nach der Prüfung des Garantie-Antrags | `true` heißt „Festpreis-Garantie [Jahr]" mit den veröffentlichten Preisen (Dienstleistung und Material). Leer heißt „Noch keine Festpreis-Garantie" ([[siegel-programm]]). Der Spaltenname bleibt aus Rücksicht auf den Code |
| `geprueft_jahr` | von Hand | Jahr der Prüfung, steht auf dem Garantie-Nachweis und löst die jährliche Erneuerung aus |
| `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt` | von Gate 2 leer angelegt, von Hand nach der Prüfung | die Preise der **Dienstleistung** (Türöffnung, nicht Gesamtbetrag): Grundpreis (werktags 7–20 Uhr), Zuschlag abends/Wochenende/Feiertag, Zuschlag nachts (0–7 Uhr, nicht kumulativ), Anfahrt. Euro-Beträge als ganze Zahl ohne Einheit; `garantie_anfahrt` = `0` heißt „im Preis enthalten". Stehen im Eintrag, auf der Stadtkarte und auf dem Garantie-Nachweis; werden beim Entzug geleert ([[siegel-programm]]) |
| `garantie_zylinder`, `garantie_zylinder_5mm` | von Gate 2 leer angelegt, von Hand nach der Prüfung | der **Materialpreis** bei abgeschlossener Tür: Standardzylinder (`garantie_zylinder`) und fester Aufschlag je 5 mm Mehrlänge (`garantie_zylinder_5mm`). Euro-Beträge als ganze Zahl ohne Einheit. Erscheinen nur im vollen Preisblock der Eintragsseite, nicht auf der Stadtkarte; werden beim Entzug mit geleert ([[siegel-programm]]) |
| `preisschutz` | von Gate 2 leer angelegt | **reserviert, nicht gebaut:** die Stufe „Preisschutz" (Erstattung der Differenz bis 100 €). Kein Skript und keine Seite wertet sie aus, bis der Betreiber die Stufe freigibt ([[konventionen]]) |
| `socials` | Gate 5, `add_socials.py` | Profillinks von der eigenen Website ([[enrichment]]) |
| `description_enriched` | Gate 3 | die angereicherte Beschreibung; die rohe `description` bleibt unberührt |
| je Merkmal eine Spalte | Gate 3 | benannt nach dem `key` in `attributes.json`, Wert `wahr` / `falsch` / `keine Angabe` |

**`geprueft`, `geprueft_jahr`, `garantie_tag`, `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt`,
`garantie_zylinder` und `garantie_zylinder_5mm` werden von keinem Skript gesetzt.** Nur der
Herausgeber setzt sie nach der Prüfung eines Garantie-Antrags
von Hand. Ein Skript, das sie setzt, wäre eine Garantie ohne Prüfung; `merge_enriched.py` reicht
sie nur unverändert durch.

## Was an den deutschen Daten auffällt

- **`state`** trägt bei deutschen Zeilen meist den Bundeslandnamen, nicht immer in der
  Schreibweise der Slugliste („Baden-Württemberg", „Baden-Wurttemberg", „BW"). Gate 2 ordnet
  auf die 16 Slugs aus [[konventionen]] zu und verlässt sich im Zweifel auf die Postleitzahl.
  `state_code` ist bei deutschen Zeilen oft leer.
- **`county`** trägt, wie im englischen Lauf beobachtet, Stadtteilnamen und nicht den
  Landkreis. Für Landkreisangaben ist eine eigene Postleitzahlentabelle nötig; ohne sie
  kommen Landkreisangaben aus der Faktensammlung ([[page-types]]).
- **`website`** trägt oft Googles Tracking-Parameter in den Pfad kodiert, was einen 404
  ergibt. `clean_listings.py` dekodiert und entfernt sie.
- **`reviews_tags`** und **`posts`** können auf jeder Zeile leer sein und `description` fast
  immer. Dann liest das Anreichern die eigenen Websites ([[enrichment]]).
- **`about`** ist Googles Merkmalsdaten als JSON (`{"Barrierefreiheit": {...}}`), nie Prosa.
  Die Dünn-Kennzeichnung liest deshalb `description` und behandelt ein JSON-`about` als
  keinen Text ([[listings-cleaning]], Regel 8). Das Anreichern liest es weiter als Daten.
- **`working_hours`** kommt mit deutschen Tagesnamen und 24-Stunden-Zeiten zurück. Der Parser
  muss deutsche und englische Tagesnamen verstehen und „Geschlossen",
  „Durchgehend geöffnet" und „24 Stunden" erkennen ([[konventionen]]).
- **`phone`** kommt in wechselnden Schreibweisen (`0621 1234567`, `+49 621 1234567`,
  `+49621/1234567`). Normalisieren nach [[konventionen]], sonst scheitern Entdoppelung und
  der Abgleich mit den eigenen Nummern.
- **Die Kategorie `locksmith`** fängt auch Schuhmacher, Gravurbetriebe, Metallbauer und
  Baumärkte ein, dazu Kettenbetriebe und Callcenter ohne Ortsbezug. Der Gate-2-Bericht macht
  das über `type` und `subtypes` sichtbar; gelöscht wird nichts ([[listings-cleaning]]).

## Siehe auch
[[konventionen]] · [[listings-cleaning]]
