import numpy as np
from pathlib import Path
from scipy import ndimage
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
w=np.load(R/"data/nisar/nisar_windows.npz")
hh1,hv1,hh2,hv2=w["hh1"],w["hv1"],w["hh2"],w["hv2"]
# gradient-based shift estimate on log amplitude, central crop
a=np.log10(np.clip(hh1,1e-6,None)); b=np.log10(np.clip(hh2,1e-6,None))
a=ndimage.gaussian_filter(a,2); b=ndimage.gaussian_filter(b,2)
A=a[800:2000,600:1800]; B=b[800:2000,600:1800]
A=A-A.mean(); B=B-B.mean()
from numpy.fft import fft2,ifft2
F=ifft2(fft2(A)*np.conj(fft2(B))); F=np.fft.fftshift(np.abs(F))
i=np.unravel_index(np.argmax(F),F.shape); print("peak",i,"center",(F.shape[0]//2,F.shape[1]//2))
print("shift row,col",i[0]-F.shape[0]//2, i[1]-F.shape[1]//2)
print("corr",F.max()/F.mean())