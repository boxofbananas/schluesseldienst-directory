#!/usr/bin/env python3
"""Der Mail-Worker des Verzeichnisses: Schlüssel speichern, prüfen, Worker einrichten, neu
ausliefern, das Beanspruchungsformular anschließen.

  python3 scripts/mail_worker.py keys --slug <slug>                 # zeigt den Terminal-Befehl, den der Betreiber zum Speichern des Schlüssels ausführt
  python3 scripts/mail_worker.py save-key anthropic --slug <slug>   # führt der Betreiber im eigenen Terminal aus: fragt den Schlüssel ab (verdeckt), testet ihn, speichert ihn
  python3 scripts/mail_worker.py save-key cloudflare --slug <slug>  # nur, wenn mit einem API-Token statt mit `wrangler login` ausgeliefert wird
  python3 scripts/mail_worker.py check --slug <slug>                # sagt, ob die gespeicherten Schlüssel funktionieren, ohne sie auszugeben
  python3 scripts/mail_worker.py setup --slug <slug> --review-to <e-mail> [--name <worker-name>] [--account-id <kennung>] [--forward-to <e-mail>]
                                                                    # templates/worker kopieren, wrangler.jsonc aus site.json füllen, listings.json,
                                                                    # KV-Namensraum, Geheimnisse, ausliefern, WORKER_URL festhalten, eine Testanfrage senden
  python3 scripts/mail_worker.py deploy --slug <slug>               # nach einer Änderung an den Einträgen: listings.json erneuern und neu ausliefern
  python3 scripts/mail_worker.py wire-form --slug <slug>            # das Formular in site.json auf /claim des Workers zeigen lassen (danach Gate 5 und die Site ausliefern)

Wo die Geheimnisse liegen: auf einem Mac im Schlüsselbund (Einträge `anthropic-<worker-name>`,
`<worker-name>-key`, `<worker-name>-url`, und `cloudflare-<worker-name>`, wenn ein Token benutzt
wird); sonst in ~/.directory-blueprint/secrets.json (eine Datei, die nur der Besitzer lesen
kann). Nichts wird je in diesen Ordner geschrieben, ausgegeben oder im Gespräch abgefragt. Das
Ausliefern benutzt den `wrangler login` aus Gate 6, außer CLOUDFLARE_API_TOKEN ist gesetzt oder
ein Token wurde mit `save-key cloudflare` gespeichert.

Die Namen der Worker-Variablen (`BRAND`, `TIERS`, `NICHE_PLURAL`, `STATE_NAME`, `NAME_NOISE` …)
bleiben englisch: `templates/worker/src/index.ts` liest sie so. `STATE_NAME` trägt in dieser
dreistufigen Fassung das **Land** („Deutschland"), weil es kein einzelnes Bundesland gibt; die
englische Fassung hatte einen Bundesstaat.
"""
import argparse, getpass, json, os, platform, re, secrets as pysecrets, shutil, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
WIN = platform.system() == "Windows"
PY = "python" if WIN else "python3"
NPX = "npx.cmd" if WIN else "npx"


# ---------- secret store ----------

def _file_store():
    return os.path.join(os.path.expanduser("~"), ".directory-blueprint", "secrets.json")


