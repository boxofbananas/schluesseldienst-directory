#!/usr/bin/env python3
"""Geschlecht einer Person für die Versand-Anrede bestimmen — nie raten.

Reihenfolge (so auch in CLAUDE.md beschrieben):
  1. Impressum-Text (aus dem Zwischenspeicher, kein neuer Abruf): „Herr"/„Frau" oder die Form der
     Funktion (Inhaber/Inhaberin, Geschäftsführer/Geschäftsführerin …) auf einer Zeile, die den
     Nachnamen der gefundenen Person trägt.
  2. Vorname gegen feste Listen eindeutig männlicher/weiblicher Vornamen (deutsch und in Deutschland
     häufige türkische, polnische, russische, italienische, arabische Namen).
  3. Unsicher → leer → Anrede „Guten Tag,".

Mehrdeutige Vornamen (Kim, Sascha, Toni, Nicola, Andrea, Luca, Deniz, Robin, Simone, Gabriele …),
unbekannte und abgekürzte Vornamen gelten als unsicher. Lieber neutral als falsch.

Keine Titel in der Anrede (Dr., Dipl.-Ing. — die stecken ohnehin nicht im Vor-/Nachnamen).
Nachnamen mit Zusatz (von, van, de) werden vollständig übernommen (sie stehen so im Nachnamen).
"""
import re
import unicodedata


def _fold(s):
    """klein, Umlaute ausgeschrieben, Akzente entfernt — für robusten Vergleich."""
    s = (s or "").lower().strip()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


# --------------------------------------------------------------------------- Vornamen-Listen
# Nur EINDEUTIGE Vornamen. Bei Zweifel gehört ein Name NICHT hierher, sondern bleibt unbekannt
# (→ unsicher → „Guten Tag,"); der Probelauf listet die unbekannten, damit sie nachgetragen werden.
MAENNLICH = {
    # deutsch
    "alexander", "andreas", "anton", "armin", "arne", "arnold", "axel", "benedikt", "benjamin",
    "bernd", "bernhard", "bjarne", "björn", "carsten", "christian", "christoph", "clemens", "claus",
    "daniel", "david", "dennis", "detlef", "dieter", "dirk", "dominik", "eberhard", "edgar", "edwin",
    "elias", "elmar", "emil", "erich", "erik", "ernst", "ewald", "fabian", "felix", "finn", "florian",
    "frank", "franz", "friedrich", "fritz", "fynn", "georg", "gerd", "gerhard", "gregor", "günter",
    "günther", "gustav", "hannes", "hans", "harald", "hartmut", "heiko", "heinrich", "heinz", "helmut",
    "henning", "henri", "herbert", "hermann", "holger", "horst", "hubert", "ingo", "jakob", "jacob",
    "jan", "jannik", "jannis", "jens", "joachim", "johann", "johannes", "jonas", "jonathan", "jörg",
    "josef", "julian", "jürgen", "kai", "karl", "karsten", "kevin", "klaus", "konrad", "kurt", "lars",
    "lennart", "leon", "lothar", "louis", "ludwig", "luis", "lukas", "maik", "manfred", "marcel",
    "marco", "markus", "martin", "mathias", "matthias", "marvin", "mats", "maximilian", "michael",
    "mirko", "moritz", "niklas", "nils", "noah", "norbert", "olaf", "oliver", "oskar", "otto", "pascal",
    "patrick", "paul", "peter", "philipp", "rainer", "ralf", "ralph", "reinhard", "reinhold", "rené",
    "richard", "robert", "roland", "rolf", "rudolf", "rüdiger", "sebastian", "siegfried", "simon",
    "sönke", "stefan", "stephan", "sven", "theo", "thomas", "thorsten", "till", "tim", "timo", "tobias",
    "torsten", "udo", "ulf", "ulrich", "uwe", "valentin", "vincent", "volker", "walter", "werner",
    "wilhelm", "wolfgang", "wolfram",
    # türkisch
    "ahmet", "ali", "arda", "aykut", "baran", "baris", "bekir", "berk", "burak", "bülent", "cem",
    "cihan", "emre", "enes", "engin", "ercan", "erdem", "erkan", "ersin", "fatih", "ferhat", "furkan",
    "gökhan", "hakan", "halil", "hasan", "hüseyin", "ibrahim", "ilyas", "ismail", "kaan", "kadir",
    "kemal", "kerem", "levent", "mahmut", "mehmet", "mert", "murat", "mustafa", "nihat", "okan", "onur",
    "orhan", "osman", "ömer", "recep", "sedat", "selim", "serdar", "serkan", "sinan", "soner", "tarik",
    "tolga", "tuncay", "ugur", "volkan", "yasin", "yusuf", "yilmaz", "zafer",
    # polnisch
    "andrzej", "dariusz", "grzegorz", "jacek", "jakub", "jaroslaw", "jerzy", "kamil", "krzysztof",
    "lukasz", "maciej", "marcin", "mariusz", "mateusz", "michal", "pawel", "piotr", "przemyslaw",
    "rafal", "ryszard", "slawomir", "stanislaw", "szymon", "tadeusz", "tomasz", "wojciech", "zbigniew",
    # russisch
    "aleksandr", "alexej", "andrej", "boris", "dmitrij", "jewgenij", "igor", "ivan", "konstantin",
    "leonid", "maksim", "michail", "nikolai", "oleg", "pavel", "roman", "sergej", "stanislav", "vadim",
    "viktor", "vitali", "vladimir", "vladislav", "jurij",
    # italienisch
    "alessandro", "antonio", "carlo", "claudio", "domenico", "enzo", "fabio", "francesco", "franco",
    "gennaro", "giacomo", "gianni", "giorgio", "giovanni", "giuseppe", "lorenzo", "luigi", "mario",
    "massimo", "matteo", "paolo", "pietro", "roberto", "salvatore", "sergio", "stefano", "vincenzo",
    "vito",
    # arabisch
    "abdullah", "ahmad", "ahmed", "amir", "bilal", "fadi", "hamza", "jamal", "karim", "khaled",
    "khalid", "mahmoud", "mohamed", "mohammed", "muhammad", "nabil", "omar", "osama", "rami", "samir",
    "tarek", "tariq", "walid", "yahya", "yasser", "youssef", "ziad", "jean",
}

