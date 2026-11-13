import requests, json
bbox=[59.55,58.15,60.10,58.65]
S=requests.Session()
body={"collections":["sentinel-2-l2a"],"bbox":bbox,"datetime":"2026-05-25T00:00:00Z/2026-08-31T23:59:59Z","limit":100}
r=S.post("https://earth-search.aws.element84.com/v1/search",json=body,timeout=90)
print(r.status_code); print(r.text[:800])