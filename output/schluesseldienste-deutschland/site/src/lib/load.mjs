// Verzeichnis-Blueprint, deutsche Fassung: die Datenschicht. Reines JS, damit astro.config.mjs und
// die Seiten dieselbe Datei nutzen. Liest src/data/site.json, listings.csv, attributes.json,
// city-copy.json.
// Die Regeln kommen aus wiki/konventionen.md (verbindlich), wiki/framework/site-architecture.md,
// page-types.md, listings-cleaning.md (dünn), monetization-slots.md (Sortierung), seo/launch-lean.md.
//
// Gliederung: drei Ebenen. Deutschland (site.country) -> Bundesland (aus der Spalte `state` der
// listings.csv, siehe loadRegions) -> Stadt. Standortseiten liegen unter /verzeichnis/,
// Betriebsseiten unter /firma/.
import fs from 'node:fs';
import path from 'node:path';

// Vom Projektstamm aus aufgelöst, nicht über import.meta.url: Astro bündelt diese Datei beim Bauen
// nach dist/chunks, der relative Pfad würde brechen. Mit DIRECTORY_DATA_DIR überschreibbar.
const DATA = process.env.DIRECTORY_DATA_DIR || path.join(process.cwd(), 'src', 'data');
const read = (f) => fs.readFileSync(path.join(DATA, f), 'utf8');

// Die 16 Bundesländer und ihre Kürzel (wiki/konventionen.md). Die Länder selbst werden NICHT in
// site.json aufgezählt, sondern aus der CSV abgeleitet; diese Tabelle liefert nur das Kürzel.
export const REGION_CODES = {
  'baden-wuerttemberg': 'BW', bayern: 'BY', berlin: 'BE', brandenburg: 'BB', bremen: 'HB',
  hamburg: 'HH', hessen: 'HE', 'mecklenburg-vorpommern': 'MV', niedersachsen: 'NI',
  'nordrhein-westfalen': 'NW', 'rheinland-pfalz': 'RP', saarland: 'SL', sachsen: 'SN',
  'sachsen-anhalt': 'ST', 'schleswig-holstein': 'SH', thueringen: 'TH',
};

// Angaben, ohne die die Seite nicht online gehen darf: Pflichtangaben nach § 5 DDG, der
// Formularempfaenger und die Zahlungslinks. Jeder Eintrag: Pfad in site.json -> Klartext.
// Ein Wert gilt als offen, wenn er leer ist oder mit OFFEN_, STRIPE_LINK_ oder FORMULAR_ID beginnt
// bzw. diese Zeichenfolge enthaelt.
const PFLICHT = [
  ['publisher.legalName', 'Firma im Impressum'],
  ['publisher.street', 'Strasse im Impressum'],
  ['publisher.postalCode', 'Postleitzahl im Impressum'],
  ['publisher.city', 'Ort im Impressum'],
  ['publisher.managingDirector', 'Geschaeftsfuehrer im Impressum'],
  ['publisher.registerCourt', 'Registergericht im Impressum'],
  ['publisher.register', 'Handelsregisternummer im Impressum'],
  // Nicht auf dieser Liste, und das mit Absicht:
  // publisher.vatId  - § 27a UStG verlangt die Angabe nur, soweit eine erteilt wurde. Leer lassen,
  //                    wenn keine vorliegt; die Seite druckt den Abschnitt dann nicht.
  // publisher.phone  - § 5 DDG verlangt eine Moeglichkeit zur unmittelbaren Kommunikation, nicht
  //                    zwingend ein Telefon. E-Mail-Adresse plus die Formulare erfuellen das.
  //                    Eine Nummer ist trotzdem ein Vertrauensgewinn, sobald es eine gibt.
  ['contact.email', 'E-Mail-Adresse'],
  ['contact.formEndpoint', 'Empfaenger der Formulare'],
];

const pick = (o, path) => path.split('.').reduce((x, k) => (x == null ? x : x[k]), o);
export const istOffen = (v) => {
  const s = String(v ?? '').trim();
  return !s || /OFFEN_|STRIPE_LINK_|FORMULAR_ID|REPLACE/.test(s);
};

/** Welche Pflichtangaben noch fehlen. Leeres Feld = startbereit. */
export function offenePflichtangaben(site) {
  return PFLICHT.filter(([p]) => istOffen(pick(site, p))).map(([p, label]) => ({ pfad: p, was: label }));
}

export function loadSite() {
  const site = JSON.parse(read('site.json'));
  // Deutschland als Ganzes statt eines Bundesstaats. `country.slug` nur, falls jemand ihn braucht.
  site.country = site.country || { name: 'Deutschland', code: 'DE' };
  site.country.slug = site.country.slug || slugify(site.country.name);
  // Beim Bauen laut sagen, was noch fehlt. Der Build bricht nicht ab, damit eine Vorschau moeglich
  // bleibt; die Impressumsseite zeigt denselben Hinweis sichtbar an, und check_live.py laesst die
  // Seite mit offenen Pflichtangaben nicht als startbereit durchgehen (wiki/seo/launch-lean.md).
  const offen = offenePflichtangaben(site);
  if (offen.length) {
    console.warn(`\n[Pflichtangaben] ${offen.length} Angabe(n) fehlen noch, die Seite ist nicht startbereit:`);
    for (const o of offen) console.warn(`  - ${o.was} (site.json: ${o.pfad})`);
    console.warn('');
  }
  return site;
}

