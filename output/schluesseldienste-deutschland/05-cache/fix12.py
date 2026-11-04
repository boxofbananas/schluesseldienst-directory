import json
p='city-copy/batch-12.json'
s=open(p,encoding='utf-8').read()
R=[
("Seine Bewertung liegt bei 4,5 aus 8 Bewertungen.","Bewertet haben ihn bisher nur wenige Kunden, die Zahl ist klein."),
("Die Bewertung beträgt 5,0 aus 51 Bewertungen, die höchste Zahl an Stimmen in dieser Stadt.","Er hat die meisten Stimmen unter den Betrieben dieser Stadt und wird durchweg sehr gut bewertet."),
("Karl-Heinz Bruckmaier ist mit 5,0 aus 3 Bewertungen ebenfalls in Moosburg zu finden.","Karl-Heinz Bruckmaier ist ebenfalls in Moosburg zu finden, mit nur wenigen Stimmen und deshalb wenig aussagekräftig."),
(", bewertet mit 5,0 aus 8 Bewertungen.",", mit nur wenigen Bewertungen, aber durchweg guten."),
("Ihre Bewertung: 5,0 aus 29 Bewertungen.","Sie wird von ihren Kunden durchweg sehr gut bewertet."),
("Die Bewertung liegt bei 4,2 aus 21 Bewertungen.","Die Kunden bewerten den Betrieb überwiegend gut."),
("ist mit 5,0 aus 923 Bewertungen der Betrieb mit der größten Bewertungsgeschichte der Stadt.","hat die größte Bewertungsgeschichte der Stadt und wird durchweg sehr gut bewertet."),
("Die Bewertung liegt bei 5,0 aus 137 Bewertungen, auch Elvin nennt Festpreise.","Er wird durchweg stark bewertet, und auch Elvin nennt Festpreise."),
("und kommt auf 4,9 aus 72 Bewertungen.","und wird von seinen Kunden sehr gut bewertet."),
("und liegt bei 5,0 aus 52 Bewertungen.","und ist durchweg stark bewertet."),
("und bringt es auf 5,0 aus 27 Bewertungen.","und wird ebenfalls durchweg stark bewertet."),
("und kommt auf 5,0 aus 2 Bewertungen.","und hat bisher nur wenige Bewertungen, die wenig aussagen."),
("und steht bei 5,0 aus 16 Bewertungen.","und wird sehr gut bewertet."),
("und wird mit 4,4 aus 17 Bewertungen bewertet.","und wird überwiegend gut bewertet."),
(" (4,3 aus 17 Bewertungen).","; die Bewertungen fallen gut, aber nicht herausragend aus."),
(", 4,2 aus 75 Bewertungen.",", bei überwiegend guten Bewertungen."),
("Auf 158 Bewertungen kommt der Betrieb im Schnitt auf 4,8.","Die Kunden bewerten den Betrieb dennoch durchweg stark."),
("Die Bewertung ist 5,0 aus 31 Bewertungen.","Seine Kunden bewerten ihn durchweg sehr gut."),
("Die Bewertung beträgt 4,9 aus 18 Bewertungen.","Er wird sehr gut bewertet."),
("Seine Bewertung: 4,6 aus 25 Bewertungen.","Seine Kunden bewerten ihn überwiegend gut."),
("steht bei 4,9 aus 29 Bewertungen.","wird ebenfalls sehr gut bewertet."),
("Die Bewertung: 4,7 aus 14 Bewertungen.","Die Kunden bewerten das Geschäft gut."),
("und steht bei 3,2 aus 22 Bewertungen.","und wird mäßig bewertet."),
(" (4,5 aus 24 Bewertungen) und die"," und die"),
(" (4,0 aus 21 Bewertungen) sind"," sind"),
("Er nennt Festpreise und kommt auf 4,9 aus 185 Bewertungen.","Er nennt Festpreise und wird von seinen Kunden durchweg sehr gut bewertet."),
("ist mit 4,9 aus 210 Bewertungen der Betrieb mit den meisten Bewertungen in Offenbach.","hat die meisten Bewertungen in Offenbach und wird sehr gut bewertet."),
("Gemessen wird er an 22 Bewertungen mit durchgehend 5,0.","Seine Kunden bewerten ihn durchgehend sehr gut."),
(" (4,2 aus 5 Bewertungen).","."),
(" (4,5 aus 16 Bewertungen) repariert"," repariert"),
(", mit Schuhreparatur, Uhrenservice und Gravuren (2,3 aus 3 Bewertungen).",", mit Schuhreparatur, Uhrenservice und Gravuren; es gibt dazu nur wenige Bewertungen."),
(" und bietet einen Notdienst an (2,8 aus 43 Bewertungen)."," und bietet einen Notdienst an; die Bewertungen fallen eher mäßig aus."),
(" (5,0 aus 9 Bewertungen) und HEL Metallbau & Feinwerkmechanik (5,0 aus 1 Bewertung)."," und HEL Metallbau & Feinwerkmechanik."),
]
for a,b in R:
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); json.loads(s)
