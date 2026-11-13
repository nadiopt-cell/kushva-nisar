import numpy as np
from PIL import Image
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
opt=Image.open(R/"web/data/s2_pre.jpg").convert("RGB")
hill=Image.open(R/"web/data/hillshade.png").convert("RGBA").resize(opt.size,Image.LANCZOS)
base=np.asarray(opt).astype("float32"); ov=np.asarray(hill).astype("float32")
a=ov[...,3:4]/255.0
out=base*(1-a)+ov[...,:3]*a
Image.fromarray(np.clip(out,0,255).astype("uint8")).save(R/"build/hill_overlay_preview.jpg",quality=88)
print("ok")