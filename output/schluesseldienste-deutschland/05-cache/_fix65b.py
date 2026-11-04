import json
p='city-copy/batch-65.json'
d=json.load(open(p))
s=json.dumps(d,ensure_ascii=False)
s=s.replace("Safekey 24 Schlüsseldienst öffnet","Safekey 24 öffnet").replace("Safekey 24 Schlüsseldienst nennt","Safekey 24 nennt")
d=json.loads(s)
h=d['schleswig-holstein/handewitt']['intro']
h[-1]+=" Das gilt in einem kleinen Ort wie Handewitt besonders, weil die Wege nach Flensburg kurz sind und mancher Betrieb von dort kommt."
m=d['thueringen/hermsdorf']['intro']
m[1]+=" Kleine Ortsbetriebe wie dieser leben von Stammkundschaft und gutem Ruf."
d['nordrhein-westfalen/hilden']={
"intro":[
"Schlüsseldienste in Hilden sind ein Markt mit klarer Arbeitsteilung: ein Betrieb für Autoschlüssel, ein Sicherheitsfachbetrieb mit Ladengeschäft und ein Schuh- und Schlüsseldienst für den Alltag. Die Stadt liegt unmittelbar bei Düsseldorf, und wer hier einen Schlüsseldienst sucht, sollte zuerst klären, welche Art von Hilfe er braucht, denn die drei Betriebe decken sehr verschiedene Aufgaben ab.",
"Der Autoschlüssel Service Hilden kopiert, repariert, programmiert und codiert Fahrzeugschlüssel für etwa 60 Automarken, mit und ohne Fernbedienung, und hilft auch bei verlorenen oder beschädigten Exemplaren. Ein funktionsfähiger Ersatzschlüssel ist in den meisten Fällen innerhalb eines Tages fertig. Mit der mit Abstand größten Bewertungsbasis auf dieser Seite und einem durchweg sehr guten Urteil ist er der am breitesten abgesicherte Betrieb am Ort. Für eine zugefallene Wohnungstür ist er allerdings nicht gedacht, sein Schwerpunkt ist das Fahrzeug.",
"Das Sicherheits-Centrum Riebe ist seit mehr als 30 Jahren in Hilden vertreten und berät zu Sicherheitstechnik für Privathaushalte, Betriebe und Mietwohnungen. Inhaber ist Kurt Riebe, die Kundschaft kommt aus dem ganzen Rheinland. Zum Angebot gehören Türöffnungen, bei denen eine zugefallene Tür in den meisten Fällen zerstörungsfrei aufgeht und die telefonisch zu den regulären Öffnungszeiten laufen. Dazu kommen Schlossaustausch, Schließanlagen, Einbruchschutz, elektronische Schließsysteme und die Betreuung von Gewerbe und Objekten. Wer eine Tür nachrüsten oder eine Schließanlage planen will, ist hier an der richtigen Stelle; als Nachtnotdienst ist der Betrieb nicht ausgewiesen.",
"Der Schuh- und Schlüsseldienst Isik verbindet Schuhreparatur mit Schlüsselarbeiten. Er fertigt Haus-, Auto- und Sicherheitsschlüssel an, macht Nachschlüssel aller Art und führt Notöffnungen von Türen aus. Dazu kommen Schlösser, Zylinder und Sicherheitsberatung. Seine Bewertungsgrundlage ist schmal, das Bestnoten-Urteil sollte deshalb mit einem Anruf ergänzt werden.",
"Als Arbeitsgebiet nennen die Betriebe vor allem Düsseldorf, daneben Solingen, Duisburg, Dortmund und Essen. Wer in Hilden niemanden erreicht, findet im Verzeichnis eigene Seiten für Solingen, Mettmann, Dormagen, Monheim am Rhein und Düsseldorf. Bei einer Notöffnung lassen Sie sich den Gesamtpreis inklusive Anfahrt vorab nennen, bevor jemand losfährt."],
"faqs":[
{"q":"Wer in Hilden hilft bei verlorenen Autoschlüsseln?","a":"Der Autoschlüssel Service Hilden kopiert, repariert, programmiert und codiert Fahrzeugschlüssel für etwa 60 Automarken, mit und ohne Fernbedienung. Ein Ersatzschlüssel ist in den meisten Fällen innerhalb eines Tages fertig."},
{"q":"Wo bekomme ich in Hilden eine Schließanlage oder elektronische Schließsysteme?","a":"Das Sicherheits-Centrum Riebe nennt Schließanlagen, Einbruchschutz und elektronische Schließsysteme, dazu Schlossaustausch und die Betreuung von Gewerbe und Objekten. Es hat ein Ladengeschäft."},
{"q":"Wer öffnet in Hilden eine zugefallene Tür?","a":"Das Sicherheits-Centrum Riebe führt Türöffnungen aus, bei denen die Tür in den meisten Fällen zerstörungsfrei aufgeht; sie laufen telefonisch zu den regulären Öffnungszeiten. Auch der Schuh- und Schlüsseldienst Isik gibt Notöffnungen von Türen an."},
{"q":"Welche Nachbarstädte haben eine eigene Seite?","a":"Solingen, Mettmann, Dormagen, Monheim am Rhein und Düsseldorf haben jeweils eine eigene Seite im Verzeichnis. Dort finden Sie weitere Betriebe, wenn in Hilden niemand passt."}]}
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