// Minimaler CSV-Parser nach RFC 4180 (Anführungszeichen, verdoppelte Anführungszeichen, Zeilenumbrüche im Feld).
export function parseCsv(text) {
  const rows = []; let row = []; let field = ''; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; }
      else field += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field); field = ''; rows.push(row); row = [];
    } else field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const header = (rows.shift() || []).map((h) => h.replace(/^\ufeff/, '').trim());
  return rows.filter((r) => r.length > 1 || (r[0] || '').trim()).map((r) => {
    const o = {}; header.forEach((h, i) => (o[h] = (r[i] ?? '').trim())); return o;
  });
}

// Umlaute und ß werden umgeschrieben, BEVOR die Sonderzeichen fallen: sonst wird aus "Nürnberg"
// `n-rnberg` (wiki/konventionen.md). Gilt für Städte, Bundesländer, Firmennamen und Leistungen.
// Euro-Betrag aus der CSV: "89", "89 €", "89,00" -> 89; leer oder unlesbar -> null.
export function euro(v) {
  const t = String(v ?? '').trim().replace(/€/g, '').replace(/\s+/g, '').replace(',', '.');
  if (!t) return null;
  const n = Number(t);
  return Number.isFinite(n) && n >= 0 ? Math.round(n) : null;
}
// Anzeige eines Garantiepreises. 0 bei der Anfahrt = "im Preis enthalten".
export function fmtEuro(n, { anfahrt = false } = {}) {
  if (n == null) return '';
  if (anfahrt && n === 0) return 'im Preis enthalten';
  return `${new Intl.NumberFormat('de-DE').format(n)} €`;
}

export const slugify = (s) => String(s || '')
  .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue')
  .replace(/Ä/g, 'Ae').replace(/Ö/g, 'Oe').replace(/Ü/g, 'Ue')
  .replace(/ß/g, 'ss')
  .replace(/[áàâã]/g, 'a').replace(/[éèêë]/g, 'e').replace(/[íìî]/g, 'i')
  .replace(/[óòôõ]/g, 'o').replace(/[úùû]/g, 'u').replace(/ç/g, 'c').replace(/ñ/g, 'n')
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'x';

// Zeichen, die der selbst gehostete Schrift-Auszug (latin + latin-ext) nicht abdeckt, aus Freitext
// entfernen: Emoji, Dingbats und fremde Schriften aus Google-Maps-Beschreibungen erscheinen sonst
// im Browser als leeres Kästchen. Die Bereiche sind gleichlautend zu scripts/check-glyphs.mjs; der
// Build-Check scheitert, falls doch eines durchrutscht. Danach doppelte Leerzeichen zusammenziehen.
const GLYPH_OK = [
  [0x0000, 0x00ff], [0x0131, 0x0131], [0x0152, 0x0153], [0x02bb, 0x02bc], [0x02c6, 0x02c6],
  [0x02da, 0x02da], [0x02dc, 0x02dc], [0x0304, 0x0304], [0x0308, 0x0308], [0x0329, 0x0329],
  [0x2000, 0x206f], [0x20ac, 0x20ac], [0x2122, 0x2122], [0x2191, 0x2191], [0x2193, 0x2193],
  [0x2212, 0x2212], [0x2215, 0x2215], [0xfeff, 0xfeff], [0xfffd, 0xfffd],
  [0x0100, 0x02ba], [0x02bd, 0x02c5], [0x02c7, 0x02cc], [0x02ce, 0x02d7], [0x02dd, 0x02ff],
  [0x1d00, 0x1dbf], [0x1e00, 0x1e9f], [0x1ef2, 0x1eff], [0x2020, 0x2020], [0x20a0, 0x20c0],
  [0x2113, 0x2113], [0x2c60, 0x2c7f], [0xa720, 0xa7ff],
];
function sanitizeGlyphs(s) {
  if (!s) return s;
  let out = '';
  for (const ch of s) {
    const cp = ch.codePointAt(0);
    if (GLYPH_OK.some(([lo, hi]) => cp >= lo && cp <= hi)) out += ch;
  }
  return out.replace(/[^\S\n]{2,}/g, ' ').replace(/[^\S\n]+([.,;:!?])/g, '$1').replace(/[^\S\n]+\n/g, '\n').trim();
}

const truthy = (v) => /^(true|wahr|ja|yes|1|y|j)$/i.test(String(v || '').trim());
const num = (v) => { const n = parseFloat(String(v || '').replace(',', '.')); return Number.isFinite(n) ? n : 0; };
const int = (v) => Math.round(num(v));

// Zahlen und Daten deutsch: Dezimaltrennzeichen Komma, Tausendertrennzeichen Punkt, Datum TT.MM.JJJJ.
export const fmtInt = (n) => Number(n || 0).toLocaleString('de-DE');
export const fmtRating = (n) => Number(n || 0).toFixed(1).replace('.', ',');
export const fmtDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso || '')); return m ? `${m[3]}.${m[2]}.${m[1]}` : String(iso || ''); };
export const plural = (n, one, many) => (n === 1 ? one : many);

