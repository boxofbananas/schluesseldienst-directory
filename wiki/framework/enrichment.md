---
title: Anreichern (Gate 3)
type: framework
status: current
updated: 2026-11-03
---

# Anreichern (Gate 3)

Anreichern macht aus einer Liste ein Werkzeug. Ein Rohscrape ist ein Telefonbuch. Merkmale
und eine Beschreibung je Eintrag machen daraus etwas, das ein Suchender benutzt und das Google
unterscheiden kann.

## Vorgehen

Für jeden behaltenen Eintrag liest das Modell, was vorliegt (`reviews_tags`, `about`,
`subtypes`, `description`, `posts`, Titel und Beschreibung der Website, wenn die
Anreicherungsspalten existieren) und beantwortet jedes Merkmal mit **genau einem** von
`wahr` / `falsch` / `keine Angabe`. Nie raten. „Keine Angabe" wird auf der Seite als solche
angezeigt.

## Die Merkmalsdatei

Eine JSON-Datei, `output/<slug>/03-attributes.json`, mit 8 bis 15 Merkmalen, jedes mit `key`,
`label`, `faq`, `true_when` (eine Zeile, was die eigenen Worte des Betriebs sagen müssen) und
`pattern` (der reguläre Ausdruck, den `build_evidence.py` und `merge_enriched.py` benutzen).
Die Form steht in `scripts/examples/README.md`; das Beispiel dort ist die Datei eines
englischen Laufs und keine Empfehlung.

**Die Muster müssen umlautunabhängig treffen.** „Türöffnung" und „Tueroeffnung" kommen beide
vor, ebenso „Schließanlage" und „Schliessanlage". Ein Muster, das nur eine Schreibweise
kennt, verliert die Hälfte der Belege.

Taugliche Merkmale für dieses Gewerbe, belegbar aus den eigenen Worten eines Betriebs:
Notdienst rund um die Uhr, zerstörungsfreie Öffnung, Festpreis vor der Anfahrt,
Anfahrtspauschale auf der Website genannt, Einbruchschutz und Nachrüstung, Schließanlagen,
Tresoröffnung, Autoschlüssel und Funkschlüssel, Fahrzeugöffnung, eigene Werkstatt,
Schlüsselnachfertigung, Notfallnummer außerhalb der Öffnungszeiten.

**Verbotene Merkmale.** Kein Merkmal darf eine Lizenz, eine Zulassung, eine Zertifizierung,
einen Meistertitel, eine Innungs-, Verbands- oder Kammerzugehörigkeit als Gütezeichen
behaupten oder nahelegen. Schlüsseldienst ist in Deutschland kein zulassungspflichtiges
Handwerk ([[konventionen]]). Die englische Fassung hatte ein Merkmal „nennt eine
Gewerbelizenz"; es entfällt ersatzlos, weil es in Deutschland keine gibt. Belegbar und
erlaubt sind Gewerbeanmeldung, Eintragung im Handelsregister und Qualifikationen, die der
Betrieb selbst nennt – als Tatsache seiner eigenen Angabe, nie als Prüfergebnis des
Verzeichnisses.

Ein Merkmal darf `core: true` tragen und festhalten, ob der Betrieb die **Kernarbeit**
überhaupt leistet: Türen öffnen und Schließtechnik. Das trennt die Schuhmacher,
Gravurbetriebe, Metallbauer und Baumärkte ab, die über die Kategorie `locksmith`
hereinkommen, ohne sie zu löschen ([[listings-cleaning]]). Die Beschreibung sagt dann, was
der Betrieb stattdessen macht. Was mit diesen Einträgen geschieht, entscheidet der Mensch in
Gate 4; der Blueprint hat dafür keinen Vorgabewert.

## Wenn der Export keinen Text trägt

Im englischen Pilotprojekt kamen `reviews_tags` und `posts` auf jeder Zeile leer zurück und
`description` auf 11 von 1.848. Dann ist die eigene Website des Betriebs die Quelle:

1. `scripts/fetch_sites.py` liest die Startseite und bis zu drei Unterseiten. Die eigenen
   Suchwörter dieser Branche mit `--want` ergänzen, umlautunabhängig:
   `--want "tuer|tür|oeffnung|öffnung|schliessanlage|schließanlage|notdienst|einbruchschutz|tresor|autoschluessel|autoschlüssel"`.
   Keine Schnittstelle, keine Kosten, kein Paket zu installieren.
2. `scripts/build_evidence.py --patterns 03-attributes.json` zieht je Merkmal höchstens zwei
   kurze Zitate aus diesen Seiten und schreibt je Stadt eine Belegdatei. Es findet Zitate; es
   beantwortet nichts.
3. Das Modell beantwortet jedes Merkmal aus dem Paket (Maps-Felder, Seitentitel,
   Überschriften, Menü, Zitate). **`wahr`** braucht ein Zitat oder eine Überschrift, die es
   sagt. **`falsch`** braucht, dass die Seite es sagt, oder eine vollständige Leistungsliste,
   in der es fehlen würde, wo es offensichtlich hingehörte (eine Seite über
   Schlüsselnachfertigung ohne jede Erwähnung von Türöffnung ist `tueroeffnung: falsch`).
   Alles andere ist **`keine Angabe`**. Ein Eintrag ohne lesbare Website bekommt durchweg
   „keine Angabe", soweit die Maps-Daten nichts beantworten.
4. `scripts/make_batches.py --attributes 03-attributes.json` schneidet die Pakete in Stapel
   von etwa 40 Einträgen und schreibt die Merkmalstabelle an den Kopf jedes Stapels. Jeder
   Stapel wird unter `scripts/enrichment-instructions.md` beantwortet, als Subagent oder über
   `scripts/run_batches.py enrich --slug <slug>`.
