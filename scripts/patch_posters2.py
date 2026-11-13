from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\scripts\posters.py")
s=p.read_text(encoding="utf-8")
old="""    cred=("NISAR: NASA/ISRO · L2 GCOV + GUNW PROVISIONAL · ASF DAAC   |   Sentinel-2: Copernicus/ESA   |   DEM: Copernicus   |   OSM: © OpenStreetMap contributors"
          if lang=="en" else "NISAR: NASA/ISRO · L2 GCOV + GUNW PROVISIONAL · ASF DAAC   |   Sentinel-2: Copernicus/ESA   |   DEM: Copernicus   |   OSM: © OpenStreetMap contributors")"""
new="""    if kind=="radar":
        cred="NISAR: NASA/ISRO · L2 GCOV + GUNW PROVISIONAL · ASF DAAC   |   DEM: Copernicus   |   OSM: © OpenStreetMap contributors"
    else:
        cred="Sentinel-2: Copernicus/ESA   |   DEM: Copernicus   |   OSM: © OpenStreetMap contributors""""
s=s.replace(old,new)
s=s.replace("f_cred=font(MONO,19)","f_cred=font(MONO,21)")
s=s.replace("fill=(111,101,90)","fill=(95,86,74)")
p.write_text(s,encoding="utf-8")
print("ok")