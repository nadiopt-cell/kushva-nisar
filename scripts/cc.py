import numpy as np
from pathlib import Path
from scipy import ndimage
import rasterio
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
idx=np.load(R/"data/s2/indices.npz"); dnbr=idx["dnbr"]; ndvi=idx["ndvi_pre"]; cloud=idx["cloud"]
m=(dnbr>0.20)&(ndvi>0.5)&(~cloud)
m=ndimage.binary_opening(m,iterations=2); m=ndimage.binary_closing(m,iterations=3)
lab,n=ndimage.label(m)
sizes=ndimage.sum(m,lab,range(1,n+1))
objs=ndimage.find_objects(lab)
print("components",n)
rows=[]
for i,(s,o) in enumerate(zip(sizes,objs)):
    if s<300: continue
    h=o[0].stop-o[0].start; w=o[1].stop-o[1].start
    elong=max(h,w)/max(1,min(h,w))
    rows.append((int(s),h,w,round(elong,1),o[0].start,o[1].start,o[0].stop,o[1].stop,i+1))
rows.sort(reverse=True)
for r in rows[:15]: print(r)
np.save(R/"data/s2/dnbr_mask.npy",m)