from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("const CENTER = [59.735,58.372];","const CENTER = [59.72,58.372];")
p.write_text(s,encoding="utf-8")
print("ok")