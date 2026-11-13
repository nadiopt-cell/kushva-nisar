from pathlib import Path
s=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html").read_text(encoding="utf-8").splitlines()
for i in range(248,276): print(i,s[i])