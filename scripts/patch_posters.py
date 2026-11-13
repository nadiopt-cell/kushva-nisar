from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\scripts\posters.py")
s=p.read_text(encoding="utf-8")
# stats block after rule
old="""    d.line([(200,545),(360,545)],fill=copper,width=5)
    # image"""
new="""    d.line([(200,545),(360,545)],fill=copper,width=5)
    # stats colophon
    f_num=font(SERIF,58,600); f_num2=font(SERIF,44,600); f_date=font(MONO,18)
    stats=[("29 КМ" if lang=="ru" else "29 KM",f_num),("≥510 ГА" if lang=="ru" else "≥510 HA",f_num2),("22.06.2026" if lang=="ru" else "22 JUN 2026",f_date)]
    yy=150
    for txt,fnt in stats:
        w=d.textlength(txt,font=fnt)
        d.text((2800-w,yy),txt,font=fnt,fill=ink if fnt is not f_date else muted)
        yy+= 66 if fnt is f_num else (54 if fnt is f_num2 else 30)
    # image"""
s=s.replace(old,new)
s=s.replace("Магентовая лента — поваленный лес; зелёный — неповреждённый. 29 км, ≥510 га.","Пурпурная лента — поваленный лес; зелёный — неповреждённый. 29 км, ≥510 га.")
# credits
old2="""    d.text((IX,CH-120),cred,font=f_cred,fill=dim)
    d.text((IX,CH-88),("Кушва · Свердловская область · 59.65°–59.82° E, 58.33°–58.51° N" if lang=="ru" else "Kushva · Sverdlovsk Oblast · 59.65°–59.82° E, 58.33°–58.51° N"),font=f_cred,fill=dim)"""
new2="""    d.line([(IX,CH-158),(IX+IW,CH-158)],fill=(201,187,166),width=1)
    f_cred=font(MONO,19)
    d.text((IX,CH-132),cred,font=f_cred,fill=(111,101,90))
    d.text((IX,CH-96),("Кушва · Свердловская область · 59.65°–59.82° E, 58.33°–58.51° N" if lang=="ru" else "Kushva · Sverdlovsk Oblast · 59.65°–59.82° E, 58.33°–58.51° N"),font=f_cred,fill=(111,101,90))"""
s=s.replace(old2,new2)
p.write_text(s,encoding="utf-8")
print("patched")