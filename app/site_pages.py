import re
import streamlit as st
import streamlit.components.v1 as components

from pathlib import Path
import base64

from app.dashboard import init_state, render_economics, render_market, render_mrv, render_policy, render_farm_simulator

# Native Streamlit page objects used by homepage page links.
_PAGE_ROUTES = {}

def set_page_routes(routes):
    global _PAGE_ROUTES
    _PAGE_ROUTES = routes


def inject_site_css():
    st.markdown("""<style>
:root{--bg:#07120f;--panel:#0d1d18;--line:#244137;--text:#edf7f2;--muted:#9ab3a8;--accent:#7ee2b1;--water:#66b7d7}
.stApp{background:radial-gradient(circle at 78% 0%,#15382d 0,#07120f 42%);color:var(--text)}
[data-testid="stHeader"]{background:rgba(7,18,15,.88)}
[data-testid="stSidebar"]{background:#091713}
.block-container{max-width:1400px!important;padding:1.25rem 3rem 4rem!important}
.site-head{display:flex;justify-content:space-between;align-items:center;min-height:112px;border-bottom:1px solid var(--line);padding:.35rem 0 .8rem;margin-bottom:1.2rem}
.brand{display:flex;align-items:center;gap:.65rem;font-weight:900;letter-spacing:.08em}.brand-logo{width:96px;height:96px;object-fit:contain;object-position:center;display:block}
.brand-mark{width:34px;height:34px;border-radius:10px;background:var(--accent);color:#07120f;display:grid;place-items:center;font-weight:900}
.brand small{display:block;color:#668276;font-size:.55rem;letter-spacing:.18em;font-weight:700;margin-top:.15rem}
.status{font-size:.62rem;letter-spacing:.14em;color:#7d998c}.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#48e39a;box-shadow:0 0 12px #48e39a;margin-right:.4rem}
.hero{border:1px solid #234537;border-radius:28px;padding:4.3rem 3.5rem;background:radial-gradient(circle at 8% 20%,rgba(48,147,105,.22),transparent 32%),radial-gradient(circle at 92% 12%,rgba(77,120,173,.16),transparent 28%),#0a1914;overflow:hidden;position:relative}
.eyebrow{color:var(--accent);font-size:.72rem;letter-spacing:.17em;font-weight:900;text-transform:uppercase}
.hero h1{font-size:clamp(3.5rem,7.5vw,7.8rem);line-height:.9;letter-spacing:-.065em;margin:1.35rem 0;color:#edf7f2;max-width:1050px}
.hero h1 span{color:var(--accent)}
.hero p{max-width:780px;color:#abc0b5;font-size:1.07rem;line-height:1.75}
.hero-actions{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:2rem}
.a-btn{display:inline-block;padding:.8rem 1.1rem;border-radius:12px;text-decoration:none;font-weight:800;font-size:.82rem}
.a-btn.primary{background:var(--accent);color:#07120f}.a-btn.secondary{border:1px solid #315949;color:#e8f2ed}
.home-action-row{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:2rem}
div.st-key-home_run_sim button,
div.st-key-home_explore_tech button{
  border-radius:12px!important;
  padding:.8rem 1.1rem!important;
  min-height:0!important;
  height:auto!important;
  font-size:.82rem!important;
  font-weight:800!important;
  line-height:1.2!important;
  text-decoration:none!important;
  box-shadow:none!important;
}
div.st-key-home_run_sim button{
  background:var(--accent)!important;
  border:1px solid var(--accent)!important;
  color:#07120f!important;
}
div.st-key-home_run_sim button:hover{
  background:#8de8bd!important;
  border-color:#8de8bd!important;
}
div.st-key-home_explore_tech button{
  background:transparent!important;
  border:1px solid #315949!important;
  color:#e8f2ed!important;
}
div.st-key-home_explore_tech button:hover{
  background:rgba(126,226,177,.06)!important;
  border-color:#4d7b68!important;
}
div.st-key-home_run_sim button p,
div.st-key-home_explore_tech button p{
  margin:0!important;
  text-decoration:none!important;
}

.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin-top:1rem}
.card,.metric-card{background:rgba(255,255,255,.035);border:1px solid rgba(126,226,177,.12);border-radius:18px;padding:1.15rem;min-height:150px}
.card b,.metric-card b{font-size:1.05rem}.num{color:var(--accent);font-size:.72rem;font-weight:900;letter-spacing:.15em}
.muted{color:var(--muted)}
.section{padding:4.3rem 0}.section h2{font-size:clamp(2.2rem,4.5vw,4.4rem);line-height:.95;letter-spacing:-.055em;margin:.7rem 0 1rem;color:#edf7f2}
.section-copy{color:#9fb6aa;line-height:1.75;max-width:800px}
.band{background:#091713;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:4.5rem 0;margin:1rem -3rem;padding-left:3rem;padding-right:3rem}
.band h2{font-size:clamp(2.4rem,5vw,5rem);line-height:.94;letter-spacing:-.06em;margin:.7rem 0;color:#edf7f2}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin-top:2rem}
.tiles.four{grid-template-columns:repeat(4,1fr)}
.tile{background:rgba(255,255,255,.035);border:1px solid rgba(126,226,177,.11);border-radius:18px;padding:1.4rem;min-height:190px}
.tile h3{margin:.75rem 0 .35rem;color:#edf7f2}.tile p{margin:0;color:#91aa9e;line-height:1.65;font-size:.88rem}
.glass{background:rgba(13,29,24,.82);border:1px solid var(--line);border-radius:20px;padding:1.2rem}
.footer-note{border-top:1px solid var(--line);padding-top:1.25rem;color:#789286;font-size:.72rem;line-height:1.6}
@media(max-width:900px){.block-container{padding:1rem 1.2rem 3rem!important}.site-head{min-height:96px}.brand-logo{width:82px;height:82px}.flow,.tiles,.tiles.four{grid-template-columns:1fr 1fr}.hero{padding:3rem 1.5rem}.hero h1{font-size:3.7rem}.band{margin:1rem -1.2rem;padding-left:1.2rem;padding-right:1.2rem}}
@media(max-width:560px){.flow,.tiles,.tiles.four{grid-template-columns:1fr}}

/* Remove Streamlit's automatic heading/link anchor icon. Keep normal page/navigation links visible. */
.stMarkdownContainer h1 a,
.stMarkdownContainer h2 a,
.stMarkdownContainer h3 a,
.stMarkdownContainer h4 a,
.stMarkdownContainer h5 a,
.stMarkdownContainer h6 a,
[data-testid="stHeading"] a,
.stHeadingWithActionElements a { display:none !important; visibility:hidden !important; pointer-events:none !important; }

/* Hide Streamlit's automatic heading anchor/link icon. */
[data-testid="stHeaderActionElements"],
[data-testid="StyledLinkIconContainer"] { display:none !important; }
</style>""", unsafe_allow_html=True)

