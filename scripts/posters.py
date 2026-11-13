from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, rasterio
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
OUT=R/"output"; OUT.mkdir(exist_ok=True)
F=R/"assets/fonts"
SERIF=str(F/"CormorantGaramond.ttf"); SERIF_I=str(F/"CormorantGaramond-Italic.ttf")
SANS=str(F/"Inter.ttf"); MONO=str(F/"IBMPlexMono-Regular.ttf"); MONO_M=str(F/"IBMPlexMono-Medium.ttf")

CW,CH=3000,4200
IX,IY,IW,IH=300,610,2400,3000
X0,X1,Y0,Y1=653000.0,669000.0,6462000.0,6482000.0

def font(path,size,weight=None):
    f=ImageFont.truetype(path,size)
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f

def paper():
    rng=np.random.default_rng(7)
    base=np.array([242,235,221],dtype="float32")
    noise=rng.normal(0,2.2,(CH,CW,1))
    yy=np.linspace(-1,1,CH)[:,None,None]
    vign=np.clip(1-0.035*(yy**2),0,1)
    a=np.clip(base+noise,0,255)*vign
    return Image.fromarray(a.astype("uint8"),"RGB")

def stretch(a,lo=1.5,hi=98.5):
    v=a[(a>0)&np.isfinite(a)]
    p1,p2=np.percentile(v,[lo,hi]); return np.clip((a-p1)/(p2-p1),0,1)

def optical_img():
    def rd(b):
        with rasterio.open(R/f"data/s2/post_{b}.tif") as ds:
            c0=int((X0-642360)/10); c1=int((X1-642360)/10)
            r0=int((6499680-Y1)/10); r1=int((6499680-Y0)/10)
            return ds.read(1,window=((r0,r1),(c0,c1))).astype("float32")
    Rc=stretch(rd("swir22"),1,99); Gc=stretch(rd("nir"),2,98); Bc=stretch(rd("red"),2,98)
    rgb=np.dstack([Rc,Gc,Bc])
    lum=(rgb*np.array([0.299,0.587,0.114])).sum(2,keepdims=True)
    rgb=lum+(rgb-lum)*0.86
    rgb=np.clip(rgb,0,1)**0.98
    im=Image.fromarray((rgb*255).astype("uint8"),"RGB").resize((IW,IH),Image.LANCZOS)
    return im

def radar_img():
    c=np.load(R/"data/nisar/coherence.npz"); coh=c["coh"]; x0=c["x0"]; y0=c["y0"]
    c0=int((X0-x0)/20); c1=int((X1-x0)/20); r0=int((y0-Y1)/20); r1=int((y0-Y0)/20)
    a=coh[r0:r1,c0:c1]
    stops=[(0.10,(250,236,207)),(0.18,(235,168,112)),(0.26,(196,98,58)),(0.34,(128,63,45)),(0.44,(60,52,45)),(0.55,(25,30,31)),(0.70,(12,16,18))]
    xs=np.array([s[0] for s in stops]); cs=np.array([s[1] for s in stops],dtype="float32")
    out=np.zeros(a.shape+(3,),dtype="float32")
    for i in range(3): out[...,i]=np.interp(a,xs,cs[:,i])
    # gentle local contrast + grain
    im=Image.fromarray(out.astype("uint8"),"RGB").resize((IW,IH),Image.LANCZOS)
    rng=np.random.default_rng(3)
    arr=np.asarray(im).astype("float32")+rng.normal(0,2.0,(IH,IW,1))
    im=Image.fromarray(np.clip(arr,0,255).astype("uint8"),"RGB")
    return im

def tracked(draw,xy,text,fnt,tracking,fill):
    x,y=xy
    for ch in text:
        draw.text((x,y),ch,font=fnt,fill=fill)
        x+=draw.textlength(ch,font=fnt)+tracking
    return x

