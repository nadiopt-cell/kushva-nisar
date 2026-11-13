import requests, json
from shapely.geometry import shape, box
bbox=[59.55,58.15,60.10,58.65]
AOI=box(*bbox)
S=requests.Session()
def q(dt,maxcloud=80):
    body={"collections":["sentinel-2-l2a"],"bbox":bbox,"datetime":dt,"limit":100,
          "query":{"eo:cloud_cover":{"lt":maxcloud}}}
    r=S.post("https://earth-search.aws.element84.com/v1/search",json=body,timeout=90)
    if r.status_code!=200: print(r.text[:500]); r.raise_for_status()
    return r.json()["features"]
for name,dt in [("pre","2026-05-25T00:00:00Z/2026-06-23T00:00:00Z"),("post","2026-06-23T00:00:00Z/2026-08-31T23:59:59Z")]:
    fs=q(dt)
    print("=====",name,len(fs))
    rows=[]
    for f in fs:
        g=shape(f["geometry"]); inter=g.intersection(AOI).area/AOI.area
        p=f["properties"]
        rows.append((p["datetime"][:10],p.get("eo:cloud_cover"),round(inter*100),f["id"]))
    for r in sorted(rows): print(r)