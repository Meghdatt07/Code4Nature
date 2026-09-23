'use client'

import { useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Droplets, Factory, Leaf, ShieldCheck, Download, Info } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import FarmMap from '../components/FarmMap'

type Scenario = 'Conservative' | 'Base Demo' | 'Custom'

const API = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
const INITIAL = { area: 10, baselineEmission: 6, projectEmission: 3.5, carbonPrice: 20, farmerShare: 60, waterReduction: 36.7 }

function calculate(v: typeof INITIAL) {
  const reduction = Math.max(0, v.baselineEmission - v.projectEmission) * v.area
  const gross = reduction * v.carbonPrice
  const farmer = gross * v.farmerShare / 100
  const acres = v.area * 2.47105381
  const waterBase = 4960000
  const waterProject = waterBase * (1 - v.waterReduction / 100)
  return { ...v, reduction, gross, farmer, company: gross - farmer, acres, waterSavedTotal: (waterBase - waterProject) * acres }
}

export default function Home() {
  const [values, setValues] = useState(INITIAL)
  const [scenario, setScenario] = useState<Scenario>('Base Demo')
  const [ran, setRan] = useState(false)
  const [farmArea, setFarmArea] = useState(INITIAL.area)
  const [apiError, setApiError] = useState('')
  const result = useMemo(() => calculate(values), [values])

  function update(key: keyof typeof INITIAL, value: number) {
    setValues((old) => ({ ...old, [key]: value }))
  }

  function useScenario(next: Scenario) {
    setScenario(next)
    if (next === 'Conservative') setValues({ area: 10, baselineEmission: 6, projectEmission: 4.5, carbonPrice: 15, farmerShare: 60, waterReduction: 20 })
    if (next === 'Base Demo') setValues(INITIAL)
  }

  function handleAreaChange(area: number) {
    setFarmArea(area)
    update('area', area)
  }

  async function downloadReport() {
    try {
      const response = await fetch(API + '/api/export/pdf')
      if (!response.ok) throw new Error()
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'carbonawd-demo-report.pdf'
      a.click()
      URL.revokeObjectURL(url)
      setApiError('')
    } catch {
      setApiError('Demo report download needs the FastAPI backend. The calculator itself remains available locally.')
    }
  }

  const chartData = [15, 20, 25, 30].map((price) => ({ price, value: result.reduction * price }))

  return (
    <main className="min-h-screen gridbg">
      <header className="sticky top-0 z-30 border-b border-[#244137] bg-[#07120f]/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
          <Link href="/" className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-xl bg-[#7ee2b1] font-black text-[#07120f]">C</div>
            <div><b>CARBONAWD</b><div className="text-[10px] tracking-[.24em] muted">CODE4NATURE • CLIMATE INTELLIGENCE</div></div>
          </Link>
          <nav className="hidden gap-7 text-sm muted md:flex">
            <a href="#technology">Technology</a><a href="#simulator">Simulator</a><a href="#mrv">MRV</a><a href="#research">Research</a>
          </nav>
          <a href="#simulator" className="rounded-full bg-[#7ee2b1] px-4 py-2 text-sm font-bold text-[#07120f]">Run Simulation</a>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-5 pb-20 pt-20">
        <div className="max-w-4xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-[#355e4d] bg-[#0d1d18] px-3 py-1 text-xs text-[#a8d7c1]">🌾 DEMO MODE • demo-v1.0</div>
          <h1 className="text-5xl font-black tracking-tight md:text-7xl">Measure. Optimize.<br/><span className="text-[#7ee2b1]">Reduce. Value.</span></h1>
          <p className="mt-7 max-w-3xl text-lg leading-8 muted">Transform rice-field water management into a transparent climate-impact and carbon-economics workflow using field evidence, remote-sensing pathways and explicit scenario assumptions.</p>
          <div className="mt-8 flex flex-wrap gap-3"><a href="#simulator" className="rounded-xl bg-[#7ee2b1] px-6 py-3 font-bold text-[#07120f]">Run Farm Simulation <ArrowRight className="ml-2 inline" size={17}/></a><Link href="/mrv" className="rounded-xl border border-[#355e4d] px-6 py-3">Open MRV</Link></div>
        </div>
        <div className="mt-16 grid gap-4 md:grid-cols-3">
          <Stat icon={<Droplets/>} title="Water" value={(result.waterSavedTotal / 1e6).toFixed(2) + 'M L'} sub="illustrative saving"/>
          <Stat icon={<Leaf/>} title="CO₂e" value={result.reduction.toFixed(2) + ' t'} sub="estimated reduction"/>
          <Stat icon={<Factory/>} title="Carbon value" value={'$' + result.gross.toFixed(0)} sub="illustrative gross value"/>
        </div>
      </section>

      <section id="technology" className="border-y border-[#1e372e] bg-[#091713] py-20"><div className="mx-auto max-w-7xl px-5"><SectionTitle eyebrow="THE LOGIC" title="From water management to climate value"/><div className="mt-10 grid gap-4 md:grid-cols-2"><Flow title="Current practice" items={['Continuous flooding','Waterlogged soil','Anaerobic conditions','Methane generation','GHG emissions']} bad/><Flow title="Climate-smart management" items={['Controlled irrigation','Dry-down periods','Reduced prolonged anaerobic conditions','Lower methane potential','Potential CO₂e reduction']}/></div></div></section>

      <section id="simulator" className="mx-auto max-w-7xl px-5 py-20">
        <SectionTitle eyebrow="CORE PRODUCT" title="Run Your Rice Field" text="Select a farm boundary, inspect the scenario, then translate the result into water, emissions and carbon-value metrics."/>
        <div className="mt-10 grid gap-5 lg:grid-cols-[1.15fr_.85fr]">
          <div className="glass overflow-hidden"><FarmMap onAreaChange={handleAreaChange}/><div className="grid grid-cols-3 gap-3 border-t border-[#244137] p-5 text-sm"><Metric label="Farm area" value={farmArea.toFixed(2) + ' ha'}/><Metric label="Acres" value={result.acres.toFixed(2)}/><Metric label="Mode" value="SIMULATED"/></div></div>
          <div className="glass p-6"><div className="flex items-center justify-between"><h3 className="text-xl font-bold">Field parameters</h3><span className="rounded-full bg-[#183a2d] px-2 py-1 text-[10px]">USER INPUT</span></div>
            <Range label="Farm area" value={values.area} min={0.5} max={50} step={0.1} unit="ha" onChange={(v) => update('area', v)}/>
            <Range label="Baseline emissions" value={values.baselineEmission} min={3} max={8} step={0.1} unit="tCO₂e/ha" onChange={(v) => update('baselineEmission', v)}/>
            <Range label="Project emissions" value={values.projectEmission} min={1} max={8} step={0.1} unit="tCO₂e/ha" onChange={(v) => update('projectEmission', v)}/>
            <Range label="Water reduction" value={values.waterReduction} min={0} max={70} step={0.1} unit="%" onChange={(v) => update('waterReduction', v)}/>
            <div className="mt-6 grid grid-cols-3 gap-2">{[15,20,25].map((p) => <button key={p} onClick={() => update('carbonPrice', p)} className={"rounded-lg border px-3 py-2 text-sm " + (values.carbonPrice === p ? 'border-[#7ee2b1] bg-[#16352a]' : 'border-[#244137]')}>{'$' + p}</button>)}</div>
            <Range label="Farmer / FPO share" value={values.farmerShare} min={0} max={100} step={1} unit="%" onChange={(v) => update('farmerShare', v)}/>
            <div className="mt-6 grid grid-cols-3 gap-2"><button onClick={() => useScenario('Conservative')} className="rounded-lg border border-[#244137] px-2 py-2 text-xs">Conservative</button><button onClick={() => useScenario('Base Demo')} className="rounded-lg border border-[#7ee2b1] px-2 py-2 text-xs">Base Demo</button><button onClick={() => { setScenario('Custom'); setRan(false) }} className="rounded-lg border border-[#244137] px-2 py-2 text-xs">Custom</button></div>
            <button onClick={() => setRan(true)} className="mt-6 w-full rounded-xl bg-[#7ee2b1] py-3 font-bold text-[#07120f]">RUN FIELD SIMULATION</button><button onClick={downloadReport} className="mt-2 w-full rounded-xl border border-[#355e4d] py-3"><Download className="mr-2 inline" size={16}/>Download Demo Report</button>
            {apiError && <p className="mt-3 text-xs text-amber-200">{apiError}</p>}
          </div>
        </div>
      </section>

      {ran && <section className="mx-auto max-w-7xl px-5 pb-20"><div className="mb-5 flex items-center justify-between"><div><div className="text-xs tracking-[.2em] text-[#7ee2b1]">RESULTS • {scenario.toUpperCase()}</div><h2 className="text-3xl font-bold">Simulation dashboard</h2></div><span className="rounded-full border border-[#5c4930] bg-[#241c10] px-3 py-1 text-xs text-[#e8c98f]">SIMULATED · ILLUSTRATIVE</span></div><div className="grid gap-3 md:grid-cols-4">
        <Card title="Farm Area" value={result.area.toFixed(2) + ' ha'}/><Card title="Water Saved" value={(result.waterSavedTotal/1e6).toFixed(2) + 'M L'}/><Card title="Estimated Reduction" value={result.reduction.toFixed(2) + ' tCO₂e'}/><Card title="Potential Credits" value={result.reduction.toFixed(2)}/><Card title="Carbon Price" value={'$' + result.carbonPrice + '/t'}/><Card title="Gross Value" value={'$' + result.gross.toFixed(2)}/><Card title="Farmer Share" value={'$' + result.farmer.toFixed(2)}/><Card title="CarbonAWD Share" value={'$' + result.company.toFixed(2)}/>
      </div><div className="mt-5 glass p-6"><h3 className="font-bold">Carbon price sensitivity</h3><div className="mt-4 h-64"><ResponsiveContainer width="100%" height="100%"><AreaChart data={chartData}><XAxis dataKey="price" stroke="#9ab3a8"/><YAxis stroke="#9ab3a8"/><Tooltip/><Area type="monotone" dataKey="value" stroke="#7ee2b1" fill="#7ee2b1" fillOpacity={0.12}/></AreaChart></ResponsiveContainer></div></div></section>}

      <section id="mrv" className="border-y border-[#1e372e] bg-[#091713] py-20"><div className="mx-auto max-w-7xl px-5"><SectionTitle eyebrow="DIGITAL MRV" title="Measure what is simulated—and what would need field evidence."/><div className="mt-10 grid gap-4 md:grid-cols-4">{[['Monitor','Boundary · water · irrigation · soil · satellite · crop stage'],['Report','Baseline · project · water · emissions · CO₂e'],['Verify','Evidence · QA/QC · validation · verification'],['Provenance','Value · unit · source · type · model · timestamp']].map((item) => <div className="glass p-6" key={item[0]}><ShieldCheck className="text-[#7ee2b1]"/><h3 className="mt-4 font-bold">{item[0]}</h3><p className="mt-2 text-sm muted">{item[1]}</p><span className="mt-5 inline-block rounded-full bg-[#241c10] px-2 py-1 text-[10px] text-[#e8c98f]">DEMO DATA</span></div>)}</div></div></section>

      <section id="research" className="mx-auto max-w-7xl px-5 py-20"><SectionTitle eyebrow="SCIENCE & CONTEXT" title="Research and industry references"/><div className="mt-8 grid gap-4 md:grid-cols-2">{[['Rice methane & AWD','Continuously flooded rice systems can create anaerobic conditions associated with methane formation; AWD periodically drains and refloods fields.'],['Remote sensing','Ground observations can provide calibration points while Sentinel‑1 provides a pathway for broader spatial evidence.'],['Carbon markets','Potential credits and revenue are scenario values until project-specific methodology, MRV and verification requirements are satisfied.'],['Policy & FPOs','The farmer, FPO and MRV-provider layers are separated so financial incentives do not get confused with certification.']].map((item)=><div className="glass p-6" key={item[0]}><div className="flex items-start justify-between"><h3 className="font-bold">{item[0]}</h3><Info size={17} className="text-[#7ee2b1]"/></div><p className="mt-3 text-sm leading-6 muted">{item[1]}</p></div>)}</div></section>
      <footer className="border-t border-[#244137] py-10"><div className="mx-auto max-w-7xl px-5 text-sm muted"><b className="text-white">CARBONAWD</b><p className="mt-3 max-w-4xl">Code4Nature prototype. Calculated methane reductions, water savings, carbon-credit quantities and financial outcomes are illustrative unless identified as measured or independently published values.</p></div></footer>
    </main>
  )
}

function Stat({icon,title,value,sub}:{icon:any,title:string,value:string,sub:string}){return <div className="glass p-5"><div className="text-[#7ee2b1]">{icon}</div><div className="mt-5 text-3xl font-black">{value}</div><div className="font-bold">{title}</div><div className="text-xs muted">{sub}</div></div>}
function SectionTitle({eyebrow,title,text}:{eyebrow:string,title:string,text?:string}){return <div><div className="text-xs tracking-[.2em] text-[#7ee2b1]">{eyebrow}</div><h2 className="mt-2 text-3xl font-black md:text-4xl">{title}</h2>{text&&<p className="mt-3 max-w-2xl muted">{text}</p>}</div>}
function Flow({title,items,bad}:{title:string,items:string[],bad?:boolean}){return <div className="glass p-6"><div className="flex items-center justify-between"><h3 className="font-bold">{title}</h3><span className="text-xs muted">{bad?'BASELINE':'PROJECT SCENARIO'}</span></div><div className="mt-6 space-y-3">{items.map((x,i)=><div className="flex items-center gap-3" key={x}><div className="grid h-7 w-7 place-items-center rounded-full border border-[#355e4d] text-xs">{i+1}</div><span className="text-sm">{x}</span></div>)}</div></div>}
function Metric({label,value}:{label:string,value:string}){return <div><div className="text-xs muted">{label}</div><b>{value}</b></div>}
function Card({title,value}:{title:string,value:string}){return <div className="glass p-5"><div className="text-xs muted">{title}</div><div className="mt-2 text-2xl font-black">{value}</div></div>}
function Range({label,value,min,max,step,unit,onChange}:{label:string,value:number,min:number,max:number,step:number,unit:string,onChange:(v:number)=>void}){return <label className="mt-5 block text-sm muted">{label}: <b className="text-white">{value.toFixed(step<1?1:0)} {unit}</b><input type="range" min={min} max={max} step={step} value={value} onChange={(e)=>onChange(Number(e.target.value))} className="mt-2 w-full"/></label>}
