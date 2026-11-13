import numpy as np, rasterio
from pathlib import Path
from scipy import ndimage
from pyproj import Transformer
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]; cloud=idx["cloud"]
tr=Transformer.from_crs(4326,32640,always_xy=True)
# corridor around track line
pts=[(59.7592,58.2986),(59.735,58.35),(59.742,58.40),(59.755,58.45),(59.78,58.50),(59.80,58.55)]
xy=np.array([tr.transform(*p) for p in pts])
print(xy)
# distance to polyline
H,W=dnbr.shape
ys,xs=np.mgrid[0:H,0:W]
X=642360+xs*10+5; Y=6499680-ys*10-5
def seg_dist(px,py,ax,ay,bx,by):
    vx,vy=bx-ax,by-ay; wx,wy=px-ax,py-ay
    t=np.clip((wx*vx+wy*vy)/(vx*vx+vy*vy+1e-9),0,1)
    return np.hypot(px-(ax+t*vx),py-(ay+t*vy))
dist=np.full((H,W),1e9,dtype="float32")
for i in range(len(xy)-1):
    dist=np.minimum(dist,seg_dist(X,Y,xy[i,0],xy[i,1],xy[i+1,0],xy[i+1,1]).astype("float32"))
print("corridor", (dist<800).mean())
for th in [0.10,0.12,0.15,0.20,0.25]:
    m=(dnbr>th)&(ndvi>0.45)&(~cloud)&(dist<800)
    m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=3)
    lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
    big=sizes[sizes>200]
    print("th",th,"px",m.sum(),"ha",round(m.sum()/100,1),"comps>200",len(big),"largest ha",round(big.max()/100 if len(big) else 0,1))
# save th .12
m=(dnbr>0.12)&(ndvi>0.45)&(~cloud)&(dist<800)
m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=3)
np.save(R/"data/s2/track_mask012.npy",m)
print("saved")