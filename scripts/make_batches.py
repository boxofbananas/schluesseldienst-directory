#!/usr/bin/env python3
"""Helfer für Gate 3: die Belegpakete in Stapel schneiden, die ein Anreicherungslauf in einem Zug
lesen kann.

Gruppiert die Einträge nach Stadt, hält eine Stadt zusammen, wo sie hineinpasst, und überspringt
jeden Eintrag, der im Zwischenspeicher schon eine Antwort hat; ein zweiter Lauf stapelt also nur
das Neue oder Fehlende. Jeder Stapel ist eine einfache Textdatei (kurze Zeilen, von oben nach
unten zu lesen) plus die Liste der Slugs.

Aufruf:
  python3 scripts/make_batches.py --evidence output/<slug>/03-cache/evidence \
      --enriched output/<slug>/03-cache/enriched --out output/<slug>/03-cache/batches \
      --attributes output/<slug>/03-attributes.json [--max-tokens 26000] [--max-listings 40] [--start 11]

Jede Stapeldatei beginnt mit der Merkmalstabelle aus der Merkmalsdatei dieser Branche (Schlüssel
und was ein „wahr" verlangt), damit scripts/enrichment-instructions.md allgemein bleibt und die
Regeln der Branche mit dem Stapel reisen.

**Die Schlüssel der Paketzeilen bleiben englisch** (`### <slug>`, `name:`, `city:`,
`site_status:`, `quotes:`, `description band: … words`): `scripts/enrichment-instructions.md`
verweist die Verfasser auf `description band:`, und `scripts/build_evidence.py` liefert die Werte
unter diesen Namen. Übersetzt sind Hilfe, Tabellenkopf und Meldungen.
"""
import argparse, glob, json, os, shutil, textwrap


def render(pk):
    L = [f"### {pk['slug']}", f"name: {pk['name']}", f"city: {pk['city']}",
         f"maps_type: {pk['maps_type']}", f"maps_subtypes: {pk['maps_subtypes']}"]
    stars = [str(int(float(x))) if str(x).strip() not in ("", "None") else "0" for x in pk["stars_1_to_5"]]
    def _int(x):
        try: return int(float(str(x)))
        except (ValueError, TypeError): return 0
    reviews = _int(pk["reviews"])
    rating = str(pk.get("rating") or "").strip()
    if reviews > 0 and rating:
        L.append(f"rating: {rating} from {reviews} reviews (1 star: {stars[0]}, 2: {stars[1]}, 3: {stars[2]}, 4: {stars[3]}, 5 star: {stars[4]})")
    else:
        # Nachgetragene eigene Betriebe haben kein öffentliches Profil und deshalb keine Bewertung
        # (wiki/framework/eigene-betriebe.md); nie eine erfinden.
        L.append("rating: none (no public reviews)")
    L.append(f"hours_posted: {'yes' if pk['has_hours'] else 'no'}")
    if pk.get("maps_about"): L.append("maps_about: " + "; ".join(pk["maps_about"]))
    if pk.get("maps_description"): L.append("maps_description: " + pk["maps_description"])
    L.append(f"site_status: {pk['site_status']}")
    for k in ("site_title", "site_meta"):
        if pk.get(k): L.append(f"{k}: {pk[k]}")
    for k in ("site_headings", "site_menu"):
        if pk.get(k): L += textwrap.wrap(f"{k}: " + " | ".join(pk[k]), 300, subsequent_indent="  ")
    if pk.get("quotes"):
        L.append(f"description band: {'80' if len(pk['quotes']) <= 2 else '120'} to 200 words")
        L.append("quotes (the patterns that found them are loose; read what the sentence says):")
        for k, qs in pk["quotes"].items():
            for q in qs: L += textwrap.wrap(f"  [{k}] {q}", 300, subsequent_indent="      ")
    else:
        L.append("description band: 50 to 90 words")
        L.append("quotes: none")
    return L


