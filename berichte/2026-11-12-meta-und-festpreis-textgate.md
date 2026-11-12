# Neue Stadtseiten-Meta, /festpreis-garantie/ durchs Textgate, Wiki-Zeile

**Datum:** 2026-11-12 · **Branch:** `main` (live) · **Deploy:** `5eaf0d86` · **Projekt:** `schluesseldienste-deutschland`

## 1. Meta-Description der Stadtseiten neu

Die Reihenfolge-Formel steht jetzt nur noch sichtbar auf der Seite, nicht mehr im Suchtreffer. Neue
Meta aus den Daten (Zahl + Stadt, **ohne Bundesland, ohne Spitzenbetrieb**). Build und Template.

**Formel (am Beispiel Mannheim, 139 Zeichen):**
> 19 Schlüsseldienste in Mannheim mit Bewertungen, Telefonnummern und Leistungen. Wer nennt vorab
> seinen Preis für die Türöffnung, wer nicht?

Zur Vorgabe „sinngemäß": der erste Satz ist wörtlich übernommen. Der zweite musste von der
Aussageform („Sehen Sie vor dem Anruf, welcher Betrieb …") in eine **Frageform** wechseln, weil die
Aussageform bei den drei längsten Stadtnamen die 160 Zeichen gerissen hätte (max 166). Die Frage sagt
dasselbe und behält die seitenübliche Wendung „Preis für die Türöffnung". Die Aussage gilt auf **jeder**
Stadtseite, auch wo kein Betrieb eine Festpreis-Garantie hat (dann lautet die Antwort schlicht: keiner).

**Länge über alle 787 gebauten Stadtseiten gemessen (aus `dist/`):**
- **kürzeste 133 Zeichen** — Hof: „6 Schlüsseldienste in Hof mit Bewertungen, Telefonnummern und Leistungen. Wer nennt vorab seinen Preis für die Türöffnung, wer nicht?"
- **längste 156 Zeichen** — Neustadt an der Weinstraße: „3 Schlüsseldienste in Neustadt an der Weinstraße mit Bewertungen …"
- **über 160: 0.**

**Textgate:** Stadtseite Mannheim (dist) **BESTANDEN ohne** `--erlaube-rechtswoerter`.

## 2. /festpreis-garantie/ durchs Textgate (gebaute Seite, mit `--erlaube-rechtswoerter`)

Vorher drei Durchfälle; jetzt **BESTANDEN**. Was geändert wurde:

**a) Gedankenstriche (11 → 0), durch Satzbau ersetzt.** Fünf waren Zeitbereiche („7–20 Uhr",
„0–7 Uhr") → „7 bis 20 Uhr", „0 bis 7 Uhr" (Tatsache unverändert). Sechs waren freistehende
Gedankenstriche → Kommas bzw. Satzteilung.

**b) Branchenwort in den ersten Absatz.** Der Linter prüft den **ersten Textblock der gebauten Seite,
und das ist das H1** (`lint_copy.py:276` nimmt den Kopfbereich mit; `:373` sucht das Plural
„Schlüsseldienste"). Das alte H1 „Festpreis-Garantie: der Preis steht, bevor jemand kommt" trug kein
Branchenwort — die Stadtseiten bestehen nur, weil ihr H1 „Schlüsseldienste in …" lautet. Das H1 nennt
jetzt die Branche, sinnerhaltend. Zusätzlich beginnt der erste Absatz mit „Nicht alle Schlüsseldienste
nennen ihren Preis …".

**c) Das Zitat „ab 49 Euro".** Stelle: erster Absatz unter „Das Problem …". Regel: `keine_verbotenen_wendungen`
— der String steht wörtlich als Lockangebot-Floskel in
`skills/seo-content-engine/references/forbidden_words.txt:122` (neben „ab 59/69/89 Euro"), der Linter
matcht ihn mit bis zu sechs Füllwörtern. **Sinnerhaltend umformuliert** (du hattest das erlaubt): aus
dem wörtlichen Lockpreis-Zitat wird die Beschreibung „ein niedriger Lockpreis am Telefon" — dieselbe
Aussage (Lockangebot mit niedrigem Ab-Preis, dann 400 auf der Rechnung), ohne die verbotene Floskel.

**An den Tatsachen der Seite hat sich nichts geändert:** Voraussetzungen, Preise, Zeiten, Fristen und
Zusagen stehen Wort für Wort im Sinn erhalten; geändert sind nur Zeichensetzung, das H1 und das
illustrative Betrugs-Beispiel.

### Diff der Texte (Build; Template identisch)

```diff
-    <h1>Festpreis-Garantie: der Preis steht, bevor jemand kommt</h1>
+    <h1>Festpreis-Garantie: Schlüsseldienste, die den Preis nennen, bevor jemand kommt</h1>

-      Kurzfassung: Ein {site.niche.singular} mit Festpreis-Garantie nennt in seinem Eintrag seine
-      Preise – einen Grundpreis für die Türöffnung, zwei benannte Zuschläge und die Anfahrt – und
-      garantiert, dass der genannte Preis der Preis auf der Rechnung ist. …
+      Kurzfassung: Nicht alle {site.niche.plural} nennen ihren Preis, bevor sie kommen. Ein
+      {site.niche.singular} mit Festpreis-Garantie nennt in seinem Eintrag seine Preise, einen
+      Grundpreis für die Türöffnung, zwei benannte Zuschläge und die Anfahrt, und garantiert, dass
+      der genannte Preis der Preis auf der Rechnung ist. …

-      Antwort lautet oft „ab 49 Euro“, und auf der Rechnung stehen 400. …
+      Antwort ist oft ein niedriger Lockpreis am Telefon, und auf der Rechnung stehen 400. …

-        Grundpreis für die Türöffnung (werktags 7–20 Uhr) … nachts von 0–7 Uhr) …
+        Grundpreis für die Türöffnung (werktags 7 bis 20 Uhr) … nachts von 0 bis 7 Uhr) …
   (dieselbe Ersetzung 7–20 → 7 bis 20 und 0–7 → 0 bis 7 an allen fünf Zeitangaben)

-      … freiwillige Mitgliedschaften – und genau deshalb prüfen wir …
+      … freiwillige Mitgliedschaften. Und genau deshalb prüfen wir …

-        … belegter Verstoß erreicht – insbesondere eine Rechnung über dem garantierten Preis. …
+        … belegter Verstoß erreicht, insbesondere eine Rechnung über dem garantierten Preis. …

-      … weil eine käufliche Garantie wertlos wäre – auch für die, die sie gekauft haben.
+      … weil eine käufliche Garantie wertlos wäre, auch für die, die sie gekauft haben.

-      … wir prüfen die sechs Voraussetzungen – kostenlos, in wenigen Tagen. …
+      … wir prüfen die sechs Voraussetzungen, kostenlos, in wenigen Tagen. …
```

## 3. Wiki-Zeile

`wiki/seo/on-page-rules.md:85` (nicht `wiki/framework/…`, dort liegt die Datei nicht) auf die geltende
Reihenfolge gebracht: die Kartenabschneidung bei 60 Einträgen ist jetzt „geordnet nach bezahltem Platz,
**dann Festpreis-Garantie,** dann Bewertung × Zahl der Bewertungen".

## 4. Bauen, Ausliefern, Prüfen

- `npm run build` (Build + Template) grün, Schriftprüfung grün, Sitemap 2823.
- Textgate: /festpreis-garantie/ (dist, mit Flag) **BESTANDEN**; Stadtseite Mannheim (dist, ohne Flag)
  **BESTANDEN**; Template-/festpreis-garantie/ ebenfalls BESTANDEN.
- `wrangler pages deploy` → Deploy `5eaf0d86`.
- `check_live.py … --expect-urls 2823` → **alle Prüfungen bestanden**.
- Live-Stichprobe: Mannheim-Meta 139 Zeichen in neuer Form ✓, festpreis-H1 mit Branchenwort ✓,
  „Lockpreis" statt „ab 49 Euro" ✓, kein Gedankenstrich im Fließtext ✓.
