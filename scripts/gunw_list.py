import json
d=json.load(open(r'E:\ai_project\30days_challenge\day14_borges\asf_kushva.json',encoding='utf-8-sig'))
for x in d[0]:
    if x.get('processingLevel')=='GUNW':
        print(x['startTime'][:10], x.get('stopTime','')[:10], x.get('polarization'), x.get('relativeOrbit'), x.get('flightDirection'), x.get('sizeMB'))
        print("   ",x['downloadUrl'])