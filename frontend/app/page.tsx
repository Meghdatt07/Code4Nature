import Link from 'next/link';
import { ArrowRight, Droplets, Eye, Globe2, Leaf, Play, ShieldCheck, Sprout } from 'lucide-react';
import { ButtonLink, CTA, Kicker, Newsletter, Reveal } from '@/components/marketing/marketing';
import { HeroBackdrop, TechTabs, VideoGallery } from '@/components/marketing/home';
import { Footer } from '@/components/shared/footer';
import { HERO_POSTER, HERO_VIDEO } from '@/lib/videos';

const pillars = [
  {
    icon: ShieldCheck,
    title: 'Permanent',
    copy: 'Methane is roughly 80× more potent than CO₂ over 20 years. Keeping paddies from staying flooded avoids that methane at the source, instead of offsetting it later.',
  },
  {
    icon: Eye,
    title: 'Measurable',
    copy: 'Boundary, water regime and practice evidence stay linked from the farm to the number, so every claim can be traced and challenged.',
  },
  {
    icon: Globe2,
    title: 'Scalable',
    copy: 'Rice feeds almost half the planet and flooded paddies are responsible for roughly 8–12% of human-made methane. Fixing water management reaches both climate and farm costs.',
  },
];

const stats = [
  { value: '~48%', label: 'average methane reduction with AWD', note: 'CGIAR CCAFS, 2014' },
  { value: 'up to 30%', label: 'irrigation water saved', note: 'CGIAR CCAFS, 2014' },
  { value: '8–12%', label: 'of human-made methane comes from rice', note: 'FAO · ADB' },
  { value: '≈80×', label: 'CO₂ potency of methane over 20 years', note: 'IPCC AR6' },
];

const science = ['IRRI · AWD protocol', 'CGIAR · CCAFS research', 'IPCC AR6 · GWP', 'Sentinel-1 · SAR', 'Process-based CH₄ models', 'Digital MRV'];

const journeys = [
  { href: '/climate-smart-rice', tag: '01', title: 'Climate-smart rice', copy: 'How water, soil and methane interact in the paddy.', cls: 'j1', Icon: Sprout },
  { href: '/technology', tag: '02', title: 'Our technology', copy: 'Satellite evidence, models and dMRV in one workflow.', cls: 'j2', Icon: Leaf },
  { href: '/simulator', tag: '03', title: 'Farm simulator', copy: 'Draw a field and explore water, methane and carbon value.', cls: 'j3', Icon: Droplets },
  { href: '/about', tag: '04', title: 'Our vision & team', copy: 'The people and principles behind the platform.', cls: 'j4', Icon: Globe2 },
];

