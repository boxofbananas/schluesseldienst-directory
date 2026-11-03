---
title: Textgate (Gate 5)
type: seo
status: active
updated: 2026-11-03
---

# Textgate

Die Merkmalsliste in [[design-seed]] fängt die optischen Verräter einer KI-gebauten Site. Dieses
Gate fängt die sprachlichen, und es läuft in Gate 5: auf `city-copy.json` und die
Ratgeberseiten **vor** `npm run build`, und auf die gebauten Seiten Startseite, Bundesland und
„Über uns" in `dist/` **danach**, weil die ihren Text aus `site.json` ziehen. Es benutzt die
**seo-content-engine**-Skill aus `skills/seo-content-engine/` auf zwei Weisen.

## 1. Jeden kurzen Block prüfen (kein Zugang nötig)

`scripts/lint_copy.py` liest die Verbotsliste der Skill
(`skills/seo-content-engine/references/forbidden_words.txt`, **deutsche Werbefloskeln**) plus
die eigenen Zusätze des Blueprints (`scripts/copy-bans.txt`) und wendet sie mit den Funktionen
der Skill an. Nur Standardbibliothek, Rückgabewert 1 bei jedem Fehler, also läuft es als
Schleife: laufen lassen, nachbessern, erneut laufen lassen.

| Text | Befehl | Was geprüft wird |
|---|---|---|
| Stadtblöcke und Fragen | `python3 scripts/lint_copy.py output/<slug>/site/src/data/city-copy.json --niche "schlüsseldienste" --city-sizes output/<slug>/05-city-sizes.json` | Wort- und Fragenband der Größenklasse ([[page-types]]), jede Antwort 20 bis 120 Wörter, Branchenwort im ersten Absatz, keine verbotenen Wörter, keine Gedankenstriche |
| Bundesland-Seite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/verzeichnis/<bundesland>/index.html --min-words 300 --max-words 500` | Seitenband, Verbote, Gedankenstriche |
| „Über uns" (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/ueber-uns/index.html --min-words 300 --max-words 500` | Seitenband, Verbote, Gedankenstriche |
| Startseite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/index.html --min-words 800 --max-words 1500 --niche "schlüsseldienste"` | Seitenband, Branchenwort früh, Verbote, Gedankenstriche. Der Ratgeberblock darin bleibt bei 400 bis 600 Wörtern und die Fragen bei 5 bis 8 |
| Siegel-Seite (gebaut) | `python3 scripts/lint_copy.py output/<slug>/site/dist/siegel/index.html --min-words 400 --max-words 700` | Seitenband, Verbote. **Zusätzlich von Hand prüfen:** alle sechs Kriterien stehen da, der Satz „kein Test vor Ort" steht da, der Satz zur Nichtkäuflichkeit steht da ([[siegel-programm]]) |
| Ratgeberseite | `python3 scripts/lint_copy.py output/<slug>/site/src/pages/ratgeber/<slug>.md --min-words 1200 --niche "<thema>"` | 1.200 Wörter oder mehr, Thema früh, Verbote, Gedankenstriche |

Die Lesbarkeitsstufe wird berichtet, nicht erzwungen. Für deutsche Texte über ein
Handwerksthema taugt eine Stufe, die ein Laie im Notfall am Telefon versteht; sehr lange
Sätze kürzen. Die englischen Stufenwerte der Skill sind auf deutsche Sätze nicht
übertragbar, weil deutsche Wörter länger sind; sie sind ein Hinweis, kein Maß.

`.astro`-Seiten werden als Ganzes geprüft, feste Absätze eingeschlossen, also gilt das
Seitenband und nicht das Blockband. **Die Startseite nie aus `index.astro` prüfen:** sie zählt
zu wenig, und ihr erster Absatz nach dem Entfernen des Auszeichnungscodes ist die
H1-Formulierung, sodass die Branchenprüfung aus dem falschen Grund scheitert.

**Warum das Band der gebauten Startseite 800 bis 1.500 ist.** Der Aufbau des Templates
(Länderkarten, Städtekarten, Zahlenreihe, Suchfeldbeschriftungen, die drei Versprechen, die
vier Prüfschritte) ergibt im gebauten Zustand etwa 350 Wörter Text, bevor ein Satz geschrieben
ist – in dieser Fassung mehr als in der englischen, weil die Bundeslandkarten dazukommen und
deutsche Beschriftungen länger sind. Mit dem Ratgeber bei 400 bis 600 und den Fragen bei 5 bis
8 muss die Obergrenze 1.500 sein, damit beide Bänder zugleich halten. Der geschriebene Text
sind etwa 800 bis 1.200 Wörter.

## 2. Was der Prüfer zusätzlich fängt

`scripts/check_city_copy.py` läuft das Textgate und prüft vier Dinge mehr: jede Zahl muss in
den Daten der Stadt oder auf der Faktensammlung stehen, **keine Prozentangabe und kein
Eurobetrag**, keine interne Wortwahl, und kein Satz und kein Anfang, den drei oder mehr Städte
teilen.

Für diese Fassung kommt dazu, was in keinem sichtbaren Text vorkommen darf und von Hand oder
über `scripts/copy-bans.txt` geprüft wird:

- **„lizenziert", „zugelassen", „zertifiziert", „Meisterbetrieb" als Gütezeichen,
  „Konzession".** Schlüsseldienst ist kein zulassungspflichtiges Handwerk; es gibt keine
  Lizenz und keine Meisterpflicht ([[konventionen]]).
- **„Innung", „Verband", „Kammer", „amtlich", „offiziell geprüft", „Verbraucherschutz",
  „getestet".** Grund: Verwechslungsgefahr mit einer amtlichen Stelle. Das Verzeichnis ist
  ein privates Angebot der DOM Holding GmbH, und sein Siegel ist seine eigene Auszeichnung
  ([[siegel-programm]]).
- **„geprüft"** nur im Zusammenhang mit dem Siegel und seinem Jahr, nie als allgemeines Lob
  für einen Betrieb.
- **Jeder Preis und jede Preisspanne in Euro** in Stadt-, Bundesland- und Eintragstexten.
  Erlaubt sind Preise nur auf `/premium/` und in den AGB (die eigenen Stufen) und in einer
  Ratgeberseite, wenn eine amtliche Quelle sie belegt und als deren Angabe genannt wird
  ([[page-types]]).
- **Werbefloskeln** aus `forbidden_words.txt`: „schnell und günstig", „rund um die Uhr für
  Sie da", „unschlagbar", „führend", „Nummer 1", „seriös und zuverlässig" als Behauptung über
  einen Betrieb, den das Verzeichnis nicht geprüft hat.
- **Erfundene Ortsangaben.** Eine Stadttatsache ohne Quelle aus der Liste in
  [[konventionen]] wird nicht geschrieben.

## 3. Die artikelförmigen Seiten mit der Skill schreiben

Ratgeberseiten und der Ratgeberblock der Startseite sind der Text, der wirklich
artikelförmig ist: ein Thema, eine Seite, gebaut um verlinkt zu werden
([[authority-and-links]]). Dafür den vollständigen Ablauf der Skill benutzen. Stufe 1 holt die
aktuellen Treffer zum Thema über die DataForSEO-Anmeldung des Betreibers, die späteren Stufen
entwerfen, glätten, prüfen die Tatsachen und geben aus.

- DataForSEO ist **wahlweise**. Der Start (Gates 1 bis 6) braucht nichts davon. Ohne
  Verbindung diese Seiten von Hand aus der Faktensammlung schreiben und mit der Tabelle oben
  prüfen.
- Die Skill findet die Verbindung am Werkzeugnamen; sie fragt nie einen Zugang im Gespräch ab,
  und `references/credentials.md` bleibt leer.
- **Die Tatsachenprüfung der Skill ersetzt die Faktensammlung nicht.** Was die Skill findet,
  wird gegen die Quellen aus [[konventionen]] gehalten: Handwerkskammer, Gewerbeamt,
  Verbraucherzentrale, polizei-beratung.de, Stiftung Warentest. Ein Punkt, für den nur eine
  kommerzielle Quelle oder ein anderes Branchenbuch gefunden wird, gilt als **unbelegt** und
  darf in keinem Text auftauchen.
- Was die Skill schreibt, ist auf Deutsch zu schreiben. Englische Textmuster der Skill
  („TL;DR", „verdict") werden nicht übersetzt übernommen, sondern durch deutsche Formen
  ersetzt: ein Vorspann und ein Fazit.

## Wofür die Skill nicht da ist

Der Stadtblock. Die Skill schreibt je Lauf einen langen Artikel; Stadtseiten wären so viele
Läufe in der falschen Form. Ein Stadtblock sind 500 bis 800 Wörter Ortstext über den Karten,
aus den angereicherten Daten geschrieben. **Prüfen, nicht erzeugen.**

## Siehe auch
[[konventionen]] · [[page-types]] · [[design-seed]] · [[siegel-programm]]
