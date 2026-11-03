#!/usr/bin/env python3
"""Helfer für Gate 5: aus der Städtestruktur (05-cities.json, geschrieben von dump-cities.mjs der
Site) lesbare Pakete machen, gestapelt für den Lauf der Stadttexte.

Jede Zahl, die ein Verfasser verwenden darf, steht im Paket: check_city_copy.py verwirft jede
Zahl im Text, die nicht im Paket oder auf dem Faktenblatt steht.

Aufruf:
  python3 scripts/make_city_packets.py output/<slug>/05-cities.json --attributes output/<slug>/03-attributes.json \\
      --out output/<slug>/05-cache/city-batches --done output/<slug>/05-cache/city-copy \\
      --niche "Schlüsseldienste" [--bundesland "Bayern"] [--words-per-batch 4800] \\
      [--city-facts output/<slug>/05-city-facts.json]

Jeder Stapel beginnt mit der Zeile `directory:`, die Branche und Gebiet nennt, damit
scripts/city-copy-instructions.md allgemein bleibt. Diese Fassung hat drei Ebenen: Vorgabe für
das Gebiet ist **Deutschland**, und jede Stadt trägt ihr Bundesland in der Zeile `bundesland:`.
`--bundesland` ist nur für einen Lauf gedacht, der sich auf ein Land beschränkt. Orte unter der
Mindestzahl, die eine eigene Seite behalten (foldMaxKm), sind mit einer kürzeren Spanne dabei;
sie sind indexiert wie jede Stadtseite. Das Paket ist ortsbezogen aufgebaut (page-types): es
nennt, wozu das örtliche Gewerbe neigt, die Orte, die die Betriebe auf ihren eigenen Websites
als Arbeitsgebiet nennen, und wahlweise einen Block mit Stadtfakten. Es zählt nichts, was
unbekannt ist, denn der Text sagt nichts über Unbekanntes.

**Die Schlüssel der Paketzeilen bleiben englisch** (`### <slug>`, `city:`, `intro band: … words`,
`page type: small town`, `city facts:`, `directory:`). Zwei Leser hängen daran:
`scripts/check_city_copy.py` liest `### `, `city:` und `intro band:` mit festen Mustern
(`load_packets`), und `scripts/city-copy-instructions.md` verweist die Verfasser auf `directory:`,
`intro band:`, `page type: small town` und `city facts:`. Eine Übersetzung müsste beide Dateien
gleichzeitig ändern und brächte dem Betreiber nichts: er liest diese Zeilen nicht, er ruft nur
dieses Skript auf. Übersetzt sind deshalb Hilfe, Beispiele und Meldungen, nicht die Schlüssel.
"""
import argparse, glob, json, os, re, textwrap
from collections import Counter


def band(n):
    # Wortuntergrenzen nach Seitengröße (wiki/framework/page-types.md). Unter 3 Einträgen ist es
    # eine Ortsseite, die foldMaxKm freigestellt hat.
    return (120, 800) if n < 3 else (250, 800) if n < 5 else (380, 800) if n < 10 else (500, 800)


def first_sentences(text, k=3, cap=420):
    s = re.split(r"(?<=[.!?])\s+", (text or "").strip())
    return " ".join(s[:k])[:cap]


def places_named(c, place_names):
    """Orte und Kreise, die die Beschreibungen der Einträge nennen, außer der Stadt selbst: das
    Arbeitsgebiet, aus dem der ortsbezogene Text geschrieben wird. Deutsche Kreisbezeichnungen
    („Landkreis Bergstraße", „Kreis Groß-Gerau", „Rhein-Neckar-Kreis") zählen mit."""
    text = " ".join(l.get("description") or "" for l in c["listings"])
    found = Counter()
    # „Landkreis X", „Kreis X" mit nachgestelltem Namen (der Name endet am Satzzeichen) …
    for m in re.finditer(r"\b(Landkreis|Stadtkreis|Kreis)\s+([A-ZÄÖÜ][A-Za-zÄÖÜäöüß'-]*(?:[ -][A-ZÄÖÜ][A-Za-zÄÖÜäöüß'-]*){0,2})", text):
        found[f"{m.group(1)} {m.group(2)}"] += 1
    # … und „X-Kreis" mit vorangestelltem Namen (Rhein-Neckar-Kreis, Main-Taunus-Kreis).
    for m in re.finditer(r"\b([A-ZÄÖÜ][A-Za-zÄÖÜäöüß]+(?:-[A-ZÄÖÜ][A-Za-zÄÖÜäöüß]+)*-Kreis)\b", text):
        found[m.group(1)] += 1
    for name in place_names:
        if name == c["name"]:
            continue
        n = len(re.findall(r"(?<![A-Za-zÄÖÜäöüß])" + re.escape(name) + r"(?![A-Za-zÄÖÜäöüß])", text))
        if n:
            found[name] += n
    return found


