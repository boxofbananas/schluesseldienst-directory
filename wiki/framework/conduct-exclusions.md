---
title: Ausschluss wegen Verhaltens
type: framework
status: stable
updated: 2026-11-04
---

# Ausschluss wegen Verhaltens

Das Verzeichnis listet grundsätzlich **jeden** Schlüsseldienst in Deutschland ([[footprint-rules]]).
Ein Betrieb wird nur aus zwei Gründen entfernt: Er ist **kein Schlüsseldienst**
([[directory-overview]], Punkt 3), oder sein **Verhalten** gegenüber Kunden oder dem Betreiber ist
belegt zu beanstanden. Diese Seite hält den Maßstab für den zweiten Fall fest. Er gilt für **alle**
Betriebe gleich — auch für die eigenen ([[footprint-rules]]).

## Wann ein Betrieb wegen Verhaltens ausgeschlossen wird

Ein Ausschluss setzt **einen belegten** der folgenden Punkte voraus, nicht einen bloßen Verdacht:

1. **Behördliche oder Verbraucher-Warnung.** Eine Verbraucherzentrale, die Polizei oder eine andere
   amtliche Stelle warnt namentlich vor dem Betrieb.
2. **Presse- oder Gerichtsbericht.** Eine nachvollziehbare Quelle (Zeitung, Urteil, Ermittlungs­
   verfahren) dokumentiert Betrug, Wucher, Nötigung oder ähnliches Fehlverhalten.
3. **Auffälliges Bewertungsmuster mit Preisstreit.** Mehrere unabhängige, glaubhafte Bewertungen
   schildern dasselbe Muster — etwa eine Rechnung weit über dem am Telefon genannten Preis, Nötigung
   vor Ort, unnötigen Schlosstausch.
4. **Dokumentierte eigene Kenntnis des Betreibers.** Der Betreiber hat mit dem Betrieb selbst eine
   belegbare Erfahrung gemacht: Betrug, Erpressungsversuch, Sabotage eines Eintrags, nachweisliche
   Falschauskunft. „Belegbar" heißt: mit Datum, Vorgang und, wo möglich, Beleg festgehalten.

Ein einzelner anonymer Kommentar genügt nicht. Ein laufender Preisstreit ohne Muster genügt nicht.
Persönliche Abneigung oder Wettbewerb genügen nicht.

## Warum eigene Kenntnis zählt

Eigene, belegbare Kenntnis über einen Betrieb **wiegt schwerer als dessen Google-Bewertung.** Die
Festpreis-Garantie und die Google-Sterne messen beide nur, was öffentlich sichtbar ist; ein Betrieb,
der den Betreiber nachweislich betrogen oder einen Eintrag sabotiert hat, kann trotzdem eine gute
Bewertung tragen. Das Verzeichnis dient den Nutzern — es darf einen Betrieb, von dessen Fehlverhalten
der Betreiber sichere Kenntnis hat, nicht weiter empfehlen, nur weil die öffentliche Bewertung hoch
ist. Der Maßstab ersetzt keine der anderen Regeln; er ergänzt sie um das, was der Betreiber selbst
weiß.

## Wie der Ausschluss ausgeführt wird

- Der Betrieb kommt nach `output/<slug>/04-exclusions.csv` mit `action=drop`.
- In die Spalte `reason` kommt **ausschließlich das Kürzel `verhalten_betreiber`**, das auf diesen
  Maßstab verweist. **Keine Schilderung des Vorgangs** — nicht in der CSV, nicht in Berichten, nicht
  im Wiki. Der Grund bleibt damit ehrlich (er behauptet kein fremdes Gewerbe und keine fehlende
  Türöffnung) und zugleich frei von schriftlichen Vorwürfen gegen einen namentlich genannten Dritten.
- **Warum nur ein Kürzel:** `04-exclusions.csv` liegt im Git-Repository; was dort, in einem Bericht
  oder im Wiki steht, bleibt dauerhaft in der Versionsgeschichte. Die **Belege liegen beim Betreiber
  außerhalb des Repositorys**. Eine schriftliche Schilderung von Betrug, Nötigung oder Sabotage gegen
  einen mit Namen genannten Betrieb gehört nicht in eine versionierte Datei; das Kürzel trägt die
  Entscheidung, der Beleg bleibt beim Betreiber.
- Danach werden alle **Stadttexte** geprüft, in denen der Betrieb vorkommt, und die betroffenen
  Stellen neu geschrieben, ohne Lücke oder Bruch. Auch **Nachbarstädte** werden geprüft, weil ein
  Betrieb dort als Arbeitsgebiet genannt sein kann.
- Der Ausschluss ist eine Datenänderung wie jede andere: CSV ändern, neu bauen ([[konventionen]],
  „Neu bauen bei Änderung").

## Siehe auch
[[footprint-rules]] · [[directory-overview]] · [[siegel-programm]] · [[konventionen]]
