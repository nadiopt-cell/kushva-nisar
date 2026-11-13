import h5py, numpy as np
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

R=Path(r"E:\ai_project\30days_challenge\day14_borges")
files=sorted((R/"data/nisar").glob("*.h5"))
pre=[p for p in files if "20260620" in p.name][0]
post=[p for p in files if "20260702" in p.name][0]
X0,X1=640000.0,686000.0
Y0,Y1=6446000.0,6504000.0

def read(p):
    f=h5py.File(p,"r"); g=f["science/LSAR/GCOV/grids/frequencyA"]
    x=g["xCoordinates"][:]; y=g["yCoordinates"][:]
    c0=int((X0-x[0])/20); c1=int((X1-x[0])/20)
    r0=int((y[0]-Y1)/20); r1=int((y[0]-Y0)/20)
    c0=max(c0,0); r0=max(r0,0); c1=min(c1,len(x)); r1=min(r1,len(y))
    hh=g["HHHH"][r0:r1,c0:c1].astype("float32")
    hv=g["HVHV"][r0:r1,c0:c1].astype("float32")
    mk=g["mask"][r0:r1,c0:c1]
    x0=x[c0]; y0=y[r0]
    f.close()
    return hh,hv,mk,x0,y0

hh1,hv1,mk1,x0,y0=read(pre); hh2,hv2,mk2,_,_=read(post)
print("shapes",hh1.shape, "x0,y0",x0,y0)
print("mask1",np.unique(mk1,return_counts=True),"mask2",np.unique(mk2,return_counts=True))
for name,a in [("hh1",hh1),("hv1",hv1),("hh2",hh2),("hv2",hv2)]:
    v=a[np.isfinite(a)&(a>0)]
    print(name,"n",v.size,"p1/50/99",np.percentile(v,[1,50,99]))
np.savez_compressed(R/"data/nisar/nisar_windows.npz",hh1=hh1,hv1=hv1,mk1=mk1,hh2=hh2,hv2=hv2,mk2=mk2,x0=x0,y0=y0)

valid=(mk1==1)&(mk2==1)&(hh1>0)&(hv1>0)&(hh2>0)&(hv2>0)
print("valid",valid.mean())
for nm,arr in [("HV1",hv1),("HV2",hv2)]:
    d=10*np.log10(np.clip(arr,1e-6,None)); print(nm,np.percentile(d[valid],[2,25,50,75,98]))
dhv=10*np.log10(np.clip(hv2,1e-6,None))-10*np.log10(np.clip(hv1,1e-6,None))
dhh=10*np.log10(np.clip(hh2,1e-6,None))-10*np.log10(np.clip(hh1,1e-6,None))
print("dhv",np.percentile(dhv[valid],[1,2,5,25,50,75,95,98,99]))
print("dhh",np.percentile(dhh[valid],[1,2,5,25,50,75,95,98,99]))

fig,ax=plt.subplots(1,4,figsize=(22,7),dpi=80)
def show(a,title,cm="magma",pct=(2,98)):
    v=a[valid]; lo,hi=np.percentile(v,pct); im=ax[ax_i].imshow(a,cmap=cm,vmin=lo,vmax=hi); ax[ax_i].set_title(title); ax[ax_i].axis("off")
ax_i=0
show(10*np.log10(np.clip(hv1,1e-6,None)),"HV pre dB")
ax_i=1; show(10*np.log10(np.clip(hv2,1e-6,None)),"HV post dB")
ax_i=2; show(dhv,"dHV dB",cm="RdBu_r",pct=(1,99))
ax_i=3; show(dhh,"dHH dB",cm="RdBu_r",pct=(1,99))
plt.tight_layout(); plt.savefig(R/"build/nisar_windows.png",dpi=80)
print("saved")