5. `scripts/merge_enriched.py` prüft jede Antwort (gültige Werte, ein Beleg hinter jedem
   `wahr`, Wortband, keine Gedankenstriche, keine verbotenen Wörter, kein Satzanfang, den vier
   oder mehr Einträge teilen) und schreibt `03-listings-enriched.csv` erst, wenn nichts
   scheitert.

Nach Bundesland und Stadt stapeln, zwischenspeichern, damit ein Neubau unveränderte Zeilen
nicht erneut anreichert.

## Kosten vorher nennen

Vor dem Lauf: Einträge zählen, Token je Eintrag schätzen, die Kosten in einer Zeile nennen und
auf Freigabe warten. Dann einen kleinen Probestapel laufen lassen und lesen, bevor der Rest
folgt.

**Die Zahlen stammen aus dem englischen Pilotprojekt und sind nur Größenordnungen:** etwa
4.000 Token je Eintrag bei Subagenten auf Sonnet (gemessen 2026-09-29 an 1.848 Einträgen),
etwa 4 Cent je Eintrag über den Stapelläufer auf Sonnet (gemessen 2026-09-30 an 349
Einträgen; auf dem Standardmodell des Kontos 16 Cent bei gleicher Bestehensquote, weshalb der
Läufer Sonnet als Vorgabe nimmt). Für deutsche Texte gibt es keine Messung. Beide Zahlen
nennen und als Herkunft das englische Pilotprojekt dazusagen; **keine deutschen Messwerte
erfinden.**

## Die Beschreibung

120 bis 200 Wörter, eine Stimme, sachlich, nur aus den Daten. Sie sagt, was der Betrieb macht,
wo, was in den Bewertungsstichwörtern auffällt, und die Merkmalsantworten in Prosa. Keine
Superlative, die die Daten nicht tragen. Keine Gedankenstriche. Sie-Form wird nicht gebraucht,
weil über den Betrieb in der dritten Person geschrieben wird.

Bänder nach Belegmenge (aus dem englischen Pilotprojekt): 120 bis 200 Wörter bei Zitaten für
drei oder mehr Merkmale, 80 bis 200 bei einem oder zwei, 50 bis 90 ohne Zitate. Ein einziges
Band von 120 bis 200 ließ die Schreiber dünne Einträge aufpolstern.

**Die Beschreibung nennt nie ihre Quelle:** kein „laut Website", kein „die Seite nennt", kein
„im Impressum steht", kein „auf Google Maps", und kein Satz darüber, was unbekannt ist. Die
Ehrlichkeitsschicht steht schon auf der Seite (die gedämpfte Zeile unter dem Merkmalsraster,
die Herkunftszeile, der Hinweiskasten). Der Satz über die Bewertung darf Google als Einheit
nennen („4,8 bei 126 Bewertungen auf Google"). Jede Aussage muss sich auf das Paket
zurückführen lassen; `merge_enriched.py` lässt eine Beschreibung scheitern, die ihre Quelle
nennt.

Ohne Zitate (das Band von 50 bis 90) sagt die Beschreibung nie, der Betrieb sei „auf Google
Maps gelistet", und beginnt mit etwas, das nur für ihn gilt (Name, Stadt, was seine
Maps-Kategorie und etwaige Maps-Formulierungen sagen), damit zwei solche Beschreibungen nicht
denselben Anfang haben.

**Nie in einer Beschreibung:** „lizenziert", „zugelassen", „zertifiziert", „Meisterbetrieb"
als Gütezeichen, „Innung", „Verband", „Kammer", „amtlich", „Verbraucherschutz", „getestet",
„geprüft" (letzteres ist dem Siegel vorbehalten, [[siegel-programm]]). Ebenso kein Preis und
keine Preisspanne in Euro, weil der Export keine trägt.

## Profillinks

Der Outscraper-Basisexport trägt keine Profillinks. Der Blueprint nimmt sie von der eigenen
Website: `scripts/fetch_sites.py` behält die Links auf Facebook, Instagram, X, LinkedIn,
YouTube, TikTok und Pinterest, die es auf den gelesenen Seiten findet, und `--socials` ergänzt
sie in einem vorhandenen Zwischenspeicher. `scripts/add_socials.py` schreibt sie als Spalte
`socials` in die Eintrags-CSV; die Eintragsseite zeigt sie als Zeichen unter dem Kontaktblock,
`nofollow`, solange der Eintrag nicht ausgebaut ist, und führt sie als `sameAs` im Schema. Ein
Profil, das die Website nicht verlinkt, wird nicht gezeigt; gesucht wird nichts.

## Der Bericht (`03-enrich-report.md`)

Am Ende des Gates von Hand geschrieben: die Eingabezeilen aus Gate 2; die Merkmalsdatei, ihre
Zahl und welcher Schlüssel die Kernarbeit ist; das Ergebnis des Website-Abrufs nach Zustand
(lesbar, keine Website, gesperrt, tot, per Skript aufgebaut, anderes); Belegmenge und
Stapelzahl; die Läufe mit Bestehens- und Wiederholungszahlen; Kosten und Zeit; die
Merkmalszählungen aus dem Zusammenbau (`wahr` / `falsch` / `keine Angabe` je Schlüssel); die
Zahl dünner Einträge vor und nach dem Zusammenbau; und jede stehengelassene Warnung mit
Begründung. Dazu, für Gate 4: die Zahl der Einträge, die auf das Kernarbeits-Merkmal `falsch`
geantwortet haben, nach Haupt-Kategorie aufgeschlüsselt.

## Siehe auch
[[konventionen]] · [[listings-cleaning]] · [[page-types]] · [[siegel-programm]]
