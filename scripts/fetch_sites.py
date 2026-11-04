#!/usr/bin/env python3
"""Helfer für Gate 3: die eigene Website jedes behaltenen Eintrags in den Anreicherungs-Zwischen-
speicher lesen.

Gebraucht, wenn der Export keinen Text zum Anreichern mitbringt (leere reviews_tags, posts und
description). Gelesen werden die Startseite und bis zu drei Unterseiten, deren Link nach
Leistungen, Über uns, Notdienst, Preisen oder Einbruchschutz aussieht. Keine Schnittstelle, kein
Zugang, keine Kosten.

Aufruf:
  python3 scripts/fetch_sites.py output/<slug>/02-listings-clean.csv --cache output/<slug>/03-cache/sites \
      [--workers 24] [--timeout 12] [--limit 0] [--retry-failed]

Schreibt je Eintrags-Slug eine JSON-Datei: {slug, website, status, pages: [{url, title, meta,
headings, nav, text}], socials: {facebook, instagram, x, linkedin, youtube, tiktok, pinterest:
url}}. Die socials sind die Profillinks von den gelesenen Seiten (Teilen- und Anmeldelinks
übergangen). Ein Eintrag, der schon eine Datei im Zwischenspeicher hat, wird übersprungen; ein
zweiter Lauf liest also nur das Neue. `--socials` liest allein die Startseite jeder
zwischengespeicherten Website, die noch keine Profillinks hat, und ergänzt sie, ohne den übrigen
Zwischenspeicher anzufassen; `scripts/add_socials.py` schreibt sie danach in die Eintrags-CSV.
Am Ende steht die Aufstellung nach rohem Status und eine Zusammenfassungszeile nach Gruppe
(lesbar, keine Website, gesperrt, tot, per Skript aufgebaut, anderes), über jeden Eintrag der CSV
aus dem Zwischenspeicher gelesen, für den Gate-3-Bericht.

Die **Statuswerte** in den Dateien bleiben englisch (`ok`, `no website`, `http 403`, …): sie sind
Daten, nicht Meldungen, wandern über build_evidence.py als Zeile `site_status:` in die
Anreicherungspakete und stehen in schon geschriebenen Zwischenspeichern. Übersetzt sind Hilfe,
Beispiele und die Meldungen des Laufs.

Das Verfahren steht in wiki/framework/enrichment.md.
"""
import argparse, csv, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import ssl, urllib.request, urllib.error

csv.field_size_limit(10**9)

# Profile links worth keeping, by network. Order matters: x.com and twitter.com both map to "x".
NETWORKS = (("facebook", "facebook.com"), ("instagram", "instagram.com"), ("x", "x.com"), ("x", "twitter.com"),
            ("linkedin", "linkedin.com"), ("youtube", "youtube.com"), ("tiktok", "tiktok.com"), ("pinterest", "pinterest.com"))
NOT_PROFILE = re.compile(r"/(sharer|share|intent|login|signup|dialog|plugins|home\.php|hashtag|explore|reel/|p/|photo\.php|watch|embed|policies|help|about)\b|[?&](u|url|text|share)=", re.I)


def socials_from(links, page_url):
    """Profile links per network from a page's links, first one wins."""
    out = {}
    for href, _ in links:
        try: u = urljoin(page_url, href).split("#")[0]
        except Exception: continue
        host = urlparse(u).netloc.lower().removeprefix("www.").removeprefix("m.")
        path = urlparse(u).path.rstrip("/")
        for net, dom in NETWORKS:
            if (host == dom or host.endswith("." + dom)) and path and not NOT_PROFILE.search(u):
                if net not in out: out[net] = u
                break
    return out


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
# Adressen, die keine eigene Website sind: Profile, Branchenbücher, Baukästen. Die deutschen
# Branchenbücher stehen mit dabei, weil im Export oft ein Eintrag dort statt der Website steht.
SOCIAL = ("facebook.com", "instagram.com", "linkedin.com", "yelp.com", "google.com", "youtube.com",
          "x.com", "twitter.com", "nextdoor.com", "houzz.com", "thumbtack.com", "angi.com", "homeadvisor.com",
          "business.site", "linktr.ee", "tiktok.com",
          "gelbeseiten.de", "dasoertliche.de", "11880.com", "meinestadt.de", "golocal.de",
          "werkenntdenbesten.de", "cylex.de", "yellowmap.de", "jameda.de", "wlw.de")
