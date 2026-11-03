---
title: Footprint-Regeln
type: framework
status: stable
updated: 2026-11-03
---

# Footprint-Regeln

Der Betreiber besitzt selbst viele Schlüsseldienst-Websites. Das Verzeichnis soll sie
stärken, und gleichzeitig darf nicht erkennbar sein, dass Verzeichnis und Websites derselben
Hand gehören. Diese Seite sagt, wie beides zusammengeht.

## Die Grundregel

**Eigene Betriebe werden wie jeder andere Betrieb gelistet.** Dieselbe Karte, dieselbe
Eintragsvorlage, dieselbe `nofollow`-Regel auf dem Link zur Website, solange der Betrieb keine
bezahlte Stufe zum **öffentlichen Preis** gebucht hat. Keine seitenweiten Links, kein
Zeichen „empfohlen", keine Sonderplatzierung, kein Siegel ohne erfüllte Kriterien.

Die Bevorzugung ist echt, aber nicht sichtbar: das Verzeichnis enthält alle Schlüsseldienste
in Deutschland, und ein paar davon zu besitzen, fällt darin nicht auf. Die Stärkung kommt
daraus, dieselbe Trefferliste dreifach zu belegen (eigene Website, Verzeichnis,
Google-Unternehmensprofil), nicht aus Links.

Die Spalte `owned` aus Gate 2 existiert, damit der Bericht die eigenen Zeilen dem Menschen
zeigt. **Sie darf die Darstellung nie verändern.** Kein Template, kein Bauschritt und keine
Sortierung liest `owned`.

## Zusätzlich für dieses Projekt

- **Je Stadt höchstens ein eigener Betrieb auf einem bezahlten Platz.** Auch wenn dem
  Betreiber in einer Stadt mehrere Betriebe gehören: nur einer bekommt Premium, Stadt-Premium
  oder Top-Platzierung. Zwei oder drei eigene Namen auf den oberen Plätzen derselben Stadt
  sind das Muster, das die ganze Tarnung auffliegen lässt. Gate 4 prüft das gegen die
  `owned`-Spalte und nennt jeden Verstoß im Plan.
- **Eigenes Cloudflare-Konto.** Das Verzeichnis liegt auf einem Konto, das keine der
  Schlüsseldienst-Websites hält: eigene Domain, eigenes Konto, eigene Abrechnung. Wo die
  Registrierungsstelle es zulässt, werden die Inhaberangaben variiert.
- **Kein Google Analytics, keine Search Console auf dieser Domain.** Ausgewertet wird mit
  Cloudflares eigener Statistik (ohne Cookies, deshalb ohne Einwilligung zulässig,
  [[konventionen]]) und mit den Berichten des Indexierungsdienstes. Ein Konto, das die
  Websites und das Verzeichnis zugleich sieht, verbindet sie.
- **Keine gegenseitigen Links** zwischen den eigenen Websites und dem Verzeichnis, über die
  Eintragsseiten hinaus, die jeder Betrieb hat. Kein Linktausch, kein Fußzeilenlink.
- Dieselbe Trennung gilt für Mailadressen, Zahlungsdienste und die Angaben im Impressum, wo
  die Rechtslage das zulässt: das Impressum nennt die DOM Holding GmbH als Herausgeber des
  Verzeichnisses, nicht die einzelnen Betriebe.

## Merz Sicherheit in Mannheim

Merz Sicherheit ist die Hauptfirma des Betreibers in Mannheim, und Mannheim ist die
wichtigste Stadt des Verzeichnisses. Der Betrieb bekommt dort **Premium-Eintrag und
Top-Platzierung zum öffentlichen Preis** aus `templates/featured-tiers.md`. Das ist ein
normaler Vorgang und wird so behandelt: dieselbe Buchung, derselbe Preis, derselbe Eintrag in
der CSV (`premium=true`, `best_of_rank`), dieselbe Darstellung wie bei jedem anderen
Betrieb, der diese Stufen kauft.

Es ist **keine Sonderregel** und wird nirgends als eine beschrieben: nicht auf der Seite,
nicht im Plan, nicht im Build-Bericht. Dass es derselbe Hand gehört, steht in `01-umfang.md`
und in der `owned`-Spalte, weil der Mensch das wissen muss, und sonst nirgends. Und weil je
Stadt nur ein eigener Betrieb einen bezahlten Platz bekommt, ist mit Merz Sicherheit der Platz
in Mannheim belegt.

Das Siegel bekommt Merz Sicherheit nur, wenn der Betrieb die sechs Kriterien erfüllt und den
Antrag stellt wie jeder andere ([[siegel-programm]]). Es ist nicht kaufbar, und es wird auch
dem eigenen Betrieb nicht geschenkt.

## Siehe auch
[[konventionen]] · [[site-architecture]] · [[monetization-slots]] · [[siegel-programm]]