def render(c, labels, place_names, facts):
    lo, hi = band(c["count"])
    L = [f"### {c['slug']}", f"city: {c['name']}"]
    if c.get("region"):
        L.append(f"bundesland: {c['region']}")
    L += [f"listings on this page: {c['count']}", f"intro band: {lo} to {hi} words"]
    if c.get("underFloor"):
        L.append("page type: small town with its own page (too far from a larger city to share one); 2 to 4 paragraphs, 2 to 6 FAQs")
    if facts.get(c["slug"]):
        L.append("city facts (each with its source; use what is here, add nothing):")
        L += [f"  - {x}" for x in facts[c["slug"]]]
    counties = Counter(l["county"] for l in c["listings"] if l["county"])
    L.append("Kreise der Einträge (aus den Postleitzahlen): " + (", ".join(f"{k} {v}" for k, v in counties.most_common()) or "keine zugeordnet"))
    towns = Counter(l["basedIn"] for l in c["listings"] if l["basedIn"] and l["basedIn"] != c["name"])
    if towns:
        L += textwrap.wrap("kleinere Orte, deren Einträge auf dieser Seite stehen: " + ", ".join(f"{k} {v}" for k, v in towns.most_common()), 300, subsequent_indent="  ")
    L.append(f"Google-Bewertungen aller Einträge zusammen: {c['totalReviews']}; Durchschnitt: {c['avgRating']:.1f}")
    L.append("wozu das örtliche Gewerbe neigt (Einträge, die es auf ihrer eigenen Website angeben): " + ", ".join(f"{labels[k]} {v}" for k, v in c["attrCounts"].items() if v and k in labels))
    pl = places_named(c, place_names)
    if pl:
        L += textwrap.wrap("Orte, die die Websites der Einträge als Arbeitsgebiet nennen (Erwähnungen): " + ", ".join(f"{k} {v}" for k, v in pl.most_common(20)), 300, subsequent_indent="  ")
    L.append("Nachbarstädte mit eigener Seite: " + (", ".join(f"{n['name']} {n['count']}" for n in c["nearby"]) or "keine"))
    L.append("Einträge, in der Reihenfolge der Seite:")
    for l in c["listings"]:
        head = f"  {l['position']}. {l['name']} | {l['rating']:.1f} aus {l['reviews']} Bewertungen"
        if l["basedIn"] and l["basedIn"] != c["name"]:
            head += f" | sitzt in {l['basedIn']}"
        if l["county"]:
            head += f" | {l['county']}"
        L.append(head)
        L += textwrap.wrap("     ja: " + (", ".join(labels[k] for k in l["yes"]) or "nichts angegeben") + (" | nein: " + ", ".join(labels[k] for k in l["no"]) if l["no"] else ""), 300, subsequent_indent="       ")
        if l["position"] <= 20 and l.get("description"):
            L += textwrap.wrap("     Notiz: " + first_sentences(l["description"]), 300, subsequent_indent="       ")
    return L


