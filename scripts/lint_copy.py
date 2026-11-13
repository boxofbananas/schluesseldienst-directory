#!/usr/bin/env python3
"""
lint_copy.py, das Textgate für Gate 5 des Verzeichnis-Baukastens, deutsche Fassung.

Führt die Prüfungen des Linters aus skills/seo-content-engine auf den **kurzen** Texten aus, die
die Skill selbst nicht schreibt: die Stadtblöcke und FAQs in city-copy.json, die Blöcke „Über uns"
und Ratgeber in den .astro-Seiten und jede Markdown-Datei. Keine Abfrage bei DataForSEO, nur
Standardbibliothek.

Aufruf:
    python3 scripts/lint_copy.py output/<slug>/site/src/data/city-copy.json --niche "Schlüsseldienste"
    python3 scripts/lint_copy.py output/<slug>/site/src/pages/ueber-uns.astro --min-words 300 --max-words 500
    python3 scripts/lint_copy.py output/<slug>/site/src/pages/index.astro --min-words 800 --max-words 1200 --niche "Schlüsseldienste"
    python3 scripts/lint_copy.py output/<slug>/site/src/pages/ratgeber/<slug>.md --min-words 1200 --niche "..."
    --json für maschinenlesbare Ausgabe

    python3 scripts/lint_copy.py output/<slug>/site/dist/index.html --min-words 800 --max-words 1200 --niche "Schlüsseldienste"

Eine gebaute .html-Seite wird auf dem Text innerhalb von <main> geprüft: auf dem, was der Besucher
liest, einschließlich der Texte aus site.json und den Daten. Dieser Weg ist dem .astro-Quelltext
vorzuziehen, sobald eine Seite Texte aus Daten zieht.

Eine .astro-Seite wird als Ganzes geprüft (ihre festen Absätze plus der Block aus Gate 5), die
Wortspanne ist also die Seitenspanne aus wiki/framework/page-types.md, nicht die Blockspanne.

Mit --city-sizes (eine JSON-Datei, die city_slug auf die Zahl der Einträge abbildet) bekommt jede
Stadtseite die Spanne ihrer Größenklasse aus wiki/framework/page-types.md: 500 bis 800 Wörter und
4 bis 6 FAQs ab 10 Einträgen, 380 bis 800 bei 5 bis 9, 250 bis 800 bei 3 oder 4, und auf einer
Kleinstadtseite (1 oder 2 Einträge, über foldMaxKm gehalten) 120 bis 800 Wörter und 2 bis 6 FAQs.
Der Bericht markiert jede Seite unter 10 Einträgen als kleine Stadt. Ohne --city-sizes braucht jede
Stadt 500 Wörter und 4 FAQs. check_city_copy.py liest dieselben Klassen aus den Spannenzeilen der
Pakete und verwendet faq_band() aus dieser Datei, damit beide Prüfungen übereinstimmen.

Deutsche Besonderheiten dieser Fassung:
- **Wortzählung:** Umlaute, ß und zusammengesetzte Wörter mit Bindestrich zählen richtig.
  „Schlüsseldienst" ist ein Wort, „Schlüssel-Notdienst" ebenfalls. Die englische Zählung über
  [A-Za-z0-9]+ hätte aus jedem Wort mit Umlaut zwei gemacht.
- **Lesbarkeit:** Flesch-Lesbarkeitsindex in der deutschen Anpassung nach Amstad
  (180 - Satzlänge - 58,5 × Silben je Wort; höher ist leichter, etwa 60 bis 70 bei
  Gebrauchsprosa). Dazu der Anteil der Wörter mit drei Silben und mehr. Beides wird nur
  **berichtet**, nicht erzwungen (Regel der Skill).
- **Verbotene Wörter** werden umlauttolerant verglichen (ä/ae, ö/oe, ü/ue, ß/ss), damit
  „zuverlässig" auch „zuverlaessig" findet.
- **Wortstämme:** ein Listeneintrag, der auf `*` endet, ist ein Stamm und trifft jede
  Fortsetzung. `lizenzier*` fängt „lizenziert", „lizenzierte" und „Lizenzierung". Ohne das
  entging dem Gate jede gebeugte Form, weil nur Grundformen in den Listen stehen.

Prüfungen je Stadtblock: Wortspanne und FAQ-Zahl der Größenklasse, jede FAQ-Antwort 20 bis 120
Wörter, die Branchenbezeichnung im ersten Absatz, keine verbotenen Wörter oder Wendungen (die
Liste der Skill plus scripts/copy-bans.txt), keine Gedankenstriche. Beendet mit 1, sobald eine
Prüfung durchfällt: prüfen, beheben, erneut prüfen.

Die **Rechtswörter** („lizenziert", „zugelassen", „Kammer", „amtlich", „Testsieger" …) stehen in
beiden Listen in einem eigenen Block ([RECHTSWOERTER] und [RECHTSWENDUNGEN]) und lassen sich für
eine einzelne Seite mit `--erlaube-rechtswoerter` zulassen. Das ist nötig, weil
`/festpreis-garantie/`, `/premium/`, `/agb/` und Ratgeberseiten über die Rechtslage genau diese
Wörter brauchen, um sie zu bestreiten („es gibt keine Lizenz und keine Meisterpflicht"). Wofür
der Schalter gilt und wofür nie, steht in wiki/seo/copy-gate.md; die Werbefloskeln bleiben in
jedem Fall verboten.

**„Garantie" und „garantiert"** stehen seit dem 2026-11-03 als Stamm `garantie*` im selben Block:
ohne Schalter gemeldet, mit Schalter zugelassen. Einzige Ausnahme ist der Name des Programms,
**„Festpreis-Garantie"** in genau dieser Schreibweise mit Bindestrich: ihn verlangt
wiki/konventionen.md auf jedem Eintrag, auf jeder Stadtkarte und auf der Startseite, also wird er
vor dem Vergleich aus dem Text genommen (PROGRAMMNAME). Jede andere Form („garantiert",
„Garantie", „Festpreisgarantie" ohne Bindestrich) bleibt ohne Schalter ein Treffer.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL_SCRIPTS = os.path.join(ROOT, "skills", "seo-content-engine", "scripts")
SKILL_FORBIDDEN = os.path.join(ROOT, "skills", "seo-content-engine", "references", "forbidden_words.txt")
LOCAL_BANS = os.path.join(HERE, "copy-bans.txt")

sys.path.insert(0, SKILL_SCRIPTS)
try:
    import lint_article as la  # noqa: E402
except ImportError:
    print(f"FEHLER: die Skill seo-content-engine fehlt unter {SKILL_SCRIPTS}. Entpacken Sie den Baukasten erneut.")
    sys.exit(2)

CITY_WORDS = (500, 800)
TOWN_WORDS = (120, 800)     # Kleinstadtseite mit 1 oder 2 Einträgen, über foldMaxKm gehalten (page-types)
FAQ_COUNT = (4, 6)
TOWN_FAQ_COUNT = (2, 6)     # dieselbe Seite: zwei ehrliche Fragen sind besser als vier aufgefüllte
FAQ_ANSWER_WORDS = (20, 120)

UMLAUTE = (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"),
           ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"))

# Ein deutsches Wort: Buchstaben mit Umlauten und ß, Ziffern, und durchgekoppelte
# Zusammensetzungen bleiben ein Wort (Schlüssel-Notdienst, 24-Stunden-Notdienst).
WORD = re.compile(r"[0-9A-Za-zÄÖÜäöüßÀ-ÿ]+(?:[-'’][0-9A-Za-zÄÖÜäöüßÀ-ÿ]+)*")
VOWELS = "aeiouyäöü"
# Der Name des Garantie-Programms (wiki/konventionen.md, Abschnitt „Festpreis-Garantie"). Er steht
# auf jedem Eintrag und auf der Startseite und ist deshalb kein Treffer für `garantie*`; jede
# andere Schreibweise bleibt einer. Verglichen wird auf dem gefalteten Text (fold_text).
PROGRAMMNAME = re.compile(r"\bfestpreis-garantie\b")

# Deutsche Doppellaute, die eine Silbe bilden.
DIPHTHONGS = ("eau", "äu", "au", "ei", "ai", "eu", "ie", "oi", "ui")


def fold_text(s):
    """Vergleichsform eines Textes: Kleinbuchstaben, Umlaute umgeschrieben (ä/ae, ö/oe, ü/ue,
    ß/ss), übrige Akzente entfernt. Satzzeichen und Leerzeichen bleiben, damit Wortgrenzen (\\b)
    weiter gelten."""
    s = s or ""
    for a, b in UMLAUTE:
        s = s.replace(a, b)
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def fold_pattern(p):
    """Dasselbe für eine Mustervorlage, aber **ohne** Kleinschreibung: ein `\\D` darf nicht zu
    `\\d` werden. Groß- und Kleinschreibung erledigt re.I."""
    for a, b in UMLAUTE:
        p = p.replace(a, b)
    return p


SECTIONS = {
    "[WORDS]": ("words", "floskeln"),
    "[PHRASES]": ("phrases", "floskeln"),
    "[RECHTSWOERTER]": ("words", "recht"),
    "[RECHTSWENDUNGEN]": ("phrases", "recht"),
}


def parse_bans(path):
    """Eine Verbotsliste in ihre vier Fächer lesen: Wörter und Wendungen, je in der Gruppe
    „floskeln" (Werbesprache, immer verboten) und „recht" (Behauptungen über Zulassung,
    Lizenz oder eine amtliche Stelle). Rückgabe {("words"|"phrases", Gruppe): [Einträge]}.
    Eine fehlende Datei ist keine Ausnahme, sondern eine Warnung: dann prüft das Gate weniger,
    statt gar nicht zu laufen (Regel der Skill)."""
    out = {k: [] for k in SECTIONS.values()}
    if not os.path.exists(path):
        print(f"WARNUNG: Verbotsliste nicht gefunden: {path} – diese Prüfung entfällt.")
        return out
    fach = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            head = SECTIONS.get(line.upper())
            if head:
                fach = head
                continue
            if fach:
                out[fach].append(line.lower())
    return out


def load_bans(erlaube_rechtswoerter=False):
    """Die beiden Listen (Skill und Baukasten) zu einem Paar (Wörter, Wendungen) zusammenziehen.
    Mit erlaube_rechtswoerter=True bleibt der Block der Rechtswörter außen vor – nur für die
    Seiten, die in wiki/seo/copy-gate.md genannt sind."""
    words, phrases = [], []
    for path in (SKILL_FORBIDDEN, LOCAL_BANS):
        fach = parse_bans(path)
        words += fach[("words", "floskeln")]
        phrases += fach[("phrases", "floskeln")]
        if not erlaube_rechtswoerter:
            words += fach[("words", "recht")]
            phrases += fach[("phrases", "recht")]
    # Beide Listen führen einen Teil der Einträge doppelt (die Rechtswörter stehen absichtlich in
    # beiden). Entdoppeln, damit der Bericht jeden Treffer einmal nennt.
    return list(dict.fromkeys(words)), list(dict.fromkeys(phrases))


def count_words(text):
    """Wörter zählen, deutsch: Umlaute und ß gehören zum Wort, eine Zusammensetzung mit Bindestrich
    ist ein Wort."""
    return len(WORD.findall(text or ""))


def count_syllables(word):
    """Näherung für die Silbenzahl eines deutschen Wortes: Vokalgruppen zählen, Doppellaute als
    eine Silbe. Für einen Lesbarkeitsindex genügt eine über den ganzen Text stabile Schätzung."""
    w = fold_text(word)
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 0
    # Doppellaute vorweg durch einen einzelnen Vokal ersetzen, damit sie eine Silbe ergeben.
    w = w.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü")
    for d in DIPHTHONGS:
        w = w.replace(d, "a")
    return max(len(re.findall(r"[aeiouyäöü]+", w)), 1)


def readability_de(text):
    """Flesch-Lesbarkeitsindex in der deutschen Anpassung nach Amstad:
    180 - Wörter je Satz - 58,5 × Silben je Wort. Höher ist leichter zu lesen; Gebrauchsprosa
    liegt etwa bei 60 bis 70. Nur ein Bericht, kein Gate."""
    sentences = [s for s in re.split(r"[.!?]+", text or "") if s.strip()]
    words = WORD.findall(text or "")
    if not sentences or not words:
        return 0.0, 0.0
    syll = [count_syllables(w) for w in words]
    index = 180 - (len(words) / len(sentences)) - 58.5 * (sum(syll) / len(words))
    hard = sum(1 for n in syll if n >= 3) / len(words)
    return round(index, 1), round(hard * 100, 1)


def stem_pattern(token):
    """Das Vergleichsmuster eines einzelnen Listeneintrags oder Wendungsteils, umlauttolerant
    gefaltet. Endet der Eintrag auf `*`, gilt er als **Wortstamm** und trifft jede Fortsetzung:
    aus `lizenzier*` wird `\\blizenzier\\w*`, und das findet „lizenziert", „lizenzierte" und
    „Lizenzierung". Ohne Stern bleibt es beim ganzen Wort zwischen zwei Wortgrenzen."""
    t = fold_text(token).strip()
    if t.endswith("*"):
        return r"\b" + re.escape(t[:-1]) + r"\w*"
    return r"\b" + re.escape(t) + r"\b"


