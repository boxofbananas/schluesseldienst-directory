# Wiki-Verzeichnis

Diese Seite zuerst lesen, dann die Seiten öffnen, auf die sie zeigt. Bei jeder neuen Seite eine
Zeile ergänzen und `log.md` fortschreiben.

**Vor allem anderen:** `konventionen.md`. Bei Widerspruch zu einer anderen Seite gilt sie.

## Der Vertrag und das Protokoll
- [konventionen](konventionen.md): der verbindliche Vertrag der deutschen Fassung – Projekt,
  Domain, Herausgeber, die dreistufige URL-Tabelle, die 16 Bundesland-Slugs, Umlautregel,
  Telefon- und Öffnungszeitenformat, Sprache und Ton, die Wortliste, die Festpreis-Garantie, die
  Rechtspflichten und die Reihenfolge der zulässigen Quellen. **Nur lesen, nie ändern.**
- [log](log.md): fortgeschriebenes Protokoll jedes Gates und jeder Änderung, neueste Zeile
  unten.

## Regelwerk
- [directory-overview](framework/directory-overview.md): was dieses Verzeichnis ist, warum der
  Betreiber es baut, wie ein sauberes aussieht, die vier Punkte, in denen der deutsche Markt
  anders ist, und dass alle Messwerte aus dem englischen Pilotprojekt stammen.
- [site-architecture](framework/site-architecture.md): die drei Ortsebenen Startseite →
  Bundesland → Stadt → Eintrag, jede Adresse und was sie leistet, die Rechnung für die
  Seitenzahl, die Adressregeln samt Umlauten, die interne Verlinkung über drei Ebenen,
  Mindestzahl und `foldMaxKm`, Navigation und Fußbereich mit der Rechtszeile.
- [page-types](framework/page-types.md): jeder Seitentyp mit Pflichtinhalten und
  Wortuntergrenzen, die Bundesland-Seite als neuer Typ, Impressum und Datenschutz als
  Pflichtseiten, die Garantieseiten, die Größenklassen der Stadtseite, die Ortsregel für
  Stadttexte und die verbotenen Wörter, die Bildregel.
- [siegel-programm](framework/siegel-programm.md): **die Festpreis-Garantie** (die Datei heißt
  noch nach dem alten Namen des Programms, damit die Wikilinks halten). Warum eine Garantie und
  kein Prüfzeichen, die drei Teile (Preis vor dem Anruf, der Preis ist der Rechnungspreis,
  Verstoß hat Folgen), die zwei Stufen (Garantie kostenlos, Sichtbarkeit kostenpflichtig), die
  sechs Voraussetzungen, die Spalten `geprueft`, `geprueft_jahr`, `garantie_tag`,
  `garantie_zuschlag_abend`, `garantie_zuschlag_nacht`, `garantie_anfahrt`, der Arbeitsablauf von `/festpreis-garantie/antrag/` bis
  zum Neubau, der Entzug nach Rechnung, die jährliche Erneuerung als Anrufgrund, „Noch keine
  Festpreis-Garantie" als Verkaufsanlass und die reservierte Stufe Preisschutz.
- [listings-cleaning](framework/listings-cleaning.md): die Regeln von Gate 2, die Zuordnung
- `framework/eigene-betriebe.md` — eigene Betriebe nachtragen, die im Abruf fehlen: was ein solcher Eintrag bekommt (owned, thin) und was nie (Bewertung, Garantie).
  zum Bundesland statt eines Bundesstaatfilters, die deutschen Branchenwörter mit
  umlautunabhängigem Vergleich, und die vier Listen, mit denen der Bericht die fremden
  Gewerbe, die Kettenbetriebe und die Callcenter sichtbar macht, ohne eine Zeile zu löschen.
- [enrichment](framework/enrichment.md): die Merkmalsmethode von Gate 3 (wahr / falsch / keine
  Angabe), die tauglichen und die verbotenen Merkmale, das Kernarbeits-Merkmal, der Weg über
  die eigenen Websites, die Beschreibungsregeln und das Kostengate.
- [footprint-rules](framework/footprint-rules.md): eigene Betriebe wie jeder andere gelistet,
  je Stadt höchstens ein eigener Betrieb auf einem bezahlten Platz, eigenes Cloudflare-Konto,
  kein Google Analytics und keine Search Console, und Merz Sicherheit in Mannheim als normaler
  Vorgang zum öffentlichen Preis.
