import numpy as np, json, rasterio
from pathlib import Path
from scipy import ndimage
from shapely.geometry import shape, mapping, LineString, MultiPolygon, Polygon
from shapely.ops import unary_union
from rasterio.features import shapes
from pyproj import Transformer
import geopandas as gpd

R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=3)
m=np.load(R/"data/nisar/coh_mask2.npy")
# filter components near manual axis and large
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
keep=np.zeros_like(m)
for i in range(n):
    if sizes[i]>=40: keep|=lab==i+1
# north ribbon manual points (UTM40N)
north=[(658200,6480200),(658700,6481400),(659300,6482800),(660100,6484400),(661100,6486300),
       (662200,6488400),(663400,6490300),(664500,6492200),(665500,6493800),(666100,6494700)]
line=LineString(north).buffer(62,cap_style=2,join_style=2)
# polygonize mask
tr=rasterio.transform.from_origin(x0,y0,20,20)
geoms=[shape(g) for g,v in shapes(keep.astype("uint8"),transform=tr) if v==1]
poly=unary_union(geoms+[line])
poly=poly.buffer(25).buffer(-25)
if isinstance(poly,MultiPolygon):
    poly=max(poly.geoms,key=lambda g:g.area)
poly=poly.simplify(4)
print("area ha",poly.area/1e4,"length km",poly.length/1000)
# stats inside
from rasterio.features import rasterize
mask_in=rasterize([(poly,1)],out_shape=coh.shape,transform=tr,fill=0).astype(bool)
print("coh mean",np.nanmean(sm[mask_in]),"area comp",mask_in.sum()*400/1e4)
# max width: distance transform inside
dist=ndimage.distance_transform_edt(mask_in)*20
print("max width m",dist.max()*2)
# centerline: skeleton-ish via medial axis approx (use polygon centroid line along y)
# build centerline from mask per row median x, smooth
rows=np.where(mask_in.any(1))[0]
pts=[]
for r in rows[::10]:
    xs=np.where(mask_in[r])[0]
    if len(xs)>0: pts.append((x0+xs.mean()*20+10, y0-r*20-10))
cl=LineString(pts).simplify(10)
print("centerline km",cl.length/1000)
# export
trf=Transformer.from_crs(32640,4326,always_xy=True)
def togeo(g):
    from shapely.ops import transform as shp_tr
    return shp_tr(lambda x,y,z=None: trf.transform(x,y),g)
g=gpd.GeoDataFrame([{"name":"Ветровал Кушва · 22.06.2026","area_ha":round(poly.area/1e4,1),
   "length_km":round(cl.length/1000,1),"width_max_m":round(dist.max()*2,0),
   "coh_mean":round(float(np.nanmean(sm[mask_in])),3)}],geometry=[togeo(poly)],crs="EPSG:4326")
g.to_file(R/"web/data/contour.geojson",driver="GeoJSON")
gpd.GeoDataFrame([{"name":"ось следа"}],geometry=[togeo(cl)],crs="EPSG:4326").to_file(R/"web/data/track.geojson",driver="GeoJSON")
print(g.drop(columns="geometry").to_string())
# preview
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(8,11),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+coh.shape[1]*20,y0-coh.shape[0]*20,y0])
xs,ys=poly.exterior.xy; ax.plot(xs,ys,color="#5eead4",lw=1)
xs,ys=cl.xy; ax.plot(xs,ys,color="white",lw=.6,ls="--")
ax.set_xlim(655000,670000); ax.set_ylim(6464000,6497000)
plt.tight_layout(); plt.savefig(R/"build/final_contour.png",dpi=100)
print("saved")