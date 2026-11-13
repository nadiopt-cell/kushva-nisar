import numpy as np, rasterio
from pathlib import Path
from scipy import ndimage
from pyproj import Transformer
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
d=np.load(R/"data/nisar/nisar_windows.npz")
x0,y0=d["x0"],d["y0"]; hh1,hv1,hh2,hv2=d["hh1"],d["hv1"],d["hh2"],d["hv2"]
dhv=10*np.log10(np.clip(hv2,1e-6,None))-10*np.log10(np.clip(hv1,1e-6,None))
dhh=10*np.log10(np.clip(hh2,1e-6,None))-10*np.log10(np.clip(hh1,1e-6,None))
bg=ndimage.uniform_filter(dhv,size=101)
anom=dhv-bg
np.savez(R/"data/nisar/deltas.npz",dhv=dhv,dhh=dhh,anom=anom,x0=x0,y0=y0)
print("bounds",x0,x0+dhv.shape[1]*20,y0-dhv.shape[0]*20,y0,flush=True)
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi_pre=idx["ndvi_pre"]
CX0,CX1=651000,676000; CY0,CY1=6454000,6494000
def ci(a):
    c0=int((CX0-642360)/10); c1=int((CX1-642360)/10); r0=int((6499680-CY1)/10); r1=int((6499680-CY0)/10)
    return a[r0:r1,c0:c1]
def nc(a):
    c0=int((CX0-x0)/20); c1=int((CX1-x0)/20); r0=int((y0-CY1)/20); r1=int((y0-CY0)/20)
    return a[r0:r1,c0:c1]
fig,ax=plt.subplots(1,4,figsize=(24,8),dpi=85); ext=[CX0,CX1,CY0,CY1]
im=ax[0].imshow(ci(dnbr),cmap="RdBu_r",vmin=-0.5,vmax=0.5,extent=ext); ax[0].set_title("dNBR")
ax[1].imshow(ci(ndvi_pre),cmap="Greens",vmin=0.3,vmax=0.9,extent=ext); ax[1].set_title("NDVI pre")
im=ax[2].imshow(nc(dhv),cmap="RdBu_r",vmin=-3,vmax=3,extent=ext); ax[2].set_title("NISAR dHV"); plt.colorbar(im,ax=ax[2],fraction=.03)
im=ax[3].imshow(nc(anom),cmap="RdBu_r",vmin=-1.5,vmax=1.5,extent=ext); ax[3].set_title("NISAR dHV anomaly"); plt.colorbar(im,ax=ax[3],fraction=.03)
for a in ax: a.set_xlim(CX0,CX1); a.set_ylim(CY0,CY1)
plt.tight_layout(); plt.savefig(R/"build/track_crop1.png",dpi=85)
print("saved",flush=True)