export default function Home() {
  return (
    <main className="c4n-root hv-root">
      <section className="hv-hero">
        <HeroBackdrop src={HERO_VIDEO} poster={HERO_POSTER} />
        <div className="c4n-container hv-hero-inner">
          <Reveal><Kicker>RICE CARBON CREDITS · METHANE INTELLIGENCE</Kicker></Reveal>
          <Reveal delay={0.06}>
            <h1>Methane.<br /><em>The next frontier in climate impact.</em></h1>
          </Reveal>
          <Reveal delay={0.12}>
            <p>Asterisk Climos combines satellite evidence, field science and water intelligence to make methane reductions in rice farming visible, measurable and valuable.</p>
          </Reveal>
          <Reveal delay={0.18} className="hv-hero-actions">
            <ButtonLink href="/simulator" dark>Start your methane journey</ButtonLink>
            <a href="#videos" className="hv-ghost">
              <span className="hv-ghost-play"><Play size={14} fill="currentColor" /></span>
              Watch how it works
            </a>
          </Reveal>
        </div>
        <div className="c4n-container">
          <div className="hv-hero-strip">
            {stats.map((s) => <div key={s.label}><strong>{s.value}</strong><span>{s.label}</span></div>)}
          </div>
        </div>
      </section>

      <section className="hv-marquee" aria-label="Science and methods we build on">
        <div className="c4n-container">
          <small>BUILT ON OPEN SCIENCE</small>
          <div className="hv-marquee-track">{[...science, ...science].map((s, i) => <span key={i}>{s}</span>)}</div>
        </div>
      </section>

      <section className="c4n-section">
        <div className="c4n-container">
          <Reveal>
            <Kicker>WHY RICE METHANE</Kicker>
            <h2>High-integrity climate action,<br /><em>grown in the paddy.</em></h2>
            <p className="c4n-section-intro">Alternate wetting and drying (AWD) lets fields dry between irrigations. Methane-producing microbes slow down, the pump runs less, and yield is maintained when the practice is applied correctly.</p>
          </Reveal>
          <div className="hv-pillars">
            {pillars.map((p, i) => <Reveal key={p.title} delay={i * 0.08}><div className="hv-pillar"><div className="hv-pillar-icon"><p.icon size={26} /></div><h3>{p.title}</h3><p>{p.copy}</p></div></Reveal>)}
          </div>
        </div>
      </section>

      <section id="videos" className="c4n-section c4n-section-dark hv-videos">
        <div className="c4n-container">
          <Reveal>
            <Kicker>SEE IT IN THE FIELD</Kicker>
            <h2>Climate-smart rice,<br /><em>explained in motion.</em></h2>
            <p className="c4n-section-intro">From controlled dry-down to satellite evidence, watch how better water management changes a rice season.</p>
          </Reveal>
          <VideoGallery />
        </div>
      </section>

      <section className="hv-impact">
        <div className="c4n-container">
          <div className="hv-impact-grid">
            <Reveal>
              <Kicker>THE SCIENCE IN NUMBERS</Kicker>
              <h2>Small water decisions,<br /><em>large climate returns.</em></h2>
            </Reveal>
            <div className="hv-impact-stats">
              {stats.map((s, i) => <Reveal key={s.label} delay={i * 0.06}><div className="hv-impact-stat"><strong>{s.value}</strong><span>{s.label}</span><small>{s.note}</small></div></Reveal>)}
            </div>
          </div>
        </div>
      </section>

      <section className="c4n-section c4n-section-paper">
        <div className="c4n-container">
          <Reveal>
            <Kicker>OUR TECHNOLOGY</Kicker>
            <h2>Cutting-edge technology<br /><em>unlocks a new frontier.</em></h2>
            <p className="c4n-section-intro">Assess, monitor and measure methane reductions at project scale with field-level evidence.</p>
          </Reveal>
          <Reveal delay={0.1}><TechTabs /></Reveal>
          <div className="hv-center"><ButtonLink href="/technology">Explore the technology</ButtonLink></div>
        </div>
      </section>

      <section className="c4n-section">
        <div className="c4n-container">
          <Reveal>
            <Kicker>LEARN MORE AND TAKE ACTION</Kicker>
            <h2>Where would you<br /><em>like to start?</em></h2>
          </Reveal>
          <div className="hv-journeys">
            {journeys.map((j, i) => <Reveal key={j.href} delay={i * 0.06}><Link href={j.href} className={`hv-journey ${j.cls}`}><span className="hv-journey-tag">{j.tag}</span><j.Icon className="hv-journey-icon" size={64} strokeWidth={1.2} /><div><h3>{j.title}</h3><p>{j.copy}</p><span className="hv-journey-link">Explore <ArrowRight size={15} /></span></div></Link></Reveal>)}
          </div>
          <Newsletter />
        </div>
      </section>

      <CTA title="Start your methane journey." button="Open the farm simulator" href="/simulator" />
      <div className="hv-disclaimer"><div className="c4n-container">Prototype demonstration only. Simulator outputs are deterministic, illustrative equations and are not measured agronomic results or certified carbon credits. Science figures: CGIAR CCAFS (2014), FAO, ADB and IPCC AR6.</div></div>
      <Footer />
    </main>
  );
}
