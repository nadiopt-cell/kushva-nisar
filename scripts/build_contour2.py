import numpy as np, json, rasterio
from pathlib import Path
from scipy import ndimage
from shapely.geometry import shape, LineString, MultiPolygon
from shapely.ops import unary_union, transform as shp_tr
from rasterio.features import shapes, rasterize
from pyproj import Transformer
import geopandas as gpd

R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=5)
# forest mask at 20m
idx=np.load(R/"data/s2/indices.npz"); ndvi=idx["ndvi_pre"]
tr10=rasterio.transform.from_origin(642360,6499680,10,10); tr=rasterio.transform.from_origin(x0,y0,20,20)
nd20=np.zeros(coh.shape,dtype="float32")
rasterio.warp.reproject(ndvi.astype("float32"),nd20,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
# corridor
dist=np.load(R/"data/nisar/corridor2.npy")
base=(sm<0.30)&(dist<900)&(nd20>0.38)&(mk==11)
# close along track
st=ndimage.generate_binary_structure(2,1)
m=ndimage.binary_closing(base,structure=st,iterations=12)
m=ndimage.binary_opening(m,structure=st,iterations=2)
m=ndimage.binary_fill_holes(m)
# keep parts near corridor and reasonably sized
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1)); keep=np.zeros_like(m)
for i in range(n):
    if sizes[i]>200: keep|=lab==i+1
# north ribbon
north=[(658400,6480600),(659000,6482300),(659900,6484200),(661000,6486200),(662100,6488300),
       (663300,6490200),(664400,6492100),(665400,6493700),(666100,6494700)]
line=LineString(north).buffer(65,cap_style=2,join_style=1)
geoms=[shape(g) for g,v in shapes(keep.astype("uint8"),transform=tr) if v==1]
poly=unary_union(geoms+[line])
poly=poly.buffer(25).buffer(-25).simplify(4)
print("type",poly.geom_type)
if isinstance(poly,MultiPolygon):
    print("parts",[round(g.area/1e4,1) for g in poly.geoms])
    poly=unary_union([g for g in poly.geoms if g.area>2e4] or [poly])
if isinstance(poly,MultiPolygon): poly=unary_union(list(poly.geoms))
print("area ha",poly.area/1e4)
mask_in=rasterize([(poly,1)],out_shape=coh.shape,transform=tr,fill=0).astype(bool)
print("coh mean",np.nanmean(sm[mask_in]),"px ha",mask_in.sum()*400/1e4)
dist_in=ndimage.distance_transform_edt(mask_in)*20
print("max width",dist_in.max()*2)
# centerline from manual full track
center=[(658200,6465500),(658000,6467000),(658100,6469000),(658500,6471200),(658800,6473500),(659100,6476000),
        (659500,6478500),(660000,6480800),(660600,6483000),(661300,6485200),(662200,6487400),(663200,6489500),
        (664200,6491500),(665300,6493500),(666100,6494700)]
cl=LineString(center)
print("length km",cl.length/1000)
trf=Transformer.from_crs(32640,4326,always_xy=True)
togeo=lambda g: shp_tr(lambda x,y,z=None: trf.transform(x,y),g)
g=gpd.GeoDataFrame([{"name":"Ветровал Кушва · 22.06.2026","area_ha":round(poly.area/1e4,1),
   "length_km":round(cl.length/1000,1),"width_max_m":round(dist_in.max()*2,0),
   "coh_mean":round(float(np.nanmean(sm[mask_in])),3)}],geometry=[togeo(poly)],crs="EPSG:4326")
g.to_file(R/"web/data/contour.geojson",driver="GeoJSON")
gpd.GeoDataFrame([{"name":"ось следа"}],geometry=[togeo(cl)],crs="EPSG:4326").to_file(R/"web/data/track.geojson",driver="GeoJSON")
# also save polygon utm for later
import pickle; pickle.dump((poly,cl),open(R/"build/contour.pkl","wb"))
print(g.drop(columns="geometry").to_string())
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,12),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+coh.shape[1]*20,y0-coh.shape[0]*20,y0])
for gg in (poly.geoms if hasattr(poly,"geoms") else [poly]):
    xs,ys=gg.exterior.xy; ax.plot(xs,ys,color="#5eead4",lw=1)
xs,ys=cl.xy; ax.plot(xs,ys,color="white",lw=.6,ls="--")
ax.set_xlim(655000,670000); ax.set_ylim(6464000,6497000)
plt.tight_layout(); plt.savefig(R/"build/final_contour2.png",dpi=100)
print("saved")