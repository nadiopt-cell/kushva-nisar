from pathlib import Path
for fn in ["web_export_s2.py","web_export_nisar2.py"]:
    p=Path(r"E:\ai_project\30days_challenge\day14_borges\scripts")/fn
    s=p.read_text(encoding="utf-8")
    s=s.replace("dst_grid(20.0)","dst_grid(30.0)").replace("res=20.0","res=30.0")
    p.write_text(s,encoding="utf-8")
    print(fn,"patched")