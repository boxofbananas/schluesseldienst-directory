# Website-Links nur für geprüfte, freigeschaltete und zahlende Einträge

**Datum** 2026-11-13 · **Branch/Stand** main, live · **Deployment** 0c5579bc · **check_live** 2821 bestanden
Betreiberentscheidung. Umgesetzt in Build **und** Template.

## Die Regel (eine Quelle: `load.mjs` → `websiteRel`)

| Zustand des Eintrags | sichtbarer Website-/Profil-Link | `rel` | JSON-LD `url` / `sameAs` |
|---|---|---|---|
| **geprüft** (`geprueft=true`) **oder** freigeschaltet (`link_follow=true`) | ja | `noopener` (gefolgt, ohne nofollow, ohne sponsored) | Website / Socials |
| **bezahlter Platz** (`premium`/`featured`/`best_of_rank`) ohne die beiden | ja | `sponsored noopener` | Website / Socials |
| **alle übrigen** | **kein** Website- und kein Profil-Link (auch nicht die Adresse als Text) | — (`websiteRel` leer) | eigene Eintragsseite / kein `sameAs` |

`owned` wird für die Darstellung **nicht** gelesen. Google-Maps-Link, Routenplanung und Telefonnummer
bleiben bei allen. Gilt auf der ganzen Site gleich, ohne Ausnahme nach Stadt.

## Punkt 1 — Spalte `link_follow`

- Neue Spalte in `site/src/data/listings.csv` (wahr/leer), eingefügt nach `preisschutz`.
- In `PROTECTED` von `scripts/_listings_guard.py` aufgenommen (Verlustschutz gefüllt→leer).
- Einmalig aus `owned=true` geseedet → **21 Einträge** auf `true`. Danach eigenständige, von `owned`
  unabhängige Spalte.

**Die 21 Einträge** (alle mit Website; 18 davon geprüft, 3 ohne Garantie):

Baden-Württemberg: `heidelberg-schluesseldienst-heidelberg`, `sperber-schluesseldienst-heidelberg`,
`i-s-e-schluesseldienst-hockenheim`, `mein-schluesseldienst-hockenheim-hockenheim`,
`tuerklar-schluesseldienst-leimen-leimen` *(ohne Garantie)*, `aes-schluesseldienst-mannheim-mannheim`,
`merz-sicherheit-einbruchschutz-schliessanlagen-schluesseldienst-mannheim`,
`riegelklar-schluesseldienst-schwetzingen-schwetzingen`, `kraichgau-schluesseldienst-sinsheim-sinsheim`,
`hardt-schluesseldienst-waghaeusel-waghaeusel`, `mein-schluesseldienst-weinheim-weinheim`,
`kurpfalz-schluesseldienst-wiesloch-wiesloch`.
Hessen: `odenwald-schluesseldienst-bensheim-bensheim`,
`lampertheimer-schluesseldienst-lampertheim` *(ohne Garantie)*,
`ried-schluesseldienst-viernheim-viernheim` *(ohne Garantie)*.
Rheinland-Pfalz: `rheinpfalz-schluesseldienst-frankenthal-frankenthal-pfalz`,
`suedpfalz-schluesseldienst-landau-landau-in-der-pfalz`,
`merz-schluesseldienst-ludwigshafen-ludwigshafen-am-rhein`,
`paelzer-schluesseldienst-neustadt-neustadt-an-der-weinstrasse`,
`merz-schluesseldienst-speyer-speyer`, `merz-schluesseldienst-worms-worms`.

Nur `merz-…-mannheim` hat zusätzlich einen bezahlten Platz (`premium`).

## Punkt 3 — jede Stelle, an der eine Betriebs-Website erscheint

| # | Stelle | Vorher | Nachher |
|---|---|---|---|
| 1 | Eintragsseite, Website-Link (Haupttext + Seitenleiste, 2×) | `rel=linkRel` | an `l.websiteRel` gekoppelt (Regel 2); leer → kein Link |
| 2 | Eintragsseite, Profil-Links (`SocialLinks`) | `rel=linkRel` | an `l.websiteRel` gekoppelt; leer → keine Profil-Links |
| 3 | Eintragsseite, JSON-LD `LocalBusiness.url` | immer Website | `websiteRel` → Website, sonst eigene Eintragsseite |
| 4 | Eintragsseite, JSON-LD `sameAs` | immer Socials | nur bei `websiteRel` |
| — | Stadt-/Bundesland-/Startseiten-Karten, Premium-Band | — | verlinken nur `l.path`, keine Betriebs-Website (unverändert) |
| — | Suchindex `search-index.json.ts` | — | kein `website`-Feld (unverändert) |
| — | `city-copy.json`, Leistungsseiten | — | 0 externe URLs / kein `website` (unverändert) |

**JSON-LD (3+4):** zuerst als „unverändert lassen" geklickt, dann von dir auf **Option 1 (an Regel 2
angleichen)** korrigiert und so umgesetzt.

## Punkt 4 — Verkaufshinweis

Im Beanspruchen-Kasten der Eintragsseite bei Einträgen **ohne** Link (`!hasWebLink`): ein Satz, dass der
Link mit der [Festpreis-Garantie] (ohne nofollow) oder einem [Premium-Platz] (als bezahlt gekennzeichnet)
kommt, mit Verweis auf beide Seiten. Im Build auf 3776 Seiten (3797 − 21).

## Punkt 5 — Texte angeglichen

