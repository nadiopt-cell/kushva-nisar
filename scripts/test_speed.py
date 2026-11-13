import requests, json, time
from pathlib import Path
ROOT=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=Path(r"E:\ai_project\NISAR\earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(ROOT/"asf_kushva.json",encoding="utf-8-sig"))
url=None
for e in js[0]:
    if e.get("processingLevel")=="GCOV" and "20260620" in e["startTime"]:
        url=e["downloadUrl"]
print(url)
h={"Authorization":f"Bearer {tok}","Range":"bytes=0-33554431"}
t=time.time(); r=requests.get(url,headers=h,timeout=180)
print(r.status_code, len(r.content)/1e6,"MB", round(time.time()-t,1),"s")
