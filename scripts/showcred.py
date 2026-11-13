from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\scripts\posters.py")
lines=p.read_text(encoding="utf-8").splitlines()
for i,l in enumerate(lines):
    if "cred=" in l or "f_cred=" in l or "CH-132" in l or "CH-96" in l:
        print(i,repr(l))