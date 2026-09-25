import { ArrowRight, ExternalLink } from 'lucide-react';
import Link from 'next/link';
import { CTA, Kicker, Newsletter, Reveal, Section } from '@/components/marketing/marketing';

const MITTI = 'https://www.mittilabs.earth';

const items=[
  {
    date:'Sep 10, 2026',
    category:'CLIMATE + WATER',
    title:'One million carbon credits to cut methane emissions and save water',
    summary:'Google signed a four-year agreement to purchase 1 million carbon credits from Mitti Labs by 2030. The article connects rice methane reduction, water savings and GeoAI-enabled field monitoring.',
    image:'https://framerusercontent.com/images/ox87vh4KJgar1GBdMbhHxGXpA.jpg?height=388&width=640',
    href:`${MITTI}/insights/one-million-carbon-credits-to-eliminate-methane-and-save-water`
  },
  {
    date:'Aug 15, 2026',
    category:'WATER',
    title:"Why rice irrigation matters: a look at India's 2026 water crisis",
    summary:'A look at why rice irrigation and water resilience matter as India faces growing pressure from heat, rainfall variability and stressed water systems.',
    image:'https://framerusercontent.com/images/SJ9R3bayFImfIvT6U61ZnEoUFQc.jpg?height=3944&width=5916',
    href:`${MITTI}/insights/why-rice-irrigation-matters-a-look-at-indias-2026-water-crisis`
  },
  {
    date:'Aug 5, 2026',
    category:'CLIMATE-SMART RICE',
    title:"Mitti Labs raises $9.5M to build water resilience in Asia's rice fields",
    summary:'Mitti Labs announced a $9.5M Series A to expand climate-smart rice programs across India and into the Philippines and Indonesia, using GeoAI and field data to verify AWD at scale.',
    image:'https://framerusercontent.com/images/ox87vh4KJgar1GBdMbhHxGXpA.jpg?height=388&width=640',
    href:`${MITTI}/insights/mitti-labs-raises-9.5m-to-build-water-resilience-in-asia-s-rice-ields`
  },
  {
    date:'Jul 28, 2026',
    category:'CARBON CREDITS',
    title:"Sylvera issues an 'A' Rating for Mitti Labs' carbon credits based on rice methane",
    summary:'The article explains the project’s Sylvera rating and the field-level monitoring system combining satellite data, geo-tagged evidence, water-level tracking and direct emissions measurement.',
    image:'https://framerusercontent.com/images/KBPj8j0Lffivecp1wu3rmMm3yrk.png?height=441&width=600',
    href:`${MITTI}/insights/sylvera-rating`
  },
  {
    date:'Jul 15, 2026',
    category:'MRV',
    title:'Leveraging technology for traceable impact: our first carbon credit issuance',
    summary:'A milestone on traceable carbon issuance, showing how field operations, digital monitoring and evidence can stay connected through a rice methane project.',
    image:'https://framerusercontent.com/images/PHSFrlTkzH1j6EZRqevIza4z8A.png?height=904&width=2240',
    href:`${MITTI}/insights/leveraging-technology-for-trackeable-impact`
  },
  {
    date:'Jun 19, 2026',
    category:'SUPERPOLLUTANTS',
    title:'Beyond CO₂: Carbon Direct X Mitti Labs',
    summary:'An exploration of methane and other short-lived climate pollutants, and why reducing near-term warming can complement longer-term climate action.',
    image:'https://framerusercontent.com/images/hOqc3RKzRg0p9V9a3aBKOSYI.png?height=910&width=2224',
    href:`${MITTI}/insights/carbon-direct-x-mitti-labs-beyond-co2-webinar`
  },
  {
    date:'May 18, 2026',
    category:'CLIMATE',
    title:'The other half of global warming, and what we can do about it',
    summary:'A field-focused discussion of methane, its role in near-term warming and the practical opportunity to reduce emissions from agriculture.',
    image:'https://framerusercontent.com/images/ULUMYH42UmrhRPAgrn4Dg6Gm4I.png?height=1080&width=1920',
    href:`${MITTI}/insights/the-other-half-of-global-warming-%E2%80%94-and-what-we-can-do-about-it`
  },
  {
    date:'May 13, 2026',
    category:'METHANE',
    title:'Cool Effect and Mitti Labs: partnering on a world first for superpollutant credits based on rice methane reduction',
    summary:'A partnership focused on rice methane, high-integrity climate action, water conservation and farmer livelihoods through Alternate Wetting and Drying.',
    image:'https://framerusercontent.com/images/ULUMYH42UmrhRPAgrn4Dg6Gm4I.png?height=1080&width=1920',
    href:`${MITTI}/insights/cool-effect-and-mitti-labs-partnering-on-a-world-first`
  },
  {
    date:'Mar 27, 2026',
    category:'CARBON MARKETS',
    title:'An update from ICVCM: Rice methane gets its Core Carbon Principles label',
    summary:'The article covers ICVCM approval of a rice methane methodology and what the Core Carbon Principles framework means for integrity and confidence in carbon markets.',
    image:'https://framerusercontent.com/images/KBPj8j0Lffivecp1wu3rmMm3yrk.png?height=441&width=600',
    href:`${MITTI}/insights/an-update-from-icvcm-rice-methane-gets-its-core-carbon-principle-label`
  },
  {
    date:'Feb 10, 2026',
    category:'RESEARCH',
    title:"Mitti Labs partners with ICAR-IARI, India's leading institution for scientific innovation in agriculture",
    summary:'The partnership combines field gas and soil sampling with gas chromatography, biogeochemical modelling and satellite remote sensing to strengthen rice methane quantification.',
    image:'https://framerusercontent.com/images/THHB3FbAFczZ99q7fgclT9Lrwhk.png?height=627&width=1200',
    href:`${MITTI}/insights/mitti-labs-and-icar-iari-partner-on-ground-breaking-research-to-quantify-methane-emissions-from-rice-farming`
  },
  {
    date:'Dec 3, 2025',
    category:'FIELD PARTNERSHIPS',
    title:'ACCESS and Mitti Labs: a partnership to transform rice farming in India',
    summary:'A partnership story focused on farmer implementation, climate-smart rice practices and the operational work needed to move from evidence to adoption.',
    image:'https://framerusercontent.com/images/THHB3FbAFczZ99q7fgclT9Lrwhk.png?height=627&width=1200',
    href:`${MITTI}/insights/mitti-labs-and-access-are-transforming-rice-farming-in-india`
  },
  {
    date:'Nov 21, 2025',
    category:'CLIMATE',
    title:'The future of rice: is climate change reshaping India’s monsoon?',
    summary:'An examination of the relationship between rice farming, changing monsoon patterns, water availability and the need for more resilient production systems.',
    image:'https://framerusercontent.com/images/SJ9R3bayFImfIvT6U61ZnEoUFQc.jpg?height=3944&width=5916',
    href:`${MITTI}/insights/the-future-of-rice-is-climate-change-reshaping-india-s-monsoon`
  },
  {
    date:'Nov 13, 2025',
    category:'FAQ',
    title:'Mitti Labs: Frequently Asked Questions',
    summary:'A practical reference covering the company’s rice methane work, climate-smart practices, carbon credits and monitoring approach.',
    image:'https://framerusercontent.com/images/hOqc3RKzRg0p9V9a3aBKOSYI.png?height=910&width=2224',
    href:`${MITTI}/insights/frequently-asked-questions`
  },
  {
    date:'Sep 26, 2025',
    category:'WATER',
    title:'Every drop counts: how farmers protect India’s water future with Alternate Wetting and Drying',
    summary:'An introduction to AWD and how controlled wetting and drying can reduce irrigation demand while supporting rice production and methane reduction.',
    image:'https://framerusercontent.com/images/SJ9R3bayFImfIvT6U61ZnEoUFQc.jpg?height=3944&width=5916',
    href:`${MITTI}/insights/every-drop-counts-how-farmers-and-mitti-labs-are-protecting-india-s-water-future`
  }
];

