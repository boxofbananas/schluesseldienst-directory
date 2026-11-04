p="output/schluesseldienste-deutschland/05-cache/city-copy/batch-71.json"
s=open(p,encoding="utf-8").read()
R=[
("Die Kunden, die ihn bewertet haben, geben ihm 5,0, bei 58 Stimmen.","Die Kunden, die ihn bewertet haben, geben ihm durchweg Bestnoten, und das bei einer breiten Bewertungsbasis."),
("Eisleben Bahnhof erreicht 3,9 aus 11 Bewertungen. Die Bauschlosserei Jockschies GmbH hat eine einzige Bewertung, und die lautet 5,0. Eine 5,0 aus einer Stimme ist etwas anderes als eine 5,0 aus 58, und das lohnt sich beim Vergleich im Blick zu behalten.","Eisleben Bahnhof liegt im Mittelfeld der Bewertungen. Die Bauschlosserei Jockschies GmbH hat eine einzige Bewertung, und die fällt bestens aus. Eine Bestnote aus einer Stimme ist etwas anderes als eine aus vielen, und das lohnt sich beim Vergleich im Blick zu behalten."),
(" 21 Kunden haben ihn bewertet, mit einem Schnitt von 4,8."," Seine Kunden bewerten ihn durchweg stark."),
("Lotto und Zeitschriften Müller, das 4,3 aus 16 Bewertungen erreicht.","Lotto und Zeitschriften Müller, das solide bewertet ist."),
("nicht dasselbe wie 4,8 aus 21.","nicht dasselbe wie die vielen guten Stimmen für Hinreiner-Sicherheitstechnik."),
("Die Günter Meinhardt Schlosserei trägt 5,0 aus einer einzigen Bewertung.","Die Günter Meinhardt Schlosserei trägt eine einzige Bestbewertung."),
("Gewertet wird er mit 4,8 aus 21 Bewertungen.","Seine Kunden bewerten ihn durchweg stark."),
("Der Laden steht bei 4,3 aus 16 Bewertungen.","Die Bewertungen fallen solide aus."),
("Sie hat 5,0 aus einer Bewertung, was eine sehr kleine Grundlage ist.","Sie hat nur eine einzige Bewertung, was eine sehr kleine Grundlage ist."),
(" 36 Kunden haben ihn bewertet, das ergibt 4,8."," Seine Kunden bewerten ihn durchweg stark."),
("und liegt bei 3,7 aus 9 Bewertungen. Schließanlagen Gröger hat noch keine Bewertung. 0,0 aus 0 Bewertungen heißt hier, dass bisher niemand eine abgegeben hat, nicht dass der Betrieb schlecht abgeschnitten hätte.","und hat nur wenige, eher gemischte Bewertungen. Schließanlagen Gröger hat noch keine Bewertung, das heißt hier nur, dass bisher niemand eine abgegeben hat, nicht dass der Betrieb schlecht abgeschnitten hätte."),
("Bewertet wurde er 36 Mal.","Seine Bewertungsbasis ist breit."),
("und steht bei 3,7 aus 9 Bewertungen. Der Ort","und hat nur wenige Bewertungen. Der Ort"),
(" Bei 187 Bewertungen steht ein Schnitt von 4,9."," Sie hat die größte Bewertungsbasis am Ort und wird durchweg stark bewertet."),
(" 26 Bewertungen ergeben bei ihm 4,7."," Seine Bewertungen fallen durchweg gut aus."),
("mit 5,0 aus 2 Bewertungen. Zwei Stimmen sind","mit nur zwei Bewertungen. Zwei Stimmen sind"),
("und hat 5,0 aus 2 Bewertungen. Die Zahl","und hat nur zwei Bewertungen. Die Zahl"),
(" Von 54 Kunden bewertet, kommt er auf 4,8."," Seine Kunden bewerten ihn durchweg stark."),
("bewertet mit 4,6 aus 36 Stimmen.","gut bewertet."),
("steht bei 5,0 aus 4 Bewertungen.","hat nur vier Bewertungen."),
(" Ihre 20 Bewertungen ergeben 4,8."," Ihre Bewertungen fallen durchweg gut aus."),
(" 5,0 aus 17 Bewertungen steht bei ihm."," Die Bewertungen fallen durchweg bestens aus."),
("mit 5,0 aus einer Bewertung. Der Betrieb betreut","mit einer einzigen Bewertung. Der Betrieb betreut"),
("und steht bei 5,0 aus 17 Bewertungen.","und wird durchweg bestens bewertet."),
("und hat 5,0 aus einer Bewertung. Es betreut","und hat nur eine einzige Bewertung. Es betreut"),
(" Seine 72 Bewertungen ergeben 4,7."," Seine Kunden bewerten ihn durchweg gut."),
(" Bewertet wurde er 38 Mal, durchweg mit 5,0."," Er wird von seinen Kunden durchweg bestens bewertet."),
(" Die Wertung lautet 4,6 aus 41 Bewertungen."," Die Bewertungsbasis ist solide und fällt gut aus."),
]
for a,b in R:
    if s.count(a)!=1: print("MISS",s.count(a),a[:50])
    s=s.replace(a,b)
open(p,"w",encoding="utf-8").write(s)
