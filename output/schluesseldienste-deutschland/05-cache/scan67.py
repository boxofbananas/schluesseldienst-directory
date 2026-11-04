import json
d=json.load(open('output/schluesseldienste-deutschland/05-cache/city-copy/batch-67.json'))
print(d['baden-wuerttemberg/kraichtal']['intro'][2]); print()
print(d['bayern/lindau-bodensee']['intro'][2]); print()
print(d['hessen/karben']['intro'][2])
