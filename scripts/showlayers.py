from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
for i,l in enumerate(s.splitlines()):
    if any(k in l for k in ["l_hill","l_water","l_waterline","l_cfill","l_cline","l_places","l_roads","l_track","applyMain"]):
        print(i, l.strip()[:220])