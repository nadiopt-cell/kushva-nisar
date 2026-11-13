import json
from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data\contour.geojson")
d=json.load(open(p,encoding="utf-8"))
print(d["features"][0]["properties"])
print(len(open(p,encoding="utf-8").read()))