def main():
    ap = argparse.ArgumentParser(description="Gate 5: aus 05-cities.json die Stadtpakete für die Stadttexte stapeln.",
                                 epilog="Beispiel:\n  python3 scripts/make_city_packets.py output/<slug>/05-cities.json "
                                        "--attributes output/<slug>/03-attributes.json --out output/<slug>/05-cache/city-batches "
                                        "--done output/<slug>/05-cache/city-copy --niche \"Schlüsseldienste\"",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cities", help="die Städtestruktur: output/<slug>/05-cities.json, von node dump-cities.mjs geschrieben")
    ap.add_argument("--attributes", required=True, help="die Merkmalsdatei output/<slug>/03-attributes.json (ihre Bezeichnungen stehen in den Paketen)")
    ap.add_argument("--out", required=True, help="Ordner für die Stapel, output/<slug>/05-cache/city-batches")
    ap.add_argument("--done", required=True, help="Ordner mit den schon beantworteten Stapeln, output/<slug>/05-cache/city-copy; "
                                                 "diese Städte werden übersprungen")
    ap.add_argument("--words-per-batch", type=int, default=4800, help="wie viele Wörter Text ein Stapel kosten darf (Vorgabe 4800)")
    ap.add_argument("--start", type=int, default=1, help="Nummer des ersten Stapels, damit neue Stapel keine schon beantwortete Nummer wiederverwenden")
    ap.add_argument("--niche", required=True, help='die Branchenbezeichnung, die der erste Absatz tragen muss, z. B. "Schlüsseldienste"')
    ap.add_argument("--bundesland", "--state", default="", dest="bundesland",
                    help="nur für einen Lauf, der sich auf ein Bundesland beschränkt: dessen Name steht dann in der Zeile "
                         "`directory:`. Vorgabe ist das ganze Land; das Bundesland jeder Stadt steht ohnehin in ihrer Zeile "
                         "`bundesland:`")
    ap.add_argument("--land", default="Deutschland", help="das Gebiet in der Zeile `directory:`, wenn kein Bundesland angegeben ist (Vorgabe: Deutschland)")
    ap.add_argument("--city-facts", default="", help="wahlweise eine JSON-Datei {stadt-slug: [\"Tatsache (Quelle)\", …]}, die als Block mit Stadtfakten ins Paket kommt")
    a = ap.parse_args()
    facts = json.load(open(a.city_facts, encoding="utf-8")) if a.city_facts else {}
    labels = {x["key"]: x["label"] for x in json.load(open(a.attributes, encoding="utf-8")) if not x["key"].startswith("_")}
    cities = json.load(open(a.cities, encoding="utf-8"))   # jede Seite, die gebaut wird, Ortsseiten eingeschlossen
    place_names = sorted({c["name"] for c in cities} | {l["basedIn"] for c in cities for l in c["listings"] if l.get("basedIn")}, key=len, reverse=True)
    gebiet = a.bundesland.strip() or a.land.strip()
    header = f"directory: {a.niche}" + (f" in {gebiet}" if gebiet else "")
    done = set()
    for p in glob.glob(os.path.join(a.done, "*.json")):
        try:
            done |= set(json.load(open(p, encoding="utf-8")).keys())
        except Exception:
            pass
    todo = [c for c in cities if c["slug"] not in done]
    batches, cur, w = [], [], 0
    for c in todo:
        target = {120: 160, 250: 320, 380: 460, 500: 620}[band(c["count"])[0]] + 330
        if cur and w + target > a.words_per_batch:
            batches.append(cur); cur, w = [], 0
        cur.append(c); w += target
    if cur:
        batches.append(cur)
    os.makedirs(a.out, exist_ok=True)
    for p in glob.glob(os.path.join(a.out, "batch-*")):
        if int(os.path.basename(p)[6:8]) >= a.start:
            os.remove(p)
    for i, b in enumerate(batches, a.start):
        name = f"batch-{i:02d}"
        with open(os.path.join(a.out, name + ".md"), "w", encoding="utf-8") as f:
            f.write(f"# {name}: {len(b)} Städte\n{header}\n\n" + "\n\n".join("\n".join(render(c, labels, place_names, facts)) for c in b) + "\n")
        json.dump([c["slug"] for c in b], open(os.path.join(a.out, name + ".slugs.json"), "w"))
    towns = sum(1 for c in cities if c.get("underFloor"))
    print(f"Seiten: {len(cities)} (davon {towns} Ortsseiten unter der Mindestzahl), schon geschrieben: {len(cities) - len(todo)}, "
          f"offen: {len(todo)} in {len(batches)} Stapeln")
    print("Städte je Stapel:", [len(b) for b in batches])


if __name__ == "__main__":
    main()
