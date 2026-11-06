# notify-worker

Schlanker Benachrichtigungs-Worker: sendet jede Formular-Einsendung (Eintrag beanspruchen,
Garantie-Antrag) per Cloudflare Email Routing an den Betreiber. Kein Drittanbieter, kein
API-Schlüssel.

Die Pages-Function `../site/functions/api/claim.ts` schreibt die Einsendung in KV und ruft diesen
Worker über das Service-Binding `MAILER` auf (Pages selbst kann nicht mailen). Der Worker hat kein
öffentliches Ziel (`workers_dev: false`, keine Route) und ist nur über das Binding erreichbar.

## Ausliefern

```
npx wrangler deploy
```

## Voraussetzungen im Cloudflare-Konto des Verzeichnisses

1. Email Routing auf `die-besten-schluesseldienste.de` aktiv.
2. Die gewöhnliche Adresse des Betreibers als Destination verifiziert (Bestätigungsklick).
3. Service-Binding `MAILER` → dieser Worker (steht in `../site/wrangler.toml`, wird beim
   Pages-Deploy gesetzt).
4. Pages-Secret `NOTIFY_TO` (gewöhnliche Adresse) und Variable `NOTIFY_FROM`
   (`formular@die-besten-schluesseldienste.de`).

Details: `../05-build-report.md` und `berichte/2026-11-06-formular-benachrichtigung.md`.
