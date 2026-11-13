from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
s=s.replace("url:'data/hillshade.jpg',coordinates:meta.hillshade","url:'data/hillshade.png',coordinates:meta.hillshade")
s=s.replace("m.addLayer(raster('l_hill','hill',0.40));","m.addLayer(raster('l_hill','hill',1.0));")
s=s.replace("map.setPaintProperty('l_hill','raster-opacity', nisar?0.18:0.42);","map.setPaintProperty('l_hill','raster-opacity', nisar?0.55:1.0);")
s=s.replace("paint:{'fill-color':'#04161B','fill-opacity':0.72}","paint:{'fill-color':'#03151A','fill-opacity':0.78}")
s=s.replace("paint:{'line-color':'#8FC6CB','line-opacity':0.60,'line-width':1.0}","paint:{'line-color':'#9FD3D8','line-opacity':0.75,'line-width':1.2,'line-blur':0.4}")
# defaults on load
s=s.replace("try{ addLayers(map); applyMain(); }catch(e){ console.error('addLayers failed',e); $('#loader .ls').textContent='ошибка слоёв: '+e.message; }",
"try{ addLayers(map); $('#cbPre').checked=false; $('#cbPost').checked=false; $('#cbNisar').checked=true; $('#cbContour').checked=true; $('#cbHill').checked=false; applyMain(); }catch(e){ console.error('addLayers failed',e); $('#loader .ls').textContent='ошибка слоёв: '+e.message; }")
# title card size
s=s.replace("max-width:min(690px,calc(100vw - 40px));padding:20px 24px 18px","max-width:min(620px,calc(100vw - 40px));padding:18px 22px 16px")
s=s.replace("font-size:clamp(32px,4vw,56px)","font-size:clamp(30px,3.6vw,48px)")
# credits simplify
old='''<div class="credits">
  <b>Ветровал:</b> смерч 22.06.2026, Кушва (29 км, ≥510 га) + второй смерч у Малой Лаи (16,5 км, ≥200 га).<br>
  <b>NISAR:</b> NASA/ISRO L2 GCOV и GUNW PROVISIONAL, L-band 24 см, HH/HV · 20.06.2026 и 02.07.2026 · трек 93D · ASF DAAC.<br>
  <b>Оптика:</b> Sentinel-2 L2A 21.05.2026 / 28.07.2026 · синтез SWIR B12-B8-B4 · Copernicus. <b>Рельеф:</b> Copernicus DEM 30 м · <b>OSM</b>: дороги, вода, подписи.
</div>'''
new='''<div class="credits"><b>NISAR</b> NASA/ISRO · <b>Sentinel-2</b> Copernicus/ESA · <b>DEM</b> Copernicus · <b>OSM</b> © OpenStreetMap</div>'''
s=s.replace(old,new)
# credits style
s=s.replace(".credits{position:absolute;right:20px;bottom:16px;z-index:7;max-width:min(590px,calc(100vw - 40px));text-align:right;font-family:var(--mono);font-size:8.5px;line-height:1.6;color:#7E7363;letter-spacing:.01em}",
".credits{position:absolute;right:20px;bottom:16px;z-index:7;max-width:calc(100vw - 40px);text-align:right;font-family:var(--mono);font-size:9px;line-height:1.5;color:#A19077;letter-spacing:.02em;background:rgba(18,16,13,.74);border:1px solid var(--line);padding:6px 9px;border-radius:2px;backdrop-filter:blur(8px)}")
p.write_text(s,encoding="utf-8")
print("ok")