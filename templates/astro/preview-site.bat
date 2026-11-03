@echo off
rem Diese Datei unter Windows doppelklicken, um die gebaute Website im Browser anzusehen.
rem Sie liefert den Ordner dist genau so aus, wie er veroeffentlicht wird. Fenster schliessen beendet sie.
cd /d "%~dp0"
where npm >nul 2>nul
if errorlevel 1 (
  echo Node.js ist nicht installiert. Holen Sie es bei nodejs.org und oeffnen Sie diese Datei erneut.
  pause
  exit /b 1
)
if not exist node_modules call npm install --no-audit --no-fund
if not exist dist\index.html call npm run build
echo Die Website wird ausgeliefert. Der Browser oeffnet sich gleich. Dieses Fenster schliessen beendet sie.
call npx astro preview --open
pause
