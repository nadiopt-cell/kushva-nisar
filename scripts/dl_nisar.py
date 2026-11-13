import requests, json, time, sys, re
from pathlib import Path
ROOT=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=Path(r"E:\ai_project\30days_challenge\day14_borges\earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(ROOT/"asf_kushva.json",encoding="utf-8-sig"))
want=["20260620","20260702"]
urls={}
for e in js[0]:
    if e.get("processingLevel")=="GCOV":
        d=e["startTime"][:10].replace("-","")
        if d in want: urls[d]=e["downloadUrl"]
out=ROOT/"data"/"nisar"; out.mkdir(parents=True,exist_ok=True)
CH=64*1024*1024
for d in want:
    url=urls[d]; fn=out/url.split("/")[-1]
    if fn.exists() and fn.stat().st_size==0: fn.unlink()
    h={"Authorization":f"Bearer {tok}","Range":"bytes=0-0"}
    r=requests.get(url,headers=h,timeout=120)
    cr=r.headers.get("Content-Range") or ""
    total=int(cr.split("/")[-1]) if "/" in cr else int(r.headers.get("Content-Length",0))
    pos=fn.stat().st_size if fn.exists() else 0
    print("start",fn.name,pos,total,flush=True)
    t0=time.time()
    with open(fn,"ab" if pos else "wb") as f:
        while pos<total:
            end=min(pos+CH,total)-1
            for attempt in range(8):
                try:
                    rr=requests.get(url,headers={"Authorization":f"Bearer {tok}","Range":f"bytes={pos}-{end}"},timeout=(30,600))
                    if rr.status_code==206 or rr.status_code==200:
                        f.write(rr.content); f.flush()
                        if rr.status_code==200 and pos>0:
                            print("server ignored range!",flush=True); sys.exit(1)
                        pos+=len(rr.content)
                        print(f"{d} {pos/1e9:.2f}/{total/1e9:.2f} GB {pos/1e6/max(time.time()-t0,1):.1f} MB/s",flush=True)
                        break
                    print("status",rr.status_code,flush=True); time.sleep(5)
                except Exception as ex:
                    print("retry",attempt,type(ex).__name__,str(ex)[:100],flush=True); time.sleep(5)
            else:
                print("FAILED",pos,flush=True); sys.exit(1)
    print("done",fn,fn.stat().st_size,flush=True)