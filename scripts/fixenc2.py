from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
# reverse double-encoding; keep chars not in cp1251 as-is via latin1 fallback per char
out=[]
for ch in s:
    try:
        out.append(ch.encode("cp1251"))
    except UnicodeEncodeError:
        out.append(ch.encode("utf-8"))
raw=b"".join(out)
fixed=raw.decode("utf-8",errors="replace")
q=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index_fixed.html")
q.write_text(fixed,encoding="utf-8")
i=fixed.find("<title>")
print("title bytes",fixed[i:i+60].encode("utf-8")[:40].hex())
print("title",fixed[i:i+40])
print("qmarks",fixed.count("?"))