- [conduct-exclusions](framework/conduct-exclusions.md): wann ein Betrieb wegen belegten
  Fehlverhaltens ausgeschlossen wird (Warnung, Presse/Gericht, Bewertungsmuster, eigene Kenntnis
  des Betreibers), der Grund wird wahrheitsgemäß eingetragen, Maßstab gilt für alle gleich.
- [monetization-slots](framework/monetization-slots.md): die Stufen mit Europreisen, die
  Landkreis- und Bundesland-Stufe als später zu aktivieren, die zwei Türen (beanspruchen und
  Festpreis-Garantie beantragen), die beiden Eintragszustände, der Garantie-Nachweis als HTML
  und die
  Ansprache, die das Verzeichnis ermöglicht.
- [outscraper-columns](framework/outscraper-columns.md): das Spaltenlayout der Eintrags-CSV,
  wie der DataForSEO-Abruf darauf abbildet, welche Spalten die Verarbeitung benutzt, die neuen
  Spalten dieser Fassung samt `geprueft` und `geprueft_jahr`, und was an den deutschen Daten
  auffällt.
- [master-template](framework/master-template.md): `templates/astro/` ist der Aufbau und wiegt
  am schwersten; der Referenzbau als englisches Pilotprojekt ist Maßstab für Aufbau und Optik
  und nie für Inhalt; Abschnitt für Abschnitt mit der neuen Bundesland-Ebene, dem
  Garantie-Zeichen und dem Kartenplatzhalter; was eine Optikvorlage ändern darf und was nicht.
- [template-build-drift](framework/template-build-drift.md): für dieses Verzeichnis ist der Build
  die Wahrheit, nicht das Template; die 25 Build-voraus-Dateien nach zwei Sorten; die Sperre in
  `init_site.py`, die ein Überschreiben von `output/<slug>/site/` abbricht.
- [design-seed](framework/design-seed.md): die Optikfrage in Gate 1, das Ableiten der
  Gestaltungsmarken in Gate 4, Vorgabe und Rückfall, Augenbrauen und Zeichen nur von der
  Vorlage, die wegzugestaltenden Merkmale, selbst gehostete Schriften, und was längere
  deutsche Wörter an der Optik ändern.
- [refresh-and-upkeep](framework/refresh-and-upkeep.md): keine Zugänge und zwei von Hand
  geprüfte Türen, Neubau bei Änderung, die jährliche Erneuerung und der Entzug der Festpreis-Garantie,
  Geldseiten als allgemeiner Auffrischungsrat, und der Pflichtweg für Korrektur und Löschung.
- [authority-and-links](framework/authority-and-links.md): wie das Verzeichnis nach dem Start
  stark wird – der Garantie-Nachweis als wichtigste Linkquelle, Pressemitteilungen, Ratgeberseiten mit
  belegten Quellen, örtliche Ansprache, der saisonale Anlass, und keine Linkgeschäfte mit den
  eigenen Websites.
- [mail-worker](framework/mail-worker.md): nach dem Start, wahlweise – die echte Adresse mit
  Empfangsbestätigung, Einordnung durch Claude und Prüfseite, die neue Anfrageart „Festpreis-Garantie" (`garantie_request`),
  die Prüfregel in den Entwürfen, deutsche Texte mit Sie-Anrede, das Einrichten und die
  Fehlersuche.
- [gate-1-intake](framework/gate-1-intake.md): was feststeht und nicht gefragt wird, und die
  drei verbliebenen Fragen – eigene Telefonnummern, Optik, Freigabe des Datenabrufs mit
  Kostenangabe; dazu was `01-umfang.md` enthält.
- [publisher-entity](framework/publisher-entity.md): der feste Herausgeber DOM Holding GmbH
  mit Geschäftsführer, was Gate 5 daraus baut (Impressum, Datenschutz, „Über uns", Schema,
  Fußzeile), und dass der Herausgeber nie als amtliche Stelle auftritt.

## SEO
- [on-page-rules](seo/on-page-rules.md): Titelmuster für die drei Ebenen, Beschreibungen ohne
  Preis, Überschriften, Verfasserzeile nur auf Ratgeberseiten, Sprache und Zahlenformat, die
  internen Links, selbst gehostete Schriften und die Karte erst nach Klick, der Seitenkopf und
  der Umgang mit großen Städten.
- [schema](seo/schema.md): JSON-LD je Seitentyp mit der neuen Bundesland-Ebene, kein
  `aggregateRating`, der feste Betriebstyp `Locksmith`, die Brotkrumen über fünf Ebenen,
  Telefonnummern in E.164 und die zwei festen Einheiten.