def load_secret(item):
    """Der gespeicherte Wert, oder eine leere Zeichenfolge."""
    if platform.system() == "Darwin":
        r = subprocess.run(["security", "find-generic-password", "-s", item, "-w"], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    p = _file_store()
    if not os.path.exists(p):
        return ""
    return json.load(open(p, encoding="utf-8")).get(item, "")


def save_secret(item, value):
    if platform.system() == "Darwin":
        r = subprocess.run(["security", "add-generic-password", "-U", "-a", os.environ.get("USER", "me"), "-s", item, "-w", value],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"{item} konnte nicht im Schlüsselbund gespeichert werden: {r.stderr.strip()}")
        return "dem Schlüsselbund des Macs"
    p = _file_store()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    data = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    data[item] = value
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass
    return p


# ---------- the key checks ----------

def check_anthropic(key):
    req = urllib.request.Request("https://api.anthropic.com/v1/models", headers={"x-api-key": key, "anthropic-version": "2023-06-01"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200, "der Schlüssel antwortet"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Anthropic antwortet mit 401: das ist kein funktionierender Schlüssel (beginnt er mit cfat_, ist es ein Cloudflare-Token, an der falschen Stelle eingefügt)"
        return False, f"Anthropic antwortet mit {e.code}"
    except urllib.error.URLError as e:
        return False, f"api.anthropic.com ist nicht erreichbar: {e.reason}"


def check_cloudflare(token):
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/user/tokens/verify", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            ok = json.loads(r.read()).get("success")
            return bool(ok), "der Token ist gültig" if ok else "Cloudflare hat den Token nicht angenommen"
    except urllib.error.HTTPError as e:
        return False, f"Cloudflare antwortet mit {e.code}: kein funktionierender Token (ein Schlüssel, der mit sk-ant- beginnt, ist der Anthropic-Schlüssel, an der falschen Stelle eingefügt)"
    except urllib.error.URLError as e:
        return False, f"api.cloudflare.com ist nicht erreichbar: {e.reason}"


# ---------- config ----------

def worker_dir(slug):
    return os.path.join(ROOT, "output", slug, "worker")


def site_dir(slug):
    return os.path.join(ROOT, "output", slug, "site")


def read_jsonc(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return json.loads(text)


def write_config(path, cfg):
    head = ("// Einstellungen des Mail-Workers, von scripts/mail_worker.py aus der site.json der Site geschrieben. Geheimnisse\n"
            "// werden mit wrangler secret put gesetzt und stehen nie hier. SEND_FROM bleibt auf der Hauptdomain (eine\n"
            "// mail.-Unterdomain lässt Antworten auflaufen).\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


def worker_name_for(slug, cfg=None):
    if cfg and not cfg["name"].startswith("REPLACE"):
        return cfg["name"]
    return re.sub(r"[^a-z0-9-]", "-", slug.lower()).strip("-")[:50] + "-mail"


def load_config(slug):
    p = os.path.join(worker_dir(slug), "wrangler.jsonc")
    if not os.path.exists(p):
        sys.exit(f"unter output/{slug}/worker gibt es noch keinen Worker: {PY} scripts/mail_worker.py setup --slug {slug} --review-to <e-mail>")
    return p, read_jsonc(p)


def wrangler_env(name, account_id=None):
    env = dict(os.environ)
    token = env.get("CLOUDFLARE_API_TOKEN") or load_secret(f"cloudflare-{name}")
    if token:
        env["CLOUDFLARE_API_TOKEN"] = token
    if account_id:
        env["CLOUDFLARE_ACCOUNT_ID"] = account_id
    return env


def wrangler(args, cwd, env, input_text=None, quiet=False):
    r = subprocess.run([NPX, "wrangler", *args], cwd=cwd, env=env, input=input_text, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        if "Authentication error" in out or "10000" in out:
            sys.exit("wrangler: Anmeldefehler. Entweder `npx wrangler login` im Worker-Ordner ausführen (die Anmeldung aus Gate 6, "
                     "im Cloudflare-Konto, auf dem das Verzeichnis liegt), oder mit `save-key cloudflare` einen Token speichern, der in "
                     "diesem Konto erstellt wurde.\n" + out[-1500:])
        sys.exit(f"wrangler {' '.join(args)} ist gescheitert:\n{out[-3000:]}")
    if not quiet:
        print(out.strip()[-1200:])
    return out


# ---------- commands ----------

def cmd_keys(a):
    name = worker_name_for(a.slug, read_jsonc(os.path.join(worker_dir(a.slug), "wrangler.jsonc")) if os.path.exists(os.path.join(worker_dir(a.slug), "wrangler.jsonc")) else None)
    script = os.path.abspath(__file__)
    print("Das führen Sie in Ihrem eigenen Terminal aus. Der Befehl fragt den Schlüssel erst nach dem Start ab: zuerst starten, dann den Schlüssel kopieren und an der Eingabeaufforderung einfügen (das Eingefügte bleibt verdeckt):")
    print()
    print(f'  {PY} "{script}" save-key anthropic --slug {a.slug}')
    print()
    print(f"Er testet den Schlüssel bei Anthropic und speichert ihn als `anthropic-{name}`. Ausgeliefert wird mit Ihrem `wrangler login` aus Gate 6.")
    print("Nur wenn Sie stattdessen mit einem API-Token ausliefern (zum Beispiel bei zwei Cloudflare-Konten), zusätzlich:")
    print()
    print(f'  {PY} "{script}" save-key cloudflare --slug {a.slug}')
    print()
    print("Dieser Token braucht die Kontoberechtigungen Workers Scripts: Edit und Workers KV Storage: Edit (dazu Cloudflare Pages: Edit für die Site) und muss im Konto erstellt sein, auf dem das Verzeichnis liegt.")


def cmd_save_key(a):
    name = worker_name_for(a.slug, read_jsonc(os.path.join(worker_dir(a.slug), "wrangler.jsonc")) if os.path.exists(os.path.join(worker_dir(a.slug), "wrangler.jsonc")) else None)
    if not sys.stdin.isatty():
        sys.exit("das in Ihrem eigenen Terminal ausführen, nicht aus Claude Code heraus: es fragt den Schlüssel ab und verdeckt, was Sie einfügen")
    if a.which == "anthropic":
        value = getpass.getpass("Den Anthropic-API-Schlüssel einfügen (beginnt mit sk-ant-), dann Eingabetaste. Die Eingabe bleibt verdeckt: ").strip()
        ok, why = check_anthropic(value)
        item = f"anthropic-{name}"
    else:
        value = getpass.getpass("Den Cloudflare-API-Token einfügen, dann Eingabetaste. Die Eingabe bleibt verdeckt: ").strip()
        ok, why = check_cloudflare(value)
        item = f"cloudflare-{name}"
    if not value:
        sys.exit("nichts eingefügt; den Befehl erneut ausführen")
    if not ok:
        sys.exit(f"nicht gespeichert: {why}. Den Schlüssel erneut kopieren und den Befehl erneut ausführen.")
    where = save_secret(item, value)
    print(f"als `{item}` in {where} gespeichert ({why}). Sagen Sie Claude Code jetzt: der Schlüssel ist gespeichert.")


def cmd_check(a):
    cfg = None
    p = os.path.join(worker_dir(a.slug), "wrangler.jsonc")
    if os.path.exists(p):
        cfg = read_jsonc(p)
    name = worker_name_for(a.slug, cfg)
    problems = 0
    key = load_secret(f"anthropic-{name}")
    if not key:
        print(f"anthropic-{name}: nicht gespeichert. Der Betreiber führt in seinem Terminal aus:  {PY} scripts/mail_worker.py save-key anthropic --slug {a.slug}"); problems += 1
    else:
        ok, why = check_anthropic(key)
        print(f"anthropic-{name}: {'in Ordnung' if ok else 'FEHLER'}, {why}")
        problems += 0 if ok else 1
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or load_secret(f"cloudflare-{name}")
    if token:
        ok, why = check_cloudflare(token)
        print(f"cloudflare-{name}: {'in Ordnung' if ok else 'FEHLER'}, {why}")
        problems += 0 if ok else 1
    else:
        r = subprocess.run([NPX, "wrangler", "whoami"], cwd=ROOT, capture_output=True, text=True)
        logged = "You are logged in" in (r.stdout + r.stderr)
        print("cloudflare: " + ("die wrangler-Anmeldung aus Gate 6 ist aktiv" if logged else "keine wrangler-Anmeldung und kein Token. Zuerst `npx wrangler login` (Gate 6) ausführen."))
        problems += 0 if logged else 1
    if load_secret(f"{name}-key"):
        print(f"{name}-key und {name}-url: gespeichert (die Prüfliste ist über scripts/mail_inbox.py erreichbar)")
    sys.exit(1 if problems else 0)


def fill_from_site(slug, cfg, review_to, forward_to, name):
    sj = os.path.join(site_dir(slug), "src", "data", "site.json")
    if not os.path.exists(sj):
        sys.exit(f"unter output/{slug}/site gibt es keine Site: Gate 5 muss laufen, bevor der Worker eingerichtet wird")
    site = json.load(open(sj, encoding="utf-8"))
    domain = site["domain"].strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
    if domain in ("", "example.com"):
        sys.exit("in site.json steht noch die Platzhalter-Domain; der Worker braucht die echte")
    tiers = site.get("tiers", {})
    # Die Stufennamen wie in templates/featured-tiers.md; die Preise kommen aus site.json.
    tier_text = (f"Stadt-Premium, oberste Karte auf der Stadtseite: {tiers.get('city', {}).get('price', '29 € im Monat')}. "
                 f"Premium-Eintrag (Fotos, gefolgte Links, vollständiges Profil): {tiers.get('premium', {}).get('price', '97 € im Jahr')}. "
                 f"Top-Platzierung: {tiers.get('bestOf', {}).get('price', 'einmalig, Preis auf Anfrage')}. "
                 "Der Eintrag selbst ist kostenlos, und die Festpreis-Garantie ist nicht kaufbar: bezahlt wird nur Sichtbarkeit.")
    niche = site["niche"]
    # Drei Ebenen: es gibt keinen einzelnen Bundesstaat. Das Gebiet des Verzeichnisses ist das Land
    # aus site.json → country; die Worker-Variable heißt weiter STATE_NAME, weil
    # templates/worker/src/index.ts sie so liest.
    gebiet = (site.get("country") or {}).get("name") or (site.get("state") or {}).get("name") or ""
    noise = set()
    for w in (niche.get("singular", "") + " " + niche.get("plural", "") + " " + niche.get("title", "") + " " + gebiet).lower().split():
        w = re.sub(r"[^a-zäöüß'&-]", "", w)
        if len(w) > 3:
            noise.add(w)
    cfg["name"] = name
    v = cfg["vars"]
    v["BRAND"] = site["brand"]
    v["SITE_URL"] = f"https://{domain}"
    v["MAIL_ADDRESS"] = f"hello@{domain}"
    v["SEND_FROM"] = f"hello@{domain}"
    v["REVIEW_TO"] = review_to
    v["FORWARD_TO"] = forward_to or ""
    v["TIERS"] = tier_text
    v["NICHE_PLURAL"] = niche.get("plural", "Betriebe")
    v["STATE_NAME"] = gebiet
    v["NAME_NOISE"] = ",".join(sorted(noise))
    return cfg


def refresh_listings(slug):
    csv_path = os.path.join(site_dir(slug), "src", "data", "listings.csv")
    out = os.path.join(worker_dir(slug), "src", "listings.json")
    r = subprocess.run([PY, os.path.join(SCRIPTS, "make_worker_listings.py"), csv_path, out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("listings.json konnte nicht geschrieben werden:\n" + (r.stderr or r.stdout))
    print(r.stdout.strip())


def cmd_setup(a):
    wd = worker_dir(a.slug)
    if not os.path.exists(wd):
        shutil.copytree(os.path.join(ROOT, "templates", "worker"), wd, ignore=shutil.ignore_patterns("node_modules", ".wrangler"))
        print(f"templates/worker nach output/{a.slug}/worker kopiert")
    cfg_path, cfg = load_config(a.slug)
    name = a.name or worker_name_for(a.slug, cfg)
    cfg = fill_from_site(a.slug, cfg, a.review_to, a.forward_to, name)
    if a.account_id:
        cfg["account_id"] = a.account_id
    write_config(cfg_path, cfg)
    print(f"wrangler.jsonc gefüllt: {name}, {cfg['vars']['MAIL_ADDRESS']}, Prüf-E-Mails an {a.review_to}")
    refresh_listings(a.slug)

    key = load_secret(f"anthropic-{name}")
    if not key:
        sys.exit(f"der Anthropic-Schlüssel ist noch nicht gespeichert. Der Betreiber führt in seinem eigenen Terminal aus:\n  {PY} scripts/mail_worker.py save-key anthropic --slug {a.slug}")
    ok, why = check_anthropic(key)
    if not ok:
        sys.exit(f"der gespeicherte Anthropic-Schlüssel funktioniert nicht ({why}); der Betreiber führt save-key erneut aus")

    env = wrangler_env(name, a.account_id)
    if not os.path.exists(os.path.join(wd, "node_modules")):
        r = subprocess.run(["npm.cmd" if WIN else "npm", "install", "--no-audit", "--no-fund"], cwd=wd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("npm install ist im Worker-Ordner gescheitert:\n" + r.stderr[-2000:])
        print("npm install fertig")

    if cfg["kv_namespaces"][0]["id"].startswith("REPLACE"):
        out = wrangler(["kv", "namespace", "create", "INBOX"], wd, env, quiet=True)
        m = re.search(r'"id":\s*"([0-9a-f]{32})"', out) or re.search(r"id\s*=\s*\"?([0-9a-f]{32})", out)
        if not m:
            sys.exit("die Kennung des neuen KV-Namensraums ließ sich nicht aus der Ausgabe von wrangler lesen:\n" + out[-1500:])
        cfg["kv_namespaces"][0]["id"] = m.group(1)
        write_config(cfg_path, cfg)
        print(f"KV-Namensraum INBOX angelegt ({m.group(1)[:8]}...)")

    inbox_key = load_secret(f"{name}-key")
    if not inbox_key:
        inbox_key = pysecrets.token_hex(24)
        save_secret(f"{name}-key", inbox_key)
        print(f"Postfach-Schlüssel erzeugt und als {name}-key gespeichert")
    wrangler(["secret", "put", "ANTHROPIC_API_KEY"], wd, env, input_text=key + "\n", quiet=True)
    wrangler(["secret", "put", "INBOX_KEY"], wd, env, input_text=inbox_key + "\n", quiet=True)
    print("Geheimnisse am Worker gesetzt (ANTHROPIC_API_KEY, INBOX_KEY)")

    out = wrangler(["deploy"], wd, env, quiet=True)
    m = re.search(r"https://[a-z0-9.-]+\.workers\.dev", out)
    if not m:
        sys.exit("ausgeliefert, aber die Adresse des Workers stand nicht in der Ausgabe von wrangler:\n" + out[-1500:])
    url = m.group(0).rstrip("/")
    if cfg["vars"].get("WORKER_URL") != url:
        cfg["vars"]["WORKER_URL"] = url
        write_config(cfg_path, cfg)
        wrangler(["deploy"], wd, env, quiet=True)     # die zweite Auslieferung trägt WORKER_URL, den die Links der Prüfseite brauchen
    save_secret(f"{name}-url", url)
    print(f"ausgeliefert: {url}")

    # eine Testanfrage, ohne Empfangsbestätigung an irgendwen; die Prüf-E-Mail geht an REVIEW_TO
    data = urllib.parse.urlencode({"business": "Setup test", "name": "Verzeichnis-Baukasten", "email": a.review_to, "phone": "",
                                   "changes": "Das ist der Einrichtungstest aus scripts/mail_worker.py. Bitte übergehen.", "_noack": "1"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f"{url}/claim", data=data, method="POST"), timeout=30)
    except urllib.error.HTTPError as e:
        if e.code not in (301, 302, 303):
            sys.exit(f"die Testanfrage wurde abgewiesen: {e.code}")
    item = None
    for _ in range(12):
        time.sleep(5)
        try:
            req = urllib.request.Request(f"{url}/inbox?status=new", headers={"Authorization": f"Bearer {inbox_key}"})
            items = json.loads(urllib.request.urlopen(req, timeout=30).read())
        except Exception:
            continue
        item = next((i for i in items if i.get("subject", "").startswith("Claim form: Setup test")), None)
        if item and (item.get("triage") or item.get("triage_error")):
            break
    if not item:
        sys.exit("die Testanfrage ist nicht in der Liste aufgetaucht; das laufende Protokoll mit `npx wrangler tail` im Worker-Ordner lesen und erneut senden")
    if item.get("triage_error"):
        print(f"Testanfrage ist in der Liste, aber die Einordnung ist gescheitert: {item['triage_error']}. Ein neuer ANTHROPIC_API_KEY braucht manchmal eine Minute; erneut einordnen mit  {PY} scripts/mail_inbox.py --slug {a.slug} --retriage {item['id']}")
    else:
        t = item["triage"]
        print(f"Testanfrage eingeordnet: {t['category']} (Sicherheit {t['confidence']:.2f}); die Prüf-E-Mail ist auf dem Weg an {a.review_to}. Übergehen mit  {PY} scripts/mail_inbox.py --slug {a.slug} --ignore {item['id']}")
    print(f"\nAls nächstes: in der Cloudflare-Oberfläche die Domain öffnen, Email, Email Routing, Routing rules, Create address: hello, Send to a Worker, {name}.")


def cmd_deploy(a):
    cfg_path, cfg = load_config(a.slug)
    refresh_listings(a.slug)
    wrangler(["deploy"], worker_dir(a.slug), wrangler_env(cfg["name"], cfg.get("account_id")), quiet=True)
    print(f"{cfg['name']} mit den aktuellen Einträgen ausgeliefert")


def cmd_wire_form(a):
    cfg_path, cfg = load_config(a.slug)
    url = cfg["vars"].get("WORKER_URL")
    if not url:
        sys.exit("der Worker hat noch keine WORKER_URL; zuerst setup ausführen")
    sj = os.path.join(site_dir(a.slug), "src", "data", "site.json")
    site = json.load(open(sj, encoding="utf-8"))
    site.setdefault("contact", {})["formEndpoint"] = f"{url}/claim"
    with open(sj, "w", encoding="utf-8") as fh:
        json.dump(site, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"site.json contact.formEndpoint zeigt jetzt auf {url}/claim. Gate 5 (bauen) laufen lassen und die Site ausliefern; danach das alte Formular beim Formulardienst löschen.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    HILFE = {"keys": "den Terminal-Befehl zum Speichern des Schlüssels zeigen",
             "check": "sagen, ob die gespeicherten Schlüssel funktionieren",
             "deploy": "listings.json erneuern und den Worker neu ausliefern",
             "wire-form": "das Beanspruchungsformular auf /claim des Workers zeigen lassen"}
    for c in ("keys", "check", "deploy", "wire-form"):
        s = sub.add_parser(c, help=HILFE[c])
        s.add_argument("--slug", required=True, help="der Build-Ordner unter output/")
    s = sub.add_parser("save-key", help="einen Schlüssel im eigenen Terminal abfragen, testen und speichern")
    s.add_argument("which", choices=["anthropic", "cloudflare"], help="welcher Schlüssel gespeichert wird")
    s.add_argument("--slug", required=True, help="der Build-Ordner unter output/")
    s = sub.add_parser("setup", help="den Worker anlegen, füllen, ausliefern und mit einer Testanfrage prüfen")
    s.add_argument("--slug", required=True, help="der Build-Ordner unter output/")
    s.add_argument("--review-to", required=True, help="die E-Mail-Adresse, an die die Prüf-E-Mails gehen")
    s.add_argument("--name", help="Name des Workers (Vorgabe: <slug>-mail)")
    s.add_argument("--account-id", help="Kennung des Cloudflare-Kontos, wenn mehrere erreichbar sind")
    s.add_argument("--forward-to", help="wahlweise: Adresse, an die eingehende Post zusätzlich weitergeleitet wird")
    a = ap.parse_args()
    {"keys": cmd_keys, "save-key": cmd_save_key, "check": cmd_check, "setup": cmd_setup, "deploy": cmd_deploy, "wire-form": cmd_wire_form}[a.cmd](a)


if __name__ == "__main__":
    main()
