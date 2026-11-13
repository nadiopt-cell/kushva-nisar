import numpy as np, rasterio
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
def rd(n,b):
    with rasterio.open(R/f"data/s2/{n}_{b}.tif") as ds: return ds.read(1), ds.bounds, ds.transform
pre={}; post={}
for b in ["swir22","swir16","nir","red","green","blue","scl"]:
    pre[b],bnd,tr=rd("pre",b); post[b],_,_=rd("post",b)
H,W=pre["nir"].shape
print("grid",W,H,bnd)
def stretch(a,lo=2,hi=98,mask=None):
    v=a[np.isfinite(a)&(a>0)] if mask is None else a[mask]
    p1,p2=np.percentile(v,[lo,hi]); return np.clip((a-p1)/(p2-p1),0,1)
def comp(d,bands):
    return np.dstack([stretch(d[b]) for b in bands])
def nbr(d): return (d["nir"]-d["swir22"])/(d["nir"]+d["swir22"]+1e-6)
dnbr=nbr(pre)-nbr(post)
ndvi_pre=(pre["nir"]-pre["red"])/(pre["nir"]+pre["red"]+1e-6)
ndvi_post=(post["nir"]-post["red"])/(post["nir"]+post["red"]+1e-6)
dndvi=ndvi_pre-ndvi_post
cloud=(post["scl"]==8)|(post["scl"]==9)|(post["scl"]==10)
np.savez_compressed(R/"data/s2/indices.npz",dnbr=dnbr,dndvi=dndvi,ndvi_pre=ndvi_pre,cloud=cloud)
fig,ax=plt.subplots(1,4,figsize=(24,7.6),dpi=85)
ax[0].imshow(comp(pre,["swir22","nir","red"])); ax[0].set_title("S2 pre 21.05 SWIR")
ax[1].imshow(comp(post,["swir22","nir","red"])); ax[1].set_title("S2 post 28.07 SWIR")
im=ax[2].imshow(dnbr,cmap="RdBu_r",vmin=-0.6,vmax=0.6); ax[2].set_title("dNBR"); plt.colorbar(im,ax=ax[2],fraction=.03)
im=ax[3].imshow(dndvi,cmap="RdBu_r",vmin=-0.5,vmax=0.5); ax[3].set_title("dNDVI"); plt.colorbar(im,ax=ax[3],fraction=.03)
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig(R/"build/s2_indices.png",dpi=85)
print("dnbr pct",np.percentile(dnbr,[50,90,95,99,99.5,99.9]),"max",dnbr.max())
print("saved")