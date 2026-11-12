# Widerspruch zur Platzierung auf /festpreis-garantie/ aufgelöst

**Datum:** 2026-11-12 · **Branch:** `main` (live) · **Deploy:** `68d052dc` · **Projekt:** `schluesseldienste-deutschland`

## Der Widerspruch

Der Reihenfolge-Absatz auf /festpreis-garantie/ sagt, dass Betriebe mit Festpreis-Garantie **vor**
den Betrieben ohne stehen. Der Abschnitt über bezahlte Sichtbarkeit sagte dagegen: „… und wer eine
Garantie hat, bekommt dadurch **keinen besseren Platz**." Beides zusammen ist falsch.

## Berichtigt (so, dass beides stimmt)

Neue Aussage an beiden Stellen: Wer zahlt, bekommt keine Garantie; wer die Garantie hat, bekommt
dadurch **keinen der bezahlten Plätze**. Die Garantie **hebt einen Betrieb vor die Betriebe ohne
Garantie, aber nie über einen bezahlten Platz**, und ist nicht käuflich.

- **/festpreis-garantie/** (Abschnitt „Was die Garantie kostet"):
  > Wer dafür zahlt, bekommt keine Garantie; wer die Garantie hat, bekommt dadurch keinen der
  > bezahlten Plätze. Die Garantie hebt einen Betrieb vor die Betriebe ohne Garantie, aber nie über
  > einen bezahlten Platz, und sie ist nicht käuflich.
- **/premium/** (Abschnitt „Die Festpreis-Garantie ist nicht kaufbar"): derselbe alte Satz („eine
  Garantie führt nicht zu einem besseren Platz") ebenso berichtigt.

Build und Template. Textgate an den gebauten Seiten (beide mit `--erlaube-rechtswoerter`, wie für diese
Seiten vorgesehen): /festpreis-garantie/ **BESTANDEN**, /premium/ **BESTANDEN**.

## Site-weite Suche nach derselben alten Aussage

Gesucht in Antragsseite, Premium, Über uns, Fragen (FAQ-Daten), AGB, Ratgeber und Stadttexten.

**Dieselbe falsche Aussage — berichtigt:**
1. `pages/festpreis-garantie/index.astro` (Abschnitt „Was die Garantie kostet") — die Ausgangsstelle.
2. `pages/premium.astro:52` — „Eine Buchung … führt nicht zur Garantie, und eine Garantie führt nicht
   zu einem besseren Platz."

**AGB — nur gemeldet, nicht geändert (wie gewünscht):**
- `pages/agb.astro:37`: „Die Festpreis-Garantie ist nicht kaufbar." Das ist allein die
  Unkäuflichkeits-Aussage und **kein** Widerspruch (es wird nichts über die Reihenfolge behauptet).
  Unverändert gelassen.

**Geprüft und korrekt — kein Eingriff nötig** (behaupten nur Unkäuflichkeit / Trennung, nicht „kein
besserer Platz"):
- `pages/festpreis-garantie/antrag/index.astro:190`: „Die Garantie kann nicht gekauft werden. Bezahlte
  Plätze … sind davon unabhängig und als bezahlt gekennzeichnet." — stimmt (bezahlte Plätze sind von
  der Garantie unabhängig; kein Platz-Versprechen).
- `pages/ueber-uns.astro:47`: „Die Festpreis-Garantie ist nicht kaufbar; bezahlt wird nur Sichtbarkeit."
- `data/site.json` (FAQ der Startseite, Z. 113 und 136): „… kostenlos und nicht käuflich."
- `pages/premium.astro:51` (H2) und `pages/festpreis-garantie/index.astro` (Z. 24, 46, 215): korrekt,
  teils schon mit der richtigen Reihenfolge-Aussage („verschiebt die Reihenfolge nicht, weil jemand
  zahlt, sondern weil der Preis geprüft ist").
- Ratgeber und Stadttexte: keine Aussage über den Einfluss der Garantie auf die Platzierung.

## Bauen, Ausliefern, Prüfen

- `npm run build` (Build + Template) grün, Sitemap 2823.
- Textgate: /festpreis-garantie/ und /premium/ (dist, mit Flag) **BESTANDEN**, in Build und Template.
- `wrangler pages deploy` → Deploy `68d052dc`.
- `check_live.py … --expect-urls 2823` → **alle Prüfungen bestanden**.
- Live-Stichprobe: beide Seiten tragen den „hebt … vor die Betriebe ohne Garantie, aber nie über einen
  bezahlten Platz"-Satz, der alte „besserer Platz"-Satz ist weg.
