import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
for n in ["pre","post"]:
    im=Image.open(R/f"s2_{n}.jpg").convert("RGB")
    a=np.asarray(im).astype("float32")/255
    lum=(a*np.array([0.299,0.587,0.114])).sum(2,keepdims=True)
    sat=0.58
    b=lum+(a-lum)*sat
    # warm tint in shadows, cool highlights
    b=b*np.array([1.02,0.995,0.955])
    b=np.clip(b,0,1)**1.02
    Image.fromarray((b*255).astype("uint8")).save(R/f"s2_{n}_muted.jpg",quality=88,optimize=True)
print("ok")