- [launch-lean](seo/launch-lean.md): was zum Start in die Sitemap kommt (die Bundesland-Seiten
  eingeschlossen) und was mit `noindex` startet, die Reihenfolge des Einreichens, das
  Erweitern über die Ebenen, und die zusätzlichen Prüfungen dieser Fassung zu Impressum,
  Datenschutz und externen Ladungen.
- [copy-gate](seo/copy-gate.md): das Textgate von Gate 5 – welcher Befehl welchen Block
  prüft, warum das Band der gebauten Startseite 800 bis 1.500 und das der Garantie-Seite 700
  bis 1.200 ist, warum das Band der Bundesland-Seite erst nach dem Einleitungstext greift,
  **der Schalter `--erlaube-rechtswoerter` und die drei Seiten, für die er gilt**, die
  verbotenen Wörter dieser Fassung mit Begründung, und wofür die seo-content-engine-Skill da
  ist und wofür nicht.

## Abschnittsfolgen
- [page-sections](components/page-sections.md): die Abschnittsfolge jedes Seitentyps, wie das
  Template sie liefert, mit den Bundeslandkarten, den Garantieseiten, dem Garantie-Zeichen auf
  jeder Karte und der Rechtszeile im Fußbereich.

## Referenzen
- [reference-directories](references/reference-directories.md): die sieben fremden
  Verzeichnisse als Optik- und Aufbauvergleich, nur auf Nachfrage zu zeigen; alle
  englischsprachig und aus anderen Branchen, und was von jedem ausdrücklich **nicht**
  übernommen wird.

## Vorlagen (außerhalb des Wikis)
- [claim-form.html](../templates/claim-form.html): die beiden Formulare ohne eigenen Server –
  Eintrag beanspruchen und der Garantie-Antrag mit den Preisen (Dienstleistung und Material) als Pflichtfeldern.
- [featured-tiers.md](../templates/featured-tiers.md): die Stufen mit Europreisen, die später
  zu aktivierenden Stufen, wohin die Stripe-Zahlungslinks gehören, und der Garantie-Nachweis als
  HTML, der kostenlos ist und zu keiner Stufe gehört. Die Spaltenwerte sind englisch (`featured` = `city`, `county`, `state`), weil der Code
  sie so liest, und die Stufennamen sind dort festgelegt.
- [astro/](../templates/astro/README.md): das vollständige Astro-Projekt, das Gate 5 nach
  `output/<slug>/site/` kopiert und füllt.
- [astro-skeleton.md](../templates/astro-skeleton.md): die Dateikarte dieses Projekts auf
  einem Bildschirm.
- [worker/](../templates/worker/README.md): der Mail-Worker, von `scripts/mail_worker.py
  setup` kopiert und gefüllt.
- [master-reference/](../templates/master-reference/README.md): der Referenzbau als HTML mit
  Bildschirmfotos. Der englische Pilot: Maßstab für Aufbau und Optik, nie für Inhalt. Seine
  Seiten nach Pfad öffnen, nicht durchsuchen.

## Skripte
Die Skripte liegen in `scripts/` und gehören nicht zum Wiki. Welches Skript in welchem Gate
läuft, steht in `CLAUDE.md`, Abschnitt 3, und in der Ordnerkarte in Abschnitt 2.
`scripts/check_vertical.py` wird in diesem Projekt **nicht** benutzt: die Branche steht fest
([[gate-1-intake]]).

Jedes Skript nennt seinen Aufruf mit `--help`. Die Verbotslisten
(`scripts/copy-bans.txt`, `skills/seo-content-engine/references/forbidden_words.txt`) haben
vier Blöcke: `[WORDS]` und `[PHRASES]` für die Floskeln, `[RECHTSWOERTER]` und
`[RECHTSWENDUNGEN]` für die Rechts- und Amtswörter, und ein Eintrag, der auf `*` endet, ist
ein Wortstamm und trifft jede gebeugte Form ([copy-gate](seo/copy-gate.md)).

## Skills
- [seo-content-engine](../skills/seo-content-engine/SKILL.md): die Skill, deren Linter
  `lint_copy.py` aufruft und deren vollständiger Ablauf die artikelförmigen Seiten schreibt.
  Was sie hier schreibt und was nicht, steht in [copy-gate](seo/copy-gate.md). Ihre
  Verbotsliste und ihre Stilregeln sind in dieser Fassung deutsch.
