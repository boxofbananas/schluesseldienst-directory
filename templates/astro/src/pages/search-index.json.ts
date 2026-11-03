import type { APIRoute } from 'astro';
import { loadDirectory, attrValue } from '../lib/load.mjs';

// Der Suchindex für public/search.js: jeder Eintrag und jede Stadtseite, nur kleine Felder.
// Einmal je Bau erzeugt, vom Browser geholt, sobald ein Besucher das erste Mal ein Suchfeld berührt.
export const GET: APIRoute = () => {
  const dir = loadDirectory();
  const cities = dir.cities.map((c) => ({ n: c.name, p: c.path, c: c.count, b: c.regionName, lat: Number(c.lat.toFixed(4)), lng: Number(c.lng.toFixed(4)) }));
  const listings = dir.listings.map((l) => ({
    n: l.name, p: l.path, c: l.city, t: l.foldedFrom && l.foldedFrom !== l.city ? l.foldedFrom : '',
    r: l.rating, v: l.reviews, g: l.geprueft ? 1 : 0,
    a: dir.attributes.filter((a) => attrValue(l, a.key) === 'true').map((a) => a.label),
  }));
  return new Response(JSON.stringify({ cities, listings }), { headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } });
};
