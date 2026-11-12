# Rückgabe an Henry — Design-Pilot 1 (Website)

Kompakte Rückmeldung aus der Umsetzung des Website-Piloten. **Nur Vorschläge**; nichts wurde in
Henrys Skills, Learning-Registry oder das Medien-Repo geschrieben.

## Wiederverwendbare Layoutentscheidungen

- **Zweispaltiger Hero (Navy links, helle Karte rechts)** trägt gut, wenn die linke Spalte den
  echten Bestandstext behält (Augenbraue, nutzenorientierte H1, Vorspann, Suche, Belege) und die
  rechte Karte **echte Daten** zeigt statt Platzhalter. Ab ~1024 px zweispaltig, darunter einspaltig
  mit der Suche vor der Karte.
- **Helle Fläche rechts** als absolut positioniertes Panel mit gerader/leicht schräger Kante
  (`clip-path`) hinter einer schwebenden weißen Karte (starker, weicher Schatten) — ein einziger
  dezenter Zierkreis reicht.
- **Ergebnisliste als Zeilenkarten** (Angaben links gestapelt, Kontakt + eine ruhige „Details"-Pille
  rechts, vertikal mittig über Grid-Platzierung) liest sich auf Verzeichnisseiten klarer als enge
  Kacheln. Links eine schmale, klebende Orientierungsspalte auf getönter Fläche.
- **Pillen-Suche mit Lupe** und sichtbarer Beschriftung; große Kartenradien (~22 px) und ein weicher
  Schatten als durchgehende Marken reichen, um die Referenzstimmung zu treffen.

## Konkrete Problemfälle der Referenzen im echten Layout

- Die **grauen Balken, Symbolkacheln (`+ ○ ^`), die Stecknadel-Karte, die Rasterpunkte und die
  zweifarbige Fortschrittslinie** sind reine Medienelemente. Im echten Layout wurden sie durch echte
  Links/Daten ersetzt; als „Inhalt" wirken sie sonst wie eine Anzeigenseite und täuschen Funktion vor.
- Das **einzelne „D"** ist kein Logoauftrag — Logo/Favicon blieben.
- Mobil gewinnt die **Suche** den ersten Bildschirm nur, wenn die Kopfzeile nicht umbricht; eine lange
  Wortmarke erzwingt ein eingeklapptes Menü (hier zugänglich per Checkbox statt `<details>`, damit die
  Links auf dem Desktop in der Tab-Reihenfolge bleiben).
- Der **Bernstein-Akzent** braucht dunkle Schrift und auf hellen Flächen einen dunklen Fokusring
  (Bernstein auf Weiß < 3:1).

## Markenwerte — nur als Vorschlag

Aus den PNGs abgeleitet, im Website-Build gesetzt; **keine neue globale Markenfassung**:

- `cardRadius: 22px`, `cardShadow: 0 18px 44px -26px rgba(11,37,69,.30), 0 4px 12px -8px rgba(11,37,69,.14)`,
  `spaceSection: clamp(3.25rem, 6vw, 5.5rem)`, `buttonRadius: 999px`.
- Farben/Schriften wie gemessen aus den vorhandenen Marken (Navy `#0B2545`, Bernstein `#F5A623`,
  Petrol `#126665`, Tönung `#E6F2F4`, Fläche `#F5F6F8`; Roboto Slab / Roboto). Die PNG-Abweichungen
  waren Renderrauschen — kein Anlass, die Palette zu ändern.

Übernahme ins projektübergreifende Markenwissen bitte über den bestehenden Henry-Prozess, geprüft.
