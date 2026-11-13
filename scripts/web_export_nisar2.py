import numpy as np, rasterio, json, glob
from pathlib import Path
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.transform import from_origin
from rasterio.merge import merge
from PIL import Image
R=Path(r"E:\ai_project\30days_challenge\day14_borges"); W=R/"web/data"
AOI=(59.45,58.18,60.10,58.60); res=30.0
l,b,r,t=transform_bounds("EPSG:4326","EPSG:3857",*AOI)
l=np.floor(l/res)*res; b=np.floor(b/res)*res; r=np.ceil(r/res)*res; t=np.ceil(t/res)*res
w=int((r-l)/res); h=int((t-b)/res); tr=from_origin(l,t,res,res)
def warp(src,srctr,srccrs,resamp=Resampling.bilinear,nodata=None):
    out=np.full((h,w),np.nan,dtype="float32")
    reproject(src,out,src_transform=srctr,src_crs=srccrs,dst_transform=tr,dst_crs="EPSG:3857",resampling=resamp,src_nodata=nodata,dst_nodata=np.nan)
    return out
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]; anom=d["anom"]
wnd=np.load(R/"data/nisar/nisar_windows.npz"); hh2,hv2=wnd["hh2"],wnd["hv2"]
trn=from_origin(x0,y0,20,20); crs="EPSG:32640"
def db(a): return 10*np.log10(np.clip(a,1e-6,None))
coh_w=warp(coh,trn,crs); mk_w=warp(mk.astype("float32"),trn,crs,Resampling.nearest)
hv2_w=warp(db(hv2),trn,crs); hh2_w=warp(db(hh2),trn,crs); anom_w=warp(anom,trn,crs)
valid=np.isfinite(coh_w)&(coh_w>0)
def cmap(v,stops):
    xs=np.array([s[0] for s in stops]); cs=np.array([s[1] for s in stops],dtype="float32")
    out=np.zeros(v.shape+(3,),dtype="float32")
    for i in range(3): out[...,i]=np.interp(v,xs,cs[:,i])
    return out
def save_jpg(name,rgb,alpha=None,q=91):
    a=np.clip(rgb,0,255).astype("uint8")
    Image.fromarray(a).save(W/name,quality=q,optimize=True,progressive=True)
    print(name,(W/name).stat().st_size/1e6)

stops=[(0.10,(250,236,207)),(0.18,(235,168,112)),(0.26,(196,98,58)),(0.34,(128,63,45)),(0.44,(60,52,45)),(0.55,(25,30,31)),(0.70,(12,16,18))]
save_jpg("nisar_coh.jpg",cmap(coh_w,stops),q=90)

stops2=[(-22,(12,15,16)),(-16,(45,40,36)),(-12,(110,74,53)),(-9,(190,120,74)),(-6,(240,206,166)),(-4,(252,240,215))]
save_jpg("nisar_hv.jpg",cmap(hv2_w,stops2),q=90)

stops3=[(-0.8,(31,90,110)),(-0.3,(110,160,160)),(0,(233,223,201)),(0.3,(206,130,82)),(0.8,(122,35,24))]
save_jpg("nisar_dhv.jpg",cmap(anom_w,stops3),q=88)

def st(a,lo,hi): return np.clip((a-lo)/(hi-lo),0,1)
Rc=st(hv2_w,-20,-5); Gc=st(hh2_w,-17,-3); Bc=st(coh_w,0.12,0.62)
save_jpg("nisar_comp.jpg",np.dstack([Rc**0.9*255,Gc**0.9*255,Bc**0.9*255]),q=90)

# hillshade
dems=sorted(glob.glob(str(R/"data/dem/*.tif")))
mosaic,mtr=merge(dems); mosaic=mosaic[0].astype("float32")
print("dem",mosaic.shape,mtr)
res2=60.0
l2=np.floor(l/res2)*res2; b2=np.floor(b/res2)*res2; r2=np.ceil(r/res2)*res2; t2=np.ceil(t/res2)*res2
w2=int((r2-l2)/res2); h2=int((t2-b2)/res2); tr2=from_origin(l2,t2,res2,res2)
dem=np.full((h2,w2),np.nan,dtype="float32")
reproject(mosaic,dem,src_transform=mtr,src_crs="EPSG:4326",dst_transform=tr2,dst_crs="EPSG:3857",resampling=Resampling.bilinear,dst_nodata=np.nan)
print("dem nan",np.isnan(dem).mean(),np.nanmin(dem),np.nanmax(dem))
dy,dx=np.gradient(np.nan_to_num(dem,nan=float(np.nanmedian(dem))),res2)
slope=np.pi/2-np.arctan(np.hypot(dx,dy)); aspect=np.arctan2(-dx,dy)
az=np.deg2rad(315); alt=np.deg2rad(38)
hs=np.sin(alt)*np.sin(slope)+np.cos(alt)*np.cos(slope)*np.cos(az-aspect)
hs=np.clip(hs,0,1); hs=(hs**1.1*255).astype("uint8")
Image.fromarray(hs).save(W/"hillshade.jpg",quality=82,optimize=True)
print("hill",hs.shape,hs.min(),hs.max())
meta=json.load(open(W/"meta.json")); meta["hillshade"]=[[l2,b2],[r2,b2],[r2,t2],[l2,t2]]
json.dump(meta,open(W/"meta.json","w"),ensure_ascii=False,indent=1)
print("done")