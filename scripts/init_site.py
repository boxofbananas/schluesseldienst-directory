#!/usr/bin/env python3
"""Legt output/<slug>/site/ aus templates/astro/ an — mit Sperre gegen Ueberschreiben.

Gate 5 kopiert templates/astro/ nach output/<slug>/site/ und fuellt dann die Daten. Nach dem
ersten Anlegen ist der Build die Wahrheit, nicht das Template: alle weitere Arbeit passiert im
Build (wiki/framework/template-build-drift.md). Ein erneuter Kopierlauf wuerde diese Arbeit
verwerfen.

Deshalb: Existiert output/<slug>/site/ schon, bricht dieses Skript ab und nennt, was verloren
ginge. Nur mit --force wird fortgesetzt — und auch dann wird der bestehende Ordner zuerst nach
site.backup-<Zeitstempel> beiseitegelegt, nie geloescht.

Aufrufe:
  python3 scripts/init_site.py --slug schluesseldienste-deutschland
  python3 scripts/init_site.py --slug <slug> --force   # nur nach Pruefung des Befunds
"""
import argparse
import filecmp
import os
import shutil
import sys
import time

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
IGNORE = shutil.ignore_patterns("node_modules", ".wrangler", "dist", ".astro")


def divergence(template_src, build_src):
    """Dateien, die sich zwischen den beiden src-Baeumen unterscheiden (ohne data/).

    Rueckgabe: (verschieden, nur_im_build, nur_im_template) als relative Pfade."""
    diff, only_build, only_template = [], [], []

    def walk(rel=""):
        tp_dir = os.path.join(template_src, rel)
        bp_dir = os.path.join(build_src, rel)
        names = set()
        if os.path.isdir(tp_dir):
            names |= set(os.listdir(tp_dir))
        if os.path.isdir(bp_dir):
            names |= set(os.listdir(bp_dir))
        for n in sorted(names):
            r = os.path.join(rel, n)
            if r == "data" or r.startswith("data" + os.sep):
                continue  # data/ soll sich unterscheiden
            tp, bp = os.path.join(template_src, r), os.path.join(build_src, r)
            if os.path.isdir(tp) or os.path.isdir(bp):
                walk(r)
                continue
            te, be = os.path.exists(tp), os.path.exists(bp)
            if te and be:
                if not filecmp.cmp(tp, bp, shallow=False):
                    diff.append(r)
            elif be:
                only_build.append(r)
            elif te:
                only_template.append(r)

    if os.path.isdir(template_src) and os.path.isdir(build_src):
        walk()
    return diff, only_build, only_template


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True,
                    help="der Build-Ordner unter output/, z. B. schluesseldienste-deutschland")
    ap.add_argument("--force", action="store_true",
                    help="einen bestehenden Build ueberschreiben; legt ihn vorher nach "
                         "site.backup-<Zeitstempel> beiseite, nie geloescht")
    a = ap.parse_args()

    template = os.path.join(ROOT, "templates", "astro")
    target = os.path.join(ROOT, "output", a.slug, "site")
    if not os.path.isdir(template):
        sys.exit(f"Template fehlt: {template}")

    # Erstanlage: einfach kopieren.
    if not os.path.exists(target):
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copytree(template, target, ignore=IGNORE)
        print(f"angelegt: output/{a.slug}/site/ aus templates/astro/")
        print("Ab jetzt ist der Build die Wahrheit. Alle Aenderungen hier, nicht im Template "
              "(wiki/framework/template-build-drift.md).")
        return

    # Ziel existiert: Sperre.
    diff, only_b, only_t = divergence(
        os.path.join(template, "src"), os.path.join(target, "src"))
    lost = len(diff) + len(only_b)
    lines = [
        f"ABBRUCH: output/{a.slug}/site/ existiert bereits.",
        "",
        "Nach dem ersten Anlegen ist der Build die Wahrheit, nicht das Template; ein erneuter",
        "Kopierlauf wuerde die seitdem im Build geleistete Arbeit verwerfen.",
        "",
        f"Was verloren ginge (src/, ohne data/): {lost} Datei(en) — {len(diff)} inhaltlich",
        f"verschieden, {len(only_b)} nur im Build. Dazu alles ausserhalb von src/ (functions/ "
        "u. a.).",
    ]
    if only_t:
        lines.append(
            f"Hinweis: {len(only_t)} Datei(en) nur im Template — die saehe der Build neu; "
            "pruefe sie einzeln (moegliche 'Template voraus'-Faelle).")
    lines += [
        "",
        "Nichts wurde geaendert. Wenn du wirklich neu anlegen willst: zuerst den Befund pruefen",
        "(wiki/framework/template-build-drift.md), dann mit --force wiederholen. Der bestehende",
        "Ordner wird dabei nach site.backup-<Zeitstempel> beiseitegelegt, nicht geloescht.",
    ]
    if not a.force:
        sys.exit("\n".join(lines))

    # --force: ausdrueckliche Bestaetigung. Bestehendes beiseitelegen, dann frisch anlegen.
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(ROOT, "output", a.slug, f"site.backup-{stamp}")
    shutil.move(target, backup)
    shutil.copytree(template, target, ignore=IGNORE)
    print(f"Bestehender Build beiseitegelegt nach {os.path.relpath(backup, ROOT)}")
    print(f"neu angelegt: output/{a.slug}/site/ aus templates/astro/")
    print(f"Gegenueber dem Backup verworfen: {lost} src-Datei(en). Bei Bedarf aus dem Backup "
          "zurueckholen (siehe wiki/framework/template-build-drift.md).")


if __name__ == "__main__":
    main()
