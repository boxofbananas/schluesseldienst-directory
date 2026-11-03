#!/bin/sh
# Diese Datei auf einem Mac doppelklicken, um die gebaute Website im Browser anzusehen.
# Sie liefert den Ordner dist genau so aus, wie er veröffentlicht wird. Fenster schließen beendet sie.
cd "$(dirname "$0")" || exit 1
if ! command -v npm >/dev/null 2>&1; then
  echo "Node.js ist nicht installiert. Holen Sie es bei nodejs.org und öffnen Sie diese Datei erneut."
  printf "Zum Schließen die Eingabetaste drücken. "; read _; exit 1
fi
[ -d node_modules ] || npm install --no-audit --no-fund || exit 1
[ -f dist/index.html ] || npm run build || exit 1
echo "Die Website wird ausgeliefert. Der Browser öffnet sich gleich. Dieses Fenster schließen beendet sie."
if [ -n "$NO_OPEN" ]; then exec npx astro preview "$@"; fi
exec npx astro preview --open "$@"
