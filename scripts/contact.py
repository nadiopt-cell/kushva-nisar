from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\output")
files=[("poster_radar_ru.jpg","NISAR · RU"),("poster_radar_en.jpg","NISAR · EN"),("poster_optical_ru.jpg","Sentinel-2 · RU"),("poster_optical_en.jpg","Sentinel-2 · EN")]
thumbs=[]
for f,lab in files:
    im=Image.open(R/f); im.thumbnail((900,1260),Image.LANCZOS); thumbs.append((im,lab))
W=2*940+60; H=2*1320+120
sheet=Image.new("RGB",(W,H),(242,235,221)); d=ImageDraw.Draw(sheet)
font=ImageFont.truetype(r"E:\ai_project\30days_challenge\day14_borges\assets\fonts\IBMPlexMono-Regular.ttf",22)
for i,(im,lab) in enumerate(thumbs):
    x=30+(i%2)*940; y=30+(i//2)*1320
    sheet.paste(im,(x,y))
    d.text((x,y+1270),lab,font=font,fill=(90,80,68))
sheet.save(R/"posters_contact.jpg",quality=90,optimize=True)
for f,_ in files:
    for ext in ["png","jpg","pdf"]:
        p=R/f"{f.rsplit('.',1)[0]}.{ext}"
        print(p.name, round(p.stat().st_size/1e6,2),"MB")
print("contact", round((R/"posters_contact.jpg").stat().st_size/1e6,2),"MB")