import numpy as np
from pathlib import Path
from scipy import ndimage
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
w=np.load(R/"data/nisar/nisar_windows.npz"); hv1=w["hv1"]; hv2=w["hv2"]
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]
import rasterio, rasterio.warp
from rasterio.transform import from_origin
tr10=from_origin(642360,6499680,10,10); tr20=from_origin(x0,y0,20,20)
out=np.zeros(coh.shape,dtype="float32"); rasterio.warp.reproject(dnbr.astype("float32"),out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=rasterio.warp.Resampling.average)
sm=ndimage.uniform_filter(coh,size=3)
H,W=coh.shape; ys,xs=np.mgrid[0:H,0:W]; X=x0+xs*20+10; Y=y0-ys*20-10
def box(xa,xb,ya,yb):
    return (X>xa)&(X<xb)&(Y>ya)&(Y<yb)
regions={"north_band":box(660000,663000,6482000,6492000),"mid_band":box(658000,660500,6473000,6481000),"south_band":box(657000,659500,6465500,6472000)}
for nm,m in regions.items():
    forest=m&(sm<0.35)
    print(nm,"px",m.sum(),"coh",round(float(np.mean(sm[m])),3),"preHV",round(float(np.mean(10*np.log10(np.clip(hv1[m],1e-6,None)))),2),"postHV",round(float(np.mean(10*np.log10(np.clip(hv2[m],1e-6,None)))),2),"dHV",round(float(np.mean(dhv[m])),2),"dNBR",round(float(np.mean(out[m])),3))
# compare forest buffer around north band
buf=box(657000,666000,6482000,6492000)&~box(659500,663500,6481000,6492000)&(sm>0.4)
print("north buffer forest",buf.sum(),"coh",round(float(np.mean(sm[buf])),3),"preHV",round(float(np.mean(10*np.log10(np.clip(hv1[buf],1e-6,None)))),2),"dHV",round(float(np.mean(dhv[buf])),2),"dNBR",round(float(np.mean(out[buf])),3))