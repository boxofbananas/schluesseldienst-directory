#!/usr/bin/env python3
"""Ansprechpartner aus dem Impressum lesen — höflich, zwischengespeichert, nie geraten.

Der Rückweg für Anträge wird persönlich: „Guten Tag Herr Müller" statt „Guten Tag". Dieses
Skript ruft je Domain EINMAL das Impressum ab (üblich /impressum, sonst über den Link im
Fußbereich), liest den Namen der verantwortlichen natürlichen Person heraus (Inhaber,
Geschäftsführer, „vertreten durch") und legt ihn neben das Kontaktbuch. Es

  * sendet nichts, liefert nichts aus und rührt listings.csv NICHT an (nur Lesen),
  * ruft je Domain höchstens einmal ab, mit Pause dazwischen, und speichert das Ergebnis
    zwischen (output/<slug>/impressum-cache.json) — ein zweiter Lauf holt nur die noch
    offenen Domains nach,
  * rät NIE: kein Name aus der E-Mail-Adresse, aus dem Firmennamen oder aus Bewertungen.
    Ohne eindeutigen Fund bleiben die Namensfelder leer.

Ergebnisdatei (steht in .gitignore, personenbezogen):
  output/<slug>/kontakt-ansprechpartner.csv   eintrag_slug, vorname, nachname, fundstelle, abrufdatum

    # Probelauf: die ersten 30 noch offenen Domains, zehn Treffer mit Fundstelle zeigen
    python3 scripts/impressum.py --limit 30 --zeige 10

    # den Rest nachholen (nutzt den Zwischenspeicher, nur offene Domains)
    python3 scripts/impressum.py

    # nur Zahlen, nichts abrufen (liest den Zwischenspeicher)
    python3 scripts/impressum.py --stand

Nur Zahlen gehen in einen Bericht: gefunden, nicht gefunden, nicht abrufbar. Namen und
Adressen bleiben in der gitignorierten Datei.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import ssl

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)

from verkauf import WURZEL, truthy, fehler, finde_verzeichnis, lade_csv, heute

csv.field_size_limit(10**9)

AP_FELDER = ["eintrag_slug", "vorname", "nachname", "fundstelle", "abrufdatum"]

# Höflicher, neutraler Client-Name ohne Projekt-/Personenbezug.
UA = "Mozilla/5.0 (compatible; Impressum-Lesebot/1.0)"

# Rollen-/Füllwörter, die vor einem Namen stehen dürfen und entfernt werden.
FUELL = {"herr", "herrn", "frau", "den", "die", "der", "durch", "vertreten", "geschäftsführer",
         "geschäftsführerin", "geschäftsführung", "geschäftsführende", "inhaber", "inhaberin",
         "eigentümer", "eigentümerin", "betreiber", "betreiberin", "gesellschafter", "i.v.",
         "ppa.", "dipl.-ing.", "und"}
# Titel, die zum Namen gehören, aber nicht Vor-/Nachname sind.
TITEL = re.compile(r"^(dr\.|prof\.|dipl\.-?\w+\.?|mag\.|ing\.|m\.a\.|b\.a\.|m\.sc\.|b\.sc\.|ll\.m\.|med\.)$", re.I)
# Firmen-/Rechtsformkennzeichen — taucht eins im Namenssegment auf, ist es kein Personenname.
FIRMA = re.compile(r"\b(gmbh|mbh|ug|haftungsbeschränkt|ag|kg|ohg|gbr|kgaa|e\.?\s?k\.?|e\.?\s?v\.?|"
                   r"ltd|inc|co\.|&\s?co|gesellschaft|unternehmergesellschaft)\b", re.I)
# Ein Namenstoken: großgeschrieben, Umlaute und Bindestriche erlaubt.
TOKEN = re.compile(r"[A-ZÄÖÜ][A-Za-zÄÖÜäöüß'’]*(?:-[A-ZÄÖÜ][A-Za-zÄÖÜäöüß'’]*)*")
PARTIKEL = {"von", "van", "vom", "zu", "de", "da", "di"}
# Wörter, die nie Teil eines Personennamens sind — Adresse, Überschriften, Amts- und Firmensprache,
# Artikel/Pronomen. Ein Kandidat mit einem dieser Wörter wird verworfen (lieber leer als geraten).
STOPWORT = {
    "straße", "strasse", "str", "weg", "platz", "allee", "ring", "gasse", "chaussee", "damm",
    "ufer", "hof", "steig", "pfad", "berg", "feld",
    "unser", "unsere", "angebot", "angebote", "impressum", "kontakt", "startseite", "start",
    "leistungen", "leistung", "service", "dienstleistungen", "home", "menü", "navigation",
    "plattform", "kommission", "eu", "europäische", "europäischen", "online", "streitbeilegung",
    "verbraucherschlichtungsstelle", "telefon", "telefax", "fax", "email", "mail", "webseite",
    "website", "internet", "inhalt", "inhalte", "sitz", "amtsgericht", "registergericht",
    "steuernummer", "umsatzsteuer", "verantwortlich", "vertretungsberechtigt", "vertreten",
    "firma", "betrieb", "fachbetrieb", "meisterbetrieb", "schlüsseldienst", "sicherheitstechnik",
    "rollladen", "rolladen", "bauelemente", "notdienst", "aufsperrdienst",
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einer",
    "wir", "sie", "ihr", "ihre", "für", "und", "oder", "zur", "zum", "mit", "bei", "nach", "aus",
    "herr", "frau", "herrn", "geschäftsführer", "geschäftsführerin", "inhaber", "inhaberin",
}

# Labels in Prüf-Reihenfolge: Geschäftsführer/Vertretung vor Inhaber vor „verantwortlich".
LABELS = [
    r"vertreten\s+durch",
    r"vertretungsberechtigt\w*",
    r"gesch[aä]ftsf[uü]hr\w*",
    r"inhaber(?:in)?",
    r"eigent[uü]mer(?:in)?",
    r"einzelunternehmer(?:in)?",
    r"verantwortlich(?:e[rn]?)?(?:\s+(?:i\.?\s?s\.?\s?d\.?|im\s+sinne|f[uü]r\s+den\s+inhalt))?",
]


def domain_von(website):
    w = (website or "").strip()
    if not w:
        return ""
    w = re.sub(r"^\s*https?://", "", w, flags=re.I)
    w = w.split("/")[0].split("?")[0].strip().lower()
    w = re.sub(r"^www\.", "", w)
    return w


# Branchen-/Rechtsform-/Füllwörter, die einen Betrieb nicht von einem anderen unterscheiden.
GENERISCH = {
    "schluesseldienst", "schluesseldienste", "schluessel", "schluesselnotdienst", "schliesstechnik",
    "schliessanlagen", "sicherheitstechnik", "sicherheit", "notdienst", "aufsperrdienst", "aufsperren",
    "tueroeffnung", "einbruchschutz", "service", "key", "keys", "lock", "meisterbetrieb", "fachbetrieb",
    "meister", "team", "profi", "express", "blitz", "zentrale", "gmbh", "ug", "kg", "ohg", "gbr", "ag",
    "co", "ek", "ev", "inh", "inhaber", "und", "der", "die", "das", "fuer", "std", "stunden",
}


def _norm(s):
    s = (s or "").lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _tokens(s):
    return [t for t in _norm(s).split() if len(t) >= 3]


def gehoert_zum_betrieb(name, domain, text, nachname, stadt, land):
    """Gehört das Impressum erkennbar dem gelisteten Betrieb? Nur dann wird der Name übernommen.

    Positivsignale (eins reicht): ein unterscheidender Namensteil steckt in der Domain; mindestens
    zwei Namensteile (auch Branche/Ort) stecken in der Domain — die Domain registriert der Betrieb
    selbst; der Nachname steckt in Domain oder Firmenname; ein unterscheidender Namensteil (ohne Ort)
    steht im Impressum-Kopf. Agentur-, Portal- oder Fremdimpressen erfüllen keins -> kein Name.
    """
    flat = _norm(domain).replace(" ", "")
    btok = _tokens(name)
    ortset = set(_tokens(stadt)) | set(_tokens(land))
    distinct = [t for t in btok if t not in GENERISCH]
    distinct_ohne_ort = [t for t in distinct if t not in ortset]
    # Domain: unterscheidender Teil, oder >= zwei Namensteile (auch generische/Ort)
    if any(t in flat for t in distinct):
        return True
    if sum(1 for t in set(btok) if t in flat) >= 2:
        return True
    # Nachname in Domain oder im Firmennamen
    nn = _norm(nachname).replace(" ", "")
    if len(nn) >= 3 and (nn in flat or nn in _norm(name).replace(" ", "")):
        return True
    # Impressum-Kopf: unterscheidender Teil OHNE Ort (ein Ort kommt in jeder Adresse vor)
    kopf = _norm(text[:600])
    if any(t in kopf for t in distinct_ohne_ort):
        return True
    return False


def hole(url, pause):
    """Einen Abruf, höflich. Gibt (text, endgueltige_url) oder (None, None)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # viele Handwerker-Seiten haben kaputte Zertifikatsketten
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
            ct = (r.headers.get("Content-Type") or "").lower()
            if "html" not in ct and "text" not in ct and ct:
                return None, None
            roh = r.read(2_000_000)  # 2 MB reichen für ein Impressum
            final = r.geturl()
    except (urllib.error.HTTPError, urllib.error.URLError, ssl.SSLError, TimeoutError,
            ConnectionError, UnicodeError, ValueError, OSError):
        return None, None
    finally:
        time.sleep(pause)
    # Zeichensatz bestimmen
    enc = None
    m = re.search(rb'charset=["\']?\s*([\w-]+)', roh[:4000], re.I)
    if m:
        try:
            enc = m.group(1).decode("ascii")
        except Exception:
            enc = None
    for versuch in (enc, "utf-8", "cp1252", "latin-1"):
        if not versuch:
            continue
        try:
            return roh.decode(versuch), final
        except (LookupError, UnicodeDecodeError):
            continue
    return roh.decode("utf-8", "replace"), final


