import json, math
from pathlib import Path
import geopandas as gpd
from shapely.geometry import LineString, Polygon, Point, shape
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
d=json.load(open(R/"data/osm_kushva.json",encoding="utf-8"))
els={e["id"]:e for e in d["elements"]}
def geom_way(e):
    pts=[]
    for nid in e.get("nodes",[]):
        n=els.get(nid)
        if n: pts.append((n["lon"],n["lat"]))
    return pts
roads=[]; water=[]
for e in d["elements"]:
    if e["type"]!="way": continue
    t=e.get("tags",{})
    pts=geom_way(e)
    if len(pts)<2: continue
    if "highway" in t:
        roads.append({"highway":t["highway"],"name":t.get("name",""),"geometry":LineString(pts)})
    elif t.get("natural")=="water" or t.get("water"):
        if len(pts)>=4:
            try:
                p=Polygon(pts)
                if p.is_valid and p.area>1e-7: water.append({"geometry":p})
            except: pass
places=[]
for e in d["elements"]:
    if e["type"]=="node" and e.get("tags",{}).get("place"):
        places.append({"name":e["tags"].get("name",""),"place":e["tags"]["place"],"geometry":Point(e["lon"],e["lat"])})
# add labels
extra=[{"name":"Кушвинский пруд","place":"water","geometry":Point(59.742,58.295)},
       {"name":"Кушва","place":"city","geometry":Point(59.759,58.299)},
       {"name":"Малая Лая","place":"village","geometry":Point(59.85,58.153)},
       {"name":"Баранчинский","place":"town","geometry":Point(59.72,58.28)}]
places+=extra
for name,rows in [("roads",roads),("water",water),("places",places)]:
    g=gpd.GeoDataFrame(rows,crs="EPSG:4326")
    if name=="places": g=g.drop_duplicates(subset=["name"])
    g.to_file(R/f"web/data/{name}.geojson",driver="GeoJSON")
    print(name,len(g))