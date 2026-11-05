#!/usr/bin/env python3
"""Helfer für Gate 6: ein veröffentlichtes Verzeichnis von außen prüfen. Deutsche Fassung.

Liest nur. Nach dem Deploy gegen die echte Domain laufen lassen, und gegen die pages.dev-Adresse,
um zu bestätigen, dass diese Adresse aus der Suche herausgehalten wird.

Die geprüften Pfade sind die der deutschen Fassung (wiki/konventionen.md):
  /verzeichnis/                      Blättern, noindex und follow
  /verzeichnis/<bundesland>/         Bundesland
  /verzeichnis/<bundesland>/<stadt>/ Stadt
  /firma/<bundesland>/<stadt>/<slug>/ Eintrag
  /impressum/, /datenschutz/         Pflichtseiten, aus dem Fußbereich verlinkt
  /eintrag-beanspruchen/, /premium/  noindex

Aufruf:
  python3 scripts/check_live.py https://die-besten-schluesseldienste.de [--pages-dev https://projekt.pages.dev] [--expect-urls 1076]
"""
import argparse, re, sys, ssl, socket, urllib.request, urllib.error
from urllib.parse import urlparse

UA = {"User-Agent": "verzeichnis-blueprint-check/1.0"}


def get(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20)
        return r.status, dict((k.lower(), v) for k, v in r.headers.items()), r.read().decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, dict((k.lower(), v) for k, v in e.headers.items()), e.read().decode("utf-8", "replace"), url
    except Exception as e:
        return 0, {}, str(e), url


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None   # die Weiterleitung nicht folgen, sondern die 3xx-Antwort zeigen


def redirect_of(url):
    """Status und Location einer Adresse, ohne der Weiterleitung zu folgen – für die www-Prüfung."""
    try:
        r = urllib.request.build_opener(_NoRedirect).open(urllib.request.Request(url, headers=UA), timeout=20)
        return getattr(r, "status", r.getcode()), r.headers.get("location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("location", "")
    except Exception:
        return 0, ""


def tls_notafter(host):
    """(True, Ablaufdatum) wenn das TLS-Zertifikat der Domain gültig verifiziert; sonst (False, Grund).
    Eine erfolgreiche verifizierte TLS-Verbindung heißt: das Zertifikat passt zum Hostnamen und ist von
    einer anerkannten Stelle, nicht abgelaufen."""
    try:
        with socket.create_connection((host, 443), timeout=20) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=host) as ss:
                return True, ss.getpeercert().get("notAfter", "")
    except Exception as e:
        return False, str(e)[:70]


