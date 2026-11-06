# Live-Mailtest beider Formularpfade

**Datum:** 2026-11-06
**Auslöser:** Daniel hat Email Routing aktiviert, seine Adresse als Destination verifiziert und
`NOTIFY_TO` als Pages-Secret gesetzt. Jetzt der echte Test über das Live-Formular — mit Nachweis,
dass die Mail wirklich rausging, nicht nur, dass die Function den Worker aufrief.

## Vorbereitung

Ein Pages-Secret greift erst mit der nächsten Auslieferung, darum zuerst neu ausgeliefert:

- **Worker** `schluesseldienste-claim-notify` neu ausgeliefert (Version `e77e703d…`): eine Logzeile
  bei Erfolg (`notify: EMAIL.send ok`) bzw. Fehler ergänzt, **ohne die Empfängeradresse zu loggen**,
  damit `wrangler tail` den Ausgang des Versands zeigt.
- **Pages** neu ausgeliefert, damit `NOTIFY_TO` greift. Per API bestätigt: `MAILER` als
  Service-Binding an der Produktion, `NOTIFY_TO` als `secret_text` (Wert verborgen), `NOTIFY_FROM`
  als Klartext-Variable.

## Test und die vier Nachweise, je Pfad einzeln

`wrangler tail` lief auf dem Worker mit, währenddessen je eine echte POST an
`https://die-besten-schluesseldienste.de/api/claim`.

### 1) Beanspruchung (`formular=eintrag-beanspruchen`)

1. **303 statt 500:** `HTTP/2 303`.
2. **Weiterleitung:** `location: /eintrag-beanspruchen/?gesendet=1`.
3. **Eintrag in KV:** `beansprucht:2026-11-06T12-15-31:go1t` (Felder vollständig, Testmarker).
4. **Mail wirklich raus:** Tail-Ereignis `url=https://mailer.internal/send`, `outcome=ok`,
   `response_status=200`, keine Exception, Log `notify: EMAIL.send ok` → `EMAIL.send()` ist
   durchgelaufen, Cloudflare Email Routing hat die Nachricht zur Zustellung angenommen.

### 2) Garantie-Antrag (`formular=garantie-antrag`)

1. **303 statt 500:** `HTTP/2 303`.
2. **Weiterleitung:** `location: /festpreis-garantie/antrag/?gesendet=1`.
3. **Eintrag in KV:** `garantie:2026-11-06T12-15-31:tasj` (`art=garantie`, Felder, Testmarker).
4. **Mail wirklich raus:** zweites Tail-Ereignis, identisch: `outcome=ok`, `response_status=200`,
   keine Exception, `notify: EMAIL.send ok`.

Der Tail zeigte **genau zwei** Ereignisse, beide mit Status 200 und ohne Exception — einer je Pfad.
Damit sind beide Zweige derselben Function geprüft, nicht nur die Beanspruchung.

## Aufräumen

Beide Testeinträge aus KV gelöscht (`beansprucht:…go1t`, `garantie:…tasj`); Kontrolle: kein
Eintrag mit dem Testmarker `2026-11-06T12-15` mehr vorhanden.

## Stand

Die Benachrichtigung bei Formulareingang ist **live und beidseitig geprüft**. Bei jeder echten
Beanspruchung und jedem Garantie-Antrag geht innerhalb einer Minute eine Mail mit dem Inhalt an
Daniels gewöhnliche Adresse; die Einsendung liegt zusätzlich in KV. Scheitert der Versand, bleibt
die Einsendung in KV und das Formular zeigt trotzdem „gesendet".
