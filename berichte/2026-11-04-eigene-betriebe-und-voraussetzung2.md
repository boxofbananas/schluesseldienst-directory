# Eigene Betriebe vervollständigt + Voraussetzung 2 geändert (2026-11-04)

## (1) Acht eigene Betriebe nachgetragen
`input/eigene-betriebe.csv` um 7 Zeilen ergänzt (Schwetzingen war bereits enthalten, daher per
Domain entdoppelt → 20 Zeilen). `add_own_listings.py` erneut gelaufen: **+8 nachgetragen** (die 7
neuen + Schwetzingen), alle 8 exakt über Nominatim geokodiert; die übrigen 12 als Dublette
übersprungen. 02 jetzt **4.387** Zeilen.

Nachgetragen: AES Schlüsseldienst Mannheim, Sperber Schlüsseldienst (Heidelberg), Merz
Schlüsseldienst Worms, Merz Schlüsseldienst Ludwigshafen, Mein Schlüsseldienst Weinheim, I-S-E
Schlüsseldienst (Hockenheim), Merz Schlüsseldienst Speyer, Riegelklar Schlüsseldienst Schwetzingen.

**Merz Sicherheit Mannheim – nicht nachgetragen, Anschrift geprüft:** im Scrape als
„Schulstraße 87, 68199 Mannheim", Telefon 0621-79936088 → **stimmt** mit der angegebenen Adresse.

### Schwetzingen-/Arslan-Fall behoben
- Der Eintrag „Schlüsseldienst und Schuhmacherei K.Arslan" (Ludwigshafen) gehört **nicht** zu den
  eigenen Betrieben, trug im Google-Export aber dieselbe Nummer (+4915563825636) wie Schwetzingen.
  Dadurch war Schwetzingen fälschlich als Dublette verworfen und Arslan als `owned` markiert.
- **`owned` bei Arslan zurückgenommen** (false). **Schwetzingen regulär aufgenommen.**
- **Dublettenregel in `add_own_listings.py` geändert:** eine übereinstimmende Telefonnummer allein
  begründet keine Dublette mehr; nur gleiche Domain **oder** gleiche Anschrift zählt.

### Struktur neu gerechnet (echter Build, `dump-cities.mjs`)
3.945 Einträge (442 gedroppt). **597 Stadtseiten ≥ 2 Einträge**, **209 Einzelseiten** (46
Entfernung, 140 Einwohner, 6 beides), davon **132 indexierbar** über „Betriebe in der Umgebung";
**729 Start-Sitemap-Stadtseiten**. 806 Stadt-/Ortsseiten gesamt.

### Footprint ([[footprint-rules]], aktualisiert)
Zwei eigene Betriebe je Stadt in **Mannheim, Heidelberg, Hockenheim** (bestätigt). Dort darf
höchstens einer einen bezahlten Platz bekommen. Festgehalten, dass die Stadtseiten-Sortierung
`owned` **nicht** liest und keine Ausnahme für eigene Betriebe macht.

## (2) Voraussetzung 2 der Festpreis-Garantie geändert
**Neu:** „Eine Telefonnummer, unter der der Betrieb erreichbar ist und bei der Prüfung tatsächlich
abgehoben hat. Die Nummer wird vor der Erteilung angerufen."

Begründung (im Wiki): Voraussetzung 1 verlangt bereits ein vollständiges Impressum mit Anschrift,
Voraussetzung 5 schließt ortsfremde Callcenter-Weiterleitung aus. Die Festnetz-/Vorwahl-Forderung
fügte wenig hinzu, hätte aber Betriebe ausgeschlossen, die alle inhaltlichen Voraussetzungen
erfüllen. Die telefonische Prüfung ist die stärkere Aussage (Anruf statt Vorwahl).

Angeglichen in: `konventionen.md`, `siegel-programm.md`, `/festpreis-garantie/` (Punkt + „Was wir
prüfen": die Nummer wird angerufen) und **beiden Antragsformularen** (`claim-form.html` und die
astro-Antragsseite): Telefonnummer bleibt Pflichtfeld, der Hinweis „reine Mobilnummer reicht nicht"
entfällt, neuer Hinweis „wir rufen diese Nummer an".

**Unverändert:** die Stadtseiten-Sortierung (bezahlte Plätze → Garantie → Festnetz mit zur PLZ
passender Ortsvorwahl → Rest). Die Ortsvorwahl bleibt ein **Sortier**signal, ist aber keine
Garantie-Voraussetzung mehr.

## Stand
Datenstand und Rechtstexte aktualisiert. Weiterhin offen für den Bau (nach Entscheidung):
Stadttext-Probestapel und die Formular-Function.
</content>
