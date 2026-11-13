import numpy as np, rasterio, pickle
from pathlib import Path
from scipy import ndimage
from shapely.geometry import shape, LineString, MultiPolygon, Point
from shapely.ops import unary_union, transform as shp_tr
from rasterio.features import shapes, rasterize
from pyproj import Transformer
import geopandas as gpd
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=3)
idx=np.load(R/"data/s2/indices.npz"); ndvi=idx["ndvi_pre"]
tr10=rasterio.transform.from_origin(642360,6499680,10,10); tr=rasterio.transform.from_origin(x0,y0,20,20)
nd20=np.zeros(coh.shape,dtype="float32")
rasterio.warp.reproject(ndvi.astype("float32"),nd20,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
dist=np.load(R/"data/nisar/corridor2.npy")
center=[(658200,6465900),(658050,6467500),(658120,6469300),(658350,6471000),(658600,6472600),(658800,6474200),
        (659050,6476000),(659300,6477600),(659650,6479300),(660050,6481000),(660500,6482800),(661000,6484500),
        (661600,6486200),(662300,6488000),(663100,6489800),(664000,6491500),(664900,6493100),(665700,6494300)]
cl=LineString(center)
base=(sm<0.285)&(dist<800)&(nd20>0.4)&(mk==11)
lab,n=ndimage.label(base); sizes=ndimage.sum(base,lab,range(1,n+1)); keep=np.zeros_like(base)
for i in range(n):
    if sizes[i]<30: continue
    ys,xs=np.where(lab==i+1)
    cx=x0+xs.mean()*20; cy=y0-ys.mean()*20
    if cl.distance(Point(cx,cy))<260: keep|=lab==i+1
print("components ha",keep.sum()*400/1e4)
ribbon=cl.buffer(38,cap_style=2,join_style=1)
geoms=[shape(g) for g,v in shapes(keep.astype("uint8"),transform=tr) if v==1]
poly=unary_union(geoms+[ribbon]).buffer(15).buffer(-15).simplify(3)
if isinstance(poly,MultiPolygon): poly=unary_union([g for g in poly.geoms if g.area>5000])
print("area ha",poly.area/1e4, "type",poly.geom_type)
mask_in=rasterize([(poly,1)],out_shape=coh.shape,transform=tr,fill=0).astype(bool)
dw=ndimage.distance_transform_edt(mask_in)*20
print("coh mean",np.nanmean(sm[mask_in]),"mask ha",mask_in.sum()*400/1e4,"maxw",dw.max()*2)
trf=Transformer.from_crs(32640,4326,always_xy=True)
togeo=lambda g: shp_tr(lambda x,y,z=None: trf.transform(x,y),g)
props={"name":"Ветровал Кушва · 22.06.2026","area_ha":round(poly.area/1e4,1),
   "length_km":round(cl.length/1000,1),"width_max_m":round(dw.max()*2,0),
   "coh_mean":round(float(np.nanmean(sm[mask_in])),3)}
g=gpd.GeoDataFrame([props],geometry=[togeo(poly)],crs="EPSG:4326")
g.to_file(R/"web/data/contour.geojson",driver="GeoJSON")
gpd.GeoDataFrame([{"name":"ось следа"}],geometry=[togeo(cl)],crs="EPSG:4326").to_file(R/"web/data/track.geojson",driver="GeoJSON")
pickle.dump((poly,cl,mask_in),open(R/"build/contour.pkl","wb"))
print(props)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,12),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+coh.shape[1]*20,y0-coh.shape[0]*20,y0])
for gg in (poly.geoms if hasattr(poly,"geoms") else [poly]):
    xs,ys=gg.exterior.xy; ax.plot(xs,ys,color="#5eead4",lw=1)
xs,ys=cl.xy; ax.plot(xs,ys,color="white",lw=.6,ls="--")
ax.set_xlim(655000,670000); ax.set_ylim(6464000,6497000)
plt.tight_layout(); plt.savefig(R/"build/final_contour4.png",dpi=100)
print("saved")