WEIBLICH = {
    # deutsch
    "angelika", "anja", "anke", "anna", "annett", "annette", "antje", "astrid", "barbara", "beate",
    "bettina", "birgit", "brigitte", "carina", "carmen", "carola", "caroline", "charlotte", "christa",
    "christel", "christiane", "christina", "christine", "claudia", "cornelia", "dagmar", "daniela",
    "diana", "doreen", "doris", "dorothea", "edith", "elena", "elfriede", "elisabeth", "elke", "ella",
    "emilia", "emma", "erika", "eva", "franziska", "frauke", "frieda", "gerda", "gertrud", "gisela",
    "gudrun", "hanna", "hannah", "hannelore", "hedwig", "heide", "heidi", "heike", "helene", "helga",
    "henriette", "hilde", "hildegard", "ilona", "ilse", "inge", "ingeborg", "ingrid", "irene", "iris",
    "irmgard", "jana", "janina", "jasmin", "jennifer", "jessica", "johanna", "josefine", "judith",
    "julia", "juliane", "jutta", "karin", "karina", "karla", "katharina", "kathrin", "katja", "katrin",
    "kerstin", "klara", "kristin", "laura", "lea", "lena", "leonie", "lieselotte", "linda", "lisa",
    "lotte", "luise", "magdalena", "maike", "manuela", "margarete", "margit", "maria", "marianne",
    "marie", "marion", "marlene", "marta", "martha", "martina", "mathilde", "melanie", "meike",
    "michaela", "monika", "nadine", "nadja", "natalie", "nicole", "nina", "petra", "pia", "regina",
    "renate", "rita", "romy", "rosa", "rosemarie", "ruth", "sabine", "sabrina", "sandra", "sara",
    "sarah", "saskia", "selina", "sibylle", "sigrid", "silke", "silvia", "sonja", "sophia", "sophie",
    "stefanie", "stephanie", "susanne", "svenja", "tanja", "theresa", "therese", "ulrike", "ursula",
    "ute", "vanessa", "vera", "veronika", "victoria", "waltraud", "wiebke", "yvonne",
    # türkisch
    "arzu", "aylin", "ayse", "buket", "burcu", "busra", "cansu", "ceren", "dilek", "ebru", "elif",
    "emine", "esra", "fadime", "fatma", "filiz", "gamze", "gül", "gülay", "hatice", "havva", "hülya",
    "kübra", "leyla", "melek", "meltem", "merve", "nurcan", "özlem", "pinar", "sema", "sevda", "sevim",
    "sibel", "yasemin", "zehra", "zeynep",
    # polnisch
    "agata", "agnieszka", "aleksandra", "beata", "dorota", "edyta", "elzbieta", "ewa", "grazyna",
    "halina", "iwona", "joanna", "justyna", "katarzyna", "krystyna", "malgorzata", "renata", "sylwia",
    "urszula", "wanda", "zofia",
    # russisch
    "anastasia", "ekaterina", "galina", "irina", "ksenia", "larisa", "ludmila", "marina", "nadezhda",
    "natalia", "natalja", "oksana", "olga", "svetlana", "tatjana", "valentina", "julija",
    # italienisch
    "alessia", "angela", "antonella", "carla", "chiara", "elisa", "francesca", "giulia", "giuseppina",
    "lucia", "paola", "serena", "valeria",
    # arabisch
    "amal", "amina", "aya", "fatima", "hana", "huda", "khadija", "lina", "mariam", "maryam", "nour",
    "nur", "rania", "salma", "samira", "yara", "zainab", "zeinab",
}

