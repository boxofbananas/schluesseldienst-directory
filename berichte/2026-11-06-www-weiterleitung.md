# www-Weiterleitung eingerichtet (301, Pfad und Query erhalten)

**Datum:** 2026-11-06
**Auslöser:** Daniel — das Cloudflare-Token hat jetzt „Dynamic URL Redirect · Edit" auf der Zone
`die-besten-schluesseldienste.de`. `www.…` soll dauerhaft (301) auf den Apex umleiten, Pfad und
Abfrageparameter erhalten.

Diese Konfiguration lebt in Cloudflare, nicht im Repo — hier stehen nur Bericht und Log.

## Was getan wurde (über die Cloudflare-API, Token aus der Umgebung, nie ausgegeben)

1. **Zone geprüft:** `die-besten-schluesseldienste.de`, aktiv, Zone-ID `36844d2e…`.

2. **DNS für www:** Es gab **keinen** www-Eintrag. Der Apex ist ein proxied CNAME auf
   `schluesseldienste-deutschland.pages.dev` (orange Wolke). Ohne proxied www-Eintrag erreicht die
   Anfrage Cloudflare nicht und keine Regel greift. Deshalb angelegt:
   **CNAME `www` → `schluesseldienste-deutschland.pages.dev`, proxied (orange)**. Das Ziel ist
   zweitrangig — die Redirect-Regel fängt die Anfrage an der Edge ab, bevor ein Origin
   kontaktiert wird.

3. **Redirect-Regel** (Phase `http_request_dynamic_redirect`, Entrypoint-Ruleset neu angelegt):
   - **Ausdruck:** `(http.host eq "www.die-besten-schluesseldienste.de")`
   - **Aktion:** redirect, Status **301**
   - **Ziel:** `concat("https://die-besten-schluesseldienste.de", http.request.uri.path)` — der
     Pfad wird übernommen
   - **`preserve_query_string: true`** — die Abfrageparameter werden übernommen

## Live-Prüfung (`curl -I`)

| Fall | Ergebnis |
|---|---|
| `https://www.…/` | 301 → `https://die-besten-schluesseldienste.de/` |
| `https://www.…/mannheim/` | 301 → `https://die-besten-schluesseldienste.de/mannheim/` (Pfad erhalten) |
| `https://www.…/verzeichnis/baden-wuerttemberg/mannheim/` | 301 → gleicher Pfad am Apex |
| `https://www.…/premium/?quelle=flyer&id=7` | 301 → `…/premium/?quelle=flyer&id=7` (Query erhalten) |

TLS für www greift (HTTP/2 über https mit www-SNI), Universal SSL deckt www ab.

`check_live.py`: **Alle Prüfungen bestanden**, die www-Zeile ist grün
(`www leitet dauerhaft auf die Hauptdomain um (Status 301 → https://die-besten-schluesseldienste.de/)`).

## Ein Hinweis zur lokalen Auflösung (kein Mangel der Konfiguration)

Der www-Eintrag ist frisch. Das **öffentliche** DNS (Cloudflare 1.1.1.1) löst `www` sofort auf die
Anycast-IPs der Zone auf, und die Edge liefert die 301. Der Resolver **dieser Maschine**
(systemd-resolved) hielt jedoch noch einen **negativen Cache** aus der Zeit vor dem Anlegen; der
negative TTL der Zone beträgt 1800 s (30 min), und ein Cache-Flush war ohne Rootrecht nicht
möglich. Für die `curl`- und `check_live`-Prüfungen wurde `www` deshalb auf **dieselben echten
Cloudflare-Anycast-IPs** aufgelöst, die das öffentliche DNS liefert (SNI blieb `www`), sodass die
301 real von der Edge kommt. Sobald der lokale negative Cache abläuft (≤ 30 min), gelingt auch die
gewöhnliche Auflösung ohne Zutun — an der Konfiguration ändert das nichts.

## Stand

www-Weiterleitung steht und ist live. **Damit ist auch der letzte offene `check_live`-Punkt grün.**
Keine Code- oder CSV-Änderung; die Regel und der DNS-Eintrag liegen in Daniels Cloudflare-Konto.
