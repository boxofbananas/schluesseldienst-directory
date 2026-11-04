import json
p='city-copy/batch-22.json'
s=open(p,encoding='utf-8').read()
R=[
("33 Bewertungen ergeben die Bestnote 5,0.","Die Kundenstimmen sind durchweg bestens."),
("Er steht mit 5,0 aus 30 Bewertungen da.","Die Kundenbewertungen fallen durchweg hervorragend aus."),
("(4,9 aus 32 Bewertungen)","(durchweg stark bewertet)"),
("Zwölf Bewertungen ergeben dort eine 5,0.","Die wenigen Stimmen dort sind durchweg bestens."),
("Die Bewertung liegt bei 4,1 aus 10 Bewertungen.","Die Bewertung ist gut, stützt sich aber auf wenige Stimmen."),
("kommt auf 5,0 aus 11 Bewertungen.","wird mit wenigen Stimmen bestens bewertet."),
("Seine Bewertung ist 5,0 aus 49 Bewertungen.","Er wird von seinen Kunden durchweg bestens bewertet."),
("Die Bewertung von 4,8 beruht auf 28 Stimmen.","Die Bewertung ist durchweg stark."),
("(5,0 aus 18 Bewertungen)","(bestens bewertet)"),
("(5,0 aus 2 Bewertungen)","(bestens bewertet, aber mit sehr wenigen Stimmen)"),
("Die Bewertung liegt bei 3,8 aus 21 Bewertungen.","Die Bewertung fällt eher mittelmäßig aus."),
("Andreas Essendorfer hat 4,8 aus 4 Bewertungen.","Andreas Essendorfer ist gut bewertet, allerdings mit wenigen Stimmen."),
("(4,0 aus 28 Bewertungen)","(ordentlich bewertet)"),
("Die 4,0 beruht auf 28 Bewertungen, die Zahl reicht für ein erstes Bild, wie die Kunden den Laden erleben.","Die Bewertungsbasis reicht für ein erstes Bild, wie die Kunden den Laden erleben."),
("(4,5 aus 31 Bewertungen)","(gut bewertet)"),
("(5,0 aus 13 Bewertungen)","(bestens bewertet)"),
("deren Bewertung bei 5,0 aus 1 Bewertung liegt","die nur eine einzige Bewertung trägt"),
("Er kommt auf 4,6 aus 66 Bewertungen.","Er ist gut bewertet."),
("Die Bewertung liegt bei 4,7 aus 23 Bewertungen.","Die Bewertung ist gut."),
("Er hat 5,0 aus 28 Bewertungen und die meisten Bewertungen auf dieser Seite.","Er ist bestens bewertet und hat die meisten Bewertungen auf dieser Seite."),
("(3,5 aus 8 Bewertungen)","(mäßig bewertet)"),
("Die Note von 3,5 stützt sich auf acht Bewertungen, ein kleines Bild.","Die Note stützt sich auf wenige Stimmen, ein kleines Bild."),
("(5,0 aus 16 Bewertungen)","(bestens bewertet)"),
("(4,4 aus 7 Bewertungen)","(gut bewertet, aber mit wenigen Stimmen)"),
("Mit 5,0 aus 73 Bewertungen ist das eine Bestnote, die über viele","Das ist eine Bestnote, die über viele"),
("Auch er erreicht eine 5,0, bei 21 Bewertungen.","Auch er wird bestens bewertet."),
("(4,9 aus 20 Bewertungen)","(durchweg stark bewertet)"),
("(3,5 aus 42 Bewertungen)","(mäßig bewertet)"),
("Die Note von 3,5 stützt sich auf 42 Bewertungen, nicht auf eine Handvoll.","Die Note stützt sich auf viele Stimmen, nicht auf eine Handvoll."),
("(4,4 aus 12 Bewertungen)","(gut bewertet)"),
("kommt dort auf 4,9 aus 16 Bewertungen.","wird dort durchweg stark bewertet."),
]
for a,b in R:
    if a not in s: print('MISSING',a)
    s=s.replace(a,b)
json.loads(s)
open(p,'w',encoding='utf-8').write(s)
