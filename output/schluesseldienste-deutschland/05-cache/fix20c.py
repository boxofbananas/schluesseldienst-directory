import json
p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-20.json'
d=json.load(open(p))
def rep(k,a,b):
    L=d[k]['intro']
    for i,t in enumerate(L):
        if a in t: L[i]=t.replace(a,b); return
    raise SystemExit('nicht gefunden '+a)
rep('nordrhein-westfalen/recklinghausen','Das Profil dieses Betriebs liegt damit eher bei Objekten als bei der Notöffnung an der Haustür.','Das Profil dieses Betriebs liegt damit eher bei Objekten als bei der Notöffnung an der Haustür, sodass Privatleute mit einer Aussperrung hier meist nicht zuerst anrufen.')
rep('nordrhein-westfalen/schloss-holte-stukenbrock','Wer einen Schlüssel braucht, geht deshalb eher in einen Laden als zu einem Notdienst-Fahrzeug.','Wer einen Schlüssel braucht, geht deshalb eher in einen Laden als zu einem Notdienst-Fahrzeug, und wer nachts vor verschlossener Tür steht, klärt vorab, ob der Betrieb überhaupt Türen öffnet.')
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
