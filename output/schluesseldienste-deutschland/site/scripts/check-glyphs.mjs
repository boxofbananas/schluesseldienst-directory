// Build-Prüfung: scheitert, wenn eine gebaute Seite oder ein CSS ein Zeichen enthält, das der
// selbst gehostete Schrift-Auszug (@fontsource „latin") nicht abdeckt. Solche Zeichen (z. B. ★ ☆ ✓)
// fallen im Browser auf eine Systemschrift zurück und erscheinen dort, wo sie fehlt, als leeres
// Kästchen. Statt eines Schriftzeichens gehört ein Inline-SVG in die Seite (siehe components/Star.astro,
// Check.astro). Auch CSS-content-Angaben werden geprüft.
//
// Die erlaubten Bereiche sind die unicode-range der importierten Auszüge „latin" und „latin-ext"
// von Roboto / Roboto Slab (node_modules/@fontsource/*/400.css bzw. 800.css). Wird ein anderer
// Auszug importiert, hier und in src/lib/load.mjs (sanitizeGlyphs) gleichlautend anpassen.
import { readFileSync } from 'node:fs';
import { readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';

const DIST = join(process.cwd(), 'dist');

// Erlaubte Codepunkte: [von, bis] (einschließlich). Steuerzeichen (\t \n \r) liegen in 0x00-0xFF.
// latin + latin-ext zusammen; Überschneidungen sind harmlos.
const RANGES = [
  // latin
  [0x0000, 0x00ff], [0x0131, 0x0131], [0x0152, 0x0153], [0x02bb, 0x02bc],
  [0x02c6, 0x02c6], [0x02da, 0x02da], [0x02dc, 0x02dc], [0x0304, 0x0304],
  [0x0308, 0x0308], [0x0329, 0x0329], [0x2000, 0x206f], [0x20ac, 0x20ac],
  [0x2122, 0x2122], [0x2191, 0x2191], [0x2193, 0x2193], [0x2212, 0x2212],
  [0x2215, 0x2215], [0xfeff, 0xfeff], [0xfffd, 0xfffd],
  // latin-ext
  [0x0100, 0x02ba], [0x02bd, 0x02c5], [0x02c7, 0x02cc], [0x02ce, 0x02d7],
  [0x02dd, 0x02ff], [0x1d00, 0x1dbf], [0x1e00, 0x1e9f], [0x1ef2, 0x1eff],
  [0x2020, 0x2020], [0x20a0, 0x20c0], [0x2113, 0x2113], [0x2c60, 0x2c7f],
  [0xa720, 0xa7ff],
];
const allowed = (cp) => RANGES.some(([lo, hi]) => cp >= lo && cp <= hi);

async function* walk(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.isFile() && /\.(html|css)$/.test(e.name)) yield p;
  }
}

const hits = [];
for await (const file of walk(DIST)) {
  const text = readFileSync(file, 'utf8');
  let line = 1, col = 0;
  for (const ch of text) {
    const cp = ch.codePointAt(0);
    if (ch === '\n') { line++; col = 0; continue; }
    col++;
    if (!allowed(cp)) {
      hits.push({ file: relative(process.cwd(), file), line, col, cp, ch });
    }
  }
}

if (hits.length) {
  console.error(`\nSchriftprüfung FEHLGESCHLAGEN: ${hits.length} Zeichen außerhalb des Latin-Auszugs.`);
  console.error('Solche Zeichen erscheinen als leeres Kästchen. Ersetze sie durch ein Inline-SVG.\n');
  const seen = new Map();
  for (const h of hits) {
    const key = h.cp;
    if (!seen.has(key)) seen.set(key, []);
    seen.get(key).push(h);
  }
  for (const [cp, list] of seen) {
    const u = 'U+' + cp.toString(16).toUpperCase().padStart(4, '0');
    console.error(`  ${list[0].ch}  ${u}  (${list.length}x), z. B. ${list[0].file}:${list[0].line}:${list[0].col}`);
  }
  console.error('');
  process.exit(1);
}
console.log('Schriftprüfung bestanden: keine Zeichen außerhalb des Latin-Auszugs.');
