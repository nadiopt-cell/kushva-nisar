import numpy as np
from PIL import Image
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
hs=np.asarray(Image.open(R/"hillshade.jpg").convert("L")).astype("float32")/255
# shadows: black with alpha; highlights: white with subtle alpha
alpha=np.clip((0.58-hs)*1.5,0,0.62)
hi=np.clip((hs-0.62)*0.7,0,0.12)
a=np.maximum(alpha,hi)
rgb=np.zeros(hs.shape+(3,),dtype="float32")
rgb[...,:]=0
mask=hs>0.62
rgb[mask]=255
rgba=np.dstack([rgb,np.clip(a*255,0,255)]).astype("uint8")
Image.fromarray(rgba,"RGBA").save(R/"hillshade.png",optimize=True)
print("saved",rgba.shape,(R/"hillshade.png").stat().st_size/1e6)