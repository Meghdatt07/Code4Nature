'use client'

import { useMemo, useState } from 'react'
import { ArrowRight, Download, Droplets, Factory, Info, Leaf, MapPinned, Satellite, ShieldCheck, Sparkles } from 'lucide-react'
import { Bar, BarChart, CartesianGrid, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from 'recharts'

const api = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
type Scenario = 'Conservative' | 'Base Demo' | 'Custom'

function calc(v:{area:number;base:number;project:number;price:number;share:number;water:number}){
  const reduction=(v.base-v.project)*v.area
  const gross=reduction*v.price
  const farmer=gross*v.share/100
  return{...v,reduction,gross,farmer,company:gross-farmer,waterSaved:4.96e6*v.water/100}
}

export default function Home(){
  const[area,setArea]=useState(10),[base,setBase]=useState(6),[project,setProject]=useState(3.5),[price,setPrice]=useState(20),[share,setShare]=useState(60),[water,setWater]=useState(36.7),[ran,setRan]=useState(false)
  const r=useMemo(()=>calc({area,base,project,price,share,water}),[area,base,project,price,share,water])
  const scenario=(s:Scenario)=>{
    if(s==='Conservative'){setProject(4.5);setPrice(15);setWater(20)}
    else if(s==='Base Demo'){setArea(10);setBase(6);setProject(3.5);setPrice(20);setShare(60);setWater(36.7)}
  }

  return <main className="min-h-screen bg-[#07120f] text-[#edf7f2]">
    <section className="relative overflow-hidden border-b border-[#1d352b]">
      <div className="absolute inset-0 opacity-70" style={{background:'radial-gradient(circle at 80% 10%,rgba(80,154,116,.26),transparent 28%),linear-gradient(90deg,rgba(126,226,177,.035) 1px,transparent 1px),linear-gradient(rgba(126,226,177,.035) 1px,transparent 1px)',backgroundSize:'auto,40px 40px,40px 40px'}}/>
      <div className="relative mx-auto grid max-w-7xl gap-12 px-5 pb-18 pt-18 lg:grid-cols-[1.05fr_.95fr] lg:items-center lg:py-24">
        <div>
          <div className="status-pill"><span className="status-dot"/> Climate intelligence · demo-v1.0</div>
          <h1 className="mt-7 max-w-5xl text-balance text-5xl font-black leading-[.95] tracking-[-.05em] md:text-7xl">Make every rice field <span className="text-[#8bcfa6]">measurable.</span></h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-[#9ab3a8]">Connect water management, methane modelling, field evidence and carbon economics in one transparent climate workflow.</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a href="#simulator" className="inline-flex items-center gap-2 rounded-xl bg-[#8bcfa6] px-5 py-3.5 font-bold text-[#07120f]">Explore a field <ArrowRight size={17}/></a>
            <a href="#how-it-works" className="inline-flex items-center gap-2 rounded-xl border border-[#355e4d] px-5 py-3.5 font-semibold text-[#d9e9e1]">How it works</a>
          </div>
          <div className="mt-11 grid max-w-2xl grid-cols-3 divide-x divide-[#244137] rounded-2xl border border-[#244137] bg-[#0a1813]/80">
            <HeroMetric label="Water" value={water+'%'} note="illustrative saving"/>
            <HeroMetric label="CO₂e" value={r.reduction.toFixed(1)+' t'} note="estimated reduction"/>
            <HeroMetric label="Value" value={'$'+r.gross.toFixed(0)} note="illustrative gross value"/>
          </div>
        </div>

        <div className="glass relative min-h-[400px] overflow-hidden p-3 md:min-h-[500px]">
          <div className="absolute inset-3 rounded-[20px] border border-[#355e4d] bg-[#0b2119]"/>
          <div className="absolute inset-8 rounded-[18px]" style={{backgroundImage:'linear-gradient(rgba(139,207,166,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(139,207,166,.06) 1px,transparent 1px)',backgroundSize:'28px 28px'}}/>
          <div className="absolute left-[16%] top-[22%] h-[55%] w-[68%] rotate-[-4deg] rounded-[32%_48%_38%_45%] border-2 border-[#8bcfa6]/60 bg-[#8bcfa6]/10"/>
          <div className="absolute left-[45%] top-[47%] grid h-14 w-14 place-items-center rounded-2xl border border-[#8bcfa6]/30 bg-[#07120f]/90 text-[#8bcfa6] shadow-2xl"><MapPinned size={22}/></div>
          <div className="absolute right-6 top-6 grid gap-2 text-[10px] uppercase tracking-[.12em] text-[#87a095]">
            <span className="rounded-lg border border-[#355e4d] bg-[#07120f]/80 px-3 py-2">Boundary captured</span>
            <span className="rounded-lg border border-[#355e4d] bg-[#07120f]/80 px-3 py-2">Water regime · AWD</span>
            <span className="rounded-lg border border-[#355e4d] bg-[#07120f]/80 px-3 py-2">MRV · simulated</span>
          </div>
          <div className="absolute bottom-6 left-6 max-w-[240px] rounded-2xl border border-[#355e4d] bg-[#07120f]/90 p-4 backdrop-blur">
            <div className="text-[10px] font-bold tracking-[.15em] text-[#8bcfa6]">FIELD 042</div>
            <div className="mt-2 text-2xl font-black">{area.toFixed(1)} ha</div>
            <div className="mt-1 text-xs text-[#8fa99d]">Live scenario preview · values remain illustrative</div>
          </div>
        </div>
      </div>
    </section>

    <section id="how-it-works" className="border-b border-[#1d352b] bg-[#0a1713]">
      <div className="mx-auto max-w-7xl px-5 py-16 md:py-20">
        <div className="max-w-3xl">
          <div className="text-[11px] font-bold tracking-[.16em] text-[#8bcfa6]">ONE FIELD · ONE STORY</div>
          <h2 className="mt-3 text-3xl font-black tracking-tight md:text-5xl">From water practice to climate value.</h2>
          <p className="mt-4 text-[#94aba0]">Each step stays connected, so the user can trace a scenario from the farm boundary to the modelled outcome.</p>
        </div>
        <div className="mt-10 grid gap-4 md:grid-cols-4">
          <JourneyStep n="01" icon={<MapPinned size={19}/>} title="Define the field" text="Draw or select a farm boundary and see the area update."/>
          <JourneyStep n="02" icon={<Droplets size={19}/>} title="Choose practice" text="Explore the water-management scenario and its assumptions."/>
          <JourneyStep n="03" icon={<Leaf size={19}/>} title="Estimate impact" text="See water, methane, CO₂e and economic outputs recalculate together."/>
          <JourneyStep n="04" icon={<ShieldCheck size={19}/>} title="Inspect evidence" text="Understand what is simulated, observed or still unverified."/>
        </div>
      </div>
    </section>

    <section id="simulator" className="mx-auto max-w-7xl px-5 py-16 md:py-24">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="text-[11px] font-bold tracking-[.16em] text-[#8bcfa6]">CORE PRODUCT</div>
          <h2 className="mt-3 text-3xl font-black tracking-tight md:text-5xl">Explore a rice field scenario.</h2>
          <p className="mt-4 max-w-2xl text-[#94aba0]">Adjust the same inputs you already use today. The redesign changes only how the experience is presented.</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-[#355e4d] bg-[#0c1a15] px-3 py-2 text-xs text-[#9eb8aa]"><Sparkles size={14} className="text-[#8bcfa6]"/> All outputs are illustrative</div>
      </div>

      <div className="mt-10 grid gap-5 lg:grid-cols-[1.22fr_.78fr] lg:items-start">
        <div className="glass overflow-hidden">
          <div className="relative h-[440px] overflow-hidden bg-[#0b2119]">
            <div className="absolute inset-0 opacity-50" style={{backgroundImage:'linear-gradient(rgba(139,207,166,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(139,207,166,.06) 1px,transparent 1px)',backgroundSize:'32px 32px'}}/>
            <svg className="absolute inset-0 h-full w-full" viewBox="0 0 800 440" preserveAspectRatio="none"><path d="M160 90 L620 70 L690 270 L560 365 L230 330 L110 220 Z" fill="rgba(126,226,177,.16)" stroke="#8bcfa6" strokeWidth="3"/><path d="M220 140 C320 110 420 170 590 125 M180 230 C310 190 430 280 630 220" fill="none" stroke="#84b7cf" strokeWidth="2"/></svg>
            <div className="absolute left-5 top-5 rounded-xl border border-[#355e4d] bg-[#07120f]/90 px-3 py-2 text-xs text-[#c4ddd1]"><MapPinned className="mr-2 inline text-[#8bcfa6]" size={15}/> Demo polygon · {area.toFixed(1)} ha</div>
            <div className="absolute right-5 top-5 flex gap-1"><span className="rounded-lg bg-[#07120f]/90 px-3 py-2 text-xs text-[#8bcfa6]">Map</span><span className="rounded-lg bg-[#07120f]/60 px-3 py-2 text-xs text-[#8ba397]">Satellite</span></div>
            <div className="absolute bottom-5 left-5 rounded-xl border border-[#355e4d] bg-[#07120f]/90 px-3 py-2 text-xs text-[#9db8ab]"><Satellite className="mr-2 inline text-[#8bcfa6]" size={14}/> Interactive boundary preview</div>
          </div>
          <div className="grid grid-cols-3 divide-x divide-[#244137] border-t border-[#244137]">
            <MiniMetric label="Farm area" value={area.toFixed(2)+' ha'}/>
            <MiniMetric label="Acres" value={(area*2.471).toFixed(2)}/>
            <MiniMetric label="Status" value="SIMULATED"/>
          </div>
        </div>

        <div className="glass p-6 lg:sticky lg:top-28">
          <div className="flex items-center justify-between">
            <div><div className="text-[11px] font-bold tracking-[.16em] text-[#8bcfa6]">01 · FIELD ASSUMPTIONS</div><h3 className="mt-2 text-xl font-bold">Tune the scenario</h3></div>
            <span className="status-pill">Demo</span>
          </div>
          <div className="mt-6 grid gap-5">
            <Slider label={'Farm area: '+area.toFixed(1)+' ha'} value={area} min=".5" max="20" step=".1" set={setArea}/>
            <Slider label={'Baseline emissions: '+base.toFixed(1)+' tCO₂e/ha'} value={base} min="3" max="8" step=".1" set={setBase}/>
            <Slider label={'Project emissions: '+project.toFixed(1)+' tCO₂e/ha'} value={project} min="1" max="8" step=".1" set={setProject}/>
            <Slider label={'Water reduction: '+water.toFixed(1)+'%'} value={water} min="0" max="70" step=".1" set={setWater}/>
          </div>
          <div className="mt-6 grid gap-3 rounded-2xl border border-[#244137] bg-[#0a1813] p-4">
            <div className="flex items-center gap-2 text-xs font-bold tracking-[.12em] text-[#89a397]">PRICE SCENARIO</div>
            <div className="grid grid-cols-3 gap-2">{[15,20,25].map(p=><button key={p} onClick={()=>setPrice(p)} className={'rounded-xl border px-3 py-2.5 text-sm transition '+(price===p?'border-[#8bcfa6] bg-[#8bcfa6]/10 text-[#dff1e6]':'border-[#355e4d] text-[#94ada1] hover:bg-white/[.03]')}>{'$'+p}</button>)}</div>
          </div>
          <Slider label={'Farmer share: '+share+'%'} value={share} min="0" max="100" step="1" set={setShare}/>
          <div className="mt-6 grid grid-cols-3 gap-2">{['Conservative','Base Demo','Custom'].map(s=><button key={s} onClick={()=>s==='Custom'?setRan(true):scenario(s as Scenario)} className={'rounded-xl border px-2 py-2.5 text-xs transition '+((s==='Base Demo'&&!ran)|| (s==='Custom'&&ran)?'border-[#8bcfa6] bg-[#8bcfa6]/10 text-[#dff1e6]':'border-[#355e4d] text-[#93aa9f] hover:bg-white/[.03]')}>{s}</button>)}</div>
          <button onClick={()=>setRan(true)} className="mt-6 w-full rounded-xl bg-[#8bcfa6] py-3.5 font-black tracking-wide text-[#07120f]">RUN FIELD SIMULATION <ArrowRight className="ml-2 inline" size={16}/></button>
          <button onClick={()=>window.open(api+'/api/export/pdf','_blank')} className="mt-2 w-full rounded-xl border border-[#355e4d] py-3 text-sm text-[#c2d7cd] hover:bg-white/[.03]"><Download className="mr-2 inline" size={16}/>Download demo report</button>
        </div>
      </div>

      {ran&&<section className="mt-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between"><div><div className="text-[11px] font-bold tracking-[.16em] text-[#8bcfa6]">02 · IMPACT OUTPUT</div><h3 className="mt-2 text-2xl font-bold">Scenario result</h3></div><div className="rounded-full border border-[#355e4d] px-3 py-2 text-xs text-[#94aca0]">{'Demo scenario'} · illustrative</div></div>
        <div className="mt-4 grid gap-3 md:grid-cols-4">{[
          ['Farm area',area.toFixed(2)+' ha'],['Water saved',(r.waterSaved/1e6).toFixed(2)+'M L'],['Estimated reduction',r.reduction.toFixed(2)+' tCO₂e'],['Potential credits',r.reduction.toFixed(2)],
          ['Carbon price','$'+price+'/t'],['Gross value','$'+r.gross.toFixed(2)'],['Farmer share','$'+r.farmer.toFixed(2)'],['Asterisk Climos','$'+r.company.toFixed(2)]
        ].map(([title,value])=><div key={title} className="glass p-5"><div className="text-[11px] uppercase tracking-[.1em] text-[#789084]">{title}</div><div className="mt-2 text-2xl font-black tracking-tight">{value}</div><div className="mt-3 inline-flex items-center gap-2 rounded-full border border-[#355e4d] px-2.5 py-1 text-[9px] font-bold tracking-[.1em] text-[#8fa99e]"><Info size={11}/> ILLUSTRATIVE DEMO</div></div>)}</div>
        <div className="mt-5 grid gap-5 lg:grid-cols-2">
          <Chart title="Water use comparison"><ResponsiveContainer width="100%" height={260}><BarChart data={[{name:'Water',Conventional:496,Optimized:496*(1-water/100)}]}><CartesianGrid strokeDasharray="3 3" opacity={.08}/><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="Conventional" name="Conventional"/><Bar dataKey="Optimized" name="Optimized"/></BarChart></ResponsiveContainer></Chart>
          <Chart title="Illustrative revenue split"><ResponsiveContainer width="100%" height={260}><PieChart><Pie data={[{name:'Farmer',value:r.farmer},{name:'Asterisk Climos',value:r.company}]} dataKey="value" nameKey="name" outerRadius={90} label>{[0,1].map(i=><Cell key={i}/>)}</Pie><Legend/><Tooltip/></PieChart></ResponsiveContainer></Chart>
        </div>
      </section>}
    </section>

    <section className="border-y border-[#1d352b] bg-[#0a1713]">
      <div className="mx-auto max-w-7xl px-5 py-16 md:py-20">
        <div className="grid gap-5 lg:grid-cols-[1fr_1.2fr] lg:items-center">
          <div><div className="text-[11px] font-bold tracking-[.16em] text-[#8bcfa6]">03 · EVIDENCE LAYER</div><h2 className="mt-3 text-3xl font-black tracking-tight md:text-5xl">Make the certainty visible.</h2><p className="mt-5 max-w-xl text-[#93aaa0]">The site now surfaces the same scientific limitation already in the project instead of burying it inside footer copy.</p></div>
          <div className="grid gap-3 sm:grid-cols-2">{[['SYNTHETIC','Demo datasets and assumptions'],['MODELLED','Deterministic scenario outputs'],['OBSERVED','Field observations when available'],['VERIFIED','Independent verification status']].map(([a,b])=><div key={a} className="rounded-2xl border border-[#244137] bg-[#0d1d18] p-5"><div className="text-xs font-black tracking-[.13em] text-[#8bcfa6]">{a}</div><div className="mt-3 text-sm leading-6 text-[#a6bcb2]">{b}</div></div>)}</div>
        </div>
      </div>
    </section>

    <section className="bg-[#f3f0e8] text-[#0a1712]">
      <div className="mx-auto max-w-7xl px-5 py-16 md:py-24">
        <div className="grid gap-10 lg:grid-cols-[.85fr_1.15fr] lg:items-center">
          <div><div className="text-[11px] font-black tracking-[.16em] text-[#5d7d68]">DIGITAL MRV</div><h2 className="mt-3 text-4xl font-black tracking-tight md:text-5xl">From field boundary to evidence chain.</h2><p className="mt-5 max-w-xl leading-7 text-[#5f7067]">Monitor, report, verify and preserve provenance as separate layers of the same story.</p></div>
          <div className="grid gap-3 sm:grid-cols-2">{[['Monitor',Satellite],['Report',Download],['Verify',ShieldCheck],['Provenance',Info]].map(([name,Icon])=>{const I=Icon as any;return <div key={name as string} className="rounded-2xl border border-[#d3d7ce] bg-[#fffdf7] p-6"><I size={20} className="text-[#5f8c6c]"/><h3 className="mt-4 text-xl font-black">{name as string}</h3><p className="mt-2 text-sm leading-6 text-[#6c7972]">Boundary, water, irrigation, soil, satellite observations, crop stage and QA/QC can sit inside one traceable workflow.</p></div>})}</div>
        </div>
      </div>
    </section>

    <footer className="border-t border-[#244137] bg-[#07120f]">
      <div className="mx-auto flex max-w-7xl flex-col gap-5 px-5 py-10 md:flex-row md:items-end md:justify-between">
        <div><div className="text-lg font-black tracking-[.12em]">CODE4NATURE</div><div className="mt-2 text-xs text-[#6f887d]">Climate intelligence for measurable rice-field impact.</div></div>
        <div className="max-w-xl text-xs leading-6 text-[#708980]">Prototype demonstration only. Calculated methane reductions, water savings, carbon-credit quantities and financial outcomes are illustrative and require project-specific MRV and verification.</div>
      </div>
    </footer>
  </main>
}

function HeroMetric({label,value,note}:{label:string,value:string,note:string}){return <div className="p-4"><div className="text-[10px] uppercase tracking-[.12em] text-[#71897f]">{label}</div><div className="mt-2 text-2xl font-black">{value}</div><div className="mt-1 text-[10px] text-[#71897f]">{note}</div></div>}
function MiniMetric({label,value}:{label:string,value:string}){return <div className="p-5"><div className="text-[10px] uppercase tracking-[.12em] text-[#6f887c]">{label}</div><div className="mt-2 font-bold">{value}</div></div>}
function JourneyStep({n,icon,title,text}:{n:string,icon:any,title:string,text:string}){return <div className="rounded-2xl border border-[#244137] bg-[#0d1d18] p-5"><div className="flex items-center justify-between"><span className="number-chip">{n}</span><span className="text-[#8bcfa6]">{icon}</span></div><h3 className="mt-5 font-bold">{title}</h3><p className="mt-2 text-sm leading-6 text-[#8fa99e]">{text}</p></div>}
function Slider({label,value,min,max,step,set}:{label:string,value:number,min:string,max:string,step:string,set:(v:number)=>void}){return <label className="block text-sm text-[#8ea79b]"><div className="flex items-center justify-between gap-3"><span>{label}</span><span className="font-bold text-[#edf7f2]">{label.split(': ')[1]}</span></div><input className="mt-3 w-full" type="range" min={min} max={max} step={step} value={value} onChange={e=>set(+e.target.value)}/></label>}
function Chart({title,children}:{title:string,children:any}){return <div className="glass p-5"><div className="flex items-center justify-between"><h3 className="font-bold">{title}</h3><span className="text-[9px] font-bold tracking-[.12em] text-[#6f887d]">ILLUSTRATIVE</span></div><div className="mt-4">{children}</div></div>}
