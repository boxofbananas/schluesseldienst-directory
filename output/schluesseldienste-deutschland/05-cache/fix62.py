f='output/schluesseldienste-deutschland/05-cache/city-copy/batch-62.json'
s=open(f,encoding='utf-8').read()
R=[
("Seine Bewertung von 4,0 beruht auf 4 Stimmen und ist deshalb ein schmaler Anhaltspunkt, anders als die 5,0 aus 130 des Autoschlüsseldienstes.","Seine Bewertung beruht auf nur wenigen Stimmen und ist deshalb ein schmaler Anhaltspunkt, anders als die breite Bewertungsbasis des Autoschlüsseldienstes."),
("Ernst Duschinger sitzt in Teublitz und steht mit 5,0 aus 3 Bewertungen auf der Seite.","Ernst Duschinger sitzt in Teublitz und steht mit sehr wenigen Stimmen auf der Seite, weshalb sich daraus kaum etwas ableiten lässt."),
("Die Bewertung ist gut, stützt sich aber auf wenige Stimmen.","Gut bewertet ist dieser Betrieb, doch hinter dem Urteil stehen nur wenige Kunden."),
("Er kommt auf 4,1 aus 9 Bewertungen, ein Wert aus wenigen Stimmen.","Sein Urteil ist ordentlich, ruht aber auf wenigen Stimmen."),
("Schlüsseldienst Gerber in Burgwedel hat 3,2 aus 39 Bewertungen.","Schlüsseldienst Gerber in Burgwedel fällt in den Bewertungen eher mäßig aus."),
("Er kommt auf 4,8 aus 29 Bewertungen.","Auch er wird durchweg sehr gut bewertet."),
("Haus und Schloss Sicherheitstechnik & Einbruchsicherungen hat 5,0 aus 4 Bewertungen und nennt","Haus und Schloss Sicherheitstechnik & Einbruchsicherungen hat nur wenige, dafür sehr gute Bewertungen und nennt"),
("Die konsysta GmbH sitzt in Lich und hat 2,8 aus 4 Bewertungen.","Die konsysta GmbH sitzt in Lich und hat nur wenige, eher schwache Bewertungen."),
("Er hat 5,0 aus 4 Bewertungen.","Hinter seiner Spitzenbewertung stehen nur wenige Stimmen."),
("Sie kommt auf 5,0 aus 30 Bewertungen.","Sie wird von ihren Kunden durchweg bestens bewertet."),
("Der Schlüsseldienst von Peik Rast betreut seit 2002 Kunden in Dessau-Roßlau und Umgebung.","Der Schlüsseldienst von Peik Rast ist seit 2002 in Dessau-Roßlau und Umgebung für seine Kundschaft im Einsatz."),
]
for k,v in R:
    assert k in s,k
    s=s.replace(k,v)
open(f,'w',encoding='utf-8').write(s)
