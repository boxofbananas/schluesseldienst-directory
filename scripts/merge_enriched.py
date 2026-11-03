#!/usr/bin/env python3
"""Gate 3 helper: check the enrichment answers and write 03-listings-enriched.csv.

Reads the clean CSV, the evidence packets and the answers in 03-cache/enriched/<city_slug>.json
(a list of {slug, attributes: {key: value}, description}). Nothing is written to the CSV unless
every listing passes, so a bad batch is fixed in the cache and the merge is run again.

Checks per listing:
  - every attribute key from the attribute set is answered with true, false or not enough info
  - a "true" can be traced: the attribute's pattern matches the packet (quotes, headings, menu,
    title, meta, Maps fields), or the answer carries trace.<key> with words copied exactly from
    the packet. An answer of true with nothing behind it is a guess and fails.
  - the description says nothing about how the directory was built ("the packet", website error codes)
  - the description states facts as presented and never names its source ("its site says", "the website",
    "on Google Maps", "does not say"); the page's own lines carry the sourcing (Shawn, 2026-09-30)
  - the description sits in its word band, carries no em dash and no banned word or phrase
    (the copy gate's list)
  - the description's opener (its first nine words, the business name removed) is not shared by
    four or more listings in the run. The tally runs over every answers file in --enriched, so a
    batch checked with --only is measured against the batches already written; only the checked
    batch's own listings are reported, each as a FAIL line asking for a reword. In the full merge
    the shared openers are listed with their slugs and batches, to be rerun with run_batches.py --only.

Usage:
  python3 scripts/merge_enriched.py output/<slug>/02-listings-clean.csv \
      --attributes output/<slug>/03-attributes.json --patterns output/<slug>/03-attributes.json \
      --evidence output/<slug>/03-cache/evidence --enriched output/<slug>/03-cache/enriched \
      --out output/<slug>/03-listings-enriched.csv [--band 120 200] [--short-band 50 90] [--partial]
      [--only output/<slug>/03-cache/enriched/batch-001.json --slugs output/<slug>/03-cache/batches/batch-001.slugs.json]

--short-band applies to listings with no quotes at all. A listing with quotes for only one or
two attributes keeps the upper limit and gets a floor of --thin-floor words, so nobody pads. --partial reports on the cities
answered so far and writes nothing.
"""
import argparse, csv, glob, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

csv.field_size_limit(10**9)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
VALID = {"true", "false", "not enough info"}
UMLAUTE = [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")]
# Ein Wort auf Deutsch: Umlaute und ß gehoeren dazu, eine Zusammensetzung mit Bindestrich ist
# ein Wort. Gleiche Zaehlung wie lint_copy.count_words, damit Wortbaender uebereinstimmen.
WORD = re.compile(r"[A-Za-zÄÖÜäöüß0-9]+(?:[-’'][A-Za-zÄÖÜäöüß0-9]+)*")


def fold(s):
    """Vergleichsform: Kleinbuchstaben, Umlaute umgeschrieben, uebrige Akzente entfernt.
    Satzzeichen bleiben, damit Wortgrenzen (\\b) weiter gelten. Wie lint_copy.fold_text."""
    s = s or ""
    for a, b in UMLAUTE:
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


# Formulierungen, die zur Entstehung des Verzeichnisses gehoeren und nicht in den Text duerfen.
# Die Muster laufen gegen die gefaltete Form, deshalb stehen hier keine Umlaute.
SOURCE = re.compile(
    r"\blaut (?:eigener |der |seiner |ihrer )?(?:website|webseite|seite|homepage|angabe|angaben|darstellung)\b"
    r"|\bauf (?:der |seiner |ihrer )?(?:eigenen )?(?:website|webseite|homepage)\b"
    r"|\b(?:die|seine|ihre) (?:website|webseite|homepage) (?:nennt|sagt|zeigt|fuehrt|gibt|weist|erwaehnt|listet)\b"
    r"|\bim impressum\b|\bim fussbereich\b|\bin der fusszeile\b"
    r"|\b(?:bei|auf|laut|nach) google(?: maps)?\b|\bgoogle[- ]eintrag\b|\bunternehmensprofil\b"
    r"|\bnicht (?:genannt|angegeben|erwaehnt|aufgefuehrt|ersichtlich|auffindbar)\b"
    r"|\bkeine angabe\b|\bkeine angaben\b|\bnichts (?:dazu|darueber)\b"
    r"|\bbezeichnet sich (?:selbst )?als\b|\bnach eigener darstellung\b|\bnach eigenen angaben\b"
    r"|\boeffentlich (?:einsehbar|zugaenglich)\b", re.I)
# Formulierungen aus dem Bauvorgang: Pakete, Abrufe, Fehlercodes.
INTERNAL = re.compile(
    r"\bpaket\w*\b|\battribut\w*\b|\bdatensatz\b|\bdatenpaket\b|\bmerkmalsliste\b"
    r"|nicht[- ]gefunden|zugriffsfehler|serverfehler|http \d{3}|\b40[34]\b|zeitueberschreitung"
    r"|\bbeim (?:abruf|pruefen|aufruf)\b|\bkonnte nicht (?:gelesen|abgerufen|geladen|geprueft) werden\b"
    r"|\bleer geladen\b|\bverweigert\b|\bautomatisierte[rn]? (?:zugriff|abruf|anfrage)\b"
    r"|\blieferte einen? fehler\b|\bnicht auslesbar\b", re.I)
# geprueft bis preisschutz: die Spalten der Festpreis-Garantie (wiki/konventionen.md), von Hand
# gesetzt, hier nur unveraendert durchgereicht.
EXTRA = ["premium", "best_of_rank", "photos", "geprueft", "geprueft_jahr",
         "garantie_tag", "garantie_nacht", "garantie_anfahrt", "preisschutz"]


def load_patterns(path):
    """The pattern source is the per-vertical attribute file (a list of attributes, each with a
    `pattern`), or a plain {key: regex} object. Both compile to {key: regex}."""
    data = json.load(open(path, encoding="utf-8"))
    items = data.items() if isinstance(data, dict) else ((x["key"], x.get("pattern", "")) for x in data)
    pats = {}
    for k, v in items:
        if k.startswith("_"): continue
        if not v: raise SystemExit(f"ERROR: {path}: attribute {k} has no pattern (a regex of the words that count as evidence)")
        try: pats[k] = re.compile(v, re.I)
        except re.error as e: raise SystemExit(f"ERROR: {path}: pattern for {k} does not compile: {e}")
    return pats


def load_bans():
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "seo-content-engine", "scripts"))
    try:
        import lint_article as la
    except ImportError:
        raise SystemExit("skills/seo-content-engine/scripts/lint_article.py is missing. Unzip the whole Blueprint; the copy gate needs the skill's linter.")
    w, p = la.load_forbidden(os.path.join(os.path.dirname(HERE), "skills", "seo-content-engine", "references", "forbidden_words.txt"))
    w2, p2 = la.load_forbidden(os.path.join(HERE, "copy-bans.txt"))
    return [x.lower() for x in w + w2], [x.lower() for x in p + p2]


