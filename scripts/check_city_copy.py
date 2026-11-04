#!/usr/bin/env python3
"""Helfer für Gate 5: die Stadttexte prüfen, bevor sie in city-copy.json wandern. Deutsche Fassung.

Liest die Antworten in 05-cache/city-copy/*.json (je ein JSON-Objekt: city_slug -> {intro:
[Absätze], faqs: [{q, a}]}), die Stadtpakete und das Faktenblatt.

Prüfungen je Stadt:
  - das Textgate (scripts/lint_copy.py): verbotene Wörter und Wendungen (umlauttolerant
    verglichen), keine Gedankenstriche, die Branchenbezeichnung im ersten Absatz, 4 bis 6 FAQs
    (2 bis 6 auf einer Kleinstadtseite, lint_copy.faq_band), jede Antwort 20 bis 120 Wörter
  - die Wortspanne der Stadtgröße: 500 bis 800 ab 10 Einträgen, 380 bis 800 bei 5 bis 9,
    250 bis 800 bei 3 oder 4, 120 bis 800 auf einer über foldMaxKm gehaltenen Kleinstadtseite
    (kleine Seiten werden nicht auf 500 aufgepolstert); die Spanne steht in der Zeile
    `intro band:` des Pakets
  - jede Zahl im Text steht im Paket dieser Stadt oder auf dem Faktenblatt. Deutsche und
    englische Schreibweise gelten als dieselbe Zahl: `4,8` im Text findet `4.8` im Paket,
    `1.200` und `1,200` sind beide 1200
  - keine Prozentangaben und keine Preise (kein €, kein $)
  - keine Formulierung darüber, wie das Verzeichnis gebaut wurde (Website-Fehler, Suchmaschinen,
    „Attribut", „Paket"), keine Zählung dessen, was die Einträge sagen
Über die Städte hinweg:
  - kein Satz einer Einleitung oder FAQ-Antwort kommt in drei oder mehr Städten vor
    (Textbaustein mit getauschtem Stadtnamen)
  - kein Satz ist in drei oder mehr Städten FAST gleich: teilt ein Satz (ab neun Wörtern,
    Stadtname entfernt) mindestens 75 % seiner Wörter mit je einem Satz aus zwei weiteren
    Städten, fällt er. Das trifft die schablonenhafte Wiederholung, die der Exakt-Vergleich
    verfehlt (ein Faktenblatt-Satz oder eine Bewertungszeile mit getauschten Zahlen), und war
    im Probelauf vom 04.11.2026 der Unterschied zwischen dem Gate-3-Modell und dem kleineren
  - kein Anfang (erste acht Wörter, Stadtname entfernt) wird von drei oder mehr Städten geteilt
  Gezählt wird über jede Antwortdatei in --copy plus den geprüften Stapel, damit ein mit --only
  geprüfter Stapel an den bereits geschriebenen gemessen wird. Berichtet werden nur die Städte des
  geprüften Stapels. Der vollständige Lauf (ohne --only, oder mit --write) nennt die Nummern der
  Stapel, die mit run_batches.py --only erneut laufen sollen.

Aufruf:
  python3 scripts/check_city_copy.py --copy output/<slug>/05-cache/city-copy --batches output/<slug>/05-cache/city-batches \
      --facts output/<slug>/05-fact-sheet.md --niche "Schlüsseldienste" [--only batch-03] [--write output/<slug>/site/src/data/city-copy.json]

--only prüft eine Antwortdatei gegen ihren eigenen Stapel. --write verlangt, dass jede Stadt
beantwortet ist und nichts durchfällt.
"""
import argparse, glob, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint_copy as lc  # noqa: E402

