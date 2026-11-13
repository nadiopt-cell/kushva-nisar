import numpy as np, rasterio
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"].astype("float32")
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]; x0=d["x0"]; y0=d["y0"]
print("dnbr",np.nanmin(dnbr),np.nanmax(dnbr),dnbr.shape)
tr10=from_origin(642360,6499680,10,10); tr20=from_origin(x0,y0,20,-20)
print(tr10,tr20,dhv.shape)
out=np.zeros(dhv.shape,dtype="float32")
reproject(dnbr,out,src_transform=tr10,src_crs="EPSG:32640",dst_transform=tr20,dst_crs="EPSG:32640",resampling=Resampling.average)
print("out",out.min(),out.max(),(out>0).mean())