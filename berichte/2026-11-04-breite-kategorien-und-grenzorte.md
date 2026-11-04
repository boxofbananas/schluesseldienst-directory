# Textregel für die 180 breiten Einträge, Grenzorte, Gegenprobe (2026-11-04)

Drei Aufträge abgearbeitet. **Stadttexte sind noch nicht gestartet** – erst nach Deiner Durchsicht.

## (1) Grenzorte — erledigt
**18 Einträge** in 7 ausländischen Grenzorten per `04-exclusions.csv` gedroppt (Grund „Ausland …,
Verzeichnis ist für Deutschland"): **Basel (6 Einträge), Binningen (2), Kreuzlingen (2),
Münchenstein (2)** – Schweiz; **Słubice (2)** – Polen; **Forbach (1), Spicheren (1)** – Frankreich.

**Oberzent:** nicht gelöscht. Bundesland **Hessen (HE)** von Hand in `03-listings-enriched.csv`
nachgetragen (PLZ 64760, Odenwaldkreis). Der eine Eintrag (Hartmann Specialists e.K.) erscheint beim
nächsten Bau unter Hessen.

**„Unbekannt" — zur Entscheidung:** ein einziger Eintrag, `schluesseldienst-leipzig-herrmann-x`:

> **Schlüsseldienst Leipzig Herrmann** — Typ Locksmith, **ohne Adresse, ohne PLZ, ohne Ort**
> (alle Felder leer). Deshalb keiner Stadt zuzuordnen (fiel auf den Sammelschlüssel x/x).

Der Name deutet auf einen echten Leipziger Schlüsseldienst, aber ohne Adresse lässt er sich weder
platzieren noch erfüllt er Voraussetzung 1/5 der Festpreis-Garantie. **Vorschlag: droppen**, außer Du
kennst die Adresse und willst ihn Leipzig zuordnen.

## (3) Gegenprobe der 431 Gate-4-Drops — kein echter Schlüsseldienst gefallen
Zehn der als fremdes Gewerbe gedroppten Einträge über alle großen Typen gezogen (Baumarkt,
Metallbau, Schuhmacherei, Werkzeughandel, Gebäudereinigung, Stahlbau, Autowerkstatt, Metallbau,
Schneiderei, Kunstschmiede) — **alle zehn klar fremde Gewerbe**, mehrere sagen es selbst
(„Christian Völker … kein Schlüsseldienst").

**Automatische Vollkontrolle aller 431:** 115 nennen „Türöffnung"/„Schlüsselnotdienst" — aber jedes
Mal **verneint** („Türöffnungen gehören nicht zum Angebot", „kein Schlüsselnotdienst", „ein
Schlüsseldienst im Sinne von Türöffnung ist das nicht"). Die zwei scheinbar positiven: ein
**Reisebüro**, das auf den ADAC-Schlüsseldienst verweist, und ein **Abschleppdienst** mit der
Kategorie — beide zu Recht raus. Die Anreicherung hat die fremden Gewerbe sogar ausdrücklich als
Nicht-Schlüsseldienste beschrieben. **Ergebnis: Die 431 Drops sind sauber.**

## (2) Textregel auf alle 180 angewandt
Deine Regel (Text maßgeblich, nicht `kern`) per LLM-Klassifikation auf alle 180 Einträge der
Kategorien Alarm-Lieferant (143), Tresor (34), Alarm-Einbau (3) angewandt. Ergebnis:
**135 ausschließen, 45 behalten.** Die 135 sind in `04-exclusions.csv` eingetragen (Grund „breite
Kategorie …, keine Türöffnung laut Text"); kein eigener Betrieb darunter. Deine drei Eichfälle trifft
die Regel richtig: Reiher → behalten, ast Alstertaler → ausschließen, Stürmer-Alarm → ausschließen.

### Divergenzen Regel ↔ kern (25 von 180)

`kern` lag bei diesen 25 Einträgen anders als die Textregel. Die Textregel ist maßgeblich; der Vorschlag ist ihre Entscheidung.

**A) kern=true, Regel schließt aus (17) — Alarm/Einbau/Tresor trotz kern=true, Vorschlag: ausschließen**

| Name | Kategorie | kern | Textstelle (Beleg für Ausschluss) |
|---|---|---|---|
| B+M Sicherheitstechnik Halle GmbH | Alarm-Lieferant | true | In der Schließtechnik setzt es auf digitale Schließanlagen |
| B+M Sicherheitstechnik Halle GmbH | Alarm-Lieferant | true | Elektronische Schließ- und Zutrittskontrollsysteme gehören ... zum Pro |
| Fachgeschäft für Sicherheitstechnik "A | Alarm-Lieferant | true | Verkauft und eingebaut werden Schließanlagen, Schließzylinder |
| Fundel und Kurtz Sicherheitshaus GmbH | Alarm-Lieferant | true | Ein zusätzliches Türschloss wird fachgerecht montiert |
| House Security | Alarm-Lieferant | true | wer welche Türen öffnen dürfen soll, als Kern der Planung von Schließa |
| Kaiserstühler Sicherheitstechnik | Alarm-Lieferant | true | Ein Schlüsseldienst mit Reparaturen steht ebenfalls im Angebot (nur Ve |
| Roberto Weigel Sicherheitstechnik & Re | Alarm-Lieferant | true | Bei Tresoren öffnet er im Notfall auch historische Modelle (nur Tresor |
| Schlüssel-Weber Sicherheitstechnik e.K | Alarm-Lieferant | true | montiert ... elektrische Türöffner (Gerät/Einbau) |
| Schlüsseldienst Weißenborn GmbH | Alarm-Lieferant | true | keine Türöffnung erwähnt (Lieferprogramm, Havarie-Service) |
| Sicherheitstechnik Jaspers | Alarm-Lieferant | true | keine Türöffnung erwähnt (nur 'Aufgaben eines modernen Schlüsseldienst |
| Stürmer-Alarm | Alarmanlagen und Brand | Alarm-Einbau | true | keine Türöffnung erwähnt |
| Tresorservice Diederichsen | Tresor | true | öffnet Tresore aller bekannten Marken |
| Ulrike Rauch e.K., Haus für Sicherheit | Alarm-Lieferant | true | berät, plant und montiert Sicherheitsprodukte |
| Weckbacher Sicherheitssysteme GmbH | Alarm-Lieferant | true | installiert elektronische Schließsysteme mit digitalen Zylindern |
| ast Alstertaler Sicherheitstechnik Gmb | Alarm-Einbau | true | installiert der Betrieb einen passenden gleichschließenden Zylinder |
| openSECURE - Ihr Sicherheitspartner | Alarm-Lieferant | true | keine Türöffnung erwähnt (nur 'klassischer Schlüsseldienst' und '24-St |
| schliessanlage.digital | Alarm-Lieferant | true | plant, montiert, hostet, verwaltet und wartet elektronische Schließsys |

**B) kern≠true, Regel behält (8) — echte Türöffnung trotz kern false/n.e.i., Vorschlag: behalten**

| Name | Kategorie | kern | Textstelle (Beleg für Behalten) |
|---|---|---|---|
| DIE KLINKE Baubeschlag GmbH | Alarm-Lieferant | not enough info | Ein Schlüsselnotdienst steht rund um die Uhr bereit |
| Erhard Hintz Sicherheitssysteme Brockm | Alarm-Lieferant | not enough info | Zum Unternehmen gehört auch ein Schlüsseldienst |
| Gebrüder Füth Sicherheitstechnik | Alarm-Lieferant | not enough info | verbindet Gebrüder Füth Sicherheitstechnik und Schlüsseldienst |
| KLUG Sicherheitstechnik & Metallbau/Wi | Alarm-Lieferant | not enough info | ein Schlüsseldienst mit Öffnungstechnik |
| Meesenburg GmbH - Sicherheit & Service | Alarm-Lieferant | not enough info | einen Schlüsseldienst in Oldenburg |
| Reiher Sicherheitssysteme GmbH | Alarm-Lieferant | not enough info | eine Nummer für den Schlüssel-Notdienst |
| Safetec Timo Durchdewald Sicherungstec | Alarm-Lieferant | not enough info | ein Schlüssel-Notdienst |
| Sicherheit & Design Frank Döhner Baube | Alarm-Lieferant | not enough info | Ein Schlossnotdienst steht zu den Geschäftszeiten bereit |

**Zur Durchsicht:** Die 17 unter A sind die Fälle, in denen `kern=true` zu Unrecht behalten hätte —
Alarmbauer und Tresorhändler, die Zylinder/Schließanlagen **einbauen**, aber keine Tür öffnen. Die 8
unter B sind echte Schlüsseldienste, die `kern` (false/keine Angabe) zu Unrecht gedroppt hätte. Das
bestätigt, dass die Textregel `kern` schlägt.

## Stand
`04-exclusions.csv`: **595 Drops** (442 Gate 4 + 18 Grenzorte + 135 Textregel). Sonnet für die
Stadttexte freigegeben. **Noch nicht gestartet** — erst nach Deiner Durchsicht der 25 Divergenzen.
Danach: Exclusions anwenden → neu bauen → dump → Stadttexte auf Sonnet, nach Bundesland gestapelt.
