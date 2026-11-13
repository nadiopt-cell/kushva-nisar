import numpy as np, rasterio, json
from pathlib import Path
from scipy import ndimage
from shapely.geometry import shape, LineString, MultiPolygon, Polygon
from shapely.ops import unary_union, transform as shp_tr
from rasterio.features import shapes, rasterize
from pyproj import Transformer
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
mask=np.load(R/"data/s2/main_mask.npy")
tr=rasterio.transform.from_origin(642360,6499680,10,10)
geoms=[shape(g) for g,v in shapes(mask.astype("uint8"),transform=tr) if v==1]
p=unary_union(geoms)
parts=[Polygon(g.exterior) for g in (p.geoms if hasattr(p,"geoms") else [p])]
p=unary_union(parts).buffer(45).buffer(-45).simplify(18)
north=[(658400,6480600),(659000,6482300),(659900,6484200),(661000,6486200),(662100,6488300),(663300,6490200),(664400,6492100),(665400,6493700),(666100,6494400)]
p=unary_union([p,LineString(north).buffer(55,cap_style=2,join_style=1)]).buffer(25).buffer(-25).simplify(10)
if isinstance(p,MultiPolygon): p=unary_union([g for g in p.geoms if g.area>3e4])
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=3); trn=rasterio.transform.from_origin(x0,y0,20,20)
mi=rasterize([(p,1)],out_shape=coh.shape,transform=trn,fill=0).astype(bool)
dw=ndimage.distance_transform_edt(mi)*20
cl=LineString([(658200,6465900),(658050,6467500),(658120,6469300),(658350,6471000),(658600,6472600),(658800,6474200),(659050,6476000),(659300,6477600),(659650,6479300),(660050,6481000),(660500,6482800),(661000,6484500),(661600,6486200),(662300,6488000),(663100,6489800),(664000,6491500),(664900,6493100),(665700,6494300)])
trf=Transformer.from_crs(32640,4326,always_xy=True)
pg=shp_tr(lambda x,y,z=None: trf.transform(x,y),p); clg=shp_tr(lambda x,y,z=None: trf.transform(x,y),cl)
props={"name":"Ветровал Кушва · 22.06.2026","area_ha":round(p.area/1e4,1),"length_km":round(cl.length/1000,1),"width_max_m":round(dw.max()*2,0),"coh_mean":round(float(np.nanmean(sm[mi])),3)}
gj={"type":"FeatureCollection","features":[{"type":"Feature","properties":props,"geometry":pg.__geo_interface__}]}
with open(R/"web/data/contour.geojson","w",encoding="ascii") as f: json.dump(gj,f,ensure_ascii=True)
tg={"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"track"},"geometry":clg.__geo_interface__}]}
with open(R/"web/data/track.geojson","w",encoding="ascii") as f: json.dump(tg,f,ensure_ascii=True)
print("area",p.area/1e4,"verts",len(pg.exterior.coords) if p.geom_type=="Polygon" else sum(len(g.exterior.coords) for g in p.geoms))