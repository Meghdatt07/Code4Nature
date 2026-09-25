from pathlib import Path

import streamlit as st

from app.intro import render_intro
from app.site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology


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
render_intro()

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

/* Hide Streamlit's automatic heading anchor/link icon. */
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
</style>
""", unsafe_allow_html=True)

current_page.run()
