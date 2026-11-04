import json
p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-113.json'
raw=open(p,encoding='utf-8').read()
R=[
("Dafür stehen 4,9 aus 981 Bewertungen.","Dafür steht eine sehr breite Bewertungsbasis bei durchweg hoher Note."),
("kommt auf 5,0 aus 429 Bewertungen und versorgt","ist mit vielen durchweg starken Bewertungen vertreten und versorgt"),
("hat 4,9 aus 304 Bewertungen und baut","ist durchweg stark bewertet und baut"),
("ohne Spuren und hat 4,9 aus 299 Bewertungen.","ohne Spuren und ist durchweg stark bewertet."),
("und 4,9 aus 153 Bewertungen hat","und durchweg stark bewertet ist"),
("(4,6 aus 88 Bewertungen)","(solide bewertet)"),
("(4,5 aus 72 Bewertungen)","(ordentlich bewertet)"),
("(4,1 aus 50 Bewertungen)","(mit eher gemischten Stimmen)"),
("(5,0 aus 19 Bewertungen)","(Bestnote bei überschaubar vielen Stimmen)"),
("und der Betrieb hat 5,0 aus 36 Bewertungen.","und der Betrieb ist mit Bestnote bei überschaubar vielen Stimmen bewertet."),
("kommt auf 5,0 aus 20 Bewertungen.","hat Bestnote bei wenigen Stimmen."),
("Eine 5,0 aus 20 Bewertungen ist eine andere Aussage als 4,9 aus 981, und das gilt","Eine Bestnote bei wenigen Stimmen ist eine andere Aussage als eine hohe Note bei der größten Bewertungsbasis am Ort, und das gilt"),
("hat 5,0 aus 819 Bewertungen.","hat bei Bestnote mit Abstand die größte Bewertungsbasis."),
("Auf 70 Bewertungen kommt er im Schnitt auf 4,7.","Er ist bei einer ordentlichen Zahl von Stimmen gut bewertet."),
("(5,0 aus 9 Bewertungen)","(Bestnote, aber nur sehr wenige Stimmen)"),
("und hat 3,5 aus 11 Bewertungen.","und ist bei wenigen Stimmen nur mittelmäßig bewertet."),
("Auf 20 Bewertungen kommt der Betrieb auf 5,0.","Der Betrieb hat Bestnote bei überschaubar vielen Stimmen."),
("Eine 5,0 aus 20 Bewertungen und eine 5,0 aus 819 Bewertungen sind nicht dasselbe, und bei 5,0 aus 9 gilt es erst recht.","Eine Bestnote bei überschaubar vielen Stimmen und eine Bestnote bei der größten Bewertungsbasis sind nicht dasselbe, und bei nur sehr wenigen Stimmen gilt es erst recht."),
("Er steht bei 3,9 aus 67 Bewertungen.","Er wird eher durchwachsen bewertet."),
("kommt auf 4,6 aus 30 Bewertungen, der in Belm auf 2,8 aus 52.","wird ordentlich bewertet, der in Belm deutlich schlechter."),
("wobei sich die 3,0 auf nur 2 Bewertungen stützt","wobei sich die Note auf nur sehr wenige Stimmen stützt"),
("und hat 4,9 aus 15 Bewertungen.","und ist bei wenigen Stimmen sehr gut bewertet."),
("Auf 48 Bewertungen kommt er auf 4,9.","Er ist durchweg stark bewertet."),
("(4,5 aus 23 Bewertungen)","(ordentlich bewertet)"),
(", 4,8 steht bei 14 Bewertungen.",", die Note ist gut, die Zahl der Stimmen überschaubar."),
("Er hat 5,0 aus nur 1 Bewertung.","Er hat Bestnote, doch nur von einer einzigen Stimme."),
("seine 5,0 beruht auf 2 Bewertungen","seine Bestnote beruht auf nur zwei Stimmen"),
("(5,0 aus 16 Bewertungen)","(Bestnote bei überschaubar vielen Stimmen)"),
("(5,0 aus 4 Bewertungen)","(Bestnote, aber nur wenige Stimmen)"),
("für ihn stehen 4,7 aus 16 Bewertungen.","für ihn spricht eine gute Note bei überschaubar vielen Stimmen."),
("hat 5,0 aus 136 Bewertungen, das ist mit Abstand die größte Zahl am Ort,","hat bei Bestnote mit Abstand die größte Bewertungsbasis am Ort,"),
("und hat 4,8 aus 16 Bewertungen.","und ist gut bewertet."),
("(4,6 aus 25 Bewertungen)","(ordentlich bewertet)"),
("und hat 4,6 aus 62 Bewertungen.","und wird ordentlich bewertet."),
("(5,0 aus 2 Bewertungen)","(Bestnote, aber nur sehr wenige Stimmen)"),
("und hat 5,0 aus 23 Bewertungen.","und hat Bestnote bei überschaubar vielen Stimmen."),
("Der Betrieb hat 5,0 aus 136 Bewertungen und nennt","Der Betrieb hat die größte Bewertungsbasis und nennt"),
("Sie hat 5,0 aus 55 Bewertungen.","Sie ist durchweg stark bewertet."),
("Hier stehen 4,9 aus 9 Bewertungen.","Hier stehen sehr gute Noten, aber nur wenige Stimmen."),
("mit 4,8 aus 19 Bewertungen.","bei guter Bewertung."),
("dazu 5,0 aus 11 Bewertungen.","dazu Bestnote bei überschaubar vielen Stimmen."),
]
for a,b in R:
    if raw.count(a)==0: print("FEHLT",a)
    raw=raw.replace(a,b)
json.loads(raw)
open(p,'w',encoding='utf-8').write(raw)
