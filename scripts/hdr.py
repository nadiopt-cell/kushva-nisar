import requests,json
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=(R/"earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(R/"asf_kushva.json",encoding="utf-8-sig"))
url=[e["downloadUrl"] for e in js[0] if e.get("processingLevel")=="GUNW" and e["startTime"][:10]=="2026-06-20"][0]
r=requests.get(url,headers={"Authorization":f"Bearer {tok}","Range":"bytes=0-1023"},timeout=60)
print(r.status_code, r.headers)