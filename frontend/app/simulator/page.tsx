'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { Activity, ArrowRight, Leaf, Satellite } from 'lucide-react';
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

  return <main className="min-h-screen grid-bg">
    <div className="mx-auto max-w-7xl px-5 py-14">
      <DataBadge type="SIMULATED"/>
      <div className="mt-5 text-xs tracking-[.2em] text-white/30">FARM SIMULATOR</div>
      <h1 className="mt-3 text-5xl font-bold">Run your rice field scenario.</h1>
      <p className="mt-5 max-w-3xl text-lg leading-8 text-white/55">
        Calculate illustrative methane abatement, CO₂e opportunity, water savings and carbon value using the same rice-MRV reference standard as Digital MRV.
      </p>

      <div className="mt-6 rounded-2xl border border-[#8bcfa6]/30 bg-[#8bcfa6]/5 p-5">
        <div className="text-xs tracking-[.18em] text-[#8bcfa6]">DIGITAL MRV REFERENCE STANDARD</div>
        <div className="mt-3 grid gap-3 sm:grid-cols-3">
          <Metric title="CH₄ abatement" value={RICE_CH4_ABATEMENT_KG_PER_HA+' kg/ha/season'}/>
          <Metric title="CH₄ GWP100" value={String(CH4_GWP100)}/>
          <Metric title="CO₂e opportunity" value={RICE_CO2E_T_PER_HA_PER_SEASON.toFixed(2)+' t/ha/season'}/>
        </div>
        <p className="mt-3 text-xs text-white/40">
          This keeps the simulator aligned with Digital MRV: area × 120 kg CH₄/ha × 28 / 1000 = CO₂e tonnes.
        </p>
      </div>

      <div className="mt-10 grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
        <Card className="overflow-hidden p-2">
          <FarmMap value={geometry} onChange={(g,a)=>{setGeometry(g);if(a>0)setArea(a)}}/>
        </Card>

        <Card>
          <div className="text-xs tracking-[.18em] text-white/30">FIELD PARAMETERS</div>

          <Range label="Farm area" value={area} min={.5} max={100} step={.1} unit="ha" set={setArea}/>

          <div className="mt-5 rounded-xl border border-white/10 p-4">
            <div className="text-sm text-white/55">Rice methane-abatement standard</div>
            <div className="mt-1 text-lg font-bold">{RICE_CH4_ABATEMENT_KG_PER_HA} kg CH₄/ha/season</div>
            <div className="mt-1 text-xs text-white/35">Fixed to match Digital MRV.</div>
          </div>

          <Range label="Water reduction" value={waterPct} min={0} max={70} step={.1} unit="%" set={setWaterPct}/>
          <Range label="Carbon price" value={price} min={1} max={150} step={.5} unit="USD/t" set={setPrice}/>
          <Range label="Farmer/FPO share" value={farmer} min={0} max={100} step={1} unit="%" set={setFarmer}/>

          <div className="mt-5 grid grid-cols-3 gap-2">
            <button onClick={()=>scenario('CONSERVATIVE')} className="rounded-lg border border-white/10 p-2 text-xs">Conservative</button>
            <button onClick={()=>scenario('BASE DEMO')} className="rounded-lg border border-[#8bcfa6] p-2 text-xs">Base Demo</button>
            <button onClick={()=>setMode('CUSTOM')} className="rounded-lg border border-white/10 p-2 text-xs">Custom</button>
          </div>

          <button onClick={()=>setResult({...calc,geometry,mode})} className="mt-5 w-full rounded-xl bg-[#dcefe5] py-3 font-bold text-[#0a1a13]">
            RUN FIELD SIMULATION
          </button>
        </Card>
      </div>

      {result&&<section className="mt-6">
        <div className="mb-4 flex items-center gap-3">
          <Activity className="text-[#8bcfa6]"/>
          <div>
            <h2 className="text-2xl font-bold">Simulation result</h2>
            <div className="text-xs text-white/35">{result.mode} • illustrative</div>
          </div>
        </div>

        <div className="grid gap-3 md:grid-cols-4">
          <Metric title="CH₄ reduction" value={result.methaneKg.toFixed(0)+' kg/season'}/>
          <Metric title="CH₄ / CO₂e reduction" value={result.reduction.toFixed(2)+' tCO₂e'}/>
          <Metric title="Potential credits" value={result.credits.toFixed(2)+' tCO₂e'}/>
          <Metric title="Gross value" value={'$'+result.gross.toFixed(2)}/>
          <Metric title="Farmer / FPO" value={'$'+result.farmer.toFixed(2)}/>
          <Metric title="MRV / Company" value={'$'+result.company.toFixed(2)}/>
          <Metric title="Farm boundary" value={geometry?'Selected':'Manual area'}/>
          <Metric title="MRV standard" value="120 kg CH₄/ha"/>
        </div>

        <div className="mt-5 flex flex-wrap gap-3">
          <Link href="/mrv"><Button variant="outline">Open Digital MRV <ArrowRight size={15}/></Button></Link>
          <Link href="/carbon"><Button>Open Carbon Economics <Leaf size={15}/></Button></Link>
          <Link href="/technology"><Button variant="ghost">View Technology <Satellite size={15}/></Button></Link>
        </div>
      </section>}
    </div>
  </main>
}

function Range({label,value,min,max,step,unit,set}:{label:string;value:number;min:number;max:number;step:number;unit:string;set:(n:number)=>void}){
  return <label className="mt-5 block text-sm text-white/55">
    {label}: <b className="text-white">{value.toFixed(step<1?1:0)} {unit}</b>
    <input type="range" min={min} max={max} step={step} value={value} onChange={e=>set(Number(e.target.value))} className="mt-2 w-full"/>
  </label>
}

function Metric({title,value}:{title:string;value:string}){
  return <div className="glass rounded-2xl p-5">
    <div className="text-xs text-white/35">{title}</div>
    <div className="mt-2 text-2xl font-bold">{value}</div>
  </div>
}
