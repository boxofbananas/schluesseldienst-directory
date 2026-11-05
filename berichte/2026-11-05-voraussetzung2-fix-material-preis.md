# Voraussetzung-2-Fund korrigiert + Festpreis-Garantie um Material präzisiert (2026-11-05)

Zwei Teile: zuerst der gemeldete Fund bereinigt und seine Ursache geklärt, dann die
Material-Präzisierung der Festpreis-Garantie nach deinen vier Entscheidungen gebaut und
ausgeliefert. Live: `cb47edd7`.

---

## Teil 1 — Der Fund: Voraussetzung 2 stand noch alt

### Was war

Die alte Festnetz-Pflicht-Fassung überlebte an **zwei** Stellen, **beide im `output/`-Build**
(das, was ausgeliefert wird):

1. `output/.../site/src/pages/festpreis-garantie/index.astro` (öffentliche Seite, der gemeldete
   Punkt) — „Erreichbare Festnetznummer … Ortsvorwahl zur Anschrift … Mobilnummer genügt nicht".
2. `output/.../site/src/pages/festpreis-garantie/antrag/index.astro` (das Antragsformular im
   Build) — „Festnetznummer mit Ortsvorwahl Ihres Ortes … Voraussetzung 2 (Pflicht) … reine
   Mobilnummer genügt nicht". **Diese zweite Stelle war in deiner Meldung nicht genannt, war aber
   ebenfalls noch alt** — und sie widersprach dem Wiki direkt.

Korrigiert auf den Wiki-Wortlaut: „Eine erreichbare Telefonnummer, unter der der Betrieb bei der
Prüfung tatsächlich abgehoben hat. Wir rufen die Nummer vor der Erteilung an." Das Formularfeld
`festnetz` (Pflicht) + `telefon` (optional) wurde auf ein Feld `telefon` (Pflicht) zusammengeführt,
wie es die Template-Fassung vorgibt; `festnetz` wird von keinem Skript und keinem Worker gelesen
(geprüft), der Zusammenschluss bricht nichts.

Korrekt waren bereits: `konventionen.md`, `siegel-programm.md`, `templates/astro`-Antrag,
`templates/claim-form.html`, und sogar die **Template**-Fassung der öffentlichen Seite.