def words(t):
    return len(WORD.findall(t or ""))


def opener(x, pk):
    """Die ersten neun Woerter einer Beschreibung, gefaltet, ohne den Firmennamen."""
    d = fold(x.get("description") or "").replace(fold(pk.get("name") or "\0"), "")
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", d).split()[:9])


def packet_text(pk):
    parts = [pk.get("name", ""), pk.get("maps_type", ""), pk.get("maps_subtypes", ""), pk.get("maps_description", ""),
             " ".join(pk.get("maps_about", [])), pk.get("site_title", ""), pk.get("site_meta", ""),
             " ".join(pk.get("site_headings", [])), " ".join(pk.get("site_menu", []))]
    for q in pk.get("quotes", {}).values(): parts += q
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("--attributes", required=True); ap.add_argument("--patterns", required=True)
    ap.add_argument("--evidence", required=True); ap.add_argument("--enriched", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--band", type=int, nargs=2, default=[120, 200]); ap.add_argument("--short-band", type=int, nargs=2, default=[50, 90])
    ap.add_argument("--thin-floor", type=int, default=80, help="word floor when only one or two attributes have a quote")
    ap.add_argument("--partial", action="store_true")
    ap.add_argument("--only", default="", help="check this one answers file and nothing else (implies --partial)")
    ap.add_argument("--slugs", default="", help="with --only: the batch's .slugs.json, every slug in it must be answered")
    a = ap.parse_args()

    keys = [x["key"] for x in json.load(open(a.attributes, encoding="utf-8"))]
    pats = load_patterns(a.patterns)
    missing = [k for k in keys if k not in pats]
    if missing:
        print(f"ERROR: {a.patterns} has no pattern for: {', '.join(missing)}. Every key in {a.attributes} needs one (a regex of the words that count as evidence).")
        sys.exit(1)
    ban_w, ban_p = load_bans()
    with open(a.csv, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f); cols = rd.fieldnames; rows = list(rd)
    packets = {}
    for p in glob.glob(os.path.join(a.evidence, "*.json")):
        for pk in json.load(open(p, encoding="utf-8")): packets[pk["slug"]] = pk
    answers, dupes, source = {}, [], {}
    if a.only: a.partial = True
    files = sorted(glob.glob(os.path.join(a.enriched, "*.json")))
    checked = [a.only] if a.only else files
    for p in checked:
        for x in json.load(open(p, encoding="utf-8")):
            if x["slug"] in answers: dupes.append(x["slug"])
            answers[x["slug"]] = x; source[x["slug"]] = os.path.basename(p)
    # Openers are counted over the whole run: every answers file already in --enriched plus the
    # batch being checked, so a batch sees the openers the other batches used. Only the checked
    # batch's listings can fail on it.
    openers = Counter()
    for p in files:
        if a.only and os.path.realpath(p) == os.path.realpath(a.only): continue
        for x in json.load(open(p, encoding="utf-8")):
            if x["slug"] in answers: continue
            openers[opener(x, packets.get(x["slug"], {}))] += 1
    for s, x in answers.items():
        openers[opener(x, packets.get(s, {}))] += 1

    fails, tally = defaultdict(list), {k: Counter() for k in keys}
    for r in rows:
        s = r["slug"]; x = answers.get(s)
        if x is None:
            if not a.partial: fails[s].append("no answer in the cache")
            continue
        pk = packets.get(s, {}); blob = packet_text(pk)
        for k in keys:
            v = str(x.get("attributes", {}).get(k, "")).strip().lower()
            if v not in VALID: fails[s].append(f"{k}: '{v}' is not true / false / not enough info"); continue
            tally[k][v] += 1
            if v == "true" and not pats[k].search(blob):
                tr = " ".join(str((x.get("trace") or {}).get(k, "")).lower().split())
                if len(tr) < 8 or tr not in " ".join(blob.lower().split()):
                    fails[s].append(f"{k}: true with nothing behind it (add trace.{k}: words copied exactly from the packet, or answer not enough info)")
        d = (x.get("description") or "").strip()
        nq = len(pk.get("quotes") or {})
        lo, hi = a.short_band if nq == 0 else ((a.thin_floor, a.band[1]) if nq <= 2 else a.band)
        n = words(d)
        if not lo <= n <= hi: fails[s].append(f"description is {n} words, band is {lo} to {hi}")
        if "—" in d or "–" in d or " -- " in d: fails[s].append("description has a dash used as punctuation")
        folded = fold(d)
        inside = sorted({m.group(0) for m in INTERNAL.finditer(folded)})
        if inside: fails[s].append(f"internal wording a reader should not see: {inside}")
        sourced = sorted({m.group(0) for m in SOURCE.finditer(folded)})
        if sourced: fails[s].append(f"names the source instead of stating the fact: {sourced} (say what the business does and offers; the page's own lines carry where it came from)")
        # Verbote umlauttolerant: Liste und Text werden beide gefaltet, damit "zuverlaessig"
        # auch "zuverlässig" trifft.
        for w in ban_w:
            if re.search(r"\b" + re.escape(fold(w)) + r"\b", folded): fails[s].append(f"banned word: {w}")
        for p in ban_p:
            if fold(p) in folded: fails[s].append(f"banned phrase: {p}")
        o = opener(x, pk)
        if o and openers[o] >= 4:
            fails[s].append(f"description opener is shared by {openers[o]} listings in this run ('{o}'): reword the opening so it is specific to this business")
    if a.slugs:
        for s in json.load(open(a.slugs, encoding="utf-8")):
            if s not in answers: fails[s].append("in the batch but not answered")
    for s in set(dupes): fails[s].append("answered twice in the cache")
    for s in answers:
        if s not in {r["slug"] for r in rows}: fails[s].append("slug is not in the clean CSV")
    shared = {o: n for o, n in openers.items() if n >= 4 and o}
    shared_here = defaultdict(list)   # opener -> slugs in the checked set
    for s, x in answers.items():
        o = opener(x, packets.get(s, {}))
        if o in shared: shared_here[o].append(s)

    print(f"listings: {len(rows)}, answered: {len(answers)}, failing: {len(fails)}")
    print("answers per attribute (true / false / not enough info):")
    for k in keys: print(f"  {k}: {tally[k]['true']} / {tally[k]['false']} / {tally[k]['not enough info']}")
    if shared_here:
        print("FAIL: description openers shared by four or more listings in the run (they read as one template):")
        for o, sl in sorted(shared_here.items(), key=lambda z: -shared[z[0]])[:15]:
            print(f"  {shared[o]}x  '{o}'" + (f"  in this batch: {', '.join(sl)}" if a.only else ""))
            if not a.only:
                for f in sorted({source[s] for s in sl}): print(f"    {f}: {', '.join(s for s in sl if source[s] == f)}")
        if not a.only:
            nums = sorted({re.sub(r"\D", "", source[s]) for sl in shared_here.values() for s in sl})
            print(f"  rerun those batches so each opening is specific to its business: scripts/run_batches.py enrich --slug <slug> --only <num>, for {', '.join(nums)}")
    for s, errs in list(fails.items())[:60]:
        print(f"FAIL {s}: " + "; ".join(errs))
    if len(fails) > 60: print(f"... and {len(fails) - 60} more")
    if fails or a.partial:
        sys.exit(1 if fails else 0)

    out_cols = cols + [c for c in EXTRA if c not in cols] + keys + ["description_enriched"]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols); w.writeheader()
        for r in rows:
            x = answers[r["slug"]]
            for c in EXTRA: r.setdefault(c, "")
            for k in keys: r[k] = str(x["attributes"][k]).strip().lower()
            r["description_enriched"] = " ".join(x["description"].split())
            # A listing that now has a real description and five reviews or more is no longer thin.
            if r.get("thin") == "true" and int(float(r.get("reviews") or 0)) >= 5 and packets.get(r["slug"], {}).get("quotes"):
                r["thin"] = "false"
            w.writerow(r)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
