import numpy as np
from pathlib import Path
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
sm=ndimage.uniform_filter(coh,size=5)
fig,ax=plt.subplots(figsize=(9,11),dpi=100)
ax.imshow(sm,cmap="magma",vmin=0.12,vmax=0.62)
ax.set_title("NISAR L-band coherence 20.06 -> 02.07.2026 (full window)")
plt.tight_layout(); plt.savefig(R/"build/coh_full.png",dpi=100)
print("saved")