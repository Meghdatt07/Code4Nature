import streamlit as st

from app.dashboard import (
    init_state,
    render_economics,
    render_market,
    render_mrv,
    render_policy,
)


def inject_site_css():
    st.markdown("""
    <style>
    .stApp { background:#f4f0e7; color:#183126; }
    [data-testid="stHeader"] { background:rgba(244,240,231,.92); }
    [data-testid="stSidebar"] { display:none; }
    .block-container { max-width:1400px; padding:2rem 4rem 5rem; }
    .site-brand { display:flex; justify-content:space-between; align-items:center; padding:.5rem 0 1.2rem; border-bottom:1px solid rgba(24,49,38,.14); margin-bottom:1rem; }
    .brand { font-size:1.05rem; font-weight:900; letter-spacing:.13em; color:#183126; }
    .brand span { color:#648b6f; }
    .status { font-size:.68rem; letter-spacing:.14em; color:#6b7c72; }
    .hero { position:relative; overflow:hidden; background:#e5eee2; min-height:560px; border-radius:4px; padding:5rem 5rem; margin:1rem 0 3rem; border:1px solid rgba(24,49,38,.10); }
    .hero:after { content:""; position:absolute; width:520px; height:520px; right:-160px; top:-180px; border-radius:50%; background:radial-gradient(circle,rgba(104,145,112,.35),transparent 68%); }
    .eyebrow,.kicker { color:#63866c; font-size:.7rem; letter-spacing:.16em; font-weight:900; text-transform:uppercase; }
    .hero h1 { position:relative; z-index:2; max-width:950px; font-size:clamp(3.5rem,7vw,7rem); line-height:.9; letter-spacing:-.065em; margin:1.3rem 0; color:#183126; }
    .hero h1 em { color:#638b6e; font-style:normal; }
    .lead { max-width:760px; font-size:1.08rem; line-height:1.7; color:#52675d; position:relative; z-index:2; }
    .btnrow { display:flex; gap:.8rem; margin-top:2rem; position:relative; z-index:3; }
    .section { padding:4rem 0; }
    .section h2 { font-size:clamp(2.2rem,4vw,4.4rem); line-height:.95; letter-spacing:-.055em; margin:.7rem 0 1.2rem; color:#183126; }
    .copy { color:#61736a; line-height:1.75; font-size:1rem; }
    .card { background:#fbfaf5; border:1px solid rgba(24,49,38,.13); padding:1.5rem; min-height:180px; box-shadow:0 18px 55px rgba(24,49,38,.05); }
    .card h3 { margin:.6rem 0 .4rem; color:#183126; }
    .num { color:#719078; font-weight:900; font-size:.75rem; letter-spacing:.12em; }
    .darkband { background:#183126; color:#eef3eb; padding:4rem; margin:2rem -4rem; }
    .darkband h2 { color:#eef3eb; }
    .darkband .copy { color:#b9c8be; }
    .quote { font-size:1.8rem; line-height:1.2; letter-spacing:-.03em; color:#183126; max-width:900px; }
    .footer-note { border-top:1px solid rgba(24,49,38,.13); margin-top:3rem; padding-top:1.5rem; color:#77877e; font-size:.75rem; }
    @media(max-width:800px){ .block-container{padding:1rem 1.2rem 3rem}.hero{padding:3rem 1.5rem;min-height:500px}.hero h1{font-size:3.5rem}.darkband{margin:2rem -1.2rem;padding:3rem 1.2rem}.site-brand{margin-bottom:.5rem} }
    </style>
    """, unsafe_allow_html=True)


