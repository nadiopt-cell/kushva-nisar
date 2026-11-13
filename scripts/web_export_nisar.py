import numpy as np, rasterio, json
from pathlib import Path
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.transform import from_origin
from PIL import Image
R=Path(r"E:\ai_project\30days_challenge\day14_borges"); W=R/"web/data"
AOI=(59.45,58.18,60.10,58.60)
res=20.0
l,b,r,t=transform_bounds("EPSG:4326","EPSG:3857",*AOI)
l=np.floor(l/res)*res; b=np.floor(b/res)*res; r=np.ceil(r/res)*res; t=np.ceil(t/res)*res
w=int((r-l)/res); h=int((t-b)/res); tr=from_origin(l,t,res,res)
print("grid",w,h)
def warp(src,srctr,srccrs,resamp=Resampling.bilinear,nodata=None):
    out=np.full((h,w),np.nan,dtype="float32")
    reproject(src,out,src_transform=srctr,src_crs=srccrs,dst_transform=tr,dst_crs="EPSG:3857",resampling=resamp,src_nodata=nodata,dst_nodata=np.nan)
    return out
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; mk=c["mask"]; x0=c["x0"]; y0=c["y0"]
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]; anom=d["anom"]
wnd=np.load(R/"data/nisar/nisar_windows.npz"); hh1,hv1,hh2,hv2=wnd["hh1"],wnd["hv1"],wnd["hh2"],wnd["hv2"]
trn=from_origin(x0,y0,20,20); crs="EPSG:32640"
def db(a): return 10*np.log10(np.clip(a,1e-6,None))
coh_w=warp(coh,trn,crs); mk_w=warp(mk.astype("float32"),trn,crs,Resampling.nearest)
hv2_w=warp(db(hv2),trn,crs); hh2_w=warp(db(hh2),trn,crs); dhv_w=warp(dhv,trn,crs); anom_w=warp(anom,trn,crs)
ratio_w=hv2_w-hh2_w
valid=np.isfinite(coh_w)&(coh_w>0)&(mk_w>10)
print("valid frac",valid.mean())

def cmap(x,stops):
    xs=np.array([s[0] for s in stops]); cs=np.array([s[1] for s in stops],dtype="float32")
    out=np.zeros(x.shape+(3,),dtype="float32")
    for i in range(3): out[...,i]=np.interp(x,xs,cs[:,i])
    return out
def save_rgba(name,rgb,alpha):
    a=np.dstack([np.clip(rgb,0,255).astype("uint8"),np.clip(alpha,0,255).astype("uint8")])
    Image.fromarray(a,"RGBA").save(W/name,optimize=True)
    print(name,a.shape)

# coherence: low=bright copper, high=dark ink
stops=[(0.10,(250,236,207)),(0.18,(235,168,112)),(0.26,(196,98,58)),(0.34,(128,63,45)),(0.44,(60,52,45)),(0.55,(25,30,31)),(0.70,(12,16,18))]
x=np.clip((coh_w-0.10)/(0.70-0.10),0,1)
rgb=cmap(x,stops)
save_rgba("nisar_coh.png",rgb,np.where(valid,242,0))

# HV after: dark->copper->cream
stops2=[(-22,(12,15,16)),(-16,(45,40,36)),(-12,(110,74,53)),(-9,(190,120,74)),(-6,(240,206,166)),(-4,(252,240,215))]
x2=np.clip((hv2_w+22)/18,0,1); rgb2=cmap(x2,stops2)
save_rgba("nisar_hv.png",rgb2,np.where(valid,238,0))

# dHV anomaly diverging
stops3=[(-0.8,(31,90,110)),(-0.3,(110,160,160)),(0,(233,223,201)),(0.3,(206,130,82)),(0.8,(122,35,24))]
x3=np.clip((anom_w+0.8)/1.6,0,1); rgb3=cmap(x3,stops3)
save_rgba("nisar_dhv.png",rgb3,np.where(valid,235,0))

# composite R=HV G=HH B=coherence
def st(a,lo,hi): return np.clip((a-lo)/(hi-lo),0,1)
Rc=st(hv2_w,-20,-5); Gc=st(hh2_w,-17,-3); Bc=st(coh_w,0.12,0.62)
rgb4=np.dstack([Rc**0.9*255,Gc**0.9*255,Bc**0.9*255])
save_rgba("nisar_comp.png",rgb4,np.where(valid,238,0))

# hillshade
import glob
dems=sorted(glob.glob(str(R/"data/dem/*.tif")))
arrs=[]; bounds=[]
for p in dems:
    with rasterio.open(p) as ds:
        arrs.append(ds.read(1).astype("float32")); bounds.append(ds.bounds); dtr=ds.transform; dcrs=ds.crs
print("dem tiles",len(dems),bounds[0])
# mosaic onto 32640 coarse grid then hillshade
H,Wd=arrs[0].shape
mosaic=np.zeros((H,Wd*len(arrs)),dtype="float32")
for i,a in enumerate(arrs): mosaic[:,i*Wd:(i+1)*Wd]=a
# tiles are adjacent E059,E060
from rasterio.transform import Affine
mtr=Affine(dtr.a,dtr.b,bounds[0].left,dtr.d,dtr.f,bounds[0].top)
# warp DEM to 3857 at 60m
res2=60.0
l2=np.floor(l/res2)*res2; b2=np.floor(b/res2)*res2; r2=np.ceil(r/res2)*res2; t2=np.ceil(t/res2)*res2
w2=int((r2-l2)/res2); h2=int((t2-b2)/res2); tr2=from_origin(l2,t2,res2,res2)
dem=np.full((h2,w2),np.nan,dtype="float32")
reproject(mosaic,dem,src_transform=mtr,src_crs=dcrs,dst_transform=tr2,dst_crs="EPSG:3857",resampling=Resampling.bilinear,dst_nodata=np.nan)
# hillshade
dy,dx=np.gradient(np.nan_to_num(dem,nan=np.nanmedian(dem)),res2)
slope=np.pi/2-np.arctan(np.hypot(dx,dy)); aspect=np.arctan2(-dx,dy)
az=np.deg2rad(315); alt=np.deg2rad(38)
hs=np.sin(alt)*np.sin(slope)+np.cos(alt)*np.cos(slope)*np.cos(az-aspect)
hs=np.clip(hs,0,1); hs=(hs**1.1*255).astype("uint8")
Image.fromarray(hs).save(W/"hillshade.jpg",quality=82,optimize=True)
print("hill",hs.shape,hs.min(),hs.max())
# meta
meta=json.load(open(W/"meta.json"))
meta["rasters"]["nisar"]=[[l,b],[r,b],[r,t],[l,t]]
meta["hillshade"]=[[l2,b2],[r2,b2],[r2,t2],[l2,t2]]
json.dump(meta,open(W/"meta.json","w"),ensure_ascii=False,indent=1)
print("meta ok", (W/"nisar_coh.png").stat().st_size/1e6)