def find_words(prose, words):
    """Verbotene ganze Wörter und Wortstämme, umlauttolerant verglichen. Rückgabe wie bei der
    Skill: {Eintrag: Anzahl}, der Schlüssel in der Schreibweise der Verbotsliste (mit Stern,
    damit im Bericht steht, welche Zeile der Liste angeschlagen hat)."""
    hits = {}
    low = PROGRAMMNAME.sub(" ", fold_text(prose))
    for w in words:
        n = len(re.findall(stem_pattern(w), low))
        if n:
            hits[w] = n
    return hits


def find_phrases(prose, phrases):
    """Verbotene Wendungen, umlauttolerant und mit bis zu sechs Füllwörtern zwischen den Teilen,
    damit „Ihr zuverlässiger Partner für" als „Ihr Partner für" erkannt wird."""
    hits = {}
    low = PROGRAMMNAME.sub(" ", fold_text(prose))
    for p in phrases:
        toks = fold_text(p).split()
        if not toks:
            continue
        if len(toks) == 1:
            pattern = stem_pattern(toks[0])
        else:
            # Jeder Teil darf ein Stamm sein (`staatlich anerkannt*` findet „staatlich
            # anerkannter Betrieb"); zwischen den Teilen bleiben bis zu sechs Füllwörter.
            inner = [re.escape(t[:-1]) + r"\w*" if t.endswith("*") else re.escape(t) for t in toks]
            pattern = r"\b" + r"\W+(?:\w+\W+){0,6}?".join(inner) + (r"" if toks[-1].endswith("*") else r"\b")
        n = len(re.findall(pattern, low))
        if n:
            hits[p] = n
    return hits


