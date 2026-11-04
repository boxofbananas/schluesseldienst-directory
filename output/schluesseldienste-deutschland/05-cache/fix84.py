import json
p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-84.json'
d=json.load(open(p))
R=[("Gut 20 Kunden haben ihn bewertet, der Schnitt beträgt 4,4.","Seine Kunden bewerten ihn solide, wenn auch nicht so glänzend wie den größeren Laden."),
("Die Bewertungsbasis ist breit und fällt durchweg stark aus.","Rapid hat unter den Betrieben der Stadt die größte Zahl an Rückmeldungen, und sie sind überwiegend stark."),
("31 Bewertungen ergeben einen Schnitt von 3,3.","Die Bewertungen fallen verhalten aus, bei einer spürbaren Zahl an Stimmen."),
("8 Kunden haben bisher bewertet, der Schnitt liegt bei 4,5.","bisher haben erst wenige Kunden bewertet, das Urteil fällt gut aus."),
("8 Bewertungen führen zu 4,5.","Das Urteil fällt gut aus, stützt sich aber nur auf wenige Stimmen."),
("13 Kunden haben ihn bewertet, der Schnitt beträgt 3,5.","Die Kundenurteile über ihn gehen auseinander und liegen im Mittel nur im Mittelfeld."),
("Hier stehen 4,6 aus nur 8 Bewertungen; eine so kleine Zahl verschiebt sich mit jeder neuen Stimme.","Das gute Urteil beruht hier auf nur wenigen Bewertungen; eine so kleine Zahl verschiebt sich mit jeder neuen Stimme."),
("12 Bewertungen ergeben 4,7.","Eine Handvoll Kunden hat ihn bisher sehr gut bewertet."),
("Hier stehen 16 Bewertungen mit einem Schnitt von 4,4.","Die Kundenurteile fallen hier gut aus, bei überschaubar vielen Stimmen.")]
n=0
def w(x):
    global n
    if isinstance(x,str):
        for a,b in R:
            if a in x:
                x=x.replace(a,b); n+=1
        return x
    if isinstance(x,list): return [w(i) for i in x]
    if isinstance(x,dict): return dict((k,w(v)) for k,v in x.items())
    return x
d=w(d)
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
print(n)
