// Annahme der beiden Formulare (Eintrag beanspruchen, Garantie-Antrag) ohne Formulardienst.
// Spezifikation: berichte/2026-11-04-formularannahme-spec.md.
// Die Function bleibt bewusst „dumm": annehmen, in KV schreiben, dem Betreiber mailen, Seite zeigen.
// Keine automatische Prüfung, keine Erteilung, keine Bestätigungsmail an den Absender.
//
// Bindungen, die Daniels Cloudflare-Konto bereitstellt (siehe 05-build-report.md):
//   - KV-Namespace  EINSENDUNGEN
//   - Service-Binding  MAILER  auf den Benachrichtigungs-Worker (notify-worker/), der per
//     Cloudflare Email Routing sendet. Pages Functions unterstützen das send_email-Binding NICHT
//     (in diesem Projekt bestätigt), können also nicht selbst mailen; der Worker schließt die
//     Lücke. Diese Function ruft ihn nur auf.
//   - Variablen NOTIFY_FROM (Absender, Verzeichnis-Domain) und NOTIFY_TO (Empfänger, Daniels
//     gewöhnliche Adresse; als Pages-Variable gesetzt, nie im Repo).

interface Env {
  EINSENDUNGEN: KVNamespace;
  MAILER?: Fetcher;        // Service-Binding auf den Benachrichtigungs-Worker
  NOTIFY_FROM?: string;    // Absender, Verzeichnis-Domain
  NOTIFY_TO?: string;      // Empfänger, Daniels gewöhnliche Adresse (nicht im Repo)
}

// Nur bekannte Felder landen in KV und Mail. Alles andere wird verworfen (keine Mülldeponie).
const FELDER: Record<string, string[]> = {
  "garantie": [
    "formular", "eintrag", "firma", "strasse", "plz", "ort", "website", "impressum_url",
    "telefon", "google_profil", "ansprechperson", "rolle", "email", "garantie_tag",
    "garantie_zuschlag_abend", "garantie_zuschlag_nacht", "garantie_anfahrt", "zuschlaege_sonstige", "versprechen_rechnungspreis",
    "versprechen_zuschlaege", "versprechen_rechnung", "versprechen_zerstoerungsfrei",
    "unterschrift", "gewerbeanmeldung", "handelsregister", "anrufannahme", "anmerkungen",
  ],
  "beansprucht": [
    "listing_slug", "tier", "business", "name", "email", "phone", "changes",
    "featured_interest", "garantie_interesse",
  ],
};

const MAX_FELD = 2048;   // je Feld
const MAX_GESAMT = 8192; // je Einsendung
const RL_FENSTER = 3600; // Sekunden
const RL_MAX = 6;        // Einsendungen je IP und Stunde
const TTL = 90 * 24 * 3600; // 90 Tage: abgelehnte/unbeantwortete Einsendungen laufen von selbst ab

