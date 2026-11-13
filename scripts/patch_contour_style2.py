from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("const CENTER = [59.762,58.372];","const CENTER = [59.735,58.372];")
s=s.replace("'line-color':'#1A0E08','line-width':['interpolate',['linear'],['zoom'],9,3.4,13,4.8,16,6.0],'line-opacity':0.42,'line-blur':2.2","'line-color':'#1A0E08','line-width':['interpolate',['linear'],['zoom'],9,2.6,13,3.8,16,5.0],'line-opacity':0.35,'line-blur':2.0")
s=s.replace("'line-color':'#F2B184','line-width':['interpolate',['linear'],['zoom'],9,1.6,13,2.6,16,3.4],'line-opacity':0.98","'line-color':'#E8A06E','line-width':['interpolate',['linear'],['zoom'],9,1.2,13,2.0,16,2.8],'line-opacity':0.95")
p.write_text(s,encoding="utf-8")
print("ok")