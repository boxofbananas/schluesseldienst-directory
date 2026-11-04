f='output/schluesseldienste-deutschland/05-cache/city-copy/batch-114.json'
s=open(f,encoding='utf-8').read()
R=[
("Bewertet ist er mit 4,0 bei 4 abgegebenen Stimmen, eine kleine Grundlage.","Bewertet ist er nur von wenigen Kunden, eine kleine Grundlage."),
("Mit 4,8 aus 5 Stimmen steht er gut da.","Mit seinen wenigen Stimmen steht er gut da."),
("und eine makellose 5,0 aus 5 Stimmen hat.","und durchweg beste Bewertungen hat, wenn auch von wenigen Stimmen."),
("mit 4,6 aus 28 Bewertungen.","mit solide guten Bewertungen."),
("Sie hat 5,0 aus 5 Bewertungen.","Sie hat durchweg beste Bewertungen, allerdings von wenigen Stimmen."),
("stellt die meisten Stimmen der Stadt: 4,9 aus 762 Bewertungen.","stellt die meisten Stimmen der Stadt und wird durchweg stark bewertet."),
("Wer hier zuletzt war, gab 4,7 bei 36 Stimmen.","Wer hier zuletzt war, bewertete ihn überwiegend gut."),
("Mit 5,0 aus nur 5 Stimmen ist die Grundlage klein.","Mit nur wenigen Stimmen ist die Grundlage klein."),
("Der Autoschlüssel Service hat 4,9 aus 762 Bewertungen.","Der Autoschlüssel Service hat die breiteste Bewertungsbasis und durchweg starke Bewertungen."),
("Von 98 Kunden, die bewertet haben, kommt ein Schnitt von 4,9.","Eine breite Kundenschaft hat bewertet, und das Urteil fällt durchweg stark aus."),
("18 Bewertungen ergeben einen Schnitt von 4,9.","Die Bewertungen fallen durchweg stark aus, bei überschaubarer Zahl."),
("Die Bewertung liegt bei 4,9 aus 98.","Die Bewertung ist durchweg stark bei breiter Grundlage."),
("46 Kunden haben ihn bewertet, Schnitt 4,9.","Viele Kunden haben ihn bewertet, und das Urteil fällt durchweg stark aus."),
("Die 39 Bewertungen liegen im Schnitt bei 4,6.","Die Bewertungen liegen im guten Bereich, ohne ganz an die Spitze zu reichen."),
("Acht Bewertungen ergeben einen Schnitt von 5,0, das ist eine kleine Grundlage, aber ausschließlich gute Stimmen.","Die wenigen Bewertungen sind eine kleine Grundlage, aber ausschließlich gute Stimmen."),
("hat 5,0 aus 8 Bewertungen.","ist durchweg bestens bewertet, bei kleiner Grundlage."),
("Fünf Bewertungen ergeben 5,0, eine kleine Grundlage, die aber durchweg zufrieden ausfällt.","Die wenigen Bewertungen sind eine kleine Grundlage, fallen aber durchweg zufrieden aus."),
("61 Kunden haben bewertet, ihr Schnitt liegt bei 4,9.","Viele Kunden haben bewertet, und ihr Urteil fällt durchweg stark aus."),
("72 Bewertungen ergeben einen Schnitt von 4,9, das ist für einen einzelnen Betrieb eine breite Grundlage.","Die Bewertungen fallen durchweg stark aus, und das ist für einen einzelnen Betrieb eine breite Grundlage."),
("hat 4,9 aus 72 Bewertungen.","ist durchweg stark bewertet, bei breiter Grundlage."),
]
for a,b in R:
    if a not in s: print("MISSING",a)
    s=s.replace(a,b)
open(f,'w',encoding='utf-8').write(s)
