import requests, io, json
from pathlib import Path
import h5py
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
tok=(R/"earthdata.txt").read_text(encoding="utf-8").strip()
js=json.load(open(R/"asf_kushva.json",encoding="utf-8-sig"))
url=[e["downloadUrl"] for e in js[0] if e.get("processingLevel")=="GUNW" and e["startTime"][:10]=="2026-06-20"][0]
class HTTPFile(io.RawIOBase):
    def __init__(self,url,size,tok,block=4*1024*1024):
        self.url=url; self.size=size; self.tok=tok; self.block=block; self.pos=0; self.cache={}
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,off,whence=0):
        if whence==0: self.pos=off
        elif whence==1: self.pos+=off
        else: self.pos=self.size+off
        return self.pos
    def _fetch(self,start,end):
        for a in range(5):
            r=requests.get(self.url,headers={"Authorization":f"Bearer {self.tok}","Range":f"bytes={start}-{end}"},timeout=120)
            if r.status_code in (200,206): return r.content
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
                data=self._fetch(b0,b1); self.cache={b0:data} if len(self.cache)>20 else self.cache; self.cache[b0]=data
            o=p-b0; take=min(left,len(data)-o); out.append(data[o:o+take]); p+=take; left-=take
        self.pos=p
        return b"".join(out)
    def readinto(self,b):
        d=self.read(len(b)); b[:len(d)]=d; return len(d)
size=int(requests.get(url,headers={"Authorization":f"Bearer {tok}","Range":"bytes=0-0"},timeout=60).headers["Content-Range"].split("/")[-1])
print("size",size/1e9)
f=HTTPFile(url,size,tok)
h=h5py.File(f,"r")
def show(name,obj):
    if isinstance(obj,h5py.Dataset): print("D",name,obj.shape,obj.dtype,obj.chunks)
h.visititems(show)