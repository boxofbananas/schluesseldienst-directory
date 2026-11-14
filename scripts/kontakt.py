#!/usr/bin/env python3
"""Kontaktbuch und Versand-Export für die Ansprache der Betriebe — anhängen, nie überschreiben.

Der Rückweg für Anträge beginnt mit dem Anschreiben: „Sie haben einen Eintrag in meinem
Verzeichnis." Dieses Skript hält jeden Kontakt fest, führt eine Sperrliste, sagt, wer noch nie
angesprochen wurde, macht aus den offenen Einträgen eine versandfertige CSV (je Kampagne, mit
Obergrenze) und liest die Ergebnisse einer Versandplattform zurück. Es ändert **keinen** Eintrag
und rührt listings.csv nicht an (nur Lesen); es **versendet nichts**, baut und liefert nichts aus.

Vier anhängende Bücher neben der Build-CSV (alle personenbezogen/adressbehaftet außer dem
Hauptbuch sind gitignoriert):
  output/<slug>/kontakt-hauptbuch.csv   datum, eintrag_slug, weg, ergebnis, notiz
  output/<slug>/kontakt-sperrliste.csv  datum, eintrag_slug, grund
  output/<slug>/kontakt-kampagnen.csv   datum, kampagne, eintrag_slug, status
  output/<slug>/kontakt-ansprechpartner.csv  (von impressum.py: slug, vorname, nachname, …)

    # einen Kontakt festhalten
    python3 scripts/kontakt.py eintragen --slug <slug> --weg telefon|email|formular \\
        --ergebnis "erreicht, Antrag zugesagt" [--notiz "…"] [--datum JJJJ-MM-TT]

    # einen Eintrag sperren (nie wieder als „noch zu kontaktieren" / im Export zeigen)
    python3 scripts/kontakt.py sperren --slug <slug> [--grund "bittet um Ruhe"]

    # wer wurde noch nie kontaktiert (ohne eigene Betriebe, ohne Gesperrte)
    python3 scripts/kontakt.py --offen [--bundesland "Baden-Württemberg"] [--stadt Mannheim] [--alle]

    # versandfertige CSV einer Kampagne schreiben (säubert Adressen, prüft MX, dedupliziert,
    # nur Kernbetriebe, nur Städte ohne Garantie/bezahlten Platz; Obergrenze --limit)
    python3 scripts/kontakt.py exportieren --kampagne nrw-pilot-1 --limit 100 \\
        [--bundesland "Nordrhein-Westfalen"] [--stadt Köln] [--out <pfad>] [--probe]

    # Werte des Exports gegen die gebaute Seite prüfen (platz, anzahl, Bewertung, Telefon)
    python3 scripts/kontakt.py pruefen [--anzahl 20] [--seed 0]

    # Ergebnis-CSV einer Versandplattform zurücklesen
    python3 scripts/kontakt.py importieren --kampagne nrw-pilot-1 --datei ergebnisse.csv \\
        [--spalte-slug slug] [--spalte-email email] [--spalte-status status] [--spalte-datum datum]

    # Zahlen je Status; mit --kampagne die Zahlen einer Kampagne
    python3 scripts/kontakt.py --stand [--kampagne nrw-pilot-1]

Alle Bücher werden nur **angehängt** — eine Korrektur ist eine neue Zeile, nie das Überschreiben
einer alten.

Spaltenformat der Import-Datei (Punkt: Versandplattform → Kontaktbuch)
---------------------------------------------------------------------
Eine Zeile je Empfänger. Erkannt werden (Groß/Kleinschreibung egal), sonst mit --spalte-… setzen:
  Eintrag   : slug | eintrag_slug | id            (ODER die E-Mail, siehe unten)
  E-Mail    : email | email_1 | e-mail | mail | empfaenger | recipient | to
  Status    : status | event | result | ergebnis
  Datum     : datum | date | timestamp | zeit     (optional; Vorgabe heute)
Zuordnung über den Slug, sonst über die E-Mail (muss genau einen Eintrag treffen; trifft sie
mehrere, wird die Zeile als unklar gemeldet, nicht geraten).
Status-Werte (Synonyme werden abgebildet, Unbekanntes wird gemeldet, nie geraten):
  gesendet      = sent, delivered, zugestellt, versendet, ok
  geantwortet   = replied, responded, antwort
  unzustellbar  = bounced, bounce, hard_bounce, undeliverable, failed
  abgemeldet    = unsubscribed, unsubscribe, opt-out, complaint, spam
„abgemeldet" und „unzustellbar" kommen zusätzlich auf die Sperrliste.
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
if HIER not in sys.path:
    sys.path.insert(0, HIER)

from verkauf import WURZEL, truthy, fehler, finde_verzeichnis, lade_csv, finde_zeile, _zeige_treffer, heute

csv.field_size_limit(10**9)

HB_FELDER = ["datum", "eintrag_slug", "weg", "ergebnis", "notiz"]
SP_FELDER = ["datum", "eintrag_slug", "grund"]
KAMP_FELDER = ["datum", "kampagne", "eintrag_slug", "status"]
WEGE = ["telefon", "email", "formular"]

# Spalten der versandfertigen Export-Datei (gitignoriert; enthält Adressen, nur zum Anschreiben).
# `variante` wählt den Mailtext (platz-Aufhänger oder telefon-Aufhänger), `stand` hält den
# Exporttag fest (die Plätze gelten nur bis zum nächsten Neubau).
EXPORT_FELDER = ["eintrag_slug", "kampagne", "name", "state", "city", "eintrag_url",
                 "platz", "anzahl", "bewertung", "bewertungen", "hat_bewertung", "telefon",
                 "email", "vorname", "nachname", "anrede", "variante", "stand"]

# Welche Mail-Variante ein Eintrag bekommt: den Platz-Aufhänger („Platz N von M") nur, wenn der
# Eintrag eine Bewertung hat UND die Stadtseite mindestens so viele Einträge führt — sonst wirkt
# die Reihung nicht. Darunter der Telefon-Aufhänger. Fehlt dann das Telefon, fällt der Eintrag weg.
PLATZ_HOOK_MIN_ANZAHL = 5

# Nur Einträge mit bestätigter Kernarbeit kommen in den Versand — fremde Gewerbe (Schreiner,
# Schuhmacher, Metallbauer), die nur über die Kategorie hereinkamen, nicht.
KERN_SPALTEN = ["schluesseldienst_kern", "tueroeffnung"]

# Statuswerte der Kampagne (nach „vorgesehen" kommen die Rückmeldungen der Plattform).
VERSAND_STATUS = ["vorgesehen", "gesendet", "geantwortet", "abgemeldet", "unzustellbar"]
# Status zur Sperrung.
STATUS_SPERRT = {"abgemeldet", "unzustellbar"}

# Freemailer bleiben drin (Punkt 1: „Freemailer bleiben drin"); sie sind nie ein Portal/Kette.
FREEMAILER = {
    "gmail.com", "googlemail.com", "web.de", "gmx.de", "gmx.net", "gmx.com", "gmx.at",
    "t-online.de", "online.de", "yahoo.com", "yahoo.de", "ymail.com", "outlook.com",
    "outlook.de", "hotmail.com", "hotmail.de", "live.com", "live.de", "msn.com",
    "aol.com", "aol.de", "icloud.com", "me.com", "mac.com", "mail.de", "freenet.de",
    "arcor.de", "posteo.de", "mailbox.org", " gmx.ch".strip(), "bluewin.ch", "protonmail.com",
    "proton.me", "unitybox.de", "o2online.de", "vodafone.de", "kabelmail.de", "ewe.net",
}
# Eine E-Mail-Adresse, die bei so vielen verschiedenen Einträgen steht, ist eine Zentral-/
# Sammeladresse (Portal/Kette), kein einzelner Betrieb → ganz aussortieren. Freemailer ausgenommen.
ZENTRAL_SCHWELLE = 5

EMAIL_RX = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

STATUS_MAP = {
    "gesendet": "gesendet", "sent": "gesendet", "delivered": "gesendet", "zugestellt": "gesendet",
    "versendet": "gesendet", "ok": "gesendet", "erfolgreich": "gesendet",
    "geantwortet": "geantwortet", "replied": "geantwortet", "reply": "geantwortet",
    "responded": "geantwortet", "antwort": "geantwortet", "response": "geantwortet",
    "unzustellbar": "unzustellbar", "bounced": "unzustellbar", "bounce": "unzustellbar",
    "hardbounce": "unzustellbar", "hard_bounce": "unzustellbar", "soft_bounce": "unzustellbar",
    "undeliverable": "unzustellbar", "failed": "unzustellbar", "fehler": "unzustellbar",
    "abgemeldet": "abgemeldet", "unsubscribed": "abgemeldet", "unsubscribe": "abgemeldet",
    "optout": "abgemeldet", "opt-out": "abgemeldet", "opt_out": "abgemeldet",
    "complaint": "abgemeldet", "komplaint": "abgemeldet", "spam": "abgemeldet", "beschwerde": "abgemeldet",
}

SP_SLUG = {"slug", "eintrag_slug", "id", "eintrag"}
SP_EMAIL = {"email", "email_1", "e-mail", "mail", "empfaenger", "empfänger", "recipient", "to", "adresse"}
SP_STATUS = {"status", "event", "result", "ergebnis", "zustand"}
SP_DATUM = {"datum", "date", "timestamp", "zeit", "time"}


# --------------------------------------------------------------------------- Helfer
def ist_kernbetrieb(r):
    """Ist „Schlüsseldienst" oder „Türöffnung" als Merkmal bestätigt (wahr/true)?"""
    return any(truthy(r.get(c)) for c in KERN_SPALTEN)


# Platzhalter-Namen, die manche Impressen aus einer Vorlage übrig lassen (Muster-Impressum). Sie
# dürfen nie zu „Hallo Max Mustermann," werden; der Export fängt sie am Rand ab und grüßt neutral.
PLATZHALTER_NACHNAMEN = {"mustermann", "mustermann", "musterfrau", "doe", "beispiel", "example"}


def ist_platzhalter(vorname, nachname):
    return (nachname or "").strip().lower() in PLATZHALTER_NACHNAMEN


def baue_anrede(vorname, nachname):
    """Mit Namen „Hallo Vorname Nachname," — ohne eindeutigen Namen „Guten Tag,". Nie geraten.
    Platzhalter-Namen aus Muster-Impressen (Max Mustermann) gelten als kein Name."""
    if vorname and nachname and not ist_platzhalter(vorname, nachname):
        return f"Hallo {vorname} {nachname},"
    return "Guten Tag,"


def score(r):
    """Dieselbe Rangzahl wie die Website (load.mjs): Bewertung × log10(Anzahl+1)."""
    try:
        rating = float(str(r.get("rating") or "0").replace(",", "."))
    except ValueError:
        rating = 0.0
    try:
        reviews = int(float(str(r.get("reviews") or "0").replace(",", ".")))
    except ValueError:
        reviews = 0
    return rating * math.log10(reviews + 1)


def norm_email(s):
    return (s or "").strip().lower()


def haupt_email(r):
    """Hauptadresse: email_1, sonst die nächste gefüllte."""
    for c in ("email_1", "email_2", "email_3"):
        v = (r.get(c) or "").strip()
        if v:
            return v
    return ""


def norm_bundesland(s):
    return (s or "").strip().lower()


def lade(pfad, felder=None):
    if not os.path.isfile(pfad):
        return []
    with open(pfad, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def haenge(pfad, felder, zeilen):
    """Hängt eine oder mehrere Zeilen an; schreibt den Kopf nur bei neuer Datei."""
    if isinstance(zeilen, dict):
        zeilen = [zeilen]
    neu = not os.path.isfile(pfad)
    with open(pfad, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        if neu:
            w.writeheader()
        for z in zeilen:
            w.writerow(z)


def lade_ansprechpartner(pfad):
    """slug -> (vorname, nachname) aus kontakt-ansprechpartner.csv (von impressum.py). Leer, wenn fehlt."""
    out = {}
    for z in lade(pfad):
        out[z.get("eintrag_slug")] = ((z.get("vorname") or "").strip(), (z.get("nachname") or "").strip())
    return out


# --------------------------------------------------------------------------- Kampagnen
def kampagnen_je_slug(kamp):
    """{kampagne: {slug: letzter_status}} — die zuletzt angehängte Zeile je (kampagne, slug) gewinnt."""
    out = {}
    for z in kamp:
        k = z.get("kampagne") or ""
        out.setdefault(k, {})[z.get("eintrag_slug")] = z.get("status") or ""
    return out


def kampagnen_start(kamp):
    """{kampagne: frühestes datum einer 'vorgesehen'-Zeile}."""
    out = {}
    for z in kamp:
        if z.get("status") == "vorgesehen":
            k = z.get("kampagne") or ""
            d = z.get("datum") or ""
            if d and (k not in out or d < out[k]):
                out[k] = d
    return out


def alle_vorgesehenen(kamp):
    """Jeder Slug, der in irgendeiner Kampagne schon exportiert (vorgesehen) wurde."""
    return {z.get("eintrag_slug") for z in kamp if z.get("eintrag_slug")}


# --------------------------------------------------------------------------- MX-Prüfung
def lade_mx_cache(pfad):
    if os.path.isfile(pfad):
        try:
            return json.load(open(pfad, encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}


def speichere_mx_cache(pfad, cache):
    try:
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except OSError:
        pass


def _dig(typ, domain):
    try:
        r = subprocess.run(["dig", "+short", typ, domain], capture_output=True, text=True, timeout=10)
        return [z for z in r.stdout.splitlines() if z.strip()]
    except (OSError, subprocess.TimeoutExpired):
        return []


def hat_mailserver(domain, cache):
    """True, wenn die Domain einen MX-Eintrag hat; sonst RFC-5321-Rückfall auf A/AAAA. Ergebnis
    wird je Domain zwischengespeichert. Ohne MX und ohne A/AAAA gilt die Domain als ohne
    Mail-Server (Punkt 1)."""
    domain = (domain or "").strip().lower().rstrip(".")
    if not domain:
        return False
    if domain in cache:
        return cache[domain]
    ok = bool(_dig("MX", domain)) or bool(_dig("A", domain)) or bool(_dig("AAAA", domain))
    cache[domain] = ok
    return ok


# --------------------------------------------------------------------------- Versand-Dump (aus der Datenschicht)
def lade_versand_dump(verzeichnis):
    """Ruft node dump-versand.mjs in site/ auf und gibt {slug: record} zurück. Die Werte (platz,
    anzahl, eintrag_url, bewertung, telefon, Stadt-Merkmale) kommen aus derselben Datenschicht wie
    der Build und stimmen darum mit dist/ überein."""
    site = os.path.join(verzeichnis, "site")
    helper = os.path.join(site, "dump-versand.mjs")
    if not os.path.isfile(helper):
        fehler(f"{helper} fehlt — der Versand-Export braucht den Datenschicht-Helfer (dump-versand.mjs).")
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix="versand-dump-")
    os.close(fd)
    try:
        r = subprocess.run(["node", "dump-versand.mjs", tmp], cwd=site, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:]); print(r.stderr[-2000:], file=sys.stderr)
            fehler("node dump-versand.mjs ist fehlgeschlagen; ist die Seite gebaut (npm install)?")
        daten = json.load(open(tmp, encoding="utf-8"))
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return {d["slug"]: d for d in daten}


# --------------------------------------------------------------------------- Adressen säubern
def saeubere_adressen(rows):
    """Je Eintrag eine Hauptadresse; sortiert formal ungültige, Portale/Zentraladressen und
    Mehrfachadressen (nur der bestbewertete Bezug bleibt) aus. Die Entscheidung ist GLOBAL
    (eine Adresse bei Einträgen in mehreren Bundesländern wird einmal entschieden); die
    MX-Prüfung bleibt getrennt (teuer). Gibt (behalten {slug: email}, drop {slug: grund})."""
    # 1. Hauptadresse je Eintrag; formal ungültige gleich heraus.
    kandidat = {}        # slug -> email (roh)
    drop = {}            # slug -> grund
    for r in rows:
        mail = haupt_email(r)
        if not mail:
            continue
        if not EMAIL_RX.match(mail):
            drop[r["slug"]] = "formal_ungueltig"
            continue
        kandidat[r["slug"]] = mail

    # 2. Gleiche Adresse bei mehreren Einträgen.
    je_email = {}
    for slug, mail in kandidat.items():
        je_email.setdefault(norm_email(mail), []).append(slug)
    row_by_slug = {r["slug"]: r for r in rows}
    behalten = {}
    for nmail, slugs in je_email.items():
        domain = nmail.split("@", 1)[1] if "@" in nmail else ""
        frei = domain not in FREEMAILER
        # Zentral-/Sammeladresse (Portal, Ketten-Zentrale): nicht Freemailer und bei vielen Einträgen.
        if frei and len(slugs) >= ZENTRAL_SCHWELLE:
            for s in slugs:
                drop[s] = "portal_zentrale"
            continue
        if len(slugs) == 1:
            behalten[slugs[0]] = kandidat[slugs[0]]
            continue
        # Mehrfach (unter der Zentral-Schwelle, oder Freemailer): nur den bestbewerteten behalten.
        best = max(slugs, key=lambda s: score(row_by_slug[s]))
        behalten[best] = kandidat[best]
        for s in slugs:
            if s != best:
                drop[s] = "mehrfach"
    return behalten, drop


# --------------------------------------------------------------------------- Unterbefehle
def cmd_eintragen(a, rows, hb_pfad):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    if a.weg not in WEGE:
        fehler("--weg muss telefon, email oder formular sein.")
    if not (a.ergebnis or "").strip():
        fehler("--ergebnis angeben (was bei dem Kontakt herauskam).")
    datum = a.datum or heute()
    try:
        dt.date.fromisoformat(datum)
    except ValueError:
        fehler(f"--datum '{datum}' ist kein Datum im Format JJJJ-MM-TT.")
    haenge(hb_pfad, HB_FELDER, {"datum": datum, "eintrag_slug": ziel["slug"], "weg": a.weg,
                                "ergebnis": a.ergebnis.strip(), "notiz": (a.notiz or "").strip()})
    print(f"Festgehalten: {datum} · {ziel['name']} ({ziel['slug']}) · {a.weg} · {a.ergebnis.strip()}")


def cmd_sperren(a, rows, sp_pfad, sperr):
    ziel, teil = finde_zeile(rows, a.slug)
    if ziel is None:
        _zeige_treffer(a.slug, teil)
    if ziel["slug"] in sperr:
        print(f"{ziel['name']} ({ziel['slug']}) ist bereits gesperrt. Nichts zu tun.")
        return
    haenge(sp_pfad, SP_FELDER, {"datum": heute(), "eintrag_slug": ziel["slug"], "grund": (a.grund or "").strip()})
    print(f"Gesperrt: {ziel['name']} ({ziel['slug']})"
          + (f" — {a.grund.strip()}" if (a.grund or '').strip() else "")
          + ". Erscheint in keiner Liste 'noch zu kontaktieren' und in keinem Export mehr.")


def cmd_offen(a, rows, kontaktiert, sperr):
    offen = []
    for r in rows:
        if truthy(r.get("owned")):
            continue
        if r["slug"] in sperr:
            continue
        if r["slug"] in kontaktiert:
            continue
        if a.bundesland and norm_bundesland(r.get("state")) != norm_bundesland(a.bundesland):
            continue
        if a.stadt and (r.get("city") or "").strip().lower() != a.stadt.strip().lower():
            continue
        offen.append(r)
    offen.sort(key=lambda r: ((r.get("state") or "").lower(), (r.get("city") or "").lower(), r["slug"]))

    filterhinweis = ""
    if a.bundesland:
        filterhinweis += f" · Bundesland {a.bundesland}"
    if a.stadt:
        filterhinweis += f" · Stadt {a.stadt}"
    print(f"Noch nie kontaktiert: {len(offen)} Einträge (ohne eigene, ohne gesperrte){filterhinweis}.\n")
    if not offen:
        return
    gefiltert = bool(a.bundesland or a.stadt)
    if len(offen) > 200 and not gefiltert and not a.alle:
        print("  Viele offene Einträge — Verteilung je Bundesland (mit --bundesland/--stadt einschränken,")
        print("  oder --alle zum vollständigen Auflisten):\n")
        je = {}
        for r in offen:
            je[r.get("state") or "?"] = je.get(r.get("state") or "?", 0) + 1
        for bl in sorted(je, key=lambda b: -je[b]):
            print(f"    {je[bl]:>5}  {bl}")
        return
    print(f"  {'Bundesland':<22} {'Stadt':<18} {'Betrieb':<34} {'Tel':<3} {'Mail':<4} Eintrag")
    print("  " + "-" * 110)
    for r in offen:
        tel = "ja" if (r.get("phone") or "").strip() else "—"
        mail = "ja" if any((r.get(c) or "").strip() for c in ("email_1", "email_2", "email_3")) else "—"
        print(f"  {(r.get('state') or '')[:21]:<22} {(r.get('city') or '')[:17]:<18} "
              f"{r['name'][:33]:<34} {tel:<3} {mail:<4} {r['slug']}")


def _export_kandidaten(rows, dump, kontaktiert, sperr, vorgesehen, ansprech, mx_cache, a, zaehle=None):
    """Baut die versandfertige Liste nach allen Filtern. Gibt (zeilen, statistik). Füllt mx_cache."""
    stat = {k: 0 for k in ("gesamt", "owned", "gesperrt", "kontaktiert", "vorgesehen",
                            "ohne_email", "formal_ungueltig", "kein_mailserver", "portal_zentrale",
                            "mehrfach", "kein_kernbetrieb", "stadt_hat_garantie_oder_platz",
                            "nicht_im_dump", "keine_variante", "bleiben")}
    # Adressen säubern GLOBAL (Dedup/Portal über alle Einträge), ohne MX (MX erst für die, die alle
    # anderen Filter bestehen — spart Lookups). Der Trichter unten zählt je Reihe im Kampagnen-Umfang.
    behalten, drop = saeubere_adressen(rows)

    zeilen = []
    for r in rows:
        slug = r["slug"]
        # Zuerst der Umfang der Kampagne (Bundesland/Stadt) — sonst zählte der Trichter bundesweit.
        if a.bundesland and norm_bundesland(r.get("state")) != norm_bundesland(a.bundesland):
            continue
        if a.stadt and (r.get("city") or "").strip().lower() != a.stadt.strip().lower():
            continue
        stat["gesamt"] += 1
        if truthy(r.get("owned")):
            stat["owned"] += 1; continue
        if slug in sperr:
            stat["gesperrt"] += 1; continue
        if slug in kontaktiert:
            stat["kontaktiert"] += 1; continue
        if slug in vorgesehen:
            stat["vorgesehen"] += 1; continue
        if not ist_kernbetrieb(r):
            stat["kein_kernbetrieb"] += 1; continue
        # Adresse: bei der Säuberung gefallen, gar keine, oder brauchbar?
        if slug in drop:
            stat[drop[slug]] += 1; continue
        if slug not in behalten:
            stat["ohne_email"] += 1; continue
        mail = behalten[slug]
        domain = mail.split("@", 1)[1].lower()
        if not hat_mailserver(domain, mx_cache):
            stat["kein_mailserver"] += 1; continue
        d = dump.get(slug)
        if not d:
            stat["nicht_im_dump"] += 1; continue
        # Nur Städte ohne Garantie und ohne bezahlten Platz (Punkt 3).
        if not d.get("cityEligible"):
            stat["stadt_hat_garantie_oder_platz"] += 1; continue
        telefon = (d.get("telefon") or "").strip()
        # Mail-Variante: Platz-Aufhänger nur mit Bewertung und genug Einträgen auf der Stadtseite,
        # sonst Telefon-Aufhänger. Ohne Telefon trägt der Eintrag keinen Aufhänger → fällt weg.
        if d.get("hatBewertung") and (d.get("anzahl") or 0) >= PLATZ_HOOK_MIN_ANZAHL:
            variante = "platz"
        else:
            variante = "telefon"
            if not telefon:
                stat["keine_variante"] += 1; continue
        vn, nn = ansprech.get(slug, ("", ""))
        if ist_platzhalter(vn, nn):
            vn = nn = ""
        zeilen.append({
            "eintrag_slug": slug, "kampagne": a.kampagne, "name": r.get("name", ""),
            "state": d.get("regionName") or r.get("state", ""), "city": d.get("city") or r.get("city", ""),
            "eintrag_url": d.get("eintragUrl", ""), "platz": d.get("platz", ""), "anzahl": d.get("anzahl", ""),
            "bewertung": d.get("bewertung", ""), "bewertungen": d.get("bewertungen", ""),
            "hat_bewertung": "wahr" if d.get("hatBewertung") else "falsch",
            "telefon": telefon, "email": mail,
            "vorname": vn, "nachname": nn, "anrede": baue_anrede(vn, nn),
            "variante": variante, "stand": heute(),
            "_score": score(r),
        })
    # Obergrenze gerecht schneiden: die besten (Score absteigend) über alle Städte zuerst, damit
    # späte Städte nicht ganz wegfallen. Danach erst die Datei-Reihenfolge herstellen.
    stat["ueber_limit"] = 0
    if a.limit and len(zeilen) > a.limit:
        stat["ueber_limit"] = len(zeilen) - a.limit
        zeilen.sort(key=lambda z: (-z["_score"], z["eintrag_slug"]))
        zeilen = zeilen[:a.limit]
    # Datei-Reihenfolge: Bundesland, Stadt, beste Bewertung zuerst, Slug.
    zeilen.sort(key=lambda z: (z["state"].lower(), z["city"].lower(), -z["_score"], z["eintrag_slug"]))
    stat["bleiben"] = len(zeilen)
    stat["mit_name"] = sum(1 for z in zeilen if z["vorname"] and z["nachname"])
    stat["variante_platz"] = sum(1 for z in zeilen if z["variante"] == "platz")
    stat["variante_telefon"] = sum(1 for z in zeilen if z["variante"] == "telefon")
    return zeilen, stat


def cmd_exportieren(a, rows, dump, kontaktiert, sperr, vorgesehen, ansprech, mx_cache, mx_pfad,
                    kamp_pfad, out_pfad):
    zeilen, stat = _export_kandidaten(rows, dump, kontaktiert, sperr, vorgesehen, ansprech, mx_cache, a)
    speichere_mx_cache(mx_pfad, mx_cache)

    print(f"Kampagne „{a.kampagne}“" + (f", Obergrenze {a.limit}" if a.limit else "")
          + (f", Bundesland {a.bundesland}" if a.bundesland else "")
          + (f", Stadt {a.stadt}" if a.stadt else "") + "\n")
    print("Adressen säubern und filtern (von {gesamt} Einträgen):".format(**stat))
    print(f"  eigene Betriebe                     {stat['owned']:>6}")
    print(f"  gesperrt                            {stat['gesperrt']:>6}")
    print(f"  schon kontaktiert                   {stat['kontaktiert']:>6}")
    print(f"  schon für Versand vorgesehen        {stat['vorgesehen']:>6}")
    print(f"  kein bestätigter Kernbetrieb        {stat['kein_kernbetrieb']:>6}")
    print(f"  keine E-Mail-Adresse                 {stat['ohne_email']:>6}")
    print(f"  E-Mail formal ungültig              {stat['formal_ungueltig']:>6}")
    print(f"  Domain ohne Mail-Server (MX)        {stat['kein_mailserver']:>6}")
    print(f"  Portal-/Zentraladresse              {stat['portal_zentrale']:>6}")
    print(f"  Mehrfachadresse (nur bester Bezug)  {stat['mehrfach']:>6}")
    print(f"  Stadt hat Garantie/bezahlten Platz  {stat['stadt_hat_garantie_oder_platz']:>6}")
    print(f"  keine Variante (telefon, kein Tel.) {stat['keine_variante']:>6}")
    if stat.get("ueber_limit"):
        print(f"  über der Obergrenze abgeschnitten   {stat['ueber_limit']:>6}")
    print(f"  --------------------------------------------")
    print(f"  versandfertig                       {stat['bleiben']:>6}  ({stat['mit_name']} mit persönlicher Anrede)")
    print(f"    davon Variante platz              {stat['variante_platz']:>6}")
    print(f"    davon Variante telefon            {stat['variante_telefon']:>6}\n")

    hinweis = ("Plätze gelten für den Stand von heute. Nach einem Neubau neu exportieren, "
               "nicht diese Datei versenden.")
    if a.probe:
        print("PROBE (--probe): nichts geschrieben, keine Kampagne vermerkt.")
        print(hinweis)
        return
    if not zeilen:
        print("Nichts zu exportieren — keine Datei geschrieben, keine Kampagne vermerkt.")
        return
    with open(out_pfad, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EXPORT_FELDER)
        w.writeheader()
        for z in zeilen:
            w.writerow({k: z[k] for k in EXPORT_FELDER})
    datum = heute()
    haenge(kamp_pfad, KAMP_FELDER, [{"datum": datum, "kampagne": a.kampagne,
                                     "eintrag_slug": z["eintrag_slug"], "status": "vorgesehen"} for z in zeilen])
    print(f"Export: {len(zeilen)} Zeilen nach {out_pfad}")
    print(f"Kampagne „{a.kampagne}“: {len(zeilen)} Einträge als „vorgesehen“ vermerkt "
          f"(nicht erneut exportiert). Es wurde nichts versendet.")
    print(hinweis)


def cmd_importieren(a, rows, hb_pfad, sp_pfad, sperr, kamp_pfad, datei):
    daten = lade(datei)
    if not daten:
        fehler(f"{datei} ist leer oder keine CSV mit Kopfzeile.")
    kopf = {c.lower(): c for c in daten[0].keys()}

    def finde_spalte(override, kandidaten):
        if override:
            if override not in daten[0]:
                fehler(f"Spalte '{override}' steht nicht in {datei}. Vorhanden: {', '.join(daten[0].keys())}")
            return override
        for k, orig in kopf.items():
            if k in kandidaten:
                return orig
        return None

    sp_slug = finde_spalte(a.spalte_slug, SP_SLUG)
    sp_email = finde_spalte(a.spalte_email, SP_EMAIL)
    sp_status = finde_spalte(a.spalte_status, SP_STATUS)
    sp_datum = finde_spalte(a.spalte_datum, SP_DATUM)
    if not sp_status:
        fehler("keine Status-Spalte erkannt (status/event/result/ergebnis) — mit --spalte-status setzen.")
    if not (sp_slug or sp_email):
        fehler("weder Slug- noch E-Mail-Spalte erkannt — mit --spalte-slug oder --spalte-email setzen.")

    # E-Mail -> Slug (für Zeilen ohne Slug). Mehrdeutige Adressen bleiben mehrdeutig (nie raten).
    email2slugs = {}
    for r in rows:
        for c in ("email_1", "email_2", "email_3"):
            v = norm_email(r.get(c))
            if v:
                email2slugs.setdefault(v, set()).add(r["slug"])
    slug_set = {r["slug"] for r in rows}

    je_status = {s: 0 for s in VERSAND_STATUS[1:]}
    unklar = []
    hb_neu, kamp_neu, sperr_neu = [], [], []
    schon_gesperrt = set(sperr)
    verarbeitet = 0
    for i, z in enumerate(daten, start=2):  # Zeile 1 ist der Kopf
        roh_status = (z.get(sp_status) or "").strip().lower()
        status = STATUS_MAP.get(roh_status)
        if not status:
            unklar.append((i, f"unbekannter Status '{z.get(sp_status)}'"))
            continue
        slug = (z.get(sp_slug) or "").strip() if sp_slug else ""
        if slug and slug not in slug_set:
            # evtl. Teiltreffer? Nicht raten.
            slug = ""
        if not slug and sp_email:
            mail = norm_email(z.get(sp_email))
            treffer = email2slugs.get(mail, set())
            if len(treffer) == 1:
                slug = next(iter(treffer))
            elif len(treffer) > 1:
                unklar.append((i, f"E-Mail '{mail}' trifft {len(treffer)} Einträge"))
                continue
        if not slug:
            kennung = z.get(sp_slug) or z.get(sp_email) or "?"
            unklar.append((i, f"kein Eintrag zu '{kennung}' gefunden"))
            continue
        datum = (z.get(sp_datum) or "").strip() if sp_datum else ""
        if datum:
            m = re.search(r"(\d{4})-(\d{2})-(\d{2})", datum) or re.search(r"(\d{2})\.(\d{2})\.(\d{4})", datum)
            if m and "." in datum:
                datum = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            elif m:
                datum = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            else:
                datum = heute()
        else:
            datum = heute()
        je_status[status] += 1
        verarbeitet += 1
        hb_neu.append({"datum": datum, "eintrag_slug": slug, "weg": "email",
                       "ergebnis": f"Versand: {status}", "notiz": a.kampagne or ""})
        kamp_neu.append({"datum": datum, "kampagne": a.kampagne or "", "eintrag_slug": slug, "status": status})
        if status in STATUS_SPERRT and slug not in schon_gesperrt:
            sperr_neu.append({"datum": datum, "eintrag_slug": slug,
                              "grund": f"{status}" + (f" (Kampagne {a.kampagne})" if a.kampagne else "")})
            schon_gesperrt.add(slug)

    if hb_neu:
        haenge(hb_pfad, HB_FELDER, hb_neu)
    if kamp_neu:
        haenge(kamp_pfad, KAMP_FELDER, kamp_neu)
    if sperr_neu:
        haenge(sp_pfad, SP_FELDER, sperr_neu)

    print(f"Import aus {datei}" + (f" (Kampagne „{a.kampagne}“)" if a.kampagne else "") + ":\n")
    print(f"  verarbeitet            {verarbeitet:>6}")
    for s in VERSAND_STATUS[1:]:
        print(f"    {s:<18} {je_status[s]:>6}")
    print(f"  auf die Sperrliste     {len(sperr_neu):>6}  (abgemeldet/unzustellbar)")
    print(f"  unklar, nicht geraten  {len(unklar):>6}")
    for zeile, grund in unklar[:40]:
        print(f"    Zeile {zeile}: {grund}")
    if len(unklar) > 40:
        print(f"    … und {len(unklar) - 40} weitere")


def _itemlist_positionen(html):
    """{firma-slug: position} aus dem JSON-LD ItemList der Stadtseite — die gerenderte Reihenfolge.
    Die Liste ist auf die ersten 60 begrenzt; ein Eintrag dahinter fehlt hier (kein Fehler)."""
    pos = {}
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            d = json.loads(b)
        except ValueError:
            continue
        for x in (d if isinstance(d, list) else [d]):
            if not (isinstance(x, dict) and x.get("@type") == "ItemList"):
                continue
            for e in x.get("itemListElement", []):
                item = e.get("item") or {}
                url = e.get("url") or item.get("@id") or item.get("url") or ""
                m = re.search(r"/firma/[^/]+/[^/]+/([^/]+)/", url)
                if m and e.get("position"):
                    pos[m.group(1)] = int(e["position"])
    return pos


def cmd_pruefen(a, dump, verzeichnis):
    """Stichprobe gegen dist/: platz, anzahl, Bewertung, Telefon. Jede Abweichung ist ein Fehler
    im Export (die Werte stammen aus derselben Datenschicht wie der Build), nicht in der Seite.
    platz liest das JSON-LD ItemList der Stadtseite (gerenderte Reihenfolge, erste 60), anzahl die
    Überschrift („N Schlüsseldienste in …"), Bewertung/Telefon die Eintragsseite."""
    dist = os.path.join(verzeichnis, "site", "dist")
    if not os.path.isdir(dist):
        fehler(f"{dist} fehlt — zuerst die Seite bauen (npm run build).")
    kandidaten = [d for d in dump.values() if d.get("hatBewertung")]
    rng = random.Random(a.seed)
    stichprobe = rng.sample(kandidaten, min(a.anzahl, len(kandidaten)))
    fehlerzahl = 0
    print(f"Stichprobe {len(stichprobe)} Einträge gegen {os.path.relpath(dist, WURZEL)} "
          f"(Seed {a.seed}):\n")
    for d in stichprobe:
        slug, region, cityslug = d["slug"], d["regionSlug"], d["citySlug"]
        eintrag_html = os.path.join(dist, "firma", region, cityslug, slug, "index.html")
        stadt_html = os.path.join(dist, "verzeichnis", region, cityslug, "index.html")
        probleme, hinweise = [], []
        # platz (ItemList) und anzahl (Überschrift) von der Stadtseite
        if os.path.isfile(stadt_html):
            html = open(stadt_html, encoding="utf-8").read()
            pos = _itemlist_positionen(html)
            if slug in pos:
                if pos[slug] != d["platz"]:
                    probleme.append(f"platz dist={pos[slug]} ≠ export={d['platz']}")
            elif d["platz"] > 60:
                hinweise.append(f"platz {d['platz']} (>60, nicht im ItemList)")
            else:
                probleme.append(f"platz export={d['platz']} nicht im ItemList der Seite")
            m = re.search(r"([0-9][0-9.]*)\s+Schlüsseldienste?\s+in\b", html)
            anzahl_dist = int(m.group(1).replace(".", "")) if m else None
            if anzahl_dist != d["anzahl"]:
                probleme.append(f"anzahl dist={anzahl_dist} ≠ export={d['anzahl']}")
        else:
            probleme.append(f"Stadtseite fehlt: {os.path.relpath(stadt_html, dist)}")
        # Bewertung/Telefon von der Eintragsseite
        if os.path.isfile(eintrag_html):
            html = open(eintrag_html, encoding="utf-8").read()
            m = re.search(r'class="score">([0-9]+,[0-9]+)<', html)
            bew_dist = m.group(1) if m else None
            if bew_dist != d["bewertung"]:
                probleme.append(f"bewertung dist={bew_dist} ≠ export={d['bewertung']}")
            m = re.search(r"\(([0-9.]+) Bewertung", html)
            if m and m.group(1) != d["bewertungen"]:
                probleme.append(f"bewertungen dist={m.group(1)} ≠ export={d['bewertungen']}")
            tel = d["telefon"].replace(" ", "")
            if tel and tel not in html.replace(" ", ""):
                probleme.append(f"telefon {d['telefon']} nicht auf der Seite")
        else:
            probleme.append(f"Eintragsseite fehlt: {os.path.relpath(eintrag_html, dist)}")
        if probleme:
            fehlerzahl += 1
            print(f"  ABWEICHUNG {slug}: " + "; ".join(probleme))
        elif hinweise:
            print(f"  ok      {slug}: " + "; ".join(hinweise))
    print(f"\n  geprüft {len(stichprobe)}, Abweichungen {fehlerzahl}.")
    if fehlerzahl:
        sys.exit(1)
    print("  Alle Stichproben stimmen mit dist/ überein.")


def cmd_stand(a, rows, hb, kontaktiert, sperr, kamp, garantie_hb):
    if a.kampagne:
        _stand_kampagne(a.kampagne, kamp, hb, garantie_hb)
        return
    gesamt = len(rows)
    eigen = sum(1 for r in rows if truthy(r.get("owned")))
    gesperrt = sum(1 for r in rows if r["slug"] in sperr)
    offen = sum(1 for r in rows if not truthy(r.get("owned")) and r["slug"] not in sperr and r["slug"] not in kontaktiert)
    kontaktiert_n = sum(1 for r in rows if r["slug"] in kontaktiert)
    print("Kontakt-Stand:\n")
    print(f"  Einträge gesamt          {gesamt:>6}")
    print(f"  davon eigene Betriebe    {eigen:>6}  (nie in 'noch zu kontaktieren')")
    print(f"  gesperrt                 {gesperrt:>6}")
    print(f"  schon kontaktiert        {kontaktiert_n:>6}  (eindeutige Einträge im Hauptbuch)")
    print(f"  noch offen               {offen:>6}  (nicht eigen, nicht gesperrt, nie kontaktiert)")
    if hb:
        print(f"\n  Kontakte im Hauptbuch gesamt: {len(hb)}")
        je_weg, je_erg = {}, {}
        for z in hb:
            je_weg[z.get("weg") or "?"] = je_weg.get(z.get("weg") or "?", 0) + 1
            e = (z.get("ergebnis") or "?").strip() or "?"
            je_erg[e] = je_erg.get(e, 0) + 1
        print("  je Weg:    " + ", ".join(f"{w}: {n}" for w, n in sorted(je_weg.items(), key=lambda x: -x[1])))
        print("  je Ergebnis:")
        for e, n in sorted(je_erg.items(), key=lambda x: -x[1]):
            print(f"    {n:>5}  {e}")
    if kamp:
        je = kampagnen_je_slug(kamp)
        print(f"\n  Kampagnen ({len(je)}):")
        for name in sorted(je):
            stati = je[name]
            n = len(stati)
            ges = sum(1 for s in stati.values() if s == "gesendet")
            ant = sum(1 for s in stati.values() if s == "geantwortet")
            print(f"    {name:<24} {n:>5} vorgesehen, {ges} gesendet, {ant} geantwortet "
                  f"(--stand --kampagne {name} für alle Zahlen)")


def _stand_kampagne(name, kamp, hb, garantie_hb):
    je = kampagnen_je_slug(kamp).get(name)
    if not je:
        fehler(f"keine Kampagne „{name}“ in der Kampagnen-Liste. Vorhanden: "
               + (", ".join(sorted(kampagnen_je_slug(kamp))) or "(keine)"))
    start = kampagnen_start(kamp).get(name, "")
    slugs = set(je)
    exportiert = len(slugs)
    zahl = {s: sum(1 for v in je.values() if v == s) for s in VERSAND_STATUS}
    # Anträge: Hauptbuch-Zeilen der Kampagnen-Slugs, deren Ergebnis „Antrag" nennt, ab Kampagnenstart.
    antraege = {z["eintrag_slug"] for z in hb if z.get("eintrag_slug") in slugs
                and "antrag" in (z.get("ergebnis") or "").lower()
                and (not start or (z.get("datum") or "") >= start)}
    # Garantien: Kampagnen-Slugs mit einer Erteilung ab Kampagnenstart (garantie-hauptbuch.csv).
    garantien = {z["eintrag_slug"] for z in garantie_hb if z.get("eintrag_slug") in slugs
                 and z.get("aktion") == "erteilt" and (not start or (z.get("datum") or "") >= start)}
    print(f"Kampagne „{name}“ (Start {start or 'unbekannt'}):\n")
    print(f"  exportiert (vorgesehen)  {exportiert:>6}")
    print(f"  gesendet                 {zahl['gesendet']:>6}")
    print(f"  geantwortet              {zahl['geantwortet']:>6}")
    print(f"  abgemeldet               {zahl['abgemeldet']:>6}")
    print(f"  unzustellbar             {zahl['unzustellbar']:>6}")
    print(f"  daraus Anträge           {len(antraege):>6}  (Hauptbuch-Ergebnis nennt „Antrag“)")
    print(f"  daraus Garantien         {len(garantien):>6}  (Festpreis-Garantie erteilt)")


def main():
    ap = argparse.ArgumentParser(description="Kontaktbuch & Versand-Export: eintragen, sperren, "
                                 "offene Einträge, exportieren, prüfen, importieren, Stand.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aktion", nargs="?", choices=["eintragen", "sperren", "exportieren", "importieren", "pruefen"],
                    help="eintragen | sperren | exportieren | importieren | pruefen")
    ap.add_argument("--slug", help="Slug des Eintrags (exakt oder eindeutiger Teil)")
    ap.add_argument("--weg", choices=WEGE, help="telefon | email | formular (bei eintragen)")
    ap.add_argument("--ergebnis", help="was bei dem Kontakt herauskam (bei eintragen)")
    ap.add_argument("--grund", help="Grund der Sperre (bei sperren)")
    ap.add_argument("--notiz", help="Freitext-Notiz")
    ap.add_argument("--datum", help="Datum JJJJ-MM-TT (Vorgabe: heute)")
    ap.add_argument("--offen", action="store_true", help="Einträge, die noch nie kontaktiert wurden")
    ap.add_argument("--stand", action="store_true", help="Zahlen je Status; mit --kampagne je Kampagne")
    ap.add_argument("--bundesland", help="auf ein Bundesland einschränken (Spalte state)")
    ap.add_argument("--stadt", help="auf eine Stadt einschränken")
    ap.add_argument("--alle", action="store_true", help="--offen vollständig auflisten, auch bei vielen")
    # exportieren
    ap.add_argument("--kampagne", help="Name der Kampagne (bei exportieren nötig; bei importieren/--stand optional)")
    ap.add_argument("--limit", type=int, help="Obergrenze der Stückzahl der Kampagne (exportieren)")
    ap.add_argument("--out", help="Zieldatei des Exports (Vorgabe: <verzeichnis>/kontakt-export-<kampagne>.csv)")
    ap.add_argument("--probe", action="store_true", help="exportieren: nur Zahlen, nichts schreiben, nichts vermerken")
    # pruefen
    ap.add_argument("--anzahl", type=int, default=20, help="pruefen: Zahl der Stichproben (Vorgabe 20)")
    ap.add_argument("--seed", type=int, default=0, help="pruefen: Zufalls-Seed (reproduzierbar)")
    # importieren
    ap.add_argument("--datei", help="Ergebnis-CSV der Versandplattform (importieren)")
    ap.add_argument("--spalte-slug", dest="spalte_slug", help="Spaltenname des Slugs in der Import-Datei")
    ap.add_argument("--spalte-email", dest="spalte_email", help="Spaltenname der E-Mail in der Import-Datei")
    ap.add_argument("--spalte-status", dest="spalte_status", help="Spaltenname des Status in der Import-Datei")
    ap.add_argument("--spalte-datum", dest="spalte_datum", help="Spaltenname des Datums in der Import-Datei")
    # Pfade
    ap.add_argument("--ansprechpartner", help="Pfad der Ansprechpartner-Datei (Vorgabe: <verzeichnis>/kontakt-ansprechpartner.csv)")
    ap.add_argument("--verzeichnis", help="Build-Verzeichnis (Vorgabe: einziges unter output/*/site/)")
    ap.add_argument("--hauptbuch", help="Pfad des Kontaktbuchs (Vorgabe: <verzeichnis>/kontakt-hauptbuch.csv)")
    ap.add_argument("--sperrliste", help="Pfad der Sperrliste (Vorgabe: <verzeichnis>/kontakt-sperrliste.csv)")
    ap.add_argument("--kampagnen", help="Pfad der Kampagnen-Liste (Vorgabe: <verzeichnis>/kontakt-kampagnen.csv)")
    a = ap.parse_args()

    aktionen = [bool(a.aktion), a.offen, a.stand]
    if sum(aktionen) != 1:
        ap.error("genau eine Aktion: eintragen, sperren, exportieren, importieren, pruefen, --offen oder --stand")

    verzeichnis = finde_verzeichnis(a.verzeichnis)
    csv_pfad = os.path.join(verzeichnis, "site", "src", "data", "listings.csv")

    def pfad(arg, name):
        p = arg or os.path.join(verzeichnis, name)
        if arg and not os.path.isabs(p):
            p = os.path.join(WURZEL, p)
        return p

    hb_pfad = pfad(a.hauptbuch, "kontakt-hauptbuch.csv")
    sp_pfad = pfad(a.sperrliste, "kontakt-sperrliste.csv")
    kamp_pfad = pfad(a.kampagnen, "kontakt-kampagnen.csv")
    ap_pfad = pfad(a.ansprechpartner, "kontakt-ansprechpartner.csv")
    mx_pfad = os.path.join(verzeichnis, "versand-mx-cache.json")

    _, rows = lade_csv(csv_pfad)
    hb = lade(hb_pfad)
    sp = lade(sp_pfad)
    kamp = lade(kamp_pfad)
    kontaktiert = {z.get("eintrag_slug") for z in hb}
    sperr = {z.get("eintrag_slug") for z in sp}
    ansprech = lade_ansprechpartner(ap_pfad)

    if a.aktion == "eintragen":
        if not a.slug:
            ap.error("eintragen braucht --slug")
        cmd_eintragen(a, rows, hb_pfad)
    elif a.aktion == "sperren":
        if not a.slug:
            ap.error("sperren braucht --slug")
        cmd_sperren(a, rows, sp_pfad, sperr)
    elif a.aktion == "exportieren":
        if not a.kampagne:
            ap.error("exportieren braucht --kampagne")
        if not re.match(r"^[a-z0-9][a-z0-9\-]*$", a.kampagne):
            ap.error("--kampagne nur aus Kleinbuchstaben, Ziffern und Bindestrich (Dateiname)")
        out_pfad = a.out or os.path.join(verzeichnis, f"kontakt-export-{a.kampagne}.csv")
        if a.out and not os.path.isabs(out_pfad):
            out_pfad = os.path.join(WURZEL, out_pfad)
        dump = lade_versand_dump(verzeichnis)
        vorgesehen = alle_vorgesehenen(kamp)
        mx_cache = lade_mx_cache(mx_pfad)
        cmd_exportieren(a, rows, dump, kontaktiert, sperr, vorgesehen, ansprech, mx_cache, mx_pfad,
                        kamp_pfad, out_pfad)
    elif a.aktion == "importieren":
        if not a.datei:
            ap.error("importieren braucht --datei")
        datei = a.datei if os.path.isabs(a.datei) else os.path.join(WURZEL, a.datei)
        if not os.path.isfile(datei):
            fehler(f"{datei} gibt es nicht.")
        cmd_importieren(a, rows, hb_pfad, sp_pfad, sperr, kamp_pfad, datei)
    elif a.aktion == "pruefen":
        dump = lade_versand_dump(verzeichnis)
        cmd_pruefen(a, dump, verzeichnis)
    elif a.offen:
        cmd_offen(a, rows, kontaktiert, sperr)
    elif a.stand:
        garantie_hb = lade(os.path.join(verzeichnis, "garantie-hauptbuch.csv"))
        cmd_stand(a, rows, hb, kontaktiert, sperr, kamp, garantie_hb)


if __name__ == "__main__":
    main()
