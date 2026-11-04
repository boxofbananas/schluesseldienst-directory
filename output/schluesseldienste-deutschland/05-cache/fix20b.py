import json
p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-20.json'
d=json.load(open(p))
def rep(k,a,b):
    L=d[k]['intro']
    for i,t in enumerate(L):
        if a in t: L[i]=t.replace(a,b); return
    raise SystemExit('nicht gefunden '+a)
rep('nordrhein-westfalen/schloss-holte-stukenbrock','Sebastian Küsel aus Augustdorf ist nur dünn bewertet, deshalb wenig aussagekräftig, S. Berenbrinker auf 4,0 aus 4 Bewertungen.','Sebastian Küsel aus Augustdorf ist nur dünn bewertet, deshalb wenig aussagekräftig; bei S. Berenbrinker gilt dasselbe.')
rep('niedersachsen/salzgitter','Zugefallene Türen öffnet der Betrieb beschädigungsfrei.','Zugefallene Türen öffnet der Betrieb ohne Beschädigung des Schlosses.')
rep('nordrhein-westfalen/recklinghausen','Dazu kommen Schließzylinder,','Dazu kommen auch Schließzylinder,')
rep('nordrhein-westfalen/recklinghausen','Der Betrieb macht Schlüssel nach,','Der Betrieb macht im Ladengeschäft Schlüssel nach,')
rep('nordrhein-westfalen/recklinghausen','Autoschlüssel und Tresore gehören ebenfalls zum Angebot.','Autoschlüssel und Tresore gehören ebenfalls zum Angebot, was bei ausgesperrten Autofahrern hilft.')
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
