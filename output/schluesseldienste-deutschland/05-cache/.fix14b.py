import json
p='city-copy/batch-14.json'
d=json.load(open(p))
i=d['schleswig-holstein/elmshorn']['intro']
old="In Elmshorn greifen Schuhmacherei, Sicherheitstechnik und Notdienst ineinander, und wer einen Schlüsseldienst sucht,"
assert i[0].startswith(old)
i[0]=i[0].replace(old,"Schlüsseldienste in Elmshorn sind ein Zusammenspiel aus Schuhmacherei, Sicherheitstechnik und Notdienst, und wer einen sucht,",1)
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