# Ausdrücklich mehrdeutig — nie ableiten, auch wenn ein Name sonst „deutsch klingt".
AMBIG = {
    "kim", "sascha", "toni", "nicola", "andrea", "luca", "luka", "deniz", "robin", "mika", "simone",
    "gabriele", "alex", "chris", "charlie", "dominique", "eike", "maxi", "sam", "jo", "noa", "michele",
    "daniele", "emanuele", "nikola", "sandy", "kay", "ümit", "derya", "yael", "nuri",
}

_M = {_fold(n) for n in MAENNLICH}
_F = {_fold(n) for n in WEIBLICH}
_A = {_fold(n) for n in AMBIG}


def ist_abgekuerzt(vorname):
    """Einzelbuchstabe oder abgekürzter Vorname (Th., J., J.-P.) — gilt als unsicher."""
    v = (vorname or "").strip()
    if not v:
        return True
    if v.endswith("."):
        return True
    teile = [t for t in re.split(r"[\s\-]+", v) if t]
    return all(len(t.strip(".'’")) <= 1 for t in teile)


def _teile(vorname):
    return [t for t in re.split(r"[\s\-]+", (vorname or "").strip()) if t.strip(".'’")]


def geschlecht_aus_vorname(vorname):
    """„herr" / „frau" aus dem Vornamen, sonst „" (unsicher). Mehrteilige (Hans-Peter, Anna-Maria):
    nur eindeutig, wenn kein Teil mehrdeutig ist und alle erkannten Teile dasselbe Geschlecht tragen."""
    if ist_abgekuerzt(vorname):
        return ""
    folds = [_fold(t) for t in _teile(vorname)]
    if any(f in _A for f in folds):
        return ""
    gefunden = set()
    for f in folds:
        if f in _M:
            gefunden.add("herr")
        if f in _F:
            gefunden.add("frau")
    if gefunden == {"herr"}:
        return "herr"
    if gefunden == {"frau"}:
        return "frau"
    return ""


_FRAU_ROLLE = re.compile(r"(?i)\b(inhaberin|gesch[aä]ftsf[uü]hrerin|eigent[uü]merin|betreiberin|"
                         r"einzelunternehmerin|gesellschafterin|vertretungsberechtigte)\b")
_HERR_ROLLE = re.compile(r"(?i)\b(inhaber|gesch[aä]ftsf[uü]hrer|eigent[uü]mer|betreiber|"
                         r"einzelunternehmer|gesellschafter)\b")
_FRAU_ANREDE = re.compile(r"(?i)\bfrau\b")
_HERR_ANREDE = re.compile(r"(?i)\bherrn?\b")


def geschlecht_aus_impressum(text, vorname, nachname):
    """„herr"/„frau" aus dem Impressum-Text, nur von einer Zeile, die den Nachnamen der Person trägt
    (so gehört das Signal eindeutig zu ihr). Weibliche Signale (Frau, …-in-Form) haben Vorrang."""
    if not text or not nachname:
        return ""
    letzter = nachname.split()[-1] if nachname.split() else nachname
    if len(letzter.strip(".'’")) < 2:
        return ""
    nn = re.compile(r"(?i)\b" + re.escape(letzter) + r"\b")
    for zeile in text.splitlines():
        if not nn.search(zeile):
            continue
        if _FRAU_ANREDE.search(zeile) or _FRAU_ROLLE.search(zeile):
            return "frau"
        if _HERR_ANREDE.search(zeile) or _HERR_ROLLE.search(zeile):
            return "herr"
    return ""


def bestimme_geschlecht(vorname, nachname, impressum_text=""):
    """Gibt (geschlecht, quelle, unsicherer_vorname).
    geschlecht: „herr"/„frau"/„"; quelle: „impressum"/„vorname"/„"; unsicherer_vorname: True, wenn ein
    echter (nicht abgekürzter) Vorname da ist, aber weder Impressum noch Liste ihn auflösen."""
    if not (nachname or "").strip():
        return ("", "", False)
    g = geschlecht_aus_impressum(impressum_text, vorname, nachname)
    if g:
        return (g, "impressum", False)
    g = geschlecht_aus_vorname(vorname)
    if g:
        return (g, "vorname", False)
    unsicher = bool((vorname or "").strip()) and not ist_abgekuerzt(vorname)
    return ("", "", unsicher)


PLATZHALTER_NACHNAMEN = {"mustermann", "musterfrau", "doe", "beispiel", "example"}


def ist_platzhalter(vorname, nachname):
    return (nachname or "").strip().lower() in PLATZHALTER_NACHNAMEN


def baue_anrede(vorname, nachname, geschlecht):
    """„Guten Tag Herr <Nachname>," / „Guten Tag Frau <Nachname>,". Ohne sicheren Namen ODER ohne
    sicheres Geschlecht: „Guten Tag,". Nachname voll (inkl. von/van/de), ohne Titel."""
    nn = (nachname or "").strip()
    if not nn or ist_platzhalter(vorname, nachname):
        return "Guten Tag,"
    if geschlecht == "herr":
        return f"Guten Tag Herr {nn},"
    if geschlecht == "frau":
        return f"Guten Tag Frau {nn},"
    return "Guten Tag,"
