import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# Streamlit Cloud may execute this file with /app as the script path.
# Add the repository root so the `app` package can always be imported reliably.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology, set_page_routes

FAVICON = REPO_ROOT / "assets" / "asterisk-climos-favicon-dark.svg"
st.set_page_config(page_title="Asterisk Climos | Code4Nature", page_icon=str(FAVICON), layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>html,body,[data-testid="stAppViewContainer"],.stApp{background:#07120f!important;color:#edf7f2!important}[data-testid="stHeader"]{background:rgba(7,18,15,.88)!important}[data-testid="stSidebar"]{display:none!important}.block-container{max-width:1400px!important}
/* Preloader removed: the deployed Streamlit entrypoint starts directly on the app. */
/* Hide Streamlit's automatic heading anchor/link icon. */
[data-testid="stHeaderActionElements"],
[data-testid="StyledLinkIconContainer"] { display:none !important; }
</style>""",unsafe_allow_html=True)

def branded_page(page_fn):
    """Re-apply the branded browser favicon when Streamlit activates a page."""
    def render_page():
        st.set_page_config(
            page_title="Asterisk Climos | Code4Nature",
            page_icon=FAVICON.read_text(encoding="utf-8"),
        )
        page_fn()
    return render_page


pages=[
st.Page(branded_page(home),title="Home",icon="",url_path="",default=True),
st.Page(branded_page(climate_smart_rice),title="Climate-smart rice",icon="",url_path="climate-smart-rice"),
st.Page(branded_page(technology),title="Technology",icon="",url_path="technology"),
st.Page(branded_page(simulator),title="Farm simulator",icon="",url_path="simulator"),
st.Page(branded_page(carbon),title="Carbon economics",icon="",url_path="carbon-economics"),
st.Page(branded_page(mrv),title="Digital MRV",icon="",url_path="mrv"),
st.Page(branded_page(policy),title="Policy / FPO",icon="",url_path="policy"),
st.Page(branded_page(insights),title="Insights",icon="",url_path="insights"),
st.Page(branded_page(about),title="About",icon="",url_path="about"),
st.Page(branded_page(contact),title="Partner with us",icon="",url_path="partner-with-us"),
]

# Give homepage buttons the actual Streamlit Page objects.
set_page_routes({
    "technology": pages[2],
    "simulator": pages[3],
})

st.navigation(pages,position="top").run()
