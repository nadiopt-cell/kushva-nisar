import requests,time,json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=(R/"earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(R/"asf_kushva.json",encoding="utf-8-sig"))
url=[e["downloadUrl"] for e in js[0] if e.get("processingLevel")=="GUNW" and e["startTime"][:10]=="2026-06-20"][0]
def get(i):
    st=i*32*1024*1024; en=st+16*1024*1024-1
    t=time.time(); r=requests.get(url,headers={"Authorization":f"Bearer {tok}","Range":f"bytes={st}-{en}"},timeout=120)
    return r.status_code,len(r.content)/1e6/(time.time()-t)
with ThreadPoolExecutor(8) as ex:
    res=list(ex.map(get,range(8)))
print(res); print("aggregate",sum(x[1] for x in res))