---
title: Das Verzeichnis im Überblick
type: framework
status: current
updated: 2026-11-03
---

# Das Verzeichnis im Überblick

**Ein Verzeichnis ist eine geordnete Liste, auf Suchmaschinen hin gebaut.** Startseite,
Bundesland-Seiten, Stadtseiten, Einträge. Dieselbe Absicht wie eine einzelne Ortsseite, nur
in größerem Maßstab: „Schlüsseldienst in meiner Nähe" / „Schlüsseldienst Baden-Württemberg" /
„Schlüsseldienst Mannheim".

Dieses Verzeichnis ist **Die besten Schlüsseldienste**, `die-besten-schluesseldienste.de`,
alle Schlüsseldienste in Deutschland, herausgegeben von der DOM Holding GmbH. Branche, Land,
Domain und Herausgeber stehen fest ([[konventionen]]); sie werden nicht abgefragt und nicht
bewertet ([[gate-1-intake]]).

## Warum der Betreiber es baut, in dieser Reihenfolge

1. **Die eigenen Websites stärken.** Der Betreiber betreibt viele Schlüsseldienst-Websites.
   Eigene Website, Verzeichnis und Google-Unternehmensprofil belegen dieselbe Trefferliste
   dreifach. Was dabei erlaubt ist und was nicht, steht in [[footprint-rules]].
2. **Die oberen Plätze vermieten.** Premium-Eintrag, Stadt-Premium, Top-Platzierung
   ([[monetization-slots]]).
3. **Kunden daraus gewinnen.** Jeder Eintrag ist ein Betrieb, den man jetzt anrufen kann, und
   der sichtbare Hinweis „Noch keine Festpreis-Garantie" ist der Anlass ([[siegel-programm]]). Für
   Betreiber solcher Verzeichnisse sind sie die wichtigste Quelle für SEO-Kunden. Das
   Verzeichnis ist zugleich das Schaufenster: es kann sich tragen, auch wenn die Hälfte seiner
   Einträge nicht indexiert ist, weil es da ist, um Kunden zu gewinnen und ihnen zu zeigen,
   was der Betreiber kann.
4. **Später die eigene Software vermarkten.** Das Verzeichnis ist der Zugang zu allen
   Betrieben der Branche. Nichts davon wird jetzt gebaut und nichts davon steht auf der Site.

Werbebanner sind in dieser Größe draußen.

## Wie ein sauberes Verzeichnis aussieht

- **Eine Branche, ein Land, drei Ortsebenen:** Startseite → bis 16 Bundesländer → Städte →
  Einträge ([[site-architecture]]). Schlüsseldienst ist die Branche: alltäglich, dringlich,
  vierstellige Rechnungen sind möglich und es gibt wirklich etwas zu erklären.
- Statischer Astro-Build, Cloudflare Pages, aus einer CSV neu gebaut.
- Nur echte Einträge: bereinigt auf die Betriebe, die wirklich existieren und Bewertungen
  haben ([[listings-cleaning]]).
- Angereichert: Merkmale und eine Beschreibung je Eintrag, damit die Liste ein Werkzeug ist
  und kein Telefonbuch ([[enrichment]]).
- JSON-LD auf jeder Seite, echte Sitemap, schlanker Start ([[schema]], [[launch-lean]]).
- Eine Seite zum Beanspruchen, bezahlte Plätze und **die Festpreis-Garantie** vom ersten Tag an.
  Keine Zugänge für Betriebe; zwei Türen, jede von Hand geprüft ([[refresh-and-upkeep]]).
- Eine fertige, eigene Optik, damit es nicht aussieht wie von einer KI zusammengesetzt
  ([[design-seed]]).
- Ein benannter Herausgeber mit Impressum, Datenschutzerklärung und einer Seite „Über uns"
  ([[publisher-entity]]). Nach dem Start verdient es Links so, wie arbeitende Verzeichnisse es
  tun: Garantie-Nachweis, Pressemitteilungen, Ratgeberseiten, örtliche Inhalte
  ([[authority-and-links]]).

## Was am deutschen Markt anders ist

Vier Punkte, die jede Seite dieses Wikis berühren:

