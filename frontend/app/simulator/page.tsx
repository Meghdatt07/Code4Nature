'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { Activity, ArrowRight, Check, Info, Leaf, MapPinned, Satellite, ShieldCheck } from 'lucide-react';
import { FarmMap } from '@/components/farm-map/farm-map';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { DataBadge } from '@/components/shared/data-badge';
import {
  CH4_GWP100,
  RICE_CH4_ABATEMENT_KG_PER_HA,
  RICE_CO2E_T_PER_HA_PER_SEASON,
  demoWater,
  revenue,
  standardRiceEmission,
} from '@/lib/calculations';

export default function Simulator(){
  const [area,setArea]=useState(10);
  const [price,setPrice]=useState(20);
  const [farmer,setFarmer]=useState(60);
  const [waterPct,setWaterPct]=useState(36.7);
  const [mode,setMode]=useState<'CONSERVATIVE'|'BASE DEMO'|'CUSTOM'>('BASE DEMO');
  const [geometry,setGeometry]=useState<any>(null);
  const [result,setResult]=useState<any>(null);

  const calc=useMemo(()=>{
    const e=standardRiceEmission(area);
    const w=demoWater(area,4_960_000,4_960_000*(1-waterPct/100));
    const r=revenue(e.reduction,price,farmer);
    return{
      ...e,
      ...w,
      ...r,
      credits:e.reduction
    };
  },[area,waterPct,price,farmer]);

  function scenario(x:'CONSERVATIVE'|'BASE DEMO'){
    setMode(x);
    if(x==='CONSERVATIVE'){
      setWaterPct(20);
      setPrice(15);
      setFarmer(60);
    }else{
      setArea(10);
      setWaterPct(36.7);
      setPrice(20);
      setFarmer(60);
    }
  }

  return <main className="min-h-screen bg-[#07120f] text-[#edf7f2]">
    <section className="border-b border-[#1d352b] bg-[#0a1713]">
      <div className="mx-auto max-w-7xl px-5 pb-8 pt-12 md:pb-12 md:pt-16">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <DataBadge type="SIMULATED"/>
            <div className="mt-5 text-[11px] font-bold tracking-[.18em] text-[#8bcfa6]">FARM SIMULATOR</div>
            <h1 className="mt-3 max-w-4xl text-balance text-4xl font-black tracking-[-.04em] md:text-6xl">Run your rice field scenario.</h1>
            <p className="mt-5 max-w-3xl text-base leading-7 text-[#93aaa0] md:text-lg">Calculate illustrative methane abatement, CO₂e opportunity, water savings and carbon value using the same rice-MRV reference standard as Digital MRV.</p>
          </div>
          <div className="rounded-2xl border border-[#355e4d] bg-[#0d1d18] p-4 text-sm"><div className="text-[10px] font-bold tracking-[.14em] text-[#8bcfa6]">CURRENT MODE</div><div className="mt-1 font-bold">{mode}</div></div>
        </div>

        <div className="mt-8 grid grid-cols-4 gap-2 rounded-2xl border border-[#244137] bg-[#0d1d18] p-2">
          {['01 Field','02 Inputs','03 Results','04 Evidence'].map((x,i)=><div key={x} className={'rounded-xl px-3 py-3 text-center text-xs font-bold '+(i<3?'text-[#dbece3] bg-[#8bcfa6]/5':'text-[#708980]')}>{x}</div>)}
        </div>
      </div>
    </section>

    <section className="mx-auto max-w-7xl px-5 py-8 md:py-12">
      <div className="rounded-2xl border border-[#8bcfa6]/20 bg-[#8bcfa6]/5 p-5 md:p-6">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div><div className="flex items-center gap-2 text-[10px] font-black tracking-[.18em] text-[#8bcfa6]"><ShieldCheck size={14}/> DIGITAL MRV REFERENCE STANDARD</div><p className="mt-2 max-w-2xl text-sm leading-6 text-[#9eb6aa]">The interface surfaces the existing reference inputs without changing them.</p></div>
          <div className="grid gap-3 sm:grid-cols-3 lg:min-w-[520px]">
            <Metric title="CH₄ abatement" value={RICE_CH4_ABATEMENT_KG_PER_HA+' kg/ha/season'}/>
            <Metric title="CH₄ GWP100" value={String(CH4_GWP100)}/>
            <Metric title="CO₂e opportunity" value={RICE_CO2E_T_PER_HA_PER_SEASON.toFixed(2)+' t/ha/season'}/>
          </div>
        </div>
        <div className="mt-4 inline-flex items-center gap-2 rounded-full border border-[#355e4d] bg-[#07120f]/40 px-3 py-2 text-xs text-[#8ea79a]"><Info size={13}/> This keeps the simulator aligned with Digital MRV: area × 120 kg CH₄/ha × 28 / 1000 = CO₂e tonnes.</div>
      </div>

      <div className="mt-8 grid gap-5 lg:grid-cols-[1.18fr_.82fr] lg:items-start">
        <Card className="overflow-hidden p-2 lg:sticky lg:top-28">
          <div className="flex items-center justify-between px-3 pb-3 pt-1"><div><div className="text-[10px] font-bold tracking-[.15em] text-[#8bcfa6]">STEP 01</div><div className="mt-1 text-sm font-bold">Define the field</div></div><div className="inline-flex items-center gap-2 text-xs text-[#7f988c]"><MapPinned size={14}/> {geometry?'Boundary selected':'Manual area'}</div></div>
          <FarmMap value={geometry} onChange={(g,a)=>{setGeometry(g);if(a>0)setArea(a)}}/>
        </Card>

        <Card className="p-6">
          <div className="text-[10px] font-bold tracking-[.16em] text-[#8bcfa6]">STEP 02</div>
          <h2 className="mt-2 text-2xl font-black">Tune the scenario</h2>

          <div className="mt-6 grid gap-5">
            <Range label="Farm area" value={area} min={.5} max={100} step={.1} unit="ha" set={setArea}/>
            <div className="rounded-2xl border border-[#244137] bg-[#0a1713] p-4"><div className="flex items-start justify-between gap-4"><div><div className="text-sm text-[#91a99e]">Rice methane-abatement standard</div><div className="mt-1 text-lg font-bold">{RICE_CH4_ABATEMENT_KG_PER_HA} kg CH₄/ha/season</div></div><div className="rounded-full border border-[#355e4d] px-2.5 py-1 text-[9px] font-bold tracking-[.1em] text-[#8bcfa6]">FIXED</div></div><div className="mt-2 text-xs text-[#677f74]">Fixed to match Digital MRV.</div></div>
            <Range label="Water reduction" value={waterPct} min={0} max={70} step={.1} unit="%" set={setWaterPct}/>
            <Range label="Carbon price" value={price} min={1} max={150} step={.5} unit="USD/t" set={setPrice}/>
            <Range label="Farmer/FPO share" value={farmer} min={0} max={100} step={1} unit="%" set={setFarmer}/>
          </div>

          <div className="mt-6">
            <div className="text-[10px] font-bold tracking-[.16em] text-[#7f988d]">PRESET SCENARIOS</div>
            <div className="mt-3 grid grid-cols-3 gap-2">
              {(['CONSERVATIVE','BASE DEMO','CUSTOM'] as const).map(x=><button key={x} onClick={()=>x==='CUSTOM'?setMode('CUSTOM'):scenario(x)} className={'rounded-xl border px-3 py-3 text-xs font-bold transition '+(mode===x?'border-[#8bcfa6] bg-[#8bcfa6]/10 text-[#e0f2e7]':'border-[#355e4d] text-[#91aaa0] hover:bg-white/[.03]')}>{x}</button>)}
            </div>
          </div>

          <button onClick={()=>setResult({...calc,geometry,mode})} className="mt-6 w-full rounded-xl bg-[#8bcfa6] py-3.5 font-black tracking-wide text-[#07120f]">RUN FIELD SIMULATION <ArrowRight className="ml-2 inline" size={16}/></button>
          <div className="mt-3 flex items-center gap-2 text-xs text-[#71897e]"><Check size={14} className="text-[#8bcfa6]"/> Inputs remain unchanged; this update is UI-only.</div>
        </Card>
      </div>

      {result&&<section className="mt-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between"><div><div className="text-[10px] font-bold tracking-[.16em] text-[#8bcfa6]">STEP 03 · OUTPUT</div><div className="mt-2 flex items-center gap-3"><Activity className="text-[#8bcfa6]"/><div><h2 className="text-2xl font-black">Simulation result</h2><div className="text-xs text-[#728a80]">{result.mode} • illustrative</div></div></div></div><div className="inline-flex items-center gap-2 rounded-full border border-[#355e4d] px-3 py-2 text-xs text-[#8ea69b]"><Info size={13}/> Modelled / illustrative</div></div>

        <div className="mt-5 grid gap-3 md:grid-cols-4">
          <Metric title="CH₄ reduction" value={result.methaneKg.toFixed(0)+' kg/season'}/>
          <Metric title="CH₄ / CO₂e reduction" value={result.reduction.toFixed(2)+' tCO₂e'}/>
          <Metric title="Potential credits" value={result.credits.toFixed(2)+' tCO₂e'}/>
          <Metric title="Gross value" value={'$'+result.gross.toFixed(2)}/>
          <Metric title="Farmer / FPO" value={'$'+result.farmer.toFixed(2)}/>
          <Metric title="MRV / Company" value={'$'+result.company.toFixed(2)}/>
          <Metric title="Farm boundary" value={geometry?'Selected':'Manual area'}/>
          <Metric title="MRV standard" value="120 kg CH₄/ha"/>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-3">
          <Link href="/mrv"><Button variant="outline" className="w-full">Open Digital MRV <ArrowRight size={15}/></Button></Link>
          <Link href="/carbon"><Button className="w-full">Open Carbon Economics <Leaf size={15}/></Button></Link>
          <Link href="/technology"><Button variant="ghost" className="w-full">View Technology <Satellite size={15}/></Button></Link>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          <Evidence title="Field boundary" value={geometry?'Selected':'Manual area'} state="CURRENT INPUT"/>
          <Evidence title="Scenario output" value="Deterministic model" state="MODELLED"/>
          <Evidence title="Credit status" value="Verification required" state="NOT VERIFIED"/>
        </div>
      </section>}
    </section>
  </main>
}

