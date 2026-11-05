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
- **2026-11-03** **Gate 1 freigegeben, Gate 2 gelaufen.** `clean_listings.py` auf
  `input/listings-raw.csv` mit `--category "locksmith"` (englisches Kategorie-Label in den Daten,
  nicht „Schlüsseldienst“ – der Abholbericht schlug fälschlich das deutsche Label vor),
  `--chain-addresses 3` (Spec: „Namen an mehr als drei Adressen“; der Vergleich im Skript ist
  strikt `>`), beiden owned-Schaltern (10 Nummern, 21 Domains).
  Ergebnis: **3.102 → 2.912 behalten** (93,9 %); verworfen 102 veraltet, 88 Dubletten; 1.008 dünn;
  2 eigene Zeilen; `02-listings-clean.csv`, `02-domains.txt` (2.029), `02-clean-report.md`.
  **Zwei Datenmängel behoben (vom Betreiber freigegeben):**
  (1) **Bundesland fehlte komplett** – DataForSEO liefert für DE kein `region`; `clean_listings.py`
  leitete es nicht aus der PLZ ab. Autoritativen **GeoNames-PLZ-Datensatz** (CC BY 4.0) nach
  `scripts/data/geonames-de-plz.tsv` gevendert (23.295 Zeilen, 10.814 PLZ; `scripts/data/README.md`)
  und `clean_listings.py` erweitert (`load_plz_index`, `assign_from_plz`, `_pick_city`): Bundesland
  aus der PLZ, deutscher Name aus dem Kürzel (nicht aus GeoNames’ teils englischem Namen).
  Ergebnis: **2.911/2.912 zugeordnet**, nur 64760 Oberzent offen (GeoNames-Lücke, für Gate 4
  markiert). Der Rhein-Neckar-Dreiländerrand löst exakt auf (RP/BW/HE).
  (2) **Städtenamen englische Exonyme** (Munich/Cologne…) und 300 leer – aus PLZ/`address`-Feld auf
  Deutsch normalisiert: 349 Exonyme ersetzt, 300 gefüllt; Stadtstaaten BE/HH auf eine Stadt gezogen
  (Berlin 163, Hamburg 77), Bremen bleibt Bremen+Bremerhaven; 2 leere PLZ aus `address` nachgezogen.
  **Verteilung:** NW 666, BY 409, BW 376, NI 237, HE 213, BE 162, SN 154, RP 119, BB 97, SH 96,
  MV 78, HH 77, ST 77, TH 72, SL 46, HB 30. 1.257 Städte, 216 ab 3 Einträgen (halten 1.614 Zeilen).
  **Gate-4-Listen im Bericht:** fremde Gewerbe (Metallbau 240, Schuhmacher 87, Baumärkte 32,
  Gravur 19, Kfz 10), 841 nur über Nebenkategorie, Ketten (OBI 22, PM Service 9 u. a.).
  **Wichtiger Befund für den Betreiber:** von 21 eigenen Betrieben erscheinen nur **2** überhaupt
  in den Google-Daten (Merz Sicherheit Mannheim; eine Ludwigshafener Zeile über Telefon) – die
  übrigen 19 haben kein bewertetes Google-Profil unter `locksmith` und wurden nicht etwa verworfen.
  **Wartet auf:** Freigabe von `02-listings-clean.csv`, dann Gate 3.
