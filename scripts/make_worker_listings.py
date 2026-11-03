#!/usr/bin/env python3
"""Schreibt die kurze Eintragsdatei, gegen die der Mail-Worker Absender abgleicht.

Aufruf:
  python3 scripts/make_worker_listings.py output/<slug>/site/src/data/listings.csv \\
      output/<slug>/worker/src/listings.json

Je Eintrag ein kurzer Satz Felder: Slug, Name, Stadt, Ziffern der Telefonnummer, Host der
Website, Bewertung, Zahl der Bewertungen, Wert der Spalte `featured`. Die Feldnamen bleiben
englisch, weil `templates/worker/src/index.ts` sie so liest; geändert wird hier nichts daran.

`scripts/mail_worker.py setup` und `deploy` rufen dieses Skript selbst auf, mit denselben zwei
Pfaden. Von Hand wird es nur gebraucht, wenn der Worker steht und die CSV sich geändert hat.
"""
import argparse, csv, json, re, sys
from urllib.parse import urlparse

csv.field_size_limit(10**9)


def main():
    ap = argparse.ArgumentParser(description="Die Eintragsdatei des Mail-Workers aus der Eintrags-CSV schreiben.",
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="die Eintrags-CSV der Site, output/<slug>/site/src/data/listings.csv")
    ap.add_argument("json", help="die Zieldatei, output/<slug>/worker/src/listings.json")
    a = ap.parse_args()

    try:
        f = open(a.csv, encoding="utf-8-sig")
    except OSError as e:
        print(f"FEHLER: {a.csv} lässt sich nicht lesen: {e}")
        sys.exit(1)
    rows = []
    with f:
        reader = csv.DictReader(f)
        fehlend = [s for s in ("slug", "name", "city") if s not in (reader.fieldnames or [])]
        if fehlend:
            print(f"FEHLER: in {a.csv} fehlen die Spalten {', '.join(fehlend)}. "
                  "Erwartet wird die Eintrags-CSV der Site (Gate 5).")
            sys.exit(1)
        for r in reader:
            host = urlparse((r.get("website") or "").strip()).netloc.lower().removeprefix("www.")
            rows.append({"slug": r["slug"], "name": r["name"], "city": r["city"],
                         "phone": re.sub(r"\D", "", r.get("phone") or "")[-10:],
                         "host": host, "rating": r.get("rating") or "", "reviews": r.get("reviews") or "",
                         "featured": (r.get("featured") or "").strip() or ""})
    try:
        with open(a.json, "w", encoding="utf-8") as out:
            json.dump(rows, out, ensure_ascii=False, separators=(",", ":"))
    except OSError as e:
        print(f"FEHLER: {a.json} lässt sich nicht schreiben: {e} (gibt es den Ordner output/<slug>/worker/src/ schon?)")
        sys.exit(1)
    print(f"{len(rows)} Einträge nach {a.json} geschrieben")


if __name__ == "__main__":
    main()
