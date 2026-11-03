// Mail Worker for the directory.
//
//  email()  Mail to hello@ arrives here through Email Routing. The Worker sends a fixed acknowledgement
//           to the sender, optionally forwards the original, and asks Claude to classify the message,
//           check it against the listings and draft a reply. The result is queued in KV and emailed to
//           the owner for review.
//  fetch()  POST /claim      the site's claim form can post here instead of Formspree (same queue, same triage)
//           GET  /inbox      the queue, newest first (Authorization: Bearer <INBOX_KEY>, or ?key=)
//           POST /inbox/:id  {"status": "done" | "ignored"} marks an item; {"status": "send"} sends its draft
//                            reply to the sender, which is the one outbound message that is never automatic
//           GET  /approve/:id/:token   the review page linked from the review email: the draft in a box, Send and Ignore
//           POST /approve/:id/:token   sends the (edited) draft, or marks the item ignored
//
// The Worker never changes a listing. A draft goes out only through the review page or POST /inbox/:id on the owner's word.
// Config: wrangler.jsonc, filled by scripts/mail_worker.py from the site's site.json. Nothing in here is specific to one directory.

import Anthropic from "@anthropic-ai/sdk";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import PostalMime from "postal-mime";
import { z } from "zod";
import listings from "./listings.json";
import { CATEGORIES, acknowledgement, triageSystem, UI, CATEGORY_LABELS } from "./templates";

type Listing = { slug: string; name: string; city: string; phone: string; host: string; rating: string; reviews: string; featured: string };
const LISTINGS = listings as Listing[];

interface Env {
  INBOX: KVNamespace;
  EMAIL: { send(msg: Record<string, unknown>): Promise<{ messageId: string }> };
  ANTHROPIC_API_KEY: string;
  INBOX_KEY: string;
  BRAND: string;
  SITE_URL: string;
  MAIL_ADDRESS: string;
  SEND_FROM: string;
  REVIEW_TO: string;
  FORWARD_TO: string;
  TIERS: string;
  NICHE_PLURAL: string;
  STATE_NAME: string;
  NAME_NOISE: string;   // comma-separated words too common in this trade's business names to match on (filled by scripts/mail_worker.py from site.json)
  WORKER_URL?: string;
}

const Triage = z.object({
  category: z.enum(CATEGORIES),
  confidence: z.number(),
  matched_slug: z.string().nullable(),
  checks: z.object({
    email_domain_matches_website: z.boolean().nullable(),
    phone_matches_listing: z.boolean().nullable(),
    business_in_directory: z.boolean(),
  }),
  missing: z.array(z.string()),
  summary: z.string(),
  draft_reply: z.string(),
});
type Triage = z.infer<typeof Triage>;

interface Item {
  id: string;
  received: string;
  source: "email" | "form";
  from: string;
  subject: string;
  message_id?: string;
  text: string;
  fields?: Record<string, string>;
  candidates: Listing[];
  triage: Triage | null;
  triage_error?: string;
  status: "new" | "done" | "ignored";
  sent_at?: string;
  approve_token?: string;
}

const digits = (s: string) => s.replace(/\D/g, "").slice(-10);
const domainOfEmail = (e: string) => (e.split("@")[1] || "").toLowerCase().replace(/^www\./, "");
const isEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

