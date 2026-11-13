from pathlib import Path
s=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html").read_text(encoding="utf-8")
out=[]
for i,l in enumerate(s.splitlines()):
    if any(k in l for k in ["l_hill","l_water","l_waterline","l_cfill","l_cline","l_places","l_roads","l_track","raster-opacity', nisar","row static"]):
        out.append(f"{i} {l.strip()[:240]}")
Path(r"E:\ai_project\30days_challenge\day14_borges\build\layers.txt").write_text("\n".join(out),encoding="utf-8")
print("ok")