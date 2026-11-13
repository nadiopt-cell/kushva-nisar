import numpy as np
from pathlib import Path
from scipy import ndimage
from pyproj import Transformer
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=5)
idx=np.load(R/"data/s2/indices.npz"); ndvi=idx["ndvi_pre"]; dnbr=idx["dnbr"]
# resample ndvi/dnbr to 20m nisar grid
import rasterio, rasterio.warp
from rasterio.transform import from_origin
tr10=from_origin(642360,6499680,10,10); tr20=from_origin(x0,y0,20,20)
def res(a):
    out=np.zeros(coh.shape,dtype="float32")
    rasterio.warp.reproject(a.astype("float32"),out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
    return out
nd20=res(ndvi); dn20=res(dnbr)
# corridor
tr=Transformer.from_crs(4326,32640,always_xy=True)
pts=[(59.7592,58.2986),(59.735,58.35),(59.742,58.40),(59.755,58.45),(59.78,58.50),(59.80,58.55)]
xy=np.array([tr.transform(*p) for p in pts])
H,W=coh.shape; ys,xs=np.mgrid[0:H,0:W]
X=x0+xs*20+10; Y=y0-ys*20-10
def segd(px,py,ax,ay,bx,by):
    vx,vy=bx-ax,by-ay; wx,wy=px-ax,py-ay
    t=np.clip((wx*vx+wy*vy)/(vx*vx+vy*vy+1e-9),0,1)
    return np.hypot(px-(ax+t*vx),py-(ay+t*vy))
dist=np.full((H,W),1e9,dtype="float32")
for i in range(len(xy)-1): dist=np.minimum(dist,segd(X,Y,*xy[i],*xy[i+1]).astype("float32"))
np.save(R/"data/nisar/corridor_dist.npy",dist)
for th in [0.22,0.25,0.28,0.30,0.32]:
    m=(sm<th)&(dist<800)&(nd20>0.45)&(mk==11)
    m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=3)
    lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
    print("th",th,"ha",round(m.sum()*400/1e4,1),"comps>50px",int((sizes>50).sum()),"largest ha",round(sizes.max()*400/1e4,1) if len(sizes) else 0)
m=(sm<0.275)&(dist<800)&(nd20>0.45)&(mk==11)
m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=3)
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
order=np.argsort(sizes)[::-1]
# keep components > 30 px or near track core
keep=np.zeros_like(m)
for i in order[:12]:
    if sizes[i]>30: keep|=lab==i+1
np.save(R/"data/nisar/coh_mask.npy",keep)
fig,ax=plt.subplots(figsize=(9,11),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62)
ax.contour(keep,levels=[0.5],colors="#4fd1c5",linewidths=0.8)
ax.set_title("coherence + threshold contour")
plt.tight_layout(); plt.savefig(R/"build/coh_mask.png",dpi=100)
print("saved",keep.sum()*400/1e4,"ha")