# Stadttext-Nachbesserung: Datenzahlen entfernen (ein Stapel)

Arbeiten Sie im Wurzelordner des Baukastens. `NN` ist Ihre Stapelnummer. Die Antwortdatei
`output/schluesseldienste-deutschland/05-cache/city-copy/batch-NN.json` ist bereits geschrieben und fast fertig. Eine neue
Regel verbietet **aus den Daten stammende Zahlen im Fließtext**: Bewertungsschnitte (`4,9`), Zahl der
Bewertungen (`aus 485`, `43 Kunden`), Eintrags- oder Betriebszahlen je Stadt (`3 Schlüsseldienste`),
Entfernungen in Kilometern. Diese Zahlen stehen auf der Eintragskarte und ändern sich bei jedem
Datenlauf; im Text widersprechen sie ihr.

1. Lassen Sie zuerst die Prüfliste laufen: `sh "output/schluesseldienste-deutschland/05-cache/check-batch.sh" NN`. Jede Zeile
   `Datenzahl im Fließtext … "<Satz>"` nennt einen Satz, der eine solche Zahl enthält.
2. Öffnen Sie `output/schluesseldienste-deutschland/05-cache/city-copy/batch-NN.json` und schreiben Sie **nur diese Sätze**
   um: die Aussage behalten, die Ziffer weglassen, qualitativ formulieren. Beispiele: „Die größte
   Bewertungsbasis hat Schlüsseldienst X" statt „… mit 4,9 aus 485"; „ein durchweg stark bewerteter
   Betrieb" statt „4,8 aus 120"; „wenige Stimmen, deshalb wenig aussagekräftig" statt „5,0 aus 3".
   Erlaubt bleiben vom Betrieb selbst genannte Jahre und Normen (seit 1991, DIN EN 1627, RC 2) und
   Hausnummern — die nicht anfassen.
3. **Lesen Sie das Paket nicht neu und erzeugen Sie den Text nicht neu.** Ändern Sie nur die
   gemeldeten Sätze; alle anderen bleiben Wort für Wort stehen. Fügen Sie keine neue Zahl ein und
   erfinden Sie keine Rangaussage, die die Daten nicht hergeben.
4. Lassen Sie die Prüfliste erneut laufen, bis die erste Zeile `durchgefallen: 0` sagt. Beheben Sie
   dabei auch eine etwaige neue „fast gleiche Sätze"-Zeile, indem Sie Ihren umgeschriebenen Satz
   eigenständiger formulieren.
5. Antworten Sie knapp: wie viele Sätze Sie in wie vielen Städten geändert haben.

Alles auf Deutsch, Sie-Anrede, über Betriebe in der dritten Person. Legen Sie nur diese eine
Antwortdatei an oder bearbeiten sie.
