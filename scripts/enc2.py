from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
b=p.read_bytes(); i=b.find(b"<title>")+7
t=b[i:i+10].decode("utf-8")
print([hex(ord(c)) for c in t])
for enc in ["cp1251","cp866","latin1"]:
    try:
        r=t.encode(enc).decode("utf-8")
        print(enc,repr(r))
    except Exception as e: print(enc,"ERR",e)