def _logo_data():
    try:
        theme_type = st.context.theme.type
    except Exception:
        theme_type = "light"

    theme_dir = Path(__file__).resolve().parent / "assets"
    logo_path = theme_dir / ("logo_dark.svg" if theme_type == "dark" else "logo_light.svg")
    svg = logo_path.read_text(encoding="utf-8")
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + encoded

def shell():
    inject_site_css()
    logo = _logo_data()
    st.markdown(
        f'<div class="site-head"><div class="brand"><img class="brand-logo" src="{logo}" alt="Asterisk Climos logo"></div><div class="status"><span class="dot"></span>SYSTEM ONLINE</div></div>',
        unsafe_allow_html=True
    )

def frame(eyebrow,title,text):
    st.markdown(f'<section class="section"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2><div class="section-copy">{text}</div></section>', unsafe_allow_html=True)

def tiles(items, four=False):
    cls='tiles four' if four else 'tiles'
    html=f'<div class="{cls}">'
    for num,title,body in items:
        html+=f'<div class="tile"><div class="num">{num}</div><h3>{title}</h3><p>{body}</p></div>'
    html+='</div>'
    st.markdown(html, unsafe_allow_html=True)

def home():
    st.set_page_config(page_title="Asterisk Climos | Code4Nature", page_icon="🌾", layout="wide")
    shell(); init_state()
    st.markdown('''<section class="hero">
      <div class="eyebrow">CODE4NATURE / RICE CLIMATE INTELLIGENCE</div>
      <h1>Measure. Optimize.<br><span>Reduce. Value.</span></h1>
      <p>Transform rice-field water management into measurable climate impact through field data, transparent modelling and carbon-economics simulation.</p>
      <div class="hero-actions"></div>
    </section>''', unsafe_allow_html=True)
    link_cols = st.columns([1.15, 1.1, 5.75])
    with link_cols[0]:
        if st.button("Run Farm Simulation →", key="home_run_sim", type="primary"):
            st.switch_page(_PAGE_ROUTES["simulator"])
    with link_cols[1]:
        if st.button("Explore Technology", key="home_explore_tech", type="secondary"):
            st.switch_page(_PAGE_ROUTES["technology"])
    cols=st.columns(4)
    flow=[("01","Farm data","Field boundary and water observations"),("02","Satellite","SAR wetness evidence"),("03","MRV","Methane → CO₂e scenario"),("04","Value","Farmer/FPO + company economics")]
    for col,(n,t,b) in zip(cols,flow):
        with col: st.markdown(f'<div class="card"><div class="num">{n}</div><b>{t}</b><div class="muted" style="font-size:.8rem;margin-top:.4rem">{b}</div></div>',unsafe_allow_html=True)
    frame("THE LOGIC","From water management to climate value","The prototype keeps the full pathway visible: practice → evidence → emissions scenario → carbon economics.")
    tiles([("01","Climate-smart rice","Make controlled wetting and drying visible at field scale."),("02","Digital MRV","Connect ground observations, satellite evidence and transparent calculations."),("03","Carbon economics","Explore illustrative farmer/FPO and company value from the same scenario.")])
    st.markdown('<div class="band"><div class="eyebrow">EVIDENCE STACK</div><h2>Ground truth → satellite → model → evidence.</h2><div class="section-copy">A carbon number is only useful when the assumptions and evidence pathway behind it remain inspectable.</div></div>',unsafe_allow_html=True)
    frame("DISCOVER","One workflow, separate pages","Use the application navigation to open the simulator, MRV, research, policy and partner workflows.")
    tiles([("01","Farm simulator","Move the farm and draw a boundary."),("02","Digital MRV","Inspect field and SAR evidence."),("03","Carbon economics","Change price, area and farmer share."),("04","Research","Read the scientific framing and limitations.")],True)
    st.markdown('<div class="footer-note">Prototype demonstration only. Water savings, methane reductions, carbon quantities, prices and financial outcomes are illustrative unless independently measured and verified.</div>',unsafe_allow_html=True)