- **2026-11-03** **Gate 2 freigegeben; eigene Betriebe nachgetragen; Gate 3 begonnen.**
  `add_own_listings.py` (Regeln [[eigene-betriebe]]) trug 12 eigene Betriebe nach (1 Dublette
  übersprungen): **2.912 → 2.924**, alle owned/thin/ohne Bewertung/ohne Garantie.
  **Umfang Gate 3 geändert (Betreiber):** nicht BW/RP/HE + 30 Städte, sondern **alle Einträge mit
  Belegbasis**. Belegklassifikation: **2.672 mit Textgrundlage** (Maps-Text oder lesbare Website),
  **252 ohne jeden Beleg → bleiben Grundeinträge** (nicht anreichern).
  Merkmalsdatei `03-attributes.json` aus `scripts/examples/` kopiert (14 Merkmale, Kern
  `schluesseldienst_kern`, 6 `service`-Blöcke = die sechs Leistungsseiten). Websites gelesen
  (`fetch_sites.py`), Belege gebaut (`build_evidence.py`, ~2,2 Mio. Token, 761/Eintrag).
  **Stapelläufer rechnet über das Claude-Abo** des Betreibers (kein API-Key), Verbrauch zählt
  gegen das Wochenkontingent; `run_batches.py` protokolliert jetzt die **echten Token** je Stapel.
  **Vier Skriptkorrekturen in Gate 3:**
  1. `fetch_sites.py` dekodierte latin-1/1252-Seiten als UTF-8 und packte gzip nicht aus → 48
     Cache-Dateien mit Mojibake/Binär. Neu: `_decode` (UTF-8 zuerst, tolerant gegen wenige
     Fehlbytes, dann deklarierte Kodierung, dann cp1252) und `_decompress` (gzip/deflate nach
     Header oder Magic-Bytes). Betroffene neu geholt: 48 → 1 (Rest ist eine Mojibake-Stelle in der
     Meta-Angabe der Quelle selbst).
  2. `make_batches.py` stürzte an Zeilen ohne Bewertung ab (`int('')`); rendert jetzt
     „rating: none" für die nachgetragenen eigenen Betriebe.
  3. `run_batches.py`: Token-Protokollierung (siehe oben).
  4. **Sechs Textregeln** vom Betreiber verlangt, in `enrichment-instructions.md` geschärft und als
     harte Prüfungen in `merge_enriched.py` verankert (lassen den Zusammenbau scheitern): keine
     Preise/Prozent, keine Bewertung/Sterne im Text, keine Kontaktdaten (Telefon, E-Mail,
     Straße+Nr.), keine Leseransprache (Sie/Ihr/Imperativ), nichts aus Karriere-/Partnerbereichen,
     keine Google-Ausstattungsmerkmale als Fließtext. Die alte Regel, die die Bewertungszeile
     verlangte, und die Erlaubnis für Website-Preise wurden entfernt.
  **Probeläufe auf Sonnet:** 40er-Stapel (erst mit Preisen, verworfen), dann 20er-Stapel mit den
  geschärften Regeln: **20/20 bestanden, 0 Verletzungen**, 997.766 Token / 0,975 $ (~50k Token,
  ~4,9 ct je Eintrag). Hochrechnung voller Lauf (2.672): **~130 $-Äquivalent**, überwiegend
  Cache-Reads, ~2,5–3 h bei 3 Läufern.
  **Für Gate 4 vermerkt:** Eintrag „Sicherheitsberater für Mechanische Nachrüstung…" (Goslar) ist
  ein keyword-gefüllter Google-Name; der echte Firmenname laut eigener Website ist „Schlüsseldienst
  Meineke" – Beispiel für schlechte Eintragsnamen, die Gate 4 prüft.
  **Wartet auf:** Freigabe des 20er-Probestapels, dann voller Gate-3-Lauf über die 2.672.
