from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("const CENTER = [59.783,58.372];","const CENTER = [59.762,58.372];")
s=s.replace("zoom:11.05","zoom:11.15")
s=s.replace("zoom:11.05,","zoom:11.15,")
s=s.replace("map.setPaintProperty('l_hill','raster-opacity', nisar?0.55:1.0);","map.setPaintProperty('l_hill','raster-opacity', nisar?0.55:0.78);")
# add halo before cline
s=s.replace("  m.addLayer({id:'l_cline',type:'line',source:'contour',paint:{'line-color':'#F2B184','line-width':['interpolate',['linear'],['zoom'],9,1.0,13,1.8,16,2.6],'line-opacity':0.95}});",
"  m.addLayer({id:'l_chalo',type:'line',source:'contour',paint:{'line-color':'#1A0E08','line-width':['interpolate',['linear'],['zoom'],9,3.4,13,4.8,16,6.0],'line-opacity':0.42,'line-blur':2.2}});\n  m.addLayer({id:'l_cline',type:'line',source:'contour',paint:{'line-color':'#F2B184','line-width':['interpolate',['linear'],['zoom'],9,1.6,13,2.6,16,3.4],'line-opacity':0.98}});")
s=s.replace("setVis(map,'l_cfill',cont); setVis(map,'l_cline',cont); setVis(map,'l_track',cont);","setVis(map,'l_cfill',cont); setVis(map,'l_chalo',cont); setVis(map,'l_cline',cont); setVis(map,'l_track',cont);")
s=s.replace("const on=['l_cfill','l_cline','l_track','l_water','l_waterline','l_roads','l_places'];","const on=['l_cfill','l_chalo','l_cline','l_track','l_water','l_waterline','l_roads','l_places'];")
p.write_text(s,encoding="utf-8")
print("ok")