---
title: Eintragsseite – Fehlanzeigen raus, Bewertungsschlagwörter raus, Sonntag, Städtezahl
type: bericht
status: fertig
updated: 2026-11-05
---

# Eintragsseite: zwei Blöcke entfernt, zwei Kleinigkeiten

## (1) „Leistungen und Angaben": nur noch Bestätigtes
`AttributeGrid` zeigt jetzt **nur Merkmale mit Wert „true"** (Website belegt sie). Nicht bestätigte
Merkmale – sowohl ein „nein" als auch „nicht bekannt" – werden **weggelassen, nicht benannt**; die
Zeile „Keine Angaben zu …" ist raus. Ist **kein** Merkmal bestätigt, **entfällt der ganze Abschnitt**
(Überschrift, Raster und die „In Deutschland vergleichen"-Links) auf der Eintragsseite.

### Zahlen, die du vorab wolltest (Stand 3.800 Einträge)
- **2.394** Einträge zeigten bisher die „Keine Angaben zu …"-Liste.
- **1.453** Einträge hätten nach der Änderung **gar keinen Merkmals-Abschnitt** mehr (kein einziges
  Merkmal bestätigt). Davon haben **1.403** überhaupt kein bekanntes Merkmal (weder ja noch nein).
- **2.347** Einträge haben mindestens ein bestätigtes Merkmal und behalten den Abschnitt.

**Einordnung / deine Entscheidung:** 1.453 von 3.800 (**38 %**) ohne Merkmals-Abschnitt ist viel.
Der Grund ist fast durchweg **fehlende Beleggrundlage**: die 1.403 ohne jedes bekannte Merkmal sind
Einträge, zu denen Gate 3 keine Website lesen konnte (keine Seite hinterlegt, Abruf gescheitert, oder
sehr dünn). Das ist **kein Fehler der Anzeige** – „nur Bestätigtes zeigen" ist richtig, auch wenn
Gate 3 später mehr erkennt. Die eigentliche Frage ist, ob die **Merkmalserkennung in Gate 3 zu streng
bzw. die Abdeckung zu dünn** war. Zwei Hebel, falls du mehr Abschnitte willst (beides deine
Entscheidung, nicht von mir angefasst):
1. Das Kernmerkmal „Schlüsseldienst (Türöffnung/Schließtechnik)" für Einträge der Google-Kategorie
   `locksmith` als bestätigt werten, auch ohne eigene Website (heute `schluesseldienst_kern` = true
   bei 1.795). Das wäre eine Gate-3-Regeländerung.
2. Websites der betroffenen Einträge erneut abrufen und anreichern (Gate 3 teilweise neu, kostet).

Sag, ob und welchen Weg du willst; die Anzeige-Änderung steht unabhängig davon.

## (2) Bewertungsschlagwörter (`reviews_tags`) entfernt
Der Block „Was Kunden hervorheben: satisfied (16) …" ist **ersatzlos raus** (Eintragsseite, eine
Zeile). Er war Googles `reviews_tags` im Rohzustand (englisch, mit Zählern). Gefährlich war u. a.
„damage (45)", das unter „Was Kunden hervorheben" wie ein verursachter Schaden las – eine falsche
Aussage über ein fremdes Unternehmen. **Nicht übersetzt, sondern entfernt**; die deutsche
angereicherte Beschreibung sagt bereits in Sätzen, was der Betrieb macht.

Geprüft, wo `reviews_tags`/`reviewsTags` sonst noch in die Ausgabe ginge: **nirgends** – nicht auf
Stadtseiten, nicht auf Karten/Kacheln, nicht im JSON-LD. Das Feld bleibt in den Daten (`load.mjs`
reicht es weiter), wird aber **nicht mehr gerendert**.

## Kleinigkeit A: Sonntag stand leer statt „Geschlossen"
Ursache gefunden: DataForSEO schreibt einen Ruhetag als **`"sunday": null`** (Schlüssel vorhanden,
Wert null) – nicht als leeres Intervall. `normalizeHours` gab für einen vorhandenen, aber leeren/null
Tagesschlüssel bisher einen leeren String zurück. Jetzt gilt: **ein vorhandener Tag ohne Zeiten =
„Geschlossen"** (leeres Array, null oder leer). Ein **fehlender** Tagesschlüssel erzeugt wie bisher
gar keine Zeile. Key Walter zeigt Sonntag nun „Geschlossen".

## Kleinigkeit B: „Alle 577 Städte" vs. 787 Stadtseiten
**Beide Zahlen stimmen, sie zählen Verschiedenes:**
- **577** = Städte mit mindestens `cityFloor` (2) Einträgen, die eine **eigene, indexierte**
  Stadtseite bekommen. Das ist die Zahl „Städte", die das ganze Verzeichnis verwendet
  (`stats.cities`, Zahlenkarte „577 Städte").
- **787** = **alle** Stadtseiten = die 577 **plus 210 „Kleinere Orte"** (Orte mit 1 Eintrag, je eine
  eigene `noindex`-Seite). Die Blätterseite `/verzeichnis/` listet alle 787 (Städte + kleinere Orte
  gemischt unter „Städte von A bis Z").

Die Fußzeile sagte „Alle 577 Städte", verlinkte aber auf `/verzeichnis/`, das 787 zeigt – der Label
passte nicht zum Ziel. **Fix:** die Zahl aus den Verweisen entfernt – Fußzeile und Startseite sagen
jetzt schlicht **„Alle Städte"** (→ `/verzeichnis/`). Die Kennzahl „577 Städte" bleibt dort, wo sie
die echte Städtezahl meint (Zahlenkarte, Bundesland-Zählungen). Auf der Startseite steht dadurch nur
noch **ein** „Alle Städte"-Verweis statt zweier.

## Screenshots (neu, berichte/screenshots/)
`eintrag-mit-garantie` und `stadt-mannheim`, je 1440/390 px. Die Eintragsseite zeigt jetzt nur
„Ladengeschäft" unter Leistungen, keinen Schlagwortblock, Sonntag „Geschlossen". Wie zuvor war der
Garantie-Eintrag nur **für die Aufnahme** temporär geflaggt; der ausgelieferte Stand ist unverändert
ohne Garantie (geprueft = 0).

## Prüfung
Build grün (4.629 Seiten), Schriftprüfung bestanden. Eintrag ohne bestätigtes Merkmal
(Lippstädter Sicherheitscenter) hat korrekt **keinen** Leistungen-Abschnitt; Rest der Seite intakt.
