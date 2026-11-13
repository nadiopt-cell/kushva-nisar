import numpy as np
from pathlib import Path
from PIL import Image
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
img=np.asarray(Image.open(R/"web/data/s2_post.jpg")).astype("float32")/255
ext=[642360,682280,6451360,6499680]
CX0,CX1,CY0,CY1=656000,668000,6480000,6495000
c0=int((CX0-642360)/10); c1=int((CX1-642360)/10); r0=int((6499680-CY1)/10); r1=int((6499680-CY0)/10)
crop=img[r0:r1,c0:c1]
# local contrast (CLAHE-like): divide by heavy blur
from scipy import ndimage
for i in range(3):
    ch=crop[:,:,i]; bg=ndimage.gaussian_filter(ch,25); crop[:,:,i]=np.clip((ch-bg)*3+0.5,0,1)
fig,ax=plt.subplots(1,2,figsize=(16,7),dpi=100)
ax[0].imshow(img[r0:r1,c0:c1],extent=[CX0,CX1,CY0,CY1]); ax[0].set_title("post raw")
ax[1].imshow(crop,extent=[CX0,CX1,CY0,CY1]); ax[1].set_title("post high-pass")
plt.tight_layout(); plt.savefig(R/"build/north_zoom.png",dpi=100)
print("saved")