def main():
    ap = argparse.ArgumentParser(description="Gate 6: ein veröffentlichtes Verzeichnis von außen prüfen.")
    ap.add_argument("base", help="die echte Domain, z. B. https://die-besten-schluesseldienste.de")
    ap.add_argument("--pages-dev", default="", help="die pages.dev-Adresse, die noindex senden muss")
    ap.add_argument("--expect-urls", type=int, default=0, help="erwartete Zahl der Adressen in der Sitemap")
    a = ap.parse_args()
    base = a.base.rstrip("/"); ok = True
    host = urlparse(base).netloc; scheme = urlparse(base).scheme or "https"
    real_domain = "pages.dev" not in host   # www, Zertifikat und Sitemap-Host nur gegen die echte Domain prüfen

    def line(passed, text):
        nonlocal ok
        ok = ok and passed
        print(("BESTANDEN      " if passed else "DURCHGEFALLEN  ") + text)

    s, h, body, _ = get(base + "/")
    line(s == 200, f"Startseite antwortet mit 200 (erhalten: {s})")
    line("<h1" in body, "Startseite hat eine H1")
    line('lang="de"' in body, "Startseite ist als deutschsprachig gekennzeichnet (lang=\"de\")")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', body)
    line(bool(m), f"Startseite hat ein canonical: {m.group(1) if m else 'keines'}")
    line('content="noindex' not in body, "Startseite ist nicht noindex")
    line('data-preview="1"' not in body, "Startseite zeigt keine Vorschau-Premium-Karten "
                                         "(featuredPreview in site.json auf false setzen und neu bauen)")
    # Impressum und Datenschutz müssen aus dem Fußbereich jeder Seite verlinkt sein (§ 5 DDG, Art. 13 DSGVO).
    for path in ("/impressum/", "/datenschutz/"):
        line(path in body, f"Startseite verlinkt {path} (Fußbereich)")

    s, _, body, _ = get(base + "/diese-seite-gibt-es-nicht-pruefung/")
    line(s == 404, f"eine unbekannte Adresse antwortet mit 404 (erhalten: {s}). Eine 200 hier heißt, der Hoster liefert "
                   "für jede unbekannte Adresse die Startseite")

    s, _, body, _ = get(base + "/robots.txt")
    line(s == 200 and "Sitemap:" in body, "robots.txt wird ausgeliefert und nennt die Sitemap")

    s, _, body, _ = get(base + "/sitemap-index.xml")
    parts = re.findall(r"<loc>(.*?)</loc>", body)
    line(s == 200 and bool(parts), f"Sitemap-Index wird mit {len(parts)} Teil(en) ausgeliefert")
    urls = []
    for p in parts:
        p = base + "/" + p.rsplit("/", 1)[-1]
        _, _, b, _ = get(p); urls += re.findall(r"<loc>(.*?)</loc>", b)
    line(bool(urls), f"Sitemap führt {len(urls)} Adressen")
    if real_domain:
        # Die Sitemap muss auf die echte Domain zeigen, nie auf pages.dev – sonst indexiert Google die
        # pages.dev-Adresse mit (Doppelinhalt). Geprüft an den rohen <loc>-Hosts, Index-Teile und Adressen.
        foreign = sorted({urlparse(u).netloc for u in (parts + urls) if urlparse(u).netloc and urlparse(u).netloc != host})
        line(not foreign, f"alle Sitemap-Adressen zeigen auf {host}, nicht auf pages.dev"
                          + (f" – fremde Hosts gefunden: {foreign[:3]}" if foreign else ""))
    if a.expect_urls:
        line(len(urls) == a.expect_urls, f"Zahl der Adressen stimmt mit dem Startplan überein ({a.expect_urls})")

    # Je eine Stichprobe aus den beiden tiefen Seitentypen der deutschen Struktur: ein Eintrag
    # (/firma/<bundesland>/<stadt>/<slug>/) und eine Stadtseite (/verzeichnis/<bundesland>/<stadt>/).
    def path_of(u):
        return "/" + u.split("/", 3)[3] if u.count("/") >= 3 else "/"
    firma = [u for u in urls if "/firma/" in u][:1]
    stadt = [u for u in urls if "/verzeichnis/" in u and path_of(u).count("/") == 4][:1]
    bundesland = [u for u in urls if "/verzeichnis/" in u and path_of(u).count("/") == 3][:1]
    for u, was in [(firma and firma[0], "Eintragsseite unter /firma/"),
                   (stadt and stadt[0], "Stadtseite unter /verzeichnis/"),
                   (bundesland and bundesland[0], "Bundesland-Seite unter /verzeichnis/")]:
        if not u:
            line(False, f"keine {was} in der Sitemap gefunden (stimmt die URL-Struktur aus wiki/konventionen.md?)")
            continue
        local = base + path_of(u)
        s, _, b, _ = get(local)
        line(s == 200 and 'content="noindex' not in b, f"{was} antwortet mit 200 und ist indexierbar: {path_of(u)}")

    # Blättern ist noindex, aber follow: die Seite darf verlinkt bleiben, nur nicht in den Index.
    s, _, b, _ = get(base + "/verzeichnis/")
    rob = re.search(r'name="robots" content="([^"]*)"', b)
    content = (rob.group(1) if rob else "").lower()
    line(s == 200 and "noindex" in content and "nofollow" not in content,
         f"/verzeichnis/ wird ausgeliefert und ist noindex, follow (robots: '{content or 'nichts'}')")

    # Pflichtseiten nach deutschem Recht: erreichbar und mit Inhalt.
    for path, wort in (("/impressum/", "Impressum"), ("/datenschutz/", "Datenschutz")):
        s, _, b, _ = get(base + path)
        line(s == 200 and wort.lower() in b.lower(), f"{path} antwortet mit 200 und nennt {wort}")
    s, _, b, _ = get(base + "/datenschutz/")
    line("maps.googleapis.com" not in b and "maps.google.com/maps/embed" not in b,
         "/datenschutz/ lädt selbst keine Google-Karte (Karten erst nach Klick, wiki/konventionen.md)")

    for path in ("/eintrag-beanspruchen/", "/premium/"):
        s, _, b, _ = get(base + path)
        line(s == 200 and 'content="noindex' in b, f"{path} wird ausgeliefert und ist noindex")

    if real_domain:
        # www muss dauerhaft (301/308) auf die Hauptdomain umleiten, nicht selbst Inhalt ausliefern
        # (sonst zwei indexierbare Hosts). Geprüft, ohne der Weiterleitung zu folgen.
        st, loc = redirect_of(f"{scheme}://www.{host}/")
        loc_host = urlparse(loc).netloc if loc else ""
        line(st in (301, 308) and loc_host == host,
             f"www leitet dauerhaft auf die Hauptdomain um (Status {st or 'keine Antwort'} -> {loc or 'keine Location'})")
        # Gültiges, zum Hostnamen passendes TLS-Zertifikat (verifizierte Verbindung).
        tls_ok, info = tls_notafter(host)
        line(tls_ok, f"TLS-Zertifikat der Hauptdomain gültig und passend (gültig bis {info})" if tls_ok
                     else f"TLS-Zertifikat der Hauptdomain nicht verifizierbar: {info}")

    if a.pages_dev:
        s, h, _, _ = get(a.pages_dev.rstrip("/") + "/")
        line("noindex" in h.get("x-robots-tag", ""),
             f"die pages.dev-Adresse sendet X-Robots-Tag: noindex (erhalten: '{h.get('x-robots-tag', 'nichts')}')")

    print("\nAlle Prüfungen bestanden." if ok else "\nEtwas ist durchgefallen. Beheben, bevor der Dripfeed startet.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
