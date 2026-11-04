import json
p='city-copy/batch-12.json'
d=json.load(open(p,encoding='utf-8'))
def sub(k,a,b):
    t=d[k]['intro']
    for i,x in enumerate(t):
        if a in x:
            t[i]=x.replace(a,b);return
    raise SystemExit(a)
sub('niedersachsen/osnabrueck',"In Osnabrück trifft ein klassischer Notdienst auf","Die Schlüsseldienste in Osnabrück sind vielfältig: Hier trifft ein klassischer Notdienst auf")
sub('niedersachsen/osnabrueck',"Wer einen Schlüsseldienst in Osnabrück sucht, findet beides:","Wer sich in der Stadt umsieht, findet beides:")
sub('niedersachsen/osnabrueck',"Dazu kommen Schlüsselkopien für Haus, Briefkasten und Spezialschlüssel.","Dazu kommen Schlüsselkopien für Haus, Briefkasten und Spezialschlüssel sowie Ersatz- und Funkschlüssel.")
sub('niedersachsen/osnabrueck',"Sie helfen, wenn Sie am Rand von Osnabrück","Sie helfen Ihnen weiter, wenn Sie am Rand von Osnabrück")
sub('baden-wuerttemberg/nuertingen',"Wer bei ihm anfragt, bekommt also Beratung","Wer bei diesem Betrieb anfragt, bekommt also Beratung")
sub('baden-wuerttemberg/nuertingen',"Für Nürtingen selbst lohnt sich die Frage,","Für Nürtingen selbst lohnt sich vor jedem Anruf die Frage,")
sub('baden-wuerttemberg/nuertingen',"sind hilfreich, wenn Sie nördlich oder östlich von Nürtingen wohnen.","sind hilfreich, wenn Sie nördlich oder östlich von Nürtingen wohnen und einen Betrieb in der Nähe suchen.")
sub('hessen/offenbach',"Das ist hilfreich, wenn Sie am Stadtrand von Offenbach wohnen und der nächste","Das ist besonders hilfreich, wenn Sie am Stadtrand von Offenbach wohnen und der nächste")
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