def zu_text(roh_html):
    """HTML grob zu Text mit erhaltenen Zeilenumbrüchen (für Label/Wert in getrennten Zeilen)."""
    s = re.sub(r"(?is)<script.*?</script>", " ", roh_html)
    s = re.sub(r"(?is)<style.*?</style>", " ", s)
    s = re.sub(r"(?i)<\s*br\s*/?\s*>", "\n", s)
    s = re.sub(r"(?i)</\s*(p|div|li|tr|h[1-6]|td|section|article)\s*>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return "\n".join(z.strip() for z in s.splitlines())


def ist_impressum(text):
    """Trägt die Seite tatsächlich ein Impressum (nicht nur einen Menülink darauf)?"""
    t = text.lower()
    if re.search(r"angaben\s+gem[aä][ßs]\s+§\s*5|§\s*5\s+(tmg|ddg)|§\s*55\s+rstv", t):
        return True
    treffer = sum(1 for lab in (r"vertreten\s+durch", r"gesch[aä]ftsf[uü]hr", r"inhaber",
                                r"umsatzsteuer|ust-?idnr|ust\.-?id", r"handelsregister|hrb|hra",
                                r"verantwortlich") if re.search(lab, t))
    return treffer >= 2


def finde_impressum_link(roh_html, basis):
    """Sucht im HTML einen Link, dessen Ziel oder Text 'impressum' enthält."""
    for m in re.finditer(r'(?is)<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', roh_html):
        href, text = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        if "impressum" in href.lower() or "impressum" in text.lower():
            return urllib.parse.urljoin(basis, href.strip())
    return None


def _grund_fuer_name(tokens):
    """tokens: bereinigte Wörter. Gibt (vorname, nachname) für eine klare Person, sonst None.

    Streng: lieber nichts als ein falscher Name. Ein Stoppwort, ein durchgehend
    großgeschriebenes Wort oder eine untypische Token-Zahl verwirft den Kandidaten.
    """
    namen = [t for t in tokens if not TITEL.match(t)]  # Titel gehören nicht in Vor-/Nachname
    namen = [t for t in namen if len(t.strip(".'’")) >= 2]  # Einzelbuchstaben/Initialen weg ("Klaus D Mapara" -> "Klaus Mapara")
    if not (2 <= len(namen) <= 4):
        return None
    echte = [t for t in namen if t.lower() not in PARTIKEL]
    if not (2 <= len(echte) <= 3):
        return None
    for t in namen:
        kern = t.strip(".'’")
        if kern.lower() in STOPWORT:
            return None
        if len(kern) >= 2 and kern.isupper():  # „FACHBETRIEB", „ROLLADEN" — kein Name
            return None
        if any(c.isdigit() for c in t):
            return None
    vorname = namen[0]
    if TITEL.match(vorname) or not TOKEN.fullmatch(vorname) or len(vorname.strip(".")) < 2:
        return None
    nachname = " ".join(namen[1:])
    # der Nachname braucht mindestens ein echtes Wort (nicht nur eine Initiale/Partikel)
    if not any(len(t.strip(".")) >= 2 and t.lower() not in PARTIKEL for t in namen[1:]):
        return None
    return vorname, nachname


def namen_aus_segment(segment):
    """Aus einem Textstück hinter einem Label den ersten Personennamen ziehen. Nie raten."""
    # bis zum ersten Trenner (mehrere Personen -> die erste)
    stueck = re.split(r"[,;/\n]| und | & | sowie ", segment, maxsplit=1)[0]
    stueck = stueck.strip(" .:-\t")
    if not stueck or FIRMA.search(stueck):
        # Firmenname — es sei denn, ein „… durch Herrn X Y" steht darin
        m = re.search(r"(?:durch|,)\s+(?:herrn?|frau)\s+(.+)$", segment, re.I)
        if not m:
            return None
        stueck = re.split(r"[,;/\n]| und | & ", m.group(1), maxsplit=1)[0].strip(" .:-\t")
        if FIRMA.search(stueck):
            return None
    roh_tokens = stueck.split()
    # führende Füllwörter weg
    while roh_tokens and roh_tokens[0].lower().strip(".:") in FUELL:
        roh_tokens.pop(0)
    # maximalen führenden Lauf aus Namenstoken/Titeln/Partikeln nehmen
    gesammelt = []
    for t in roh_tokens:
        tl = t.lower().strip(".:")
        if TITEL.match(t):
            gesammelt.append(t.strip(",;"))
            continue
        if t.lower() in PARTIKEL and gesammelt:
            gesammelt.append(t)
            continue
        if TOKEN.fullmatch(t.strip(",;.")):
            gesammelt.append(t.strip(",;."))
            if len(gesammelt) >= 4:
                break
        else:
            break
    return _grund_fuer_name(gesammelt)


def lies_namen(text):
    """Impressum-Text -> (vorname, nachname) oder (None, None). Labels in Prüf-Reihenfolge."""
    zeilen = text.splitlines()
    tief = text  # ganzer Text für Zeilen-Suche
    for label in LABELS:
        pat = re.compile(r"(?i)\b(" + label + r")\b\s*[:\-–]?\s*(.*)")
        for i, z in enumerate(zeilen):
            m = pat.search(z)
            if not m:
                continue
            rest = m.group(2).strip()
            kandidaten = []
            if rest:
                kandidaten.append(rest)
            # Wert kann in der/den Folgezeile(n) stehen
            for j in range(i + 1, min(i + 3, len(zeilen))):
                if zeilen[j].strip():
                    kandidaten.append(zeilen[j].strip())
            for seg in kandidaten:
                paar = namen_aus_segment(seg)
                if paar:
                    return paar
    return None, None


def hol_impressum(dom, pause):
    """Eine Domain höflich abklappern: /impressum direkt, sonst EIN Startseiten-Abruf + Fußlink.

    Reiner Abruf — speichert den Impressum-TEXT (das Namenlesen passiert offline aus dem
    Zwischenspeicher). Gibt {status_abruf, fundstelle, text}.
      status_abruf: ok (Impressum-Seite gefunden) | kein_impressum (erreichbar, keine) |
                    nicht_abrufbar (Domain antwortet nicht).
    """
    erreichbar = False
    # 1) der übliche Weg: /impressum direkt (https, sonst http)
    for schema in ("https://", "http://"):
        url = schema + dom + "/impressum"
        roh, final = hole(url, pause)
        if roh is not None:
            erreichbar = True
            t = zu_text(roh)
            if ist_impressum(t):
                return {"status_abruf": "ok", "fundstelle": final or url, "text": t[:50000]}
            break  # Seite da, aber kein Impressum -> über die Startseite suchen
    # 2) Startseite holen, Link im Fußbereich suchen, diesen einmal abrufen
    for schema in ("https://", "http://"):
        roh, final = hole(schema + dom + "/", pause)
        if roh is None:
            continue
        erreichbar = True
        link = finde_impressum_link(roh, final or (schema + dom + "/"))
        if link:
            roh2, final2 = hole(link, pause)
            if roh2 is not None:
                t = zu_text(roh2)
                if ist_impressum(t):
                    return {"status_abruf": "ok", "fundstelle": final2 or link, "text": t[:50000]}
        return {"status_abruf": "kein_impressum", "fundstelle": final or (schema + dom + "/"), "text": ""}
    return {"status_abruf": "nicht_abrufbar", "fundstelle": "", "text": ""}


def extrahiere(e):
    """(status, vorname, nachname) aus einem Zwischenspeicher-Eintrag. Offline, aus dem Text.

    status: gefunden | nicht_gefunden | nicht_abrufbar.
    """
    if e.get("status_abruf") == "nicht_abrufbar":
        return "nicht_abrufbar", "", ""
    if e.get("status_abruf") != "ok" or not e.get("text"):
        return "nicht_gefunden", "", ""
    vn, nn = lies_namen(e["text"])
    return ("gefunden", vn, nn) if vn else ("nicht_gefunden", "", "")


def lade_cache(pfad):
    if os.path.isfile(pfad):
        try:
            return json.load(open(pfad, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def schreibe_cache(pfad, cache):
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0, sort_keys=True)
    os.replace(tmp, pfad)


def schreibe_ausgabe(pfad, rows_by_slug):
    tmp = pfad + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=AP_FELDER)
        w.writeheader()
        for slug in sorted(rows_by_slug):
            w.writerow(rows_by_slug[slug])
    os.replace(tmp, pfad)


def main():
    ap = argparse.ArgumentParser(description="Ansprechpartner aus dem Impressum lesen.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=0, help="nur so viele noch offene Domains abrufen (0 = alle)")
    ap.add_argument("--zeige", type=int, default=0, help="so viele Ergebnisse mit Fundstelle am Ende zeigen")
    ap.add_argument("--pause", type=float, default=1.5, help="Pause zwischen Abrufen in Sekunden (Vorgabe 1,5)")
    ap.add_argument("--stand", action="store_true", help="nur Zahlen aus dem Zwischenspeicher, nichts abrufen")
    ap.add_argument("--neu-lesen", dest="neu_lesen", action="store_true",
                    help="Namen aus dem gespeicherten Text neu lesen, ohne abzurufen (nach Regeländerung)")
    ap.add_argument("--neu", action="store_true", help="Zwischenspeicher ignorieren und alles neu abrufen")
    ap.add_argument("--verzeichnis", help="Build-Verzeichnis (Vorgabe: einziges unter output/*/site/)")
    a = ap.parse_args()

    verzeichnis = finde_verzeichnis(a.verzeichnis)
    csv_pfad = os.path.join(verzeichnis, "site", "src", "data", "listings.csv")
    cache_pfad = os.path.join(verzeichnis, "impressum-cache.json")
    aus_pfad = os.path.join(verzeichnis, "kontakt-ansprechpartner.csv")

    _, rows = lade_csv(csv_pfad)

    def hat_email(r):
        return any((r.get(c) or "").strip() for c in ("email_1", "email_2", "email_3"))

    # Universum: anschreibbar = Website vorhanden, nicht owned UND E-Mail-Adresse vorhanden
    # (ohne E-Mail können wir den Betrieb nicht anschreiben — kein Zweck, den Namen zu sammeln).
    kandidaten = [r for r in rows if (r.get("website") or "").strip() and not truthy(r.get("owned"))
                  and hat_email(r)]
    dom_zu_slugs = {}
    slug_info = {}
    for r in kandidaten:
        d = domain_von(r.get("website"))
        if d:
            dom_zu_slugs.setdefault(d, []).append(r["slug"])
            slug_info[r["slug"]] = (r.get("name", ""), r.get("city", ""), r.get("state", ""))
    domains = sorted(dom_zu_slugs)

    # Domains, die MEHRERE gelistete Betriebe nutzen — über ALLE Zeilen mit Website gezählt.
    # Eine geteilte Domain (Portal/Kette) bekommt keinen Namen zugeordnet.
    dom_gesamt = {}
    for r in rows:
        if (r.get("website") or "").strip():
            d = domain_von(r.get("website"))
            if d:
                dom_gesamt[d] = dom_gesamt.get(d, 0) + 1
    geteilt = {d for d, c in dom_gesamt.items() if c > 1}

    cache = {} if a.neu else lade_cache(cache_pfad)

    def ergebnis_je_slug():
        """slug -> (status, vorname, nachname, fundstelle, abrufdatum, grund).

        status: gefunden | nicht_gefunden | nicht_abrufbar | offen.
        grund (nur zur Info): geteilt | fremd | '' .
        """
        out = {}
        for d, slugs in dom_zu_slugs.items():
            e = cache.get(d)
            for slug in slugs:
                if d in geteilt:  # Portal/Kette: kein Name, gar nicht erst abgerufen
                    out[slug] = ("nicht_gefunden", "", "", "", "", "geteilt")
                    continue
                if not e:
                    out[slug] = ("offen", "", "", "", "", "")
                    continue
                st, vn, nn = extrahiere(e)
                fund, dat = e.get("fundstelle", ""), e.get("abrufdatum", "")
                if st != "gefunden":
                    out[slug] = (st, "", "", fund, dat, "")
                    continue
                name, stadt, land = slug_info.get(slug, ("", "", ""))
                if not gehoert_zum_betrieb(name, d, e.get("text", ""), nn, stadt, land):
                    out[slug] = ("nicht_gefunden", "", "", fund, dat, "fremd")
                else:
                    out[slug] = ("gefunden", vn, nn, fund, dat, "")
        return out

    def zaehle(erg):
        g = sum(1 for v in erg.values() if v[0] == "gefunden")
        ng = sum(1 for v in erg.values() if v[0] == "nicht_gefunden")
        na = sum(1 for v in erg.values() if v[0] == "nicht_abrufbar")
        noch = sum(1 for v in erg.values() if v[0] == "offen")
        geteilt_n = sum(1 for v in erg.values() if v[5] == "geteilt")
        fremd_n = sum(1 for v in erg.values() if v[5] == "fremd")
        return g, ng, na, noch, geteilt_n, fremd_n

    def drucke_zahlen(erg):
        g, ng, na, noch, gn, fn = zaehle(erg)
        print(f"Anschreibbare Einträge (mit E-Mail): {len(erg)} auf {len(domains)} Domains")
        print(f"  Name gefunden        {g:>6}")
        print(f"  nicht gefunden       {ng:>6}  (davon fremdes Impressum {fn}, geteilte Domain {gn})")
        print(f"  Domain nicht abrufbar{na:>6}")
        print(f"  noch offen           {noch:>6}")

    if a.stand:
        drucke_zahlen(ergebnis_je_slug())
        return

    # Geteilte Domains (Portal/Kette) werden gar nicht erst abgerufen — sie bekommen keinen Namen.
    offen = [d for d in domains if d not in cache and d not in geteilt]
    zu_holen = [] if a.neu_lesen else (offen[:a.limit] if a.limit else offen)
    quelle = "nur neu lesen (kein Abruf)" if a.neu_lesen else \
        f"{len(zu_holen)} abrufen (Pause {a.pause}s je Abruf, ein Abruf je Domain)"
    print(f"{len(domains)} Domains ({len(kandidaten)} Einträge mit E-Mail; {len(geteilt & set(domains))} "
          f"geteilte Domains übersprungen), {len(offen)} offen. Dieser Lauf: {quelle}.", flush=True)
    for n, d in enumerate(zu_holen, 1):
        cache[d] = hol_impressum(d, a.pause)
        cache[d]["abrufdatum"] = heute()
        if n % 25 == 0 or n == len(zu_holen):
            schreibe_cache(cache_pfad, cache)
            print(f"  {n}/{len(zu_holen)} abgerufen ...", flush=True)
    schreibe_cache(cache_pfad, cache)

    erg = ergebnis_je_slug()
    rows_by_slug = {s: {"eintrag_slug": s, "vorname": v[1], "nachname": v[2],
                        "fundstelle": v[3], "abrufdatum": v[4]} for s, v in erg.items()}
    schreibe_ausgabe(aus_pfad, rows_by_slug)

    print()
    drucke_zahlen(erg)
    print(f"Ergebnis je Eintrag: {aus_pfad}")

    if a.zeige:
        holset = set(zu_holen)
        slug_dom = {s: d for d, slugs in dom_zu_slugs.items() for s in slugs}
        kand = list(erg.items())
        if holset:  # nur Einträge dieses Laufs zeigen
            kand = [(s, v) for s, v in kand if slug_dom.get(s) in holset]
        kand.sort(key=lambda sv: sv[1][0] != "gefunden")  # Treffer zuerst
        print(f"\n{min(a.zeige, len(kand))} Ergebnisse (Treffer zuerst):")
        for s, v in kand[:a.zeige]:
            name = (v[1] + " " + v[2]).strip() or "—"
            zusatz = f" ({v[5]})" if v[5] else ""
            print(f"  [{v[0]:<14}] {name:<26} {v[3] or s}{zusatz}")


if __name__ == "__main__":
    main()
