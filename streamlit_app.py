from pathlib import Path

import streamlit as st

from app.site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology, set_page_routes


APP_DIR = Path(__file__).resolve().parent
DARK_LOGO = str(APP_DIR / "assets" / "logo-dark.svg")
LIGHT_LOGO = str(APP_DIR / "assets" / "logo-light.svg")
DARK_FAVICON = str(APP_DIR / "assets" / "asterisk-climos-favicon.png")
LIGHT_FAVICON = str(APP_DIR / "assets" / "asterisk-climos-favicon.png")

# Streamlit exposes the active light/dark theme to the app. Use the matching
# Asterisk Climos artwork for both the header logo and browser favicon.
try:
    THEME_TYPE = st.context.theme.type
except Exception:
    THEME_TYPE = "dark"

ACTIVE_LOGO = LIGHT_LOGO if THEME_TYPE == "light" else DARK_LOGO
ACTIVE_FAVICON = LIGHT_FAVICON if THEME_TYPE == "light" else DARK_FAVICON

st.set_page_config(
    page_title="Asterisk Climos | Code4Nature",
    page_icon=ACTIVE_FAVICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""<style>
html,body,[data-testid="stAppViewContainer"],.stApp{background:#07120f!important;color:#edf7f2!important}
[data-testid="stHeader"]{background:rgba(7,18,15,.88)!important}
[data-testid="stSidebar"]{display:none!important}
.block-container{max-width:1400px!important}

/* Remove Streamlit's automatic heading/link anchor icon. Keep normal page/navigation links visible. */
.stMarkdownContainer h1 a,
.stMarkdownContainer h2 a,
.stMarkdownContainer h3 a,
.stMarkdownContainer h4 a,
.stMarkdownContainer h5 a,
.stMarkdownContainer h6 a,
[data-testid="stHeading"] a,
.stHeadingWithActionElements a { display:none !important; visibility:hidden !important; pointer-events:none !important; }

/* Hide Streamlit's automatic heading/link anchor icon. */
[data-testid="stHeaderActionElements"],
[data-testid="StyledLinkIconContainer"] { display:none !important; }
</style>""", unsafe_allow_html=True)

pages=[
 st.Page(home,title="Home",icon=":material/home:",url_path="",default=True),
 st.Page(climate_smart_rice,title="Climate-smart rice",icon=":material/water_drop:",url_path="climate-smart-rice"),
 st.Page(technology,title="Technology",icon=":material/satellite_alt:",url_path="technology"),
 st.Page(simulator,title="Farm simulator",icon=":material/map:",url_path="simulator"),
 st.Page(carbon,title="Carbon economics",icon=":material/eco:",url_path="carbon-economics"),
 st.Page(mrv,title="Digital MRV",icon=":material/fact_check:",url_path="mrv"),
 st.Page(policy,title="Policy / FPO",icon=":material/account_balance:",url_path="policy"),
 st.Page(insights,title="Insights",icon=":material/auto_stories:",url_path="insights"),
 st.Page(about,title="About",icon=":material/info:",url_path="about"),
 st.Page(contact,title="Partner with us",icon=":material/handshake:",url_path="partner-with-us"),
]

# Hide Streamlit's default navigation and replace it with one compact MENU
# button on the top-right, while st.logo owns the top-left brand position.
current_page = st.navigation(pages, position="hidden")

# First-visit opening screen. The button sets session state and reveals the real Streamlit site.
if not st.session_state.get("asterisk_intro_seen", False):
    intro_logo_svg = (APP_DIR / "assets" / "logo-dark.svg").read_text(encoding="utf-8")

    st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], footer, #MainMenu { display: none !important; }
    [data-testid="stAppViewContainer"], .stApp, .block-container {
        background: #07120f !important;
    }
    .block-container {
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    #asterisk-intro-overlay {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        min-height: 620px;
        z-index: 999990;
        overflow: hidden;
        color: #edf7f2;
        background: #07120f;
        isolation: isolate;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    #asterisk-intro-overlay::before {
        content: "";
        position: absolute;
        inset: -3%;
        z-index: -2;
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2400&q=90");
        background-size: cover;
        background-position: 48% 50%;
        transform: scale(1.04);
    }
    #asterisk-intro-overlay .ac-intro-video {
        position: absolute;
        inset: 0;
        z-index: 0;
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        background: #12241b url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2400&q=90") center / cover no-repeat;
        transform: scale(1.04);
        animation: ac-field-drift 28s ease-in-out infinite alternate;
    }
    #asterisk-intro-overlay .ac-announcement,
    #asterisk-intro-overlay .ac-nav,
    #asterisk-intro-overlay .ac-copy,
    #asterisk-intro-overlay .ac-foot,
    #asterisk-intro-overlay .ac-orbit,
    #asterisk-intro-overlay .ac-flying-logo,
    #asterisk-intro-overlay .ac-media-credit {
        z-index: 3;
    }
    #asterisk-intro-overlay .ac-media-credit {
        position: absolute;
        top: 112px;
        right: 25px;
        max-width: 42vw;
        color: rgba(237,247,242,.68);
        font-size: 9px;
        letter-spacing: .05em;
        text-align: right;
        pointer-events: none;
    }
    #asterisk-intro-overlay::after {
        content: "";
        position: absolute;
        inset: 0;
        z-index: 2;
        background:
          linear-gradient(90deg, rgba(3,16,9,.91) 0%, rgba(3,16,9,.70) 48%, rgba(3,16,9,.48) 100%),
          linear-gradient(180deg, rgba(3,16,9,.28), rgba(3,16,9,.18) 55%, rgba(3,16,9,.72));
    }
    #asterisk-intro-overlay * { box-sizing: border-box; }
    #asterisk-intro-overlay .ac-announcement {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 32px;
        display: flex; align-items: center; justify-content: center;
        padding: 0 14px;
        color: #9ab3a8;
        background: rgba(7,18,15,.78);
        border-bottom: 1px solid rgba(139,207,166,.16);
        font-size: 10px;
        letter-spacing: .10em;
        text-align: center;
    }
    #asterisk-intro-overlay .ac-announcement span { color: #8bcfa6; margin-left: 7px; }
    #asterisk-intro-overlay .ac-nav {
        position: absolute;
        top: 32px; left: 0; right: 0;
        min-height: 70px;
        display: flex; align-items: center;
        gap: 20px;
        padding: 10px 34px;
        border-bottom: 1px solid rgba(139,207,166,.13);
        background: rgba(7,18,15,.24);
    }
    #asterisk-intro-overlay .ac-target {
        width: 162px; height: 40px; flex: 0 0 162px;
        visibility: hidden;
    }
    #asterisk-intro-overlay .ac-nav-links {
        margin-left: auto;
        display: flex; align-items: center; gap: 25px;
        color: #c2d8cc;
        font-size: 11px;
        white-space: nowrap;
        opacity: 0;
        animation: ac-nav-reveal .6s 4.7s ease-out forwards;
    }
    #asterisk-intro-overlay .ac-nav-cta {
        border-radius: 9px;
        padding: 10px 14px;
        background: #8bcfa6;
        color: #08140f;
        font-size: 11px;
        font-weight: 800;
        white-space: nowrap;
        opacity: 0;
        animation: ac-nav-reveal .6s 4.85s ease-out forwards;
    }
    #asterisk-intro-overlay .ac-copy {
        position: absolute;
        left: clamp(24px, 5.2vw, 76px);
        top: clamp(190px, 29vh, 285px);
        width: min(720px, 83vw);
        opacity: 0;
        transform: translateY(14px);
        animation: ac-copy-reveal .8s 4.45s cubic-bezier(.22,.75,.18,1) forwards;
    }
    #asterisk-intro-overlay .ac-kicker {
        color: #a8d9bc;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .18em;
    }
    #asterisk-intro-overlay h1 {
        margin: 17px 0 0;
        max-width: 760px;
        color: #edf7f2;
        font-size: clamp(52px, 8.2vw, 96px);
        font-weight: 750;
        line-height: .94;
        letter-spacing: -.065em;
    }
    #asterisk-intro-overlay h1 em {
        display: block;
        max-width: 640px;
        margin-top: 13px;
        color: #8bcfa6;
        font-size: .48em;
        font-weight: 650;
        font-style: normal;
        line-height: 1.12;
        letter-spacing: -.035em;
    }
    #asterisk-intro-overlay .ac-description {
        max-width: 590px;
        margin: 21px 0 0;
        color: #c5d8cd;
        font-size: 14px;
        line-height: 1.75;
    }
    #asterisk-intro-overlay .ac-foot {
        position: absolute;
        left: clamp(24px, 5.2vw, 76px);
        bottom: 28px;
        color: #8bac98;
        font-size: 9px;
        letter-spacing: .16em;
        opacity: 0;
        animation: ac-nav-reveal .7s 4.8s ease-out forwards;
    }
    #asterisk-intro-overlay .ac-orbit {
        position: absolute;
        left: 50%; top: 50%;
        width: 210px; height: 210px;
        margin: -105px 0 0 -105px;
        border: 1px solid rgba(139,207,166,.34);
        border-top-color: #8bcfa6;
        border-radius: 50%;
        opacity: 0;
        pointer-events: none;
        animation: ac-orbit-pulse 3.2s ease-in-out both;
    }
    #asterisk-intro-overlay .ac-flying-logo {
        position: absolute;
        top: 50%; left: 50%;
        width: min(600px, 88vw);
        --dock-scale: .27;
        height: auto;
        opacity: 0;
        transform: translate(-50%,-50%) scale(.78);
        transform-origin: center;
        animation: ac-logo-dock 5.4s cubic-bezier(.22,.75,.18,1) forwards;
        filter: drop-shadow(0 8px 35px rgba(0,0,0,.18));
    }
    #asterisk-intro-overlay .ac-flying-logo svg {
        display: block; width: 100%; height: auto; overflow: visible;
    }
    #asterisk-intro-overlay .ac-flying-logo svg > g {
        transform-box: fill-box;
        transform-origin: center;
        animation: ac-mark-rotation 3.2s cubic-bezier(.45,0,.55,1) both;
    }
    #asterisk-intro-overlay .ac-flying-logo svg text {
        opacity: 0;
        animation: ac-wordmark-reveal .8s 3.05s ease-out forwards;
    }
    div.st-key-intro_enter {
        position: fixed !important;
        z-index: 1000004 !important;
        left: clamp(24px, 5.2vw, 76px) !important;
        top: 72vh !important;
        width: auto !important;
        max-width: calc(100vw - 48px) !important;
        margin: 0 !important;
        opacity: 0;
        animation: ac-cta-reveal .55s 4.8s ease-out forwards;
    }
    div.st-key-intro_enter button {
        min-height: 46px !important;
        padding: 12px 17px !important;
        border: 0 !important;
        border-radius: 10px !important;
        background: #8bcfa6 !important;
        color: #08140f !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        box-shadow: 0 9px 28px rgba(0,0,0,.22) !important;
    }
    div.st-key-intro_enter button:hover { background: #a4e5bb !important; }
    div.st-key-intro_skip {
        position: fixed !important;
        z-index: 1000005 !important;
        top: 49px !important;
        right: 25px !important;
        width: auto !important;
        margin: 0 !important;
    }
    div.st-key-intro_skip button {
        min-height: 38px !important;
        border: 1px solid rgba(237,247,242,.32) !important;
        border-radius: 9px !important;
        background: rgba(7,18,15,.42) !important;
        color: #edf7f2 !important;
        font-size: 11px !important;
    }
    @keyframes ac-logo-dock {
        0% { opacity: 0; transform: translate(-50%,-50%) scale(.78); }
        5% { opacity: 1; transform: translate(-50%,-50%) scale(1); }
        57% { opacity: 1; transform: translate(-50%,-50%) scale(1); }
        100% { opacity: 1; transform: translate(calc(-50vw + 34px),calc(-50vh + 50px)) scale(var(--dock-scale, .27)); }
    }
    @keyframes ac-mark-rotation {
        0% { transform: rotate(-360deg); }
        100% { transform: rotate(0deg); }
    }
    @keyframes ac-wordmark-reveal { to { opacity: 1; } }
    @keyframes ac-copy-reveal { to { opacity: 1; transform: translateY(0); } }
    @keyframes ac-nav-reveal { to { opacity: 1; } }
    @keyframes ac-cta-reveal { to { opacity: 1; } }
    @keyframes ac-orbit-pulse {
        0% { opacity: 0; transform: scale(.88); }
        18% { opacity: .45; transform: scale(1); }
        100% { opacity: 0; transform: scale(1.13); }
    }
    @keyframes ac-field-drift {
        0% { background-position: 46% 18%; transform: scale(1.04); }
        100% { background-position: 54% 78%; transform: scale(1.10); }
    }
    @media (max-width: 650px) {
        #asterisk-intro-overlay .ac-nav { padding: 10px 20px; }
        #asterisk-intro-overlay .ac-target { width: 128px; flex-basis: 128px; }
        #asterisk-intro-overlay .ac-nav-links { display: none; }
        #asterisk-intro-overlay .ac-nav-cta { display: none; }
        #asterisk-intro-overlay .ac-copy {
            top: 25vh; left: 23px; width: calc(100vw - 46px);
        }
        #asterisk-intro-overlay h1 { font-size: clamp(49px, 13vw, 66px); }
        #asterisk-intro-overlay .ac-description { font-size: 13px; line-height: 1.65; }
        #asterisk-intro-overlay .ac-flying-logo { width: min(390px, 94vw); --dock-scale: .32; }
        div.st-key-intro_enter { top: auto !important; bottom: 64px !important; left: 23px !important; }
        div.st-key-intro_skip { top: 43px !important; right: 14px !important; }
        #asterisk-intro-overlay .ac-foot { left: 23px; right: 20px; bottom: 20px; font-size: 8px; }
        #asterisk-intro-overlay .ac-media-credit { top: 108px; right: 16px; max-width: 48vw; font-size: 8px; }
    }
    @media (prefers-reduced-motion: reduce) {
        #asterisk-intro-overlay::before { animation: none !important; }
        #asterisk-intro-overlay .ac-intro-video { display: none !important; animation: none !important; }
        #asterisk-intro-overlay .ac-orbit,
        #asterisk-intro-overlay .ac-flying-logo,
        #asterisk-intro-overlay .ac-flying-logo svg > g,
        #asterisk-intro-overlay .ac-flying-logo svg text,
        #asterisk-intro-overlay .ac-copy,
        #asterisk-intro-overlay .ac-nav-links,
        #asterisk-intro-overlay .ac-nav-cta,
        #asterisk-intro-overlay .ac-foot,
        div.st-key-intro_enter { animation-duration: .01ms !important; animation-delay: 0ms !important; }
        #asterisk-intro-overlay .ac-copy { opacity: 1; transform: none; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="asterisk-intro-overlay" aria-label="Asterisk Climos website introduction">
      <video class="ac-intro-video" autoplay muted loop playsinline preload="metadata" aria-hidden="true" poster="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2400&q=90">
        <source src="https://videos.pexels.com/video-files/6981379/6981379-hd_1920_1080_25fps.mp4" type="video/mp4">
      </video>
      <div class="ac-announcement">Rice methane + water intelligence <span>· Asterisk Climos</span></div>
      <div class="ac-nav">
        <div class="ac-target" aria-hidden="true"></div>
        <div class="ac-nav-links"><span>Rice carbon credits</span><span>Our technology</span><span>Insights</span></div>
        <span class="ac-nav-cta">Satellite · Field science · Water intelligence</span>
      </div>
      <div class="ac-copy">
        <div class="ac-kicker">RICE CARBON CREDITS · METHANE INTELLIGENCE</div>
        <h1>Methane.<em>The next frontier in climate impact.</em></h1>
        <p class="ac-description">Asterisk Climos combines satellite evidence, field science and water intelligence to make methane reductions in rice farming visible, measurable and valuable.</p>
      </div>
      <div class="ac-foot">SATELLITE EVIDENCE · FIELD SCIENCE · WATER INTELLIGENCE</div>
      <div class="ac-media-credit">Farm footage: Mikhail Nilov / Pexels</div>
      <div class="ac-orbit" aria-hidden="true"></div>
      <div class="ac-flying-logo" aria-hidden="true">__INTRO_LOGO_SVG__</div>
    </div>
    """.replace("__INTRO_LOGO_SVG__", intro_logo_svg), unsafe_allow_html=True)

    skip_intro = st.button("Skip intro →", key="intro_skip")
    enter_site = st.button("Start your methane journey  →", key="intro_enter")
    if skip_intro or enter_site:
        st.session_state["asterisk_intro_seen"] = True
        st.rerun()
    st.stop()

st.logo(ACTIVE_LOGO, size="medium")

_, menu_col = st.columns([7.5, 1.25])
with menu_col:
    selected_page = st.menu_button(
        "MENU",
        options=[
            "Home",
            "Climate-smart rice",
            "Technology",
            "Farm simulator",
            "Carbon economics",
            "Digital MRV",
            "Policy / FPO",
            "Insights",
            "About",
            "Partner with us",
        ],
        icon=":material/menu:",
        width="stretch",
        key="site_nav",
    )

page_lookup = {
    "Home": pages[0],
    "Climate-smart rice": pages[1],
    "Technology": pages[2],
    "Farm simulator": pages[3],
    "Carbon economics": pages[4],
    "Digital MRV": pages[5],
    "Policy / FPO": pages[6],
    "Insights": pages[7],
    "About": pages[8],
    "Partner with us": pages[9],
}

set_page_routes({"technology": pages[2], "simulator": pages[3]})

if selected_page is not None:
    st.switch_page(page_lookup[selected_page])

st.markdown("""
<style>
/* Compact branded navigation row */
div.st-key-site_nav button {
    border-radius: 12px;
    font-weight: 800;
    letter-spacing: .04em;
}
@media (max-width: 700px) {
    div.st-key-site_nav button {
        width: 100%;
    }
}

/* LIVE STREAMLIT THEME: slow, visible rice-field ambience on every route. */
@keyframes c4n-field-drift {
  0% { background-position: 0 0, 46% 18%; }
  50% { background-position: 0 0, 52% 55%; }
  100% { background-position: 0 0, 58% 90%; }
}
.stApp {
  background-image:
    linear-gradient(180deg, rgba(5,17,12,.94) 0%, rgba(5,17,12,.84) 46%, rgba(5,17,12,.96) 100%),
    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2200&q=85") !important;
  background-size: auto, cover !important;
  background-position: 0 0, 48% 0 !important;
  background-attachment: fixed, fixed !important;
  animation: c4n-field-drift 34s ease-in-out infinite alternate !important;
}
[data-testid="stAppViewContainer"] {
  background: transparent !important;
}
[data-testid="stHeader"] {
  background: rgba(5,17,12,.72) !important;
  backdrop-filter: blur(18px) !important;
  border-bottom: 1px solid rgba(182,239,117,.16) !important;
}
.block-container {
  position: relative;
}
.hero {
  border-color: rgba(182,239,117,.42) !important;
  box-shadow: 0 24px 90px rgba(0,0,0,.34), inset 0 0 0 1px rgba(255,255,255,.025) !important;
  background-image:
    linear-gradient(100deg, rgba(4,17,11,.97) 0%, rgba(4,17,11,.91) 52%, rgba(4,17,11,.60) 100%),
    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2000&q=90") !important;
  background-size: cover !important;
  background-position: center 45% !important;
}
.hero h1, .section h2, .band h2 {
  text-shadow: 0 2px 28px rgba(0,0,0,.28);
}
.eyebrow, .num {
  color: #c8f58a !important;
}
.card, .tile, .metric-card, .glass {
  background: linear-gradient(145deg, rgba(17,43,31,.96), rgba(7,24,17,.94)) !important;
  border-color: rgba(182,239,117,.24) !important;
  box-shadow: 0 12px 36px rgba(0,0,0,.22) !important;
  transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease !important;
}
.card:hover, .tile:hover, .metric-card:hover {
  transform: translateY(-5px) !important;
  border-color: rgba(200,245,138,.72) !important;
  box-shadow: 0 18px 42px rgba(0,0,0,.3) !important;
}
.section-copy, .muted, .tile p, .hero p {
  color: #d0e0d5 !important;
}
div.st-key-site_nav button {
  border: 1px solid rgba(200,245,138,.36) !important;
  background: rgba(14,38,26,.94) !important;
  color: #edf7f2 !important;
}
@media (prefers-reduced-motion: reduce) {
  .stApp { animation: none !important; }
  *, *::before, *::after { transition-duration: .01ms !important; }
}
</style>
""", unsafe_allow_html=True)

current_page.run()
