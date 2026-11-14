---
title: Protokoll
type: log
status: current
updated: 2026-11-06
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

- 2026-11-05 Nachtrag: Merz zusätzlich `featured=city` → Premium-Band der Mannheimer Seite (ab
  29 €, Stadt-Preis steht schon in `tiers.city`). Dabei Fund+Behebung: `homeFeatured` zog
  state+county+city → ein Stadtplatz wäre auch im Startseiten-Band erschienen; jetzt speist **nur
  `featured=state`** das Startseiten-Band (load.mjs), Preis-Prop → `tiers.state.price`
  (DirectoryHub). Startseiten-Band damit ohne eigenen Betrieb und ohne Preis-Label. Preis für die
  Startseiten-/Bundesland-Stufe gehört in `tiers.state` (site.json) + /premium/ (Zeile erscheint
  bei gesetztem Preis). Ausgeliefert `8992ce52`.

- 2026-11-05 Folgerunde: (1) Hook-Screenshots A/B/C + Band-Bilder ins Repo
  (`berichte/screenshots/hook-{a,b,c}-1440.png`, `band-mannheim.png`, `band-startseite.png`),
  Überschriften als Text im Bericht. (2) Entscheidung: Startseiten-Band nicht bepreisen
  (`tiers.state` ohne Preis, keine `country`-Stufe) bis Zahlen nach der 30-Tage-Prüfung; Begründung
  + Trennungs-Warnung „Bundesland ≠ Startseite" in [[monetization-slots]] („Das Startseiten-Band"),
  Stadt-Premium-Zeile dort korrigiert (Startseite raus). (3) `check_live.py` um drei Prüfungen für
  den Domain-Umzug erweitert: www→Apex-Weiterleitung (301/308), TLS-Zertifikat, Sitemap-Hosts =
  echte Domain (kein pages.dev); greifen nur gegen die echte Domain. Lauf gegen pages.dev weiter
  grün (Sitemap 2806).

- 2026-11-05 Startseiten-Überschrift festgelegt: Fassung B. Augenbraue „Schlüsseldienste in
  Deutschland" (CSS `.eyebrow`, `--action`) über H1 „Damit die Rechnung keine Überraschung
  wird." (allein „keine Überraschung" in Bernstein); Unterzeile „… seinen Preis für Türöffnung
  und Anfahrt vorher nennt …". A/C entfallen. Augenbraue in `design.eyebrows` festgehalten
  (konkret, einzige der Site), global.css-Kommentar + [[page-sections]] (Begründung: Startseite
  ist kein Notfall-Einstieg, Publikum = Marke + Verkauf) aktualisiert. Textgate bestanden,
  ausgeliefert `6c99409f`. Seitenkopf-Bilder `berichte/screenshots/startseite-kopf-{1440,390}.png`.
  Offen (nicht vorbereitet): Domain (Daniels DNS, dann check_live), Festpreis-Garantie eigener
  Betriebe (Daniels Preise, dann geprueft/geprueft_jahr + Preisspalten).

- 2026-11-05 Voraussetzung 2 der Festpreis-Garantie: zwei im `output/`-Build verbliebene
  Alt-Fassungen (öffentliche Seite + Antragsformular) auf den Wiki-Wortlaut korrigiert; Ursache war
  Template-vs-Build-Drift (2026-11-04-Edit traf Wiki + `templates/`, nicht den `output/`-Baum).
  Maschinenprüfung vorgeschlagen (Stale-/Required-Phrase-Wächter übers ganze Repo, Single-Source der
  Listen in site.json, Template↔Build-Parität) — nicht gebaut. Bericht
  `berichte/2026-11-05-voraussetzung2-fix-material-preis.md`.
- 2026-11-05 Festpreis-Garantie um das Material präzisiert: Dienstleistung (drei Preise) vs. Material
  bei abgeschlossener Tür (neue Spalten `garantie_zylinder`, `garantie_zylinder_5mm`, Standardzylinder
  + Aufschlag je 5 mm; Variante A, zwei feste Spalten) vs. defekte Tür (Ab-Preis, vor Arbeitsbeginn
  beziffert, keine Spalte). Preissemantik in **`konventionen.md` Z. 128–155** geändert (alter Wortlaut
  im Bericht zitiert): „drei Standardpreise" → Dienstleistung + Material. Serviceversprechen auf fünf
  Punkte, Preisblock der Eintragsseite in zwei beschriftete Gruppen + Fußnote (Karte/Nachweis
  unverändert). Alle drei Antragsformulare, `load.mjs`, die Pipeline-Skripte und ~20 „drei Preise"-
  Stellen im Wiki angeglichen; Log-Historie unangetastet. Textgate: neue Preistexte sauber (drei
  vorbestehende Treffer der Rechtsseite unberührt). Ausgeliefert `cb47edd7`. Screenshot
  `berichte/screenshots/preisblock-material-5zahlen.png`.

- 2026-11-05 Template-vs-Build gemessen: 25 Dateien auseinander (`templates/astro/src` vs.
  `output/.../site/src`, ohne data/), **alle Build-voraus, null Template-voraus**. Befund als
  [[template-build-drift]] festgeschrieben (zwei Sorten: allgemeine Verbesserungen → ins Template
  beim nächsten Verzeichnis; projekteigener Inhalt bleibt verschieden). Für dieses Verzeichnis ist
  der Build die Wahrheit. **Sperre gebaut:** `scripts/init_site.py` legt `output/<slug>/site/` aus
  dem Template an und bricht ab, wenn der Ordner existiert (nur `--force`, legt vorher ein Backup
  an); Gate 5 in CLAUDE.md darauf verdrahtet (kein Hand-`cp`). Rückport, Paritätsprüfung und
  geteilter Code bewusst **nicht** gebaut — nach dem Start.

- 2026-11-05 **Domain live (Apex).** Apex-CNAME `die-besten-schluesseldienste.de` →
  `schluesseldienste-deutschland.pages.dev` (proxied) per DNS:Edit-Token angelegt; Domain springt
  auf aktiv, HTTP 200, TLS gültig bis 01.02.2027. `check_live.py --expect-urls 2806` **bestanden
  bis auf die www-Weiterleitung** (2806 Adressen, alle auf die Hauptdomain, pages.dev noindex).
  **www nicht gebaut:** Token hat kein Rules-Recht (Redirect-Regel), ein www-Eintrag ohne Regel
  gäbe 404 — www bleibt NXDOMAIN. Daniel: Token um *Zone → Dynamic Redirect* erweitern oder
  Dashboard-Vorlage. **Ratgeber (5 Seiten) geprüft:** sprachlich gut, aber viele konkrete
  Preis-/Rechtszahlen stehen **nicht** im `05-fact-sheet.md` (unbelegt); kein Lizenz-/Firmenname;
  Änderungen vorgelegt, nicht ausgeführt. **Mobil 390 px:** Ratgeber-Quellen-URLs + Startseiten-Band
  laufen horizontal über, Premium-Kartenrand asymmetrisch, Tippflächen klein — gemeldet, nichts
  geändert. `.gitignore` um `site.backup-*` ergänzt. Bericht
  `berichte/2026-11-05-domain-live-ratgeber-pruefung-mobil.md`.
