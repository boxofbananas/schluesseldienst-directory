import json
p='city-copy/batch-12.json'
d=json.load(open(p,encoding='utf-8'))
t=d['niedersachsen/osnabrueck']['intro']
a="Auch bei einem abgebrochenen Schlüssel rückt er aus."
assert a in t[2]
t[2]=t[2].replace(a,a+" Dazu zählen das Öffnen von Tresoren, der Austausch von Schlössern und der Einbruchschutz für Wohnungen und Häuser, sodass sich der Betrieb nicht auf die reine Türöffnung beschränkt.")
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
