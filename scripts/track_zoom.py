import numpy as np
from pathlib import Path
from scipy import ndimage
import rasterio, rasterio.warp
from rasterio.transform import from_origin
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]; cloud=idx["cloud"]
m0=np.load(R/"data/s2/dnbr_mask.npy")
lab,n=ndimage.label(m0); sizes=ndimage.sum(m0,lab,range(1,n+1)); big=(np.argmax(sizes)+1)
mask=lab==big; print("main comp",mask.sum()*100/1e4,"ha")
ys,xs=np.where(mask); print("rows",ys.min(),ys.max(),"cols",xs.min(),xs.max())
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]; dhh=d["dhh"]; anom=d["anom"]; x0=d["x0"]; y0=d["y0"]
w=np.load(R/"data/nisar/nisar_windows.npz"); hh1,hv1,hh2,hv2=w["hh1"],w["hv1"],w["hh2"],w["hv2"]
ratio=10*np.log10(np.clip(hv2,1e-6,None))-10*np.log10(np.clip(hh2,1e-6,None))-(10*np.log10(np.clip(hv1,1e-6,None))-10*np.log10(np.clip(hh1,1e-6,None)))
tr10=from_origin(642360,6499680,10,10); tr20=from_origin(x0,y0,20,20)
def res(a):
    out=np.zeros(dhv.shape,dtype="float32")
    rasterio.warp.reproject(a.astype("float32"),out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
    return out
mk20=res(mask.astype("float32"))>0.5
nd20=res(ndvi.astype("float32"))
buf=ndimage.binary_dilation(mk20,iterations=25)&~ndimage.binary_dilation(mk20,iterations=8)&(nd20>0.6)
print("px20",mk20.sum(),"buf",buf.sum())
for nm,a in [("dhv",dhv),("dhh",dhh),("dratio",ratio),("anom",anom)]:
    print(nm,round(float(np.nanmean(a[mk20])),3),round(float(np.nanmean(a[buf])),3),round(float(np.nanmean(a[mk20])-np.nanmean(a[buf])),3))
for s in [2,4,6]:
    sm=ndimage.gaussian_filter(dhv,s)
    print("gauss",s,round(float(np.mean(sm[mk20])),3),round(float(np.mean(sm[buf])),3))
# zoom render
CX0,CX1,CY0,CY1=654000,665000,6462000,6484000
def nc(a):
    c0=int((CX0-x0)/20); c1=int((CX1-x0)/20); r0=int((y0-CY1)/20); r1=int((y0-CY0)/20)
    return a[r0:r1,c0:c1]
def ci(a):
    c0=int((CX0-642360)/10); c1=int((CX1-642360)/10); r0=int((6499680-CY1)/10); r1=int((6499680-CY0)/10)
    return a[r0:r1,c0:c1]
fig,ax=plt.subplots(1,4,figsize=(22,9),dpi=90); ext=[CX0,CX1,CY0,CY1]
im=ax[0].imshow(ci(dnbr),cmap="inferno",vmin=0,vmax=0.5,extent=ext); ax[0].set_title("dNBR"); plt.colorbar(im,ax=ax[0],fraction=.03)
im=ax[1].imshow(nc(ndimage.gaussian_filter(dhv,2)),cmap="RdBu_r",vmin=-1.5,vmax=1.5,extent=ext); ax[1].set_title("dHV (g2)"); plt.colorbar(im,ax=ax[1],fraction=.03)
im=ax[2].imshow(nc(ndimage.gaussian_filter(ratio,2)),cmap="RdBu_r",vmin=-1.2,vmax=1.2,extent=ext); ax[2].set_title("d(HV/HH) (g2)"); plt.colorbar(im,ax=ax[2],fraction=.03)
im=ax[3].imshow(ci(mask.astype(float)),cmap="gray",extent=ext); ax[3].set_title("dNBR mask")
for a in ax: a.set_xlim(CX0,CX1); a.set_ylim(CY0,CY1)
plt.tight_layout(); plt.savefig(R/"build/track_zoom.png",dpi=90)
np.save(R/"data/s2/main_mask.npy",mask); np.save(R/"data/nisar/main_mask20.npy",mk20)
print("saved")