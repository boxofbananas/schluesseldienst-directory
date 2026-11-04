# Nachbestellungs-Test (2026-11-04)

Zweck: prüfen, ob der ursprüngliche `locksmith`-Abruf (3.102 bundesweit) lückenhaft war und ob
breitere Kategorien mehr echte Schlüsseldienste bringen – bevor in Gate 5 Stadttexte entstehen.

## Stichprobentest über 10 Städte (10-km-Umkreis)
Alle Städte aus den 194 „Einwohner ≥ 20.000, genau 1 Eintrag". V1 = nur `locksmith`,
V2 = acht schlüsseldienstnahe Kategorien.

| Stadt | EW | unsere Stadt | unser 10 km (roh) | V1 ≥1 Bew. | V1 alle | V2 ≥1 | V2 alle |
|---|--:|--:|--:|--:|--:|--:|--:|
| Speyer (RP) | 50.343 | 1 | 5 | 7 | 9 | 15 | 21 |
| Königswinter (NW) | 41.164 | 1 | 15 | 15 | 16 | 34 | 40 |
| Hofheim a.Ts. (HE) | 37.750 | 1 | 14 | 18 | 21 | 59 | 66 |
| Mörfelden-Walldorf (HE) | 32.753 | 1 | 11 | 16 | 17 | 44 | 54 |
| Zeitz (ST) | 28.328 | 1 | 1 | 1 | 1 | 2 | 3 |
| Helmstedt (NI) | 25.515 | 1 | 3 | 3 | 3 | 3 | 3 |
| Harsewinkel (NW) | 24.207 | 1 | 1 | 1 | 1 | 5 | 5 |
| Geretsried (BY) | 23.364 | 1 | 7 | 7 | 7 | 15 | 16 |
| Metzingen (BW) | 22.112 | 1 | 11 | 11 | 11 | 27 | 29 |
| Heusweiler (SL) | 20.006 | 1 | 8 | 11 | 13 | 20 | 24 |
| **Summe** | | **10** | **76** | **90** | **99** | **224** | **261** |

**Befund:** „1 Eintrag je Stadt" ist überwiegend Stadt-vs-Umkreis (die übrigen Betriebe gehören zu
Nachbarstädten), kein Erfassungsfehler. Echte Lücke unter gleicher Kategorie ~16 % (76 vs. 90),
nur im Ballungsraum. Nachbarkategorien bringen 2,5× (90→224), teils echt schlüsseldienstnah, teils
Alarm-/Wachgewerbe.

Kategorien in V2: `locksmith`, `emergency_locksmith_service`, `key_duplication_service`,
`lock_store`, `locks_supplier`, `safe_and_vault_shop`, `security_system_supplier`,
`security_system_installer`. Testkosten 0,49 $.

## Breiter Abruf + Umkreis
- Breit (8 Kategorien, bundesweit, ohne Bewertungsfilter): **9.478** Einträge, 3,53 $.
- Umkreis (381 Stadtseiten ≥ 2 Einträge, 10 km, Item-Abruf): 7.591 eindeutige, 9,21 $. Fügt dem
  breiten Abruf wenig hinzu (Prioritätsstädte: Mannheim +8, Ludwigshafen +7, Heidelberg +5,
  Nürnberg +1, Fürth +2).
- Vereinigt und gegen den Bestand entdoppelt: **6.796 neu**, nach Gate-2-Basis **5.564 neu**
  (4.648 mit Website).

## Zweistufiger Filter auf dem Website-Rohtext (fetch_sites)
| Stufe | Anzahl | Behandlung |
|---|--:|---|
| A – Türöffnung belegt | **1.106** | anreichern |
| B – Schloss/Schlüssel ohne Türöffnung | **299** | behalten, Welle 2 |
| Grundeintrag (ohne Website, `locksmith`/`emergency`) | 59 | behalten, keine Anreicherung |
| ausgeschlossen | **4.100** | raus (davon 2.116 `security_system_*`) |

Stichprobe A: „Schlüsseldienst Leipzig Herrmann", „Service Punkt Schlüsseldienst", „Autoschlüssel
Service Hilden" (… als Schlüsseldienst …). Randfälle, die Gate 3 als Kern=false fängt:
„Sonderpreis Baumarkt", „Derr Kfz – Autoschlüsseldienst".
Stichprobe ausgeschlossen: Orange (ISP), Verisure/Somfy (Alarm/Rollläden), medisign
(E-Signaturen), Hagebaumarkt, Bikeopia (Fahrräder), Car-Key-Repair (nur Autoschlüssel).

## Struktur mit erweitertem Datensatz (SIMULIERT – echter Build folgt)
| | jetzt | erweitert |
|---|--:|--:|
| Stadtseiten ≥ 2 Einträge | 381 | 599 |
| Einzelseiten (Entfernung 46 · Einwohner 139 · beides 6) | 260 | 191 |
|   indexierbar über „Betriebe in der Umgebung" (≥1 Nachbar <10 km) | 148 | 125 |
|   bleiben noindex | 112 | 66 |
| gefaltete Orte | 475 | 761 |

## Kosten und Wellen
- Abrufe bereits ausgegeben (versunken): ~14–15 $.
- Anreicherung (Abo, ~4,6 ct/Eintrag):
  - Welle 1 (Stufe A auf Start-Sitemap-Stadtseiten): 863 → ~40 $, live.
  - Welle 2 (Stufe A außerhalb 243 + alle Stufe B 299): 542 → ~25 $, nach 30 Tagen.
- Gate-5-Texte: 790 (599 Stadt + 191 Ort), +149; zum Start nötig ~724; Kosten pilot-geschätzt
  ~60–110 $ (Stadttext-Probe pinnt es fest).

## Entscheidung des Betreibers (2026-11-04)
Nachbestellung integrieren, Welle 1 starten. Zwei Korrekturen: (1) Baumarkt-/Handelsketten per
Namensliste vor der Anreicherung ausschließen, auch bei Stufe A; (2) Stadttext-Probe mit
kleinerem Modell vergleichen. Struktur am echten Build bestätigen, bevor Texte entstehen.
</content>
