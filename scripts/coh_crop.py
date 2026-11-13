import numpy as np
from pathlib import Path
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
print(coh.shape,x0,y0)
sm=ndimage.uniform_filter(coh,size=5)
CX0,CX1,CY0,CY1=654000,665000,6462000,6484000
def nc(a):
    c0=int((CX0-x0)/20); c1=int((CX1-x0)/20); r0=int((y0-CY1)/20); r1=int((y0-CY0)/20)
    return a[r0:r1,c0:c1]
fig,ax=plt.subplots(1,4,figsize=(22,9),dpi=90); ext=[CX0,CX1,CY0,CY1]
im=ax[0].imshow(nc(coh),cmap="magma",vmin=0.1,vmax=0.75,extent=ext); ax[0].set_title("coherence 20.06-02.07"); plt.colorbar(im,ax=ax[0],fraction=.03)
im=ax[1].imshow(nc(sm),cmap="magma",vmin=0.1,vmax=0.7,extent=ext); ax[1].set_title("coherence sm5"); plt.colorbar(im,ax=ax[1],fraction=.03)
mask=np.load(R/"data/s2/main_mask.npy")
def ci(a):
    c0=int((CX0-642360)/10); c1=int((CX1-642360)/10); r0=int((6499680-CY1)/10); r1=int((6499680-CY0)/10)
    return a[r0:r1,c0:c1]
ax[2].imshow(ci(mask.astype(float)),cmap="gray",extent=ext); ax[2].set_title("dNBR mask")
im=ax[3].imshow(nc(sm),cmap="magma",vmin=0.1,vmax=0.7,extent=ext); ax[3].contour(ci(mask.astype(float)),levels=[0.5],colors="#39d0c0",linewidths=0.8); ax[3].set_title("coh + mask")
for a in ax: a.set_xlim(CX0,CX1); a.set_ylim(CY0,CY1)
plt.tight_layout(); plt.savefig(R/"build/coh_crop.png",dpi=90)
print("saved")