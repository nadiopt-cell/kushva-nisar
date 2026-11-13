from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
for i,ch in enumerate(s):
    if ch=="?": print(repr(s[max(0,i-40):i+20]))