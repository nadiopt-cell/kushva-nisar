import pickle, numpy as np, rasterio
from pathlib import Path
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
poly,cl,mask_in=pickle.load(open(R/"build/contour.pkl","rb"))
# fill holes and smooth
parts=[]
for g in (poly.geoms if hasattr(poly,"geoms") else [poly]):
    parts.append(Polygon(g.exterior))
p=unary_union(parts)
p=p.buffer(45,join_style=1).buffer(-45,join_style=1)
p=p.simplify(5)
if isinstance(p,MultiPolygon): p=unary_union([g for g in p.geoms if g.area>3e4])
print(p.geom_type,p.area/1e4)
# recompute stats
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
from scipy import ndimage
sm=ndimage.uniform_filter(coh,size=3)
tr=rasterio.transform.from_origin(x0,y0,20,20)
from rasterio.features import rasterize
mi=rasterize([(p,1)],out_shape=coh.shape,transform=tr,fill=0).astype(bool)
dw=ndimage.distance_transform_edt(mi)*20
print("coh",np.nanmean(sm[mi]),"maxw",dw.max()*2,"ha",mi.sum()*400/1e4)
# update geojson props
import json
from pyproj import Transformer
from shapely.ops import transform as shp_tr
trf=Transformer.from_crs(32640,4326,always_xy=True)
pg=shp_tr(lambda x,y,z=None: trf.transform(x,y),p)
gj={"type":"FeatureCollection","features":[{"type":"Feature","properties":{
 "name":"Ветровал Кушва · 22.06.2026","area_ha":round(p.area/1e4,1),"length_km":round(cl.length/1000,1),
 "width_max_m":round(dw.max()*2,0),"coh_mean":round(float(np.nanmean(sm[mi])),3)},
 "geometry":pg.__geo_interface__}]}
json.dump(gj,open(R/"web/data/contour.geojson","w"),ensure_ascii=False)
pickle.dump((p,cl,mi),open(R/"build/contour_smooth.pkl","wb"))
print("saved", (R/"web/data/contour.geojson").stat().st_size)