// ---------------------------------------------------------------------------
// Telefonnummern (wiki/konventionen.md)
//   Anzeige: "+49 621 1234567" (Ländervorwahl, Ortsvorwahl, Rest zusammen)
//   tel:-Link und schema.org: E.164, also "+496211234567"
//   Nummern mit führender 0: Null weg, +49 davor. Nicht erkennbare Nummern unverändert.
// ---------------------------------------------------------------------------
const AREA2 = new Set(['30', '40', '69', '89']);
const AREA3 = new Set([
  '201', '202', '203', '208', '209', '211', '212', '214', '221', '228', '231', '234', '241', '251',
  '261', '271', '281', '291', '331', '335', '340', '341', '345', '351', '355', '361', '365', '371',
  '375', '381', '385', '391', '395', '421', '431', '441', '451', '461', '471', '481', '491', '511',
  '521', '531', '541', '551', '561', '571', '581', '591', '611', '621', '631', '641', '651', '661',
  '671', '681', '711', '721', '731', '741', '751', '761', '771', '781', '791', '821', '831', '841',
  '851', '861', '871', '881', '911', '921', '931', '941', '951', '961', '971', '981', '991',
]);
// Länge der Vorwahl in der nationalen Nummer (ohne führende 0).
function areaLength(d) {
  if (/^1[5-7]/.test(d)) return 3;                // Mobil: 0151, 0160, 0176 ... -> 151, 160, 176
  if (/^(800|180|190|137|700)/.test(d)) return 3; // kostenfreie und Service-Rufnummern
  if (AREA2.has(d.slice(0, 2))) return 2;
  if (AREA3.has(d.slice(0, 3))) return 3;
  return 4;                                   // alle übrigen Ortsnetze: vier Stellen
}
// Die nationale Rufnummer ohne führende 0 und ohne +49, oder null wenn nicht erkennbar.
export function nationalDe(p) {
  const raw = String(p ?? '').trim();
  if (!raw) return null;
  let d = raw.replace(/[^\d+]/g, '');
  if (d.startsWith('+49')) d = d.slice(3);
  else if (d.startsWith('0049')) d = d.slice(4);
  else if (d.startsWith('+')) return null;    // andere Ländervorwahl: unverändert lassen
  // Führende Null weg, auch nach der Ländervorwahl: "+49 (0)911 …" ist dieselbe Nummer.
  d = d.replace(/\D/g, '').replace(/^0+/, '');
  if (d.length < 5 || d.length > 13) return null;
  return d;
}
export function formatPhone(p) {
  const d = nationalDe(p);
  if (!d) return String(p ?? '');
  const n = Math.min(areaLength(d), d.length - 2);
  return `+49 ${d.slice(0, n)} ${d.slice(n)}`;
}
// schema.org telephone in E.164.
export function e164(p) {
  const d = nationalDe(p);
  return d ? `+49${d}` : (p || undefined);
}
export function telHref(p) {
  const d = nationalDe(p);
  if (d) return `tel:+49${d}`;
  const r = String(p ?? '').replace(/[^\d+]/g, '');
  return r ? `tel:${r}` : '';
}
// Der schema.org-Typ jedes gelisteten Betriebs: niche.schemaType aus site.json (für Schlüsseldienste
// `Locksmith`), LocalBusiness wenn nicht gesetzt.
export function businessType(site) { return (site.niche && site.niche.schemaType) || 'LocalBusiness'; }

