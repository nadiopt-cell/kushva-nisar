import requests, json, sys
from pathlib import Path
import numpy as np, rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.windows import from_bounds
from rasterio.transform import from_origin

ROOT=Path(r"E:\ai_project\30days_challenge\day14_borges")
OUT=ROOT/"data"/"s2"; OUT.mkdir(parents=True,exist_ok=True)
AOI=(59.45,58.18,60.10,58.60)  # lon/lat
DST_CRS="EPSG:32640"
RES=10.0
left,bottom,right,top=transform_bounds("EPSG:4326",DST_CRS,*AOI)
left=np.floor(left/RES)*RES; bottom=np.floor(bottom/RES)*RES
right=np.ceil(right/RES)*RES; top=np.ceil(top/RES)*RES
W=int(round((right-left)/RES)); H=int(round((top-bottom)/RES))
transform=from_origin(left,top,RES,RES)
print("grid",W,H,left,bottom,right,top)
BANDS=["swir22","swir16","nir","red","green","blue","scl"]

def find(date, tiles):
    body={"collections":["sentinel-2-l2a"],"bbox":list(AOI),
          "datetime":f"{date}T00:00:00Z/{date}T23:59:59Z","limit":20}
    r=requests.post("https://earth-search.aws.element84.com/v1/search",json=body,timeout=90)
    r.raise_for_status()
    fs={f["id"]:f for f in r.json()["features"]}
    out=[]
    for t in tiles:
        cand=[k for k in fs if t in k]
        if not cand: print("MISSING tile",t,date); continue
        out.append(fs[sorted(cand)[0]])
    return out

def build(name,date,tiles):
    feats=find(date,tiles)
    print(name,date,[f["id"] for f in feats])
    arrs={b:np.full((H,W),0 if b=="scl" else np.nan,dtype="float32" if b!="scl" else "uint8") for b in BANDS}
    for f in feats:
        print(" ",f["id"],"cloud",f["properties"].get("eo:cloud_cover"))
        for b in BANDS:
            href=f["assets"][b]["href"]
            with rasterio.open("/vsicurl/"+href) as ds:
                bb=transform_bounds(DST_CRS,ds.crs,left,bottom,right,top)
                win=from_bounds(*bb,ds.transform)
                win=win.round_offsets().round_lengths()
                win=win.intersection(rasterio.windows.Window(0,0,ds.width,ds.height))
                if win.width<=0 or win.height<=0: continue
                src=ds.read(1,window=win)
                src_tr=ds.window_transform(win)
                dst=np.full((H,W),np.nan,dtype="float32")
                reproject(src,dst,src_transform=src_tr,src_crs=ds.crs,
                          dst_transform=transform,dst_crs=DST_CRS,
                          resampling=Resampling.nearest if b=="scl" else Resampling.bilinear,
                          src_nodata=0,dst_nodata=None)
                m=np.isfinite(dst)&(dst!=0)
                if b=="scl":
                    m=(dst>0)&(dst<12)
                    tmp=arrs[b].astype("float32"); tmp[m]=dst[m]; arrs[b]=tmp.astype("uint8")
                else:
                    arrs[b][m]=dst[m]
    for b in BANDS:
        a=arrs[b]
        prof=dict(driver="GTiff",height=H,width=W,count=1,
                  dtype="uint8" if b=="scl" else "float32",crs=DST_CRS,transform=transform,
                  compress="deflate",tiled=True,blockxsize=512,blockysize=512)
        with rasterio.open(OUT/f"{name}_{b}.tif","w",**prof) as d: d.write(a,1)
    print("saved",name)

if __name__=="__main__":
    build("pre","2026-05-21",["40VFK","41VLE"])
    build("post","2026-07-28",["40VFK","41VLE"])