1. **Kein zulassungspflichtiges Handwerk.** Schlüsseldienst steht nicht in Anlage A der
   Handwerksordnung. Es gibt keine Lizenz, keine Zulassung, keine Meisterpflicht. Die
   englische Fassung baute an mehreren Stellen auf eine Lizenzbehörde; es gibt hier keine, und
   kein Text darf „lizenziert", „zugelassen" oder „zertifiziert" behaupten
   ([[konventionen]]).
2. **Überhöhte Rechnungen sind das Thema der Branche.** Verbraucherzentralen und die
   polizeiliche Kriminalprävention warnen seit Jahren vor Abzockern mit ortsfremden Nummern.
   Das ist der Grund, warum die Festpreis-Garantie existiert und warum keine Seite einen
   Preis nennt, der nicht belegt ist: im Eintrag stehen nur die Preise, die ein Betrieb
   verbindlich garantiert hat ([[siegel-programm]], [[page-types]]).
3. **Die Kategorie fängt fremde Gewerbe ein.** `locksmith` trifft in Deutschland auch
   Schuhmacher, Gravurbetriebe, Metallbauer und Baumärkte, dazu Kettenbetriebe und Callcenter
   ohne Ortsbezug. Gate 2 macht das sichtbar, der Mensch entscheidet in Gate 4
   ([[listings-cleaning]]). Das Merkmal `schluesseldienst_kern` ist dabei nur ein Hinweis, **nicht
   maßgeblich**: es lag im deutschen Lauf bei einem von sieben Grenzfällen falsch. Maßgeblich ist
   der **Text** der Beschreibung. Ein Eintrag bleibt, wenn der Text das **Öffnen von Türen** zeigt
   (Türöffnung, Türnotöffnung, ausgesperrt/Aussperrung, zerstörungsfreie Türöffnung), **oder** der
   Betrieb sich **selbst als Schlüsseldienst bezeichnet** – im Firmennamen oder im Text –, **oder**
   er einen Havarie-/Not-/Schlossnotdienst nennt, der sich nicht auf Tresore bezieht. Die
   Selbstbezeichnung zählt, weil „Schlüsseldienst" im Deutschen die Aussage ist, Türen zu öffnen;
   sie ist ein Beleg, kein Beiwerk. Sie zählt **nicht**, wenn der Text sie verneint oder abgrenzt
   („kein Schlüsseldienst", „Türöffnungen gehören nicht zum Angebot", „ein Schlüsseldienst im Sinne
   von Türöffnung ist das nicht"), und nicht, wenn sie sich auf einen Dritten bezieht (Verweis auf
   den ADAC-Schlüsseldienst). Ausgeschlossen wird, wessen einziger Bezug zu Schlössern im **Verkauf
   oder Einbau** liegt (Zylinder montieren, Schließanlagen planen, Zutrittskontrolle, Alarm, Video,
   Brandmeldetechnik, Tresorhandel) – auch bei `kern=true` (Regel vom 2026-11-04).
4. **Recht.** Impressum nach § 5 DDG, Datenschutzerklärung nach Art. 13 DSGVO, keine Karte
   und keine externe Schrift ohne Einwilligung ([[konventionen]], Recht). Das Wiki nennt die
   Pflichten; es ist keine Rechtsberatung, und ein Anwalt sollte die Endfassung prüfen.

## Kosten und Zeitablauf

- **Einträge:** ein paar Euro bei DataForSEO für die Kategorie in Deutschland. Die genaue Zahl
  steht erst nach `--estimate`; sie wird in Gate 1 genannt, bevor abgerufen wird. Auf dem
  Outscraper-Weg zahlt der Betreiber den Scrape selbst.
- **Bauen:** das Claude-Abonnement des Betreibers. Hosting kostenlos. Domain etwa 10 € im
  Jahr.
- **Zeitablauf:** dieselbe Reifekurve wie bei jeder neuen Site. Im ersten Monat indexiert, im
  dritten entscheidet Google, ab dem sechsten getragen.

**Es gibt für dieses Verzeichnis noch keine Messwerte.** Alle Zahlen in diesem Wiki, die aus
einem echten Lauf stammen, kommen aus dem **englischen Pilotprojekt** (Poolbauer in Florida,
Zaunbauer in Colorado) und sind dort als solche gekennzeichnet. Sie sind Größenordnungen für
den Aufwand und sagen über den deutschen Markt nichts.

## Siehe auch
[[konventionen]] · [[site-architecture]] · [[siegel-programm]] · [[monetization-slots]] · [[launch-lean]]