- **/premium/**: der Website-Link gehört zu jeder bezahlten Stufe, als bezahlt gekennzeichnet; Prosa:
  „ohne bezahlten Platz und ohne Festpreis-Garantie trägt ein Eintrag keinen Website-Link". Auf 394
  Wörter getrimmt (Grenze 400), Textgate **bestanden**.
- **/festpreis-garantie/**: unverändert, Textgate bestanden (1512 Wörter, neues Band 700–1.600).
- **/eintrag-beanspruchen/**: „ergänzen Bilder und Links" → „ergänzen Bilder"; neuer Satz, dass der Link
  mit Garantie/Premium kommt. (noindex, nicht im Pflicht-Gate; der eine `garantie*`-Treffer dort ist das
  vorbestehende „Garantie-Antrag", nicht die Ergänzung.)
- **site.json FAQ** „Kostet ein Eintrag Geld?": Sichtbarkeit umfasst jetzt den Website-Link; ohne
  bezahlt/Garantie kein Link. Startseite-Textgate **bestanden**.
- **Wiki**: on-page-rules, site-architecture, page-types, siegel-programm, authority-and-links,
  monetization-slots, templates/astro/README.md, featured-tiers.md geändert.
- **Über uns / Datenschutz**: beschreiben nur Datenquellen bzw. Datenerhebung, kein Link-Versprechen →
  keine Änderung nötig (Datenschutz nennt „Website" nur als erhobenes Formularfeld).
- **copy-gate**: Garantie-Band 700–**1.600** (gebaute Seite kommt mit Pflichtteilen auf ~1.510).
- **AGB**: nur gemeldet, nichts geändert. A3 („bezahlte Platzierungen sind gekennzeichnet") deckt sich
  mit `sponsored`; kein Follow-Versprechen, das zu bestreiten wäre.

## Punkt 6 — footprint-rules: Ausnahme offen eingetragen

Grundregel neu: „Eigene Betriebe werden gelistet und sortiert wie jeder andere Betrieb." Darunter offen:
**die einzige Ausnahme ist der Website-Link** — eigene Betriebe tragen `link_follow=true` (einmalig aus
`owned` geseedet) und bekommen dadurch einen gefolgten Link, ohne eine Stufe zu kaufen (Betreiber-
entscheidung vom 2026-11-13); sie läuft über `link_follow`, nicht über `owned`. Der `owned`-Kommentar in
`load.mjs` ist entsprechend gefasst.

## Punkt 7 — Vorschlag für `konventionen` (nicht eingetragen; Daniel ändert die Datei frei)

Vorschlag für den Abschnitt zu Links / `rel` (Wortlaut):

> **Website- und Profil-Links auf Eintragsseiten.** Einen Link auf die Website und die Profile eines
> Betriebs trägt ein Eintrag nur, wenn der Betrieb die Festpreis-Garantie hat (`geprueft`) oder über die
> Spalte `link_follow` freigeschaltet ist — dann als **gefolgter** Link ohne `nofollow` und ohne
> `sponsored` — oder wenn er einen bezahlten Platz hat (`premium`, `featured`, `best_of_rank`) — dann als
> **bezahlt gekennzeichneter** Link mit `rel="sponsored"`. Alle übrigen Einträge tragen **keinen**
> Website- und keinen Profil-Link, auch nicht die Adresse als Text. Google-Maps-Link, Routenplanung und
> Telefonnummer bleiben bei allen. `owned` wird für die Darstellung nicht gelesen; die Freischaltung
> eigener Betriebe läuft allein über `link_follow` ([[footprint-rules]]).

## Prüfung (vorher → nachher, im Build)

| Kennzahl | vorher | nachher |
|---|---|---|
| sichtbare Website-Links `nofollow noopener` | 5812 | **0** |
| sichtbare Website-Links `noopener` (gefolgt) | 36 | **42** (21 Einträge × 2) |
| sichtbare Website-Links `sponsored noopener` | 0 | **0** |
| Einträge ohne Website-Link | — | **3776** |
| JSON-LD Business-url extern (Website) | 3797 | **21** |
| JSON-LD Business-url intern (Eintragsseite) | 0 | **3776** |
| JSON-LD `sameAs` | (alle mit Socials) | **0** (qualifizierte Einträge haben keine Socials) |
| Verkaufshinweis im Kasten | — | **3776** |

Erwartung (21 gefolgt, 0 sponsored, 0 nofollow, Rest ohne Link) **erfüllt**. Dass kein `sponsored`
auftritt, liegt daran, dass der einzige bezahlte Platz (Merz Mannheim) zugleich geprüft ist.

## Live-Stichprobe (die-besten-schluesseldienste.de)

| Eintrag | sichtbarer Website-Link | Verkaufshinweis | JSON-LD url |
|---|---|---|---|
| Merz (geprüft+premium+owned) | `noopener` (gefolgt) | nein | Website |
| AES (geprüft+owned) | `noopener` | nein | Website |
| Ried Viernheim (owned, **keine** Garantie) | `noopener` (via `link_follow`) | nein | Website |
| Key Walter (fremd, Mannheim) | **keiner** | ja | eigene Eintragsseite |
| Atilla (fremd, Mannheim) | **keiner** | ja | eigene Eintragsseite |
| AOS (fremd, Hamburg) | **keiner** | ja | eigene Eintragsseite |

Telefon und Maps/Route bei allen vorhanden (Ried Viernheim hat keine Telefonnummer in den Daten; das ist
ein Datenfeld, keine Folge der Link-Regel).

## Offen / Hinweise

- `verkauf.py` setzt weiterhin nur `premium`/`featured`/`best_of_rank`; `link_follow` wird von Hand
  gepflegt (eine neue eigene Freischaltung oder Rücknahme ist ein CSV-Eintrag + Neubau, über
  `apply_exclusions.py`, das `link_follow` jetzt als geschützte Spalte zurückträgt).
- Ein künftig verkaufter bezahlter Platz an einen **fremden** Betrieb ohne Garantie erscheint dann
  korrekt als `sponsored` — im aktuellen Datenstand gibt es keinen solchen.
