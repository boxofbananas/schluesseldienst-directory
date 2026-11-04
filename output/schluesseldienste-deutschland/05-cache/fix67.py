import json
f='output/schluesseldienste-deutschland/05-cache/city-copy/batch-67.json'
d=json.load(open(f))
R=[
("Seine Note von 5,0 beruht auf 7 Bewertungen.","Seine Bestnote beruht auf einer eher kleinen Zahl an Stimmen."),
("Die Bestnote dort stützt sich nur auf wenige Stimmen aus der Kundschaft, das ist","Die Bestnote dort stützt sich nur auf wenige Stimmen aus der Kundschaft, das ist aber immerhin ein positives Zeichen und"),
]
def fix(o):
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    if isinstance(o,list): return [fix(v) for v in o]
    if isinstance(o,str):
        for k,v in R: o=o.replace(k,v)
    return o
json.dump(fix(d),open(f,'w'),ensure_ascii=False,indent=2)
