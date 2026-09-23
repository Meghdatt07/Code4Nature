'use client';

import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

type Geometry={type:'Polygon';coordinates:number[][][]};
type Props={value?:Geometry;onChange?:(geometry:Geometry|null,areaHa:number)=>void};

export default function FarmMap({value,onChange}:Props){
  const ref=useRef<HTMLDivElement|null>(null);
  const mapRef=useRef<L.Map|null>(null);
  const layerRef=useRef<L.Polygon|null>(null);
  const markersRef=useRef<L.CircleMarker[]>([]);
  const [points,setPoints]=useState<[number,number][]>(()=>value?.coordinates?.[0]?.map(([lng,lat])=>[lat,lng] as [number,number])||[]);

  useEffect(()=>{
    if(!ref.current||mapRef.current)return;
    const map=L.map(ref.current).setView([23.2135,72.6840],14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors',maxZoom:20}).addTo(map);
    map.on('click',(e)=>setPoints(old=>old.concat([[e.latlng.lat,e.latlng.lng]])));
    mapRef.current=map;
    return()=>{map.remove();mapRef.current=null};
  },[]);

  useEffect(()=>{
    const map=mapRef.current;if(!map)return;
    if(layerRef.current){layerRef.current.remove();layerRef.current=null}
    markersRef.current.forEach(m=>m.remove());markersRef.current=[];
    points.forEach((p,i)=>{
      const m=L.circleMarker(p,{radius:6,color:'#7ee2b1',weight:2,fillColor:'#7ee2b1',fillOpacity:.85}).addTo(map);
      m.bindTooltip(String(i+1));markersRef.current.push(m);
    });
    if(points.length>=2){
      layerRef.current=L.polygon(points,{color:'#7ee2b1',weight:3,fillColor:'#7ee2b1',fillOpacity:.16}).addTo(map);
    }
    if(points.length>=3&&onChange){
      const ring=points.map(([lat,lng])=>[lng,lat]);
      ring.push(ring[0]);
      const geometry:Geometry={type:'Polygon',coordinates:[ring]};
      onChange(geometry,areaHa(points));
    }
  },[points,onChange]);

  const finish=()=>{if(points.length<3||!onChange)return;const ring=points.map(([lat,lng])=>[lng,lat]);ring.push(ring[0]);onChange({type:'Polygon',coordinates:[ring]},areaHa(points))};
  const clear=()=>{setPoints([]);onChange?.(null,0)};

  return <div className="relative h-[520px]"><div ref={ref} className="h-full w-full rounded-2xl"/>
    <div className="absolute left-3 top-3 z-[500] rounded-xl border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs text-white/70">Click the map to add farm boundary points</div>
    <div className="absolute bottom-3 left-3 z-[500] flex gap-2">
      <button onClick={finish} className="rounded-lg bg-[#8bcfa6] px-3 py-2 text-xs font-bold text-[#07130f]">Finish boundary</button>
      <button onClick={clear} className="rounded-lg border border-white/10 bg-[#07130f]/90 px-3 py-2 text-xs">Clear</button>
    </div>
    <div className="absolute bottom-3 right-3 z-[500] rounded-lg bg-[#07130f]/90 px-3 py-2 text-xs">{points.length} points</div>
  </div>
}

function areaHa(points:[number,number][]){
  if(points.length<3)return 0;
  const R=6378137,rad=(x:number)=>x*Math.PI/180;let s=0;
  for(let i=0;i<points.length;i++){const j=(i+1)%points.length;s+=(rad(points[j][1])-rad(points[i][1]))*(2+Math.sin(rad(points[i][0]))+Math.sin(rad(points[j][0])))}
  return Math.abs(s*R*R/2)/10000;
}
