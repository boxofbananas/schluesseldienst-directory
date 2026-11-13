# Mannheim fest auf die Startseite, gefolgter Link folgt der Garantie

**Datum:** 2026-11-13 · **Branch:** `main` (live) · **Deploy:** `ff729a59` · **Projekt:** `schluesseldienste-deutschland`

Zwei Änderungen, Build und Template, ausgeliefert, `check_live.py` mit 2821 grün.

## 1. Mannheim fest in die Startseiten-Auswahl

`DirectoryHub` zeigte `cities.slice(0, 20)` nach Eintragszahl. Mannheim lag mit 17 Einträgen
tatsächlich auf **Rang 21** (knapp draußen): Bonn hält mit denselben 17 den Rang 20, weil „Bonn"
alphabetisch vor „Mannheim" steht.

Neu: eine Liste `pinnedCities` in `site.json` (Stadtschlüssel `regionSlug/slug`). Ihre Städte
stehen immer in der Auswahl; die Gesamtzahl bleibt 20, die übrigen nach Eintragszahl. Eingetragen:
`["baden-wuerttemberg/mannheim"]`.

**Antwort auf die Frage:** Mannheim steht danach an **Stelle 20** (letzte Karte, 17 Einträge).
Dafür weicht **Bonn** (war Stelle 20, 17 Einträge). Live geprüft: die letzten drei Karten sind
Karlsruhe, Mönchengladbach, Mannheim; Bonn ist nicht mehr dabei.

Die übrigen 19 bleiben in Eintragszahl-Reihenfolge (Berlin 226 … Mönchengladbach 19).

## 2. Der gefolgte Link folgt der Festpreis-Garantie, nicht der Bezahlung

Vorher: `followed = l.optimized` (bezahlter Platz). Neu auf der Eintragsseite und in `SocialLinks`
(`linkRel`), `owned` wird nicht gelesen:

- `geprueft = true` → Website- und Profil-Links `rel="noopener"` (ohne nofollow).
- bezahlter Platz ohne Garantie (`l.optimized`) → `rel="sponsored noopener"`.
- alle übrigen → `rel="nofollow noopener"` wie bisher.

### Linkzahl im Build, vorher und nachher (Website-Links der Eintragsseiten, 2 Layout-Kopien je Seite)

| rel | vorher | nachher |
|---|---|---|
| `nofollow noopener` | 5846 | 5812 |
| `noopener` (ohne nofollow) | 2 | **36** |
| `sponsored noopener` | 0 | **0** |

**36 ohne nofollow = 18 Einträge × 2 Kopien, alle 18 mit Festpreis-Garantie** (erwartungsgemäß).
Gegenprobe: die 18 Seiten sind genau die geprüften Betriebe. **0 `sponsored`**, weil der einzige
bezahlte Platz (Merz) zugleich geprüft ist und die Garantie vorgeht. Summe der Website-Links
unverändert (5848); 34 Links sind von `nofollow` auf `noopener` gewechselt (17 geprüfte Betriebe
zusätzlich zu Merz, × 2).

Profil-Links (`SocialLinks`): im Build rendern **0** (die Spalte `socials` ist überall leer); die
Regel greift dort, sobald Profile vorhanden sind.

**Live geprüft:** Merz (geprüft) → `rel="noopener"`; ein nicht geprüfter Eintrag (Aalen) →
`rel="nofollow noopener"`.

### Textgate (gebaute Seiten, `--erlaube-rechtswoerter`)

- **/premium/ BESTANDEN** (396 Wörter). Mein erster Zusatz überschoss die 400-Wort-Grenze (409);
  auf 396 gekürzt, Sinn erhalten.
- **/festpreis-garantie/ Inhalt BESTANDEN** (keine verbotenen Wörter, keine Gedankenstriche,
  Branchenwort früh). Einzige überschrittene Prüfung ist die **weiche Obergrenze `--max-words
  1200`** (die Seite hat 1512 Wörter). Das ist **vorbestehend**: schon vor diesem Task lag die
  Seite bei ~1488 Wörtern, mein ergänzter Satz bringt **+24**. Ich habe die ausführliche
  Garantie-/Rechtsseite nicht gekürzt (das wäre eine Umschreibung außerhalb dieses Auftrags). Die
  1200 in [[copy-gate]] ist für diese Seite seit Längerem zu niedrig — **Empfehlung:** den
  Richtwert dieser einen Seite anheben.

