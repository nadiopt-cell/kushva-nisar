from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
lines=p.read_text(encoding="utf-8").splitlines()

def idx(sub):
    for i,l in enumerate(lines):
        if sub in l: return i
    raise SystemExit("not found: "+sub)

# --- reorder layers ---
i0=idx("m.addLayer(raster('l_hill'")
i1=idx("m.addLayer({id:'l_places'")
block=lines[i0:i1]
byid={}
for l in block:
    for k in ["l_pre","l_post","l_coh","l_hv","l_dhv","l_comp","l_hill","l_roads","l_cfill","l_cline","l_track","l_water","l_waterline"]:
        if "'"+k+"'" in l:
            byid[k]=l
byid["l_hill"]="  m.addLayer(raster('l_hill','hill',0.40));"
byid["l_water"]="  m.addLayer({id:'l_water',type:'fill',source:'water',paint:{'fill-color':'#04161B','fill-opacity':0.72}});"
byid["l_waterline"]="  m.addLayer({id:'l_waterline',type:'line',source:'water',paint:{'line-color':'#8FC6CB','line-opacity':0.60,'line-width':1.0}});"
order=["l_pre","l_post","l_coh","l_hv","l_dhv","l_comp","l_hill","l_roads","l_cfill","l_cline","l_track","l_water","l_waterline"]
newblock=[byid[k] for k in order]
lines[i0:i1]=newblock

# --- applyMain hill opacity + water lock ---
i=idx("setVis(map,'l_pre',pre); setVis(map,'l_post',post); setVis(map,'l_hill',hill);")
lines[i]=lines[i]+"\n  if(map.getLayer('l_hill')) map.setPaintProperty('l_hill','raster-opacity', nisar?0.18:0.42);\n  setVis(map,'l_water',true); setVis(map,'l_waterline',true);"

# --- static water row ---
i=idx('id="cbHill"')
row=('    <label class="row static"><span class="sw" style="background-image:url(\'data/swatch_water.jpg\')"></span>'
     '<span class="lbl">\u0412\u043e\u0434\u0430 \u00b7 \u0432\u0441\u0435\u0433\u0434\u0430 \u0441\u0432\u0435\u0440\u0445\u0443'
     '<small>\u043e\u0437\u0451\u0440\u0430 \u0438 \u043f\u0440\u0443\u0434\u044b \u00b7 \u043d\u0435 \u043e\u0442\u043a\u043b\u044e\u0447\u0430\u0435\u0442\u0441\u044f</small></span>'
     '<span class="lock">\u25cf</span></label>')
lines.insert(i+1,row)

# --- css for static row ---
i=idx(".row .lbl small{")
lines.insert(i+1,".row.static{cursor:default}.row.static:hover{background:transparent}.row.static .lock{font-family:var(--mono);font-size:9px;color:#8FC6CB;border:1px solid rgba(143,198,203,.45);border-radius:2px;padding:2px 5px;letter-spacing:.06em}")

# --- panel header ---
s="\n".join(lines)+"\n"
s=s.replace("<h2>Слои <span>4 + рельеф</span></h2>","<h2>Слои <span>4 + вода</span></h2>")
p.write_text(s,encoding="utf-8")
print("patched",len(lines))