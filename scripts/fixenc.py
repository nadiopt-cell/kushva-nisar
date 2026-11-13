from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
b=p.read_bytes()
print("starts",b[:40])
s=b.decode("utf-8")
print("title raw",repr(s[s.find("<title>"):s.find("<title>")+60]))
try:
    fixed=s.encode("cp1251",errors="replace").decode("utf-8",errors="replace")
    print("fixed title",repr(fixed[fixed.find("<title>"):fixed.find("<title>")+60]))
    print("q marks",fixed.count("?"),"len",len(fixed))
    Path(r"E:\ai_project\30days_challenge\day14_borges\web\index_fixed.html").write_text(fixed,encoding="utf-8")
except Exception as e: print("ERR",e)