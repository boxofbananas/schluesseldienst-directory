// Garantie-Nachweis je Betrieb mit Festpreis-Garantie (wiki/konventionen.md). Der Betrieb bindet
// das Bild ein, es verweist auf seinen Eintrag zurueck. Nur fuer Betriebe mit aktiver Garantie.
import type { APIRoute } from 'astro';
import { loadDirectory, fmtEuro } from '../../lib/load.mjs';
export function getStaticPaths() {
  const { listings } = loadDirectory();
  return listings.filter((l) => l.geprueft).map((l) => ({ params: { slug: l.slug } }));
}
export const GET: APIRoute = ({ params }) => {
  const { site, listings, buildDate } = loadDirectory();
  const l = listings.find((x) => x.slug === params.slug)!;
  const d = site.design;
  const jahr = (l.geprueftJahr || '').trim() || buildDate.slice(0, 4);
  const line1 = `Festpreis-Garantie ${jahr}`;
  const line2 = `Türöffnung ab ${fmtEuro(l.garantie.tag)} · ${site.brand}`;
  // Auch die Anführungszeichen müssen weg: der Schriftname steht in einem Attribut.
  const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="260" height="64" viewBox="0 0 260 64" role="img" aria-label="${esc(line1)} – ${esc(line2)}">
  <rect width="260" height="64" rx="8" fill="${d.accent}"/>
  <text x="14" y="28" font-family="${esc(d.bodyFont)}" font-size="13" font-weight="700" fill="${d.accentText}">${esc(line1)}</text>
  <text x="14" y="48" font-family="${esc(d.bodyFont)}" font-size="12" fill="${d.accentText}">${esc(line2)}</text>
</svg>`;
  return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml' } });
};
