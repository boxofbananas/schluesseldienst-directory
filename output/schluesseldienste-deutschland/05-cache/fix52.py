p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-52.json'
s=open(p,encoding='utf-8').read()
R=[
("Bewertet wird er mit 4,8 bei 64 Bewertungen.","Die Kundenurteile über ihn fallen durchweg gut aus."),
("Unter dem Strich stehen 4,4 aus 63 Bewertungen.","Die Bewertungen fallen solide aus."),
("Die Kunden vergaben 4,8 Sterne bei 26 Bewertungen.","Die Kunden bewerten den Betrieb durchweg stark."),
("bewertet mit 4,7 bei 24 Bewertungen","gut bewertet"),
("Seine Bewertung beträgt 4,4 aus 63 Bewertungen.","Seine Bewertung fällt solide aus."),
("Die Note 5,0 stützt sich auf 99 Bewertungen und damit auf eine breite Grundlage.","Die Bewertung ist makellos und stützt sich auf eine breite Grundlage."),
("Hier steht eine 5,0 bei 83 Bewertungen.","Auch hier fällt die Bewertung sehr gut aus, bei ordentlicher Stimmenzahl."),
("Mit 5,0 bei nur 8 Bewertungen lohnt der Blick auf die kleine Zahl.","Die Bestnote beruht auf nur wenigen Stimmen und sagt deshalb wenig aus."),
("Der Betrieb hat 5,0 aus 99 Bewertungen.","Er ist durchweg stark bewertet."),
("Mit 4,9 bei 142 Bewertungen liegt er weit vorn.","Mit sehr guter Note und vielen Stimmen liegt er weit vorn."),
("Eine Note von 4,3 steht hier bei 13 Bewertungen.","Die Bewertung ist gut, beruht aber auf wenigen Stimmen."),
("kommt ebenfalls auf 4,3 aus 13 Bewertungen.","wird ähnlich bewertet, ebenfalls von wenigen Stimmen."),
("eine einzige Bewertung, eine 1,0.","eine einzige Bewertung, und die fällt schlecht aus."),
("bei 4,9 aus 142 Bewertungen.","und ist sehr gut bewertet."),
("Er sammelte 4,3 Sterne bei 55 Bewertungen und hat damit die breiteste Grundlage in der Stadt.","Er hat die breiteste Bewertungsgrundlage in der Stadt, mit gutem Urteil."),
("Bewertet ist er mit 4,2 bei 19 Bewertungen.","Die Bewertung fällt gut aus."),
("Klaus Göldner kommt auf 2,9 bei 10 Bewertungen.","Klaus Göldner wird nur mäßig bewertet."),
("ihre Note ist eine 5,0, die auf einer einzigen Bewertung beruht und deshalb wenig aussagt.","ihre Bestnote beruht auf einer einzigen Bewertung und sagt deshalb wenig aus."),
("Der Betrieb hat 4,2 aus 19 Bewertungen.","Kunden bewerten den Betrieb überwiegend gut."),
("Sie hat eine Bewertung von 5,0 aus einer einzigen Bewertung.","Ihre Bestnote beruht auf einer einzigen Bewertung."),
("Er erreicht 5,0 bei 170 Bewertungen, die höchste Zahl am Ort.","Er erreicht die Bestnote und hat die meisten Bewertungen am Ort."),
("Seine Kunden bewerteten ihn mit 4,9 bei 92 Bewertungen.","Seine Kunden bewerteten ihn durchweg sehr gut."),
("Für diesen Betrieb stehen 5,0 aus 34 Stimmen.","Für diesen Betrieb stimmen die Kunden mit Bestnote."),
("Gewertet mit 4,8 bei 31 Bewertungen.","Auch er ist sehr gut gewertet."),
("547 Bewertungen ergeben dort ein Mittel von 4,9.","die zahlreichen Bewertungen ergeben dort ein sehr gutes Mittel."),
("Die Kunden gaben ihm 4,8 bei 49 Bewertungen.","Die Kunden bewerten ihn sehr gut."),
("Sie hat 5,0 aus 10 Bewertungen.","Sie ist sehr gut bewertet, wenn auch von wenigen Stimmen."),
("Er kommt auf 4,6 aus 8 Bewertungen.","Auch hier sind es nur wenige Stimmen, die gut urteilen."),
("Auf 23 Bewertungen kommt ein Schnitt von 4,8.","Die Kunden bewerten ihn sehr gut."),
("Die Note 4,4 beruht auf 21 Bewertungen.","Die Bewertung fällt gut aus."),
("die Bewertung ist 5,0 aus 6 und damit noch dünn belegt","die Bestnote ist noch dünn belegt"),
("er steht bei 4,8 aus 4 Bewertungen","er ist bei nur wenigen Stimmen sehr gut bewertet"),
("und hat 4,8 aus 23 Bewertungen.","und wird sehr gut bewertet."),
]
for a,b in R:
    assert s.count(a)==1,(a,s.count(a))
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