Die Sortierregel `konventionen.md` Z. 186 („Festnetznummer, deren Ortsvorwahl zur PLZ passt")
bleibt unverändert — das ist das Sortiersignal, nicht die Garantie-Voraussetzung.

### Wie es dazu kam (3 von 4)

Der 2026-11-04-Bericht meldete die Angleichung „in `konventionen.md`, `siegel-programm.md`,
`/festpreis-garantie/` und beiden Antragsformularen (`claim-form.html` und die astro-Antragsseite)".
Tatsächlich geändert wurden die **Einzelquellen** (`konventionen.md`, `siegel-programm.md`) und die
**`templates/`-Kopien** (claim-form.html, templates/astro-Antrag **und** die templates/astro-Fassung
der öffentlichen Seite). Nicht angefasst wurde der **`output/.../site/`-Baum** — die bereits
gebauten, tatsächlich ausgelieferten Astro-Seiten.

Ursache also: **Template-vs-Build-Drift.** Es gibt zwei Kopien jeder Astro-Seite — den Master in
`templates/astro/` und die gefüllte Kopie in `output/.../site/`. Die Prüfung „überall angeglichen"
war eine Suche über Wiki und Template; sie umfasste den `output/`-Baum nicht, also blieb die
ausgelieferte Seite alt, obwohl der Master korrekt war. Eine Volltext-Suche über **das ganze Repo**
(inkl. `output/`) nach der alten Formulierung hätte beide Reststellen gefunden.

### Maschinelle Absicherung (Vorschlag — nichts davon gebaut)

Das Problem ist allgemein: jede Regel, die an mehreren Stellen wörtlich steht, driftet, sobald eine
Kopie geändert wird und die anderen nicht. Drei Mechanismen, von billig nach gründlich:

**(1) Sofort: ein Stale-/Required-Phrase-Wächter** (`scripts/check_consistency.py`). Eine kleine
Registry von Invarianten, je Invariante:
- `verboten`: Formulierungen, die **nirgends** mehr vorkommen dürfen (alte Fassungen), z. B.
  „Erreichbare Festnetznummer", „Ortsvorwahl zur … Anschrift" im Garantie-Kontext, „drei
  Standardpreise verbindlich".
- `pflicht_in`: eine kanonische Formulierung, die in einer **benannten Dateiliste** vorkommen
  **muss** (neue Voraussetzung 2 in: konventionen, siegel-programm, Seite, beide Formulare).
- Gescannt über **das ganze Repo** (`output/` + `templates/` + `wiki/` + `CLAUDE.md`) — genau der
  Baum, der diesmal fehlte. Läuft in Gate 5 und vor jedem Deploy, Exit ≠ 0 bei Treffer. Der
  Hand-Sweep, den ich in diesem Bericht fahre, ist die manuelle Form davon.

**(2) Strukturell für die höchststakigen Texte: Single-Source.** Die sechs Voraussetzungen und das
Serviceversprechen stehen als handgeschriebene Prosa an 5+ Stellen. In **eine** kanonische Liste in
`site.json` (`garantie.voraussetzungen[]`, `garantie.serviceversprechen[]`) legen und die Seite +
beide Astro-Formulare daraus rendern. Dann gibt es eine Quelle; Seite und Formulare **können** nicht
mehr auseinanderlaufen. Das Wiki bleibt Prosa, abgedeckt durch (1). Jetzt — nachdem ich für die
Material-Änderung ohnehin alle diese Stellen angefasst habe — wäre der Moment dafür.

**(3) Template↔Build-Parität als Prüfung.** Die Ursache war `output/` ≠ `templates/astro`. Eine
Prüfung, die die geteilten Struktur-/Code-Dateien (Komponenten, `lib/`, statische Seiten) zwischen
beiden Bäumen vergleicht und unerwartete Abweichung meldet (gewollte Abweichung — `site.json`,
`listings.csv`, `city-copy.json` — ausgenommen). Fängt „Template geändert, Build vergessen" und
umgekehrt.

Empfehlung: (1) jetzt bauen (klein, hoher Wert), (2) als Nächstes für die Garantie-Listen, (3) als
leichter Zusatzriegel. Sag, was davon ich angehen soll.

---

## Teil 2 — Material-Präzisierung (deine vier Entscheidungen)

### Entscheidung 1 — Datenmodell: Variante A (zwei feste Spalten)

Neu: `garantie_zylinder` (Standardzylinder, €) und `garantie_zylinder_5mm` (Aufschlag je 5 mm
Mehrlänge, €), direkt hinter `garantie_anfahrt`, von Gate 2 leer angelegt. Umgesetzt in:
`listings.csv` + angereicherter CSV (beide 80 Spalten), `clean_listings.py` (`GARANTIE`-Liste +
Bericht), `merge_enriched.py` (`EXTRA`), `add_own_listings.py`, Template-Sample, `load.mjs`
(`garantie`-Objekt um `zylinder`, `zylinder5mm`). Begründung — Vergleichbarkeit als Zweck des
Verzeichnisses — steht in `siegel-programm.md` („Warum das Material zwei feste Spalten hat, kein
Freitext"); die Antragsseite erklärt, wie die beiden Zahlen gemeint sind. Die defekte Tür bekommt
bewusst keine Spalte (sie ist der „vor Arbeitsbeginn beziffert"-Fall des Serviceversprechens).

### Entscheidung 2 — `konventionen.md` nur die Preissemantik (Z. 128–155)

Geändert: Punkt 1 der „drei Teile" (Preis-Definition) und der Voraussetzungs-Punkt zu den Preisen,
plus die eine Stufen-Zeile „nennt seine Preise verbindlich". Alter Wortlaut von Punkt 1, zum
Nachvollziehen:

> Jeder Betrieb mit Garantie veröffentlicht seine drei Standardpreise: Türöffnung tagsüber,
> Türöffnung nachts (nachts, Wochenende, Feiertag) und Anfahrt. … Spalten: `garantie_tag`,
> `garantie_nacht`, `garantie_anfahrt` – Euro-Beträge als ganze Zahl ohne Einheit; …

Neu: Dienstleistung (die drei Preise, Türöffnung, nicht Gesamtbetrag; gilt für zugefallene wie
abgeschlossene Tür) vs. Material (`garantie_zylinder`, `garantie_zylinder_5mm`, bei abgeschlossener
Tür, feste Regel) vs. defekte Tür (Ab-Preis, vor Arbeitsbeginn beziffert). Alles Übrige in
konventionen.md unverändert. Eine Zeile dazu steht in `wiki/log.md`.

### Entscheidung 3 — Texte und Listen wie vorgelegt, mit korrigierter Voraussetzung 2

`/festpreis-garantie/`: Abschnitt „Was der Festpreis abdeckt – und was dazukommen kann"
(Dienstleistung/Material/defekt), Voraussetzung 3 um die Materialpreise erweitert, Serviceversprechen
auf **fünf** Punkte. Die beiden vollständigen Listen stehen live auf der Seite; Kurzfassung:

**Sechs Voraussetzungen:** (1) Impressum · (2) erreichbare Telefonnummer, bei der Prüfung
abgehoben, wird vorher angerufen · (3) die Preise verbindlich genannt: drei Dienstleistung
(Türöffnung tagsüber, nachts, Anfahrt) **und** zwei Material (Standardzylinder, Aufschlag je 5 mm) ·
(4) ≥ 5 Bewertungen → Schnitt ≥ 4,0, sonst entscheiden die übrigen · (5) kein Callcenter ohne
Ortsbezug · (6) unterschriebenes Serviceversprechen.

**Serviceversprechen (fünf):** (1) Festpreis = Preis der Dienstleistung, steht auf der Rechnung,
gilt für zugefallene wie abgeschlossene Tür, vor Arbeitsbeginn bestätigt · (2) bei abgeschlossener
Tür kommt nur das genannte Material dazu, keine weiteren unbezifferten Zuschläge · (3) defekte
Türen/Sonderfälle vor Arbeitsbeginn beziffert, erst nach Zustimmung · (4) Rechnung mit
Firmenanschrift · (5) zerstörungsfreie Öffnung als Standard.

Kein Widerspruch zwischen den Listen: V3 verlangt alle fünf Zahlen, Versprechen 1–2 binden an genau
diese Zahlen, Versprechen 3 fängt ab, was keine feste Zahl ist.

Dieselben Änderungen in **allen drei Garantie-Antragsformularen**: die Astro-Antragsseite (zwei
Material-Felder als Pflicht, drei Preisfelder als „Dienstleistung" gerahmt, Serviceversprechen auf
fünf Checkboxen) und `templates/claim-form.html` (dieselbe Struktur). `claim-form.html` war das
dritte Formular, das der Hand-Sweep aufgedeckt hat.

### Entscheidung 4 — Preisblock: zwei beschriftete Gruppen + Fußnote

`Garantie.astro` (Vollmodus) zeigt jetzt „Dienstleistung (Festpreis)" (Türöffnung tagsüber, nachts,
Anfahrt) und „Material bei abgeschlossener Tür" (Standardzylinder, je 5 mm Mehrlänge), darunter die
Fußnote „Bei einer zugefallenen Tür fällt kein Material an. Defekte Türen und Sonderfälle werden vor
Arbeitsbeginn beziffert." Die Materialgruppe rendert nur, wenn `garantie_zylinder` gesetzt ist.
**Stadtkarte und Garantie-Nachweis unverändert** bei „Türöffnung ab … €".

Bildschirmfoto mit allen fünf Zahlen (Merz in Mannheim vorübergehend geflaggt, danach zurückgesetzt
— die ausgelieferte Site zeigt keine erfundene Garantie): `berichte/screenshots/preisblock-material-5zahlen.png`.

### Die zwei Prüfungen, um die du gebeten hast

**Textgate.** `lint_copy.py` hat keine Zahlen-/Euro-Sperre; die Preis-relevanten Hebel sind die
Werbe-Wörter/-Wendungen und der `garantie*`-Stamm (auf `/festpreis-garantie/` per
`--erlaube-rechtswoerter` frei). **Die neuen Preistexte bringen kein verbotenes Werbewort, kein
Rechtswort und (nach Bereinigung) keinen neuen Gedankenstrich ein.** Die Seite meldet weiter drei
Treffer — „ab 49 Euro" (das Zitat, mit dem der Abzock-Mechanismus benannt wird), Singular im ersten
Absatz, 6 Gedankenstriche —, aber **alle drei sind vorbestehend** (schon im HEAD so) und gehören zu
dieser Rechtsseite, nicht zu den Preistexten. Ich habe meine zunächst ergänzten Gedankenstriche
(15) auf den HEAD-Stand (6) zurückgeführt. Auf Eintragsseiten bleibt der Preisblock ein `<dl>` aus
den Daten, nie Fließtext.

**Eintragsseite übersichtlich?** Ja — siehe Screenshot. Die zwei Gruppen trennen Dienstleistung und
Material sauber; die Karte bleibt kurz (nur der Dienstleistungs-Ab-Preis).

### Konsistenz-Sweep (der Hand-Lauf des vorgeschlagenen Wächters)

Nach der Änderung das ganze Repo nach „drei Preise"/„drei Standardpreise" im Garantie-Kontext
durchsucht und **~20 faktisch gewordene Stellen** angeglichen: Antrag „drei Preise als
Pflichtfeldern" → jetzt fünf Felder; Eintrags-Zeichen „mit den drei Preisen" → jetzt plus
Materialblock; Spaltenlisten in `outscraper-columns.md`, `copy-gate.md`, `CLAUDE.md`,
`refresh-and-upkeep.md`, `siegel-programm.md` (Arbeitsablauf, Entzug, jährliche Erneuerung → sieben
Spalten). `wiki/log.md`-Historie **nicht** angefasst. Template↔Build-Parität der Garantie-Dateien
geprüft: identisch.

**Verbleibende benigne Reststellen:** einige beschreibende „drei Preise"-Erwähnungen, die die drei
**Dienstleistungs**preise korrekt benennen (das Garantie-Zeichen zeigt weiter genau diese drei, das
Material ist zusätzlich). Nicht massenhaft umgeschrieben, um keine Fehler einzuführen; der
vorgeschlagene Wächter (1) würde die kanonische Formulierung registrieren.

---

## Offen / unverändert

- Die drei konkreten Garantiepreise der eigenen Betriebe legst du separat fest; am Gerüst war dafür
  nichts vorzubereiten, und es wurde nichts vorbereitet.
- Domain: wartet weiter auf deine DNS-Klicks, dann `check_live.py`.
- Sortierung liest `owned` nicht; kein eigener Betrieb manuell nach oben; keine Empfehlung im
  Fließtext.
