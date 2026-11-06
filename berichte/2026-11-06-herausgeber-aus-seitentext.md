# Herausgeber aus dem Seitentext genommen (bis auf die Pflichtstellen)

**Datum:** 2026-11-06
**Ziel:** „DOM Holding GmbH" und „Daniel Merz" aus dem sichtbaren Seitentext entfernen, außer dort,
wo sie rechtlich oder fürs Schema stehen müssen. JSON-LD (publisher, Organization, Person) bleibt
auflösbar.

## Fundstellen vor der Änderung

Beide Namen stehen als **Literal nur in `src/data/site.json`** (`publisher.name`, `legalName`,
`managingDirector`, `bio`, `footerAbout`). Überall sonst sind es Referenzen
(`site.publisher.name` usw.).

## Entscheidungen je Stelle

**Unverändert (Pflichtstellen / Schema / Datenquelle):**
- `src/data/site.json` (name, legalName, managingDirector, bio) — Datenquelle.
- `src/pages/impressum/index.astro` — Impressum, beide Namen vollständig.
- `src/pages/datenschutz.astro` — Datenschutz, beide Namen vollständig.
- `src/pages/ueber-uns.astro` Organization- + Person-Schema — Daniel Merz nur noch hier als
  Person (`@type: Person`, `jobTitle: Geschäftsführer`).
- `src/layouts/Base.astro:46` site-weites Organization-JSON-LD.
- `src/layouts/Resource.astro:15` Artikel-Schema `author`/`publisher` (@id-Referenzen).

**Geändert (Herausgeber aus dem Fließtext):**
- `src/data/site.json` `footerAbout` — Firmenname raus, **Behörde-Satz bleibt** („Wir sind keine
  Behörde, keine Kammer und kein Verband").
- `src/layouts/Base.astro` — Fußzeile „Herausgegeben von DOM Holding GmbH" entfernt (Über uns ist
  weiterhin in Hauptnavigation und Fuß-Schnellzugriff verlinkt, nichts verwaist).
- `src/components/Byline.astro` — Verfasserzeile der Ratgeberseiten: `publisher.name` → `brand`
  („Von Die besten Schlüsseldienste").
- `src/pages/ueber-uns.astro` Fließtext — „, Geschäftsführer Daniel Merz" raus, Firma bleibt.
- `src/pages/eintrag-beanspruchen.astro` + `src/pages/festpreis-garantie/antrag/index.astro`
  Art.-13-Hinweis — „(Daniel Merz)" raus, „DOM Holding GmbH" bleibt (Verantwortlicher ist die
  Gesellschaft).

**Nicht in der Vorgabe genannt — eigene Entscheidung:**
- `src/pages/agb.astro` — **bleibt**: AGB ist eine Vertrags-/Rechtsseite, auf der die anbietende
  Gesellschaft genannt sein muss, wie Impressum.
- `src/pages/kontakt.astro` — Firmenname raus (keine Pflichtstelle); Impressum- und
  Über-uns-Links bleiben.
- `src/pages/danke.astro` — „DOM Holding GmbH meldet sich" → „Wir melden uns" (noindex, keine
  Pflichtstelle).

## Prüfung

- `npm run build`: Exit 0, keine Warnung über fehlende Daten.
- JSON-LD in `dist/`: 0 kaputte Blöcke. Startseite trägt `Organization` `publisher`
  („Die besten Schlüsseldienste") **und** `herausgeber` („DOM Holding GmbH"); „Über uns" trägt
  `herausgeber` (Organization) + `geschaeftsfuehrer` (Person, Daniel Merz). Alles auflösbar.
- Sichtbarer Text in `dist/`: beide Namen nur noch auf Impressum, Datenschutz, AGB, Über uns und
  den zwei Art.-13-Hinweisen. **Nicht** auf Startseite, Bundesland-, Stadt-, Eintrags-, Leistungs-,
  Ratgeber-, Kontakt- oder Danke-Seiten, nicht im Fuß. „Daniel Merz" im Fließtext nur noch
  Impressum + Datenschutz.
- Ausgeliefert nach Cloudflare Pages. `check_live.py … --expect-urls 2823`: **alle Prüfungen
  bestanden** (Sitemap 2823, Fuß verlinkt Impressum/Datenschutz).
- Live-Abruf `https://die-besten-schluesseldienste.de/`: kein „DOM Holding"/„Daniel Merz" im
  Startseitentext; Fuß ohne Herausgebername, Behörde-Satz steht, Impressum/Datenschutz verlinkt;
  JSON-LD `publisher`/`herausgeber` lösen auf.
