import requests, json
bbox=[59.55,58.15,60.10,58.65]
S=requests.Session()
def q(dt,maxcloud=30):
    body={"collections":["sentinel-2-l2a"],"bbox":bbox,"datetime":dt,"limit":100,
          "query":{"eo:cloud_cover":{"lt":maxcloud}},
          "sortby":[{"field":"properties.eo:cloud_cover","direction":"asc"}]}
    r=S.post("https://earth-search.aws.element84.com/v1/search",json=body,timeout=90); r.raise_for_status()
    return r.json()["features"]
for name,dt in [("pre","2026-05-20T00:00:00Z/2026-06-22T12:00:00Z"),("post","2026-06-23T00:00:00Z/2026-08-20T23:59:59Z")]:
    fs=q(dt)
    print("=====",name,len(fs))
    for f in fs[:20]:
        p=f["properties"]
        print(p["datetime"][:10], round(p.get("eo:cloud_cover",-1),1), f["id"])