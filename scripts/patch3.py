from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\scripts\posters.py")
lines=p.read_text(encoding="utf-8").splitlines()
out=[]; i=0; done=False
while i < len(lines):
    l=lines[i]
    if l.strip().startswith("cred=(") and not done:
        out.append('    if kind=="radar":')
        out.append('        cred="NISAR: NASA/ISRO \\u00b7 L2 GCOV + GUNW PROVISIONAL \\u00b7 ASF DAAC   |   DEM: Copernicus   |   OSM: \\u00a9 OpenStreetMap contributors"')
        out.append('    else:')
        out.append('        cred="Sentinel-2: Copernicus/ESA   |   DEM: Copernicus   |   OSM: \\u00a9 OpenStreetMap contributors"')
        # skip until line that ends the assignment
        j=i
        while j < len(lines) and not lines[j].rstrip().endswith(")"):
            j+=1
        i=j+1; done=True; continue
    out.append(l); i+=1
s="\n".join(out)+"\n"
s=s.replace("f_cred=font(MONO,19)","f_cred=font(MONO,21)")
s=s.replace("fill=(111,101,90)","fill=(95,86,74)")
p.write_text(s,encoding="utf-8")
print("patched",done)