def wrap(draw,text,fnt,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=fnt)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def compose(kind,lang,im):
    bg=paper(); d=ImageDraw.Draw(bg)
    ink=(20,18,15); muted=(110,98,82); copper=(194,90,50); dim=(138,123,102)
    f_kick=font(MONO,23); f_title=font(SERIF,118,600); f_title_i=font(SERIF_I,118,600)
    f_sub=font(SANS,33,450); f_cap1=font(MONO_M,21); f_cap=font(SANS,29,420)
    f_cred=font(MONO,17); f_small=font(MONO,17)
    # kicker
    tracked(d,(200,150),"#30DAYMAPCHALLENGE 2026  ·  DAY 14 — BORGESIAN MAP",f_kick,1.6,muted)
    # title
    if lang=="ru":
        d.text((200,205),"Карта, которая",font=f_title,fill=ink)
        y=205+112
        x=200
        d.text((x,y),"почти",font=f_title_i,fill=copper); x+=d.textlength("почти ",font=f_title_i)
        d.text((x,y),"стала территорией",font=f_title,fill=ink)
        sub="Крупный ветровал + NISAR · Кушва, 22 июня 2026"
    else:
        d.text((200,205),"The Map That",font=f_title,fill=ink)
        y=205+112; x=200
        d.text((x,y),"Almost",font=f_title_i,fill=copper); x+=d.textlength("Almost ",font=f_title_i)
        d.text((x,y),"Became the Territory",font=f_title,fill=ink)
        sub="A major windthrow + NISAR · Kushva, 22 June 2026"
    d.text((200,470),sub,font=f_sub,fill=(59,52,43))
    # rule
    d.line([(200,545),(2800,545)],fill=(201,187,166),width=2)
    d.line([(200,545),(360,545)],fill=copper,width=5)
    # stats colophon
    f_num=font(SERIF,58,600); f_num2=font(SERIF,44,600); f_date=font(MONO,18)
    stats=[("29 КМ" if lang=="ru" else "29 KM",f_num),("≥510 ГА" if lang=="ru" else "≥510 HA",f_num2),("22.06.2026" if lang=="ru" else "22 JUN 2026",f_date)]
    yy=150
    for txt,fnt in stats:
        w=d.textlength(txt,font=fnt)
        d.text((2800-w,yy),txt,font=fnt,fill=ink if fnt is not f_date else muted)
        yy+= 66 if fnt is f_num else (54 if fnt is f_num2 else 30)
    # image
    bg.paste(im,(IX,IY))
    d.rectangle([IX-1,IY-1,IX+IW,IY+IH],outline=(30,26,21),width=2)
    # scale bar (5 km)
    bar=IW*(5000/(X1-X0)); sx=IX+70; sy=IY+IH-80
    d.line([(sx,sy),(sx+bar,sy)],fill=(255,248,232),width=5)
    for xx in [sx,sx+bar/2,sx+bar]:
        d.line([(xx,sy-12),(xx,sy+12)],fill=(255,248,232),width=3)
    d.text((sx,sy-40),"5 км" if lang=="ru" else "5 km",font=font(SANS,24,500),fill=(255,248,232),stroke_width=2,stroke_fill=(10,10,9))
    # north
    nx,ny=IX+IW-90,IY+70
    d.text((nx,ny),"N",font=font(SANS,30,600),fill=(255,248,232),stroke_width=2,stroke_fill=(10,10,9))
    d.line([(nx+10,ny+38),(nx+10,ny+80)],fill=(255,248,232),width=3)
    d.polygon([(nx+10,ny+32),(nx+2,ny+48),(nx+18,ny+48)],fill=(255,248,232))
    # caption
    cy=IY+IH+55
    if kind=="radar":
        cap1="NISAR L-BAND · HH КОГЕРЕНТНОСТЬ · 20.06 → 02.07.2026" if lang=="ru" else "NISAR L-BAND · HH COHERENCE · 20 JUN → 2 JUL 2026"
        cap=("Светлая лента — ветровал: лес потерял когерентность между двумя проходами радара. 29 км, ≥510 га."
             if lang=="ru" else "The bright band is windthrow: the forest lost coherence between two radar passes. 29 km, ≥510 ha.")
        fig="FIG. 1 · NISAR"
    else:
        cap1="SENTINEL-2 L2A · 28.07.2026 · СИНТЕЗ SWIR (B12/B8/B4)" if lang=="ru" else "SENTINEL-2 L2A · 28 JUL 2026 · SWIR COMPOSITE (B12/B8/B4)"
        cap=("Пурпурная лента — поваленный лес; зелёный — неповреждённый. 29 км, ≥510 га."
             if lang=="ru" else "The magenta band is windthrow; green is intact forest. 29 km, ≥510 ha.")
        fig="FIG. 2 · SENTINEL-2"
    d.text((IX,cy),cap1,font=f_cap1,fill=copper)
    lines=wrap(d,cap,f_cap,IW)
    yy=cy+42
    for ln in lines:
        d.text((IX,yy),ln,font=f_cap,fill=(59,52,43)); yy+=40
    # credits
    if kind=="radar":
        cred="NISAR: NASA/ISRO \u00b7 L2 GCOV + GUNW PROVISIONAL \u00b7 ASF DAAC   |   DEM: Copernicus   |   OSM: \u00a9 OpenStreetMap contributors"
    else:
        cred="Sentinel-2: Copernicus/ESA   |   DEM: Copernicus   |   OSM: \u00a9 OpenStreetMap contributors"
    d.line([(IX,CH-158),(IX+IW,CH-158)],fill=(201,187,166),width=1)
    f_cred=font(MONO,21)
    d.text((IX,CH-132),cred,font=f_cred,fill=(95,86,74))
    d.text((IX,CH-96),("Кушва · Свердловская область · 59.65°–59.82° E, 58.33°–58.51° N" if lang=="ru" else "Kushva · Sverdlovsk Oblast · 59.65°–59.82° E, 58.33°–58.51° N"),font=f_cred,fill=(95,86,74))
    # vertical figure label
    lab=Image.new("RGBA",(420,60),(0,0,0,0)); ld=ImageDraw.Draw(lab)
    ld.text((0,0),fig,font=f_small,fill=(138,123,102))
    lab=lab.rotate(90,expand=True)
    bg.paste(lab,(CH*0+2820,900),lab)
    # coordinates vertical left
    co=Image.new("RGBA",(700,40),(0,0,0,0)); cd=ImageDraw.Draw(co)
    cd.text((0,0),("58.33°–58.51° N  ·  59.65°–59.82° E" if lang=="ru" else "58.33°–58.51° N  ·  59.65°–59.82° E"),font=f_small,fill=(138,123,102))
    co=co.rotate(90,expand=True)
    bg.paste(co,(120,1700),co)
    return bg

opt=optical_img(); rad=radar_img()
for kind,im in [("radar",rad),("optical",opt)]:
    for lang in ["ru","en"]:
        p=compose(kind,lang,im)
        name=f"poster_{kind}_{lang}"
        p.save(OUT/f"{name}.png",optimize=True)
        p.save(OUT/f"{name}.jpg",quality=93,optimize=True,progressive=True)
        p.save(OUT/f"{name}.pdf",resolution=200)
        print(name,p.size,(OUT/f"{name}.jpg").stat().st_size/1e6)
