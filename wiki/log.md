---
title: Protokoll
type: log
status: current
updated: 2026-11-03
---

# Protokoll

Je Gate und je Änderung eine Zeile anfügen, neueste unten: Datum, was gelaufen ist, die
Zahlen, was auf Freigabe wartet.

- **2026-11-03** Deutsche Fassung des Blueprints erstellt, aus der englischen Fassung vom
  2026-10-05 übertragen. Kein Gate gelaufen, keine Daten abgerufen. Die Festlegungen:
  Verzeichnis **Die besten Schlüsseldienste** auf `die-besten-schluesseldienste.de`,
  Herausgeber DOM Holding GmbH (Geschäftsführer Daniel Merz, HRB 43586), Branche
  Schlüsseldienst (`locksmith`), `niche.schemaType` = `Locksmith`, wichtigste Stadt Mannheim,
  Build-Ordner `output/schluesseldienste-deutschland/`.
  **Drei Ortsebenen** statt zwei: Startseite → bis 16 Bundesländer → Städte → Einträge;
  `site-architecture`, `page-types`, `launch-lean` und `schema` entsprechend umgebaut, die
  URL-Tabelle in `konventionen` ist maßgeblich.
  **Gate 1 auf drei Fragen gekürzt:** eigene Telefonnummern, Optik, Freigabe des Datenabrufs
  mit Kostenangabe. Branchenwahl samt Bewertungsbogen, `check_vertical.py`, Nischenfinder,
  „VERTICAL FLAG" als Entscheidungsfrage, Wahl des Bundesstaats, Domain-Empfehlung und die
  Frage nach dem Herausgeber ersatzlos gestrichen.
  **Neue Wiki-Seite `framework/siegel-programm.md`** und überall verdrahtet
  (`monetization-slots`, `page-types`, `refresh-and-upkeep`, `authority-and-links`,
  `page-sections`, `master-template`, `featured-tiers.md`, `claim-form.html`, `index.md`):
  zwei Stufen, sechs veröffentlichte Prüfkriterien, Selbstauskunft plus Unterlagenprüfung und
  kein Test vor Ort, Jahreszahl und jährliche Erneuerung, Entzug bei belegten Beschwerden,
  nicht kaufbar; „Noch nicht geprüft" als nicht abschaltbarer Verkaufsanlass.
  **Recht in die Gates eingebaut:** Gate 5 erzeugt Impressum (§ 5 DDG) und
  Datenschutzerklärung (Art. 13 DSGVO) aus `site.json` und verlinkt beide im Fußbereich jeder
  Seite; ein Platzhalter in einer der beiden macht den Build unfertig. Keine Karte, kein
  externes Skript, keine externe Schrift ohne Einwilligung; Google Maps erst nach Klick.
  Preise in Euro, Stripe-Zahlungslinks unverändert. Die Faktensammlung benutzt
  Handwerkskammer, Gewerbeamt, Verbraucherzentrale, polizei-beratung.de und Stiftung
  Warentest; die US-Quellen (Lizenzbehörde, 811, Landesstatute) ersatzlos gestrichen.
  Schlüsseldienst ist kein zulassungspflichtiges Handwerk: „lizenziert", „zugelassen",
  „zertifiziert" sind verboten, ebenso „Innung", „Verband", „Kammer", „amtlich",
  „Verbraucherschutz", „getestet" in sichtbaren Texten (Verwechslungsgefahr mit einer
  amtlichen Stelle).
  **Branchenbesonderheit beschrieben** in `listings-cleaning` und in `CLAUDE.md` (Gate 2 und
  Gate 4): `locksmith` fängt Schuhmacher, Gravurbetriebe, Metallbauer und Baumärkte ein, dazu
  Kettenbetriebe mit vielen Adressen und Callcenter ohne Ortsbezug; Gate 2 löscht nichts, der
  Bericht macht es über vier Listen sichtbar, der Mensch entscheidet in Gate 4.
  **Footprint-Regeln geschärft:** je Stadt höchstens ein eigener Betrieb auf einem bezahlten
  Platz, eigenes Cloudflare-Konto, kein Google Analytics und keine Search Console; Merz
  Sicherheit in Mannheim mit Premium und Top-Platzierung zum öffentlichen Preis, als normaler
  Vorgang.
  **Preisstufen auf Euro umgestellt:** Premium-Eintrag 97 € im Jahr, Stadt-Premium 29 € im
  Monat, Top-Platzierung 250 € einmalig; Landkreis- und Bundesland-Stufe als später zu
  aktivieren vermerkt. Siegelschnipsel auf `/auszeichnung/[slug].svg` und
  `/firma/[bundesland]/[stadt]/[slug]/` umgestellt, Alternativtext und Siegeltext deutsch mit
  Jahreszahl.
  Messwerte: keine deutschen. Alle Zahlen aus echten Läufen sind als Erfahrung aus dem
  englischen Pilotprojekt (Poolbauer Florida, Zaunbauer Colorado) gekennzeichnet.
  **Wartet auf:** Freigabe der deutschen Fassung, dann Gate 1.
