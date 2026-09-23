'use client';

import Link from 'next/link';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowDownRight, ArrowRight, Droplets, Leaf, MapPinned, Satellite, Sprout, Waves } from 'lucide-react';
import { useRef } from 'react';

const fade = { hidden: { opacity: 0, y: 35 }, visible: { opacity: 1, y: 0 } };

export default function Home() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: heroRef, offset: ['start start', 'end start'] });
  const orbY = useTransform(scrollYProgress, [0, 1], [0, 180]);

  return (
    <main>
      <section ref={heroRef} className="cc-hero">
        <div className="cc-noise" />
        <motion.div style={{ y: orbY }} className="cc-hero-orb orb-one" />
        <motion.div style={{ y: orbY }} className="cc-hero-orb orb-two" />
        <div className="cc-hero-inner">
          <motion.div initial="hidden" animate="visible" variants={fade} transition={{ duration: .7 }} className="cc-eyebrow">
            <span className="pulse-dot" /> CODE4NATURE / RICE CLIMATE INTELLIGENCE
          </motion.div>
          <motion.h1 initial="hidden" animate="visible" variants={fade} transition={{ duration: .8, delay: .08 }}>
            Turn rice farming into
            <span> measurable climate value.</span>
          </motion.h1>
          <motion.p initial="hidden" animate="visible" variants={fade} transition={{ duration: .8, delay: .16 }}>
            Satellite intelligence, field data, methane modelling and digital MRV for climate-smart rice cultivation.
            Explore a farm from the map, understand its water regime, quantify potential methane reduction and connect impact to carbon economics.
          </motion.p>
          <motion.div initial="hidden" animate="visible" variants={fade} transition={{ duration: .8, delay: .24 }} className="cc-hero-actions">
            <Link href="/simulator" className="cc-btn cc-btn-dark">Start a farm journey <ArrowRight size={16}/></Link>
            <Link href="/technology" className="cc-btn cc-btn-light">Explore our technology</Link>
          </motion.div>
          <div className="cc-hero-scroll"><span>Scroll to explore</span><ArrowDownRight size={17}/></div>
        </div>

        <div className="cc-field-stage">
          <div className="satellite-label"><Satellite size={15}/> LIVE FIELD INTELLIGENCE</div>
          <div className="rice-field">
            {Array.from({ length: 36 }).map((_, i) => (
              <motion.div
                key={i}
                className="rice-cell"
                animate={{ opacity: [.38, .9, .5], scale: [1, 1.025, 1] }}
                transition={{ duration: 2.8 + (i % 5) * .25, repeat: Infinity, delay: i * .035 }}
              />
            ))}
            <motion.div className="scan-line" animate={{ x: ['-120%', '120%'] }} transition={{ duration: 4.5, repeat: Infinity, ease: 'linear' }} />
            <div className="field-pin"><MapPinned size={22}/><span>FIELD 042</span></div>
          </div>
          <div className="field-data">
            <div><small>SOIL MOISTURE</small><strong>64%</strong></div>
            <div><small>WATER REGIME</small><strong>AWD</strong></div>
            <div><small>MRV STATUS</small><strong>TRACKED</strong></div>
          </div>
        </div>
      </section>

      <section className="cc-trust">
        <div className="cc-container">
          <p>ONE DIGITAL WORKFLOW FROM FIELD OBSERVATION TO CLIMATE VALUE</p>
          <div className="trust-line"><span>FARMERS</span><i/> <span>FPOs</span><i/> <span>PROJECT DEVELOPERS</span><i/> <span>CARBON BUYERS</span><i/> <span>RESEARCHERS</span></div>
        </div>
      </section>

      <section className="cc-section cc-light-section">
        <div className="cc-container">
          <motion.div whileInView="visible" viewport={{ once: true, amount: .2 }} initial="hidden" variants={fade} className="cc-section-heading">
            <div className="cc-kicker">THE OPPORTUNITY</div>
            <h2>Rice is essential.<br/><em>Its climate footprint is measurable.</em></h2>
            <p>Waterlogged rice fields create conditions for methane generation. Code4Nature connects practical water-management decisions with field-level evidence and an auditable climate-impact workflow.</p>
          </motion.div>
          <div className="cc-three-grid">
            <ImpactCard number="01" icon={<Waves/>} title="Water" copy="Track the water regime and model how irrigation choices change field conditions." href="/climate-smart-rice"/>
            <ImpactCard number="02" icon={<Leaf/>} title="Methane" copy="Translate field conditions and cultivation practices into an illustrative methane-reduction pathway." href="/technology"/>
            <ImpactCard number="03" icon={<Sprout/>} title="Carbon value" copy="Connect measured evidence, verification and carbon-market economics in one workflow." href="/rice-carbon-credits"/>
          </div>
        </div>
      </section>

      <section className="cc-dark-band">
        <div className="cc-container">
          <div className="cc-split">
            <div>
              <div className="cc-kicker">BUILT FOR THE FIELD</div>
              <h2>From satellite signal<br/>to farm-level decision.</h2>
            </div>
            <p>Our product architecture combines geospatial intelligence, farm mapping, remote sensing, process-based modelling and digital evidence. The goal is not another dashboard — it is a traceable chain from what happens in a field to the climate value it may create.</p>
          </div>
          <div className="cc-process">
            {[
              ['01','ASSESS','Map the project area','/simulator'],
              ['02','MONITOR','Observe practice adoption','/dashboard'],
              ['03','MODEL','Estimate water & methane impact','/technology'],
              ['04','VERIFY','Build digital evidence','/mrv'],
              ['05','VALUE','Explore carbon economics','/carbon'],
            ].map(([n,t,c,h],i)=><Link href={h} key={n} className="process-item">
              <span>{n}</span><div><b>{t}</b><p>{c}</p></div><ArrowRight size={18}/>
            </Link>)}
          </div>
        </div>
      </section>

      <section className="cc-section">
        <div className="cc-container">
          <div className="cc-feature">
            <div className="cc-feature-copy">
              <div className="cc-kicker">DIGITAL MRV</div>
              <h2>Every field gets a story the data can support.</h2>
              <p>Draw a farm boundary, select an area and inspect a transparent chain of location, satellite-derived indicators, simulated outcomes and evidence status.</p>
              <Link href="/mrv" className="cc-text-link">Explore digital MRV <ArrowRight size={16}/></Link>
            </div>
            <div className="mrv-visual">
              <div className="mrv-map">
                <div className="map-grid"/>
                <div className="map-field field-a"/><div className="map-field field-b"/><div className="map-field field-c"/>
                <motion.div className="map-radar" animate={{ scale: [0.65, 1.25], opacity: [0.65, 0] }} transition={{ duration: 3, repeat: Infinity }}/>
                <div className="map-tag">SAR / FIELD 042</div>
              </div>
              <div className="mrv-list">
                <span><b>✓</b> Farm boundary</span><span><b>✓</b> Water regime</span><span><b>✓</b> Practice evidence</span><span><b>○</b> Verification</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="cc-section cc-cream">
        <div className="cc-container">
          <div className="cc-section-heading compact">
            <div className="cc-kicker">EXPLORE CODE4NATURE</div>
            <h2>One platform.<br/><em>Multiple climate journeys.</em></h2>
          </div>
          <div className="cc-link-grid">
            <Journey href="/climate-smart-rice" title="Climate-smart rice" tag="FARMING" text="Understand AWD, water management and methane reduction."/>
            <Journey href="/technology" title="Our technology" tag="SCIENCE" text="Explore satellite, modelling, Geo-AI and field intelligence."/>
            <Journey href="/simulator" title="Farm simulator" tag="INTERACTIVE" text="Select a field and run an illustrative climate-value scenario."/>
            <Journey href="/rice-carbon-credits" title="Rice carbon credits" tag="MARKET" text="Follow the path from evidence to carbon-market value."/>
            <Journey href="/research" title="Science & research" tag="KNOWLEDGE" text="Read assumptions, methods, limitations and references."/>
            <Journey href="/contact" title="Partner with us" tag="ACTION" text="Start a conversation around farms, FPOs or climate finance."/>
          </div>
        </div>
      </section>

      <section className="cc-cta">
        <div className="cc-container cta-inner">
          <div className="cc-kicker">START YOUR CLIMATE JOURNEY</div>
          <h2>Make the field<br/><span>measurable.</span></h2>
          <Link href="/simulator" className="cc-btn cc-btn-light">Open the farm simulator <ArrowRight size={16}/></Link>
        </div>
      </section>
    </main>
  );
}

function ImpactCard({number,icon,title,copy,href}:{number:string;icon:React.ReactNode;title:string;copy:string;href:string}) {
  return <Link href={href} className="impact-card"><div className="impact-top"><span>{number}</span>{icon}</div><h3>{title}</h3><p>{copy}</p><span className="cc-text-link">Explore <ArrowRight size={15}/></span></Link>
}
function Journey({href,title,tag,text}:{href:string;title:string;tag:string;text:string}) {
  return <Link href={href} className="journey-card"><div><small>{tag}</small><h3>{title}</h3><p>{text}</p></div><ArrowRight size={18}/></Link>
}