# Formulierungen, die zum Bau des Verzeichnisses gehören und nicht zu dem, was ein Kunde liest.
# Die Muster werden mit lc.fold_pattern umgeschrieben und auf den mit lc.fold_text gefalteten Text
# angewandt (ä/ae, ö/oe, ü/ue, ß/ss), deshalb dürfen sie Umlaute enthalten und treffen trotzdem
# beide Schreibweisen. Gemeldet wird die gefaltete Form des Treffers.
INTERNAL_SRC = (
    # Die Quelle nennen statt die Tatsache zu schreiben.
    r"laut (?:seiner |ihrer |der |eigener )?(?:web ?site|seite|homepage|angabe)|"
    r"auf (?:seiner|ihrer|der eigenen) (?:web ?site|seite|homepage)|"
    r"(?:die|seine|ihre) (?:web ?site|seite|homepage|eintrag) (?:sagt|nennt|listet|zeigt|erwähnt|führt|spricht)|"
    r"nach (?:eigenen )?angaben der (?:web ?site|seite)|den angaben zufolge|laut eintrag|im eintrag steht|"
    r"(?:bei|auf) google maps|google maps|im impressum|"
    # Nichts darüber, was fehlt oder unbekannt ist.
    r"(?:sagt|nennt|erwähnt|listet|schreibt) (?:dazu )?nichts|(?:sagt|nennt|erwähnt|listet) (?:das|es|dies) nicht|"
    r"keine angabe(?:n)? (?:dazu|auf|zu)|nichts (?:bekannt|hinterlegt|zu finden)|"
    r"(?:web ?site|seite) (?:war nicht|ist nicht|konnte nicht|liess sich nicht|ließ sich nicht)|"
    r"nicht (?:lesbar|erreichbar|gefunden|abrufbar)|ohne website|keine website|"
    # Nichts über den Bau des Verzeichnisses.
    r"\bpaket(?:e|s|en)?\b|\battribut(?:e|s|en)?\b|faktenblatt|\bnoindex\b|\bsitemap\b|suchmaschine(?:n)?|"
    r"serverfehler|fehlermeldung|zeitüberschreitung|\b40[34]\b|zum zeitpunkt der (?:erhebung|abfrage)|"
    r"(?:dieses verzeichnis|wir) (?:hat|haben) (?:das |diese )?nicht (?:geprüft|überprüft|kontrolliert)|"
    r"wie die seite (?:sortiert|geordnet) ist|reihenfolge der (?:karten|einträge)|"
    # Der Text handelt vom Ort und vom Gewerk, nicht vom Bestand an Einträgen (page-types).
    r"\bdie einträge (?:sagen|nennen|geben|zeigen|haben|führen|erwähnen)|"
    r"\d+ (?:einträge|einträgen)\b|von den \d+ (?:einträgen|betrieben)|"
    r"\b\d+ (?:NICHE_NOUNS|betriebe|firmen|unternehmen|anbieter|dienste|werkstätten|läden|von ihnen) "
    r"(?:sagen|geben|nennen|erwähnen|listen|führen|bieten|machen|haben|werben)\b|"
    # Vergleiche mit anderen Städten oder innerhalb des Stapels: jede Stadt steht für sich.
    r"(?:mehr|weniger|häufiger|seltener|größer|kleiner) als in (?:den |der |allen )?(?:meisten|anderen|übrigen|nachbarstädten)|"
    r"in dieser (?:gruppe|auswahl)|in diesem stapel|die meisten (?:anderen )?städte|andere städte|"
    # Die Lehre über Bewertung und Anzahl gehört in den Ratgeber, nicht auf jede Stadtseite.
    r"bewertung(?:en)? (?:immer )?(?:zusammen )?mit (?:der |den )?(?:anzahl|zahl der bewertungen)|"
    r"sagt (?:deutlich |weit )?weniger aus"
)
INTERNAL = re.compile(lc.fold_pattern(INTERNAL_SRC.replace("NICHE_NOUNS|", "")), re.I)


def set_niche(niche):
    """Die Substantive der Branche („Schlüsseldienste" -> schluesseldienst(e|en|es|s)?) in die
    Zählmuster aufnehmen, damit „17 Schlüsseldienste nennen" genauso auffällt wie „17 Betriebe
    nennen". Verglichen wird in der gefalteten Form."""
    global INTERNAL
    words = [w for w in re.findall(r"[a-zäöüß]+", (niche or "").lower()) if len(w) > 2]
    stems = set()
    for w in words[-1:]:                       # das Hauptwort der Bezeichnung
        stems.add(re.escape(lc.fold_text(w)).rstrip("e").rstrip("s") + "(?:e|en|es|s)?")
    if len(words) > 1:                         # und die ganze Bezeichnung
        stems.add(re.escape(lc.fold_text(" ".join(words))).rstrip("e").rstrip("s") + "(?:e|en|es|s)?")
    src = INTERNAL_SRC.replace("NICHE_NOUNS|", ("|".join(sorted(stems)) + "|") if stems else "")
    INTERNAL = re.compile(lc.fold_pattern(src), re.I)


NUM = re.compile(r"(?<![A-Za-z0-9#])\d+(?:[.,]\d+)*")
# Zahlwörter, die immer erlaubt sind (wie in der englischen Fassung die Ziffern 1 bis 12).
WORDNUM = {"eins": "1", "ein": "1", "eine": "1", "zwei": "2", "drei": "3", "vier": "4", "fünf": "5",
           "sechs": "6", "sieben": "7", "acht": "8", "neun": "9", "zehn": "10", "elf": "11", "zwölf": "12"}


