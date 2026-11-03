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
