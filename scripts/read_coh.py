import requests, io, json, time, sys
from pathlib import Path
import h5py, numpy as np
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=(R/"earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(R/"asf_kushva.json",encoding="utf-8-sig"))
url=[e["downloadUrl"] for e in js[0] if e.get("processingLevel")=="GUNW" and e["startTime"][:10]=="2026-06-20"][0]
class HTTPFile(io.RawIOBase):
    def __init__(self,url,size,tok,block=8*1024*1024):
        self.url=url; self.size=size; self.tok=tok; self.block=block; self.pos=0; self.cache={}; self.nread=0
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,off,whence=0):
        self.pos = off if whence==0 else (self.pos+off if whence==1 else self.size+off); return self.pos
    def _fetch(self,start,end):
        for a in range(6):
            try:
                r=requests.get(self.url,headers={"Authorization":f"Bearer {self.tok}","Range":f"bytes={start}-{end}"},timeout=180)
                if r.status_code in (200,206):
                    self.nread+=len(r.content); return r.content
            except Exception as e: print("retry fetch",a,type(e).__name__,flush=True)
        raise IOError("fetch failed")
    def read(self,n=-1):
        if n<0: n=self.size-self.pos
        n=min(n,self.size-self.pos)
        if n<=0: return b""
        out=[]; left=n; p=self.pos
        while left>0:
            b0=(p//self.block)*self.block; b1=min(b0+self.block-1,self.size-1)
            data=self.cache.get(b0)
            if data is None:
                data=self._fetch(b0,b1)
                if len(self.cache)>8: self.cache.clear()
                self.cache[b0]=data
            o=p-b0; take=min(left,len(data)-o); out.append(data[o:o+take]); p+=take; left-=take
        self.pos=p; return b"".join(out)
    def readinto(self,b):
        d=self.read(len(b)); b[:len(d)]=d; return len(d)
size=int(requests.get(url,headers={"Authorization":f"Bearer {tok}","Range":"bytes=0-0"},timeout=60).headers["Content-Range"].split("/")[-1])
f=HTTPFile(url,size,tok)
t0=time.time()
h=h5py.File(f,"r",rdcc_nbytes=64*1024*1024)
g=h["science/LSAR/GUNW/grids/frequencyA"]
ds=g["wrappedInterferogram/HH/coherenceMagnitude"]
x=g["wrappedInterferogram/HH/xCoordinates"][:]; y=g["wrappedInterferogram/HH/yCoordinates"][:]
print("grid",ds.shape,x[0],x[-1],y[0],y[-1],"read MB",round(f.nread/1e6,1),flush=True)
X0,X1=640000.0,686000.0; Y0,Y1=6446000.0,6504000.0
c0=int((X0-x[0])/20); c1=int((X1-x[0])/20); r0=int((y[0]-Y1)/20); r1=int((y[0]-Y0)/20)
c0=max(0,c0); r0=max(0,r0); c1=min(c1,len(x)); r1=min(r1,len(y))
print("window",r0,r1,c0,c1,flush=True)
coh=ds[r0:r1,c0:c1].astype("float32")
mk=g["wrappedInterferogram/mask"][r0:r1,c0:c1]
x0=x[c0]; y0=y[r0]
print("coh shape",coh.shape,"MB read",round(f.nread/1e6,1),"time",round(time.time()-t0,1),flush=True)
print("stats",np.nanpercentile(coh,[1,5,25,50,75,95,99]),"mask",np.unique(mk,return_counts=True),flush=True)
np.savez(R/"data/nisar/coherence.npz",coh=coh,mask=mk,x0=x0,y0=y0)
print("saved",flush=True)