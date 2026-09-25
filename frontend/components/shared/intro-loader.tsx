'use client'

import { useEffect, useState } from 'react'

export function IntroLoader(){
  const [phase,setPhase] = useState<'loading'|'welcome'|'entered'>('loading')

  useEffect(()=>{
    document.body.classList.add('intro-lock')
    const timer = window.setTimeout(()=>setPhase('welcome'),4000)
    return ()=>window.clearTimeout(timer)
  },[])

  useEffect(()=>{
    if(phase==='entered') document.body.classList.remove('intro-lock')
  },[phase])

  if(phase==='entered') return null

  return <div className={`site-intro${phase==='entered'?' is-entered':''}`} data-phase={phase} aria-label="Asterisk Climos introduction">
    <div className="intro-loading-screen" aria-hidden={phase!=='loading'}>
      <div className="intro-loading-brand">CODE<span>4</span>NATURE</div>
      <div className="intro-scene-next">
        <div className="intro-panel-next flooded">
          <div className="intro-panel-tag">FLOODED SOIL</div>
          <div className="intro-waterline-next high"/>
          <div className="intro-soil-next"/>
          <div className="intro-root-next"><i/><i/><i/></div>
          <div className="intro-plant-next tall"><b/><b/><b/><b/></div>
          <div className="intro-bubbles-next many"><i/><i/><i/><i/><i/><i/><i/></div>
          <div className="intro-ch4-next">MORE CH₄ POTENTIAL</div>
        </div>
        <div className="intro-panel-next dry">
          <div className="intro-panel-tag">AWD / DRY-DOWN</div>
          <div className="intro-waterline-next low"/>
          <div className="intro-soil-next"/>
          <div className="intro-root-next"><i/><i/><i/></div>
          <div className="intro-plant-next"><b/><b/><b/><b/></div>
          <div className="intro-bubbles-next few"><i/><i/></div>
          <div className="intro-ch4-next">LOWER CH₄ POTENTIAL</div>
        </div>
      </div>
      <div className="intro-loading-copy"><span>FIELD INTELLIGENCE</span><h2>Water changes the story beneath the crop.</h2><p>Visualising the methane pathway from flooded conditions to controlled dry-down.</p></div>
      <div className="intro-progress-next"><span/></div>
      <div className="intro-status-next">CALIBRATING WATER · METHANE · EVIDENCE…</div>
    </div>

    <div className="intro-welcome-screen" aria-hidden={phase!=='welcome'}>
      <div className="intro-welcome-glow-next"/>
      <span className="intro-welcome-kicker-next">CODE4NATURE PRESENTS</span>
      <div className="intro-welcome-title-next">WELCOME TO THE WORLD OF OPPORTUNITIES</div>
      <div className="intro-welcome-brand-next">ASTERISK <span>CLIMOS</span></div>
      <p className="intro-welcome-sub-next">Climate intelligence for measurable rice-field impact.</p>
      <button className="intro-enter-next" onClick={()=>setPhase('entered')}>LET&apos;S GO <span>↗</span></button>
    </div>
  </div>
}
