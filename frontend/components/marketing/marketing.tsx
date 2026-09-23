'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowDownRight, ArrowRight, Check, ChevronRight, CircleDot, Droplets, Leaf, MapPinned, Radio, Satellite, Sprout, Waves } from 'lucide-react';
import { useState } from 'react';

export function ButtonLink({href,children,dark=false}:{href:string;children:React.ReactNode;dark?:boolean}){
 return <Link href={href} className={`c4n-button ${dark?'c4n-button-dark':'c4n-button-light'}`}>{children}<ArrowRight size={16}/></Link>;
}
export function Reveal({children,delay=0,className=''}:{children:React.ReactNode;delay?:number;className?:string}){
 return <motion.div className={className} initial={{opacity:0,y:32}} whileInView={{opacity:1,y:0}} viewport={{once:true,amount:.18}} transition={{duration:.7,delay,ease:[.22,1,.36,1]}}>{children}</motion.div>;
}
export function Kicker({children}:{children:React.ReactNode}){return <div className="c4n-kicker"><span className="c4n-kicker-dot"/>{children}</div>}

export function PageHero({eyebrow,title,description,visual='field'}:{eyebrow:string;title:React.ReactNode;description:string;visual?:'field'|'satellite'|'water'|'carbon'|'people'}){
 return <section className="c4n-hero"><div className="c4n-hero-glow"/><div className="c4n-container c4n-hero-grid">
  <div className="c4n-hero-copy"><Reveal><Kicker>{eyebrow}</Kicker></Reveal><Reveal delay={.06}><h1>{title}</h1></Reveal><Reveal delay={.12}><p>{description}</p></Reveal><Reveal delay={.18} className="c4n-hero-actions"><ButtonLink href="/simulator" dark>Start a farm journey</ButtonLink><ButtonLink href="/technology">Explore the technology</ButtonLink></Reveal><div className="c4n-scroll-cue"><span>Scroll to explore</span><ArrowDownRight size={16}/></div></div>
  <Reveal delay={.18} className="c4n-hero-visual"><VisualScene type={visual}/></Reveal>
 </div></section>;
}
function VisualScene({type}:{type:string}){
 if(type==='satellite') return <div className="c4n-scene c4n-satellite-scene"><div className="c4n-orbit orbit-a"/><div className="c4n-orbit orbit-b"/><div className="c4n-satellite-body"><Satellite size={38}/></div><div className="c4n-radar-ring"/><div className="c4n-scene-label">SAR / FIELD INTELLIGENCE</div><div className="c4n-mini-readouts"><span>BACKSCATTER <b>-12.8 dB</b></span><span>OBSERVATION <b>NEAR REAL TIME</b></span></div></div>;
 if(type==='water') return <div className="c4n-scene c4n-water-scene"><div className="c4n-water-sun"/><div className="c4n-paddy-lines">{Array.from({length:12}).map((_,i)=><i key={i}/>)}</div><motion.div className="c4n-water-wave" animate={{x:['-10%','10%','-10%']}} transition={{duration:7,repeat:Infinity,ease:'easeInOut'}}/><div className="c4n-scene-label">WATER / AWD CYCLE</div><div className="c4n-water-card"><small>FIELD 042</small><strong>DRY-DOWN WINDOW</strong><span>3.4 days</span></div></div>;
 if(type==='carbon') return <div className="c4n-scene c4n-carbon-scene"><div className="c4n-carbon-orb"/><div className="c4n-carbon-coins"><b>tCO₂e</b><b>₹</b><b>$</b></div><div className="c4n-carbon-path"><i/><i/><i/><i/></div><div className="c4n-scene-label">EVIDENCE → VALUE</div><div className="c4n-carbon-value"><small>ILLUSTRATIVE PROJECT VALUE</small><strong>₹ 18.4L</strong><span>from modeled annual reduction</span></div></div>;
 if(type==='people') return <div className="c4n-scene c4n-people-scene"><div className="c4n-people-sun"/><div className="c4n-person p1"/><div className="c4n-person p2"/><div className="c4n-person p3"/><div className="c4n-scene-label">FARMERS / FPO / SCIENCE</div><div className="c4n-people-tag"><Sprout size={17}/> Farmer-first implementation</div></div>;
 return <div className="c4n-scene c4n-field-scene"><div className="c4n-field-map">{Array.from({length:48}).map((_,i)=><i key={i}/>)}</div><motion.div className="c4n-field-scan" animate={{x:['-120%','120%']}} transition={{duration:5,repeat:Infinity,ease:'linear'}}/><div className="c4n-field-pin"><MapPinned size={18}/><span>FIELD 042</span></div><div className="c4n-scene-label"><Radio size={13}/> LIVE FIELD INTELLIGENCE</div><div className="c4n-field-metrics"><span>SOIL MOISTURE <b>64%</b></span><span>WATER REGIME <b>AWD</b></span><span>MRV <b>TRACKED</b></span></div></div>;
}
export function PageIntro({eyebrow,title,description,visual}:{eyebrow:string;title:React.ReactNode;description:string;visual?:'field'|'satellite'|'water'|'carbon'|'people'}){
 return <PageHero eyebrow={eyebrow} title={title} description={description} visual={visual}/>;
}
export function Section({kicker,title,description,children,dark=false,className=''}:{kicker:string;title:React.ReactNode;description?:string;children:React.ReactNode;dark?:boolean;className?:string}){
 return <section className={`c4n-section ${dark?'c4n-section-dark':''} ${className}`}><div className="c4n-container"><Reveal><Kicker>{kicker}</Kicker><h2>{title}</h2>{description&&<p className="c4n-section-intro">{description}</p>}</Reveal>{children}</div></section>;
}
export function Stats({items}:{items:{value:string;label:string;note?:string}[]}){
 return <div className="c4n-stats">{items.map(s=><div className="c4n-stat" key={s.label}><strong>{s.value}</strong><span>{s.label}</span>{s.note&&<small>{s.note}</small>}</div>)}</div>;
}
export function ThreePillars({items}:{items:{number:string;title:string;copy:string;icon:React.ReactNode;href:string}[]}){
 return <div className="c4n-three">{items.map(x=><Link href={x.href} key={x.number} className="c4n-pillar"><div className="c4n-pillar-top"><span>{x.number}</span>{x.icon}</div><h3>{x.title}</h3><p>{x.copy}</p><span className="c4n-inline-link">Learn more <ArrowRight size={15}/></span></Link>)}</div>;
}
export function DarkProcess({items}:{items:{number:string;title:string;copy:string;href:string}[]}){
 return <div className="c4n-process">{items.map(x=><Link href={x.href} key={x.number} className="c4n-process-row"><span>{x.number}</span><div><b>{x.title}</b><p>{x.copy}</p></div><ArrowRight size={17}/></Link>)}</div>;
}
export function EvidenceVisual(){
 return <div className="c4n-evidence"><div className="c4n-evidence-map"><div className="e-grid"/><div className="e-field e1"/><div className="e-field e2"/><div className="e-field e3"/><motion.div className="e-pulse" animate={{scale:[.55,1.35],opacity:[.8,0]}} transition={{duration:3,repeat:Infinity}}/><span className="e-chip">FIELD 042 / SAR</span></div><div className="e-checks"><span><Check size={13}/> Boundary mapped</span><span><Check size={13}/> Water regime</span><span><Check size={13}/> Practice evidence</span><span><CircleDot size={13}/> Verification</span></div></div>;
}
export function ArticleGrid({items}:{items:{date:string;category:string;title:string;href:string}[]}){
 return <div className="c4n-articles">{items.map(a=><Link href={a.href} key={a.title} className="c4n-article"><div className="c4n-article-image"><div className="c4n-article-art"/><span>{a.category}</span></div><div className="c4n-article-meta">{a.date}</div><h3>{a.title}</h3><span className="c4n-inline-link">Read the story <ArrowRight size={15}/></span></Link>)}</div>;
}
export function Quote({children,byline}:{children:React.ReactNode;byline:string}){return <div className="c4n-quote"><div className="c4n-quote-mark">“</div><blockquote>{children}</blockquote><span>{byline}</span></div>}
export function Newsletter(){
 const [email,setEmail]=useState('');const [sent,setSent]=useState(false);
 return <div className="c4n-newsletter"><div><Kicker>GET OUR NEWS</Kicker><h3>CH₄ × Code4Nature</h3><p>Updates on rice, methane, water intelligence and climate impact.</p></div><div className="c4n-newsletter-form">{sent?<span className="c4n-sent">You're on the list.</span>:<><input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email address" type="email"/><button onClick={()=>email&&setSent(true)}>Subscribe <ChevronRight size={16}/></button></>}</div></div>;
}
export function CTA({title='Make the field measurable.',button='Start a farm journey',href='/simulator'}:{title?:string;button?:string;href?:string}){
 return <section className="c4n-cta"><div className="c4n-container c4n-cta-inner"><Kicker>START YOUR CLIMATE JOURNEY</Kicker><h2>{title}</h2><ButtonLink href={href}>{button}</ButtonLink></div></section>;
}
export const Icons={Leaf,Droplets,Sprout,Waves,Satellite};