def canon_number(tok):
    """Eine Zahl in eine Form bringen, in der deutsche und englische Schreibweise gleich sind:
    `1.200` und `1,200` werden 1200, `4,8` und `4.8` werden 4.8, `142` bleibt 142. So prüft die
    Zahlenprüfung den Wert und nicht das Trennzeichen."""
    t = tok.strip().rstrip(".,")
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", t):          # Tausendertrennzeichen
        return re.sub(r"[.,]", "", t)
    m = re.fullmatch(r"(\d+)[.,](\d+)", t)                 # Dezimalzahl
    if m:
        frac = m.group(2).rstrip("0")
        return m.group(1) + ("." + frac if frac else "")   # 4,0 und 4 sind dieselbe Zahl
    return re.sub(r"[.,]", "", t)


def numbers(text):
    return {canon_number(n) for n in NUM.findall(text or "")}


def load_packets(folder):
    packets, bands, names = {}, {}, {}
    for p in glob.glob(os.path.join(folder, "batch-*.md")):
        for block in re.split(r"\n(?=### )", open(p, encoding="utf-8").read()):
            m = re.match(r"### (\S+)\ncity: (.+)\n", block)
            if not m: continue
            slug = m.group(1); packets[slug] = block; names[slug] = m.group(2).strip()
            b = re.search(r"intro band: (\d+) to (\d+) words", block)
            bands[slug] = (int(b.group(1)), int(b.group(2))) if b else lc.CITY_WORDS
    return packets, bands, names


