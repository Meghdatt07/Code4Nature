import streamlit as st

try:
    from .dashboard import init_state, render_economics, render_market, render_mrv, render_policy
except ImportError:
    from dashboard import init_state, render_economics, render_market, render_mrv, render_policy

def inject_site_css():
    st.markdown("""<style>
:root{--bg:#07120f;--panel:#0d1d18;--line:#244137;--text:#edf7f2;--muted:#9ab3a8;--accent:#7ee2b1;--water:#66b7d7}
.stApp{background:radial-gradient(circle at 78% 0%,#15382d 0,#07120f 42%);color:var(--text)}
[data-testid="stHeader"]{background:rgba(7,18,15,.88)}
[data-testid="stSidebar"]{background:#091713}
.block-container{max-width:1400px!important;padding:1.25rem 3rem 4rem!important}
.site-head{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding:.5rem 0 1.15rem;margin-bottom:1.2rem}
.brand{display:flex;align-items:center;gap:.65rem;font-weight:900;letter-spacing:.08em}
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
@media(max-width:900px){.block-container{padding:1rem 1.2rem 3rem!important}.flow,.tiles,.tiles.four{grid-template-columns:1fr 1fr}.hero{padding:3rem 1.5rem}.hero h1{font-size:3.7rem}.band{margin:1rem -1.2rem;padding-left:1.2rem;padding-right:1.2rem}}
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
</style>""", unsafe_allow_html=True)

def shell():
    inject_site_css()
    st.markdown('<div class="site-head"><div class="brand"><div class="brand-mark">A</div><div>ASTERISK CLIMOS<small>CLIMATE INTELLIGENCE</small></div></div><div class="status"><span class="dot"></span>SYSTEM ONLINE</div></div>', unsafe_allow_html=True)

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
      <div class="hero-actions"><a class="a-btn primary" href="/simulator">Run Farm Simulation →</a><a class="a-btn secondary" href="/technology">Explore Technology</a></div>
    </section>''', unsafe_allow_html=True)
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
    frame("OUR TECHNOLOGY","Soil to sky. One evidence chain.","Field observations, satellite signals and deterministic demonstration models are combined into one inspectable workflow.")
    tiles([("01","GROUND DATA","Water level, irrigation and crop-stage observations."),("02","SENTINEL-1","SAR-derived relative wetness proxy when live credentials are configured."),("03","MODELLING","Scenario equations for water, methane and CO₂e."),("04","PROVENANCE","Keep value, unit, source, model and timestamp attached.")],True)
    st.markdown('<div class="band"><div class="eyebrow">TRANSPARENT BY DESIGN</div><h2>Simulation ≠ measurement.</h2><div class="section-copy">Every dashboard estimate in this prototype is clearly marked as simulated or illustrative until project-specific measurement, validation and verification are available.</div></div>',unsafe_allow_html=True)

def simulator():
    st.set_page_config(page_title="Farm Simulator | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("FARM SIMULATOR","Move the farm. Draw the boundary.","Click a location, choose a preset or draw a polygon/rectangle. The selected geometry feeds the demonstration area and SAR workflow.")
    render_mrv()

def carbon():
    st.set_page_config(page_title="Carbon Economics | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("CARBON ECONOMICS","See the economics behind the scenario.","Change the area, abatement, carbon price and farmer/FPO share to inspect illustrative USD and INR outcomes.")
    render_market(); render_economics()

def mrv():
    st.set_page_config(page_title="Digital MRV | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("DIGITAL MRV","Measure what is simulated—and what needs field evidence.","Monitor, report and verify are kept as separate steps.")
    render_mrv()

def policy():
    st.set_page_config(page_title="Policy & FPO | Asterisk Climos", layout="wide"); shell()
    frame("POLICY / FPO","Connect implementation with the enablement layer.","Keep agricultural support, FPO aggregation and carbon-market methodology as distinct pieces of the project architecture.")
    render_policy()

def about():
    st.set_page_config(page_title="About | Asterisk Climos", layout="wide"); shell()
    frame("ABOUT","Climate intelligence for rice.","A Code4Nature prototype focused on rice water management, remote sensing, digital MRV and transparent carbon economics.")
    tiles([("01","EARTH SCIENCE","Remote sensing, soil and water context."),("02","DATA","Transparent calculations and evidence."),("03","IMPACT","Farmer/FPO economics and climate value.")])

def insights():
    st.set_page_config(page_title="Insights | Asterisk Climos", layout="wide"); shell()
    frame("INSIGHTS","Field notes, methods and context.","Explore the science and implementation questions around rice methane, AWD, remote sensing, MRV and carbon economics.")
    tiles([("01","Rice methane","Why prolonged flooding matters for methane formation."),("02","SAR evidence","How radar can support relative wetness monitoring."),("03","From methane to CO₂e","How a scenario becomes a transparent calculation.")])

def contact():
    st.set_page_config(page_title="Partner with Asterisk Climos", layout="wide"); shell()
    frame("PARTNER WITH US","Build the evidence chain with us.","For farmers, FPOs, research teams, carbon-market organisations and technology partners.")
    with st.form("partner_form"):
        name=st.text_input("Name"); organisation=st.text_input("Organisation"); email=st.text_input("Email"); message=st.text_area("What are you building?")
        if st.form_submit_button("Send partnership request"):
            st.success("Demo request captured locally. Connect an email/CRM service before production use.")