- **2026-11-05** — Ratgeber-Zahlen bereinigt: jede unbelegte Geldzahl, jedes Aktenzeichen und
  die Innungs-/Verbandswerte raus, nur VZ (~100/~180 €) und Warentest (65–415 €) bleiben;
  der Widerspruch „167,60–209,50" vs „167,60/177,00" als erfundene, nach `konventionen`
  unzulässige Innungs-Preisliste aufgeklärt und gestrichen. **Zahlenprüfung** gebaut
  (`lint_copy.py --facts`, Gate `zahlen_im_faktenblatt`): Euro/Prozent/Jahr/Aktenzeichen einer
  Ratgeberseite müssen im `05-fact-sheet.md` stehen, Normen/mm/112/110/KfW ausgenommen; alle 5
  Seiten bestehen. **Mobil 390 px** vier Befunde behoben (Tippflächen ≥44 px, Ratgeber-URL-Umbruch,
  Startseiten-Band, Premium-Kartenrand), kein Überlauf mehr, gebaut aber nicht ausgeliefert.
  www weiter blockiert (Token ohne Dynamic-Redirect-Recht). Bericht
  `berichte/2026-11-05-ratgeber-zahlen-mobil-fixes.md`.
- **2026-11-05** — Stripe-Vorbereitung. **/danke/** gebaut (noindex, nicht in Sitemap, nicht im
  Fuß; `/danke/` zu `noindexPaths` in `load.mjs`), bereit als Weiterleitungsziel. **Brutto-Preise:**
  `tiers.vatNote` „inkl. 19 % USt." in `site.json` als eine Quelle, gedämpfte Unterzeile auf
  /premium/ (3 Stufen) und im Premium-Band (freie Karte + Fußzeile). Zwei Netto-Sätze auf Brutto
  gedreht (/premium/ „Preise und Vertragspartner", AGB B3: „Alle Preise sind Bruttopreise …19 %"),
  B2B-Verkaufsbeschränkung in AGB Teil B ausdrücklich. **Eintragsseiten: kein Preis** (Entscheidung,
  Begründung in `monetization-slots.md`). Gebaut, ausgeliefert, live bei 1440/390 px geprüft.
  Stripe-Links kommen später von Daniel, nicht vorbereitet. Bericht
  `berichte/2026-11-05-stripe-vorbereitung-danke-brutto.md`.
- **2026-11-06** **Festpreis-Garantie: Grundpreis + Zuschläge statt zwei Pauschalpreisen.**
  `garantie_tag` = Grundpreis werktags (Bedeutung bleibt), `garantie_nacht` **stillgelegt**
  (nicht umbenannt; Migrations-Riegel in beiden `load.mjs` bricht bei gefüllter Zelle ab), zwei
  neue sprechende Spalten `garantie_zuschlag_abend` und `garantie_zuschlag_nacht`. Zeitfenster
  lückenlos: Grundpreis Mo–Fr 7–20, Zuschlag abend Mo–Fr 20–24 + Sa/So/Feiertag 7–24, Zuschlag
  nacht täglich 0–7 — höchstens ein Zuschlag, nicht addiert. Preisblock jetzt drei Gruppen
  (Dienstleistung · Zuschläge mit Zeile „Zuschläge werden nicht addiert" · Material). Stadtkarte
  und Nachweis unverändert („Türöffnung ab `<garantie_tag>` €"). Angeglichen: beide `load.mjs`,
  beide `Garantie.astro`, `global.css`, `listings.csv` (migriert), beide Antragsformulare,
  `claim.ts`, `clean_listings.py`/`add_own_listings.py`/`merge_enriched.py`, `konventionen.md`,
  `siegel-programm.md` und die übrigen Wiki-/Doku-Seiten. Gebaut (4629 Seiten, Riegel grün),
  ausgeliefert, Preisblock bei 390/1440 px mit geflaggtem Fremdeintrag geprüft (danach
  zurückgesetzt), `check_live.py` bestanden außer bekannter www-Umleitung. Noch kein Preis
  eingetragen. Stripe-Links ohne Zuordnung, nicht vorbereitet. Bericht
  `berichte/2026-11-06-garantie-grundpreis-zuschlaege.md`.
- **2026-11-06** **Stripe-Links eingetragen, erste Festpreis-Garantie (Mannheim).** Die drei
  Zahlungslinks in `site.json` zugeordnet (premium 97 € → …1VK02, bestOf 250 € → …1VK00,
  city 29 € → …1VK01); auf `/premium/` Preis für Preis geprüft, kein vertauschter Link. Die
  `/danke/`-Weiterleitung setzt Daniel je Link in Stripe selbst (Payment Link → After payment →
  Redirect → `/danke/`). **Garantie** für Merz Sicherheit (5,0/355) und AES Schlüsseldienst
  Mannheim (keine Bewertungen, Voraussetzung 4: übrige entscheiden): `geprueft=true`,
  `geprueft_jahr=2026`, `garantie_tag=89`, Zuschläge +30/+40, Anfahrt 0, Zylinder 39/+3. Beide
  Eintragsseiten mit vollem Preisblock, beide Stadtkarten mit „Türöffnung ab 89 €". Nebenbefund
  behoben: `FeaturedBand` zeigte keine Garantie-Zeile (Merz erster Betrieb mit Premium-Platz +
  Garantie) → `<Garantie mode="card">` eingefügt; dabei Template-Drift des `FeaturedBand`
  (fehlende `vatNote`/`Star` aus Aufgabe B) auf die Build-Fassung geglättet. Mannheimer
  Reihenfolge belegt die Regel: Merz oben allein über den bezahlten Platz, AES (owned +
  geprueft, score 0) ganz unten (#18). Gebaut, ausgeliefert, live geprüft außer www-Umleitung.
  Bericht `berichte/2026-11-06-stripe-links-und-erste-garantie-mannheim.md`.
- **2026-11-06** **Festpreis-Garantie für 16 weitere eigene Betriebe** (Heidelberg, Hockenheim je
  2; Ludwigshafen, Schwetzingen, Worms, Weinheim, Speyer, Wiesloch, Waghäusel, Frankenthal,
  Bensheim, Sinsheim, Neustadt, Landau). Überall `geprueft=true`, 2026, Zuschläge +30/+40,
  Anfahrt 0, Zylinder 39/+3; Grundpreis gestaffelt: 89 € (6), 99 € (7), 119 € (3). Zuordnung
  über Name **und** Ort (zwei Orte mit je zwei eigenen Betrieben), jede Zeile eindeutig. Geprüfte
  Betriebe gesamt jetzt 18. **Nicht eingetragen** (Voraussetzung 2, keine Telefonnummer): Ried
  Schlüsseldienst Viernheim, Türklar Schlüsseldienst Leimen, Lampertheimer Schlüsseldienst. Vor
  Auslieferung alle 16 Grundpreise im Build gegen die Vorgabe geprüft (0 Fehler, 119-€-Orte
  stimmen), nach Auslieferung je Stadt live die „Türöffnung ab … €"-Zeile mit richtigem Betrag,
  Preisblock-Stichprobe Sinsheim (119 €). `check_live.py` grün außer www-Umleitung. Bericht
  `berichte/2026-11-06-garantie-16-eigene-betriebe.md`.
- **2026-11-06** **www-Weiterleitung eingerichtet** (301, Pfad und Query erhalten). Token hat jetzt
  „Dynamic URL Redirect · Edit". Über die Cloudflare-API: www hatte keinen DNS-Eintrag → proxied
  CNAME `www` → `schluesseldienste-deutschland.pages.dev` angelegt; Redirect-Regel in der Phase
  `http_request_dynamic_redirect` (Ausdruck `http.host eq "www.…"`, 301, Ziel
  `concat("https://die-besten-schluesseldienste.de", http.request.uri.path)`,
  `preserve_query_string: true`). Live mit `curl -I` geprüft: nackte www-Startseite, `/mannheim/`,
  tiefe Stadtseite und Adresse mit Abfrageparameter — je 301 mit erhaltenem Pfad/Query.
  `check_live.py`: alle Prüfungen bestanden, www-Zeile grün. (Lokaler Resolver hielt noch 30 min
  negativen Cache; Prüfung über die echten Cloudflare-Anycast-IPs geführt, öffentliches DNS löst
  www bereits auf — reine Propagationsfrage, kein Konfigurationsmangel.) Konfiguration liegt in
  Cloudflare, keine Repo-Code-Änderung. Bericht `berichte/2026-11-06-www-weiterleitung.md`.
- **2026-11-06** **Gate 6 begonnen — Ist-Stand und `06-launch.md`** (noch nichts an der Sitemap
  geändert). Build 4646 Seiten, Sitemap 2806 (Startseite 1, Vertrauensseiten 2, Bundesländer 16,
  Stadtseiten 577 von 787, Leistungsseiten 7, Ratgeber 6, Eintragsseiten 2197 von 3799); noindex
  1840 (1602 dünne Einträge, 210 Einzeleintrag-Stadtseiten, 18 `/auszeichnung/`, ~11
  Formular-/Pflichtseiten). `featuredPreview` im ausgelieferten Build nachweislich **false** (0
  Vorschau-Karten, 804 „Dieser Platz ist frei"); 404.html und _headers (pages.dev-noindex)
  vorhanden. **Befund:** 17 der 18 Garantie-Betriebe stehen auf noindex (thin & !claimed &
  !optimized in `load.mjs:550`); nur Merz Sicherheit Mannheim in der Sitemap. Plan schreibt die
  `geprueft`-Ausnahme (`&& !l.geprueft`) als den Start sperrende Vorbedingung fest (Sitemap dann
  2806 → 2823), noch nicht umgesetzt. Indexierungsplan ohne Search Console/Analytics (Sitemap via
  robots.txt, IndexNow/Crawler Hints, Cloudflare-Auswertung), geordnete Adressliste (18
  Garantie-Seiten vorgezogen), vier Erweiterungsstufen, 30-Tage-Prüfung Starttag+30. Bericht
  `berichte/2026-11-06-gate6-schlanker-start.md`.
- **2026-11-06** **Garantie-Ausnahme mit Inhaltsschranke umgesetzt + Start-Checks.** Inhaltsprüfung
  der 18 Garantie-Seiten: 9 praktisch leer (0 Wörter, 0 Merkmale — AES Mannheim, I-S-E Hockenheim,
  Mein Weinheim, Merz Ludwigshafen/Speyer/Worms, Rheinpfalz Frankenthal, Riegelklar Schwetzingen,
  Sperber Heidelberg), 9 mit Inhalt (120–134 Wörter). `load.mjs` (Build + Template):
  `thin && !claimed && !optimized && !(geprueft && description)` — eine geprüfte Seite entgeht der
  Sperre nur mit Beschreibung. Sitemap 2806 → **2814** (+8; Merz Sicherheit war schon drin); 9
  Garantie-Seiten indexiert, 9 leere bleiben noindex. Live bestätigt (robots-Meta + Sitemap),
  `check_live.py` mit 2814 alle bestanden. `launchDate`/`datePublished` auf Staffel-Starttag
  **2026-11-09** gesetzt (30-Tage-Prüfung 2026-12-09). Einwilligungs-Check mit leerem Browserprofil:
  Startseite, Stadtseite, Eintragsseite laden ohne Klick **keine** externe/Google-Anfrage; Karte
  erst nach Klick (`maps.googleapis.com`), Schriften selbst gehostet. Startsperren in `06-launch.md`
  abgehakt. Bericht `berichte/2026-11-06-garantie-ausnahme-und-start-checks.md`.
- **2026-11-06** Die **neun leeren Garantie-Seiten** über den Gate-3-Weg angereichert (sie kamen
  über `eigene-betriebe.csv` nach, nie durch Gate 3). Belege allein aus den eigenen Websites
  (kein Export-Text): `fetch_sites`, `build_evidence`, `make_batches` (1 Stapel, 9 Einträge,
  ~14.800 Token), inline beantwortet (kein Extra-API-Aufwand statt ~36 Cent über Sonnet).
  Dieselben Gate-3-Regeln ohne Ausnahme, **kein werblicher Ton** für die eigenen Betriebe; alle
  neun Satzanfänge 0-mal bei den bestehenden 2.197. `merge_enriched.py`: nach einer Nachbesserung
  (Wortspanne, „am Telefon"/„nach eigener Darstellung" raus, Sperber-Anfahrt mit Trace,
  Ludwigshafen-Gewerbe auf „keine Angabe") **9/9 bestanden**. Felder in Site-CSV und
  `03-listings-enriched.csv` übertragen, Garantie-Spalten unberührt, neu gebaut und ausgeliefert.
  **Sitemap 2814 → 2823** (genau die neun), `check_live.py` mit 2823 grün, jede Seite live
  `index, follow`. Alle 18 Garantie-Betriebe tragen jetzt Inhalt. Bericht
  `berichte/2026-11-06-garantie9-anreicherung.md`.
- **2026-11-06** **Ähnlichkeitsprüfung der 18 Garantie-Beschreibungen gegeneinander** (die
  Zusammenführung hielt die neun neuen nur gegen die 2.197, nicht untereinander). Methode von
  `check_city_copy.py`: Sätze ab neun Wörtern, Name/Stadt entfernt, Jaccard der Wortmengen,
  Schwelle 0,75. **Genau ein Muster über der Schwelle**: der Schlusssatz „ein Monteur ist … in
  etwa einer halben Stunde vor Ort" (Frankenthal, Ludwigshafen, Worms wörtlich, Speyer als
  Variante) – die einzigen Paare ≥0,75, nächsthöchstes 0,67. Nur diese vier neu geschrieben, je
  mit einer Anfahrts-Tatsache aus dem eigenen Paket; dabei auch „Anfahrtskosten … nach Ort
  gestaffelt" (3×) auf 1× gesenkt. Generische Fachausdrücke (24h, Zylinder ziehen) unverändert,
  keine über 0,75. Nachkontrolle: **kein Paar mehr ≥0,75** (Max 0,67), `merge_enriched.py` 9/9.
  Vier Beschreibungen in beide CSVs übertragen (Merkmale/Garantie unberührt), neu gebaut und
  ausgeliefert, Sitemap unverändert 2823, `check_live` grün, die vier live mit neuem Text.
  Bericht `berichte/2026-11-06-garantie18-aehnlichkeitspruefung.md`.
- **2026-11-06** **Starttag der Staffel auf heute gesetzt.** `site.json` `launchDate`
  2026-11-09 → **2026-11-06** (vom Schema als `datePublished` genutzt). Neu gebaut (4647 Seiten),
  ausgeliefert; `datePublished` im gebauten **und** im Live-Schema = 2026-11-06. `check_live.py`
  mit 2823 alle bestanden. `06-launch.md` angeglichen: Starttag 2026-11-06, erste 30-Tage-Prüfung
  **2026-12-06**, Punkt „Staffel auslösen" als erledigt markiert (offen beim Betreiber nur noch
  der IndexNow-Ping). Bericht `berichte/2026-11-06-staffelstart-heute.md`.
- **2026-11-06** **Benachrichtigung bei Formulareingang gebaut.** `functions/api/claim.ts` schrieb
  bisher nur in KV; Pages kann kein `send_email`. Weg: schlanker Worker `notify-worker/` mit
  `send_email`-Binding, den die Function per Service-Binding `MAILER` aufruft — **kein
  Drittanbieter, kein API-Schlüssel** (deckt sich mit Datenschutz Ziffer 5, „ohne weiteren
  Dienstleister"). KV-Schreiben bleibt zuerst, Versand über `waitUntil(env.MAILER.fetch(...))` im
  Hintergrund, Function antwortet immer 303 → `?gesendet=1`. Absender Verzeichnis-Domain, Empfänger
  Daniels gewöhnliche Adresse als Pages-**Secret** `NOTIFY_TO` (nie im Repo, überdauert Deploys).
  Worker ausgeliefert (kein öffentliches Ziel), `MAILER`-Binding an der Produktion per API
  bestätigt. **Live geprüft:** echte Absendung an `/api/claim` → 303, `?gesendet=1`, KV-Eintrag
  `beansprucht:2026-11-06T11-00-52:s2c8` (gelesen, dann gelöscht). **Offen beim Betreiber** (Konto,
  nicht von mir ausführbar): Email Routing aktivieren, gewöhnliche Adresse als Destination
  verifizieren, `NOTIFY_TO`-Secret setzen; „Mail angekommen" danach. Bericht
  `berichte/2026-11-06-formular-benachrichtigung.md`.
- **2026-11-06** **Live-Mailtest beider Formularpfade bestanden.** Daniel hat Email Routing
  aktiviert, seine Adresse als Destination verifiziert, `NOTIFY_TO` als Pages-Secret gesetzt.
  Worker (mit Erfolgs-/Fehler-Logzeile, ohne Empfängeradresse) und Pages neu ausgeliefert (Secret
  greift erst mit Deploy). Je eine echte Absendung an `/api/claim` mit mitlaufendem
  `wrangler tail`. **Beanspruchung:** 303, `?gesendet=1`, KV `beansprucht:…12-15-31:go1t`, Tail
  `EMAIL.send ok` / Status 200. **Garantie-Antrag:** 303, `/festpreis-garantie/antrag/?gesendet=1`,
  KV `garantie:…12-15-31:tasj`, Tail `EMAIL.send ok` / Status 200. Genau zwei Tail-Ereignisse, beide
  ohne Exception — Email Routing hat beide Nachrichten zur Zustellung angenommen (Nachweis aus den
  Worker-Logs, nicht vermutet). Beide Testeinträge aus KV gelöscht. Bericht
  `berichte/2026-11-06-mailtest-live.md`.
- **2026-11-06** **Herausgeber aus dem Seitentext genommen, bis auf die Pflichtstellen.** „DOM
  Holding GmbH" und „Daniel Merz" aus Fuß (Fließtext + „Herausgegeben von"-Zeile, Behörde-Satz
  bleibt), Ratgeber-Byline (→ Marke), Über-uns-Fließtext (Daniel raus, Firma bleibt) und den zwei
  Art.-13-Hinweisen („(Daniel Merz)" raus, Firma bleibt) entfernt. Zusätzlich Kontakt- und
  Danke-Seite (Firmenname raus); AGB bleibt (Rechtsseite). Impressum, Datenschutz sowie
  Organization- und Person-Schema unverändert — Daniel Merz nur noch als Geschäftsführer im
  Person-Schema. JSON-LD geprüft (0 kaputte Blöcke, publisher/herausgeber/Person lösen auf),
  gebaut, ausgeliefert, check_live.py mit 2823 bestanden, live gegengeprüft. Bericht
  `berichte/2026-11-06-herausgeber-aus-seitentext.md`.
- **2026-11-10** **scripts/verkauf.py — ein Befehl für verkaufte Plätze.** Setzt die Spalte je
  Stufe (premium→`premium=true`, stadt→`featured=city`, top→`best_of_rank=1–3`, aus dem
  Datenlayer, nie die Garantie-Spalten), hält Verkauf/Ende im Hauptbuch
  `output/<slug>/verkauf-hauptbuch.csv` fest, baut, liefert aus, prüft mit check_live.py.
  `--liste` zeigt den Ist-Zustand mit „seit". Zwei Prüfungen brechen ab: Stadt-Premium je Stadt
  nur einmal; höchstens ein eigener Betrieb je Stadt auf bezahltem Platz ([[footprint-rules]]).
  Slug auf keine/mehrere Zeilen → Abbruch mit Treffern, nie geraten. Probelauf (--liste,
  Abbrüche, --entfernen auf Testwert mit Scratch-Hauptbuch, danach CSV zurückgesetzt) ohne
  Live-Änderung. Aufruf in CLAUDE.md eingetragen. Bericht
  `berichte/2026-11-10-verkauf-skript.md`.
- **2026-11-10** **Stadt-Premium: drei Plätze je Stadt, Reihenfolge nach Buchung.** `featured=city`
  bis zu dreimal je Stadt; neue CSV-Spalte `featured_seit` (Buchungsdatum), `load.mjs`
  (`orderFeaturedBand`) ordnet das Band danach (früheste oben, fehlendes Datum wird gemeldet),
  `FeaturedBand.astro` zeigt je freiem Platz eine Frei-Karte. `scripts/verkauf.py`: Sperre erst ab
  dem vierten Stadt-Platz (nennt die drei Halter), setzt/leert `featured_seit`, Footprint streng
  (zweiter eigener Betrieb bricht ab, [[footprint-rules]] geschärft), meldet fehlende Daten, laute
  „NICHT AUSGELIEFERT"-Meldung bei `--kein-deploy`/`--kein-bauen`. Merz Mannheim im Hauptbuch auf
  2026-11-06 datiert. `/premium/` umgeschrieben (bis zu drei, nach Buchung; Textgate bestanden).
  Live geprüft: Mannheim Merz oben + 2 frei, Leipzig 3 frei, check_live 2823 bestanden. Bericht
  `berichte/2026-11-10-stadt-premium-drei-plaetze.md`.
- **2026-11-10** **Premium-Band: eine Frei-Karte je Stadt, und Rückport ins Template.** (1) Hinter
  den verkauften Plätzen steht wieder höchstens **eine** „Dieser Platz ist frei"-Karte, nicht eine
  je offenem Platz (`FeaturedBand.astro`) — sonst würden 787 Stadtseiten zu Anzeigenseiten. Live
  geprüft: Mannheim Merz + 1 Frei, Leipzig 1 Frei, lokal drei verkauft → 0 Frei; check_live 2823
  bestanden, ausgeliefert. (2) Rückport nach [[template-build-drift]]: `FeaturedBand.astro`
  (Textzeile) und `premium.astro` (ganz, generisch) → Template == Build; `load.mjs` hunkweise
  (`orderFeaturedBand`, `featuredSince`). `featured_seit` liest das Template tolerant.
  template-build-drift.md fortgeschrieben (Abschnitt + Sorte-A-Zeile, 2026-11-10). Bericht
  `berichte/2026-11-10-premium-band-eine-freikarte-und-template-rueckport.md`.
- **2026-11-10** **Rückport ins Template: sanitizeGlyphs und normalizeHours.** Die zwei
  Fehlerbehebungen hunkweise nach `templates/astro/src/lib/load.mjs` ([[template-build-drift]]):
  `sanitizeGlyphs`+`GLYPH_OK` (auf name/address/street/description) und die
  Öffnungszeiten-Behandlung in `normalizeHours` (DataForSEO-Array → Text, leerer Tag →
  „Geschlossen"). `featured=state`-Band **bewusst draußen** — Entscheidung dieses Verzeichnisses,
  keine Korrektur; ebenso unangetastet BOM-Regex und `/danke/`-noindex, offen bleibt
  fonts.css-latin-ext. Verbleibender Diff = nur die drei ausgelassenen Hunks; node --check grün;
  normalizeHours funktional getestet. template-build-drift.md fortgeschrieben (zwei als ✓
  zurückportiert, featured=state als bewusst nicht portiert mit Grund). Build unverändert, kein
  Deploy. Bericht `berichte/2026-11-10-template-rueckport-glyph-oeffnungszeiten.md`.
- **2026-11-10** **fonts.css im Template auf Build-Stand (latin-ext).** Die vier
  latin-ext-Importe (@fontsource/roboto + roboto-slab) nach `templates/astro/src/styles/fonts.css`
  zurückportiert; `fonts.css` ist Template == Build. Damit ist das Glyph-Thema vollständig
  zurückportiert. template-build-drift.md: Sorte-A-Zeile „Glyph-Bereinigung + latin-ext" als ✓
  vollständig markiert, Prosa ergänzt.
- **2026-11-12** **Design-Pilot 1 (Branch `design/pilot1`, nicht freigegeben).** Sichtbarer
  Gestaltungs-Pilot für Startseite und Mannheimer Stadtseite, Desktop und mobil, auf den bestehenden
  Marken (Farben/Schriften unverändert) plus vier aus den PNG-Referenzen abgeleitete Marken
  (`--card-radius`, `--card-shadow`, `--space-section`, `buttonRadius`=Pille). Zweispaltiger Hero mit
  Übersichtskarte aus echten Daten; zweigeteilter Stadt-Ergebnisbereich mit Orientierungsspalte und
  Zeilenkarten; Suche als Pille mit Lupe und sichtbarer Beschriftung; Fokusring; zugängliches mobiles
  Menü (Checkbox). Vergleich gegen den Ausgangsstand: 0 Abweichungen bei Titel/Description/Canonical/
  robots/H1/JSON-LD über alle 4647 Seiten, Linkziele erhalten, Sitemap 2823; kein Überlauf 320–1440;
  Textgate bestanden. Kein Deploy, kein Merge nach main, kein Rückport. Bericht
  `berichte/2026-11-12-design-pilot1.md`, Rückgabe `design-pilot1/rueckgabe-henry.md`.
- **2026-11-12** **Teil A (main, live):** Stadtseiten-Liste richtig sortiert und vollständig.
  `sortListings` setzt jetzt die volle Konventions-Reihenfolge um (bezahlt → Festpreis-Garantie
  `geprueft` → [Ortsbezug, nicht umgesetzt: keine Vorwahl↔PLZ-Referenz] → Rest); Git-Verlauf zeigt,
  die Gruppen 2/3 waren nie im Code. Band-Einträge stehen zusätzlich in der Liste und Sprungliste
  (A2), Sprunganker nur auf der Listenkarte (keine doppelten id), `maxCardsPerCity` zählt sie mit.
  Bundesland-Seiten (nur Städte-Liste) und Startseite (nationales Band leer) unverändert. Mannheim
  live: Merz, AES, Key Walter. Gebaut, mit wrangler ausgeliefert, `check_live.py` 2823 grün.
  Rückport ins Template, 04-plan (Entscheidung A2). Bericht
  `berichte/2026-11-12-stadtseiten-sortierung-und-band.md`.
- **2026-11-12** **Design-Pilot 1 freigegeben (Teil B, main, live).** `main` (Teil A) in
  `design/pilot1` geholt (Stadtseite auto-gemergt: A2 + Pilot-Layout beide; `04-plan.md` doppelte
  Überschrift von Hand zusammengeführt). Screenshot-Prüfung von acht Seitentypen (Desktop 1440 +
  mobil 390): keine Pilot-Brüche, kein Überlauf 320–1440, Menü klappt überall. Ein vorbestehender
  Befund (nicht Pilot): `public/search.js` zeichnet die Sterne der Suchergebnisse als Textzeichen
  `★`/`☆` (Tofu, auf `main` zeichengleich) — Merge nicht blockiert, als eigener Fix offen.
  `design/pilot1` → `main` (Fast-Forward), gebaut, mit wrangler ausgeliefert, `check_live.py` 2823
  grün; live geprüft (Startseite, Mannheim = Merz/AES/Key Walter, Merz-Eintrag ohne Fremd-Host vor
  Karten-Klick, beide Formulare, Suche 1 Treffer). Gestaltung hunkweise ins Template zurückportiert
  (pilot-eigene Hunks Fork `11f8445`→`2c1e118`; aufgeschobene Vor-Pilot-Drift außen vor); dabei den
  vorbestehenden, nicht mehr baubaren Template-Zustand behoben (`FeaturedBand` brauchte das nie
  mitportierte `Star.astro` — jetzt mit dabei). `template-build-drift.md`-Eintrag „Design-Pilot 1"
  auf freigegeben/portiert gesetzt. Worktree `blueprint-pilot1` entfernt, Branch steht. Berichte
  `berichte/2026-11-12-design-pilot1-freigabe.md`.
- **2026-11-12** **Sortierung offengelegt, Premium aus Stufe 0, /suche/-Sterne (main, live).**
  (1) Die neue Reihenfolge (bezahlte Plätze → Festpreis-Garantie → Rest) wird jetzt genannt:
  sichtbare Zeile unter „Die besten …" auf der Stadtseite (Textgate ohne --erlaube-rechtswoerter
  bestanden), Ersatz-Vorspann berichtigt, Absatz auf /festpreis-garantie/, lede auf /premium/
  berichtigt. Weitere Fundstellen genannt, nicht geändert (Bundesland-lede, FeaturedBand,
  Stadtseiten-Meta-Description); Über uns, Startseiten-Liste, Leistungsseiten, FAQ, Ratgeber geprüft
  und korrekt. (2) `l.premium` aus `sortListings` Stufe 0 entfernt (Stufe 0 = Stadt-Premium +
  Top-Platzierung); Build und Template. Mannheim unverändert (Merz hält Stadt-Premium über
  `featured='city'`), kein reiner Premium-Eintrag in der CSV. (3) `public/search.js` zeichnet die
  Sterne jetzt als Inline-SVG wie Star.astro (beide Render-Pfade), Build und Template; live geprüft
  (SVG-Sterne, kein Tofu). Gebaut, ausgeliefert, check_live.py 2823 grün. Bericht
  `berichte/2026-11-12-sortierung-offenlegen.md`.
- **2026-11-12** **Offenlegung abgeschlossen: drei Reststellen + Template-Nachtrag (main, live, cfbc517b).**
  Die drei genannten Stellen berichtigt, überall die Reihenfolge der Sortierzeile (bezahlte Plätze →
  Festpreis-Garantie → Rest nach Bewertung): Bundesland-lede, FeaturedBand-Frei-Karte und die
  Stadtseiten-Meta-Description. Meta-Description Mannheim 265 → 148 Zeichen (unter Googles ~160;
  on-page-rules gibt keine Description-Länge vor, nur Titel ≤ 60); der bestbewertete Betrieb entfällt,
  um unter 160 zu bleiben. Textgate an den gebauten dist-Seiten: Stadt (Mannheim) und Bundesland (BW)
  BESTANDEN ohne --erlaube-rechtswoerter; /premium/ BESTANDEN mit Flag; /festpreis-garantie/
  DURCHGEFALLEN nur an vorbestehenden Punkten (Build-Datei == HEAD, mein Absatz fügt 0 Gedankenstriche
  hinzu). Template-Nachtrag: alle Copy-Änderungen der vorigen Runde fehlten im Template (Sortierzeile,
  Ersatz-Vorspann, Meta, Festpreis-Absatz, /premium/-Sätze) und wurden mit den drei Stellen
  nachgetragen; Template baut grün, Build und Template gleicher Stand. check_live.py 2823 grün,
  Live-Stichprobe bestätigt. Bericht berichte/2026-11-12-offenlegung-abschluss.md.
- **2026-11-12** **Neue Stadtseiten-Meta, /festpreis-garantie/ durchs Textgate, Wiki-Zeile (main, live, 5eaf0d86).**
  (1) Stadtseiten-Meta neu gefasst: die Reihenfolge-Formel raus aus dem Suchtreffer, stattdessen Zahl +
  Stadt (ohne Bundesland, ohne Spitzenbetrieb) plus „Wer nennt vorab seinen Preis für die Türöffnung, wer
  nicht?". Gilt auf jeder Stadtseite. Über alle 787 gemessen: kürzeste 133 (Hof), längste 156 (Neustadt
  a.d.W.), 0 über 160. Textgate Mannheim ohne --erlaube-rechtswoerter BESTANDEN. Frageform statt Aussage,
  weil die Aussageform bei den längsten Namen die 160 riss. Build und Template. (2) /festpreis-garantie/
  durchs Textgate (mit Flag): 11 Gedankenstriche durch Satzbau ersetzt (5 Zeitbereiche 7–20/0–7 → „bis",
  6 frei stehende → Komma/Satzteilung); Branchenwort ins H1 (der Linter prüft den ersten Block = H1) und
  in den ersten Absatz; Zitat „ab 49 Euro" (verbotene Lockangebot-Floskel, forbidden_words.txt:122)
  sinnerhaltend zu „niedriger Lockpreis am Telefon" umformuliert. Tatsachen unverändert. Build und
  Template, beide BESTANDEN. (3) wiki/seo/on-page-rules.md:85 (nicht framework/) auf die Reihenfolge
  gebracht: Kartenabschneidung „bezahlter Platz, dann Festpreis-Garantie, dann Bewertung". check_live.py
  2823 grün, Live-Stichprobe bestätigt. Bericht berichte/2026-11-12-meta-und-festpreis-textgate.md.
- **2026-11-12** **Widerspruch zur Platzierung auf /festpreis-garantie/ aufgelöst (main, live, 68d052dc).**
  Der Abschnitt über bezahlte Sichtbarkeit sagte „wer eine Garantie hat, bekommt dadurch keinen besseren
  Platz", der Reihenfolge-Absatz sagt das Gegenteil. Neu an beiden Stellen (festpreis und premium): Wer
  zahlt, bekommt keine Garantie; wer die Garantie hat, bekommt keinen der bezahlten Plätze; die Garantie
  hebt einen Betrieb vor die ohne Garantie, aber nie über einen bezahlten Platz, und ist nicht käuflich.
  Site-weite Suche: zwei echte Treffer (festpreis, premium.astro:52) berichtigt; agb.astro:37 nur
  gemeldet, nicht geändert (nur „nicht kaufbar", kein Widerspruch); antrag:190, ueber-uns:47, site.json-FAQ
  geprüft und korrekt. Build und Template; Textgate beider Seiten mit Flag BESTANDEN; check_live.py 2823
  grün. Bericht berichte/2026-11-12-widerspruch-platzierung.md.
- **2026-11-12** **Zwei Mannheimer Einträge entfernt (Betreiberentscheidung, main, live, 9f0ec5a5).**
  Ausschluss nach [[conduct-exclusions]] mit dem Code verhalten_betreiber in 04-exclusions.csv (beide
  Slugs trafen genau eine Zeile), danach die zwei Zeilen CSV-sicher aus listings.csv entfernt (Garantie-
  und Verkaufsdaten intakt). Fundstellen: nur der Mannheim-Stadttext in city-copy.json nannte die beiden
  (Intro + zwei FAQ); alles andere (Eintragsseiten, Kartenliste, Suchindex, Sitemap, Kennzahlen) erzeugt
  sich aus listings.csv neu. Ein gleichnamiger, eigener Betrieb in Essen (tuerengel-schluesseldienst-24-7-
  essen) bleibt samt Essen-Stadttext unberührt. Mannheim-Stadttext auf dem vorgesehenen Weg neu (frisches
  17er-Paket, check_city_copy --only bestanden, --write, Textgate Mannheim BESTANDEN); nur Mannheim
  geändert, 786 Städte identisch. Neu gebaut: Mannheim 17 Einträge (2 geprüft, 4,8 aus 1.593), Spitze
  Merz/AES/Key Walter, beide Eintragsseiten weg, kein interner Link mehr, Sitemap 2823 -> 2821.
  Ausgeliefert, check_live.py 2821 grün, beide Adressen 404, Suche findet die beiden nicht mehr.
  06-launch.md auf 2821 nachgezogen. Bericht berichte/2026-11-12-mannheim-zwei-ausschluesse.md.

- 2026-11-13 — listings.csv als alleinige Quelle der operativen Spalten festgelegt und gegen
  Überschreiben gesichert. Ausmaß: enriched (4387×80) vs Build-listings.csv (3797×82) — 18
  Garantien (geprueft + 6 Preisspalten) und Merz' Mannheimer Platz (featured=city, premium=true,
  featured_seit) stehen nur im Build, enriched hat sie leer; Schema-Divergenz (abend/nacht-Zuschlag
  vs garantie_nacht, featured_seit). Neues Modul scripts/_listings_guard.py: merge_protected()
  trägt die operativen Spalten beim Neulauf per Slug aus der bestehenden CSV zurück,
  pruefe_kein_verlust() bricht ab, wenn eine bleibende Zeile einen gefüllten Wert verlöre, und
  nennt die Einträge. Verdrahtet in apply_exclusions.py (Rücktrag + Sperre + Warnung bei Ausschluss
  mit Garantie), verkauf.py und add_socials.py. Probe: Vollneulauf in eine Kopie — 3797 Zeilen, alle
  18 Garantien identisch, Merz-Platz erhalten; Gegenbeweis: ohne Rücktrag bricht die Sperre ab und
  nennt 18 Einträge. Quelle+Sperre in CLAUDE.md festgehalten. Nebenbefund: lint_copy.py auf
  city-copy.json — die 725 Durchfaller behebt --city-sizes mit einer nach <bundesland>/<stadt>
  verschlüsselten Größenkarte (725 -> 0), nichts geändert, Vorschlag zur Aufnahme in copy-gate offen.
  Kein Deploy. Bericht berichte/2026-11-13-listings-quelle-und-sperre.md.

- 2026-11-13 — --city-sizes fest ins Textgate für city-copy.json aufgenommen. lint_copy.py bekam
  --cities <05-cities.json>: baut die Größenkarte regionSlug/slug -> count bei jedem Lauf frisch
  (keine zu pflegende, veraltende 05-city-sizes.json mehr) und erzwingt beim Lauf auf city-copy.json
  eine Größenquelle — fehlt sie, FEHLER/Abbruch; fehlt eine Stadt aus city-copy.json in der Karte,
  ABBRUCH, der sie nennt (kein stiller Rückfall auf die generische Wortspanne). Der eigentliche
  Fehler hinter den 725 Durchfallern: die bisher vorgeschriebene 05-city-sizes.json war nach dem
  bloßen slug verschlüsselt statt bundesland/stadt und traf nichts. copy-gate, CLAUDE.md (Gate 5)
  und page-types auf --cities umgestellt. Voller Textgate-Lauf über city-copy.json: 787 bestanden,
  0 durchgefallen (die 725 waren Fehlalarme; keine echten Befunde), deckungsgleich mit
  check_city_copy.py. Kein Deploy. Bericht berichte/2026-11-13-textgate-city-sizes-fest.md.

- 2026-11-13 — Zwei Änderungen (Build + Template, Deploy ff729a59, check_live 2821 grün).
  (1) Mannheim fest auf die Startseite: neue Liste site.json pinnedCities (Stadtschlüssel
  regionSlug/slug), DirectoryHub garantiert diese Städte in der 20er-Auswahl, Gesamtzahl bleibt 20,
  Rest nach Eintragszahl. Mannheim lag mit 17 auf Rang 21 (Bonn hält Rang 20, alphabetisch davor);
  nach dem Pin steht Mannheim an Stelle 20, Bonn weicht (live geprüft). (2) Der gefolgte Link folgt
  der Festpreis-Garantie, nicht der Bezahlung: auf der Eintragsseite und in SocialLinks jetzt
  linkRel — geprueft -> rel="noopener" (Website + Profile ohne nofollow), bezahlter Platz ohne
  Garantie -> rel="sponsored", sonst nofollow; owned wird nicht gelesen. Build: Website-Links ohne
  nofollow 2 -> 36 (= 18 Einträge x 2, alle geprüft), sponsored 0 (Merz ist geprüft), Rest nofollow.
  Texte: /premium/ „alle Links ohne nofollow" gestrichen (sponsored statt nofollow; ohne nofollow
  nur mit Garantie), /festpreis-garantie/ Satz ergänzt (Garantie -> Link ohne nofollow). Textgate
  gebaut: /premium/ BESTANDEN (auf 396 Wörter gekürzt), /festpreis-garantie/ Inhalt BESTANDEN,
  einzig die weiche Obergrenze 1200 überschritten (1512, vorbestehend, +24 durch den Satz) — nicht
  umgeschrieben, Empfehlung den copy-gate-Richtwert dieser Seite anheben. Weitere Fundstellen der
  alten Regel: featured-tiers.md und monetization-slots.md geändert; AGB nur gemeldet (kein
  Follow-Versprechen, A3 deckt sich mit sponsored); die rulebeschreibenden Wiki-Seiten (on-page-rules,
  site-architecture, page-types, siegel-programm, authority-and-links, footprint-rules, README)
  genannt, nicht geändert (Quelle ist konventionen). Regel nicht in konventionen eingetragen, Wortlaut
  vorgeschlagen (Daniel ändert die Datei frei). Bericht berichte/2026-11-13-mannheim-pin-und-follow-garantie.md.
- **2026-11-13** **Website-Links nur für geprüfte, freigeschaltete und zahlende Einträge (main, live, 0c5579bc).**
  Betreiberentscheidung. Neue Spalte `link_follow` (wahr/leer) in `site/src/data/listings.csv`, in
  `PROTECTED` von `_listings_guard.py` aufgenommen, einmalig aus `owned=true` geseedet → 21 Einträge
  auf `true`. Regel in `load.mjs` (`websiteRel`): geprüft oder `link_follow` → gefolgter Link ohne
  nofollow/sponsored; bezahlter Platz ohne beides → `rel="sponsored noopener"`; alle übrigen → **kein**
  Website- und kein Profil-Link (leerer `websiteRel`), `owned` wird nicht gelesen. Eintragsseite:
  Website-Link (2×) und `SocialLinks` an `websiteRel` gekoppelt; Verkaufshinweis im Beanspruchen-Kasten
  bei Einträgen ohne Link (Verweis auf /festpreis-garantie/ und /premium/). JSON-LD an Regel 2
  angeglichen (Betreiberwahl, erst Option 2, dann korrigiert auf Option 1): `url` = Website nur bei
  `websiteRel`, sonst eigene Eintragsseite; `sameAs` nur bei `websiteRel`. Nachher im Build: 42
  sichtbare Website-Links (21×2) `noopener`, 0 sponsored, 0 nofollow, 3776 Einträge ohne Link; JSON-LD
  21 extern / 3776 intern, `sameAs` nirgends (qualifizierte Einträge ohne Socials). Texte: /premium/
  (Link gehört zu jeder bezahlten Stufe, als bezahlt gekennzeichnet; auf 394 Wörter getrimmt, Textgate
  bestanden), /festpreis-garantie/ (unverändert, bestanden), /eintrag-beanspruchen/ (Link kommt mit
  Garantie/Premium), FAQ „Kostet ein Eintrag Geld?" in site.json, Startseite bestanden. Wiki: on-page-rules,
  site-architecture, page-types, siegel-programm, authority-and-links, monetization-slots, README,
  featured-tiers.md geändert; footprint-rules: Ausnahme offen eingetragen (einzige Ausnahme = Link-
  Freischaltung über `link_follow`, 2026-11-13); copy-gate Garantie-Band auf 700–1.600 angehoben. AGB
  nur gemeldet. konventionen nicht eingetragen, Wortlaut vorgeschlagen. Live-Stichprobe (Merz, AES, Ried
  Viernheim ohne Garantie, Key Walter + Atilla Mannheim fremd, AOS Hamburg fremd) bestätigt die Regel.
  check_live 2821 bestanden. Bericht berichte/2026-11-13-website-links-geprueft-freigeschaltet-zahlend.md.
- **2026-11-13** **Link-Regel: drei Abschlüsse (main).** (1) Absatz „Website- und Profil-Links auf
  Eintragsseiten" auf ausdrückliche Betreiberfreigabe in `wiki/konventionen.md` eingetragen (nach
  „Darstellung im Eintrag", vor „Stadtkarte"), mit Datum 2026-11-13; sonst nichts an der Datei. (2) AGB
  auf Umfang eines Eintrags / einer bezahlten Stufe durchgesehen (nichts geändert): nur **B1,
  Premium-Eintrag** passt nicht mehr vollständig — „Verlinkung … **ohne Suchmaschinen-Einschränkung**"
  trifft einen bezahlten Platz ohne Garantie/`link_follow` nicht, der jetzt `rel="sponsored"` (also
  gekennzeichnet) trägt; A3, B5, B7, Teil-B-Einleitung bleiben stimmig. (3) Ab jetzt wird `main` nach
  jedem Commit gepusht, ohne Aufforderung. Kein Deploy (reine Text-/Regelarbeit).
- **2026-11-13** **AGB B1 (Premium-Eintrag) an die Link-Regel angepasst (main, live, ee8524e7).**
  Betreiberfreigabe für genau diese Stelle. „Verlinkung … ohne Suchmaschinen-Einschränkung" →
  „… als bezahlte Platzierung gekennzeichnet", plus Satz, dass ein Link ohne diese Kennzeichnung
  allein mit der Festpreis-Garantie verbunden und nicht Gegenstand dieser Bedingungen ist (Build und
  Template). Standdatum im Build fest auf 13.11.2026 (Template behält `{buildDateDe}`). /premium/,
  featured-tiers.md und AGB beschreiben den Premium-Eintrag jetzt deckungsgleich. Textgate /agb/ mit
  `--erlaube-rechtswoerter`: Wörter/Floskeln/Rechtswörter bestanden; einziger Befund 2 Gedankenstriche
  in den vorbestehenden Überschriften „Teil A —"/„Teil B —", nicht angefasst (nur gemeldet). check_live
  2821 bestanden. Bericht berichte/2026-11-13-agb-b1-premium-link-berichtigt.md.
- **2026-11-13** **Rückweg für Anträge: garantie.py, kontakt.py (main, kein Deploy).** (1)
  `scripts/garantie.py` nach dem Muster von `verkauf.py`: erteilen/ändern/entziehen/--liste,
  schreibt nur die Garantie-Spalten, nutzt `_listings_guard.py`, führt
  `garantie-hauptbuch.csv`, baut/liefert/prüft; Vorprüfung der sechs Voraussetzungen, soweit
  lesbar (Telefon, Bewertungsschnitt), `--bestaetigt` für die von Hand zu prüfenden; Testschalter
  und laute Schlussmeldung wie verkauf.py. (2) `scripts/kontakt.py` + anhängendes
  `kontakt-hauptbuch.csv` und `kontakt-sperrliste.csv`: eintragen/sperren/--offen/--stand; `--offen`
  ohne eigene, ohne gesperrte, ohne kontaktierte, filterbar nach Bundesland/Stadt. (3)
  Bestandsaufnahme (nur Zahlen, keine Adressen): 3797 Einträge, 97 % Telefon, 30 % E-Mail, 968
  Sammelpostfächer, 114 Mehrfach-Adressen; je Bundesland im Bericht. (4) Antwortwege von info@
  (Empfehlung: eigenes mailbox.org-Postfach ~3 €/Monat, getrennt von Websites und LeadHawk; Worker
  mit Resend/Cloudflare Email Sending als zweiter Weg) — nichts eingerichtet. Probeläufe für
  garantie.py und kontakt.py auf einer Kopie (`--kein-bauen`, nichts ausgeliefert); die 18
  bestehenden Garantien überlebten. Aufrufe in CLAUDE.md festgehalten. Bericht
  berichte/2026-11-13-rueckweg-fuer-antraege.md.
- **2026-11-13** **Ansprechpartner aus dem Impressum (main, kein Versand, kein Deploy).**
  `scripts/impressum.py`: liest je Domain einmal das Impressum (üblich `/impressum`, sonst
  Startseite + Fußlink), zieht die verantwortliche natürliche Person heraus (Inhaber,
  Geschäftsführer, „vertreten durch"), rät nie (kein Name aus E-Mail/Firmenname/Bewertung).
  Universum: Website, nicht owned und E-Mail = 1.144 Einträge auf 1.073 Domains; 60 geteilte
  Domains nicht abgerufen. Ergebnis: gefunden 558, nicht gefunden 554 (fremdes Impressum 23,
  geteilte Domain 131, keine Person lesbar 400), nicht abrufbar 32. Ergebnis und Cache
  personenbezogen und gitignoriert (`kontakt-ansprechpartner.csv`, `impressum-cache.json`).
  Drei Regeln: fremde Impressen/geteilte Domains aussperren (Besitzprüfung über Domain/Firmenname/
  Nachname, Ort ausgenommen); Einzelbuchstaben weg („Klaus D Mapara" → „Klaus Mapara"); Anrede
  „Hallo Vorname Nachname," bzw. „Guten Tag,". Export in `kontakt.py` (`--offen --export`) bekommt
  `vorname`/`nachname`/`anrede` und **nur Kernbetriebe** (`schluesseldienst_kern` oder
  `tueroeffnung` bestätigt): von 1.144 anschreibbaren bleiben 728, 416 fallen weg (Haupt-Kategorien
  im Bericht); 348 der 728 mit persönlichem Namen. `listings.csv` und Verzeichnis unverändert.
  Bericht berichte/2026-11-13-ansprechpartner-impressum.md.

- **2026-11-14 — Den Export versandfertig gemacht.** `kontakt.py` um `exportieren`, `pruefen`,
  `importieren` und `--stand --kampagne` erweitert; neuer Datenschicht-Helfer
  `site/dump-versand.mjs` liefert platz/anzahl/eintrag_url/Bewertung/Telefon genau so, wie die
  Seite sie zeigt (geprüft an Stichproben gegen `dist/`, 0 Abweichungen). Adressen gesäubert
  (Hauptadresse je Eintrag, MX-Prüfung, Portal-/Zentral- und Mehrfachadressen raus, Freemailer
  drin), nur Kernbetriebe, nur Städte ohne Garantie/bezahlten Platz. National von 3.797 Einträgen
  640 versandfertig, davon 331 mit persönlicher Anrede. Kampagnen mit Name und Obergrenze
  (vorgesehen → nicht zweimal exportiert); Plattform-Ergebnisse zurücklesen (abgemeldet/unzustellbar
  → Sperrliste, Unbekanntes gemeldet, nie geraten). Platzhalter-Namen aus Muster-Impressen
  („Max Mustermann") am Rand abgefangen. `listings.csv` und Verzeichnis unverändert, nichts
  versendet/ausgeliefert. Bericht berichte/2026-11-14-versand-export.md.