// ---------------------------------------------------------------------------
// Öffnungszeiten (wiki/konventionen.md)
//   Tage: Montag … Sonntag und Monday … Sunday, auch Mo/Mon.
//   Zeiten: 08:00–17:00, 8:00-17:00, 00:00–24:00; englisches 8AM-5PM wird weiter akzeptiert.
//   "Geschlossen"/"Closed" -> geschlossen; "Durchgehend geöffnet"/"24 Stunden"/"Open 24 hours"
//   -> 00:00–23:59.
// ---------------------------------------------------------------------------
export const DE_DAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'];
const EN_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const DAY_KEYS = {};
DE_DAYS.forEach((d, i) => { DAY_KEYS[d.toLowerCase()] = i; });
EN_DAYS.forEach((d, i) => { DAY_KEYS[d.toLowerCase()] = i; });
['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so'].forEach((d, i) => { DAY_KEYS[d] = i; });
['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].forEach((d, i) => { DAY_KEYS[d] = i; });
['montags', 'dienstags', 'mittwochs', 'donnerstags', 'freitags', 'samstags', 'sonntags'].forEach((d, i) => { DAY_KEYS[d] = i; });
const dayIndex = (k) => { const n = DAY_KEYS[String(k || '').trim().toLowerCase().replace(/\.$/, '')]; return n === undefined ? -1 : n; };

const RX_CLOSED = /^\s*(geschlossen|closed|zu)\s*$/i;
const RX_ALLDAY = /(durchgehend|rund um die uhr|24\s*stunden|24\s*std|open\s*24|24\s*hours|00:00\s*[-–—]\s*24:00|0:00\s*[-–—]\s*24:00)/i;

// "08:00–17:00" bleibt, "8AM-5PM" wird umgeschrieben, "Closed" wird "Geschlossen".
export function normalizeHours(v) {
  // DataForSEO liefert je Tag ein Array von Intervallen:
  // [{ open: { hour, minute }, close: { hour, minute } }, ...]. Ein leeres Array heißt geschlossen,
  // ein einzelnes 00:00–24:00 durchgehend geöffnet. Ohne diese Behandlung würde String(Array) zu
  // "[object Object]" (der Fehler, der auf jeder Eintragsseite sichtbar war).
  if (Array.isArray(v)) {
    const fmt = (t) => (t && typeof t.hour === 'number')
      ? `${String(t.hour).padStart(2, '0')}:${String(t.minute || 0).padStart(2, '0')}` : null;
    const parts = v.map((iv) => { const o = fmt(iv && iv.open), c = fmt(iv && iv.close); return (o && c) ? `${o}–${c}` : null; }).filter(Boolean);
    if (!parts.length) return 'Geschlossen';
    if (parts.length === 1 && /^00:00–(24:00|00:00)$/.test(parts[0])) return 'Durchgehend geöffnet';
    return parts.join(', ');
  }
  // normalizeHours wird nur je vorhandenem Tagesschlüssel aufgerufen (parseHours). Ein Tag, der im
  // working_hours-Objekt steht, aber null oder leer ist, bedeutet geschlossen (DataForSEO schreibt
  // einen Ruhetag als "sunday": null). Sonst bliebe die Zeile leer statt "Geschlossen".
  const s = String(v ?? '').trim();
  if (!s) return 'Geschlossen';
  if (RX_CLOSED.test(s)) return 'Geschlossen';
  if (RX_ALLDAY.test(s)) return 'Durchgehend geöffnet';
  const spec = hoursToSpec(s);
  return spec ? `${spec.opens}–${spec.closes}` : s;
}
// "08:00–17:00" -> { opens: "08:00", closes: "17:00" } für das Schema; null wenn nicht lesbar.
export function hoursToSpec(h) {
  const s = String(h ?? '').trim();
  if (!s || RX_CLOSED.test(s)) return null;
  if (RX_ALLDAY.test(s)) return { opens: '00:00', closes: '23:59' };
  // 24-Stunden-Schreibweise, deutsch und neutral: 8-17, 8:00-17:00, 08:00–17:00, 9 bis 18 Uhr
  let m = /^(\d{1,2})(?:[:.](\d{2}))?\s*(?:bis|[-–—])\s*(\d{1,2})(?:[:.](\d{2}))?(?:\s*uhr)?$/i.exec(s);
  if (m && !/\b(am|pm)\b/i.test(s)) {
    const to = (hh, mm) => {
      let x = parseInt(hh, 10); let n = mm || '00';
      if (x === 24) { x = 23; n = '59'; }
      if (x > 23 || parseInt(n, 10) > 59) return null;
      return `${String(x).padStart(2, '0')}:${n}`;
    };
    const o = to(m[1], m[2]); const c = to(m[3], m[4]);
    if (o && c) return { opens: o, closes: c };
  }
  // Englische Schreibweise mit AM/PM bleibt lesbar.
  m = /^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)\s*[-–—]\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$/i.exec(s);
  if (m) {
    const to24 = (hh, mm, ap) => { let x = parseInt(hh, 10) % 12; if (/pm/i.test(ap)) x += 12; return `${String(x).padStart(2, '0')}:${mm || '00'}`; };
    return { opens: to24(m[1], m[2], m[3]), closes: to24(m[4], m[5], m[6]) };
  }
  return null;
}
// working_hours kommt als JSON-artiger String: {"Montag": "08:00-17:00", ...}
export function parseHours(raw) {
  if (!raw) return [];
  let obj = null;
  try { obj = JSON.parse(raw); } catch { try { obj = JSON.parse(String(raw).replace(/'/g, '"')); } catch { return []; } }
  if (!obj || typeof obj !== 'object') return [];
  const out = [];
  for (const [k, v] of Object.entries(obj)) {
    const i = dayIndex(k);
    if (i < 0) continue;
    out.push({ index: i, day: DE_DAYS[i], schemaDay: EN_DAYS[i], hours: normalizeHours(v) });
  }
  return out.sort((a, b) => a.index - b.index);
}

function haversine(a, b) {
  const R = 6371, toRad = (x) => (x * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat), dLon = toRad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}

// ---------------------------------------------------------------------------
// Bundesländer: aus der Spalte `state` der listings.csv abgeleitet, nicht aus site.json.
// Je Land: Name, Slug, Kürzel, Anzahl Einträge, Anzahl Städte (eindeutige Stadtnamen in der CSV).
// ---------------------------------------------------------------------------
let regionCache = null;
export function loadRegions() {
  if (regionCache) return regionCache;
  const rows = parseCsv(read('listings.csv'));
  const map = new Map();
  for (const r of rows) {
    const name = (r.state || '').trim();
    if (!name) continue;
    const slug = slugify(name);
    if (!map.has(slug)) map.set(slug, { name, slug, code: REGION_CODES[slug] || (r.state_code || '').trim().toUpperCase() || slug.slice(0, 2).toUpperCase(), listings: 0, cityNames: new Set() });
    const reg = map.get(slug);
    reg.listings++;
    reg.cityNames.add(slugify(r.city_slug || r.city || ''));
  }
  regionCache = [...map.values()]
    .map((r) => ({ name: r.name, slug: r.slug, code: r.code, listings: r.listings, cities: r.cityNames.size, path: `/verzeichnis/${r.slug}/` }))
    .sort((a, b) => b.listings - a.listings || a.name.localeCompare(b.name, 'de'));
  return regionCache;
}

let cache = null;
export function loadDirectory() {
  if (cache) return cache;
  const site = loadSite();
  const attributes = JSON.parse(read('attributes.json'));
  const cityCopyRaw = JSON.parse(read('city-copy.json'));
  const cityCopy = Object.fromEntries(Object.entries(cityCopyRaw).filter(([k]) => !k.startsWith('_')));
  const rows = parseCsv(read('listings.csv'));
  const regionList = loadRegions();
  const regionBySlug = Object.fromEntries(regionList.map((r) => [r.slug, r]));

  // Zwei Städte gleichen Namens im selben Bundesland: Postleitzahl an den Stadt-Slug anhängen
  // (wiki/konventionen.md). Erkannt über die Lage, nicht über die Postleitzahl: eine große Stadt
  // deckt mehrere Leitregionen ab (Köln liegt in 50xxx und 51xxx), zwei gleichnamige Orte liegen
  // dagegen weit auseinander. Einfachverkettung bei CITY_SPLIT_KM; ein Haufen bleibt eine Stadt.
  const CITY_SPLIT_KM = 25;
  const nameGroups = new Map();   // regionSlug|cityBase -> Liste von Punkthaufen
  for (const r of rows) {
    const key = `${slugify(r.state || '')}|${slugify(r.city_slug || r.city || '')}`;
    if (!nameGroups.has(key)) nameGroups.set(key, []);
    nameGroups.get(key).push({ lat: num(r.latitude), lng: num(r.longitude), postal: String(r.postal_code || '').replace(/\D/g, '') });
  }
  const cityClusters = new Map();
  for (const [key, pts] of nameGroups) {
    const clusters = [];
    for (const p of pts) {
      const near = (q) => q.lat && q.lng && p.lat && p.lng && haversine(q, p) <= CITY_SPLIT_KM;
      let hit = (!p.lat || !p.lng) ? clusters[0] : clusters.find((c) => c.pts.some(near));
      if (hit) hit.pts.push(p);
      else clusters.push({ pts: [p], postal: p.postal });
    }
    cityClusters.set(key, clusters);
  }
  const citySlugFor = (regionSlug, cityBase, postal) => {
    const clusters = cityClusters.get(`${regionSlug}|${cityBase}`) || [];
    if (clusters.length < 2) return cityBase;
    const pc = String(postal || '').replace(/\D/g, '');
    const i = Math.max(0, clusters.findIndex((c) => c.pts.some((q) => q.postal === pc)));
    return `${cityBase}-${clusters[i].postal || pc || i + 1}`;
  };

  // Einträge
  const seen = new Set();
  const listings = rows.map((r) => {
    const city = r.city || 'Unbekannt';
    const regionName = (r.state || '').trim();
    const regionSlug = slugify(regionName);
    const region = regionBySlug[regionSlug] || { name: regionName, slug: regionSlug, code: (r.state_code || '').toUpperCase() };
    const citySlug = citySlugFor(regionSlug, slugify(r.city_slug || city), r.postal_code);
    let slug = r.slug ? slugify(r.slug) : slugify(`${r.name}-${city}`);
    if (seen.has(slug)) slug = `${slug}-${r.postal_code || seen.size}`;
    seen.add(slug);
    const attrs = attributes.map((a) => ({ key: a.key, label: a.label, value: normalizeAttr(r[a.key]) }));
    const featured = (r.featured || '').toLowerCase().trim(); // '', city, county, state
    const premium = truthy(r.premium);
    const claimed = truthy(r.claimed);
    const bestOfRank = int(r.best_of_rank) || 0;
    const reviews = int(r.reviews);
    const rating = num(r.rating);
    const description = sanitizeGlyphs(r.description_enriched || r.description || '');
    const thin = r.thin ? truthy(r.thin) : reviews < 5 || !description;
    const optimized = Boolean(featured) || (claimed && premium);
    const photos = optimized && r.photos ? r.photos.split(/[|,]/).map((s) => s.trim()).filter(Boolean) : [];
    const hours = parseHours(r.working_hours);
    // Festpreis-Garantie (wiki/konventionen.md): `geprueft` = Garantie aktiv, `geprueft_jahr` =
    // Jahr der Pruefung. Dienstleistung = Grundpreis der Tueroeffnung (werktags 7-20 Uhr), zwei
    // benannte Zuschlaege (abends/Wochenende/Feiertag; nachts 0-7 Uhr, nicht kumulativ) und die
    // Anfahrt; garantie_anfahrt = 0 heisst "im Preis enthalten". Ohne Grundpreis gilt die Garantie
    // als nicht aktiv, auch wenn geprueft=true steht: eine Garantie ohne Zahl ist keine.
    // Migrations-Riegel: Die Spalte `garantie_nacht` ist stillgelegt (frueher ein Absolutpreis).
    // Eine nicht-leere Zelle wuerde als Zuschlag fehlgedeutet -> Build mit klarer Meldung abbrechen.
    if ((r.garantie_nacht || '').trim() !== '') {
      throw new Error(`Stillgelegte Spalte garantie_nacht ist gefuellt (${r.garantie_nacht}) bei "${r.name || r.slug || '?'}". Auf garantie_zuschlag_abend und garantie_zuschlag_nacht umstellen (wiki/konventionen.md).`);
    }
    const garantieTag = euro(r.garantie_tag);
    const garantieZuschlagAbend = euro(r.garantie_zuschlag_abend);
    const garantieZuschlagNacht = euro(r.garantie_zuschlag_nacht);
    const garantieAnfahrt = euro(r.garantie_anfahrt);
    // Material bei abgeschlossener Tuer: Standardzylinder + Aufschlag je 5 mm Mehrlaenge
    // (wiki/konventionen.md). Die Preise oben sind die Dienstleistung, nicht der Gesamtbetrag.
    const garantieZylinder = euro(r.garantie_zylinder);
    const garantieZylinder5mm = euro(r.garantie_zylinder_5mm);
    const geprueft = truthy(r.geprueft) && garantieTag != null;
    const geprueftJahr = (r.geprueft_jahr || '').trim();
    const garantie = geprueft ? { jahr: geprueftJahr, tag: garantieTag, zuschlagAbend: garantieZuschlagAbend, zuschlagNacht: garantieZuschlagNacht, anfahrt: garantieAnfahrt, zylinder: garantieZylinder, zylinder5mm: garantieZylinder5mm } : null;
    return {
      name: sanitizeGlyphs(r.name), slug, city, citySlug, regionName: region.name, regionSlug: region.slug,
      regionCode: region.code, stateCode: region.code, postalCode: r.postal_code,
      county: r.county, address: sanitizeGlyphs(r.address), street: sanitizeGlyphs(r.street), phone: r.phone, website: r.website,
      lat: num(r.latitude), lng: num(r.longitude), population: int(r.population), geoPrecision: (r.geo_precision || '').trim(), rating, reviews, reviewsTags: r.reviews_tags,
      socials: (r.socials || '').split('|').map((s) => s.trim()).filter(Boolean).map((s) => { const i = s.indexOf('='); return i > 0 ? { network: s.slice(0, i), url: s.slice(i + 1) } : null; }).filter(Boolean),
      type: r.type, subtypes: r.subtypes, description, hours, verifiedOnGoogle: truthy(r.verified),
      mapLink: r.location_link || '', areaService: truthy(r.area_service), placeId: r.place_id,
      featured, featuredCities: (r.featured_cities || '').split(/[|,]/).map((s) => s.trim()).filter(Boolean),
      premium, claimed, bestOfRank, thin, optimized, photos, attrs, geprueft, geprueftJahr, garantie,
      path: `/firma/${region.slug}/${citySlug}/${slug}/`,
      cityPath: `/verzeichnis/${region.slug}/${citySlug}/`,
      score: rating * Math.log10(reviews + 1),
      // `owned` wird hier absichtlich nicht gelesen. Es darf die Darstellung nie verändern (footprint-rules.md).
    };
  });

  // Städte: Mindestzahl, darunter liegende Orte werden in die nächste Stadt MIT Seite gefaltet,
  // immer innerhalb desselben Bundeslandes, damit die URL-Ebene stimmt.
  const byCity = new Map();
  for (const l of listings) {
    const key = `${l.regionSlug}/${l.citySlug}`;
    if (!byCity.has(key)) byCity.set(key, { key, slug: l.citySlug, name: l.city, regionSlug: l.regionSlug, regionName: l.regionName, regionCode: l.regionCode, listings: [] });
    byCity.get(key).listings.push(l);
  }
  const all = [...byCity.values()].map((c) => ({ ...c, lat: avg(c.listings.map((l) => l.lat)), lng: avg(c.listings.map((l) => l.lng)) }));
  const floor = site.cityFloor || 3;
  const pages = all.filter((c) => c.listings.length >= floor);
  const folded = all.filter((c) => c.listings.length < floor);
  // foldMaxKm (site.json): ein Ort unter der Mindestzahl, der weiter als dieser Wert von jeder
  // Stadtseite seines Bundeslandes entfernt liegt, wird nicht gefaltet. Er bekommt eine eigene
  // Seite, indexiert und in der Sitemap, und steht auf der Bundesland-Seite unter "Kleinere Orte".
  const foldMaxKm = Number(site.foldMaxKm) || Infinity;
  // Mittelstadt-Regel (site.cityMinPopulation): eine Stadt ab dieser Einwohnerzahl bekommt eine
  // eigene Seite, auch mit nur einem Eintrag, statt auf eine kleinere Nachbarstadt gefaltet zu
  // werden. Gilt für alle gleich, auch owned. 0/leer schaltet die Regel ab.
  const minPop = Number(site.cityMinPopulation) || Infinity;
  const remote = [];
  for (const f of folded) {
    const pop = Math.max(0, ...f.listings.map((l) => Number(l.population) || 0));
    let best = null, bd = Infinity;
    for (const p of pages) { if (p.regionSlug !== f.regionSlug) continue; const d = haversine(f, p); if (d < bd) { bd = d; best = p; } }
    if (!best || bd > foldMaxKm || pop >= minPop) { remote.push({ ...f, underFloor: true }); continue; }
    for (const l of f.listings) {
      l.foldedFrom = l.city; l.citySlug = best.slug; l.city = best.name;
      l.path = `/firma/${best.regionSlug}/${best.slug}/${l.slug}/`;
      l.cityPath = `/verzeichnis/${best.regionSlug}/${best.slug}/`;
      best.listings.push(l);
    }
  }
  const sortAttr = site.sortAttribute || '';
  const cities = [...pages, ...remote].map((c) => {
    const sorted = sortListings(c.listings, c.slug, sortAttr);
    const copy = cityCopy[c.key] || cityCopy[c.slug] || null;
    const path = `/verzeichnis/${c.regionSlug}/${c.slug}/`;
    return {
      ...c, listings: sorted, path, copy, underFloor: Boolean(c.underFloor),
      count: sorted.length,
      featured: sorted.filter((l) => isFeaturedIn(l, c.slug)),
      bestOf: sorted.filter((l) => l.bestOfRank > 0),
      title: `${site.niche.title} in ${c.name}`,
      avgRating: avg(sorted.filter((l) => l.reviews > 0).map((l) => l.rating)),
      totalReviews: sorted.reduce((s, l) => s + l.reviews, 0),
      geprueftCount: sorted.filter((l) => l.geprueft).length,
      attrCounts: Object.fromEntries(attributes.map((a) => [a.key, sorted.filter((l) => attrValue(l, a.key) === 'true').length])),
    };
  }).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'de'));
  // indexCities: die Städte, die die Mindestzahl erreichen. Navigation, Startseiten-Raster und Zählungen nutzen diese.
  const indexCities = cities.filter((c) => !c.underFloor);
  for (const c of cities) {
    c.nearby = indexCities.filter((o) => o !== c).map((o) => ({ o, d: haversine(c, o) })).sort((x, y) => x.d - y.d).slice(0, 5).map((x) => x.o);
  }
  const cityBySlug = Object.fromEntries(cities.map((c) => [c.key, c]));

  // Bundesland-Ebene: eine Seite je Land, das mindestens eine Stadtseite hat.
  const regions = regionList.map((r) => {
    const own = cities.filter((c) => c.regionSlug === r.slug);
    const index = own.filter((c) => !c.underFloor);
    const small = own.filter((c) => c.underFloor);
    const ls = listings.filter((l) => l.regionSlug === r.slug);
    return {
      ...r, path: `/verzeichnis/${r.slug}/`, cities: index, smallTowns: small,
      cityCount: own.length, indexCityCount: index.length, listings: ls, count: ls.length,
      totalReviews: ls.reduce((s, l) => s + l.reviews, 0),
      geprueftCount: ls.filter((l) => l.geprueft).length,
      featured: ls.filter((l) => l.featured === 'state' || l.featured === 'county' || l.featured === 'city').slice(0, 3),
      title: `${site.niche.title} in ${r.name}`,
    };
  }).filter((r) => r.cities.length + r.smallTowns.length > 0)
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'de'));
  const regionByPathSlug = Object.fromEntries(regions.map((r) => [r.slug, r]));

  // Verwandte Einträge: jede Eintragsseite verlinkt die nächsten vier in der Reihenfolge ihrer Stadt,
  // am Ende umlaufend, damit jede Seite von vier anderen verlinkt ist und keine eine Sackgasse ist.
  for (const l of listings) l.related = [];
  for (const c of cities) {
    const n = c.listings.length;
    c.listings.forEach((l, i) => {
      l.related = n > 1 ? Array.from({ length: Math.min(4, n - 1) }, (_, k) => c.listings[(i + 1 + k) % n])
        : (c.nearby[0] ? c.nearby[0].listings.slice(0, 4) : []);
    });
  }
  // Leistungsseiten (/leistungen/<slug>/): eine je Merkmal mit einem `service`-Block in
  // attributes.json ({ title, slug, intro }), das mindestens die Mindestzahl an Einträgen bestätigt.
  const services = attributes.filter((a) => a.service && a.service.title).map((a) => {
    const confirmed = listings.filter((l) => attrValue(l, a.key) === 'true').sort((x, y) => y.score - x.score || x.name.localeCompare(y.name, 'de'));
    const slug = a.service.slug || slugify(a.key);
    return {
      key: a.key, label: a.label, slug, title: a.service.title, intro: a.service.intro || [], path: `/leistungen/${slug}/`,
      listings: confirmed, count: confirmed.length,
      cities: cities.map((c) => ({ city: c, count: c.attrCounts[a.key] || 0 })).filter((x) => x.count > 0).sort((x, y) => y.count - x.count || x.city.name.localeCompare(y.city.name, 'de')),
    };
  }).filter((s) => s.count >= floor);
  const missingCopy = cities.filter((c) => !c.copy).map((c) => c.key);   // jede Seite, die gebaut wird, kleine Orte eingeschlossen
  if (missingCopy.length && process.env.NODE_ENV !== 'test') {
    console.warn(`[verzeichnis] ${missingCopy.length} Stadtseite(n) ohne Eintrag in city-copy.json, sie nutzen den datengetriebenen Ersatztext: ${missingCopy.join(', ')}`);
  }

  // Das Startseiten-Band ist die nationale Fläche: nur die oberste Stufe (featured=state) speist es.
  // Stadt- und Umland-Plätze (featured=city/county) stehen im Band ihrer eigenen Seite, nicht national
  // – sonst bekäme ein Stadtplatz die Startseite gratis dazu, und ein eigener Betrieb stünde im
  // Startseiten-Band, für das es (noch) keinen veröffentlichten Preis gibt (wiki/framework/footprint-rules).
  const countryFeatured = listings.filter((l) => l.featured === 'state');
  let homeFeatured = [...countryFeatured].filter((l, i, arr) => arr.indexOf(l) === i).slice(0, 6);
  // Gestaltungsvorschau (site.featuredPreview): unverkaufte Plätze zeigen die besten echten Einträge,
  // mit `preview` markiert, damit die Karten data-preview tragen. Beim Start aus.
  if (site.featuredPreview) {
    const best = (list) => [...list].filter((l) => !l.featured && !l.thin && l.reviews >= 25 && l.rating >= 4.5 && (!sortAttr || attrValue(l, sortAttr) === 'true'))
      .sort((a, b) => b.score - a.score);
    const fill = (have, list) => [...have, ...best(list).filter((l) => !have.includes(l)).slice(0, Math.max(0, 2 - have.length))];
    homeFeatured = fill(homeFeatured, listings);
    homeFeatured.forEach((l) => { if (!l.featured) l.preview = true; });
    for (const c of cities) { c.featured = fill(c.featured, c.listings); c.featured.forEach((l) => { if (!l.featured) l.preview = true; }); }
  }

  // Launch lean: was aus der Sitemap bleibt und noindex bekommt.
  const noindexPaths = new Set();
  for (const l of listings) if (l.thin && !l.claimed && !l.optimized) noindexPaths.add(l.path);
  for (const l of listings) if (l.geprueft) noindexPaths.add(`/auszeichnung/${l.slug}/`);
  // Stadtseiten mit nur einem Eintrag (eigenständige Orte jenseits foldMaxKm und Mittelstädte mit
  // einem Eintrag) starten außerhalb der Sitemap und werden nach der 30-Tage-Prüfung in Tranchen
  // freigeschaltet (Betreiber-Regel, output/<slug>/06-launch.md). Sie bleiben gebaut und verlinkt.
  for (const c of cities) if (c.count <= 1) noindexPaths.add(c.path);
  for (const p of ['/eintrag-beanspruchen/', '/premium/', '/datenschutz/', '/agb/', '/impressum/',
    '/kontakt/', '/suche/', '/verzeichnis/', '/festpreis-garantie/antrag/', '/danke/', '/404/']) noindexPaths.add(p);

  const stats = {
    listings: listings.length, cities: indexCities.length, regions: regions.length,
    reviews: listings.reduce((s, l) => s + l.reviews, 0),
    geprueft: listings.filter((l) => l.geprueft).length,
    sortAttrTrue: sortAttr ? listings.filter((l) => attrValue(l, sortAttr) === 'true').length : 0,
    sortAttrLabel: sortAttr ? (attributes.find((a) => a.key === sortAttr) || {}).label || '' : '',
    // Verzeichnisweite Zahl der Einträge, die ein Merkmal bestätigen, für Texte, die sich auf die Daten stützen.
    attr: Object.fromEntries(attributes.map((a) => [a.key, listings.filter((l) => attrValue(l, a.key) === 'true').length])),
  };
  const buildDate = new Date().toISOString().slice(0, 10);
  cache = {
    site, attributes, listings, cities, indexCities, regions, regionByPathSlug, services, stats,
    cityBySlug, homeFeatured, noindexPaths, missingCopy,
    countryPath: '/verzeichnis/', buildDate, buildDateDe: fmtDate(buildDate),
  };
  return cache;
}

