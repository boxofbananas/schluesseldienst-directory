---
title: Merkmalserkennung – indexierte Zahl, subtypes-Zuordnung (zur Entscheidung), Mannheim-Leerfläche
type: bericht
status: zur-entscheidung
updated: 2026-11-05
---

# Merkmalserkennung: Zahl, subtypes-Vorschlag, Mannheim

## Die fehlende Zahl
Von den **1.453** Einträgen ohne bestätigtes Merkmal:
- **204** stehen in der Start-Sitemap (indexiert) — alle mit `thin=false`.
- **1.249** sind `noindex` — alle `thin=true`.

Die Überdeckung ist exakt: indexiert ↔ `thin=false`, noindex ↔ `thin=true`. Deine Vermutung stimmt:
die Gruppe sind fast ausschließlich die dünnen Einträge. **Kein Startproblem** im Kern — nur **204**
indexierte Seiten ohne Leistungen-Abschnitt (von 2.198 indexierten Eintragsseiten, ~9 %).

**204 liegt genau auf deiner Grenze (unter 200 = nichts tun).** Es ist nicht „groß". Weil es
Grenzfall ist und die subtypes-Analyse nur Lesen kostet, lege ich die Zuordnungstabelle hier vor —
**nicht angewandt**, deine Entscheidung.

## Vorschlag: Google-`subtypes` als Belegquelle (NICHT umgesetzt)
`subtypes` sind die Kategorien, die der Betrieb selbst im Google-Profil führt. Nur Werte, die sich
**eindeutig** auf ein Merkmal aus `03-attributes.json` abbilden, werden als Beleg gewertet.

### Eindeutige Zuordnung
| Google-subtype | → Merkmal | Begründung |
|---|---|---|
| `Locksmith` | `schluesseldienst_kern` | Die Google-Kategorie ist das Kerngewerbe (Türöffnung/Schließtechnik). Dieselbe Begründung wie bei der Keep-Liste: Kategorie ist Beleg. |
| `Key duplication service` | `schluessel_nachmachen` | wörtlich |
| `Emergency locksmith service` | `schluesseldienst_kern` | ist ein Schlüsseldienst (nur Kern, siehe unten) |
| `Burglar alarm store` | `einbruchschutz` | Einbruchmeldeanlagen = Einbruchschutz |

(Einen subtype `Auto locksmith`/`Car key replacement` gibt es im Datenbestand **nicht**, daher keine
Autoschlüssel-Zuordnung.)

### Bewusst NICHT zugeordnet (mehrdeutig)
- `Emergency locksmith service` → **nicht** `notdienst_24h`: „emergency" belegt einen Notdienst, aber
  nicht zwingend **24 Stunden**. Nur als Kern gewertet.
- `Safe & vault shop` → **nicht** `tresoroeffnung`: ein Tresor-Laden verkauft Tresore, öffnet sie
  nicht zwingend.
- `Security system supplier`, `Safety equipment supplier` → **nicht** zugeordnet: schwankt zwischen
  Einbruchschutz und elektronischen Schließsystemen, nicht eindeutig.
- `Lock Store`, `Locks supplier` → **nicht** `ladengeschaeft`: ein Untertyp belegt keinen
  Walk-in-Service eindeutig.
- `Shoe repair shop`, `Engraver`, `Rubber stamp store`, `Cleaners`, `Sharpening service` usw. →
  **kein** Schlüsseldienst-Merkmal (das sind Schuster/Graveure, die nebenbei Schlüssel kopieren; der
  relevante Beleg ist bei ihnen allein `Key duplication service`).

### Wirkung, wenn angewandt
- **Auf die 204:** 125 bekämen wieder einen Leistungen-Abschnitt (109 über Kern, 29 über Schlüssel
  nachmachen, 3 über Einbruchschutz); **79** blieben ohne Abschnitt (kein verwertbarer subtype).
- **Dataset-weit (nicht nur die 204!):** die Regel wirkt überall. Neu auf `true` kämen
  **+503** `schluesseldienst_kern`, **+315** `schluessel_nachmachen`, **+60** `einbruchschutz`.
  Das ist ein **Gate-3-Regeländerung mit globaler Wirkung**: mehr Leistungen-Abschnitte und mehr
  Schema-`Offers` im ganzen Verzeichnis. Inhaltlich gedeckt durch „Kategorie ist Beleg", aber eben
  nicht auf die 204 begrenzt.

### Meine Empfehlung
Grenzfall. Zwei saubere Wege:
1. **Nichts tun, nach der 30-Tage-Prüfung ansehen** — konsequent zu deiner „unter-200"-Regel; 204 ≈
   200, und es sind dünne/indexierte Seiten, die ohnehin wenig Gewicht tragen.
2. **Die vier eindeutigen Zuordnungen anwenden** — wenn du die Qualität jetzt heben willst; gut
   begründet, aber als globale Gate-3-Änderung (+503/+315/+60), nicht als 204-Pflaster.

Ich würde zu **(1)** neigen, weil die Zahl auf der Grenze liegt und die Änderung global ist. Sag,
welchen Weg; umgesetzt ist nichts.

## Mannheim: die leere rechte Hälfte (Beobachtung, kein Auftrag)
Der Einleitungstext steht in einer Lesespalte (~55 % Breite, richtige Zeilenlänge), rechts bleibt
über mehrere Bildschirme Weiß. Optionen:
- **Kartenausschnitt: würde ich nicht nehmen.** Eine Karte lädt extern (Google/OSM-Kacheln) und
  bräuchte nach unseren Regeln erst eine Einwilligung (Klick-zum-Laden), was auf einer Stadtseite
  neben dem Fließtext unpassend wirkt, und sie berührt die Footprint-Regel.
- **Sprungliste der Betriebe: meine Empfehlung.** Eine kompakte, klebende Liste „Betriebe in
  Mannheim" rechts neben der Einleitung, die zu den Karten weiter unten (oder direkt zu den
  Eintragsseiten) springt. Nur Links, kein externer Ladevorgang, zusätzliche interne Verlinkung,
  echte Navigationshilfe auf langen Stadtseiten. **Nur** ab einer sinnvollen Zahl (z. B. ≥ 8
  Betriebe) einblenden, sonst entfällt sie; auf dem Handy stapelt sie unter die Einleitung.
- **Bewusst leer lassen** wäre vertretbar, wirkt aber wie gesagt unfertig.

Wenn du die Sprungliste willst, baue ich sie in einem eigenen Schritt (mit der ≥8-Schwelle und
mobilem Stapeln). Nichts davon ist umgesetzt.
