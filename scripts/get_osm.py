import requests
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
Q="""[out:json][timeout:120];
(
  way["highway"~"^(motorway|trunk|primary|secondary|tertiary)$"](58.10,59.35,58.70,60.20);
  way["natural"="water"](58.10,59.35,58.70,60.20);
  node["place"~"^(city|town|village|hamlet)$"](58.10,59.35,58.70,60.20);
);
out body; >; out skel qt;"""
for url in ["https://overpass.kumi.systems/api/interpreter","https://overpass-api.de/api/interpreter"]:
    try:
        r=requests.post(url,data=Q.encode("utf-8"),headers={"User-Agent":"30DayMapChallenge/1.0 (map art)","Content-Type":"text/plain"},timeout=180)
        print(url,r.status_code,len(r.content))
        if r.status_code==200:
            (R/"data/osm_kushva.json").write_bytes(r.content); print("OK"); break
        print(r.text[:200])
    except Exception as e: print("ERR",e)