def main():
    ap = argparse.ArgumentParser(description="Gate 5: die Stadttexte prüfen (deutsch).")
    ap.add_argument("--copy", required=True); ap.add_argument("--batches", required=True); ap.add_argument("--facts", required=True)
    ap.add_argument("--niche", required=True, help='die Branchenbezeichnung, z. B. "Schlüsseldienste"')
    ap.add_argument("--only", default="", help="nur diese Antwortdatei prüfen, z. B. batch-03")
    ap.add_argument("--write", default="", help="bei fehlerfreiem Lauf city-copy.json schreiben")
    a = ap.parse_args()
    set_niche(a.niche)
    packets, bands, names = load_packets(a.batches)
    fact_nums = numbers(open(a.facts, encoding="utf-8").read())
    words, phrases = lc.load_bans()
    every = sorted(glob.glob(os.path.join(a.copy, "*.json")))
    files = [os.path.join(a.copy, a.only + ".json")] if a.only else every
    copy, fails, source = {}, defaultdict(list), {}
    for p in files:
        try: data = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"DURCHGEFALLEN {os.path.basename(p)}: kein gültiges JSON ({e})"); sys.exit(1)
        for slug, block in data.items():
            if slug in copy: fails[slug].append("zweimal geschrieben")
            copy[slug] = block; source[slug] = os.path.basename(p)
    # Die anderen, schon beantworteten Stapel: ihre Sätze und Anfänge gehen in die Zählung ein,
    # damit ein mit --only geprüfter Stapel sieht, was der übrige Lauf geschrieben hat; durchfallen
    # können daran aber nur die Städte des geprüften Stapels.
    others = {}
    for p in every:
        if os.path.realpath(p) in {os.path.realpath(f) for f in files}: continue
        try: data = json.load(open(p, encoding="utf-8"))
        except Exception: continue   # eine halb geschriebene Datei aus einem laufenden Lauf; ihre eigene Prüfung meldet das
        for slug, block in data.items():
            if slug not in copy: others[slug] = block; source[slug] = os.path.basename(p)
    expected = set(json.load(open(os.path.join(a.batches, a.only + ".slugs.json")))) if a.only else set(packets)
    for s in expected - set(copy):
        if a.only or a.write: fails[s].append("nicht geschrieben")
    sent_seen, opener_seen, total_words = defaultdict(set), defaultdict(set), 0
    sent_tokens = []   # (slug, frozenset(wörter)) je Satz ab neun Wörtern, für den Fast-gleich-Vergleich

    def tally(slug, block):
        """Die Sätze einer Stadt (Einleitung und FAQ-Antworten, ab neun Wörtern, Stadtname entfernt)
        und ihren Anfang in die gemeinsame Zählung geben. FAQ-Fragen bleiben außen vor: in
        verschiedenen Städten fragen die Leute dasselbe."""
        intro = [p for p in block.get("intro", []) if p.strip()]; faqs = block.get("faqs", [])
        name = lc.fold_text(names.get(slug, "\0"))
        body = "\n\n".join(intro) + "\n" + "\n".join(f.get("a", "") for f in faqs)
        for s in re.split(r"(?<=[.!?])\s+", body):
            words = re.sub(r"[^a-z0-9 ]", " ", lc.fold_text(s).replace(name, "")).split()
            if len(words) >= 9:
                sent_seen[" ".join(words)].add(slug)
                sent_tokens.append((slug, frozenset(words), " ".join(s.split())))
        if intro:
            k = " ".join(re.sub(r"[^a-z ]", "", lc.fold_text(intro[0]).replace(name, "")).split()[:8])
            opener_seen[k].add(slug)

    for slug, block in others.items(): tally(slug, block)
    for slug, block in copy.items():
        if slug not in packets: fails[slug].append("diese Stadt gibt es in den Paketen nicht"); continue
        intro = [p for p in block.get("intro", []) if p.strip()]; faqs = block.get("faqs", [])
        text = "\n\n".join(intro)
        gates, rep = lc.check_prose(text, words, phrases, niche=a.niche, band=bands[slug], label=slug)
        total_words += rep["words"]
        if not gates["in_der_wortspanne"]:
            fails[slug].append(f"Einleitung hat {rep['words']} Wörter, Spanne ist {bands[slug][0]} bis {bands[slug][1]}")
        if not gates["branche_im_ersten_absatz"]: fails[slug].append(f'"{a.niche}" steht nicht im ersten Absatz')
        if rep["forbidden_words"]: fails[slug].append(f"verbotene Wörter: {sorted(set(rep['forbidden_words']))}")
        if rep["forbidden_phrases"]: fails[slug].append(f"verbotene Wendungen: {sorted(set(rep['forbidden_phrases']))}")
        faq_lo, faq_hi = lc.faq_band(bands[slug])   # eine Kleinstadtseite mit einem oder zwei Einträgen trägt keine vier ehrlichen Fragen
        if not (faq_lo <= len(faqs) <= faq_hi): fails[slug].append(f"{len(faqs)} FAQs, nötig sind {faq_lo} bis {faq_hi}")
        everything = text + "\n" + "\n".join(f.get("q", "") + "\n" + f.get("a", "") for f in faqs)
        for i, f in enumerate(faqs, 1):
            n = lc.count_words(f.get("a", ""))
            if not (lc.FAQ_ANSWER_WORDS[0] <= n <= lc.FAQ_ANSWER_WORDS[1]):
                fails[slug].append(f"Antwort auf FAQ {i} hat {n} Wörter, Spanne ist {lc.FAQ_ANSWER_WORDS[0]} bis {lc.FAQ_ANSWER_WORDS[1]}")
            txt = f.get("a", "") + " " + f.get("q", "")
            bw = lc.find_words(txt, words); bp = lc.find_phrases(txt, phrases)
            if bw or bp: fails[slug].append(f"FAQ {i} verboten: {sorted(set(list(bw) + list(bp)))}")
        if re.search(r"[—–]| -- ", everything): fails[slug].append("Gedankenstrich als Satzzeichen")
        if "%" in everything or re.search(r"\bprozent\b", everything, re.I):
            fails[slug].append("Prozentangabe; nennen Sie die Anzahl aus dem Paket")
        if "€" in everything or "$" in everything or re.search(r"\beuro\b", everything, re.I):
            fails[slug].append("Preisangabe; Stadttexte nennen keine Preise (nur ein Betrieb, der seinen Preis selbst nennt, "
                               "und dann als dessen Angabe)")
        inside = sorted({m.group(0) for m in INTERNAL.finditer(lc.fold_text(everything))})
        if inside:
            fails[slug].append(f"interne Formulierung, die ein Kunde nicht lesen soll: {inside} (schreiben Sie, was der Betrieb "
                               "tut, lassen Sie den Betrieb aus dem Text, oder streichen Sie den Satz)")
        allowed = numbers(packets[slug]) | fact_nums | set(WORDNUM.values())
        bad = sorted(n for n in numbers(everything) if n not in allowed)
        if bad: fails[slug].append(f"Zahlen, die weder im Paket noch auf dem Faktenblatt stehen: {bad}")
        tally(slug, block)
    shared_batches = set()
    for kind, seen in (("Satz", sent_seen), ("Anfang", opener_seen)):
        for k, s in seen.items():
            if len(s) < 3: continue
            for slug in s:
                if slug not in copy: continue   # eine Stadt aus einem anderen Stapel: sie fällt in ihrer eigenen Prüfung durch
                where = sorted({source.get(o, "?") for o in s if o != slug})
                fails[slug].append(f'{kind} wird mit {len(s) - 1} anderen Städten geteilt '
                                   f'({", ".join(sorted(o for o in s if o != slug))}, in {", ".join(where)}): "{k[:80]}"')
                shared_batches |= {source[o] for o in s if o in source}

    # Fast gleiche Sätze (Jaccard der Wortmengen >= 0,75): ein Satz fällt, wenn er in zwei
    # weiteren Städten je einen Satz mit mindestens 75 % gemeinsamer Wörter hat (drei Städte
    # zusammen). Trifft die Schablone, die der Exakt-Vergleich verfehlt. Schwelle am Probelauf
    # vom 04.11.2026 kalibriert: Sonnet fiel bei 0,75 nicht, das kleinere Modell mit vierzehn
    # Sätzen in zwölf Städten. Nur Sätze aus den geprüften Städten (copy) fallen durch; Sätze aus
    # anderen Stapeln zählen als Vergleichsmenge mit.
    NEAR = 0.75
    # Kandidaten über einen invertierten Index auf die seltensten Tokens je Satz, damit die
    # Prüfung nicht jedes Satzpaar vergleicht (bei 800 Städten sonst zu langsam). Zwei Sätze mit
    # Jaccard >= 0,75 unterscheiden sich in höchstens einem Viertel der Tokens des kleineren; legt
    # man die (floor(0,25*n)+1) seltensten Tokens eines Satzes als Anker, teilt jeder solche
    # Partner mindestens einen Anker (Schubfachschluss). Keine Treffer gehen verloren.
    freq = Counter()
    for _, ts, _ in sent_tokens:
        for t in ts: freq[t] += 1
    index = defaultdict(list)   # token -> [Index in sent_tokens]
    anchors_of = []
    for idx, (_, ts, _) in enumerate(sent_tokens):
        n = len(ts)
        rare = sorted(ts, key=lambda t: (freq[t], t))[: n // 4 + 1]
        anchors_of.append(rare)
        for t in rare: index[t].append(idx)
    for i, (slug_i, ti, raw_i) in enumerate(sent_tokens):
        if slug_i not in copy:
            continue
        cand = {j for t in anchors_of[i] for j in index[t]}
        others = set()
        for j in cand:
            slug_j, tj, _ = sent_tokens[j]
            if slug_j == slug_i:
                continue
            u = ti | tj
            if u and len(ti & tj) / len(u) >= NEAR:
                others.add(slug_j)
        if len(others) >= 2:
            fails[slug_i].append(f'Satz ist in {len(others)} weiteren Städten fast gleich '
                                 f'({", ".join(sorted(others))}): "{raw_i[:80]}" – umschreiben, '
                                 f'damit diese Stadt eigenständig liest')
            shared_batches |= {source[o] for o in others if o in source}
    print(f"Städte geschrieben: {len(copy)}, durchgefallen: {len(fails)}, Wörter der Einleitungen insgesamt: {total_words}"
          + (f" (geteilte Sätze und Anfänge mitgezählt über {len(others)} Städte aus den anderen Stapeln)" if others else ""))
    for s, e in sorted(fails.items())[:80]: print(f"DURCHGEFALLEN {s}: " + "; ".join(e))
    if len(fails) > 80: print(f"... und {len(fails) - 80} weitere")
    if shared_batches and not a.only:
        nums = sorted(re.sub(r"\D", "", b) for b in shared_batches)
        print("Sätze oder Anfänge werden über Stapel hinweg geteilt; schreiben Sie sie in den Antwortdateien um, oder lassen Sie "
              "diese Stapel erneut laufen, damit jede Stadt als eigener Ort liest: "
              f"scripts/run_batches.py city-copy --slug <slug> --niche \"{a.niche}\" --only <nummer>, für {', '.join(nums)}")
    if fails: sys.exit(1)
    if a.write:
        out = {"_readme": "Bei Gate 5 aus den Stadtpaketen und dem Faktenblatt geschrieben. Geprüft von "
                          "scripts/check_city_copy.py. Nicht von Hand bearbeiten; bearbeiten Sie die Dateien in "
                          "05-cache/city-copy und lassen Sie die Prüfung mit --write laufen."}
        for slug in sorted(copy): out[slug] = {"intro": [p.strip() for p in copy[slug]["intro"] if p.strip()], "faqs": copy[slug]["faqs"]}
        json.dump(out, open(a.write, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{a.write} geschrieben")


if __name__ == "__main__":
    main()
