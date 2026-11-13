import json
from pyproj import Transformer
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
m=json.load(open(R/"meta.json"))
t=Transformer.from_crs(3857,4326,always_xy=True)
def conv(c):
    return [[round(t.transform(x,y)[0],6),round(t.transform(x,y)[1],6)] for x,y in c]
for k in list(m["rasters"].keys()):
    m["rasters"][k]=conv(m["rasters"][k])
m["hillshade"]=conv(m["hillshade"])
json.dump(m,open(R/"meta.json","w"),ensure_ascii=False,indent=1)
print(json.dumps(m,ensure_ascii=False)[:400])