- **2026-11-03** Durchsicht der deutschen Fassung abgearbeitet, sechs Mängel behoben. Kein Gate
  gelaufen, keine Daten abgerufen.
  **1. Verbotslisten fingen keine gebeugten Formen.** `lint_copy.py` und
  `skills/seo-content-engine/scripts/lint_article.py` verstehen jetzt **Wortstämme**: ein
  Listeneintrag, der auf `*` endet, trifft jede Fortsetzung (`lizenzier*` → „lizenziert",
  „lizenzierte", „Lizenzierung"), in Wörtern und in jedem Teil einer Wendung, weiter
  umlauttolerant. Beide Listen auf Stämme umgestellt, die von `konventionen` verlangten Wörter
  `Verband`, `Kammer`, `Verbraucherschutz` und `offiziell geprüft` ergänzt. Belegt am Prüfsatz
  der Durchsicht: vorher **ein** Treffer (`staatlich`), jetzt acht
  (`lizenzier*` 2, `zugelassen*`, `zertifizier*`, `verband`, `amtlich*`, `getestet*`,
  `staatlich`, Wendung `staatlich anerkannt*`); „geprüft" und „nicht zulassungspflichtig"
  schlagen weiter nicht an.
  **2. Widerspruch zwischen Verbotsliste und Siegel-Seite gelöst.** Die Rechts- und Amtswörter
  stehen in beiden Listen in eigenen Blöcken `[RECHTSWOERTER]` und `[RECHTSWENDUNGEN]`, und
  `lint_copy.py --erlaube-rechtswoerter` lässt genau diesen Block für eine einzelne Seite zu;
  die Floskeln bleiben verboten. Gilt nur für `/siegel/`, `/agb/` und Ratgeberseiten zur
  Rechtslage, **nie** für Stadttexte, Eintragsbeschreibungen oder die Startseite; festgehalten
  in `copy-gate` Abschnitt 1a. `check_city_copy.py` kennt den Schalter nicht. Wortband
  `/siegel/` von 400–700 auf **700–1.200** (sechs Kriterien plus Serviceversprechen plus
  Aufklärung; Probebau 784 Wörter), auch in `page-types`. Band der Bundesland-Seite (300–500)
  ist richtig: `site.regionIntro` ist im Template leer, deshalb 227 Wörter im Probebau – das
  Band greift erst, wenn Gate 5 den Einleitungstext geschrieben hat.
  **3. Spaltenwerte richtiggestellt.** `featured-tiers.md`: `featured` = `city`, `county`,
  `state` statt `stadt`, `landkreis`, `bundesland` (der Code liest nur die englischen),
  Zahlungslinks `STRIPE_LINK_CITY` und `STRIPE_LINK_BESTOF` nach `site.json`, eine Schreibweise
  der Stufennamen festgelegt (Stadt-Premium, Premium-Eintrag, Top-Platzierung; „Premium-Platz"
  bleibt der allgemeine Begriff aus `konventionen`). Dieselbe Verwechslung im Wiki behoben:
  `monetization-slots` nennt die drei Werte, `outscraper-columns` und `listings-cleaning` nennen
  nicht länger Spalten `bundesland`/`bundesland_slug` (es gibt sie nicht; das Bundesland steht in
  `state`/`state_code`) und halten fest, dass Gate 2 `premium` und `best_of_rank` nicht anlegt.
  **4. Sitemap-Angaben an den Code angepasst.** `launch-lean`: zum Start in die Sitemap kommen
  von den Einzelseiten nur `/siegel/` und `/ueber-uns/`; `/siegel/antrag/`,
  `/eintrag-beanspruchen/`, `/premium/`, `/kontakt/`, `/impressum/`, `/datenschutz/`, `/agb/`
  sind `noindex` und bleiben draußen (`noindexPaths` in `load.mjs`, geprüft von
  `check_live.py`). `siegel-programm`: `/siegel/antrag/` ist `noindex`, nicht indexiert.
  **5. Falsche Aufrufe berichtigt.** `check_city_copy.py --write` erwartet einen **Pfad** –
  vollständiger Befehl in `CLAUDE.md` und `copy-gate`. Für `--city-sizes` ist festgelegt: die
  Datei `05-city-sizes.json` schreibt Gate 5 unmittelbar nach `node dump-cities.mjs` aus
  `05-cities.json` (Einzeiler steht in `copy-gate`); maßgeblich für die Größenklassen bleibt
  `check_city_copy.py` über die Zeile `intro band:` der Pakete. `make_worker_listings.py` hat
  eine Argumentbehandlung und bricht nicht mehr mit `IndexError` ab.
  **6. Betreiber-Hilfen auf Deutsch und auf dieses Projekt.** `make_city_packets.py`
  (`--bundesland` statt `--state`, Vorgabe Deutschland statt eines einzelnen Landes, Zeile
  `bundesland:` je Stadt, deutsche Kreisnamen), `make_local_preview.py` (Argumentbehandlung,
  deutsche Beispielpfade), `fetch_sites.py` (deutsche Unterseitenwörter des Gewerbes,
  `Accept-Language: de`, deutsche Branchenbücher als „keine eigene Website"),
  `make_batches.py`, `run_batches.py` (deutsche Aufgabentexte) und `mail_worker.py` auf Deutsch
  umgestellt. Die **Paketschlüssel bleiben englisch** (`city:`, `intro band:`,
  `description band:`, `directory:`), weil `check_city_copy.py` und die Anweisungsdateien sie
  lesen; Begründung steht als Kommentar in beiden Skripten.
  **Zwei Fehler, die dabei auffielen und mitbehoben wurden:** `run_batches.py` suchte in der
  Prüfausgabe fest nach `failing: 0`, das nur `merge_enriched.py` schreibt – damit galt **jeder**
  Stadttextstapel als durchgefallen; die Markierung steht jetzt je Modus (`durchgefallen: 0` für
  `city-copy`). Und `mail_worker.py` las `site.json → state.name`, das es in der dreistufigen
  Fassung nicht gibt (`KeyError` beim Einrichten des Workers); es nimmt jetzt `country.name`
  („Deutschland") für die Worker-Variable `STATE_NAME`, deren Name englisch bleibt.
  **Wartet auf:** Freigabe der deutschen Fassung, dann Gate 1.
- **2026-11-03** **Prüfzeichen → Festpreis-Garantie.** Umgebaut, weil ein Prüfzeichen eine
  Eigenschaft des Betriebs beschreibt, eine Garantie aber ein Versprechen an den Kunden ist, und
  nur das Zweite dem Betrieb Kunden bringt: Der Preis steht öffentlich, vor dem Anruf, bei
  einem Dritten, der ihn bei Verstoß wegnimmt – das kann ein einzelner Betrieb nicht nachbauen.
  Vertrag: Abschnitt „Festpreis-Garantie" in `konventionen`. Umgesetzt: `siegel-programm` neu
  geschrieben (Dateiname und Wikilink bleiben, Titel „Festpreis-Garantie"); Adressen
  `/festpreis-garantie/` und `/festpreis-garantie/antrag/` überall; Spalten `garantie_tag`,
  `garantie_nacht`, `garantie_anfahrt` und die reservierte Spalte `preisschutz` in
  `clean_listings.py` (leer angelegt), `merge_enriched.py` (`EXTRA`, durchgereicht),
  `outscraper-columns` und `listings-cleaning`; Garantie-Antrag in `claim-form.html` mit den
  drei Preisen als Pflichtfeldern und den festen Feldnamen des Astro-Codes; Garantie-Nachweis in
  `featured-tiers.md` („Festpreis-Garantie {{JAHR}} · Türöffnung ab {{GARANTIE_TAG}} €",
  kostenlos, keiner Stufe zugeordnet); Mail-Worker-Kategorie `garantie_request`; Wortlisten:
  Stamm `garantie*` und die Garantie-Wendungen in den Rechtsblock, Ausnahme für den
  Programmnamen „Festpreis-Garantie" in `lint_copy.py` (`PROGRAMMNAME`), Regel in `copy-gate`
  Abschnitt 1b, `/premium/` neu in der Prüftabelle mit Schalter; `CLAUDE.md`, `README.md` und
  alle Wiki-Seiten auf die neue Wortwahl („Festpreis-Garantie 2026" mit drei Preisen /
  „Noch keine Festpreis-Garantie"). `make_worker_listings.py` nimmt `geprueft` nicht mit, also
  auch keine Preise; der Worker behandelt Einträge mit Garantie nicht gesondert. Offen:
  `templates/astro-skeleton.md` ist über die Garantie-Zeilen hinaus veraltet (englische
  Dateinamen, die im Template nicht mehr existieren). **Wartet auf:** Freigabe, dann Gate 1.
- **2026-11-03** **Gate 1 begonnen.** Build-Ordner `output/schluesseldienste-deutschland/`
  angelegt, `01-umfang.md` erstellt. Frage 1 (eigene Betriebe) beantwortet: 21 Websites, davon
  10 mit Telefonnummer; Erkennung in Gate 2 über `--owned-domains` und `--owned-phones` (beide
  per `--help` als vorhanden bestätigt); Merz Sicherheit in Mannheim ist die Hauptfirma,
  bezahlter Platz zum öffentlichen Preis erst nach dem Start. Frage 2 (Optik): Vorgabe, Marken
  des Templates unverändert.
  **Fehler in `fetch_dataforseo.py` behoben:** Der Länderfilter benutzte das von DataForSEO
  ungültige Feld `address_info.country` und ließ jeden `--estimate`/Lauf mit
  `40501 Invalid Field: 'filters'` scheitern. Gültig ist `address_info.country_code` mit
  ISO-Code; gegen die offizielle Filterliste geprüft (alle übrigen Filter – `domain`,
  `address_info.region`, `category`, `rating.votes_count` – sind gültig). Behoben über die
  Tabelle `COUNTRY_CODES` und die Funktion `country_code(name)`, Docstring nachgezogen. Danach
  Schätzung bestätigt: **3.102 `locksmith`-Einträge bundesweit, Abruf etwa 1,16 $**, ≥ 456
  Städte, keine Branchen-Warnung. Auffällig: `address_info.region` kommt im deutschen Bestand
  leer (Bundesland-Zuordnung erst in Gate 2).
  Frage 3 (Datenabruf): „1, abrufen" freigegeben. Abruf gelaufen: **3.102 Zeilen** nach
  `input/listings-raw.csv`, gemeldete Kosten **1,1771 $**, 1.266 Städte, 861 mit E-Mail,
  `last_updated_time` 2023-05-24 bis 2026-10-07. `01-umfang.md` steht auf
  `wartet-auf-freigabe`. **Wartet auf:** Freigabe von `01-umfang.md`, dann Gate 2.
