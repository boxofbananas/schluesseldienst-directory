import json,re
p='output/schluesseldienste-deutschland/05-cache/city-copy/batch-20.json'
d=json.load(open(p))
def lv(x,n):
    x=float(x.replace(',','.'));n=int(n)
    if n<15: return 'few'
    if x>=4.8: return 'a'
    if x>=4.5: return 'b'
    if x>=4.0: return 'c'
    return 'd'
ADJ=dict(a='durchweg stark',b='gut',c='ordentlich',d='verhalten')
ADJE=dict(a='durchweg starker',b='guter',c='ordentlicher',d='verhaltener')
def verb(m):
    l=lv(m.group(1),m.group(2))
    if l=='few': return 'ist nur dünn bewertet, deshalb wenig aussagekräftig'
    return 'ist '+ADJ[l]+' bewertet'
def mit(m):
    l=lv(m.group(1),m.group(2))
    if l=='few': return 'mit nur wenigen Stimmen'
    return 'mit '+ADJE[l]+' Bewertung'
def kom(m):
    l=lv(m.group(1),m.group(2))
    if l=='few': return ', nur dünn bewertet'
    return ', '+ADJ[l]+' bewertet'
def s(t):
    t=t.replace('Aus 47 Bewertungen ergibt sich eine 5,0.','Die Bewertung fällt durchweg stark aus.')
    t=t.replace('Die 93 Bewertungen ergeben eine glatte 5,0.','Ausreißer nach unten gibt es in der Bewertung nicht.')
    t=t.replace('hat 4,8 aus 138 Bewertungen und ist damit','ist durchweg stark bewertet und damit')
    t=re.sub(r'mit (\d,\d) aus (\d+) Bewertungen',mit,t)
    t=re.sub(r'(?:hat|kommt auf) (\d,\d) aus (\d+) Bewertungen',verb,t)
    t=re.sub(r', (\d,\d) aus (\d+) Bewertungen',kom,t)
    return t
def w(o):
    if isinstance(o,str): return s(o)
    if isinstance(o,list): return [w(i) for i in o]
    if isinstance(o,dict): return dict((k,w(v)) for k,v in o.items())
    return o
d=w(d)
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
