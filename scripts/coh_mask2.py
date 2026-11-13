import numpy as np
from pathlib import Path
from scipy import ndimage
import rasterio, rasterio.warp
from rasterio.transform import from_origin
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=3)
idx=np.load(R/"data/s2/indices.npz"); ndvi=idx["ndvi_pre"]
tr10=from_origin(642360,6499680,10,10); tr20=from_origin(x0,y0,20,20)
out=np.zeros(coh.shape,dtype="float32")
rasterio.warp.reproject(ndvi.astype("float32"),out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
H,W=coh.shape; ys,xs=np.mgrid[0:H,0:W]; X=x0+xs*20+10; Y=y0-ys*20-10
pts=[(657800,6468600),(658300,6471400),(658900,6474800),(659500,6477900),(660300,6481000),(661300,6484100),(662300,6487000),(663500,6490000),(664800,6492900),(665900,6494500)]
def segd(px,py,ax,ay,bx,by):
    vx,vy=bx-ax,by-ay; wx,wy=px-ax,py-ay; t=np.clip((wx*vx+wy*vy)/(vx*vx+vy*vy+1e-9),0,1)
    return np.hypot(px-(ax+t*vx),py-(ay+t*vy))
dist=np.full((H,W),1e9,dtype="float32")
for i in range(len(pts)-1): dist=np.minimum(dist,segd(X,Y,*pts[i],*pts[i+1]).astype("float32"))
np.save(R/"data/nisar/corridor2.npy",dist)
for th in [0.26,0.27,0.28,0.29,0.30]:
    m=(sm<th)&(dist<900)&(out>0.4)&(mk==11)
    m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=4)
    lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
    print("th",th,"ha",round(m.sum()*400/1e4,1),"largest",round(sizes.max()*400/1e4,1) if len(sizes) else 0,"n>50",int((sizes>50).sum()))
m=(sm<0.285)&(dist<900)&(out>0.4)&(mk==11)
m=ndimage.binary_closing(ndimage.binary_opening(m,iterations=2),iterations=4)
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
keep=np.zeros_like(m)
for i in range(n):
    if sizes[i]>40: keep|=lab==i+1
np.save(R/"data/nisar/coh_mask2.npy",keep)
fig,ax=plt.subplots(figsize=(8,12),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+W*20,y0-H*20,y0])
ax.contour(keep,levels=[0.5],colors="#5eead4",linewidths=.8,extent=[x0,x0+W*20,y0-H*20,y0])
ax.set_xlim(655000,670000); ax.set_ylim(6465000,6499000)
plt.tight_layout(); plt.savefig(R/"build/coh_mask2.png",dpi=100)
print("saved",keep.sum()*400/1e4)