function Range({label,value,min,max,step,unit,set}:{label:string;value:number;min:number;max:number;step:number;unit:string;set:(n:number)=>void}){
  return <label className="block"><div className="flex items-center justify-between gap-3 text-sm text-[#8fa79c]"><span>{label}</span><b className="text-[#edf7f2]">{value.toFixed(step<1?1:0)} {unit}</b></div><input type="range" min={min} max={max} step={step} value={value} onChange={e=>set(Number(e.target.value))} className="mt-3 w-full"/></label>
}
function Metric({title,value}:{title:string;value:string}){return <div className="glass rounded-2xl p-5"><div className="text-[10px] uppercase tracking-[.1em] text-[#6f887d]">{title}</div><div className="mt-2 text-xl font-black tracking-tight">{value}</div></div>}
function Evidence({title,value,state}:{title:string;value:string;state:string}){return <div className="rounded-2xl border border-[#244137] bg-[#0d1d18] p-5"><div className="flex items-center justify-between gap-4"><div className="text-sm font-bold">{title}</div><span className="rounded-full border border-[#355e4d] px-2 py-1 text-[9px] font-bold tracking-[.1em] text-[#8bcfa6]">{state}</span></div><div className="mt-3 text-sm text-[#9eb6aa]">{value}</div></div>}
