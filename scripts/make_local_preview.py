#!/usr/bin/env python3
"""Eine Kopie der gebauten Site, die sich mit einem Doppelklick auf index.html öffnet.

Die gebaute Site in dist/ benutzt Pfade, die an der Wurzel der Domain beginnen
(/_astro/x.css, /verzeichnis/baden-wuerttemberg/mannheim/). Für die veröffentlichte Site und für
einen lokalen Server ist das richtig, für eine Datei, die direkt von der Festplatte geöffnet
wird, falsch: das Stylesheet wird nicht gefunden, und jeder Link führt ins Leere. Dieses Skript
schreibt eine zweite Kopie mit relativen Pfaden und dem Stylesheet in der Seite selbst. Die Kopie
ist zum Ansehen, nie zum Ausliefern.

Aufruf:
  python3 scripts/make_local_preview.py output/<slug>/site/dist output/<slug>/vorschau

Der bequemere Weg ist preview-site.command (Mac) oder preview-site.bat (Windows) in site/: die
starten einen kleinen Server, und dann stimmen die Pfade ohnehin. Dieses Skript ist für den Fall,
dass eine Datei weitergegeben werden soll, die ohne Server etwas zeigt.
"""
import argparse, os, re, shutil, sys

ATTR = re.compile(r'\b(href|src|action)="(/[^"/][^"]*|/)"')
CSS_URL = re.compile(r"url\((['\"]?)/(?!/)")
SHEET = re.compile(r'<link rel="stylesheet" href="(/[^"]+\.css)"\s*/?>')


def main():
    ap = argparse.ArgumentParser(description="Eine Kopie der gebauten Site zum Ansehen ohne Server schreiben.",
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dist", help="der gebaute Ordner, output/<slug>/site/dist")
    ap.add_argument("vorschau", help="der Zielordner, z. B. output/<slug>/vorschau (wird neu angelegt)")
    a = ap.parse_args()
    src, out = a.dist.rstrip("/"), a.vorschau.rstrip("/")
    if not os.path.isfile(os.path.join(src, "index.html")):
        print(f"FEHLER: {src}/index.html gibt es nicht. Lassen Sie zuerst npm run build laufen."); sys.exit(1)
    if os.path.isdir(out): shutil.rmtree(out)
    shutil.copytree(src, out)
    pages = links = missing = 0
    for root, _, files in os.walk(out):
        depth = os.path.relpath(root, out)
        up = "" if depth == "." else "../" * (depth.count(os.sep) + 1)
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(".css"):
                t = open(p, encoding="utf-8").read()
                open(p, "w", encoding="utf-8").write(CSS_URL.sub(lambda m: f"url({m.group(1)}{up}", t))
                continue
            if not f.endswith(".html"): continue
            t = open(p, encoding="utf-8").read()

            # Das Stylesheet wandert in die Seite selbst, damit die Seite auch in einer Anzeige
            # gestaltet ist, die eine Datei zeigt und nichts nachlädt. Schriften bleiben Dateien
            # und fallen auf die Systemschriften der Gestaltungsmarken zurück, wenn sie sich
            # nicht laden lassen.
            def inline(m):
                css = open(os.path.join(src, m.group(1).lstrip("/")), encoding="utf-8").read()
                return "<style>" + CSS_URL.sub(lambda u: f"url({u.group(1)}{up}", css) + "</style>"
            t = SHEET.sub(inline, t)

            def fix(m):
                nonlocal links, missing
                attr, url = m.group(1), m.group(2)
                path, sep, tail = url.partition("?")
                frag = ""
                if "#" in path: path, _, frag = path.partition("#")
                target = path.lstrip("/")
                if path.endswith("/"): target += "index.html"
                if not os.path.exists(os.path.join(out, target)): missing += 1
                links += 1
                return f'{attr}="{up}{target}{"#" + frag if frag else ""}{sep}{tail}"'

            open(p, "w", encoding="utf-8").write(ATTR.sub(fix, t))
            pages += 1
    note = os.path.join(out, "BITTE-ZUERST-LESEN.txt")
    open(note, "w", encoding="utf-8").write(
        "Dieser Ordner ist eine Kopie der Site zum Ansehen auf dem eigenen Rechner.\n"
        "Öffnen Sie index.html. Laden Sie diesen Ordner nicht hoch. Ausgeliefert wird site/dist.\n")
    print(f"Seiten umgeschrieben: {pages}, Links umgeschrieben: {links}, Links ohne Ziel in der Kopie: {missing}")
    print(f"Zum Ansehen öffnen: {os.path.join(out, 'index.html')}")


if __name__ == "__main__":
    main()
