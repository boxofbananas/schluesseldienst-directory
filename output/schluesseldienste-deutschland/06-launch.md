---
title: Gate 6 – Schlanker Start
type: output
status: vorab-festlegungen
updated: 2026-11-04
---

# Gate 6 – Schlanker Start

Dieser Stand sammelt Festlegungen, die vor Gate 6 getroffen wurden. Der volle Indexierungs-
und Auslieferungsplan entsteht in Gate 6 ([[launch-lean]]).

## Vorab-Festlegung aus Gate 4 (Betreiber, 2026-11-04)

**Stadtseiten mit nur einem Eintrag kommen zum Start NICHT in die Sitemap.** Sie werden wie die
dünnen Eintragsseiten behandelt (gebaut, verlinkt, `noindex`) und erst nach der 30-Tage-Prüfung
**tranchenweise** freigeschaltet. Umgesetzt in `load.mjs` (`noindexPaths` für `count <= 1`).

- Mit den gewählten Einstellungen (Stadt-Mindestzahl 2, `foldMaxKm` 30, `cityMinPopulation`
  20.000) sind das **260** eigenständige 1-Eintrag-Stadtseiten: 66 nur über die Entfernung
  (`foldMaxKm`), 180 nur über die Einwohnerzahl (Mittelstadt-Regel), 14 über beides.
- Zum Start indexiert sind die **381 Stadtseiten mit mindestens zwei Einträgen**; die Start-
  Sitemap umfasst rund **2.225 Seiten**.
- Reihenfolge der Freischaltung wie bei den dünnen Einträgen: nach der 30-Tage-Prüfung, dort wo
  die Indexierung der Stadt- und Bundesland-Seiten trägt ([[launch-lean]], Abschnitt „Erweitern").
</content>
