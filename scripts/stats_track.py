import numpy as np, rasterio
from pathlib import Path
from scipy import ndimage
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]; cloud=idx["cloud"]
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]; dhh=d["dhh"]; x0=d["x0"]; y0=d["y0"]
# rebuild nisar ratio change
w=np.load(R/"data/nisar/nisar_windows.npz")
hh1,hv1,hh2,hv2=w["hh1"],w["hv1"],w["hh2"],w["hv2"]
ratio1=10*np.log10(np.clip(hv1,1e-6,None))-10*np.log10(np.clip(hh1,1e-6,None))
ratio2=10*np.log10(np.clip(hv2,1e-6,None))-10*np.log10(np.clip(hh2,1e-6,None))
dratio=ratio2-ratio1
# map 10m S2 to 20m NISAR grid
tr10=rasterio.transform.from_origin(642360,6499680,10,10)
tr20=rasterio.transform.from_origin(x0,y0,20,20)
import rasterio.warp
def resample(a):
    out=np.full(dhv.shape,np.nan,dtype="float32")
    rasterio.warp.reproject(a,out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
    return out
dn20=resample(dnbr.astype("float32")); nd20=resample(ndvi.astype("float32"))
mask=(dn20>0.22)&(nd20>0.55)&np.isfinite(dhv)
print("track px",mask.sum(),"forest", (nd20>0.6).mean())
# buffer mask
buf=ndimage.binary_dilation(mask,iterations=16) & ~ndimage.binary_dilation(mask,iterations=4) & (nd20>0.55)
print("buffer px",buf.sum())
for nm,a in [("dhv",dhv),("dhh",dhh),("dratio",dratio)]:
    print(nm,"track",np.nanmean(a[mask]),"buf",np.nanmean(a[buf]),"diff",np.nanmean(a[mask])-np.nanmean(a[buf]))
# smoothed versions
for s in [3,5,9]:
    sm=ndimage.uniform_filter(dhv,size=s)
    print("sm",s,"track",np.nanmean(sm[mask]),"buf",np.nanmean(sm[buf]))
# save mask preview and stats
np.savez(R/"data/nisar/trackstats.npz",mask=mask,dn20=dn20,nd20=nd20,dratio=dratio)
# profile across track: choose x transect at y=6482000
def prof(a,yy,xc=660200,half=1200):
    row=int((y0-yy)/20)
    return np.arange(xc-half,xc+half,20), a[row,int((xc-half-x0)/20):int((xc+half-x0)/20)]
yy=6481000
xs,p1=prof(dhv,yy); _,p2=prof(dn20,yy); _,p3=prof(ndimage.uniform_filter(dhv,size=9),yy)
print("profile len",len(p1))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(3,1,figsize=(12,8),dpi=100,sharex=True)
ax[0].plot(xs,p2); ax[0].set_ylabel("dNBR")
ax[1].plot(xs,p1); ax[1].set_ylabel("dHV"); ax[1].grid(alpha=.3)
ax[2].plot(xs,p3); ax[2].set_ylabel("dHV sm9"); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig(R/"build/profile.png")
print("saved")