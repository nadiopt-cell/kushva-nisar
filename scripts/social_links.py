from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\output\social_posts.md")
s=p.read_text(encoding="utf-8")
s=s.replace("[ссылка]","https://nadiopt-cell.github.io/kushva-nisar/")
s=s.replace("[link]","https://nadiopt-cell.github.io/kushva-nisar/")
p.write_text(s,encoding="utf-8")
print("ok")