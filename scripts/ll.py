from pyproj import Transformer
tr=Transformer.from_crs(32640,4326,always_xy=True)
for x,y in [(660000,6470000),(660000,6465000),(660000,6480000),(659000,6475000),(663000,6453000),(655000,6488000),(661200,6467000)]:
    lon,lat=tr.transform(x,y); print(x,y,"->",round(lon,4),round(lat,4))
print("Kushva",tr.transform(59.7592,58.2986)) if False else None
tr2=Transformer.from_crs(4326,32640,always_xy=True)
print("Kushva utm",tr2.transform(59.7592,58.2986))
print("Malaya Laya utm",tr2.transform(59.85,58.15))