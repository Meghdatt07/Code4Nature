(function setupIntro(){
  const intro=$("siteIntro"),enter=$("introEnter");
  if(!intro||!enter)return;
  document.body.classList.add("intro-lock");
  const READY_DELAY=4200;
  const enterSite=()=>{
    if(enter.disabled)return;
    enter.disabled=true;
    enter.classList.remove("is-ready");
    intro.classList.add("is-entered");
    document.body.classList.remove("intro-lock");
    setTimeout(()=>intro.remove(),700);
  };
  setTimeout(()=>{
    enter.disabled=false;
    enter.classList.add("is-ready");
    enter.focus({preventScroll:true});
  },READY_DELAY);
  enter.addEventListener("click",enterSite);
  enter.addEventListener("keydown",(event)=>{
    if((event.key==="Enter"||event.key===" ")&&!enter.disabled){
      event.preventDefault();
      enterSite();
    }
  });
})();


function $(id){return document.getElementById(id)}
function usd(v){return new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:2}).format(v)}
function inr(v){return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:0}).format(v)}
const FARM_KEY="carbonawdFarmAreaHa",LAT_KEY="carbonawdLat",LON_KEY="carbonawdLon";
function farmArea(){return Number(localStorage.getItem(FARM_KEY)||10)}
function saveFarm(a,lat,lon){localStorage.setItem(FARM_KEY,String(a));localStorage.setItem(LAT_KEY,String(lat));localStorage.setItem(LON_KEY,String(lon))}
function areaHa(points){if(!points||points.length<3)return 0;const R=6378137,rad=x=>x*Math.PI/180;let s=0;for(let i=0,j=points.length-1;i<points.length;j=i++)s+=(rad(points[j][1])-rad(points[i][1]))*(2+Math.sin(rad(points[i][0]))+Math.sin(rad(points[j][0])));return Math.abs(s*R*R/2)/10000}
function simulateSAR(lat,lon){const z=Math.sin(lat*3.1)+Math.cos(lon*2.7);return{wet:Math.max(18,Math.min(82,48+z*9)),vv:-14+Math.sin(lat)*2,vh:-20+Math.cos(lon)*2,source:"Built-in simulator"}}
async function getSAR(lat,lon){const base=window.CARBONAWD_API_BASE;if(base){try{const r=await fetch(base+"/api/sar?lat="+encodeURIComponent(lat)+"&lon="+encodeURIComponent(lon),{signal:AbortSignal.timeout(9000)});if(!r.ok)throw Error();const d=await r.json();return{wet:d.moisture_proxy_percent,vv:d.vv_mean_db,vh:d.vh_mean_db,source:d.source||"Sentinel Hub",note:d.note||""}}catch(e){}}return simulateSAR(lat,lon)}
async function getMarket(){let fx=88,ag=20,vcm=1.85;try{const d=await (await fetch("https://open.er-api.com/v6/latest/USD")).json();if(d&&d.rates&&d.rates.INR)fx=Number(d.rates.INR)}catch(e){}try{const d=await (await fetch("https://api.coingecko.com/api/v3/simple/price?ids=toucan-protocol-base-carbon-tonne&vs_currencies=usd")).json();if(d&&d["toucan-protocol-base-carbon-tonne"]&&d["toucan-protocol-base-carbon-tonne"].usd)vcm=Number(d["toucan-protocol-base-carbon-tonne"].usd)}catch(e){}try{const h=await (await fetch("https://www.carbon.fyi/data")).text();const m=h.match(/Agriculture[\s\S]{0,1000}?\$([0-9,.]+)[\s\S]{0,300}?\$([0-9,.]+)/i);if(m)ag=Number(m[2].replaceAll(",",""))}catch(e){}return{fx:fx,agriculture:ag,vcm:vcm,updated:new Date().toLocaleString()}}
let market=null;
function setupMap(){if(!$("map"))return;const lat0=Number(localStorage.getItem(LAT_KEY)||23.2135),lon0=Number(localStorage.getItem(LON_KEY)||72.684);const map=L.map("map").setView([lat0,lon0],14);L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{attribution:"Tiles © Esri"}).addTo(map);let marker=L.marker([lat0,lon0],{draggable:true}).addTo(map);function point(lat,lon){marker.setLatLng([lat,lon]);$("lat").value=lat.toFixed(5);$("lon").value=lon.toFixed(5);saveFarm(Number($("areaHa").value||farmArea()),lat,lon)}marker.on("dragend",()=>{const p=marker.getLatLng();point(p.lat,p.lng)});map.on("click",e=>point(e.latlng.lat,e.latlng.lng));const drawn=new L.FeatureGroup().addTo(map);let boundary=null;const draw=new L.Control.Draw({edit:{featureGroup:drawn},draw:{polyline:false,circle:false,circlemarker:false,marker:false,rectangle:{shapeOptions:{color:"#34d399"}},polygon:{allowIntersection:false}}});map.addControl(draw);function useLayer(layer){drawn.clearLayers();boundary=layer;drawn.addLayer(layer);const pts=layer.getLatLngs()[0].map(p=>[p.lat,p.lng]);const a=areaHa(pts),c={lat:pts.reduce((s,p)=>s+p[0],0)/pts.length,lon:pts.reduce((s,p)=>s+p[1],0)/pts.length};$("areaHa").value=a.toFixed(2);$("mapArea").textContent=a.toFixed(2)+" ha";$("pointCount").textContent=String(pts.length);point(c.lat,c.lon);saveFarm(a,c.lat,c.lon)}map.on(L.Draw.Event.CREATED,e=>useLayer(e.layer));map.on(L.Draw.Event.EDITED,e=>e.layers.eachLayer(useLayer));$("moveBtn").onclick=()=>{const a=Number($("lat").value),b=Number($("lon").value);point(a,b);map.setView([a,b],15)};$("clearFarm").onclick=()=>{drawn.clearLayers();boundary=null;$("areaHa").value=10;$("mapArea").textContent="10.00 ha";$("pointCount").textContent="0";saveFarm(10,lat0,lon0)};$("sarBtn").onclick=async()=>{const a=Number($("lat").value),b=Number($("lon").value);$("sarState").textContent="LOADING";const d=await getSAR(a,b);$("sarState").textContent=d.source.includes("Sentinel")?"LIVE SAR":"SIMULATED";$("sarMoisture").textContent=d.wet==null?"—":Number(d.wet).toFixed(1)+"%";$("sarBackscatter").textContent=(d.vv==null?"—":Number(d.vv).toFixed(1))+" / "+(d.vh==null?"—":Number(d.vh).toFixed(1))+" dB";$("sarSource").textContent=d.source;$("sarNote").textContent=d.note||"Simulator fallback. Not satellite evidence."}}
function setupChart(){if(!$("awdChart"))return;const lab=Array.from({length:30},(_,i)=>"D"+(i+1)),base=lab.map(()=>5),awd=[5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7];new Chart($("awdChart"),{type:"line",data:{labels:lab,datasets:[{label:"Continuous flooding",data:base,borderWidth:2},{label:"AWD water depth (cm)",data:awd,borderWidth:3}]},options:{responsive:true,maintainAspectRatio:false,scales:{y:{title:{display:true,text:"Water depth (cm)"}},x:{grid:{display:false}}},plugins:{legend:{labels:{color:"#cbd5e1"}}}}});$("telemetryBtn").onclick=()=>{const v=Number($("depth").value),s=v>0?"WET":v>=-15?"DRYING":"REWETTING";$("depthValue").textContent=v.toFixed(1)+" cm";$("telemetryStatus").textContent=s;$("awdState").textContent=s};$("depth").oninput=()=>$("depthValue").textContent=Number($("depth").value).toFixed(1)+" cm"}
function calc(){if(!$("areaRange"))return;const a=Number($("areaRange").value),r=Number($("abatement").value),s=Number($("share").value)/100,p=$("priceModel").value==="erf"?15:(market&&market.vcm||1.85),fx=market&&market.fx||88,ch4=a*r,credits=ch4*28/1000,gross=credits*p,f=gross*s,c=gross-f;$("areaLabel").textContent=a.toFixed(1)+" ha";$("abatementLabel").textContent=r.toFixed(0)+" kg";$("shareLabel").textContent=Math.round(s*100)+"%";$("priceLabel").textContent=usd(p)+"/tCO₂e";$("ch4Out").textContent=ch4.toLocaleString()+" kg";$("creditOut").textContent=credits.toFixed(2)+" tCO₂e";$("grossOut").textContent=usd(gross);$("grossInr").textContent=inr(gross*fx);$("farmerOut").textContent=usd(f);$("farmerInr").textContent=inr(f*fx);$("companyOut").textContent=usd(c);$("companyInr").textContent=inr(c*fx);$("selectedAreaHint").textContent="Map-selected area: "+farmArea().toFixed(2)+" ha";$("fxOut").textContent="1 USD ≈ ₹"+fx.toFixed(2);$("ch4Kpi")&&($("ch4Kpi").textContent=(farmArea()*120).toLocaleString()+" kg");$("co2Kpi")&&($("co2Kpi").textContent=(farmArea()*120*28/1000).toFixed(2)+" t")}
async function setupMarket(){if(!$("marketPrice"))return;market=await getMarket();$("marketPrice").textContent=usd(market.agriculture);$("marketInr").textContent=inr(market.agriculture*market.fx)+" / tCO₂e";$("bctPrice").textContent=usd(market.vcm);$("indiaProxy").textContent=inr(market.agriculture*market.fx);$("fxText").textContent="1 USD ≈ ₹"+market.fx.toFixed(2);$("marketUpdated").textContent=market.updated;calc()}
document.addEventListener("DOMContentLoaded",()=>{
  setupMap();setupChart();setupMarket();
  ["areaRange","abatement","share"].forEach(id=>$(id)&&$(id).addEventListener("input",calc));
  $("priceModel")&&$("priceModel").addEventListener("change",calc);
  $("refreshMarket")&&$("refreshMarket").addEventListener("click",setupMarket);
  if($("areaRange"))$("areaRange").value=Math.min(50,Math.max(.5,farmArea()));
  const menu=$("menu"),links=document.querySelector(".nav-links");
  menu&&menu.addEventListener("click",()=>links&&links.classList.toggle("open"));
  links&&links.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>links.classList.remove("open")));
  calc()
});
