// Helfer für den Versand-Export (scripts/kontakt.py exportieren): schreibt je Eintrag genau die
// Werte, die die gebaute Seite zeigt — Platz und Anzahl auf der Stadtseite, die vollständige
// Adresse der Eintragsseite, Bewertung/Bewertungszahl/Telefon im Format der Website. Weil es
// dieselbe Datenschicht (src/lib/load.mjs) nutzt wie der Build, stimmen die Werte mit dist/
// überein; scripts/kontakt.py prüft das zusätzlich an Stichproben gegen dist/.
//
// Die Stadt ist die Stadt der SEITE: ein Eintrag, der in die Nachbarstadt mit eigener Seite
// gefaltet wird (load.mjs), trägt deren Stadt und deren Platz/Anzahl — genau wie im Verzeichnis.
//
// Je Stadt zwei Merkmale für den Städte-Filter (nur Städte ohne Garantie und ohne bezahlten Platz
// dürfen die Pilot-Mail „noch kein Betrieb hat die Festpreis-Garantie" tragen):
//   cityGeprueft  mindestens ein Betrieb der Stadt hat die Festpreis-Garantie
//   cityPaid      mindestens ein Betrieb der Stadt hat einen bezahlten Platz (premium/featured/best_of)
//
// Aufruf: node dump-versand.mjs <out.json>
import fs from 'node:fs';
import { loadDirectory, fmtInt, fmtRating, formatPhone } from './src/lib/load.mjs';

const args = process.argv.slice(2);
if (args.length !== 1) {
  console.error('Aufruf: node dump-versand.mjs <out.json>');
  process.exit(2);
}
const outPath = args[0];
process.env.NODE_ENV = 'test';
const dir = loadDirectory();
const domain = dir.site.domain || '';

const out = [];
for (const c of dir.cities) {
  const cityPaid = c.listings.some((l) => l.premium || Boolean(l.featured) || l.bestOfRank > 0);
  const cityGeprueft = (c.geprueftCount || 0) > 0;
  c.listings.forEach((l, i) => {
    out.push({
      slug: l.slug,
      name: l.name,
      regionName: l.regionName,
      regionSlug: l.regionSlug,
      city: l.city,                 // Stadt der Seite (nach Faltung)
      citySlug: l.citySlug,
      foldedFrom: l.foldedFrom || '',
      eintragUrl: `https://${domain}${l.path}`,
      cityUrl: `https://${domain}${l.cityPath}`,
      platz: i + 1,                 // Rang in der geltenden Sortierung der Stadtseite
      anzahl: c.count,              // Zahl der Einträge auf der Stadtseite
      bewertung: l.reviews > 0 ? fmtRating(l.rating) : '',
      bewertungen: l.reviews > 0 ? fmtInt(l.reviews) : '',
      hatBewertung: l.reviews > 0,
      ratingRaw: l.rating,
      reviewsRaw: l.reviews,
      telefon: formatPhone(l.phone),
      cityGeprueft,
      cityPaid,
      cityEligible: !cityGeprueft && !cityPaid,
    });
  });
}
fs.writeFileSync(outPath, JSON.stringify(out));
const eligible = out.filter((r) => r.cityEligible).length;
console.log(`Einträge: ${out.length}, Städte: ${dir.cities.length}, in Städten ohne Garantie/bezahlten Platz: ${eligible}`);
