import numpy as np
from pathlib import Path
from scipy import ndimage
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
w=np.load(R/"data/nisar/nisar_windows.npz")
hh1,hv1,hh2,hv2=w["hh1"],w["hv1"],w["hh2"],w["hv2"]
d=np.load(R/"data/nisar/deltas.npz"); dhv=d["dhv"]
mask=np.load(R/"data/nisar/main_mask20.npy")
# fill nan
a=np.log10(np.clip(hh1,1e-6,None)); b=np.log10(np.clip(hh2,1e-6,None))
a=np.nan_to_num(a,nan=np.nanmedian(a)); b=np.nan_to_num(b,nan=np.nanmedian(b))
a=ndimage.gaussian_filter(a,3); b=ndimage.gaussian_filter(b,3)
A=a[700:2100,500:1900]; B=b[700:2100,500:1900]
A-=A.mean(); B-=B.mean()
F=np.fft.ifft2(np.fft.fft2(A)*np.conj(np.fft.fft2(B)))
F=np.fft.fftshift(np.abs(F))
i=np.unravel_index(np.argmax(F),F.shape); sh=(i[0]-F.shape[0]//2, i[1]-F.shape[1]//2)
print("shift (row,col) px",sh,"m",(sh[0]*20,sh[1]*20),"peak ratio",F.max()/np.median(F))
# distance profile
dist=ndimage.distance_transform_edt(~mask)
for r in [0,1,2,3,4,5,7,10,15,20,30]:
    sel=(dist>=r*1)&(dist<(r+1)*1)
    if sel.sum(): print("dist",r,"px",sel.sum(),"dhv",round(float(np.nanmean(dhv[sel])),3))
# high-pass variants
for size in [11,25,51,101]:
    bg=ndimage.uniform_filter(dhv,size=size)
    an=dhv-bg
    print("hp",size,"track",round(float(np.nanmean(an[mask])),3),"buf",round(float(np.nanmean(an[(dist>6)&(dist<20)])),3))