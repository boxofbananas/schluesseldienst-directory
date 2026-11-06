# Festpreis-Garantie für 16 weitere eigene Betriebe

**Datum:** 2026-11-06
**Auslöser:** Daniel — 16 weitere eigene Betriebe bekommen die Festpreis-Garantie. Gleiche
Zuschläge und Material überall, nur der Grundpreis (`garantie_tag`) unterscheidet sich.

Für alle 16: `geprueft = true`, `geprueft_jahr = 2026`, `garantie_zuschlag_abend = 30`,
`garantie_zuschlag_nacht = 40`, `garantie_anfahrt = 0`, `garantie_zylinder = 39`,
`garantie_zylinder_5mm = 3`.

## Zuordnung (über Name **und** Ort, nicht über den Namen allein)

Zwei Orte haben je zwei unserer Betriebe (Heidelberg, Hockenheim); dort war die Ort-Spalte allein
nicht genug, der Name entschied. Jeder Betrieb ließ sich **eindeutig** einer CSV-Zeile zuordnen —
keiner blieb unklar.

| Betrieb | Ort | `garantie_tag` | CSV-Zeile (slug) |
|---|---|---:|---|
| Sperber Schlüsseldienst | Heidelberg | 89 | `sperber-schluesseldienst-heidelberg` |
| Heidelberg Schlüsseldienst | Heidelberg | 89 | `heidelberg-schluesseldienst-heidelberg` |
| Merz Schlüsseldienst Ludwigshafen | Ludwigshafen | 89 | `merz-schluesseldienst-ludwigshafen-ludwigshafen-am-rhein` |
| I-S-E Schlüsseldienst | Hockenheim | 89 | `i-s-e-schluesseldienst-hockenheim` |
| Mein Schlüsseldienst Hockenheim | Hockenheim | 89 | `mein-schluesseldienst-hockenheim-hockenheim` |
| Riegelklar Schlüsseldienst Schwetzingen | Schwetzingen | 89 | `riegelklar-schluesseldienst-schwetzingen-schwetzingen` |
| Merz Schlüsseldienst Worms | Worms | 99 | `merz-schluesseldienst-worms-worms` |
| Mein Schlüsseldienst Weinheim | Weinheim | 99 | `mein-schluesseldienst-weinheim-weinheim` |
| Merz Schlüsseldienst Speyer | Speyer | 99 | `merz-schluesseldienst-speyer-speyer` |
| Kurpfalz Schlüsseldienst Wiesloch | Wiesloch | 99 | `kurpfalz-schluesseldienst-wiesloch-wiesloch` |
| Hardt Schlüsseldienst Waghäusel | Waghäusel | 99 | `hardt-schluesseldienst-waghaeusel-waghaeusel` |
| Rheinpfalz Schlüsseldienst Frankenthal | Frankenthal (Pfalz) | 99 | `rheinpfalz-schluesseldienst-frankenthal-frankenthal-pfalz` |
| Odenwald Schlüsseldienst Bensheim | Bensheim | 99 | `odenwald-schluesseldienst-bensheim-bensheim` |
| Kraichgau Schlüsseldienst Sinsheim | Sinsheim | **119** | `kraichgau-schluesseldienst-sinsheim-sinsheim` |
| Pälzer Schlüsseldienst Neustadt | Neustadt a. d. Weinstraße | **119** | `paelzer-schluesseldienst-neustadt-neustadt-an-der-weinstrasse` |
| Südpfalz Schlüsseldienst Landau | Landau in der Pfalz | **119** | `suedpfalz-schluesseldienst-landau-landau-in-der-pfalz` |

Verteilung der Grundpreise: 89 € (6), 99 € (7), 119 € (3). Geprüfte Betriebe gesamt jetzt **18**
(die 16 plus Merz Sicherheit und AES Schlüsseldienst Mannheim).

## Nicht eingetragen — fehlende Telefonnummer

Drei Betriebe verfehlen **Voraussetzung 2** der Festpreis-Garantie (erreichbare Telefonnummer).
Ihre `phone`-Spalte ist leer; sie bleiben ohne Garantie:

- **Ried Schlüsseldienst Viernheim** (`ried-schluesseldienst-viernheim-viernheim`)
- **Türklar Schlüsseldienst Leimen** (`tuerklar-schluesseldienst-leimen-leimen`)
- **Lampertheimer Schlüsseldienst** (`lampertheimer-schluesseldienst-lampertheim`)

Sobald eine erreichbare Nummer vorliegt und die übrigen Voraussetzungen erfüllt sind, können sie
nachgezogen werden.

## Prüfung

Vor dem Ausliefern jede der 16 Eintragsseiten im Build gegen den vorgegebenen Grundpreis geprüft:
Grundpreis im Preisblock = vorgegebener `garantie_tag`, Zuschläge +30/+40, Zylinder 39 € — **0
Fehler**, besonders die drei 119-€-Orte stimmen (ein vertauschter Grundpreis wäre dort am
teuersten gewesen).

Nach dem Ausliefern je Stadt live geprüft (`curl`): die Stadtkarten-Zeile „Festpreis-Garantie ·
Türöffnung ab … €" trägt in jeder der 14 Städte den richtigen Betrag, in Heidelberg und Hockenheim
je zweimal (beide 89 €), und **kein** abweichender Ab-Preis taucht auf einer Stadtseite auf.
Bildschirmfoto des vollen Preisblocks am 119-€-Ort Sinsheim (Kraichgau Schlüsseldienst): drei
Gruppen, Grundpreis 119 €, Zuschläge +30/+40 mit „Zuschläge werden nicht addiert", Material 39 €/+3 €.

`check_live.py`: bestanden außer der www-Umleitung (Token weiter ohne Dynamic-Redirect-Recht —
Daniels Schritt).

## Stand

Gebaut (4629 Seiten, Migrations-Riegel grün), ausgeliefert, live geprüft. 18 Betriebe mit
Festpreis-Garantie. Offen bei Daniel: die www-Weiterleitung.
