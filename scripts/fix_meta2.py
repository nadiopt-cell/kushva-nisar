import json
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
b=[[59.449967,58.17988],[60.100257,58.17988],[60.100257,58.600097],[59.449967,58.600097]]
h=[[59.449967,58.17988],[60.100526,58.17988],[60.100526,58.600238],[59.449967,58.600238]]
meta={"rasters":{"s2_pre":b,"s2_post":b,"nisar":b},"aoi":[6617940.0,8005200.0,6690330.0,8094450.0],"hillshade":h}
json.dump(meta,open(R/"meta.json","w"),ensure_ascii=False,indent=1)
p=R/"nisar_comp.jpg"
if p.exists(): p.unlink()
print("meta ok",p.exists())