### Texte geändert

- **/premium/** Premium-Eintrag: „alle Links ohne nofollow" gestrichen; neu: Bilder, Karte,
  Öffnungszeiten; Links als bezahlter Platz mit `rel="sponsored"` statt nofollow; ohne nofollow nur
  mit der Festpreis-Garantie. Stadt-Premium: „ein Link ohne nofollow" → „ein als bezahlt
  gekennzeichneter Link (`rel="sponsored"`) statt nofollow".
- **/festpreis-garantie/** (Absatz „Für Betriebe"): Satz ergänzt — der Link vom Eintrag auf die
  Website trägt kein nofollow; bezahlte Plätze bekommen das nicht, ihre Links werden als bezahlt
  gekennzeichnet.

## Weitere Fundstellen zur alten Regel „bezahlte Stufe → gefolgter Link"

**Geändert (die vom Betreiber genannten Verkaufsdokumente):**
- `templates/featured-tiers.md` (Premium-Eintrag „alle Links gefolgt", Stadt-Premium „gefolgter
  Link") → auf `rel="sponsored"` umgestellt; der gefolgte Link gehört zur Garantie.
- `wiki/framework/monetization-slots.md` (Z. 16 „alle Links gefolgt"; Zustand „Ausgebaut … alle
  Links gefolgt"; Stufe Stadt-Premium „gefolgter Link"; Zustand „Einfach … Website-Link mit
  nofollow") → auf `sponsored`/„ohne nofollow nur mit Garantie" umgestellt.

**Nur gemeldet, nicht geändert — AGB (wie gewünscht):**
- `pages/agb.astro` enthält **kein** „gefolgter Link"-Versprechen. A3 („Bezahlte Platzierungen
  sind gekennzeichnet") deckt sich sogar mit der neuen `sponsored`-Regel; B117 verspricht „keine
  bestimmte Platzierung in Suchmaschinen". Unverändert.
- `pages/festpreis-garantie/antrag/index.astro:68` und das FAQ in `site.json`: kein
  Follow-Versprechen (Antrag:68 ist ein Formularfeld „Link zu Ihrem Google-Unternehmensprofil").

**Gefunden, nicht geändert — die Regel beschreibende Wiki-Seiten (ihre Quelle ist [[konventionen]],
die nur Daniel ändert; Vorschlag, sie zusammen mit konventionen anzugleichen):**
- `wiki/seo/on-page-rules.md:58` „… außer bei bezahlter Stufe"
- `wiki/framework/site-architecture.md:102` „bezahlte Stufen bekommen einen gefolgten Link"
- `wiki/framework/page-types.md:16` „ausgebaut … alle Links gefolgt"
- `wiki/framework/siegel-programm.md:75` „Premium/Top … gefolgte Links"
- `wiki/framework/authority-and-links.md:59` „… wenn sie einen gefolgten Link wollen"
- `wiki/framework/footprint-rules.md:17` „dieselbe nofollow-Regel auf dem Link zur Website"
- `templates/astro/README.md:70` „Grundeintrag (Website-Link mit nofollow) und [ausgebaut]"

## Vorschlag für [[konventionen]] (nicht eingetragen — Daniel ändert die Datei frei)

> **Gefolgte Links folgen der Festpreis-Garantie, nicht der Bezahlung.** Der Link auf die Website
> eines Betriebs und seine Profil-Links tragen `rel="nofollow"`, außer der Betrieb hat die
> Festpreis-Garantie (`geprueft=true`); dann stehen sie ohne nofollow. Ein bezahlter Platz ohne
> Garantie macht den Link nicht gefolgt, sondern kennzeichnet ihn als bezahlt (`rel="sponsored"`).
> `owned` wird dabei nicht gelesen. Der gefolgte Link gehört damit, wie der Garantie-Nachweis, zur
> Garantie und ist nicht käuflich.

## Bauen, Ausliefern, Prüfen

- `npm run build` ohne Datenwarnung (die „warn"-Zeile im Log ist der Betriebsname „warns-…").
- Build und Template geändert.
- `wrangler pages deploy` → Deploy `ff729a59`.
- Sitemap 2821 Adressen (unverändert; Pin und `rel` ändern keine Seite im Sitemap).
- `check_live.py … --expect-urls 2821` → **alle Prüfungen bestanden**.
