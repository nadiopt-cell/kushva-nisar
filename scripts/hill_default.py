from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("$('#cbHill').checked=false; applyMain();","$('#cbHill').checked=true; applyMain();")
p.write_text(s,encoding="utf-8")
print("hill default on")