// Listings the message could be about: a listing address pasted in, the same phone, the same website host,
// or the name's distinctive words.
function candidates(env: Env, text: string, from: string): Listing[] {
  const found = new Map<string, Listing>();
  const lower = text.toLowerCase();
  const slugs = new Set(Array.from(lower.matchAll(/\/company\/[a-z-]+\/[a-z0-9-]+\/([a-z0-9-]+)\/?/g), (m) => m[1]));
  const phones = new Set(Array.from(text.matchAll(/\+?1?[\s.(-]*\d{3}[\s.)-]*\d{3}[\s.-]*\d{4}/g), (m) => digits(m[0])));
  const hosts = new Set(Array.from(text.matchAll(/(?:https?:\/\/)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)/gi), (m) => m[1].toLowerCase()));
  const senderHost = domainOfEmail(from);
  const free = new Set(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com", "me.com", "live.com"]);
  if (senderHost && !free.has(senderHost)) hosts.add(senderHost);
  const words = new Set((text.toLowerCase().match(/[a-z][a-z'&-]{3,}/g) || []));
  const noise = new Set(["inc", "llc", "corp", "company", "service", "services", "construction", "custom", "south", "north", "east", "west", "the", "and",
    ...(env.NAME_NOISE || "").toLowerCase().split(",").map((w) => w.trim()).filter(Boolean)]);
  for (const l of LISTINGS) {
    if (slugs.has(l.slug)) found.set(l.slug, l);
    else if (l.phone && phones.has(l.phone)) found.set(l.slug, l);
    else if (l.host && hosts.has(l.host)) found.set(l.slug, l);
    else {
      const parts = l.name.toLowerCase().split(/[^a-z'&-]+/).filter((w) => w.length > 3 && !noise.has(w));
      const distinctive = parts.length >= 2 || (parts.length === 1 && parts[0].length >= 6);   // "Into H2O Pools" must not match every "into"
      if (distinctive && parts.every((w) => words.has(w))) found.set(l.slug, l);
    }
    if (found.size >= 8) break;
  }
  return [...found.values()];
}

async function triage(env: Env, item: Item): Promise<Triage> {
  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const body = item.text.length > 6000 ? item.text.slice(0, 6000) + "\n[trimmed]" : item.text;
  const cands = item.candidates.length
    ? item.candidates.map((c) => `- ${c.slug}: ${c.name}, ${c.city}; phone ${c.phone || "none"}; website ${c.host || "none"}; ${c.rating} from ${c.reviews} reviews${c.featured ? "; featured" : ""}`).join("\n")
    : "(none matched)";
  const user = [
    `<message source="${item.source}">`,
    `From: ${item.from}`,
    `Subject: ${item.subject}`,
    item.fields ? `Form fields: ${JSON.stringify(item.fields)}` : "",
    ``,
    body,
    `</message>`,
    ``,
    `<listing_candidates>`,
    cands,
    `</listing_candidates>`,
  ].join("\n");
  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    system: triageSystem(env.BRAND, env.SITE_URL, env.TIERS, env.NICHE_PLURAL, env.STATE_NAME),
    messages: [{ role: "user", content: user }],
    output_config: { effort: "low", format: zodOutputFormat(Triage) },
  });
  if (response.stop_reason === "refusal") throw new Error("the model declined this message");
  const text = response.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  return Triage.parse(JSON.parse(text));
}

// Every outbound message goes through here. Headers are tried first and dropped if the service refuses them.
async function send(env: Env, to: string, subject: string, text: string, headers: Record<string, string> = {}, bcc?: string): Promise<string> {
  const base = { to, from: { email: env.SEND_FROM, name: env.BRAND }, replyTo: env.MAIL_ADDRESS, subject, text, ...(bcc ? { bcc } : {}) };
  try { return (await env.EMAIL.send({ ...base, headers })).messageId; }
  catch (e) {
    const code = (e as { code?: string }).code || "";
    if (Object.keys(headers).length && code.startsWith("E_HEADER")) return (await env.EMAIL.send(base)).messageId;
    throw e;
  }
}

function reviewText(env: Env, item: Item): string {
  const t = item.triage;
  const ja = (v: boolean | null | undefined) => (v === true ? "ja" : v === false ? "nein" : "unbekannt");
  const lines = [`Prüfen und senden: ${approveUrl(env, item)}`, ``,
    `Vorgang ${item.id}, eingegangen ${item.received.slice(0, 16).replace("T", " ")} über ${item.source}`,
    `${UI.fieldFrom}: ${item.from}`, `Betreff: ${item.subject}`, ``];
  if (!t) lines.push(`Einordnung fehlgeschlagen: ${item.triage_error || "unbekannt"}`, ``);
  else {
    const c = t.checks;
    lines.push(`${UI.fieldCategory}: ${CATEGORY_LABELS[t.category] || t.category} (${UI.fieldConfidence} ${t.confidence.toFixed(2)})`,
      `${UI.fieldMatched}: ${t.matched_slug || UI.noMatch} | im Verzeichnis: ${ja(c.business_in_directory)} | E-Mail passt zur Website: ${ja(c.email_domain_matches_website)} | Telefon passt zum Eintrag: ${ja(c.phone_matches_listing)}`,
      ``, t.summary, ``);
    if (t.missing.length) lines.push(`${UI.fieldMissing}: ${t.missing.join("; ")}`, ``);
    if (t.draft_reply) lines.push(`${UI.draftLabel} (noch nicht gesendet):`, ``, t.draft_reply, ``);
    else lines.push(UI.emptyDraft, ``);
  }
  lines.push(`--- die Nachricht im Original ---`, item.text.slice(0, 4000));
  return lines.join("\n");
}

function approveUrl(env: Env, item: Item): string {
  return `${env.WORKER_URL || ""}/approve/${item.id}/${item.approve_token}`;
}

const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c] as string));

// The review page: plain HTML, no script. The draft sits in a box the owner can edit before sending.
function approvePage(env: Env, item: Item, note = ""): Response {
  const t = item.triage;
  const draft = t?.draft_reply || "";
  const done = item.status !== "new";
  const ja = (v: boolean | null | undefined) => (v === true ? "ja" : v === false ? "nein" : "unbekannt");
  const body = `<!doctype html><html lang="${UI.lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>${esc(item.subject)}</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;color:#0B2545}h1{font-size:1.3rem}textarea{width:100%;min-height:16rem;font:inherit;padding:.6rem;border:1px solid #c9d6e3;border-radius:8px}
button{font:inherit;padding:.6rem 1.2rem;border-radius:8px;border:0;background:#F5A623;color:#0B2545;font-weight:700;margin-right:.6rem}button.quiet{background:#e6f2f4}pre{white-space:pre-wrap;background:#f5f6f8;padding:.8rem;border-radius:8px}.note{background:#e6f2f4;padding:.6rem .8rem;border-radius:8px}small{color:#4F6B74}</style>
<h1>${esc(UI.reviewHeading(env.BRAND, item.subject))}</h1>
${note ? `<p class="note">${esc(note)}</p>` : ""}
<p><small>${esc(UI.fieldFrom)}: ${esc(item.from)}, ${esc(item.received.slice(0, 16).replace("T", " "))}, ${item.source}. Status: ${item.status}${item.sent_at ? `, Antwort gesendet ${esc(item.sent_at.slice(0, 16).replace("T", " "))}` : ""}.</small></p>
${t ? `<p><b>${esc(CATEGORY_LABELS[t.category] || t.category.replace(/_/g, " "))}</b> (${esc(UI.fieldConfidence)} ${t.confidence.toFixed(2)}). ${esc(UI.fieldMatched)}: ${esc(t.matched_slug || UI.noMatch)}. Im Verzeichnis: ${ja(t.checks.business_in_directory)}. E-Mail passt zur Website: ${ja(t.checks.email_domain_matches_website)}. Telefon passt zum Eintrag: ${ja(t.checks.phone_matches_listing)}.</p><p>${esc(t.summary)}</p>${t.missing.length ? `<p>${esc(UI.fieldMissing)}: ${esc(t.missing.join("; "))}</p>` : ""}` : `<p>Einordnung fehlgeschlagen: ${esc(item.triage_error || "unbekannt")}</p>`}
${done ? `<p class="note">${esc(UI.alreadyHandled)}</p>` : draft ? `<form method="post"><p><label>${esc(UI.draftLabel)} an ${esc(item.from)} (vor dem Senden änderbar):</label><br><textarea name="text">${esc(draft)}</textarea></p>
<p><button name="action" value="send">${esc(UI.sendButton)}</button><button class="quiet" name="action" value="ignore">${esc(UI.ignoreButton)}</button></p></form>` : `<p class="note">${esc(UI.emptyDraft)}</p>`}
<h2>Die Nachricht im Original</h2><pre>${esc(item.text.slice(0, 6000))}</pre></html>`;
  return new Response(body, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
}

async function sendDraft(env: Env, item: Item, text: string): Promise<string> {
  const headers: Record<string, string> = {};
  if (item.message_id) { headers["In-Reply-To"] = item.message_id; headers["References"] = item.message_id; }
  // The owner is blind-copied on every reply that goes out, so the sent message lands in their inbox as proof.
  const copyTo = env.REVIEW_TO && !env.REVIEW_TO.startsWith("REPLACE") && env.REVIEW_TO.toLowerCase() !== item.from.toLowerCase() ? env.REVIEW_TO : undefined;
  const id = await send(env, item.from, UI.subjectReply(item.subject).slice(0, 200), text, headers, copyTo);
  item.status = "done"; item.sent_at = new Date().toISOString();
  await store(env, item);
  return id;
}

async function store(env: Env, item: Item): Promise<void> {
  await env.INBOX.put(`msg:${item.id}`, JSON.stringify(item), { expirationTtl: 60 * 60 * 24 * 90 });
}

async function enqueue(env: Env, ctx: ExecutionContext, item: Item): Promise<void> {
  item.approve_token = crypto.randomUUID().replace(/-/g, "");
  await store(env, item);   // stored before triage, so a model error never loses the message
  ctx.waitUntil((async () => {
    try { item.triage = await triage(env, item); }
    catch (e) { item.triage_error = e instanceof Error ? e.message : String(e); }
    await store(env, item);
    if (env.REVIEW_TO && !env.REVIEW_TO.startsWith("REPLACE")) {
      const tag = item.triage ? item.triage.category.replace(/_/g, " ") : "triage failed";
      try { await send(env, env.REVIEW_TO, `[${env.BRAND}] ${tag}: ${item.subject}`.slice(0, 200), reviewText(env, item)); }
      catch (e) { console.log("review email failed:", e instanceof Error ? e.message : e); }
    }
  })());
}

// Auto-replies, bounces and list mail get no acknowledgement, so two robots never talk to each other.
function isAutomated(from: string, headers: Headers): boolean {
  const auto = (headers.get("auto-submitted") || "no").toLowerCase();
  const prec = (headers.get("precedence") || "").toLowerCase();
  return auto !== "no" || ["bulk", "list", "junk"].includes(prec) || /no-?reply|mailer-daemon|postmaster|bounce|notification/i.test(from);
}

function newId(): string {
  return `${Date.now().toString(36)}-${crypto.randomUUID().slice(0, 8)}`;
}

export default {
  async email(message: ForwardableEmailMessage, env: Env, ctx: ExecutionContext): Promise<void> {
    const raw = await new Response(message.raw).arrayBuffer();
    const parsed = await PostalMime.parse(raw);
    const from = message.from;
    const subject = parsed.subject || "(no subject)";
    const text = (parsed.text || parsed.html?.replace(/<[^>]+>/g, " ") || "").replace(/\s+/g, " ").trim().slice(0, 20000);
    const messageId = message.headers.get("message-id") || undefined;
    const item: Item = { id: newId(), received: new Date().toISOString(), source: "email", from, subject, message_id: messageId, text,
      candidates: candidates(env, `${subject}\n${text}`, from), triage: null, status: "new" };

    if (env.FORWARD_TO) {
      try { await message.forward(env.FORWARD_TO, new Headers({ "X-Directory-Queue": item.id })); }
      catch (e) { console.log("forward failed:", e instanceof Error ? e.message : e); }
    }
    if (!isAutomated(from, message.headers)) {
      const headers: Record<string, string> = { "Auto-Submitted": "auto-replied" };
      if (messageId) { headers["In-Reply-To"] = messageId; headers["References"] = messageId; }
      try { await send(env, from, `Re: ${subject}`.slice(0, 200), acknowledgement(env.BRAND, env.SITE_URL), headers); }
      catch (e) { console.log("acknowledgement failed:", e instanceof Error ? e.message : e); }
    }
    await enqueue(env, ctx, item);
  },

  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "POST" && url.pathname === "/claim") {
      const form = await request.formData();
      const fields: Record<string, string> = {};
      for (const [k, v] of form.entries()) if (typeof v === "string" && !k.startsWith("_")) fields[k] = v.slice(0, 2000);
      if (form.get("_gotcha")) return Response.redirect(`${env.SITE_URL}/claim/?sent=1`, 303);   // honeypot: look accepted, keep nothing
      const from = (fields.email || "").trim() || "(no email given)";
      const text = Object.entries(fields).map(([k, v]) => `${k}: ${v}`).join("\n");
      const subject = `Claim form: ${fields.business || fields.name || "(no business named)"}`;
      const item: Item = { id: newId(), received: new Date().toISOString(), source: "form", from, subject, text, fields, candidates: candidates(env, text, from), triage: null, status: "new" };
      await enqueue(env, ctx, item);
      // The same acknowledgement an email gets. `_noack` is for re-entering an old submission by hand.
      if (isEmail(from) && !form.get("_noack")) {
        try { await send(env, from, `Re: your listing request on ${env.BRAND}`, acknowledgement(env.BRAND, env.SITE_URL), { "Auto-Submitted": "auto-replied" }); }
        catch (e) { console.log("form acknowledgement failed:", e instanceof Error ? e.message : e); }
      }
      return Response.redirect(`${env.SITE_URL}/claim/?sent=1`, 303);
    }

    const ap = url.pathname.match(/^\/approve\/([a-z0-9-]+)\/([a-f0-9]{32})$/);
    if (ap) {
      const item = (await env.INBOX.get(`msg:${ap[1]}`, "json")) as Item | null;
      if (!item || !item.approve_token || item.approve_token !== ap[2]) return new Response("not found", { status: 404 });
      if (request.method === "GET") return approvePage(env, item);
      if (request.method === "POST") {
        const form = await request.formData();
        if (item.status !== "new") return approvePage(env, item, UI.alreadyHandled);
        if (form.get("action") === "ignore") { item.status = "ignored"; await store(env, item); return approvePage(env, item, UI.ignoredNotice); }
        const text = String(form.get("text") || "").trim();
        if (!text) return approvePage(env, item, "Nichts zu senden: das Antwortfeld ist leer.");
        if (!isEmail(item.from)) return approvePage(env, item, `No usable sender address: ${item.from}`);
        try { await sendDraft(env, item, text); }
        catch (e) { return approvePage(env, item, `Senden fehlgeschlagen: ${e instanceof Error ? e.message : String(e)}`); }
        return approvePage(env, item, `Sent to ${item.from}. A copy is on its way to ${env.REVIEW_TO}.`);
      }
      return new Response("method not allowed", { status: 405 });
    }

    const key = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "") || url.searchParams.get("key") || "";
    if (!env.INBOX_KEY || key !== env.INBOX_KEY) return new Response("not found", { status: 404 });

    if (request.method === "GET" && url.pathname === "/inbox") {
      const list = await env.INBOX.list({ prefix: "msg:" });
      const items = (await Promise.all(list.keys.map((k) => env.INBOX.get(k.name, "json")))) as Item[];
      const wanted = url.searchParams.get("status") || "new";
      const out = items.filter((i) => i && (wanted === "all" || i.status === wanted)).sort((a, b) => b.received.localeCompare(a.received));
      return Response.json(out);
    }
    const m = url.pathname.match(/^\/inbox\/([a-z0-9-]+)$/);
    if (request.method === "POST" && m) {
      const item = (await env.INBOX.get(`msg:${m[1]}`, "json")) as Item | null;
      if (!item) return new Response("no such item", { status: 404 });
      const body = (await request.json().catch(() => ({}))) as { status?: string; text?: string };
      if (body.status === "retriage") {   // after a matcher or prompt change: match again, triage again, email the review again
        item.candidates = candidates(env, `${item.subject}\n${item.text}`, item.from); item.triage = null; delete item.triage_error; item.status = "new";
        await enqueue(env, ctx, item);
        return Response.json({ id: item.id, status: "retriage started", candidates: item.candidates.map((c) => c.slug) });
      }
      if (body.status === "send") {
        const text = (body.text || item.triage?.draft_reply || "").trim();   // the owner may send an edited text instead of the draft
        if (!text) return Response.json({ error: "nichts zu senden: kein Entwurf und kein Text angegeben" }, { status: 400 });
        if (!isEmail(item.from)) return Response.json({ error: `no usable sender address: ${item.from}` }, { status: 400 });
        const id = await sendDraft(env, item, text);
        return Response.json({ id: item.id, status: item.status, sent: id, to: item.from });
      }
      if (body.status === "done" || body.status === "ignored") item.status = body.status;
      await store(env, item);
      return Response.json({ id: item.id, status: item.status });
    }
    return new Response("not found", { status: 404 });
  },
} satisfies ExportedHandler<Env>;
