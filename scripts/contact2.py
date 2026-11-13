from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\output")
files=[("poster_radar_ru.jpg","NISAR · RU"),("poster_radar_en.jpg","NISAR · EN"),("poster_optical_ru.jpg","Sentinel-2 · RU"),("poster_optical_en.jpg","Sentinel-2 · EN")]
CW,CH=1040,1460
W=2*CW+120; H=2*CH+120
sheet=Image.new("RGB",(W,H),(242,235,221)); d=ImageDraw.Draw(sheet)
f=ImageFont.truetype(r"E:\ai_project\30days_challenge\day14_borges\assets\fonts\IBMPlexMono-Regular.ttf",24)
for i,(fn,lab) in enumerate(files):
    im=Image.open(R/fn).convert("RGB")
    im=ImageOps.contain(im,(CW-80,CH-110),Image.LANCZOS)
    x=40+(i%2)*CW; y=30+(i//2)*CH
    # center horizontally in cell
    px=x+(CW-80-im.width)//2; py=y
    d.rectangle([px-1,py-1,px+im.width,py+im.height],outline=(180,165,145),width=1)
    sheet.paste(im,(px,py))
    d.text((x+10,py+im.height+18),lab,font=f,fill=(90,80,68))
sheet.save(R/"posters_contact.jpg",quality=91,optimize=True)
print(sheet.size,(R/"posters_contact.jpg").stat().st_size/1e6)