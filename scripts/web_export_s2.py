import numpy as np, rasterio, json
from pathlib import Path
from rasterio.warp import reproject, Resampling, transform_bounds, calculate_default_transform
from rasterio.transform import from_origin
from PIL import Image
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
W=Path(R/"web/data"); W.mkdir(parents=True,exist_ok=True)
AOI=(59.45,58.18,60.10,58.60)
def dst_grid(res=20.0):
    l,b,r,t=transform_bounds("EPSG:4326","EPSG:3857",*AOI)
    l=np.floor(l/res)*res; b=np.floor(b/res)*res; r=np.ceil(r/res)*res; t=np.ceil(t/res)*res
    w=int((r-l)/res); h=int((t-b)/res)
    return l,b,r,t,w,h,from_origin(l,t,res,res)
def warp(src,src_tr,src_crs,g,resampling=Resampling.bilinear,nodata=None):
    l,b,r,t,w,h,tr=g
    out=np.zeros((h,w),dtype="float32")
    reproject(src,out,src_transform=src_tr,src_crs=src_crs,dst_transform=tr,dst_crs="EPSG:3857",
              resampling=resampling,src_nodata=nodata,dst_nodata=0)
    return out
def rd(n,b):
    with rasterio.open(R/f"data/s2/{n}_{b}.tif") as ds: return ds.read(1).astype("float32"),ds.transform,ds.crs

def stretch(a,lo=2,hi=98):
    v=a[(a>0)&np.isfinite(a)]
    p1,p2=np.percentile(v,[lo,hi]); x=np.clip((a-p1)/(p2-p1),0,1)
    return x

def srgb(x,gam=1.0):
    x=np.clip(x,0,1)**gam
    return (255*x+0.5).astype("uint8")

g=dst_grid(20.0)
l,b,r,t,w,h,tr=g
print("grid",w,h)
meta={"rasters":{},"aoi":[l,b,r,t]}
for name in ["pre","post"]:
    arrs={}
    for band in ["swir22","nir","red","scl"]:
        a,tt,cc=rd(name,band)
        arrs[band]=warp(a,tt,cc,g,Resampling.nearest if band=="scl" else Resampling.bilinear)
    def st(a,lo=1.5,hi=98.5):
        v=a[(a>0)&np.isfinite(a)]
        p1,p2=np.percentile(v,[lo,hi]); return np.clip((a-p1)/(p2-p1),0,1)
    Rc=st(arrs["swir22"],1,99); Gc=st(arrs["nir"],2,98); Bc=st(arrs["red"],2,98)
    # gentle filmic tone + slight desat
    rgb=np.dstack([Rc,Gc,Bc])
    lum=(rgb*np.array([0.299,0.587,0.114])).sum(2,keepdims=True)
    rgb=lum+(rgb-lum)*0.92
    rgb=np.clip(rgb,0,1)**0.95
    img=srgb(rgb)
    Image.fromarray(img).save(W/f"s2_{name}.jpg",quality=88,optimize=True,progressive=True)
    print(name,img.shape)
    # swatch
    cy,cx=h//2,w//2
    Image.fromarray(img[cy-90:cy+90,cx-90:cx+90]).save(W/f"swatch_{name}.jpg",quality=90)
    meta["rasters"][f"s2_{name}"]=[[l,b],[r,b],[r,t],[l,t]]

# save meta
json.dump(meta,open(W/"meta.json","w"),ensure_ascii=False,indent=1)
print("saved",w,h, (W/"s2_pre.jpg").stat().st_size/1e6,"MB")