from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("  map=makeMap('map');\n  map.on('load',()=>{\n    addLayers(map); applyMain();","  map=makeMap('map');\n  window.__map=map;\n  map.on('load',()=>{\n    try{ addLayers(map); applyMain(); }catch(e){ console.error('addLayers failed',e); $('#loader .ls').textContent='ошибка слоёв: '+e.message; }")
p.write_text(s,encoding="utf-8")
print("ok")