# Der Rückweg für Anträge: garantie.py, kontakt.py, Kontaktdaten, Antwortwege

**Datum** 2026-11-13 · **Stand** main · **Kein Deploy** (Probeläufe liefen auf einer Kopie mit
`--kein-bauen`, die Live-Seite blieb unverändert).

## 1. scripts/garantie.py — Festpreis-Garantie erteilen, ändern, entziehen, auflisten

Nach dem Muster von `verkauf.py`, mit dem es die Infrastruktur teilt (Build-Verzeichnis finden,
bauen, ausliefern, `check_live.py`, Sperre, Testschalter, laute Schlussmeldung). Es schreibt
**nur** die acht Garantie-Spalten (`geprueft`, `geprueft_jahr`, die sechs `garantie_*`),
führt `output/<slug>/garantie-hauptbuch.csv` (anhängend) und ruft vor dem Schreiben
`pruefe_kein_verlust` aus `_listings_guard.py`.

```
python3 scripts/garantie.py --slug <slug> --erteilen \
    --tag 89 --abend 30 --nacht 40 --anfahrt 0 --zylinder 39 --zylinder5mm 3 [--jahr 2026] --bestaetigt
python3 scripts/garantie.py --slug <slug> --aendern --tag 95 --nacht 45
python3 scripts/garantie.py --slug <slug> --entziehen
python3 scripts/garantie.py --liste
```

**Die sechs Voraussetzungen**, soweit aus den Daten lesbar (wiki/framework/siegel-programm.md):

| # | Voraussetzung | Prüfung im Skript |
|---|---|---|
| 2 | erreichbare Telefonnummer | **lesbar** — fehlt sie, **Abbruch** (die Nummer wird vor Erteilung angerufen) |
| 4 | ab 5 Bewertungen Schnitt ≥ 4,0 | **lesbar** — bei ≥ 5 Bewertungen und Schnitt < 4,0 **Abbruch**; bei < 5 Bewertungen **kein Riegel** (Satzung: die übrigen entscheiden) |
| 3 | die sechs Preise verbindlich | **gesetzt** — Pflichtangaben beim Erteilen, Grundpreis > 0 |
| 1 | vollständiges Impressum | **von Hand** — mit `--bestaetigt` zu bestätigen |
| 5 | kein Callcenter ohne Ortsbezug | **von Hand** (Hinweis, wenn der Eintrag keine feste Anschrift / Flächenbedienung hat) |
| 6 | unterschriebenes Serviceversprechen | **von Hand** |

Ohne `--bestaetigt` bricht das Erteilen ab und nennt die drei von Hand zu prüfenden
Voraussetzungen. Testschalter `--kein-deploy` / `--kein-bauen` wie bei `verkauf.py`.

## 2. scripts/kontakt.py + Kontaktbuch

Hält die Ansprache fest, ändert **keinen** Eintrag, liest `listings.csv` nur, baut/liefert
nichts. Zwei **anhängende** Bücher (nie überschrieben):
`output/<slug>/kontakt-hauptbuch.csv` (datum, eintrag_slug, weg, ergebnis, notiz) und
`output/<slug>/kontakt-sperrliste.csv` (datum, eintrag_slug, grund).

```
python3 scripts/kontakt.py eintragen --slug <slug> --weg telefon|email|formular --ergebnis "…" [--notiz "…"]
python3 scripts/kontakt.py sperren --slug <slug> [--grund "…"]
python3 scripts/kontakt.py --offen [--bundesland "…"] [--stadt "…"] [--alle]
python3 scripts/kontakt.py --stand
```

`--offen` (noch nie kontaktiert) lässt **eigene Betriebe**, **Gesperrte** und schon
**kontaktierte** weg; filterbar nach Bundesland (Spalte `state`) und Stadt. Bei vielen offenen
Einträgen ohne Filter zeigt es die Verteilung je Bundesland (vollständig mit `--alle`).
`--stand` zählt je Status.

## 3. Bestandsaufnahme der Kontaktdaten (nur Zahlen, keine Adressen)

