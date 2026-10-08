import sys
from pathlib import Path

import streamlit as st


# Streamlit Cloud may execute this file with /app as the script path.
# Add the repository root so the `app` package can always be imported reliably.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology, set_page_routes
from app.ui_theme import inject_ui_theme

st.set_page_config(page_title="Asterisk Climos | Code4Nature", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>html,body,[data-testid="stAppViewContainer"],.stApp{background:#07120f!important;color:#edf7f2!important}[data-testid="stHeader"]{background:rgba(7,18,15,.88)!important}[data-testid="stSidebar"]{display:none!important}.block-container{max-width:1400px!important}
/* Preloader removed: the deployed Streamlit entrypoint starts directly on the app. */
/* Hide Streamlit's automatic heading anchor/link icon. */
[data-testid="stHeaderActionElements"],
[data-testid="StyledLinkIconContainer"] { display:none !important; }
</style>""",unsafe_allow_html=True)

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

# Give homepage buttons the actual Streamlit Page objects.
set_page_routes({
    "technology": pages[2],
    "simulator": pages[3],
})

st.navigation(pages,position="top").run()

# Apply the final visual layer after the page renders so it can restyle
# every existing page component without changing page content or logic.
inject_ui_theme()
