// Schlanker Benachrichtigungs-Worker für das Verzeichnis.
//
// Zweck: Die Pages-Function functions/api/claim.ts nimmt die beiden Formulare (Eintrag
// beanspruchen, Garantie-Antrag) an und schreibt sie in KV. Pages Functions kennen das
// send_email-Binding NICHT (in diesem Projekt bestätigt), können also selbst keine Mail
// verschicken. Dieser Worker schließt die Lücke: Pages ruft ihn über ein Service-Binding
// (MAILER) auf, er sendet die fertige Nachricht über Cloudflare Email Routing.
//
// Kein Drittanbieter, kein API-Schlüssel. Absender ist die Verzeichnis-Domain, Empfänger ist
// Daniels gewöhnliche Adresse (eine in Email Routing verifizierte Zieladresse); beide reicht
// die Pages-Function mit, sie stehen nicht hier im Code.
//
// Erreichbar ist der Worker nur über das Service-Binding, nicht öffentlich (kein Route-Eintrag).
// Er ändert nichts, speichert nichts; er sendet genau eine Mail je Aufruf.

import { EmailMessage } from "cloudflare:email";

interface Env {
  // Email-Routing-Sende-Binding (wrangler.jsonc: send_email). Sendet nur an verifizierte
  // Zieladressen des Kontos; das ist hier gewollt, Empfänger ist allein der Betreiber.
  EMAIL: { send(message: EmailMessage): Promise<void> };
}

interface Payload {
  from: string; // Absender, von der Pages-Function (Verzeichnis-Domain)
  to: string;   // Empfänger, von der Pages-Function (verifizierte Zieladresse des Betreibers)
  raw: string;  // vollständige Roh-MIME-Nachricht (Header + Base64-Text), von der Pages-Function gebaut
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return new Response("Nur POST.", { status: 405 });
    }
    let p: Payload;
    try {
      p = (await request.json()) as Payload;
    } catch {
      return new Response("Ungültige Anfrage.", { status: 400 });
    }
    if (!p || !p.from || !p.to || !p.raw) {
      return new Response("from, to und raw sind nötig.", { status: 400 });
    }
    try {
      await env.EMAIL.send(new EmailMessage(p.from, p.to, p.raw));
      return new Response("gesendet", { status: 200 });
    } catch (e) {
      // Der Aufrufer wertet den Fehlschlag nicht aus (KV hält die Einsendung ohnehin); der Text
      // hilft nur bei `wrangler tail` während eines Testlaufs.
      return new Response("Versand fehlgeschlagen: " + (e as Error).message, { status: 502 });
    }
  },
};
