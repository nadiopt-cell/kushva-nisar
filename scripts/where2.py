import numpy as np
from pathlib import Path
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=5)
img=np.asarray(Image.open(R/"web/data/s2_post.jpg")); ext_img=[642360,682280,6451360,6499680]
CX0,CX1,CY0,CY1=656000,668000,6469000,6496000
fig,ax=plt.subplots(1,3,figsize=(20,11),dpi=100)
def ci(a):
    c0=int((CX0-642360)/10); c1=int((CX1-642360)/10); r0=int((6499680-CY1)/10); r1=int((6499680-CY0)/10); return a[r0:r1,c0:c1]
def nc(a):
    c0=int((CX0-x0)/20); c1=int((CX1-x0)/20); r0=int((y0-CY1)/20); r1=int((y0-CY0)/20); return a[r0:r1,c0:c1]
ax[0].imshow(ci(img),extent=[CX0,CX1,CY0,CY1]); ax[0].set_title("S2 post")
im=ax[1].imshow(ci(dnbr),cmap="inferno",vmin=0,vmax=0.5,extent=[CX0,CX1,CY0,CY1]); ax[1].set_title("dNBR")
im=ax[2].imshow(nc(sm),cmap="magma",vmin=0.12,vmax=0.62,extent=[CX0,CX1,CY0,CY1]); ax[2].set_title("coherence")
for a in ax:
    for gx in range(657000,668000,1000): a.axvline(gx,color="cyan",lw=.25,alpha=.6)
    for gy in range(6470000,6497000,1000): a.axhline(gy,color="cyan",lw=.25,alpha=.6)
    a.set_xlim(CX0,CX1); a.set_ylim(CY0,CY1)
plt.tight_layout(); plt.savefig(R/"build/where2.png",dpi=100)
print("saved")