def frame(title, text, eyebrow="CODE4NATURE"):
    st.markdown(f"""
    <div class="section" style="padding-top:2rem">
      <div class="eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
      <p class="copy" style="max-width:820px">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def card_grid(items):
    cols = st.columns(len(items))
    for col, (num, title, body) in zip(cols, items):
        with col:
            st.markdown(f'<div class="card"><div class="num">{num}</div><h3>{title}</h3><div class="copy">{body}</div></div>', unsafe_allow_html=True)


def home():
    st.set_page_config(page_title="Code4Nature — Rice Climate Intelligence", page_icon="🌾", layout="wide")
    inject_site_css()
    init_state()
    st.markdown('<div class="site-brand"><div class="brand">CODE<span>4</span>NATURE</div><div class="status">RICE CLIMATE INTELLIGENCE · SYSTEM ONLINE</div></div>', unsafe_allow_html=True)
    st.markdown("""
    <section class="hero">
      <div class="eyebrow">CODE4NATURE / RICE CLIMATE INTELLIGENCE</div>
      <h1>Turn rice farming into <em>measurable climate value.</em></h1>
      <p class="lead">Field intelligence for alternate wetting and drying, methane reduction, satellite evidence, digital MRV and transparent carbon economics — built around the people who grow rice.</p>
    </section>
    """, unsafe_allow_html=True)
    frame("A field-level climate platform", "Rice agriculture can become a measurable climate opportunity when water management, satellite observations and economics are connected in one evidence chain.", "THE OPPORTUNITY")
    card_grid([
        ("01","Climate-smart rice","Make AWD understandable, actionable and visible at field scale."),
        ("02","Digital MRV","Connect ground observations with satellite evidence and transparent calculations."),
        ("03","Carbon economics","Translate scenario abatement into farmer/FPO and company economics."),
    ])
    st.markdown('<div class="darkband"><div class="kicker">FROM FIELD TO VALUE</div><h2>Assess. Monitor. Measure. Verify. Value.</h2><p class="copy">Select a farm, draw its boundary, inspect the water regime, query the SAR layer and explore the carbon-value pathway.</p></div>', unsafe_allow_html=True)
    frame("Explore the platform", "Each destination is a separate application page rather than a long scrolling dashboard.", "DISCOVER")
    card_grid([
        ("01","Climate-smart rice","Water, methane and farmer-first implementation."),
        ("02","Our technology","Satellite + ground evidence + modelling."),
        ("03","Farm simulator","Move the farm marker and draw the field boundary."),
        ("04","Digital MRV","Inspect evidence and methodology assumptions."),
    ])
    st.markdown('<div class="footer-note">Prototype demonstration. Methane reductions, carbon quantities, prices and financial outcomes are illustrative unless independently measured and verified.</div>', unsafe_allow_html=True)


def climate_smart_rice():
    st.set_page_config(page_title="Climate-smart Rice — Code4Nature", layout="wide")
    inject_site_css()
    frame("Rice can use less water and create better evidence.", "Alternate Wetting & Drying (AWD) is the practical story at the field: manage water deliberately, observe the field state, and create a traceable evidence trail.", "CLIMATE-SMART RICE")
    card_grid([
        ("01","SEEDING","Start with field context, variety and agronomic practice."),
        ("02","IRRIGATION","Move from continuous flooding toward controlled wetting and drying."),
        ("03","HARVEST","Carry the evidence chain through the full growing season."),
    ])
    st.markdown('<div class="section"><div class="quote">“The goal is not another dashboard. The goal is a field process that can be observed, explained and valued.”</div></div>', unsafe_allow_html=True)
    frame("Farmer-first implementation", "FPOs can aggregate farms, coordinate training and help connect field practice with MRV workflows. This prototype keeps those roles visible rather than hiding them behind a carbon number.", "COMMUNITY")
    card_grid([
        ("A","FARMER","Adopt the practice and supply field evidence."),
        ("B","FPO","Aggregate farms and coordinate implementation."),
        ("C","MRV PLATFORM","Organise evidence and calculations."),
    ])


def technology():
    st.set_page_config(page_title="Technology — Code4Nature", layout="wide")
    inject_site_css()
    frame("Assess. Monitor. Measure.", "Code4Nature combines field observations, satellite signals and transparent process-based calculations to create a digital evidence layer for rice climate projects.", "OUR TECHNOLOGY")
    card_grid([
        ("01","GROUND DATA","Water-level observations provide calibration and context."),
        ("02","SENTINEL-1 SAR","Radar observations provide a relative wetness signal across the farm."),
        ("03","MODELLING","AWD state is translated into methane and CO2e scenario outputs."),
        ("04","DIGITAL MRV","Evidence, assumptions and calculations remain inspectable."),
    ])
    st.markdown('<div class="darkband"><div class="kicker">EVIDENCE STACK</div><h2>Ground truth → satellite retrievals → models → evidence.</h2><p class="copy">The platform is designed so a carbon number is never presented without the assumptions and evidence pathway behind it.</p></div>', unsafe_allow_html=True)


def simulator():
    st.set_page_config(page_title="Farm Simulator — Code4Nature", layout="wide")
    inject_site_css()
    init_state()
    frame("Move the farm. Draw the boundary. Explore the signal.", "Use the interactive map to select a location or draw a farm polygon. The selected area feeds the soil-moisture/SAR and carbon scenario tools.", "FARM SIMULATOR")
    render_mrv()


def carbon():
    st.set_page_config(page_title="Carbon Economics — Code4Nature", layout="wide")
    inject_site_css()
    init_state()
    frame("Carbon economics without hiding the assumptions.", "Explore global reference pricing, India conversion proxies and the farmer/FPO versus MRV-company split using the current scenario inputs.", "CARBON ECONOMICS")
    render_market()
    render_economics()


def mrv():
    st.set_page_config(page_title="Digital MRV — Code4Nature", layout="wide")
    inject_site_css()
    init_state()
    frame("Evidence you can inspect.", "Digital MRV connects farm observations, satellite signals and scenario equations. The outputs below are demonstrator values, not certified carbon credits.", "DIGITAL MRV")
    render_mrv()


def policy():
    st.set_page_config(page_title="Policy & FPO — Code4Nature", layout="wide")
    inject_site_css()
    frame("Policy, finance and the FPO layer.", "Understand the role of agriculture infrastructure support, FPO aggregation and the separation between voluntary carbon-market scenarios and India's evolving compliance framework.", "POLICY / FPO")
    render_policy()


def about():
    st.set_page_config(page_title="About — Code4Nature", layout="wide")
    inject_site_css()
    frame("Technology grounded in the field.", "Code4Nature is a climate-intelligence prototype focused on connecting rice farming practice with measurable evidence and transparent carbon economics.", "ABOUT")
    card_grid([
        ("01","EARTH SCIENCE","Remote sensing, soil and water context."),
        ("02","DATA","Transparent calculations and evidence."),
        ("03","IMPACT","Farmer/FPO economics and climate value."),
    ])


def insights():
    st.set_page_config(page_title="Insights — Code4Nature", layout="wide")
    inject_site_css()
    frame("Field notes, methods and climate intelligence.", "A growing library for understanding rice methane, AWD, remote sensing, digital MRV and carbon markets.", "INSIGHTS")
    card_grid([
        ("01","Why rice emits methane","How flooded soil creates anaerobic conditions."),
        ("02","What SAR can tell us","Why radar is useful for monitoring relative surface wetness."),
        ("03","From methane to CO2e","How scenario assumptions become a transparent calculation."),
    ])


def contact():
    st.set_page_config(page_title="Partner with Code4Nature", layout="wide")
    inject_site_css()
    frame("Build the evidence chain with us.", "For farmers, FPOs, research teams, carbon-market organisations and technology partners exploring climate-smart rice.", "PARTNER WITH US")
    with st.form("partner_form"):
        name = st.text_input("Name")
        organisation = st.text_input("Organisation")
        email = st.text_input("Email")
        message = st.text_area("What are you building?")
        submitted = st.form_submit_button("Send partnership request")
        if submitted:
            st.success("Thanks — the prototype captured your request locally for this demo. Connect an email/CRM service before production use.")
