from pathlib import Path
p=Path(r"E:\ai_project\30days_challenge\day14_borges\web\index.html")
s=p.read_text(encoding="utf-8")
# remove image source additions from addSources
for line in [
"  m.addSource('s2_pre',{type:'image',url:'data/s2_pre.jpg',coordinates:r.s2_pre});\n",
"  m.addSource('s2_post',{type:'image',url:'data/s2_post.jpg',coordinates:r.s2_post});\n",
"  m.addSource('nisar_coh',{type:'image',url:'data/nisar_coh.jpg',coordinates:r.nisar});\n",
"  m.addSource('nisar_hv',{type:'image',url:'data/nisar_hv.jpg',coordinates:r.nisar});\n",
"  m.addSource('nisar_dhv',{type:'image',url:'data/nisar_dhv.jpg',coordinates:r.nisar});\n",
"  m.addSource('hill',{type:'image',url:'data/hillshade.png',coordinates:meta.hillshade});\n",
]:
    s=s.replace(line,"")
# insert canvas loader before addLayers
anchor="function addLayers(m){"
loader='''function canvasSource(m,id,url,coords){
  return new Promise((resolve,reject)=>{
    const img=new Image();
    img.crossOrigin='anonymous';
    img.onload=()=>{
      const c=document.createElement('canvas');
      c.width=img.width; c.height=img.height;
      c.getContext('2d').drawImage(img,0,0);
      c.style.display='none'; document.body.appendChild(c);
      m.addSource(id,{type:'canvas',canvas:c,coordinates:coords,animate:false});
      resolve();
    };
    img.onerror=()=>reject(new Error('image '+url));
    img.src=url;
  });
}
async function addRasterSources(m){
  const r=meta.rasters;
  await Promise.all([
    canvasSource(m,'s2_pre','data/s2_pre.jpg',r.s2_pre),
    canvasSource(m,'s2_post','data/s2_post.jpg',r.s2_post),
    canvasSource(m,'nisar_coh','data/nisar_coh.jpg',r.nisar),
    canvasSource(m,'nisar_hv','data/nisar_hv.jpg',r.nisar),
    canvasSource(m,'nisar_dhv','data/nisar_dhv.jpg',r.nisar),
    canvasSource(m,'hill','data/hillshade.png',meta.hillshade)
  ]);
}

'''
s=s.replace(anchor,loader+"async "+anchor)
# add await in addLayers after addSources
s=s.replace("function addLayers(m){\n  addSources(m);","function addLayers(m){\n  addSources(m);")
s=s.replace("  addSources(m);\n  m.addLayer(raster('l_pre'","  addSources(m);\n  await addRasterSources(m);\n  m.addLayer(raster('l_pre'")
# make addLayers async already replaced
# map load call await
s=s.replace("try{ addLayers(map);","try{ await addLayers(map);")
s=s.replace("map.on('load',()=>{\n    try{ await addLayers(map);","map.on('load',async()=>{\n    try{ await addLayers(map);")
# compare loads async
s=s.replace("cmpA.on('load',()=>{ addLayers(cmpA); done(); });","cmpA.on('load',async()=>{ await addLayers(cmpA); done(); });")
s=s.replace("cmpB.on('load',()=>{ addLayers(cmpB); done(); });","cmpB.on('load',async()=>{ await addLayers(cmpB); done(); });")
p.write_text(s,encoding="utf-8")
print("ok")