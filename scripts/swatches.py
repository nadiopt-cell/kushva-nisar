from PIL import Image
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
for src,dst in [("s2_pre.jpg","swatch_pre.jpg"),("s2_post.jpg","swatch_post.jpg"),("nisar_coh.jpg","swatch_nisar.jpg"),("hillshade.jpg","swatch_hill.jpg")]:
    im=Image.open(R/src); w,h=im.size
    s=min(w,h)//6
    im.crop((w//2-s,h//2-s,w//2+s,h//2+s)).resize((120,120)).save(R/dst,quality=90)
# contour swatch: crop coherence around the track and draw contour? simple: use track area crop
im=Image.open(R/"nisar_coh.jpg"); w,h=im.size
im.crop((int(w*0.30),int(h*0.28),int(w*0.30)+260,int(h*0.28)+260)).resize((120,120)).save(R/"swatch_contour.jpg",quality=90)
print("ok")