function avg(xs) { const v = xs.filter((x) => Number.isFinite(x) && x !== 0); return v.length ? v.reduce((a, b) => a + b, 0) / v.length : 0; }
function normalizeAttr(v) {
  const s = String(v || '').trim().toLowerCase();
  if (!s) return 'not enough info';
  if (/^(true|wahr|ja|yes|y|j|1)$/.test(s)) return 'true';
  if (/^(false|falsch|nein|no|n|0)$/.test(s)) return 'false';
  return 'not enough info';
}
export function attrValue(l, key) { return (l.attrs.find((a) => a.key === key) || {}).value || 'not enough info'; }
export function isFeaturedIn(l, citySlug) {
  if (l.featured === 'state') return true;
  if (l.featured === 'county') return l.featuredCities.includes(citySlug) || l.citySlug === citySlug;
  if (l.featured === 'city') return l.citySlug === citySlug;
  return false;
}
// Reihenfolge auf der Stadtseite: Premium-Plätze zuerst, dann bezahlte Top-Platzierungen, dann
// Einträge, bei denen site.sortAttribute wahr ist, dann alle übrigen. Innerhalb einer Gruppe:
// Bewertung x log(Anzahl Bewertungen).
export function sortListings(list, citySlug, sortAttr = '') {
  const rank = (l) => (isFeaturedIn(l, citySlug) ? 0 : l.bestOfRank ? 1 : sortAttr && attrValue(l, sortAttr) === 'true' ? 2 : 3);
  return [...list].sort((a, b) => rank(a) - rank(b) || (a.bestOfRank || 99) - (b.bestOfRank || 99) || b.score - a.score || a.name.localeCompare(b.name, 'de'));
}
// Platzhalter in den FAQ-Vorlagen aus attributes.json: {plural}, {singular}, {city}, {bundesland}, {land}.
export function fillFaq(template, site, cityName, regionName = '') {
  return String(template || '')
    .replace(/\{plural\}/g, site.niche.plural)
    .replace(/\{singular\}/g, site.niche.singular)
    .replace(/\{city\}/g, cityName || '')
    .replace(/\{(bundesland|state)\}/g, regionName || site.country.name)
    .replace(/\{(land|country)\}/g, site.country.name);
}
// Ersatz-FAQs aus den Merkmalszahlen, wenn city-copy.json keinen Eintrag hat.
export function attributeFaqs(city, site, attributes, max = 5) {
  const out = [];
  for (const a of attributes) {
    const n = city.attrCounts[a.key] || 0;
    if (n === 0) continue;
    const names = city.listings.filter((l) => attrValue(l, a.key) === 'true').slice(0, 3).map((l) => l.name);
    out.push({
      q: fillFaq(a.faq, site, city.name, city.regionName),
      a: `${n} der ${city.count} in ${city.name} gelisteten ${site.niche.plural} nennen „${a.label}“ als Leistung, darunter ${names.join(', ')}. Lassen Sie sich die Einzelheiten vor der Beauftragung bestätigen.`,
    });
    if (out.length >= max) break;
  }
  return out;
}
export function topAttrs(l, n = 3) { return l.attrs.filter((a) => a.value === 'true').slice(0, n); }

