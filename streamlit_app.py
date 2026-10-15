from pathlib import Path

import streamlit as st

from app.site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology, set_page_routes


APP_DIR = Path(__file__).resolve().parent
DARK_LOGO = str(APP_DIR / "assets" / "logo-dark.svg")
LIGHT_LOGO = str(APP_DIR / "assets" / "logo-light.svg")
DARK_FAVICON = str(APP_DIR / "assets" / "favicon-dark.svg")
LIGHT_FAVICON = str(APP_DIR / "assets" / "favicon-light.svg")

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
