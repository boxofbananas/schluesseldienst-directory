# Ähnlichkeitsprüfung der 18 Garantie-Beschreibungen gegeneinander

**Datum:** 2026-11-06
**Auslöser:** Daniel — die Zusammenführung prüfte die neun neuen gegen die bestehenden 2.197,
nicht untereinander. Die neun stammen aus Websites desselben Betreibers, vermutlich aus einer
Vorlage. Paarweise Ähnlichkeit aller 18 messen, Paare über der Schwelle und wörtliche Wendungen
in mehr als zwei zeigen, nur wirklich zu nahe Beschreibungen neu schreiben, nur mit Paketfakten.

## Methode

Exakt die von `scripts/check_city_copy.py`: Sätze ab neun Wörtern, Betriebsname und Stadt
entfernt, gefaltet (Kleinschreibung, Umlaute umgeschrieben, auf `[a-z0-9 ]` reduziert). Zwei
Maße: Exaktvergleich ganzer Sätze (Textbaustein, wenn in ≥3) und **Jaccard der Wortmengen,
Schwelle 0,75** (ein Satz fällt, wenn er in ≥2 weiteren Betrieben einen Satz ≥0,75 hat — die
dort kalibrierte Regel). Dazu wörtliche N-Gramme (5–9 Wörter) in >2 der 18.

Die 18: die neun neuen plus die neun bereits inhaltstragenden (Merz Sicherheit Mannheim,
Heidelberg, Mein Schlüsseldienst Hockenheim, Kraichgau Sinsheim, Pälzer Neustadt, Hardt
Waghäusel, Südpfalz Landau, Odenwald Bensheim, Kurpfalz Wiesloch).

## Befund (vor der Änderung)

**Genau ein Muster lag über der Schwelle** — der Schlusssatz zur Anfahrtszeit:

> „ein monteur ist nach eigener angabe meist in etwa einer halben stunde vor ort"

wörtlich in **Frankenthal, Ludwigshafen, Worms** (Jaccard 1,00) und als Variante ohne „nach
eigener Angabe" in **Speyer** (0,79). Das waren die **einzigen** Satzpaare ≥0,75 im ganzen Set.
Nächsthöchstes Paar: **0,67** (AES ↔ Merz Sicherheit) — darunter.

Wörtliche Wendungen in >2 der 18: der „halbe Stunde vor Ort"-Satzrest (dasselbe Muster) sowie
„die anfahrtskosten gibt er nach ort gestaffelt an" (3×: Weinheim, Ludwigshafen, Worms). Der
Rest sind generische Fachausdrücke, deren ganze Sätze sich klar unterscheiden und kein Paar über
0,75 bilden: „rund um die uhr erreichbar", „bei abgeschlossenen türen wird der", „plant und
montiert der betrieb". Künstlicher Abstand dort wäre gegen die Vorgabe, also unverändert.

## Änderung

Nur die **vier** Betriebe mit dem geteilten Schlusssatz neu geschrieben, jeweils mit einer
Anfahrts-Tatsache aus dem **eigenen** Belegpaket:

- **Frankenthal:** „Zur Anfahrt rechnet der Betrieb je nach Stadtteil und Verkehr mit einer
  halben bis Dreiviertelstunde." (Paket: „Je nach Stadtteil, Verkehr und Einsatzlage … ca. 30–40
  Minuten vor Ort")
- **Ludwigshafen:** „Lange Anfahrtzeiten entstehen nach eigener Angabe im Regelfall nicht."
  (Paket: „keine langen Anfahrtzeiten"); dazu die Anfahrt-Klausel zu „die Anfahrt staffelt er
  nach Entfernung" und eine Schließanlagen-Tatsache ergänzt („ein einziger Schlüssel regelt den
  Zugang zu bestimmten Bereichen"), um die Wortspanne zu halten.
- **Speyer:** „Kurze Anfahrtswege nennt der Betrieb als Merkmal seiner Lage in der Region."
  (Paket: „ein in der Region Unternehmen, kurze Anfahrtswege")
- **Worms:** „Zum Einsatzort braucht er nach eigener Angabe meist weniger als eine halbe Stunde."
  (Paket: „nicht einmal 30 Minuten zum Einsatzort"); Anfahrt-Klausel zu „Für die Anfahrt gelten
  je nach Ort unterschiedliche Pauschalen".

Damit fällt auch „die anfahrtskosten gibt er nach ort gestaffelt an" auf 1 von 18 (nur Weinheim).

## Nachkontrolle

Prüfung erneut gelaufen: **kein Satz mehr über der Regel, kein Paar ≥0,75**, höchster Wert jetzt
0,67 (AES ↔ Merz Sicherheit, unverändert, unter der Schwelle). `merge_enriched.py` erneut:
**9/9 bestanden** (Wortspannen 115→126 … 140, keine verbotenen Wörter, Traces intakt).

Die vier Beschreibungen in Site-CSV und `03-listings-enriched.csv` übertragen (nur
`description_enriched`; Merkmale und Garantie-Spalten unberührt), neu gebaut (4647 Seiten,
Schriftprüfung bestanden), ausgeliefert (nur 4 Dateien neu). **Sitemap unverändert 2823**,
`check_live.py` grün. Die vier Seiten live mit neuem Text, `index, follow`.

## Stand

Die 18 Garantie-Beschreibungen lesen jetzt auch untereinander eigenständig. Keine weitere
Änderung nötig.
