---
title: Gate 4 – Callcenter ohne Ortsbezug (Entscheidung 9)
type: output
status: entschieden
updated: 2026-11-04
---

# Callcenter ohne Ortsbezug (Entscheidung 9)

Ausschluss nur bei **≥ 2** zutreffenden Merkmalen. Geprüfte Merkmale:

- Ortsvorwahl der Festnetznummer passt nicht zur PLZ (Heimvorwahl je Stadt datenintern aus den
  Festnetznummern der Stadt abgeleitet; Städte mit < 2 Festnetznummern nicht geprüft),
- Anschrift ist Postfach, Packstation oder „c/o",
- nur eine 0800-/0180-Nummer als Kontakt,
- dieselbe Nummer in mehreren Städten.

**Entfernt (Betreiber, 2026-11-04): das Merkmal „keine Straße".** Begründung: Bei
Schlüsseldiensten ist das Service-Area-Geschäft der Normalfall; Google blendet die Anschrift
dort selbst aus. Eine fehlende Straße ist deshalb **kein** Vertrauensmerkmal und damit auch das
abgeleitete „nur Mobil ohne Straße" nicht. Eine Mobilnummer allein ist ohnehin kein
Ausschlussgrund.

## Ergebnis

**0 Kandidaten** mit ≥ 2 Merkmalen. Die Daten aus dem DataForSEO-Abruf sind in dieser Hinsicht
sauber: 0 Postfach/Packstation, 3 reine 0800-Nummern (jeweils ohne zweites Merkmal), keine
Festnetznummer mit ortsfremder Vorwahl in Städten mit genug Vergleichsnummern, keine Nummer in
mehreren Städten, die nicht schon über die Ketten-Prüfung (Entscheidung 8) abgedeckt wäre.

Der zuvor zur Prüfung hierher verschobene Eintrag mit Google-Kategorie
`emergency_locksmith_service` trägt **kein** Merkmal und bleibt als regulärer Grundeintrag.

**Keine Zeilen in `04-exclusions.csv` aus dieser Entscheidung.**
</content>
