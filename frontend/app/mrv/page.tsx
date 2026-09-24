'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { Activity, ArrowRight, Calculator, CheckCircle2, Mail, Phone, ShieldCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';

type EquipmentStatus = 'PURCHASED' | 'NOT_PURCHASED';

export default function MRV() {
  const [equipment,setEquipment]=useState<EquipmentStatus>('PURCHASED');
  const [vv,setVv]=useState(-17.6);
  const [vh,setVh]=useState(-23.8);
  const [ran,setRan]=useState(false);
  const [showTechnical,setShowTechnical]=useState(false);

  const wetness=useMemo(()=>Math.max(0,Math.min(100,50+(vv+15)*7)),[vv]);

  return <main className="min-h-screen grid-bg p-8">
    <div className="mx-auto max-w-6xl pt-10 pb-20">
      <Link href="/" className="text-[#7ee2b1]">← Asterisk Climos</Link>
      <div className="mt-14 text-xs tracking-[.2em] text-[#7ee2b1]">DIGITAL MRV · FOR EQUIPMENT USERS</div>
      <h1 className="mt-3 text-5xl font-black">Monitor. Report. Verify.</h1>
      <p className="mt-5 max-w-3xl text-lg leading-8 text-white/55">Equipment-connected users can trigger the MRV calculation, inspect the result and reveal the technical steps behind it when needed.</p>

      <div className="mt-8 rounded-2xl border border-[#8bcfa6]/25 bg-[#8bcfa6]/5 p-5">
        <div className="text-xs tracking-[.18em] text-[#8bcfa6]">WHICH WORKFLOW IS RIGHT FOR YOU?</div>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          <button onClick={()=>setEquipment('PURCHASED')} className={`rounded-2xl border p-5 text-left ${equipment==='PURCHASED'?'border-[#8bcfa6] bg-[#8bcfa6]/10':'border-white/10'}`}>
            <div className="text-xs tracking-[.16em] text-[#8bcfa6]">PURCHASED OUR EQUIPMENT</div>
            <div className="mt-2 text-xl font-bold">Digital MRV</div>
            <div className="mt-1 text-sm text-white/55">Your section: equipment measurements + satellite evidence + MRV calculation.</div>
          </button>
          <button onClick={()=>setEquipment('NOT_PURCHASED')} className={`rounded-2xl border p-5 text-left ${equipment==='NOT_PURCHASED'?'border-[#8bcfa6] bg-[#8bcfa6]/10':'border-white/10'}`}>
            <div className="text-xs tracking-[.16em] text-white/45">NOT PURCHASED</div>
            <div className="mt-2 text-xl font-bold">Farm Simulator</div>
            <div className="mt-1 text-sm text-white/55">Explore scenarios first; contact us to discuss equipment and field onboarding.</div>
          </button>
        </div>
        {equipment==='NOT_PURCHASED'&&<div className="mt-4 flex flex-wrap gap-3"><Link href="/simulator"><Button>Open Farm Simulator <ArrowRight size={15}/></Button></Link><Link href="/contact"><Button variant="outline">Book a consultation <ArrowRight size={15}/></Button></Link></div>}
      </div>

      {equipment==='PURCHASED' ? <section className="mt-8">
        <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]">
          <div className="glass rounded-2xl p-6">
            <div className="text-xs tracking-[.18em] text-white/30">EQUIPMENT DATA</div>
            <div className="mt-5 grid gap-4">
              <label className="text-sm text-white/55">VV mean (dB)<input value={vv} onChange={e=>setVv(Number(e.target.value))} type="number" step=".01" className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 p-3 text-white"/></label>
              <label className="text-sm text-white/55">VH mean (dB)<input value={vh} onChange={e=>setVh(Number(e.target.value))} type="number" step=".01" className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 p-3 text-white"/></label>
            </div>
            <button onClick={()=>{setRan(true);setShowTechnical(false)}} className="mt-5 w-full rounded-xl bg-[#8bcfa6] py-3 font-bold text-[#07130f]"><Calculator className="mr-2 inline" size={17}/>RUN MRV CALCULATION</button>
            <div className="mt-4 text-xs text-white/35">The calculation runs in the browser; the technical working is hidden until you request it.</div>
          </div>

          <div className="glass rounded-2xl p-6">
            <div className="flex items-center gap-2 text-[#8bcfa6]"><ShieldCheck size={18}/><div className="text-xs tracking-[.18em]">EQUIPMENT-CONNECTED WORKFLOW</div></div>
            <h2 className="mt-3 text-2xl font-bold">Your field evidence, translated into an MRV signal.</h2>
            <p className="mt-3 text-sm leading-7 text-white/55">The result below is an MRV proxy. It should be interpreted with project-specific calibration and verification rather than as a certified carbon-credit measurement by itself.</p>
            {ran&&<div className="mt-6 grid gap-3 md:grid-cols-3">
              <Metric title="Relative wetness" value={wetness.toFixed(1)+'%'}/>
              <Metric title="VV mean" value={vv.toFixed(2)+' dB'}/>
              <Metric title="VH mean" value={vh.toFixed(2)+' dB'}/>
            </div>}
            {ran&&<div className="mt-5 rounded-xl border border-[#8bcfa6]/25 bg-[#8bcfa6]/5 p-4 text-sm"><CheckCircle2 className="mr-2 inline text-[#8bcfa6]" size={16}/>MRV calculation completed.</div>}
          </div>
        </div>

        {ran&&<div className="mt-6">
          <button onClick={()=>setShowTechnical(!showTechnical)} className="rounded-xl border border-white/10 px-4 py-3 text-sm"><Activity className="mr-2 inline" size={16}/>{showTechnical?'Hide':'Show'} technical calculation</button>
          {showTechnical&&<Card title="Behind the scenes">
            <p><b>1.</b> VV is used to derive a relative wetness proxy for this demonstrator.</p>
            <p className="mt-2"><b>Formula:</b> relative wetness = clamp(50 + (VV + 15) × 7, 0, 100).</p>
            <p className="mt-2"><b>2.</b> Current VV = {vv.toFixed(2)} dB → relative wetness = {wetness.toFixed(1)}%.</p>
            <p className="mt-2"><b>3.</b> VH mean = {vh.toFixed(2)} dB. <b>VH (cross-polarized backscatter)</b> records the radar signal returned with a changed polarization and complements VV when interpreting vegetation and surface scattering.</p>
            <p className="mt-2"><b>4.</b> These signals are inputs to the evidence chain; field calibration is needed before treating the proxy as an absolute soil-moisture measurement.</p>
          </Card>}
        </div>}
      </section> : <section className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-8">
        <div className="text-xs tracking-[.18em] text-[#8bcfa6]">NOT PURCHASED</div>
        <h2 className="mt-3 text-3xl font-bold">Start with the Farm Simulator.</h2>
        <p className="mt-3 max-w-2xl text-sm leading-7 text-white/55">You can model the opportunity without our equipment. When you are ready to move from scenario modelling to equipment-backed field evidence, book a consultation with Code4Nature.</p>
        <div className="mt-6 flex flex-wrap gap-3"><Link href="/simulator"><Button>Open Farm Simulator <ArrowRight size={15}/></Button></Link><Link href="/contact"><Button variant="outline">Book consulting <ArrowRight size={15}/></Button></Link></div>
      </section>}

      <div className="mt-8 rounded-2xl border border-white/10 bg-[#0c1713] p-6">
        <div className="text-xs tracking-[.18em] text-[#8bcfa6]">CONSULTING</div>
        <h2 className="mt-2 text-2xl font-bold">Need equipment onboarding or project MRV support?</h2>
        <p className="mt-2 text-sm text-white/55">Book a consultation for farm onboarding, data setup, MRV workflows and project design.</p>
        <div className="mt-5 flex flex-wrap gap-5 text-sm text-white/60">
          <a href="mailto:hello@code4nature.earth" className="hover:text-white"><Mail className="mr-2 inline" size={16}/>hello@code4nature.earth</a>
          <span><Phone className="mr-2 inline" size={16}/>Phone: add your consulting number</span>
        </div>
        <div className="mt-5 rounded-xl border border-white/10 bg-white/5 p-4 text-xs text-white/40">Your phone number is intentionally left unfilled here because no business phone number is present in the repository.</div>
      </div>
    </div>
  </main>
}

function Metric({title,value}:{title:string;value:string}){return <div className="rounded-2xl border border-white/10 bg-white/5 p-5"><div className="text-xs text-white/35">{title}</div><div className="mt-2 text-2xl font-bold">{value}</div></div>}
function Card({title,children}:{title:string;children:React.ReactNode}){return <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 p-6"><h3 className="text-lg font-bold">{title}</h3><div className="mt-3 text-sm leading-7 text-white/60">{children}</div></div>}
