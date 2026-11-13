# AGB B1 (Premium-Eintrag) an die Link-Regel angepasst

**Datum** 2026-11-13 · **Stand** main, live · **Deployment** ee8524e7 · **check_live** 2821 bestanden
Ausdrückliche Betreiberfreigabe für genau diese Stelle. Build **und** Template geändert (Standdatum nur Build).

## Diff (`src/pages/agb.astro`)

**Standzeile (Zeile 13) — nur Build:**
```diff
-    <p>Stand {buildDateDe}.</p>
+    <p>Stand 13.11.2026.</p>
```
Im **Template** bleibt `Stand {buildDateDe}.` stehen: ein fester Datumstext gehört zu dieser
veröffentlichten Fassung, nicht in das Gerüst künftiger Verzeichnisse.

**B1, Premium-Eintrag (Build und Template):**
```diff
       <li>
         <strong>Premium-Eintrag:</strong> hervorgehobene Darstellung des Eintrags, Aufnahme von durch den
-        Kunden bereitgestellten Bildern, Verlinkung der Website und der Profile des Kunden ohne
-        Suchmaschinen-Einschränkung, Einbindung einer Karte, Angabe der Öffnungszeiten.
+        Kunden bereitgestellten Bildern, Verlinkung der Website und der Profile des Kunden, als bezahlte Platzierung
+        gekennzeichnet, Einbindung einer Karte, Angabe der Öffnungszeiten. Ein Link ohne diese
+        Kennzeichnung ist allein mit der Festpreis-Garantie verbunden und nicht Gegenstand dieser
+        Bedingungen.
       </li>
```
Sonst nichts an den AGB geändert.

## Beschreiben /premium/, featured-tiers.md und die AGB den Premium-Eintrag jetzt gleich?

**Ja, deckungsgleich** in der Aussage: der Premium-Eintrag bringt den Website-/Profil-Link, **als
bezahlt gekennzeichnet** (`rel="sponsored"`); der **gefolgte** Link ohne Kennzeichnung hängt allein an
der Festpreis-Garantie und nicht an der Stufe.

| Quelle | Wortlaut (Kern) |
|---|---|
| **AGB B1** | „Verlinkung der Website und der Profile des Kunden, **als bezahlte Platzierung gekennzeichnet** … Ein Link ohne diese Kennzeichnung ist **allein mit der Festpreis-Garantie** verbunden und nicht Gegenstand dieser Bedingungen." |
| **/premium/** (Kachel) | „… dazu der **als bezahlt gekennzeichnete Link** auf Ihre Website." |
| **/premium/** (Prosa) | „Der Website-Link gehört zu jeder bezahlten Stufe (als bezahlt gekennzeichnet) oder zur **Festpreis-Garantie** (ohne nofollow); ohne beides fehlt er." |
| **featured-tiers.md** | „… der Website- und Profil-Link … ist als bezahlter Platz mit `rel="sponsored"` **gekennzeichnet** … Der gefolgte Link ohne nofollow gehört zur **Festpreis-Garantie**, nicht zu einer Stufe." |

## Textgate (gebaute Seite, `--erlaube-rechtswoerter`)

- Wörter 898 (im Band), Floskeln und Rechtswörter **bestanden** (Rechtswörter für /agb/ zugelassen).
- Einziger Befund: **„Gedankenstriche: 2"** — die **vorbestehenden** Abschnittsüberschriften
  „Teil A — Nutzung des Verzeichnisses" und „Teil B — Bedingungen für bezahlte Einträge und
  Werbeplätze". Sie stammen nicht aus dieser Änderung (B1 enthält keinen Gedankenstrich) und wurden
  nach deiner Vorgabe „sonst nichts an den AGB ändern" **nicht** angefasst. Nur gemeldet — falls
  gewünscht, ließen sich die beiden „ — " in den Überschriften später durch einen Doppelpunkt
  ersetzen.

## Live-Prüfung

- check_live `--expect-urls 2821`: alle Prüfungen bestanden.
- `/agb/` live: „Stand 13.11.2026." und der vollständige B1-Wortlaut bestätigt.