function ArticleCard({item,index}:{item:typeof items[number];index:number}){
  return <Reveal delay={Math.min(index*.035,.18)}>
    <a href={item.href} target="_blank" rel="noreferrer" className="c4n-source-card">
      <div className="c4n-source-image">
        <img src={item.image} alt="" loading={index<4?'eager':'lazy'} />
        <span>{item.category}</span>
        <div className="c4n-source-image-overlay"/>
      </div>
      <div className="c4n-source-meta"><span>{item.date}</span><span>Mitti Labs</span></div>
      <h3>{item.title}</h3>
      <p>{item.summary}</p>
      <span className="c4n-inline-link">Read the original insight <ExternalLink size={14}/></span>
    </a>
  </Reveal>;
}

export default function Insights(){
  const featured=items[0];
  return <main className="c4n-root">
    <section className="c4n-insights-hero">
      <div className="c4n-container">
        <Reveal><Kicker>/ INSIGHTS · FIELD INTELLIGENCE</Kicker></Reveal>
        <Reveal delay={.06}><h1>Rice, methane, water<br/><em>and the evidence in between.</em></h1></Reveal>
        <Reveal delay={.12}><p>Explore the latest research, field stories and climate intelligence from the rice-methane ecosystem — using the current Mitti Labs Insights archive as the source reference.</p></Reveal>
      </div>
    </section>

    <section className="c4n-feature-source">
      <div className="c4n-container">
        <Reveal className="c4n-source-feature">
          <a href={featured.href} target="_blank" rel="noreferrer" className="c4n-source-feature-image">
            <img src={featured.image} alt="" />
            <span>FEATURED · {featured.category}</span>
          </a>
          <div className="c4n-source-feature-copy">
            <Kicker>{featured.date} · MITTI LABS</Kicker>
            <h2>{featured.title}</h2>
            <p>{featured.summary}</p>
            <a href={featured.href} target="_blank" rel="noreferrer" className="c4n-button c4n-button-light">Read featured insight <ExternalLink size={16}/></a>
          </div>
        </Reveal>
      </div>
    </section>

    <Section kicker="THE LATEST" title={<>What’s happening<br/><em>in the field.</em></>} description="The latest entries are presented as source-linked insight cards so the evidence, dates and original articles remain traceable.">
      <div className="c4n-source-grid">
        {items.slice(1,7).map((item,index)=><ArticleCard item={item} index={index} key={item.title}/>)}
      </div>
    </Section>

    <section className="c4n-section-dark c4n-source-band">
      <div className="c4n-container">
        <Reveal>
          <Kicker>THE EVIDENCE CHAIN</Kicker>
          <h2>From field practice<br/><em>to climate value.</em></h2>
          <p className="c4n-source-band-copy">Across the Mitti Labs archive, the recurring thread is clear: Alternate Wetting and Drying, farmer implementation, satellite and field evidence, methane measurement, digital MRV and carbon-market integrity are connected parts of one system.</p>
        </Reveal>
        <div className="c4n-evidence-links">
          {[
            ['01','AWD','Water management that alternates wetting and drying in rice paddies.','/climate-smart-rice'],
            ['02','GeoAI','Satellite radar, field observations and digital intelligence for plot-level evidence.','/technology'],
            ['03','dMRV','Monitoring, reporting and verification built around field-level evidence.','/mrv'],
            ['04','CARBON','Transparent calculations connecting measured outcomes to climate value.','/carbon']
          ].map(([n,t,c,h])=><Link href={h} key={n} className="c4n-evidence-link"><span>{n}</span><div><b>{t}</b><p>{c}</p></div><ArrowRight size={17}/></Link>)}
        </div>
      </div>
    </section>

    <Section kicker="ARCHIVE" title={<>More field notes<br/><em>and research.</em></>}>
      <div className="c4n-source-grid">
        {items.slice(7).map((item,index)=><ArticleCard item={item} index={index} key={item.title}/>)}
      </div>
    </Section>

    <div className="c4n-container"><Newsletter/></div>
    <CTA title="Turn the next field note into a field experiment."/>
  </main>
}
