import numpy as np, rasterio, json, pickle
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
p=Polygon(p.exterior) if p.geom_type=="Polygon" else unary_union([Polygon(g.exterior) for g in p.geoms])
p=p.buffer(30).buffer(-30).simplify(4)
north=[(658400,6480600),(659000,6482300),(659900,6484200),(661000,6486200),(662100,6488300),(663300,6490200),(664400,6492100),(665400,6493700),(666100,6494400)]
ribbon=LineString(north).buffer(38,cap_style=2,join_style=1)
p=unary_union([p,ribbon]).buffer(20).buffer(-20).simplify(4)
if isinstance(p,MultiPolygon): p=unary_union([g for g in p.geoms if g.area>2e4])
print(p.geom_type,"area",p.area/1e4)
# stats
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=3)
trn=rasterio.transform.from_origin(x0,y0,20,20)
mi=rasterize([(p,1)],out_shape=coh.shape,transform=trn,fill=0).astype(bool)
dw=ndimage.distance_transform_edt(mi)*20
print("maxw",dw.max()*2,"coh",np.nanmean(sm[mi]),"ha",mi.sum()*400/1e4)
cl=LineString([(658200,6465900),(658050,6467500),(658120,6469300),(658350,6471000),(658600,6472600),(658800,6474200),(659050,6476000),(659300,6477600),(659650,6479300),(660050,6481000),(660500,6482800),(661000,6484500),(661600,6486200),(662300,6488000),(663100,6489800),(664000,6491500),(664900,6493100),(665700,6494300)])
trf=Transformer.from_crs(32640,4326,always_xy=True)
pg=shp_tr(lambda x,y,z=None: trf.transform(x,y),p)
gj={"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"Ветровал Кушва · 22.06.2026","area_ha":round(p.area/1e4,1),"length_km":round(cl.length/1000,1),"width_max_m":round(dw.max()*2,0),"coh_mean":round(float(np.nanmean(sm[mi])),3)},"geometry":pg.__geo_interface__}]}
json.dump(gj,open(R/"web/data/contour.geojson","w"),ensure_ascii=False)
print(json.dumps(gj["features"][0]["properties"],ensure_ascii=False))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,12),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+coh.shape[1]*20,y0-coh.shape[0]*20,y0])
for g in (p.geoms if hasattr(p,"geoms") else [p]):
    xs,ys=g.exterior.xy; ax.plot(xs,ys,color="#5eead4",lw=1.2)
ax.set_xlim(655000,670000); ax.set_ylim(6464000,6497000)
plt.tight_layout(); plt.savefig(R/"build/contour_final.png",dpi=100)