- **2026-11-04** **Gate 3 voll gelaufen.** 20er-Probestapel freigegeben, dann 86 Stapel (2.652
  Einträge) auf Sonnet im Hintergrund, Monitor mit 5-%-Abbruchregel (griff nicht). Ergebnis:
  **86/86 bestanden, 0 durchgefallen, 0 Wiederholungen.** Verbrauch **123,06 $-Äquivalent,
  131,96 Mio. Token, 4,6 ct/Eintrag, 3 h 12 min** – deckt sich mit der Hochrechnung (~130 $).
  `merge_enriched.py --basic-unanswered` schrieb `03-listings-enriched.csv`: **2.924 Zeilen,
  2.672 angereichert, 252 Grundeinträge** (ohne Beleg, jedes Merkmal „keine Angabe"). Dünne
  Einträge 1.020 → 741. Merkmalszählung u. a. **schluesseldienst_kern: 1.432 wahr / 507 falsch /
  733 keine Angabe** – die 507 (darunter 75 mit primärer Kategorie `Locksmith`) sind die
  Kernarbeits-Entscheidung für Gate 4. Bericht `03-enrich-report.md` geschrieben (Website-Status,
  Verbrauch vs. Hochrechnung, Merkmalszählung, core=false nach Kategorie, 737 Läufer-Notizen
  zusammengefasst, offene Punkte: 507 core=false, schlechte Namen wie Goslar/„Meineke", 252
  Grundeinträge, Vermittler). **Wartet auf:** Durchsicht `03-cache/review.md` + Freigabe, dann
  Gate 4.
- **2026-11-04** **Gate 3 freigegeben, Gate 4 begonnen.** Betreiber-Korrektur zu den 507
  `kern=false`: zwei Gruppen. **431 fremde Gewerbe ausschließen** (`04-exclusions.csv`), **76
  locksmith-Kategorie behalten** als Grundeinträge (75 `Locksmith` + 1
  `emergency_locksmith_service`; Liste `04-keep-locksmith-review.md` zur Ausreißer-Durchsicht).
  Behalten nach Ausschluss: **2.493**. Zahlen für die Entscheidungstabelle gerechnet:
  Stadt-Mindestzahl 2 → 380 Seiten/1.755 Einträge, 3 → 170/1.335; `foldMaxKm` 30 → 310
  eigenständige Ortsseiten, 50 → 98 (+4 ohne Koordinaten); dünn nach Ausschluss 675 (nicht dünn
  1.818); Sitemap zum Start 2.324 (foldMaxKm 30) bzw. 2.112 (50). Bundesländer-Reihenfolge nach
  Einträgen (NW 582 … HB 25), alle 16 mit Seite. `04-plan.md` (Entwurf) mit Entscheidungstabelle
  und Vorschlägen (Mindestzahl 3, foldMaxKm 50, sechs Leistungsseiten) geschrieben.
  **Wartet auf:** Entscheidungen zu Mindestzahl/foldMaxKm (und Durchsicht Keep-Liste, Ketten,
  Callcenter), dann Gate 5.
- **2026-11-04** **Gate-4-Entscheidungen (Betreiber):** Stadt-**Mindestzahl 2**, **foldMaxKm 30**.
  Begründung: Notdienst fährt 20–30 km, bei 50 km erschienen Betriebe aus 45 km auf fremden
  Stadtseiten. Neu gerechnet mit Mindestzahl 2: **380 Stadtseiten**, und bei foldMaxKm 30 nur
  **80** eigenständige 1-Eintrag-Ortsseiten (die 310 galten für Mindestzahl 3 – korrigiert).
  Sitemap zum Start **2.224** (die 80 Ortsseiten zunächst draußen). **Gate-6-Regel:** die 80
  1-Eintrag-Ortsseiten starten außerhalb der Sitemap, nach der 30-Tage-Prüfung tranchenweise
  frei – in `06-launch.md` festgehalten. Bestätigt: jede Stadt ab 2 Einträgen bekommt eine eigene
  Seite (Nürnberg 22, Fürth 8, Mannheim 19, Ludwigshafen a. Rh. 5, Heidelberg 7; getrennt von
  Namensnachbarn). Für Gate 5 vermerkt: Template-Mindestzahl ist 3 – auf 2 parametrisieren.
  **Wartet auf:** Durchsicht Keep-Liste (76) und Kandidatenlisten Ketten/Callcenter, dann Gate 5.
- **2026-11-04** **Gate 4: drei Listen gerechnet, Datenstand steht.** Keep-Liste (75 Locksmith)
  nach Betreiber-Regeln vorsortiert: **alle 75 → Gruppe B (behalten)** (irgendwo Schloss-/Schlüssel-
  Bezug), 0 Gruppe A, 0 Gruppe C; `04-keep-sorted.md`. **Ketten** (`04-chains.md`): 42 Gruppen
  gleichen Namens in ≥2 Städten, aber **0 Standorte** erfüllen die Ausschlussregel (geteilte
  Domain+Nummer und keine prüfbare Anschrift) – alle haben eigene Nummer oder Anschrift.
  **Callcenter** (`04-callcenter.md`): Daten sind sauber (0 Postfach, 7 ohne Straße, 3×0800),
  Vorwahl-Prüfung datenintern (Heimvorwahl je Stadt); nur **2 Kandidaten** mit ≥2 Merkmalen
  (beide nur „keine Straße + Mobil", echte Einmannbetriebe ohne Straßenangabe), kein owned; der
  1 `emergency_locksmith_service` ohne Merkmal → bleibt. **Template** `site.json` auf
  `cityFloor: 2`, `foldMaxKm: 30` gesetzt. Datenstand: **431 ausgeschlossen, 2.493 behalten**.
  **Wartet auf:** Entscheidung 9 (2 Callcenter-Kandidaten) und 10 (4 Orte ohne Koordinaten),
  dann Gate 5.
- **2026-11-04** **Gate 4 abgeschlossen; vier Betreiber-Nachträge.** (1) **Callcenter:** Merkmal
  „keine Straße" (und „nur Mobil ohne Straße") gestrichen – Service-Area ist Normalfall, Google
  blendet die Anschrift aus. Verbliebene Merkmale: Vorwahl≠PLZ, Postfach/Packstation/c-o, nur
  0800, Nummer in mehreren Städten. Ergebnis **0 Kandidaten**; `04-callcenter.md` neu. (2)
  **Koordinaten im Skript:** `add_own_listings.py` geokodiert jetzt über Nominatim (1 Anfrage/s,
  eigener User-Agent) mit Rückfall auf den PLZ-Mittelpunkt aus dem GeoNames-Datensatz; neue
  Spalte `geo_precision` (exact/plz), PLZ-Mittelpunkte zeigen später die Ortsfläche. Vendorter
  Datensatz um lat/lon erweitert; `clean_listings.py` setzt `geo_precision=exact` für
  Scrape-Zeilen. Pipeline neu gelaufen: alle **12 eigenen Betriebe exakt geokodiert**; die 4
  1-Eintrag-Orte falten innerhalb 30 km (Sinsheim→Kraichtal, Lampertheim→Viernheim,
  Frankenthal→frankenthal-pfalz, Bensheim→Heppenheim); 80 eigenständige Ortsseiten unverändert.
  (3) **Stadtseiten-Sortierung** in `konventionen` festgehalten: nach bezahlten Plätzen →
  Garantie → Festnetz mit passender Ortsvorwahl → Rest (je Gruppe nach Bewertung); Mobil oder
  Mehrstadt-Nummer zählt nicht als Ortsbezug (ersetzt „Garantie verändert die Reihenfolge
  nicht"). (4) **Festpreis-Garantie-Voraussetzung 2** verschärft: Festnetz mit passender
  Ortsvorwahl, Mobil allein genügt nicht – in `konventionen`, `siegel-programm`, der
  `/festpreis-garantie/`-Seite und beiden Antragsformularen (Pflichtfeld). Datenstand fix:
  **431 ausgeschlossen, 2.493 behalten.** **Wartet auf:** Freigabe der Voraussetzungsliste, dann
  Gate 5.
- **2026-11-04** **Vier weitere Betreiber-Nachträge.** (A) **Voraussetzung 4** gelockert: „liegen
  mind. 5 Google-Bewertungen vor, Schnitt ≥ 4,0; sonst entscheiden die übrigen Voraussetzungen"
  (Garantie = Preissicherheit, nicht Bekanntheit). In `konventionen`, `siegel-programm`,
  `/festpreis-garantie/`-Seite (+ Abschnitt „nicht geprüft": keine Aussage über Bekanntheit) und
  beiden Formularen (Google-Profil jetzt optional). (B) **Ortsnamen-Normalisierung** in
  `clean_listings.py` (`city_base`/`canonicalize_cities`): amtliche Zusätze fallen beim Vergleich
  weg, Varianten derselben Stadt < 5 km bekommen die häufigste Schreibweise; `add_own_listings.py`
  übernimmt die Scrape-Schreibweise (reuse der Normalisierung). Ergebnis: **1 Scrape-intern**
  (Königstein i.Ts. ← Falkenstein), **1 eigener** (Frankenthal → Frankenthal (Pfalz)) – die
  Daten waren schon sauber. `merge_enriched.py` toleriert jetzt verwaiste Antworten (Slug durch
  Umbenennung geändert) unter `--basic-unanswered`; der eine betroffene eigene Eintrag
  (Frankenthal) wird Grundeintrag (regeneriert beim nächsten Vollbau). Pipeline neu: **2.670
  angereichert, 254 Grundeinträge**. (C) **Mittelstadt-Schwelle (Vorschlag, noch nicht
  umgesetzt):** Einwohner aus GeoNames cities5000 (Feature P, Name + Bundesland). Schwelle 20.000
  → **+180** Stadtseiten (alle 1 Eintrag), 30.000 → **+84**; Sinsheim (37.036) fällt sonst auf
  Kraichtal (14.416), Bensheim (41.124) ganz. Würden wie die 80 Ortsseiten behandelt (Start außer
  Sitemap, Tranchen). **Wartet auf:** Freigabe der Mittelstadt-Schwelle (20k/30k/keine), dann
  Gate 5.
- **2026-11-04** **Mittelstadt-Regel: 20.000 gewählt und umgesetzt.** Datensatz
  `scripts/data/de-city-population.tsv` (GeoNames cities5000, CC BY 4.0) vendored; `clean_listings.py`
  und `add_own_listings.py` schreiben die Spalte `population`; `site.json` trägt
  `cityMinPopulation: 20000`; `load.mjs` gibt einer Stadt unter der Mindestzahl mit
  `population ≥ cityMinPopulation` eine eigene Seite und setzt alle Stadtseiten mit `count ≤ 1`
  auf `noindex` (Start außerhalb der Sitemap, Tranchen). `launch-lean`, `06-launch.md` und
  `04-plan.md` angeglichen. Seitenbild (simuliert): **381 Stadtseiten ≥ 2 Einträge**, **260
  eigenständige 1-Eintrag-Seiten** (66 Entfernung, 180 Einwohner, 14 beides), 475 gefaltet;
  Start-Sitemap ~2.225, Tranchen 260 + 675 dünne. **Gate 4 abgeschlossen.** Verifikation der
  `load.mjs`-Logik erfolgt mit `npm run build` in Gate 5. **Wartet auf:** Start von Gate 5.

- **2026-11-04 — Stadttext-Probestapel (20 Städte, 2 Modelle) + Welle-1-Stichprobe.** Faktenblatt
  mit 5 belegten Branchenfakten gefüllt (HWK/Handwerksordnung, Verbraucherzentrale, K-EINBRUCH,
  Stiftung Warentest). 20 gemischte Städte je einmal auf **Sonnet** (2,94 $, 14,7 ct/Stadt, alle
  bestanden) und **Haiku** (1,05 $, 5,3 ct) geschrieben. Größengewichtet auf 729 Seiten: Sonnet
  ~86 $, Haiku ~30 $. **Unterscheidbarkeit:** Sonnet 0 fast-gleiche Sätze; Haiku 4 Schablonen über
  12 der 20 Städte (ein Faktenblatt-Satz fast wörtlich, zwei Bewertungszeilen, ein Verzeichnis-
  Meta-Satz). Herkunft: beide ~70–76 % stadteigene Wörter, nur ~5 % Faktenblatt. **`check_city_copy.py`
  um einen Fast-gleich-Durchgang erweitert** (Jaccard ≥ 0,75, ≥3 Städte) – den alten Exakt-Vergleich
  bestand Haiku trotz Schablonen. **Empfehlung: Stadttexte auf Sonnet.** Welle-1-Stichprobe aus den
  breiten Kategorien bestätigt: `kern≠true` aus security/safe-Kategorien gehört per Gate-4-Ausschluss
  heraus. Nebenfund: 9 Städte ohne Bundesland (ausländische Grenzorte, u. a. Basel mit 9 Einträgen).
  Bericht: `berichte/2026-11-04-stadttext-probe.md`. **Wartet auf:** Entscheidungen des Betreibers.

- **2026-11-04 — Grenzorte, Textregel für 180 breite Einträge, Gegenprobe.** (1) 18 Einträge in 7
  ausländischen Grenzorten (Basel 6, Binningen/Kreuzlingen/Münchenstein, Słubice, Forbach,
  Spicheren) gedroppt; Oberzent auf Hessen korrigiert; „Unbekannt" (Schlüsseldienst Leipzig Herrmann,
  ohne Adresse) zur Entscheidung vorgelegt. (2) Textregel des Betreibers (Türöffnung im Text
  maßgeblich, nicht `kern`) per LLM auf alle 180 Einträge der Kategorien Alarm/Tresor angewandt:
  **135 ausschließen, 45 behalten**, in `04-exclusions.csv`. 25 Divergenzen zu `kern` (17×
  kern=true→ausschließen, 8× kern≠true→behalten) vorgelegt. Eichfälle ast/Stürmer/Reiher richtig
  getroffen. (3) Gegenprobe der 431 Gate-4-Drops: alle sauber, die 115 „Türöffnung"-Erwähnungen sind
  sämtlich Verneinungen. `04-exclusions.csv` nun **595 Drops**. Sonnet für Stadttexte freigegeben,
  aber **noch nicht gestartet** — wartet auf Durchsicht der Divergenzen. Bericht:
  `berichte/2026-11-04-breite-kategorien-und-grenzorte.md`.

- **2026-11-04 — Textregel ergänzt (Selbstbezeichnung) und neu angewandt.** Betreiber: Gruppe B (8)
  bestätigt behalten; Gruppe A 12/17 bestätigt, 5 zu hart. Regel ergänzt: Selbstbezeichnung als
  „Schlüsseldienst" (Name/Text) zählt als Beleg, ebenso Havarie-/Not-/Schlossnotdienst (nicht
  Tresor); Ausnahme bei Verneinung/Abgrenzung/Drittbezug. Begründung im Wiki
  (`directory-overview.md` Punkt 3): „Schlüsseldienst" ist im Deutschen die Aussage, Türen zu öffnen.
  Ergänzte Regel per LLM auf alle 135 Ausschlüsse angewandt: **18 kommen zurück** (13 davon waren in
  der Divergenzliste unsichtbar, kern=keine Angabe). 180-Bilanz 63/117. `04-exclusions.csv` 578.
  Leipzig Herrmann gedroppt. B+M Halle = 5 echte Filialen, keine Dublette. Bericht:
  `berichte/2026-11-04-textregel-ergaenzt-rueckkehrer.md`.

- **2026-11-04 — Stadttexte auf Sonnet erzeugt (792 Seiten).** Ausschlüsse (578) angewandt →
  3.809 Einträge, 792 Stadtseiten; Oberzent unter Hessen. Sonnet-Hauptlauf 69,99 $, 8,9 ct/Stadt,
  85 min, 111/112 im 1. Versuch; Nachläufe ~2,2 $; `city-copy.json` 792/792, 0 Durchfaller.
  **Slug-Kollision behoben** (friedberg/halle/senden): `make_city_packets.py` schlüsselt jetzt nach
  vollem `key`, vorhandene Pakete/Antworten umgeschlüsselt. **Near-Dup-Prüfung subquadratisch**
  gemacht (invertierter Index/Prefix-Filter) und 16+1 Schablonen neu geschrieben.
  Bericht: `berichte/2026-11-04-stadttexte-sonnet-fertig.md`.

- **2026-11-04 — Bewertungszahlen, Slug-Audit, Verhaltens-Ausschlüsse (Analyse + Härtung).**
  (1) 775/792 Stadttexte nennen datenstämmige Zahlen im Fließtext. Harte Regel in
  `city-copy-instructions.md` ergänzt (keine Bewertungsschnitte/-zahlen, Eintragszahlen je Stadt,
  km; qualitative Rangaussagen erlaubt), widersprüchliche Stellen umgeschrieben; Prüfung in
  `check_city_copy.py` ergänzt (meldet 775 durchgefallen). Gezielter Umschreib-Lauf wartet auf
  Freigabe (~5–12 $, Probe zuerst). (1c) Nur 4 Eintragsbeschreibungen mit Zahl, alle DataForSEO.
  (2) Slug-Audit: Eintrags-Slugs eindeutig; Stadtebene per vollem `key` behoben; keine zweite Stelle.
  (3) Vier Verhaltens-Drops identifiziert (Herzog/Mannheim, Kurt/Nürnberg, Schlüssel One/Erlangen+Fürth),
  warten auf Bestätigung + Vorgänge; Wiki `framework/conduct-exclusions.md`. Bericht:
  `berichte/2026-11-04-bewertungszahlen-kollision-ausschluesse.md`.

- **2026-11-04 — Datenstand abgeschlossen + Gate 5 gestartet.** Vier Verhaltens-Drops angewandt
  (`verhalten_betreiber`), Mannheim/Nürnberg/Erlangen/Fürth neu erzeugt (ohne die Betriebe,
  zahlenfrei, alle behalten ihre Seite). 3.805 Einträge, 792 Stadtseiten, `check_city_copy` 792/792.
  **Gate 5:** `npm run build` läuft durch (4634 Seiten), Rechtstexte erzeugen aus site.json,
  Schriften selbst gehostet, Maps nur nach Klick, kein aggregateRating, Sitemap ohne noindex-Seiten,
  featuredPreview=false. **Startsperren** (in `05-build-report.md`): (1) contact.formEndpoint fehlt
  (PFLICHT), (2) Stripe-Links fehlen, (3) Ratgeber leer, (4) Anwaltsprüfung Rechtstexte + USt-IdNr./
  Telefon offen, (5) fünf Schweizer Grenzorte noch im Datenstand (Entscheidung). Bericht:
  `output/schluesseldienste-deutschland/05-build-report.md`.

- **2026-11-04 (Nachtlauf):** Autonomer Lauf, sieben Punkte erledigt. Grenzorte: 5 Schweizer Orte
  (Allschwil, Arlesheim, Oberwil, Riehen, Siegershausen) gedroppt, kein weiterer Auslandsort übrig
  → 3.800 Einträge / 787 Stadtseiten. Impressum: USt-IdNr. und Telefon als bewusst leer entschieden
  (kein Blocker mehr). Formularannahme als Cloudflare Pages Function gebaut (`/api/claim`), PFLICHT-
  Sperre weg; Cloudflare-Bindungen (KV `EINSENDUNGEN`, `send_email` `SEB`) bleiben als Betreiber-
  Klicks offen. Linkcheck: 0 gebrochene/leere interne Links, keine noindex-Verlinkung. Screenshots:
  12 Seiten × 1440/390 px unter `berichte/screenshots/`. Textgate: Startseite, Bundesländer,
  „Über uns" bestanden; Stadttexte 787/787. **Fünf Ratgeberseiten** aus den zugelassenen Quellen
  geschrieben (nicht mit der seo-content-engine-Skill, da deren SERP-Basis die Quellenregel
  verletzt), alle durch `lint_copy.py --erlaube-rechtswoerter`; 0 $ externe Kosten. Berichte:
  `berichte/2026-11-04-morgenbericht.md`, `output/schluesseldienste-deutschland/05-build-report.md`.

- **2026-11-05:** Darstellungsfehler behoben. Sterne (★/☆) und Häkchen (✓) waren Schriftzeichen
  außerhalb des Latin-Auszugs und erschienen als Kästchen → Inline-SVG (`components/Star.astro`,
  `Check.astro`). `latin-ext` zusätzlich eingebunden, damit europäische Namen (ẞ, Š, İ, ş) rendern;
  Emoji/fremde Schriften werden in `load.mjs` (`sanitizeGlyphs`) aus Freitext entfernt; neue
  Build-Prüfung `scripts/check-glyphs.mjs` als `postbuild` scheitert bei jedem Zeichen außerhalb
  latin+latin-ext. Startseite ohne die 787er-Stadtliste (Verweis „Alle Städte" auf `/verzeichnis/`),
  Höhe 8.430 px (1440). Suchfeld-Platzhalter gekürzt; U+FEFF in load.mjs (Regex, gewollt) auf Escape
  umgestellt. Nebenbei: Öffnungszeiten zeigten „[object Object]" (DataForSEO-Array), `normalizeHours`
  repariert. Bericht: `berichte/2026-11-05-darstellungsfehler-und-startseite.md`.

- **2026-11-05 (Eintragsseite):** „Leistungen und Angaben" zeigt nur noch bestätigte Merkmale
  (Wert true); nicht bestätigte werden weggelassen, „Keine Angaben zu …"-Zeile raus; ohne
  bestätigtes Merkmal entfällt der ganze Abschnitt. **2.394** Einträge zeigten bisher die Fehlanzeigen-
  Liste; **1.453** (38 %) haben nach der Änderung keinen Merkmals-Abschnitt (1.403 ohne jedes bekannte
  Merkmal = fehlende Website-Beleggrundlage) → Frage an Daniel, ob Gate-3-Erkennung/Abdeckung
  nachgebessert wird (offen, nicht angefasst). Bewertungsschlagwörter (`reviews_tags`, u. a.
  „damage (45)") ersatzlos entfernt; nirgends sonst gerendert, bleibt in den Daten. `normalizeHours`:
  vorhandener leerer/`null`-Tag → „Geschlossen" (DataForSEO schreibt Ruhetag als `"sunday": null`).
  Städtezahl: 577 = indexierte Städte (≥2 Einträge), 787 = inkl. 210 kleinerer Orte; Verweise sagen
  jetzt „Alle Städte" (ohne Zahl). Bericht:
  `berichte/2026-11-05-eintragsseite-merkmale-schlagwoerter.md`.

- **2026-11-05 (Vorlage, zur Entscheidung):** Von den 1.453 Einträgen ohne bestätigtes Merkmal sind
  **204** indexiert (= thin=false) und **1.249** noindex (= thin=true) — exakte Überdeckung, also
  kein Startproblem. 204 liegt auf Daniels „unter-200"-Grenze. Vorgelegt (nicht umgesetzt): Zuordnung
  Google-`subtypes` → Merkmale, nur eindeutige (Locksmith→kern, Key duplication→schluessel_nachmachen,
  Emergency locksmith→kern, Burglar alarm→einbruchschutz); rettet 125 der 204, global +503/+315/+60.
  Dazu Empfehlung zur leeren rechten Hälfte der Stadtseiten (Sprungliste statt Karte). Entscheidung
  offen. `berichte/2026-11-05-merkmalserkennung-subtypes-vorlage.md`.

- **2026-11-05 (subtypes angewandt + Sprungliste):** Geprüft: kein Skript/Build liest
  `core`/`schluesseldienst_kern` für Aufnahme/Ausschluss/Sichtbarkeit; `apply_exclusions.py`
  droppt nur per `slug` aus dem eingefrorenen `04-exclusions.csv`. Änderung daher in der
  angereicherten CSV, `listings.csv` reproduziert (4.387→587 drop→3.800). 04-exclusions 587 → 587,
  Build 3.800 → 3.800, kein ausgeschlossener Eintrag zurück. Eindeutige subtypes → Merkmal
  angewandt, konservativ (nur keine-Angabe→wahr, `falsch` bewahrt: 9 kern, 2 nachmachen). Neu wahr:
  +496 kern, +313 nachmachen, +60 einbruchschutz; 809 Einträge mit ≥1 neuem Merkmal, 125 der 204
  gerettet. Herkunftssatz im Hinweiskasten ergänzt. Leistungsseiten: nur Einbruchschutz ändert sich
  (1.261→1.321), Stichprobe 10 alle korrekt; Türöffnung 1.572 unverändert. Stadtseiten:
  Sprungliste „Betriebe in <Stadt>" (Anker `#b-<slug>`) ab 8 Betrieben, sonst aus; Mannheim 20,
  Tuttlingen/Emden ohne. Bericht: `berichte/2026-11-05-subtypes-merkmale-angewandt-sprungliste.md`.

- **2026-11-05 (Gate 6, Teil 1 – Deploy):** Auf Cloudflare Pages ausgeliefert, Projekt
  `schluesseldienste-deutschland`, Produktionszweig `main`, Adresse
  https://schluesseldienste-deutschland.pages.dev/. whoami ok (Konto Domholdinggmbh, keine
  IP-/Rechtefehler, IPv4-first). KV-Namespace `EINSENDUNGEN` angelegt (id in wrangler.toml) und
  **über wrangler gebunden** — kein Dashboard nötig. `send_email` wird von Pages in der Konfig NICHT
  unterstützt (auskommentiert); gehört ins Dashboard und ist erst für den Mail-Worker nötig.
  `check_live.py` gegen pages.dev: alle 22 Prüfungen bestanden, Sitemap 2.807 Adressen. pages.dev
  sendet `X-Robots-Tag: noindex` (live bestätigt) → kein Doppelinhalt, kein Problem. Domain/Sitemap/
  Suchmaschinen bewusst noch nicht. Bericht: `berichte/2026-11-05-gate6-deploy-pages-dev.md`.

- **2026-11-05 (Gate 6, Teil 1 korrigiert):** KV-Namespace `EINSENDUNGEN` zuerst angelegt, echte id in
  wrangler.toml, dann Build/Deploy. `send_email` recherchiert: Pages Functions unterstützen es NICHT
  (Doku listet 12 Binding-Typen ohne E-Mail; wrangler lehnt es ab) → Binding auskommentiert, ohne
  ausgeliefert; Einsendungen gehen in KV, Daniel liest im Dashboard. KV zur Laufzeit als gebunden
  bestätigt. **Bug gefunden+gefixt:** `functions/api/claim.ts` `seite()` nutzte `Response.redirect`
  mit relativem Pfad → 1101 bei jedem Formular-POST; jetzt relativer `Location`-Header (live: 303
  bestätigt). `cloudflare:email` nur noch Typ-Import + dynamisch. Benachrichtigungswege im Bericht
  (KV+Dashboard jetzt; Mail-Dienst oder eigener Worker + Email Routing später; Ziel = Daniels
  verifiziertes Postfach, nicht info@). check_live alle bestanden, Sitemap 2.807. pages.dev noindex
  live bestätigt. Bericht: `berichte/2026-11-05-gate6-deploy-korrigiert-sendemail-kv.md`.

- 2026-11-05 WO-5: (1) Apex-Domain ans Pages-Projekt angehängt – Status pending, „CNAME record
  not set"; Token ist Pages-beschränkt, kann DNS nicht setzen → Daniel setzt den CNAME (Dashboard,
  ein Klick) oder gibt DNS/Rules-Token; www→Apex + check_live gegen echte Domain stehen aus.
  (2) Merz `premium=true` (Mannheim) → Kennzeichen „Premium-Eintrag", AES ohne Platz; kein Band
  (Band liest nur `featured`); Platz 1 durch Score 5,0/355, nicht manuell. (3) „Über uns" neu:
  Mission zuerst, Serviceversprechen + Verbraucherzentrale-Quelle, DOM Holding ein Satz + Schema,
  Startseite ohne Holding, Fuß behält sie; Gate bestanden. (4) `schluesseldienst-josef-mannheim`
  ausgeschlossen (verhalten_betreiber); Mannheim-Text per Pipeline neu, ohne Lücke; Nachbarn
  sauber. (5) Drei Überschriften A/B/C gebaut und verglichen; A/B mit Branchenzeile über der H1
  gate-fähig, jetzige Fassung wiederhergestellt/live. Neuer Build auf pages.dev ausgeliefert.
  Bericht: `berichte/2026-11-05-domain-merz-ueberuns-josef-ueberschriften.md`.
