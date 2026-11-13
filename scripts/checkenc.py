from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
i=s.find("<title>"); print(repr(s[i:i+80]))
i=s.find("Карта"); print("found Карта at",i)
i=s.find("Рљ"); print("found mojibake at",i, repr(s[i:i+40]) if i>0 else "")