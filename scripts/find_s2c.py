import requests
from shapely.geometry import shape, box
bbox=[59.55,58.15,60.10,58.65]; AOI=box(*bbox)
for dt in ["2026-05-21","2026-07-20","2026-07-28","2026-06-17"]:
    body={"collections":["sentinel-2-l2a"],"bbox":bbox,"datetime":dt+"T00:00:00Z/"+dt+"T23:59:59Z","limit":50}
    r=requests.post("https://earth-search.aws.element84.com/v1/search",json=body,timeout=90)
    fs=r.json()["features"]
    print("==",dt,len(fs))
    for f in fs:
        g=shape(f["geometry"]); inter=g.intersection(AOI).area/AOI.area
        p=f["properties"]
        print(f["id"], round(p.get("eo:cloud_cover",-1),1), round(inter*100), list(f["assets"].keys())[:20])