def attribute_table(attrs):
    L = ["## Merkmale dieses Verzeichnisses (jeden Schlüssel beantworten, in dieser Reihenfolge)", ""]
    L.append("| Schlüssel | „wahr\" nur, wenn die eigenen Worte des Betriebs das sagen |")
    L.append("|---|---|")
    for x in attrs:
        if x["key"].startswith("_"): continue
        tw = x.get("true_when") or x.get("label", "")
        if x.get("core"): tw += " (Kernarbeit: ist das falsch, sagt die Beschreibung klar, was der Betrieb stattdessen tut)"
        L.append(f"| `{x['key']}` | {tw} |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Gate 3: aus den Belegpaketen die Stapel für den Anreicherungslauf schneiden.",
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evidence", required=True, help="Ordner der Belegpakete, output/<slug>/03-cache/evidence")
    ap.add_argument("--enriched", required=True, help="Ordner der Antwortdateien, output/<slug>/03-cache/enriched; beantwortete Einträge werden übersprungen")
    ap.add_argument("--out", required=True, help="Ordner für die Stapel, output/<slug>/03-cache/batches")
    ap.add_argument("--attributes", required=True, help="die Merkmalsdatei dieser Branche (output/<slug>/03-attributes.json); ihre Tabelle steht oben in jedem Stapel")
    ap.add_argument("--max-tokens", type=int, default=26000, help="Obergrenze geschätzter Token je Stapel (Vorgabe 26000)")
    ap.add_argument("--max-listings", type=int, default=40, help="Obergrenze Einträge je Stapel (Vorgabe 40)")
    ap.add_argument("--start", type=int, default=1, help="Nummer des ersten Stapels, damit neue Stapel keine schon beantwortete Nummer wiederverwenden")
    a = ap.parse_args()
    attrs = json.load(open(a.attributes, encoding="utf-8"))
    if not isinstance(attrs, list) or not attrs or "key" not in attrs[0]:
        raise SystemExit(f"FEHLER: {a.attributes} ist keine Liste von Merkmalen (die Form steht in scripts/examples/README.md)")
    if not all(x.get("true_when") for x in attrs if not x["key"].startswith("_")):
        print(f"Hinweis: einigen Merkmalen in {a.attributes} fehlt die Zeile true_when; gedruckt wird dann die Bezeichnung. Ergänzen Sie je Merkmal eine, damit die Verfasser wissen, was ein „wahr\" verlangt.")
    table = attribute_table(attrs)
    done = set()
    for p in glob.glob(os.path.join(a.enriched, "*.json")):
        try: done |= {x["slug"] for x in json.load(open(p, encoding="utf-8"))}
        except Exception: pass
    cities = []
    for p in glob.glob(os.path.join(a.evidence, "*.json")):
        pks = [pk for pk in json.load(open(p, encoding="utf-8")) if pk["slug"] not in done]
        if pks: cities.append(pks)
    cities.sort(key=lambda c: (-len(c), c[0]["city"]))
    batches, cur, tok = [], [], 0
    for pks in cities:
        for pk in pks:
            lines = render(pk); t = sum(len(x) for x in lines) // 4 + 20
            if cur and (tok + t > a.max_tokens or len(cur) >= a.max_listings):
                batches.append(cur); cur, tok = [], 0
            cur.append((pk["slug"], lines)); tok += t
    if cur: batches.append(cur)
    os.makedirs(a.out, exist_ok=True)
    for p in glob.glob(os.path.join(a.out, "batch-*")):
        if int(os.path.basename(p)[6:9]) >= a.start: os.remove(p)
    for i, b in enumerate(batches, a.start):
        name = f"batch-{i:03d}"
        with open(os.path.join(a.out, name + ".md"), "w", encoding="utf-8") as f:
            f.write(f"# {name}: {len(b)} Einträge\n\n{table}\n\n## Einträge\n\n" + "\n\n".join("\n".join(l) for _, l in b) + "\n")
        with open(os.path.join(a.out, name + ".slugs.json"), "w", encoding="utf-8") as f:
            json.dump([s for s, _ in b], f)
    n = sum(len(b) for b in batches)
    print(f"schon beantwortet: {len(done)}, offen: {n} Einträge in {len(batches)} Stapeln")
    print("Einträge je Stapel:", [len(b) for b in batches])


if __name__ == "__main__":
    main()