- **Einträge gesamt: 3797.** Mit Telefon: **3717 (97 %)**. Mit E-Mail: **1144 (30 %)**.
  Beides: **1138**. Weder noch: **74**.
- **E-Mail-Adressen:** 1643 Vorkommen, 1459 eindeutige. Nach **Sammelpostfach** aussehend
  (`info@`, `kontakt@`, `service@`, …): **968**. Adressen, die **mehrfach** vorkommen: **114**
  (betreffen 298 Zeilen) — meist Ketten/Callcenter mit einer Zentraladresse.
- **Je Bundesland** (gesamt · Telefon · E-Mail):

| Bundesland | gesamt | Telefon | E-Mail |
|---|---:|---:|---:|
| Nordrhein-Westfalen | 886 | 868 | 284 |
| Bayern | 542 | 534 | 173 |
| Baden-Württemberg | 466 | 452 | 139 |
| Hessen | 305 | 298 | 72 |
| Niedersachsen | 305 | 302 | 93 |
| Berlin | 226 | 220 | 78 |
| Sachsen | 195 | 192 | 65 |
| Rheinland-Pfalz | 165 | 161 | 36 |
| Schleswig-Holstein | 132 | 130 | 41 |
| Brandenburg | 113 | 109 | 32 |
| Thüringen | 101 | 100 | 28 |
| Sachsen-Anhalt | 97 | 96 | 25 |
| Hamburg | 93 | 90 | 30 |
| Mecklenburg-Vorpommern | 73 | 71 | 21 |
| Saarland | 53 | 50 | 10 |
| Bremen | 45 | 44 | 17 |