// Der Astro-Compiler nimmt keine <p>-Elemente in einem .map()-Ausdruck, deshalb werden Absatzlisten
// als ein HTML-String auf den Rahmen gesetzt: <div set:html={paragraphs(list)}></div>
export function escapeHtml(s) { return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
export function paragraphs(list) { return (list || []).filter(Boolean).map((t) => `<p>${escapeHtml(t)}</p>`).join('\n'); }

// Verlinkt die erste Nennung jedes gelisteten Betriebs in einem Textblock auf seine Eintragsseite.
// Namen werden als Ganzes gesucht, längste zuerst, damit "Merz Sicherheit GmbH" nicht von
// "Merz Sicherheit" gefangen wird. Gibt HTML zurück.
export function linkNames(text, listings) {
  const names = [...listings].filter((l) => l.name && l.name.length > 3).sort((a, b) => b.name.length - a.name.length);
  const parts = [{ t: text, html: false }];
  for (const l of names) {
    const rx = new RegExp(`(^|[^A-Za-zÄÖÜäöüß0-9&])(${l.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})(?![A-Za-zÄÖÜäöüß0-9])`);
    for (let i = 0; i < parts.length; i++) {
      const p = parts[i];
      if (p.html) continue;
      const m = rx.exec(p.t);
      if (!m) continue;
      const at = m.index + m[1].length;
      parts.splice(i, 1, { t: p.t.slice(0, at), html: false }, { t: `<a href="${l.path}">${escapeHtml(l.name)}</a>`, html: true }, { t: p.t.slice(at + l.name.length), html: false });
      break;
    }
  }
  return parts.map((p) => (p.html ? p.t : escapeHtml(p.t))).join('');
}
export function linkedParagraphs(list, listings) { return (list || []).filter(Boolean).map((t) => `<p>${linkNames(t, listings)}</p>`).join('\n'); }

// Zahlungslinks aus site.json sind beim Start Platzhalter (STRIPE_LINK_…). Nur echte Adressen
// werden verlinkt, sonst führt die Schaltfläche auf die Anfrage.
export function payLink(v) { return /^https?:\/\//i.test(String(v || '')) ? String(v) : ''; }
