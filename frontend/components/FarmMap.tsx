'use client'
import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

type Props = { onAreaChange: (hectares:number) => void }

export default function FarmMap({ onAreaChange }: Props) {
  const ref = useRef<HTMLDivElement | null>(null)
  const map = useRef<L.Map | null>(null)
  const layer = useRef<L.Polygon | null>(null)
  const marker = useRef<L.Marker | null>(null)
  const [points, setPoints] = useState<[number,number][]>([])

  useEffect(() => {
    if (!ref.current || map.current) return
    const m = L.map(ref.current).setView([23.2135,72.6840],14)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(m)
    marker.current = L.marker([23.2135,72.6840],{draggable:true}).addTo(m)
    marker.current.on('dragend',()=>{const p=marker.current?.getLatLng();if(p) m.setView(p,14)})
    m.on('click',(e)=>setPoints((old)=>old.concat([[e.latlng.lat,e.latlng.lng]])))
    map.current = m
    return ()=>{m.remove();map.current=null}
  },[])

  useEffect(()=>{
    const m=map.current
    if(!m) return
    if(layer.current){layer.current.remove();layer.current=null}
    if(points.length>=3){
      layer.current=L.polygon(points,{color:'#7ee2b1',fillColor:'#7ee2b1',fillOpacity:.18,weight:3}).addTo(m)
      const center=points.reduce((a,p)=>[a[0]+p[0],a[1]+p[1]],[0,0]).map((x)=>x/points.length) as [number,number]
      marker.current?.setLatLng(center)
      onAreaChange(areaHa(points))
    }
  },[points,onAreaChange])

  const finish=( )=>{ if(points.length>=3){ onAreaChange(areaHa(points)) } }
  const reset=()=>{setPoints([]);onAreaChange(10)}
  return <div className="relative h-[470px]">
    <div ref={ref} className="h-full w-full"/>
    <div className="absolute left-4 top-4 z-[500] rounded-xl border border-[#355e4d] bg-[#07120f]/90 px-3 py-2 text-xs">Click map to add boundary points</div>
    <div className="absolute bottom-4 left-4 z-[500] flex gap-2">
      <button onClick={finish} className="rounded-lg bg-[#7ee2b1] px-3 py-2 text-xs font-bold text-[#07120f]">Finish boundary</button>
      <button onClick={reset} className="rounded-lg border border-[#355e4d] bg-[#07120f]/90 px-3 py-2 text-xs">Reset</button>
    </div>
    <div className="absolute right-4 bottom-4 z-[500] rounded-xl bg-[#07120f]/90 px-3 py-2 text-xs">Points: {points.length}</div>
  </div>
}

function areaHa(points:[number,number][]) {
  if(points.length<3) return 0
  const R=6378137
  const rad=(x:number)=>x*Math.PI/180
  let s=0
  for(let i=0;i<points.length;i++){const j=(i+1)%points.length;s+=(rad(points[j][1])-rad(points[i][1]))*(2+Math.sin(rad(points[i][0]))+Math.sin(rad(points[j][0])))}
  return Math.abs(s*R*R/2)/10000
}
