Hier gehört die Rohdatei mit den Einträgen hin, und nichts anderes.

**Dateiname:** `listings-raw.csv`

**Zwei Wege, dieselben Spalten** (`wiki/framework/outscraper-columns.md`):

1. **DataForSEO.** Claude ruft die Kategorie `locksmith` für Deutschland ab und legt die Datei
   hier ab, zusammen mit `listings-raw-report.md`. Die Kosten werden vorher genannt; abgerufen
   wird erst nach Ihrer Freigabe (Gate 1, Frage 3).
2. **Outscraper-Export.** Sie scrapen die Kategorie selbst und legen den Export hier als
   `listings-raw.csv` ab. Die Standardspalten genügen; die Spalten der
   Anreicherungs-Erweiterung sind willkommen, aber nicht nötig.

Dann in Claude Code sagen: `Gate 2 starten.`

**Nie in diesen Ordner:** Zugangsdaten, API-Schlüssel, Passwörter. Die DataForSEO-Anmeldung
wird einmalig im eigenen Terminal gespeichert und liegt in den Einstellungen von Claude Code,
nicht in diesem Ordner (`wiki/framework/gate-1-intake.md`).

Umlaute: Die Datei wird als UTF-8 erwartet. Kommt der Export als Windows-1252, zeigen
„Schlüsseldienst" und „Nürnberg" kaputte Zeichen, und die Slugs werden falsch. Vor Gate 2
nach UTF-8 umwandeln.
