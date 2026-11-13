import h5py, numpy as np
from pathlib import Path
p=next(Path(r"E:\ai_project\30days_challenge\day14_borges\data\nisar").glob("*20260620*.h5"))
print(p.name, p.stat().st_size/1e9)
f=h5py.File(p,"r")
def show(name,obj):
    if isinstance(obj,h5py.Dataset) and obj.ndim<=2:
        print("D",name,obj.shape,obj.dtype, dict(obj.attrs).get("units",""))
f.visititems(show)
print("--- grids attrs")
g=f["science/LSAR/GCOV/grids/frequencyA"]
for k,v in g.attrs.items(): print(k,v)
print("--- projection")
for k in g.keys():
    if "projection" in k.lower() or "coordinate" in k.lower(): print(k, g[k].shape if hasattr(g[k],"shape") else "")
print(list(g.keys()))