def climate_smart_rice():
    st.set_page_config(page_title="Climate-smart Rice | Asterisk Climos", layout="wide"); shell()
    frame("CLIMATE-SMART RICE","The farming practice is the climate intervention.","Alternate Wetting and Drying (AWD) introduces controlled dry-down periods between irrigations. The prototype focuses on making that field process observable and explainable.")
    tiles([("01","WET","Flooded state and irrigation event."),("02","DRYING","Controlled drawdown toward the target threshold."),("03","REWET","Reflood when the field reaches the operating threshold.")])
    st.markdown('<div class="band"><div class="eyebrow">FARMER-FIRST</div><h2>Make the field measurable.</h2><div class="section-copy">Farmers supply the practice, FPOs help aggregate and coordinate, and the MRV layer organises evidence for the project team.</div></div>',unsafe_allow_html=True)

def technology():
    st.set_page_config(page_title="Technology | Asterisk Climos", layout="wide"); shell()
    frame("OUR TECHNOLOGY","Soil to sky. One evidence chain.","Field observations, satellite signals, methane measurement and transparent modelling are combined into one workflow for rice climate projects.")
    tiles([
        ("01","GROUND DATA","Water level, irrigation and crop-stage observations."),
        ("02","SENTINEL-1","SAR-derived relative wetness proxy for field-scale monitoring."),
        ("03","MODELLING","Scenario equations connect water regime with methane and CO₂e outcomes."),
        ("04","PROVENANCE","Keep field, signal, sample, method, model and timestamp attached to every result."),
    ],True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">FIELD VALIDATION</div>
      <h2>Measure methane at the source.</h2>
      <div class="section-copy">
        Satellite and model outputs help us monitor fields at scale, but the project also needs
        direct greenhouse-gas measurements to establish what is happening at the field.
      </div>
      <div style="display:grid;grid-template-columns:1.15fr .85fr;gap:1rem;margin-top:2rem;align-items:stretch;">
        <div class="tile" style="min-height:0;">
          <div class="num">01 / CHAMBER SAMPLING</div>
          <h3>Capture the gas released by the rice field.</h3>
          <p>
            Closed chambers are placed over defined areas of a rice plot. Air samples are collected
            from the chamber headspace at set time intervals so the change in methane concentration
            can be measured.
          </p>
          <div class="num" style="margin-top:1.2rem;">02 / GAS CHROMATOGRAPHY</div>
          <h3>Turn a gas sample into a methane concentration.</h3>
          <p>
            Gas chromatography is the laboratory measurement layer used to quantify methane in the
            collected samples. The concentration measured across time is then used to estimate the
            methane flux from the field.
          </p>
          <div class="num" style="margin-top:1.2rem;">03 / DIGITAL MRV</div>
          <h3>Connect measured data with the digital evidence chain.</h3>
          <p>
            The resulting location-specific measurements can be used as field evidence for calibration,
            validation and transparent MRV alongside satellite observations and modelled scenarios.
          </p>
        </div>
        <div class="tile" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/cd/GCMS_Instrument.jpg" alt="Gas chromatograph laboratory instrument" style="width:100%;height:320px;object-fit:contain;display:block;background:#06110d;" />
          <div style="padding:1.2rem;">
            <div class="num">GAS CHROMATOGRAPHY</div>
          </div>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">FIELD EVIDENCE / PRESS REPORT</div>
      <h2>Why this matters for Code4Nature.</h2>
      <div class="section-copy">
        A recent field report on rice methane highlighted the same measurement pathway that matters
        for our platform: reducing prolonged flooding through Alternate Wetting and Drying (AWD),
        measuring emissions from individual fields, and using laboratory gas chromatography to turn
        collected gas samples into location-specific methane data.
      </div>
      <div class="tiles" style="margin-top:2rem;">
        <div class="tile">
          <div class="num">AWD</div>
          <h3>Reduce prolonged flooding.</h3>
          <p>Periodic dry-downs interrupt the continuously flooded conditions that support methane-producing processes in rice soils.</p>
        </div>
        <div class="tile">
          <div class="num">MEASUREMENT</div>
          <h3>Use chambers + gas chromatography.</h3>
          <p>Field chambers capture gas samples; laboratory gas chromatography quantifies methane concentration so field flux can be estimated from the concentration change over time.</p>
        </div>
        <div class="tile">
          <div class="num">CARBON MRV</div>
          <h3>Build evidence that can be traced.</h3>
          <p>Real, verified, location-specific measurements strengthen the evidence chain needed to connect farm practice, modeled impact and carbon-credit MRV.</p>
        </div>
      </div>
      <div class="footer-note" style="margin-top:1.5rem;">
        Source context: supplied newspaper clipping about rice methane and farmer economics. The report describes AWD,
        field chambers and gas-chromatography analysis; project-specific measurements and verification are still required.
      </div>
    </section>
    """, unsafe_allow_html=True)


def simulator():
    st.set_page_config(page_title="Farm Simulator | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("FARM SIMULATOR","Explore a rice-field scenario.","Use this page for scenario modelling. Map your farm and change assumptions without running satellite/MRV retrieval.")
    render_farm_simulator()

def carbon():
    st.set_page_config(page_title="Carbon Economics | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("CARBON ECONOMICS","See the economics behind the scenario.","Change the area, abatement, carbon price and farmer/FPO share to inspect illustrative USD and INR outcomes.")
    render_market(); render_economics()

def mrv():
    st.set_page_config(page_title="Digital MRV | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("DIGITAL MRV","Field evidence and satellite intelligence.","Use this page for SAR retrieval, relative wetness, VV/VH backscatter and AWD telemetry/MRV evidence.")
    render_mrv()

def policy():
    st.set_page_config(page_title="Policy & FPO | Asterisk Climos", layout="wide"); shell()
    frame("POLICY / FPO","Connect implementation with the enablement layer.","Keep agricultural support, FPO aggregation and carbon-market methodology as distinct pieces of the project architecture.")
    render_policy()

def about():
    st.set_page_config(page_title="About | Asterisk Climos", layout="wide"); shell()

    frame(
        "ABOUT / OUR DIRECTION",
        "Building climate intelligence for rice, water and measurable impact.",
        "Asterisk Climos is a student-driven initiative at IIT Gandhinagar bringing together Earth Science, computer science, data science, remote sensing, machine learning and sustainability."
    )

    st.markdown("""
    <section class="section" style="padding-top:0;">
      <div class="eyebrow">OUR APPROACH</div>
      <h2>One problem. Multiple layers. One measurable impact.</h2>
      <div class="section-copy">
        Climate-smart rice requires more than a single technology. Our approach connects
        farmers and field observations with Earth observation, scientific measurement,
        data-driven modelling, digital MRV and transparent carbon economics.
        The aim is to create an evidence chain from what happens on the farm to
        measurable environmental and economic outcomes.
      </div>
    </section>

    <div class="tiles">
      <div class="tile">
        <div class="num">01 / FIELD</div>
        <h3>Farmers & implementation</h3>
        <p>Understand farming practices, water management and field conditions while keeping the needs of farmers and local partners at the centre.</p>
      </div>
      <div class="tile">
        <div class="num">02 / EARTH OBSERVATION</div>
        <h3>Satellite + GeoAI</h3>
        <p>Use radar and other Earth-observation data with data science and AI to understand field conditions at scale.</p>
      </div>
      <div class="tile">
        <div class="num">03 / SCIENCE</div>
        <h3>dMRV & measurement</h3>
        <p>Combine ground observations, field measurements, laboratory evidence and scientific models to make environmental outcomes traceable.</p>
      </div>
      <div class="tile">
        <div class="num">04 / VALUE</div>
        <h3>Carbon + farmer economics</h3>
        <p>Explore how credible methane reductions and climate-smart practices can connect to transparent carbon and farmer-value pathways.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">OUR IIT GANDHINAGAR MISSION</div>
      <h2>We are students. We can build, test and learn in the field.</h2>
      <div class="section-copy">
        Asterisk Climos is our student-driven attempt to apply science and technology
        to a practical climate problem. We are bringing together Earth Science,
        computer science, data science, remote sensing, machine learning and
        sustainability to build a working prototype—not just a presentation.
      </div>

      <div class="band" style="margin-top:2rem;">
        <div class="eyebrow">OUR MOTTO</div>
        <h2>Learn from the field.<br>Measure with science.<br>Build with technology.<br>Create impact.</h2>
        <div class="section-copy">
          As students of IIT Gandhinagar, our goal is to turn what we learn in classrooms
          and laboratories into useful tools for farmers, researchers, FPOs and climate
          practitioners. We start small, validate our assumptions, stay transparent
          about uncertainty, and improve the system with evidence.
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    tiles([
        ("01","OBSERVE","Understand the field before building the model."),
        ("02","MEASURE","Use Earth observation, field data and scientific methods."),
        ("03","MODEL","Turn observations into transparent, explainable scenarios."),
        ("04","ACT","Design tools that can support climate-smart decisions."),
        ("05","LEARN","Test, validate, document limitations and iterate."),
        ("06","IMPACT","Keep farmers, water, climate and measurable outcomes at the centre.")
    ], True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">OUR DIFFERENCE</div>
      <h2>Student-built does not mean science-light.</h2>
      <div class="section-copy">
        We are building an educational and research-oriented platform around open data,
        documented assumptions and reproducible methods. The project is designed to
        learn through experimentation, field validation and continuous improvement,
        while clearly separating prototype results from independently measured or
        verified outcomes.
      </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-note">Asterisk Climos is an independent IIT Gandhinagar student initiative focused on climate-smart rice, Earth observation, digital MRV and transparent carbon economics.</div>',
        unsafe_allow_html=True
    )

def insights():
    st.set_page_config(page_title="Insights | Asterisk Climos", layout="wide"); shell()
    frame(
        "INSIGHTS / CLIMATE INTELLIGENCE",
        "Rice. Water. Methane. Earth observation.",
        "Research, field evidence and emerging technologies shaping climate-smart rice and digital MRV. These insights are sourced from scientific literature and public institutions rather than company marketing."
    )

    articles = [
        ("01","Mar 19, 2026","India's water security is becoming an agricultural priority",
         "India has 18% of the world's population but only 4% of its water resources. Agriculture consumes roughly 80–90% of India's water, making efficient irrigation, groundwater monitoring and digital water intelligence central to climate-resilient rice.",
         "WORLD BANK / WATER FOR FOOD",
         "https://www.worldbank.org/en/brief/2026/03/19/how-india-is-addressing-its-water-needs"),
        ("02","2026","Optimized rice water management could cut global rice GHG emissions by 39.17%",
         "A global study using 15,458 field observations and machine-learning scenario simulations estimated that optimized water management could reduce rice greenhouse-gas emissions by 39.17% (340.46 Mt CO₂e) while increasing simulated yields by 3.55%. This is a modeled potential, not a guaranteed field outcome.",
         "RESEARCH / GLOBAL RICE",
         "https://agris.fao.org/search/en/providers/122413/records/699588e4e6c33ba92ad5780d"),
        ("03","2026","Smart irrigation is moving toward real-time field monitoring",
         "Recent Indian agricultural-engineering research is combining automated Alternate Wetting and Drying with sensors, controllers and digital monitoring. Reported water savings are experimental results, so field performance still depends on soil, climate, crop and irrigation conditions.",
         "FIELD STUDY / TECHNOLOGY",
         "https://agris.fao.org/search/en/providers/124598/records/69959e8ce6c33ba92ad640e7"),
        ("04","2026","Sentinel-1 can help us see rice-field water conditions through clouds",
         "Sentinel-1 radar provides repeat observations independent of daylight and can support monitoring of waterlogged ground, soil moisture and crop structure. For Asterisk Climos, SAR is an observation layer that complements—not replaces—field measurements and methane MRV.",
         "EARTH OBSERVATION / ESA",
         "https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/10_ways_Sentinel-1_data_lets_us_see_our_world"),
        ("05","Apr 2026","Indian rice research is pushing genetic and ecosystem-level innovation",
         "ICAR-CRRI's 61st Annual Rice Group Meetings highlighted genetic gain, pre-breeding and genome-editing research across rainfed and irrigated ecosystems. Climate-smart rice therefore extends beyond irrigation: varieties, agronomy and ecosystem adaptation matter too.",
         "INDIA / ICAR",
         "https://www.icar.gov.in/en/61st-annual-rice-group-meetings-inaugurated-icar-crri-cuttack"),
        ("06","Mar 2026","AI, drones and digital advisory are entering rice agriculture",
         "ICAR-CRRI has highlighted AI-based precision agriculture, drone applications, digital advisory through RiceXpert, methane-reduction research and nitrogen-efficient technologies. The direction is clear: farm decisions are increasingly supported by connected data and field intelligence.",
         "TECHNOLOGY / ICAR",
         "https://www.icar.gov.in/en/journalists-uttarakhand-visits-icar-crri-cuttack-understand-research-and-development-initiatives"),
        ("07","2026","AWD is powerful—but methane MRV needs more than a dry/wet label",
         "Field research shows that methane response to AWD can vary with timing, crop-residue management and other conditions, while nitrous oxide can also change. A credible MRV system therefore needs water regime, crop stage, residues, weather, nutrients and measured evidence—not a single proxy.",
         "MRV / FIELD EVIDENCE",
         "https://agris.fao.org/search/en/providers/122535/records/65df83da4c5aef494fe31e25"),
        ("08","Jun 11, 2026","Direct-seeded rice is part of India's water-efficiency transition",
         "A World Bank feature on Uttar Pradesh describes direct-seeded rice as a pathway being used to reduce water use, emissions and production costs. It reinforces a broader point for climate-smart rice: practice change has to work agronomically and economically at farm scale.",
         "INDIA / WATER EFFICIENCY",
         "https://www.worldbank.org/en/news/feature/2026/06/11/farming-is-building-a-stronger-rural-economy-in-uttar-pradesh-india"),
    ]

    cards = '<div class="insight-grid">'
    for num, date, title, body, source, url in articles:
        cards += f'''<article class="insight-card">
          <div class="insight-top">
            <div class="num">{num} / {date}</div>
            <div class="insight-source">{source}</div>
          </div>
          <div class="insight-content">
            <h3>{title}</h3>
            <p>{body}</p>
            <a class="insight-link" href="{url}" target="_blank" rel="noopener noreferrer">Read source →</a>
          </div>
        </article>'''
    cards += "</div>"

    st.markdown("""
    <style>
      .insight-grid{
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:1rem;
        margin:0 0 3rem;
      }
      .insight-card{
        overflow:hidden;
        border:1px solid rgba(126,226,177,.13);
        border-radius:20px;
        background:rgba(255,255,255,.035);
        transition:transform .18s ease,border-color .18s ease;
        min-height:300px;
        display:flex;
        flex-direction:column;
      }
      .insight-card:hover{
        transform:translateY(-3px);
        border-color:rgba(126,226,177,.38);
      }
      .insight-top{
        min-height:82px;
        padding:1.15rem 1.25rem;
        background:linear-gradient(135deg,rgba(126,226,177,.10),rgba(102,183,215,.07));
        border-bottom:1px solid rgba(126,226,177,.10);
        display:flex;
        justify-content:space-between;
        gap:1rem;
        align-items:flex-start;
      }
      .insight-source{
        color:#7d998c;
        font-size:.58rem;
        line-height:1.35;
        letter-spacing:.10em;
        font-weight:900;
        text-align:right;
        max-width:48%;
      }
      .insight-content{
        padding:1.25rem;
        display:flex;
        flex-direction:column;
        flex:1;
      }
      .insight-content h3{
        margin:.2rem 0 .7rem;
        color:#edf7f2;
        font-size:1.08rem;
        line-height:1.28;
      }
      .insight-content p{
        margin:0;
        color:#91aa9e;
        line-height:1.65;
        font-size:.86rem;
      }
      .insight-link{
        display:inline-block;
        margin-top:auto;
        padding-top:1.1rem;
        color:#7ee2b1;
        font-size:.78rem;
        font-weight:800;
        text-decoration:none;
      }
      .insight-link:hover{text-decoration:underline;}
      @media(max-width:1000px){.insight-grid{grid-template-columns:1fr 1fr;}}
      @media(max-width:620px){
        .insight-grid{grid-template-columns:1fr;}
        .insight-card{min-height:0;}
        .insight-top{min-height:74px;}
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(cards, unsafe_allow_html=True)

    st.markdown(
        '<div class="band"><div class="eyebrow">THE ASTERISK CLIMOS EVIDENCE CHAIN</div><h2>Practice → observation → measurement → MRV → value.</h2><div class="section-copy">Climate-smart rice is not one number. We connect farmer practice, Earth observation, field measurement, transparent modelling and carbon economics while keeping assumptions and uncertainty visible.</div></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="footer-note">Sources: World Bank, FAO AGRIS-indexed research, ESA Copernicus/Sentinel-1 and ICAR. All insight summaries are paraphrased from the linked sources. Modeled or experimental results are presented as study findings, not universal guarantees.</div>',
        unsafe_allow_html=True
    )

def contact():
    st.set_page_config(page_title="Partner with Asterisk Climos", layout="wide"); shell()
    frame(
        "PARTNER WITH US",
        "Build the evidence chain with us.",
        "Tell us who you are, what you want to contribute and how we can work together."
    )

    # Submit from the visitor's browser to FormSubmit's AJAX endpoint.
    # This avoids the Streamlit server acting as a bot-like relay and keeps
    # the recipient address out of the visible success message.
    partner_form_html = """
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Inter, Arial, sans-serif;
        background: transparent;
        color: #edf7f2;
      }
      .wrap {
        max-width: 900px;
        margin: 0 auto;
        padding: 8px 0 18px;
      }
      .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
      }
      .field { margin-bottom: 14px; }
      .full { grid-column: 1 / -1; }
      label {
        display: block;
        margin: 0 0 7px;
        font-size: 13px;
        font-weight: 700;
        color: #b9cec3;
      }
      input, select, textarea {
        width: 100%;
        border: 1px solid #29483c;
        border-radius: 10px;
        padding: 12px 13px;
        background: #0d1d18;
        color: #edf7f2;
        font: inherit;
        outline: none;
      }
      input:focus, select:focus, textarea:focus {
        border-color: #7ee2b1;
        box-shadow: 0 0 0 2px rgba(126,226,177,.12);
      }
      textarea { min-height: 150px; resize: vertical; }
      .other { display: none; }
      button {
        border: 0;
        border-radius: 11px;
        padding: 12px 18px;
        background: #7ee2b1;
        color: #07120f;
        font-weight: 900;
        cursor: pointer;
      }
      button:disabled { opacity: .65; cursor: wait; }
      .status {
        margin-top: 14px;
        padding: 12px 14px;
        border-radius: 10px;
        display: none;
        line-height: 1.5;
        font-size: 14px;
      }
      .success { display: block; background: rgba(72,227,154,.10); border: 1px solid rgba(72,227,154,.28); color: #bdf4d8; }
      .error { display: block; background: rgba(240,90,90,.10); border: 1px solid rgba(240,90,90,.30); color: #ffd0d0; }
      @media(max-width: 700px) {
        .grid { grid-template-columns: 1fr; }
        .full { grid-column: auto; }
      }
    </style>

    <div class="wrap">
      <form id="partner-form">
        <div class="grid">
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" name="name" required placeholder="Your name">
          </div>

          <div class="field">
            <label for="email">Email *</label>
            <input id="email" name="email" type="email" required placeholder="you@example.com">
          </div>

          <div class="field">
            <label for="partner_type">I am interested in partnering as *</label>
            <select id="partner_type" name="partner_type" required>
              <option value="Farmers">Farmers</option>
              <option value="FPOs">FPOs</option>
              <option value="Research teams">Research teams</option>
              <option value="Carbon-market organisations">Carbon-market organisations</option>
              <option value="Technology partners">Technology partners</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="field other" id="other-wrap">
            <label for="other_type">Please define your partner type *</label>
            <input id="other_type" name="other_type" placeholder="e.g. NGO, investor, government body">
          </div>

          <div class="field">
            <label for="organisation">Organisation / Farm / Institution</label>
            <input id="organisation" name="organisation" placeholder="Optional">
          </div>

          <div class="field">
            <label for="phone">Phone / WhatsApp</label>
            <input id="phone" name="phone" placeholder="Optional">
          </div>

          <div class="field full">
            <label for="message">Tell us about the partnership *</label>
            <textarea id="message" name="message" required placeholder="What do you want to collaborate on, and how can we work together?"></textarea>
          </div>
        </div>

        <input type="hidden" name="_subject" value="New Code4Nature partnership request">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_replyto" id="_replyto">

        <button id="submit-btn" type="submit">Send partnership request</button>
        <div id="status" class="status"></div>
      </form>
    </div>

    <script>
      const form = document.getElementById("partner-form");
      const typeSelect = document.getElementById("partner_type");
      const otherWrap = document.getElementById("other-wrap");
      const otherInput = document.getElementById("other_type");
      const emailInput = document.getElementById("email");
      const replyTo = document.getElementById("_replyto");
      const button = document.getElementById("submit-btn");
      const status = document.getElementById("status");

      function toggleOther() {
        const isOther = typeSelect.value === "Other";
        otherWrap.style.display = isOther ? "block" : "none";
        otherInput.required = isOther;
      }

      typeSelect.addEventListener("change", toggleOther);
      toggleOther();

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        status.className = "status";
        status.textContent = "";
        replyTo.value = emailInput.value.trim();
        button.disabled = true;
        button.textContent = "Sending...";

        const data = Object.fromEntries(new FormData(form).entries());
        if (data.partner_type === "Other") {
          data.partner_type = data.other_type || "Other";
        }
        delete data.other_type;

        try {
          const response = await fetch("https://formsubmit.co/ajax/meghdatt712@gmail.com", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify(data)
          });

          let result = {};
          try {
            result = await response.json();
          } catch (_) {}

          if (!response.ok || result.success === false) {
            throw new Error(result.message || ("Email service returned HTTP " + response.status));
          }

          status.className = "status success";
          status.textContent = "Thanks! Your partnership request has been submitted.";
          form.reset();
          toggleOther();
        } catch (error) {
          status.className = "status error";
          status.textContent = "We couldn't submit the request right now. Please try again in a moment.";
          console.error("Partner form submission error:", error);
        } finally {
          button.disabled = false;
          button.textContent = "Send partnership request";
        }
      });
    </script>
    """

    components.html(partner_form_html, height=610, scrolling=False)

    st.markdown(
        '<div class="footer-note">Your information is used only to respond to the partnership request.</div>',
        unsafe_allow_html=True,
    )

