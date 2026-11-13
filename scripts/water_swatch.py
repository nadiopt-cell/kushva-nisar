from PIL import Image, ImageDraw
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
im=Image.new("RGB",(160,160),(7,28,34)); d=ImageDraw.Draw(im)
for k in range(4):
    y=40+k*24
    pts=[(10,y+6),(40,y-4),(70,y+6),(100,y-4),(130,y+6),(150,y-2)]
    d.line(pts,fill=(120,175,180),width=3)
im.save(R/"swatch_water.jpg",quality=92)
print("ok")