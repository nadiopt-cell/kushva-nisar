from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
b=p.read_bytes()
i=b.find(b"<title>")
print(b[i:i+60])
print(b[i:i+60].hex())
print("decoded:", b[i:i+60].decode("utf-8"))