// Helfer für Gate 5: schreibt die Städtestruktur genau so, wie die Website sie baut (Faltungen
// eingeschlossen), damit die Stadttexte zu derselben Zuordnung geschrieben werden, die die Seiten
// zeigen. Mit drei Ebenen trägt jede Stadt ihr Bundesland.
//
// Aufruf: node dump-cities.mjs [plz-kreis.json] <out.json>
//   plz-kreis.json (optional): ein JSON-Objekt, das fünfstellige Postleitzahlen auf Kreisnamen
//   abbildet, { "68159": "Mannheim", ... }. Ohne die Datei wird die Spalte `county` der CSV genutzt,
//   die bei einem DataForSEO-Abzug leer bleibt.
import fs from 'node:fs';
import { loadDirectory, attrValue } from './src/lib/load.mjs';
const args = process.argv.slice(2);
if (args.length < 1 || args.length > 2) {
  console.error('Aufruf: node dump-cities.mjs [plz-kreis.json] <out.json>');
  process.exit(2);
}
const outPath = args[args.length - 1];
const zipCounty = args.length === 2 ? JSON.parse(fs.readFileSync(args[0], 'utf8')) : null;
if (!zipCounty) console.log('Hinweis: keine PLZ-Kreis-Datei angegeben; die Kreise kommen aus der Spalte county der CSV (bei einem DataForSEO-Abzug leer)');
const countyOf = (l) => (zipCounty && zipCounty[(l.postalCode || '').slice(0, 5)]) || l.county || '';
process.env.NODE_ENV = 'test';
const dir = loadDirectory();
const out = dir.cities.map((c) => ({
  key: c.key, slug: c.slug, name: c.name, region: c.regionName, regionSlug: c.regionSlug,
  count: c.count, underFloor: c.underFloor, path: c.path,
  avgRating: Number(c.avgRating.toFixed(2)), totalReviews: c.totalReviews, geprueft: c.geprueftCount,
  attrCounts: c.attrCounts,
  nearby: c.nearby.map((n) => ({ name: n.name, region: n.regionName, count: n.count })),
  listings: c.listings.map((l, i) => ({
    position: i + 1, name: l.name, slug: l.slug, rating: l.rating, reviews: l.reviews, thin: l.thin,
    basedIn: l.foldedFrom || '', county: countyOf(l), geprueft: l.geprueft, geprueftJahr: l.geprueftJahr,
    serviceArea: l.areaService, hasWebsite: Boolean(l.website), hasHours: l.hours.length > 0,
    yes: dir.attributes.filter((a) => attrValue(l, a.key) === 'true').map((a) => a.key),
    no: dir.attributes.filter((a) => attrValue(l, a.key) === 'false').map((a) => a.key),
    description: l.description,
  })),
}));
fs.writeFileSync(outPath, JSON.stringify(out));
const withCounty = out.reduce((s, c) => s + c.listings.filter((l) => l.county).length, 0);
console.log(`Bundesländer: ${dir.regions.length}, Städte: ${out.length}, davon mit Seite im Verzeichnis: ${out.filter((c) => !c.underFloor).length}, Einträge: ${out.reduce((s, c) => s + c.count, 0)}, mit Kreis: ${withCounty}`);
