import json,re
d=json.load(open('output/schluesseldienste-deutschland/05-cache/city-copy/batch-84.json'))
pat=re.compile(r'\d+[,.]?\d*\s*(Bewertung|Kunden|Rezension|Stimmen|km)|Schnitt|\d,\d|aus \d+')
def walk(k,path,x):
    if isinstance(x,str):
        for s in re.split(r'(?<=[.!?])\s+',x):
            if pat.search(s): print(k,path,'|',s)
    elif isinstance(x,list):
        for i,v in enumerate(x): walk(k,path+'/%d'%i,v)
    elif isinstance(x,dict):
        for a,v in x.items(): walk(k,path+'/'+a,v)
for k,v in d.items(): walk(k,'',v)