**Folgerung:** Telefon ist der tragende Weg (97 %), die E-Mail-Abdeckung ist dünn (30 %) und zu
zwei Dritteln Sammelpostfächer. Der Anruf („Sie haben einen Eintrag …") bleibt der Hauptkanal;
E-Mail ist Nachfass, nicht Erstkontakt. Nichts versandt, keine Adressen notiert.

## 4. Antworten von info@die-besten-schluesseldienste.de — Wege, Kosten, Aufwand

**Ausgangslage.** Cloudflare **Email Routing** (geplanter Mail-Worker, [[mail-worker]]) ist
**nur Empfang**: eine Antwort auf eine weitergeleitete Mail geht von der Zieladresse (z. B.
Gmail) aus, **nicht** von `info@`. Um **als `info@`** zu senden, braucht es einen eigenen
Sender mit SPF/DKIM/DMARC auf der Domain. Der Footprint-Punkt: dieser Sender — Konto, Bezahlung,
Wiederherstellungs-Adresse/-Nummer, DKIM-Schlüssel — darf **nichts** mit den Schlüsseldienst-
Websites oder mit **LeadHawk** teilen (kein gemeinsamer Google-/Microsoft-Mandant, kein
gemeinsamer ESP/geteilter DKIM, keine LeadHawk-Versandstrecke).

| Weg | Was | Kosten | Aufwand | Footprint |
|---|---|---|---|---|
| **A. Eigenes unabhängiges Postfach (empfohlen)** | mailbox.org Standard o. ä., eigenes Konto nur fürs Verzeichnis; `info@` per IMAP/Webmail, Antwort **von Hand** | **~3 €/Monat** (mailbox.org Standard, eigene Domain; Zoho-Gratis geht auch, aber nur Webmail, kein IMAP) | gering–mittel: Postfach anlegen, SPF/DKIM/DMARC in die Cloudflare-DNS | **sauber**, wenn Konto + Zahlung getrennt sind |
| **B. Mail-Worker sendet programmatisch** | Empfang über Cloudflare Email Routing, Antwort als `info@` aus dem Worker über eine Versand-API | **Resend-Gratis** (100/Tag, 3.000/Monat) oder **Cloudflare Email Sending** auf Workers Paid (~5 $/Monat); Amazon SES ~0,10 $/1.000 | höher: Code + API-Konto + DKIM; passt aber zum ohnehin geplanten Worker | sauber, wenn das API-Konto frisch ist (nicht LeadHawks ESP) |
| **C. Gmail „Senden als" + externer SMTP** | `info@` als Absenderadresse in einem Gmail-Konto, Versand über fremden SMTP | SMTP-Kosten wie A/B; Gmail selbst kostenlos | gering | **riskant**: bindet `info@` an ein Google-Konto; nur mit einem ganz frischen Google-Konto sauber — sonst Verknüpfung über Wiederherstellung/Gerät |
| **D. Eigenes Google Workspace / Microsoft 365** | dedizierter Mandant nur fürs Verzeichnis | **~6 €/Nutzer/Monat** | mittel | funktioniert, aber schwerer und leichter verknüpfbar (Zahlung, Mandant) — nur wenn strikt getrennt |

**MailChannels** (früher der kostenlose Weg aus Cloudflare Workers) ist seit dem 31.08.2024
nicht mehr gratis (jetzt 100 Mails/Tag über die eigene API) — in Weg B durch Resend/SES ersetzt.

**Empfehlung:** Weg **A** für das Antworten von Hand (ein eigenes mailbox.org-Postfach, eigenes
Konto, eigene Zahlung, DKIM auf der Domain) — getrennt von allem anderen, geringe Kosten, kein
Code. Weg **B** zusätzlich, sobald der Mail-Worker automatisch bestätigen soll. **Nichts
eingerichtet.**

Quellen (Preise/Verfügbarkeit, Stand November 2026): Cloudflare Email Routing/Sending-Doku,
MailChannels End-of-Life-Hinweis, Resend-Preise, mailbox.org/Zoho-Preise.

## Probeläufe (auf einer Kopie, nichts ausgeliefert)

Kopie: `listings.csv` + `site.json` in ein Scratch-Verzeichnis, Aufrufe mit `--kein-bauen`.

**garantie.py** (Testeintrag `leipziger-…-leipzig`, nicht owned, 2167 Bewertungen, Schnitt 5,0):
- `--liste` → zeigt die **18** bestehenden Garantien mit Preisen.
- `--erteilen` **ohne** `--bestaetigt` → **Abbruch**, nennt (1)(5)(6) zur Handprüfung.
- `--erteilen` bei Schnitt 3,7 / 142 Bewertungen → **Abbruch** V4.
- `--erteilen` ohne Telefon → **Abbruch** V2.
- `--erteilen` mit fehlendem Preis → **Abbruch** V3.
- `--erteilen --bestaetigt --kein-bauen` → geschrieben (18 → **19**), Hauptbuch-Zeile `erteilt`,
  lauter „NICHT AUSGELIEFERT"-Banner.
- `--aendern --tag 95 --nacht 45` → Preise geändert, Hauptbuch-Zeile `geaendert`.
- `--entziehen` → Garantie-Spalten geleert (19 → **18**), Hauptbuch-Zeile `entzogen`.
- Die **18 bestehenden Garantien überlebten** jeden Schreibvorgang (die Sperre schlug nicht an).

**kontakt.py:**
- `--stand` anfangs: 3797 gesamt, 21 eigene, **3776 offen**.
- `eintragen` (telefon) + `eintragen` (email) → zwei Zeilen angehängt.
- `sperren` (mit Grund) → Sperrlisten-Zeile.
- `--offen --bundesland Hamburg` → **92** (von 93; der kontaktierte Hamburger Eintrag fehlt).
- gesperrter BW-Eintrag erscheint **nicht** in `--offen --bundesland Baden-Württemberg`.
- `--offen` ohne Filter → Verteilung je Bundesland, **3773** offen (3776 − 2 kontaktiert − 1 gesperrt).
- `--stand` danach: gesperrt 1, kontaktiert 2, offen 3773; je Weg und je Ergebnis aufgeschlüsselt.
- Beide Bücher sind reine Anhäng-CSV (Korrektur = neue Zeile).

## Festgehalten

Aufrufe von `garantie.py` und `kontakt.py` in CLAUDE.md (Abschnitte „Neu bauen bei Änderung" und
„Nach dem Start: das Kontaktbuch"); `garantie.py` in die Sperr- und Quellen-Absätze aufgenommen.
