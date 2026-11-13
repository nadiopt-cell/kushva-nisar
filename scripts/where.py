import numpy as np
from pathlib import Path
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=5)
from PIL import Image
img=np.asarray(Image.open(R/"web/data/s2_post.jpg"))
ext_img=[642360,682280,6451360,6499680]
fig,ax=plt.subplots(1,3,figsize=(21,10),dpi=85)
ax[0].imshow(img,extent=ext_img); ax[0].set_title("S2 post SWIR")
im=ax[1].imshow(dnbr,cmap="inferno",vmin=0,vmax=0.5,extent=ext_img); ax[1].set_title("dNBR")
ax[2].imshow(sm,cmap="magma",vmin=0.12,vmax=0.62,extent=[x0,x0+2300*20,y0-2900*20,y0]); ax[2].set_title("coherence")
for a in ax:
    a.set_xlim(650000,670000); a.set_ylim(6455000,6500000)
    for gx in range(650000,671000,5000): a.axvline(gx,color="cyan",lw=.3,alpha=.5)
    for gy in range(6460000,6501000,5000): a.axhline(gy,color="cyan",lw=.3,alpha=.5)
plt.tight_layout(); plt.savefig(R/"build/where.png",dpi=85)
print("saved")