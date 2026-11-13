from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
old="    setTimeout(()=>$('#loader').classList.add('hide'),650);"
new="""    let loaderDone=false;
    const hideLoader=()=>{ if(loaderDone) return; loaderDone=true; $('#loader').classList.add('hide'); };
    const checkLoaded=()=>{ if(map.isSourceLoaded('nisar_coh') && map.isSourceLoaded('s2_pre')) hideLoader(); };
    map.on('sourcedata',checkLoaded);
    setTimeout(hideLoader,15000);"""
if old not in s: print("old not found")
s=s.replace(old,new)
p.write_text(s,encoding="utf-8")
print("ok")