function zeitstempel(now: number): string {
  // ISO mit Bindestrichen statt Doppelpunkten, im KV-Browser lesbar: 2026-11-04T13-55-07
  return new Date(now).toISOString().slice(0, 19).replace(/:/g, "-");
}
function zufall(): string {
  const a = "abcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  const r = crypto.getRandomValues(new Uint8Array(4));
  for (const b of r) s += a[b % a.length];
  return s;
}
function seite(pfad: string): Response {
  // Erfolg wird als Seitenanzeige gelöst: zurück zum Formular mit ?gesendet=1 (das Skript dort
  // blendet die Dankesmeldung ein). Keine Bestätigungsmail an den Absender.
  // Relativer Location-Header statt Response.redirect(): Letzteres verlangt eine absolute URL und
  // wirft sonst "Unable to parse URL". Der Browser löst den relativen Pfad gegen die Anfrage auf.
  return new Response(null, { status: 303, headers: { Location: pfad + "?gesendet=1" } });
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env, waitUntil }) => {
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  const referer = request.headers.get("Referer") || "";

  let form: FormData;
  try { form = await request.formData(); } catch { return new Response("Ungültige Anfrage.", { status: 400 }); }

  // Honeypot: ausgefülltes _gotcha ist ein Bot. Wir tun so, als sei alles gut, speichern aber nichts.
  if ((form.get("_gotcha") || "").toString().trim() !== "") {
    return seite(referer.includes("festpreis-garantie") ? "/festpreis-garantie/antrag/" : "/eintrag-beanspruchen/");
  }

  // Ratelimit je IP über KV-Zähler mit kurzer TTL.
  try {
    const key = "rl:" + ip;
    const n = parseInt((await env.EINSENDUNGEN.get(key)) || "0", 10) + 1;
    if (n > RL_MAX) return new Response("Zu viele Einsendungen. Bitte später erneut.", { status: 429 });
    await env.EINSENDUNGEN.put(key, String(n), { expirationTtl: RL_FENSTER });
  } catch { /* Ratelimit darf die Annahme nicht blockieren */ }

  const art = (form.get("formular") || "").toString() === "garantie-antrag" ? "garantie" : "beansprucht";
  const erlaubt = FELDER[art];

  const daten: Record<string, string> = {};
  let gesamt = 0;
  for (const name of erlaubt) {
    const v = form.get(name);
    if (v == null) continue;
    let s = v.toString().slice(0, MAX_FELD);
    gesamt += s.length;
    if (gesamt > MAX_GESAMT) { s = s.slice(0, Math.max(0, s.length - (gesamt - MAX_GESAMT))); gesamt = MAX_GESAMT; }
    if (s.trim() !== "") daten[name] = s;
    if (gesamt >= MAX_GESAMT) break;
  }

  const now = Date.now();
  const key = `${art}:${zeitstempel(now)}:${zufall()}`;
  const satz = { art, eingegangen: new Date(now).toISOString(), ip, felder: daten };

  try {
    await env.EINSENDUNGEN.put(key, JSON.stringify(satz), { expirationTtl: TTL });
  } catch {
    return new Response("Die Einsendung konnte nicht gespeichert werden. Bitte später erneut.", { status: 500 });
  }

  // Benachrichtigung an den Betreiber. KV ist bereits geschrieben; der Versand läuft im
  // Hintergrund (waitUntil) über den Benachrichtigungs-Worker (Service-Binding MAILER), der per
  // Cloudflare Email Routing sendet. Scheitert er, bleibt die Einsendung in KV, und das Formular
  // zeigt dem Absender trotzdem "gesendet" (der 303 unten läuft unabhängig). Absender ist die
  // Verzeichnis-Domain, Empfänger Daniels gewöhnliche Adresse (NOTIFY_TO). Fehlt MAILER oder
  // NOTIFY_TO, wird nichts gesendet; die Einsendung steht dann allein in KV.
  const from = env.NOTIFY_FROM || "formular@die-besten-schluesseldienste.de";
  const to = env.NOTIFY_TO || "";
  if (env.MAILER && to) {
    const betreff = art === "garantie"
      ? `Garantie-Antrag: ${daten.firma || "ohne Firmenname"}`
      : `Eintrag beanspruchen: ${daten.business || "ohne Firmenname"}`;
    const zeilen = [`Formularart: ${art}`, `KV-Schlüssel: ${key}`, `Eingegangen: ${satz.eingegangen}`, ""];
    for (const [k, v] of Object.entries(daten)) zeilen.push(`${k}: ${v}`);
    const body = zeilen.join("\r\n");
    const raw =
      `From: ${from}\r\nTo: ${to}\r\nSubject: =?UTF-8?B?${btoa(unescape(encodeURIComponent(betreff)))}?=\r\n` +
      `Date: ${new Date(now).toUTCString()}\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset="UTF-8"\r\n` +
      `Content-Transfer-Encoding: base64\r\n\r\n` +
      btoa(unescape(encodeURIComponent(body))).replace(/(.{76})/g, "$1\r\n");
    const req = new Request("https://mailer.internal/send", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ from, to, raw }),
    });
    // Versand darf die Antwort weder verzögern noch blockieren; Fehler werden geschluckt.
    waitUntil(env.MAILER.fetch(req).catch(() => {}));
  }

  return seite(art === "garantie" ? "/festpreis-garantie/antrag/" : "/eintrag-beanspruchen/");
};