# Unterseiten, die sich zu lesen lohnen: deutsche Benennungen des Schlüsseldienst-Gewerbes zuerst,
# die englischen bleiben für Betriebe mit englischen Pfaden stehen. Eigene Wörter kommen mit
# --want "wort|wort" dazu.
WANT_BASE = (r"leistung|service|dienstleistung|ueber-uns|über-uns|ueber_uns|unternehmen|firma|profil|"
             r"notdienst|notfall|24-?stunden|tueroeffnung|türöffnung|aufsperr|schliessanlage|schließanlage|"
             r"einbruchschutz|sicherheitstechnik|tresor|autoschluessel|autoschlüssel|werkstatt|montage|"
             r"preis|kosten|festpreis|anfahrt|faq|fragen|about|pricing|repair|install")
WANT = re.compile(WANT_BASE, re.I)
SKIP = re.compile(r"\.(pdf|jpe?g|png|gif|webp|svg|zip|mp4|docx?)($|\?)|/(blog|news|tag|category|cart|wp-login|privacy|terms)\b|^(mailto|tel|javascript):", re.I)
MAX_BYTES = 1_500_000
MAX_TEXT = 8000
DROP = {"script", "style", "noscript", "svg", "template", "iframe"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.headings, self.links, self.text = "", "", [], [], []
        self._skip = 0; self._in_title = False; self._h = None; self._a = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in DROP: self._skip += 1
        elif tag == "title": self._in_title = True
        elif tag == "meta" and (a.get("name") or a.get("property") or "").lower() in ("description", "og:description"):
            if not self.meta: self.meta = (a.get("content") or "").strip()
        elif tag in ("h1", "h2", "h3"): self._h = []
        elif tag == "a" and a.get("href"): self._a = [a["href"], []]
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr", "section"): self.text.append("\n")

    def handle_endtag(self, tag):
        if tag in DROP and self._skip: self._skip -= 1
        elif tag == "title": self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._h is not None:
            h = " ".join("".join(self._h).split())
            if h and len(h) < 140: self.headings.append(h)
            self._h = None
        elif tag == "a" and self._a:
            self.links.append((self._a[0], " ".join("".join(self._a[1]).split())))
            self._a = None

    def handle_data(self, d):
        if self._skip: return
        if self._in_title: self.title += d; return
        if self._h is not None: self._h.append(d)
        if self._a: self._a[1].append(d)
        self.text.append(d)


def clean(s):
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


_CTX_OK = ssl.create_default_context()
_CTX_ANY = ssl._create_unverified_context()


def _decompress(raw, content_encoding):
    """Manche Server liefern trotz `Accept-Encoding: identity` gzip oder deflate; urllib packt das
    nicht selbst aus, dann landet der rohe Strom als Text im Zwischenspeicher. Nach Header, sonst
    nach den Magic-Bytes (gzip 1f 8b) auspacken, tolerant gegen den MAX_BYTES-Schnitt
    (decompressobj liefert, so weit es kommt)."""
    import gzip, zlib
    ce = (content_encoding or "").lower()
    is_gzip = "gzip" in ce or raw[:2] == b"\x1f\x8b"
    is_deflate = "deflate" in ce
    if not (is_gzip or is_deflate):
        return raw
    try:
        wbits = zlib.MAX_WBITS | 16 if is_gzip else zlib.MAX_WBITS
        return zlib.decompressobj(wbits).decompress(raw) or raw
    except zlib.error:
        try:    # roher deflate ohne zlib-Kopf
            return zlib.decompressobj(-zlib.MAX_WBITS).decompress(raw) or raw
        except zlib.error:
            return raw


_META_CHARSET = re.compile(rb'charset=["\']?\s*([a-zA-Z0-9_.\-]+)', re.I)


def _decode(raw, header_charset):
    """HTML robust dekodieren. UTF-8 gewinnt zuerst, denn gültiges UTF-8 entsteht fast nie
    zufällig; eine Seite, die fälschlich windows-1252 angibt, aber UTF-8 ist, wird so richtig
    gelesen. Ein paar kaputte Bytes in einer sonst gültigen UTF-8-Seite (Fehler der Quelle)
    werden ersetzt, statt die ganze Seite auf 1252 zu kippen. Erst wenn UTF-8 deutlich scheitert,
    kommt die ausdrücklich deklarierte Kodierung, sonst windows-1252. Die alte Fassung erzwang bei
    iso-8859-1 UTF-8 und dekodierte latin-1/1252-Seiten als UTF-8 – daher das Mojibake im Cache."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    rep = raw.decode("utf-8", errors="replace")
    if rep.count("�") <= max(2, len(raw) // 5000):   # fast-gültiges UTF-8: wenige Fehlbytes
        return rep
    m = _META_CHARSET.search(raw[:4096])
    meta = (m.group(1).decode("ascii", "ignore").lower() if m else "")
    for enc in ((header_charset or "").lower(), meta):
        if enc and enc not in ("utf-8", "utf8", "iso-8859-1", "latin-1", "latin1", "ascii", "us-ascii"):
            try:
                return raw.decode(enc)
            except (LookupError, UnicodeDecodeError):
                pass
    return raw.decode("cp1252", errors="replace")


def get(url, timeout):
    """Nur Standardbibliothek, damit es mit dem mitgelieferten Python eines Macs läuft. Erst eine
    geprüfte TLS-Verbindung, dann eine ungeprüfte, wenn das Zertifikat nicht taugt (bei kleinen
    Handwerksbetrieben häufig)."""
    for ctx in (_CTX_OK, _CTX_ANY):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "de-DE,de;q=0.9", "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                ctype = r.headers.get("content-type", "")
                if "html" not in ctype and ctype: return None, f"not html ({ctype[:30]})", r.url
                raw = r.read(MAX_BYTES)
                raw = _decompress(raw, r.headers.get("Content-Encoding", ""))
                return _decode(raw, r.headers.get_content_charset()), "ok", r.url
        except urllib.error.HTTPError as e:
            return None, f"http {e.code}", url
        except ssl.SSLError:
            continue
        except urllib.error.URLError as e:
            if isinstance(e.reason, ssl.SSLError) or "CERTIFICATE" in str(e.reason).upper(): continue
            return None, type(e.reason).__name__ if hasattr(e, "reason") else "URLError", url
        except Exception as e:
            return None, type(e).__name__, url
    return None, "ssl", url


def parse(html, url):
    p = Page()
    try: p.feed(html)
    except Exception: pass
    return p, {"url": url, "title": clean(p.title)[:200], "meta": clean(p.meta)[:400],
               "headings": list(dict.fromkeys(p.headings))[:40],
               "nav": list(dict.fromkeys(t for _, t in p.links if t and len(t) < 40))[:60],
               "text": clean("".join(p.text))[:MAX_TEXT]}


def fetch(row, cache, timeout, retry=False):
    path = os.path.join(cache, row["slug"] + ".json")
    if os.path.exists(path):
        if not retry: return "cached"
        with open(path, encoding="utf-8") as f: old = json.load(f)
        if old.get("website") == (row.get("website") or "").strip() and (old["status"] == "ok" or old["status"].startswith(("no website", "social"))): return "cached"
    site = (row.get("website") or "").strip()
    out = {"slug": row["slug"], "website": site, "status": "", "pages": []}
    if not site or site.lower() == "none":
        out["status"] = "no website"
    elif any(s in urlparse(site).netloc.lower() for s in SOCIAL):
        out["status"] = "social or profile link, not read"
    else:
        if not site.startswith("http"): site = "http://" + site
        html, st, final = get(site, timeout)
        out["status"] = st
        if html:
            p, page = parse(html, final); out["pages"].append(page)
            host = urlparse(final).netloc.lower().removeprefix("www.")
            seen, picks = {final.rstrip("/")}, []
            for href, text in p.links:
                if SKIP.search(href): continue
                u = urljoin(final, href).split("#")[0]
                if urlparse(u).netloc.lower().removeprefix("www.") != host: continue
                if u.rstrip("/") in seen: continue
                if WANT.search(urlparse(u).path) or WANT.search(text):
                    seen.add(u.rstrip("/")); picks.append(u)
            out["socials"] = socials_from(p.links, final)
            for u in picks[:3]:
                h2, st2, f2 = get(u, timeout)
                if h2:
                    p2, page2 = parse(h2, f2); out["pages"].append(page2)
                    for k, v in socials_from(p2.links, f2).items(): out["socials"].setdefault(k, v)
            if sum(len(pg["text"]) for pg in out["pages"]) < 200: out["status"] = "ok but empty (script-rendered or parked)"
    with open(path, "w", encoding="utf-8") as f: json.dump(out, f, ensure_ascii=False)
    return out["status"]


# Die Gruppen der Zusammenfassungszeile. Nur für die Ausgabe, sie stehen in keiner Datei.
GROUPS = ("lesbar", "keine Website", "gesperrt", "tot", "per Skript aufgebaut", "anderes")
DEAD = ("gaierror", "ConnectionRefusedError", "ConnectionResetError", "TimeoutError", "timeout", "RemoteDisconnected",
        "IncompleteRead", "ssl", "URLError", "OSError", "BadStatusLine")


def group(status):
    """Einen rohen Status (englisch, wie er in der Datei steht) auf eine der GROUPS abbilden,
    nur für die Zusammenfassungszeile."""
    st = (status or "").strip()
    if st == "ok": return "lesbar"
    if st == "no website": return "keine Website"
    if st.startswith("ok but empty"): return "per Skript aufgebaut"
    m = re.match(r"http (\d{3})$", st)
    if m:
        code = int(m.group(1))
        if code in (401, 403, 405, 406, 429, 999): return "gesperrt"
        if code in (404, 410) or code >= 500: return "tot"
        return "anderes"
    if st in DEAD or st.endswith("Error"): return "tot"
    return "anderes"


def summary(rows, cache):
    """Eine Zeile nach Gruppe über die Dateien im Zwischenspeicher zu jedem Eintrag der CSV."""
    counts = {g: 0 for g in GROUPS}; missing = 0
    for r in rows:
        path = os.path.join(cache, r["slug"] + ".json")
        if not os.path.exists(path): missing += 1; continue
        try:
            with open(path, encoding="utf-8") as f: counts[group(json.load(f).get("status", ""))] += 1
        except Exception: counts["anderes"] += 1
    line = ", ".join(f"{counts[g]} {g}" for g in GROUPS)
    return f"Zusammenfassung: {line} (von {len(rows)} Einträgen" + (f", {missing} noch nicht gelesen" if missing else "") + ")"


def add_socials(row, cache, timeout):
    """--socials: die Startseite einer zwischengespeicherten Website erneut lesen und ihre
    Profillinks ablegen."""
    path = os.path.join(cache, row["slug"] + ".json")
    if not os.path.exists(path): return "no cache"
    with open(path, encoding="utf-8") as f: old = json.load(f)
    if "socials" in old: return "had socials"
    if old["status"] != "ok" or not old["pages"]: old["socials"] = {}; st = "not readable"
    else:
        html, st, final = get(old["pages"][0]["url"], timeout)
        old["socials"] = socials_from(parse(html, final)[0].links, final) if html else {}
        st = "ok" if html else st
    with open(path, "w", encoding="utf-8") as f: json.dump(old, f, ensure_ascii=False)
    return st


def main():
    ap = argparse.ArgumentParser(description="Gate 3: die eigenen Websites der Einträge in den Zwischenspeicher lesen.",
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="die bereinigte CSV aus Gate 2, output/<slug>/02-listings-clean.csv")
    ap.add_argument("--cache", required=True, help="Ordner für die gelesenen Seiten, output/<slug>/03-cache/sites")
    ap.add_argument("--workers", type=int, default=24, help="wie viele Websites gleichzeitig gelesen werden (Vorgabe 24)")
    ap.add_argument("--timeout", type=int, default=12, help="Sekunden, die eine Website zum Antworten hat (Vorgabe 12)")
    ap.add_argument("--limit", type=int, default=0, help="nur die ersten N Zeilen lesen (Probelauf); 0 heißt alle")
    ap.add_argument("--retry-failed", action="store_true", help="jeden Eintrag erneut lesen, dessen letzter Versuch scheiterte oder dessen Adresse sich geändert hat")
    ap.add_argument("--want", default="", help='weitere Wörter für Unterseiten, als Regex-Alternativen, z. B. "schluesselnotdienst|fenstersicherung"')
    ap.add_argument("--socials", action="store_true", help="nur Profillinks ergänzen, bei zwischengespeicherten Websites, die noch keine haben (die Startseite wird dafür erneut gelesen)")
    a = ap.parse_args()
    global WANT
    if a.want.strip(): WANT = re.compile(WANT_BASE + "|" + a.want.strip(), re.I)
    os.makedirs(a.cache, exist_ok=True)
    with open(a.csv, newline="", encoding="utf-8") as f: rows = list(csv.DictReader(f))
    if a.limit: rows = rows[:a.limit]
    tally, done = {}, 0
    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(add_socials, r, a.cache, a.timeout) if a.socials else ex.submit(fetch, r, a.cache, a.timeout, a.retry_failed) for r in rows]
        for fu in as_completed(futs):
            try: st = fu.result()
            except Exception as e: st = "error " + type(e).__name__   # Statuswerte bleiben englisch: sie stehen so in den Dateien
            tally[st] = tally.get(st, 0) + 1; done += 1
            if done % 200 == 0: print(f"{done}/{len(rows)}", file=sys.stderr, flush=True)
    print(f"Einträge: {len(rows)}")
    for k, v in sorted(tally.items(), key=lambda x: -x[1]): print(f"  {k}: {v}")
    print(summary(rows, a.cache))


if __name__ == "__main__":
    main()
