---
title: Gate 5 – Faktensammlung
type: output
status: in-arbeit
updated: 2026-11-04
---

# Gate 5 – Faktensammlung

Jede Aussage über Recht, Gewerbe, Preise, örtliche Besonderheiten oder Auftragsverarbeiter mit
Quelle und Abrufdatum. Quellenreihenfolge für Branchenfakten ([[konventionen]]): Handwerkskammer,
Stadt-/Gemeindeportale (Gewerbeamt), Verbraucherzentrale, polizei-beratung.de, Stiftung Warentest.
Nicht als Quelle: andere Schlüsseldienst-Websites, Branchenbücher, Presseportale. Ein Punkt mit nur
einer kommerziellen Quelle gilt als unbelegt.

## Auftragsverarbeiter (für Impressum/Datenschutz)

### Zahlungsdienst Stripe
- **Vertragspartei im EWR:** Stripe Payments Europe, Limited, One Wilton Park, Wilton Place,
  Dublin 2, D02 FX04, Irland.
- **Quelle:** Stripe, „Guide for Service of Process, Legal Notices and Law Enforcement Requests"
  (`stripe.com/legal/legal-process-guide`) – nennt diese Gesellschaft als Vertragspartei für den
  Europäischen Wirtschaftsraum. Bestätigt über das LEI-Register / irisches Companies Registration
  Office, **Registernummer 513174**. **Abrufdatum 04.11.2026.**
- **Drittland:** Ja. Die irische Gesellschaft ist Vertragspartei; es findet eine Weiterübermittlung
  an Stripe, Inc. (USA) unter Standardvertragsklauseln statt. In `site.json` als
  `processors.payment` mit `thirdCountry: true` hinterlegt.
- **Status:** belegt (Primärquelle des Anbieters + unabhängiges Register).

### Formulardienst
- **Offen.** Formsprees eigene Unterlagen nennen keine Anschrift, Wirtschaftsdatenbanken
  widersprechen sich (Austin vs. Seattle). Es wird **nichts** eingetragen; `processors.form.company`
  bleibt `OFFEN_` (die Datenschutzerklärung nennt dann nur den Namen des Dienstes). Entfällt ganz,
  wenn die Annahme auf eine Cloudflare Pages Function umgestellt wird (siehe
  `berichte/2026-11-04-startsperren-zahlung-und-formular.md`): dann ist Cloudflare der einzige
  Verarbeiter und steht ohnehin als Hoster in der Datenschutzerklärung.

## Branchen- und Rechtsfakten
Werden beim Schreiben der Stadt- und Ratgebertexte in Gate 5 ergänzt (mit Quelle und Abrufdatum).
Grundsatz, der in keinem Text fehlen darf: Das Schlüsseldienst-Handwerk ist in Deutschland **kein
zulassungspflichtiges Handwerk** nach Anlage A der Handwerksordnung – keine Lizenz, keine
Meisterpflicht. Belegbar und erlaubt: Gewerbeanmeldung, Handelsregistereintrag, freiwillige
Mitgliedschaften, selbst genannte Qualifikationen.
</content>
