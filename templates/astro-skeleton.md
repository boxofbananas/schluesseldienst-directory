# Astro-Grundgerüst, die Dateikarte auf einem Bildschirm

Das Projekt liegt in `templates/astro/` (seine README sagt, was Gate 5 füllt). Dies ist die
Karte. Die Dateinamen bleiben englisch, weil die Astro-Routen und die Skripte sie so lesen;
die **Adressen** der gebauten Seiten sind deutsch und stehen in `wiki/konventionen.md`.

```
templates/astro/
├── package.json              astro ^5, @astrojs/sitemap, selbst gehostete Schriften
├── astro.config.mjs          Site-Adresse aus site.json; Sitemap-Filter entfernt noindex-Pfade
├── src/
│   ├── data/                 site.json · listings.csv · attributes.json · city-copy.json   (die Füllungen)
│   ├── lib/load.mjs          CSV-Leser, Eintragsmodell, Umlaut-Slugify, Zuordnung zum Bundesland,
│   │                         Stadt-Mindestzahl und Zusammenlegen (foldMaxKm hält entfernte Orte als
│   │                         indexierte Seiten), Nachbarstädte über Landesgrenzen, Reihenfolge,
│   │                         noindex-Menge, Öffnungszeiten mit deutschen Tagesnamen,
│   │                         Telefonnummern nach E.164, Siegelzustand aus geprueft/geprueft_jahr
│   ├── styles/global.css     nur Aufbau; die Marken kommen aus site.json
│   ├── styles/fonts.css      selbst gehostete Schriften, nie von Google geladen
│   ├── layouts/Base.astro    head, lang="de", robots, canonical, OG, Marken, Site-Schema,
│   │                         Kopfzeile, Fußbereich mit der Rechtszeile (Impressum, Datenschutz, AGB)
│   ├── layouts/Resource.astro  Ratgeberseiten aus Markdown (Article-Schema, Verfasserzeile)
│   ├── components/           JsonLd · Breadcrumbs (fünf Ebenen) · Card · Rating · Faq ·
│   │                         AttributeGrid · ClaimCta · FeaturedBand · DirectoryHub ·
│   │                         SearchForm · SocialLinks · Byline · SiegelBadge (Geprüft / Noch
│   │                         nicht geprüft) · MapPlaceholder (Karte erst nach Klick)
│   └── pages/
│       ├── index.astro                       Startseite: Kopfbereich, Bundeslandkarten,
│       │                                     Städtekarten, Premium-Block, Ratgeber, Fragen
│       ├── directory/index.astro             Blätterseite -> /verzeichnis/ (noindex, follow)
│       ├── directory/[state]/index.astro     Bundesland-Seite -> /verzeichnis/[bundesland]/
│       ├── directory/[state]/[city]/index.astro   Stadtseite = die Geldseite
│       ├── company/[state]/[city]/[slug]/index.astro  Eintragsseite -> /firma/..., einfach oder ausgebaut
│       ├── services/[...slug].astro           Leistungsseiten -> /leistungen/[slug]/
│       ├── search.astro · search-index.json.ts   Suche im Browser -> /suche/ (noindex)
│       ├── claim.astro                       -> /eintrag-beanspruchen/
│       ├── featured.astro                    -> /premium/
│       ├── siegel.astro                      -> /siegel/ (die sechs Kriterien)
│       ├── siegel/antrag.astro               -> /siegel/antrag/ (der Fragebogen)
│       ├── about.astro · contact.astro       -> /ueber-uns/ · /kontakt/
│       ├── impressum.astro                   -> /impressum/   PFLICHT, § 5 DDG, aus site.json
│       ├── datenschutz.astro                 -> /datenschutz/ PFLICHT, Art. 13 DSGVO, aus site.json
│       ├── agb.astro                         -> /agb/
│       ├── 404.astro
│       ├── resources/index.astro · resources/_example.md   -> /ratgeber/
│       ├── badge/[slug].svg.ts · badge/[slug]/index.astro   -> /auszeichnung/[slug].svg und
│       │                                                       /auszeichnung/[slug]/ (noindex)
│       └── robots.txt.ts
├── public/                   search.js, _headers (Cloudflare), images/ (Bild des
│                             Geschäftsführers, vom Inhaber gelieferte Eintragsfotos)
└── preview-site.command / .bat   zum Doppelklicken: liefert dist/ wie im Netz aus
```

Die Adressen in der rechten Spalte sind maßgeblich und stehen in `wiki/konventionen.md`. Wo
Dateiname und Adresse auseinandergehen (`directory/` → `/verzeichnis/`, `company/` →
`/firma/`, `badge/` → `/auszeichnung/`), setzt das Routing die deutsche Adresse; `_redirects`
in `dist/` leitet die englischen Formen und die Zwischenebenen `/firma/` und
`/firma/[bundesland]/` auf die passende Verzeichnisseite.

Bauen: `npm run build` → `dist/`. Ansehen: `preview-site.command` (Mac) oder
`preview-site.bat` (Windows), **nie** `dist/index.html` doppelklicken. Ausliefern: Cloudflare
Pages mit Wrangler (`npx wrangler pages deploy dist`), auf dem **eigenen Cloudflare-Konto**
des Verzeichnisses.

Der Aufbau ist das [[master-template]], die drei Ortsebenen sind [[site-architecture]], und was
Pflicht ist, steht in [[page-types]] und [[konventionen]].
