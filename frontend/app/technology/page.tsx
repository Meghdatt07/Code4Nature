import { ArrowRight, FlaskConical, Satellite, Sparkles } from 'lucide-react';
import Link from 'next/link';
import { CTA, DarkProcess, Kicker, PageIntro, Reveal, Section, ThreePillars } from '@/components/marketing/marketing';

const gcImage = 'https://upload.wikimedia.org/wikipedia/commons/c/cd/GCMS_Instrument.jpg';

export default function Technology() {
  return (
    <main className="c4n-root">
      <PageIntro eyebrow="/ OUR TECHNOLOGY" title={<>Soil to sky<br/><em>technology.</em></>} description="Country-level scale. Field-level context. A connected technology stack for assessing, monitoring and measuring rice methane projects." visual="satellite"/>

      <Section kicker="ASSESS. MONITOR. MEASURE." title={<>One system.<br/><em>Three questions.</em></>} description="The platform brings together geospatial intelligence, field workflows, crop and environmental modelling and digital evidence.">
        <DarkProcess items={[
          {number:'01',title:'Assess project area',copy:'Understand crop, soil, water and historical practice context before a project starts.',href:'/simulator'},
          {number:'02',title:'Monitor practice adoption',copy:'Use field observations and satellite-derived indicators to follow the season.',href:'/mrv'},
          {number:'03',title:'Measure real impact',copy:'Combine direct measurements and models to quantify greenhouse-gas and water outcomes.',href:'/mrv'}
        ]}/>
      </Section>

      <section className="c4n-section c4n-section-paper">
        <div className="c4n-container">
          <Reveal className="c4n-center-heading"><Kicker>BUILT FOR RICE</Kicker><h2>Three layers of<br/><em>evidence.</em></h2></Reveal>
          <ThreePillars items={[
            {number:'01',title:'Satellite imagery',copy:'SAR and multisource data create field-level spatial context.',icon:<Satellite/>,href:'/mrv'},
            {number:'02',title:'Biochemical models',copy:'Process-based models translate environmental conditions into scenario outcomes.',icon:<Sparkles/>,href:'/research'},
            {number:'03',title:'Lab measurements',copy:'In-situ methane observations support calibration and validation where available.',icon:<FlaskConical/>,href:'#field-validation'}
          ]}/>
        </div>
      </section>

      <Section kicker="NEXT-GEN dMRV" title={<>Digital twins for<br/><em>rice fields.</em></>} description="Fuse agronomy, remote sensing, crop modelling and field measurements to create a more complete picture of the field over time.">
        <div className="c4n-feature-article">
          <div className="c4n-feature-art"><div className="c4n-feature-art-grid"/><span>FIELD 042 / DIGITAL TWIN</span></div>
          <div><Kicker>FIELD MODEL</Kicker><h3>A field gets an evolving digital story.</h3><p>Boundary · water regime · crop stage · satellite signal · observed practice · measured methane · modeled outcome · evidence status.</p></div>
        </div>
      </Section>

      <section id="field-validation" className="c4n-section c4n-section-dark">
        <div className="c4n-container">
          <div className="c4n-two-col">
            <div>
              <Kicker>FIELD VALIDATION</Kicker>
              <h2>Measure methane at the source.</h2>
              <p>Satellite observations and models help monitor rice fields at scale. Direct field sampling provides the measurement layer: closed chambers capture gas from a defined plot area, samples are collected over time, and laboratory gas chromatography quantifies methane concentration.</p>
              <p>The concentration change over time is then used to estimate methane flux. These location-specific observations can support calibration, validation and a more traceable MRV evidence chain.</p>
              <Link href="/mrv" className="c4n-button c4n-button-lime">Open digital MRV <ArrowRight size={16}/></Link>
            </div>
            <div className="overflow-hidden rounded-2xl border border-white/10 bg-black/20">
              <img src={gcImage} alt="Gas chromatograph laboratory instrument" className="h-[420px] w-full object-contain bg-[#06110d]"/>
              <div className="px-5 py-4 text-xs text-white/45">Gas chromatograph reference image: Cyberwork 95, Wikimedia Commons, CC BY-SA 4.0.</div>
            </div>
          </div>

          <div className="mt-12 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6"><div className="text-xs tracking-[.18em] text-[#8bcfa6]">AWD</div><h3 className="mt-3 text-xl font-bold">Reduce prolonged flooding</h3><p className="mt-2 text-sm leading-7 text-white/55">Alternate Wetting and Drying introduces controlled dry-down periods before re-flooding, targeting the water regime associated with methane formation in flooded rice systems.</p></div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6"><div className="text-xs tracking-[.18em] text-[#8bcfa6]">MEASUREMENT</div><h3 className="mt-3 text-xl font-bold">Chamber + GC analysis</h3><p className="mt-2 text-sm leading-7 text-white/55">Air samples from chambers can be analysed by gas chromatography to quantify methane concentration and derive field-level emission flux.</p></div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6"><div className="text-xs tracking-[.18em] text-[#8bcfa6]">CARBON MRV</div><h3 className="mt-3 text-xl font-bold">Connect measurement to evidence</h3><p className="mt-2 text-sm leading-7 text-white/55">Real, location-specific measurements can serve as evidence alongside satellite signals and model outputs when building a project MRV workflow.</p></div>
          </div>

          <div className="mt-8 border-t border-white/10 pt-6 text-xs leading-6 text-white/40">Source context: newspaper clipping supplied for this project, describing rice methane reduction through AWD and direct field measurement using chambers and gas-chromatography analysis. The clipping also highlights reported AWD water savings in the 15–50% range compared with continuous flooding, depending on field conditions. Technical measurement wording is aligned with IRRI rice GHG measurement guidance.</div>
        </div>
      </section>

      <CTA title="See the technology behind the field." button="Open digital MRV" href="/mrv"/>
    </main>
  );
}
