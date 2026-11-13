from pathlib import Path
s=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html").read_text(encoding="utf-8")
for line in s.splitlines():
    if "cbPre" in line or "cbPost" in line:
        print(line.strip()[:400])