def astro_to_text(raw):
    """Nur den lesbaren Text einer .astro-Seite behalten: Frontmatter, Tags, Kommentare und
    Vorlagenausdrücke fallen weg."""
    raw = re.sub(r"^---.*?---", "", raw, count=1, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"\{[^{}]*\}", " ", raw)
    raw = re.sub(r"</?(p|h[1-6]|li|section|div|br)[^>]*>", "\n\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    return raw


def html_to_text(raw):
    """Eine gebaute Seite aus dist/: den Text innerhalb von <main> behalten, also das, was der
    Besucher liest. Kopf, Fuß, Skripte, Stile und JSON-LD bleiben außen vor."""
    # Der Seitenkopf (H1, Vorspann) steht in einem eigenen Band über <main> und gehört zum Text.
    m = re.search(r'(<div class="page-head.*?)?<main[^>]*>(.*?)</main>', raw, flags=re.S)
    raw = ((m.group(1) or "") + m.group(2)) if m else raw
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
    # Eine Seite kann einen Block, der kein Text ist (das Städteverzeichnis), mit copy:skip ausnehmen.
    raw = re.sub(r"<!-- copy:skip -->.*?<!-- /copy:skip -->", " ", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    # Navigation ist kein Text: Brotkrumen und Listen von Stadtlinks zählen nicht mit.
    raw = re.sub(r"<nav[^>]*>.*?</nav>", " ", raw, flags=re.S)
    raw = re.sub(r'<ul class="city-grid"[^>]*>.*?</ul>', " ", raw, flags=re.S)
    raw = re.sub(r"</?(p|h[1-6]|li|section|div|br|dt|dd|article|aside|ul|ol|dl)[^>]*>", "\n\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    for ent, ch in (("&amp;", "&"), ("&quot;", '"'), ("&#39;", "'"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&nbsp;", " "), ("&auml;", "ä"), ("&ouml;", "ö"), ("&uuml;", "ü"), ("&szlig;", "ß"),
                    ("&Auml;", "Ä"), ("&Ouml;", "Ö"), ("&Uuml;", "Ü"), ("&euro;", "€")):
        raw = raw.replace(ent, ch)
    return raw


def md_to_text(raw):
    raw = re.sub(r"^---.*?---", "", raw, count=1, flags=re.S)
    return la.strip_markdown(raw)


# --- Zahlenprüfung gegen die Faktensammlung (05-fact-sheet.md) -------------------------------
# Die Lehre aus dem Nachtlauf: Das Textgate prüft Wörter, nicht Tatsachen. Eine Ratgeberseite,
# die aus einer Faktensammlung entsteht, darf keine Zahl tragen, die dort nicht mit Quelle und
# Abrufdatum steht. Geprüft werden die vier Kategorien des Auftrags: Euro-Beträge, Prozente,
# Jahreszahlen und Gerichts-/Aktenzeichen. Normkennungen (DIN, EN, RC), Maße (mm), Notruf- und
# Programmnummern sind Bezeichner, keine belegpflichtigen Tatsachenzahlen, und bleiben außen vor.
_URL_RE = re.compile(r"https?://\S+")
_NUM = r"\d{1,3}(?:\.\d{3})*(?:,\d+)?"
_CONN = r"(?:\s*(?:bis|und|oder|beziehungsweise|bzw\.?|je|–|-|/|,)\s*" + _NUM + r")*"
# Eine Geldkette ist eine oder mehrere durch „bis/und/oder …" verbundene Zahlen vor Euro/%,
# damit „60 bis 150 Euro" beide Zahlen prüft, nicht nur die letzte.
_EURO_RE = re.compile(r"(" + _NUM + _CONN + r")\s*(?:€|Euro|EUR)\b", re.I)
_PERCENT_RE = re.compile(r"(" + _NUM + _CONN + r")\s*(?:%|Prozent)\b", re.I)
_NUM_RE = re.compile(_NUM)
_YEAR_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
_COURT_RE = re.compile(
    r"(?:Amts|Land|Ober(?:landes)?|Verwaltungs|Sozial|Arbeits|Bundes)gericht[a-zäöüß]*\s+"
    r"[A-ZÄÖÜ][a-zäöüß.\-]+"
    r"|Aktenzeichen\s*:?[\s\w./-]{2,30}"
    r"|(?<!\d)\d{1,3}\s?[A-Za-z]{1,3}\s?\d{1,5}/\d{2,4}\b")


def _num_token_in_facts(num, facts):
    """Steht die Zahl als eigenständiges Token im Faktenblatt (nicht Teil einer längeren Zahl
    oder einer URL-Ziffernfolge)?"""
    return bool(re.search(r"(?<![\d.,])" + re.escape(num) + r"(?![\d.,])", facts))


def numbers_not_in_facts(prose, facts):
    """Zahlen der vier Auftragskategorien, die nicht in der Faktensammlung belegt sind.
    Rückgabe: Liste lesbarer Fundstellen (ohne Dopplungen)."""
    text = _URL_RE.sub(" ", prose)
    missing, seen = [], set()

    def add(disp, key):
        if key not in seen:
            seen.add(key)
            missing.append(disp)

    for m in _EURO_RE.finditer(text):
        for n in _NUM_RE.findall(m.group(1)):
            if not _num_token_in_facts(n, facts):
                add(f"{n} Euro", ("e", n))
    for m in _PERCENT_RE.finditer(text):
        for n in _NUM_RE.findall(m.group(1)):
            if not _num_token_in_facts(n, facts):
                add(f"{n} Prozent", ("p", n))
    for m in _YEAR_RE.finditer(text):
        n = m.group(0)
        if not _num_token_in_facts(n, facts):
            add(f"Jahr {n}", ("y", n))
    for m in _COURT_RE.finditer(text):
        ref = re.sub(r"\s+", " ", m.group(0)).strip().rstrip(".,;")[:40]
        if fold_text(ref) not in fold_text(facts):
            add(f"Gericht/Az.: {ref}", ("c", ref.lower()))
    return missing


def check_prose(prose, words, phrases, niche=None, band=None, label=""):
    """Gemeinsame Prüfungen für einen Textblock. Rückgabe (gates, report)."""
    wc = count_words(prose)
    word_hits = find_words(prose, words)
    phrase_hits = find_phrases(prose, phrases)
    em_dashes = prose.count("—") + prose.count("–") + prose.count(" -- ")
    first_para = next((p for p in re.split(r"\n\s*\n", prose) if p.strip()), "")
    index, hard = readability_de(prose)
    gates = {
        "keine_verbotenen_woerter": not word_hits,
        "keine_verbotenen_wendungen": not phrase_hits,
        "keine_gedankenstriche": em_dashes == 0,
    }
    if band:
        gates["in_der_wortspanne"] = band[0] <= wc <= band[1]
    if niche:
        gates["branche_im_ersten_absatz"] = fold_text(niche) in fold_text(first_para)
    report = {
        "label": label,
        "words": wc,
        "lesbarkeit": index,
        "schwere_woerter_prozent": hard,
        "forbidden_words": word_hits,
        "forbidden_phrases": phrase_hits,
        "em_dashes": em_dashes,
        "gates": gates,
    }
    return gates, report


def city_band(n):
    """Wortspanne nach der Zahl der Einträge auf der Stadtseite (die Größenklassen aus
    page-types.md). Eine Seite mit drei Einträgen trägt keine 500 ehrlichen Wörter, kleine Städte
    bekommen deshalb eine niedrigere Untergrenze statt Füllmaterial."""
    if n is None or n >= 10:
        return CITY_WORDS
    return TOWN_WORDS if n < 3 else (250, CITY_WORDS[1]) if n < 5 else (380, CITY_WORDS[1])


def faq_band(band):
    """Die FAQ-Zahl zur Wortspanne: eine Kleinstadtseite (Untergrenze 120) trägt 2 bis 6, jede
    andere Stadtseite 4 bis 6. check_city_copy.py ruft das mit der Spanne aus dem Paket auf."""
    return TOWN_FAQ_COUNT if band[0] < 250 else FAQ_COUNT


def build_city_sizes(cities_path, city_sizes_path):
    """Die Größenkarte Stadtschlüssel -> Zahl der Einträge. Aus 05-cities.json wird sie bei
    jedem Lauf FRISCH gebaut (regionSlug/slug -> count), damit keine zu pflegende Datei
    veraltet. --city-sizes bleibt als vorgefertigte Datei für Sonderfälle. Gibt None, wenn
    keine Quelle genannt ist."""
    if cities_path:
        data = json.load(open(cities_path, encoding="utf-8"))
        return {f"{c['regionSlug']}/{c['slug']}": c.get("count") for c in data}
    if city_sizes_path:
        return json.load(open(city_sizes_path, encoding="utf-8"))
    return None


def lint_city_copy(path, niche, words, phrases, sizes=None):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    reports = []
    for slug, block in data.items():
        if slug.startswith("_"):
            continue
        intro = "\n\n".join(block.get("intro", []))
        faqs = block.get("faqs", [])
        band = city_band((sizes or {}).get(slug))
        fband = faq_band(band)
        gates, rep = check_prose(intro, words, phrases, niche=niche, band=band, label=slug)
        rep["band"] = band
        rep["faq_band"] = fband
        gates["faq_anzahl"] = fband[0] <= len(faqs) <= fband[1]
        bad_answers = []
        for i, fq in enumerate(faqs):
            a = fq.get("a", "")
            n = count_words(a)
            if not (FAQ_ANSWER_WORDS[0] <= n <= FAQ_ANSWER_WORDS[1]):
                bad_answers.append(f"FAQ {i + 1}: {n} Wörter, Spanne {FAQ_ANSWER_WORDS[0]} bis {FAQ_ANSWER_WORDS[1]}")
            fw = find_words(a, words)
            fp = find_phrases(a, phrases)
            if fw or fp:
                bad_answers.append(f"FAQ {i + 1}: verboten {list(fw) + list(fp)}")
            if re.search(r"[—–]| -- ", a + " " + fq.get("q", "")):
                bad_answers.append(f"FAQ {i + 1}: Gedankenstrich")
        gates["faq_antworten_ok"] = not bad_answers
        rep["faqs"] = len(faqs)
        rep["faq_problems"] = bad_answers
        rep["gates"] = gates
        reports.append(rep)
    return reports


def lint_file(path, niche, band, words, phrases, facts=None):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith(".astro"):
        prose = astro_to_text(raw)
    elif path.endswith(".html"):
        prose = html_to_text(raw)
    elif path.endswith(".json"):
        raise SystemExit("Für city-copy.json geben Sie --niche an und keine Wortspanne; die Stadtspanne steht fest.")
    else:
        prose = md_to_text(raw)
    gates, rep = check_prose(prose, words, phrases, niche=niche, band=band, label=os.path.basename(path))
    if facts is not None:
        missing = numbers_not_in_facts(prose, facts)
        gates["zahlen_im_faktenblatt"] = not missing
        rep["zahlen_ohne_beleg"] = missing
    return [rep]


def print_report(reports):
    for r in reports:
        failed = [g for g, ok in r["gates"].items() if not ok]
        status = "BESTANDEN" if not failed else "DURCHGEFALLEN"
        line = (f"{status}  {r['label']}: {r['words']} Wörter, Lesbarkeit {r['lesbarkeit']} "
                f"(höher ist leichter), {r['schwere_woerter_prozent']} % Wörter mit drei Silben oder mehr")
        if "faqs" in r:
            line += f", {r['faqs']} FAQs"
        if r.get("band") and r["band"] != CITY_WORDS:
            line += (f" (kleine Stadt, Untergrenze {r['band'][0]}"
                     + (f", {r['faq_band'][0]} bis {r['faq_band'][1]} FAQs)" if r.get("faq_band") == TOWN_FAQ_COUNT else ")"))
        print(line)
        if r["forbidden_words"]:
            print(f"       verbotene Wörter: {r['forbidden_words']}")
        if r["forbidden_phrases"]:
            print(f"       verbotene Wendungen: {r['forbidden_phrases']}")
        if r["em_dashes"]:
            print(f"       Gedankenstriche: {r['em_dashes']}")
        if r.get("zahlen_ohne_beleg"):
            print(f"       Zahlen ohne Beleg im Faktenblatt ({len(r['zahlen_ohne_beleg'])}): "
                  f"{', '.join(r['zahlen_ohne_beleg'])}")
        for p in r.get("faq_problems", []):
            print(f"       {p}")
        if failed:
            print(f"       durchgefallene Prüfungen: {', '.join(failed)}")


def main():
    ap = argparse.ArgumentParser(description="Textgate für Gate 5 des Verzeichnis-Baukastens (deutsch).")
    ap.add_argument("file", help="city-copy.json, eine .astro-Seite oder eine Markdown-Datei")
    ap.add_argument("--niche", help='die Branchenbezeichnung, die früh im Text stehen muss, z. B. "Schlüsseldienste"')
    ap.add_argument("--min-words", type=int)
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--cities", help="Pfad zu 05-cities.json. Daraus baut der Lauf die Größenkarte "
                                     "regionSlug/slug -> count bei JEDEM Aufruf frisch (keine zu pflegende, "
                                     "veraltende Datei). Der vorgesehene Weg für city-copy.json (wiki/seo/copy-gate.md): "
                                     "fehlt ein Stadtschlüssel darin, BRICHT der Lauf ab, statt still auf die generische "
                                     "Wortspanne zurückzufallen.")
    ap.add_argument("--city-sizes", help="Vorgefertigte JSON-Datei, die den Stadtschlüssel (bundesland/stadt) auf die "
                                        "Zahl der Einträge abbildet; Städte unter 10 Einträgen bekommen eine niedrigere "
                                        "Untergrenze (380 bei 5 bis 9, 250 bei 3 oder 4, 120 und 2 bis 6 FAQs bei 1 oder 2). "
                                        "Für city-copy.json ist --cities vorzuziehen (frisch statt gepflegt).")
    ap.add_argument("--erlaube-rechtswoerter", "--allow-legal-words", action="store_true",
                    dest="erlaube_rechtswoerter",
                    help="den Block der Rechtswörter ([RECHTSWOERTER], [RECHTSWENDUNGEN]) für diese eine Seite "
                         "zulassen: „lizenziert“, „zugelassen“, „Kammer“, „amtlich“, „Testsieger“, „garantiert“ und die "
                         "übrigen. Nur für /festpreis-garantie/, /premium/, /agb/ und Ratgeberseiten, die über die "
                         "Rechtslage aufklären und diese Wörter bestreiten müssen (wiki/seo/copy-gate.md). NIE für "
                         "Stadttexte, Eintragsbeschreibungen oder die Startseite. Der Programmname „Festpreis-Garantie“ "
                         "ist überall erlaubt. Die Werbefloskeln bleiben verboten")
    ap.add_argument("--facts", help="Pfad zu 05-fact-sheet.md. Dann muss jede Zahl der Seite (Euro, "
                                    "Prozent, Jahre, Gerichts-/Aktenzeichen) in der Faktensammlung belegt "
                                    "sein, sonst scheitert die Prüfung. Für Ratgeberseiten, die aus der "
                                    "Faktensammlung entstehen (wiki/seo/copy-gate.md)")
    ap.add_argument("--json", action="store_true", help="maschinenlesbare Ausgabe")
    args = ap.parse_args()

    facts_text = None
    if args.facts:
        if not os.path.exists(args.facts):
            print(f"FEHLER: Faktensammlung nicht gefunden: {args.facts}")
            sys.exit(1)
        with open(args.facts, encoding="utf-8") as f:
            facts_text = f.read()

    if not os.path.exists(args.file):
        print(f"FEHLER: Datei nicht gefunden: {args.file}")
        sys.exit(1)

    words, phrases = load_bans(args.erlaube_rechtswoerter)
    if args.file.endswith(".json"):
        if not args.niche:
            print("FEHLER: --niche wird für city-copy.json gebraucht")
            sys.exit(1)
        sizes = build_city_sizes(args.cities, args.city_sizes)
        if sizes is None:
            print("FEHLER: city-copy.json braucht die Größen je Stadt. --cities <05-cities.json> angeben "
                  "(frische Karte regionSlug/slug -> count). Ohne Größen fiele die Prüfung auf die "
                  "generische Wortspanne zurück und verschluckte echte Befunde (wiki/seo/copy-gate.md).")
            sys.exit(1)
        # Volle Abdeckung erzwingen: jeder Stadtschlüssel aus city-copy.json muss in der Karte
        # stehen. Ein fehlender Schlüssel würde sonst still auf die generische Wortspanne
        # zurückfallen — genau der Fehler, den die Karte verhindern soll.
        cc = json.load(open(args.file, encoding="utf-8"))
        fehlen = sorted(s for s in cc if not s.startswith("_") and s not in sizes)
        if fehlen:
            quelle = args.cities or args.city_sizes
            print(f"ABBRUCH: {len(fehlen)} Stadt(e) aus city-copy.json fehlen in der Größenkarte "
                  f"(aus {quelle}). Kein stiller Rückfall auf die generische Wortspanne. Betroffen:")
            for s in fehlen:
                print(f"  {s}")
            sys.exit(1)
        reports = lint_city_copy(args.file, args.niche, words, phrases, sizes)
    else:
        band = None
        if args.min_words is not None or args.max_words is not None:
            band = (args.min_words or 0, args.max_words or 10**9)
        reports = lint_file(args.file, args.niche, band, words, phrases, facts=facts_text)

    for r in reports:
        r["rechtswoerter_zugelassen"] = bool(args.erlaube_rechtswoerter)
    if args.json:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    else:
        if args.erlaube_rechtswoerter:
            print("HINWEIS: Rechtswörter für diese Seite zugelassen (--erlaube-rechtswoerter). Zulässig nur für "
                  "/festpreis-garantie/, /premium/, /agb/ und Ratgeberseiten zur Rechtslage (wiki/seo/copy-gate.md).")
        print_report(reports)
    ok = all(all(r["gates"].values()) for r in reports)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
