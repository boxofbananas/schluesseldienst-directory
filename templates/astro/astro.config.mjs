import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import { loadSite, loadDirectory } from './src/lib/load.mjs';

// Launch lean (wiki/seo/launch-lean.md): dünne Eintragsseiten, die Siegel-Nachweise und die Seiten
// zu Eintrag, Premium und Recht werden gebaut, bleiben aber aus der Sitemap. Die Seiten selbst
// setzen <meta name="robots" content="noindex"> aus denselben Daten.
const site = loadSite();
const dir = loadDirectory();
const noindex = dir.noindexPaths; // Menge absoluter Pfade wie "/firma/bayern/nuernberg/..."
// Das Ratgeber-Verzeichnis bleibt aus der Sitemap, solange es keine echte Ratgeberseite gibt.
const resources = fs.existsSync('./src/pages/ratgeber') ? fs.readdirSync('./src/pages/ratgeber').filter((f) => f.endsWith('.md') && !f.startsWith('_')) : [];
if (resources.length === 0) noindex.add('/ratgeber/');
// Cloudflare Pages liest dist/_redirects. /firma/ allein geht auf die Blätterseite, eine Adresse
// /firma/<bundesland>/ auf die Bundesland-Seite und /firma/<bundesland>/<stadt>/ (ohne Betrieb) auf
// die Stadtseite. /verzeichnis/ ist eine echte Seite.
const redirects = [
  '/firma /verzeichnis/ 301',
  '/firma/ /verzeichnis/ 301',
  '/firma/:bundesland/ /verzeichnis/:bundesland/ 301',
  '/firma/:bundesland/:stadt/ /verzeichnis/:bundesland/:stadt/ 301',
  // Die alten englischen Adressen der Vorlage, falls die Website schon einmal unter ihnen lief.
  '/directory/* /verzeichnis/:splat 301',
  '/company/* /firma/:splat 301',
  '/services/* /leistungen/:splat 301',
  '/badge/* /auszeichnung/:splat 301',
  '/claim/ /eintrag-beanspruchen/ 301',
  '/featured/ /premium/ 301',
  '/about/ /ueber-uns/ 301',
  '/contact/ /kontakt/ 301',
  '/privacy/ /datenschutz/ 301',
  '/terms/ /agb/ 301',
  '/search/ /suche/ 301',
  '/resources/* /ratgeber/:splat 301',
];
fs.writeFileSync('./public/_redirects', redirects.join('\n') + '\n');

export default defineConfig({
  site: `https://${site.domain}`,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [
    sitemap({
      filter: (page) => {
        const path = new URL(page).pathname;
        return !noindex.has(path);
      },
    }),
  ],
});
