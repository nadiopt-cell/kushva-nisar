import numpy as np, rasterio
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
def rd(n,b):
    with rasterio.open(R/f"data/s2/{n}_{b}.tif") as ds: return ds.read(1)
pre={b:rd("pre",b) for b in ["swir22","swir16","nir","red","green","blue","scl"]}
print("shape",pre["swir22"].shape)
def stretch(a,lo=2,hi=98):
    v=a[np.isfinite(a)&(a>0)]
    p1,p2=np.percentile(v,[lo,hi]); return np.clip((a-p1)/(p2-p1),0,1)
def comp(d,bands):
    return np.dstack([stretch(d[b]) for b in bands])
fig,ax=plt.subplots(1,3,figsize=(21,7),dpi=90)
ax[0].imshow(comp(pre,["swir22","nir","red"])); ax[0].set_title("SWIR 12-8-4")
ax[1].imshow(comp(pre,["nir","red","green"])); ax[1].set_title("NIR-R-G")
ax[2].imshow(pre["scl"],cmap="tab20",vmin=0,vmax=11); ax[2].set_title("SCL")
for a in ax: a.axis("off")
plt.tight_layout(); plt.savefig(R/"build/preview_pre.png",dpi=90)
print("cloud frac", ((pre["scl"]==8)|(pre["scl"]==9)|(pre["scl"]==10)).mean())