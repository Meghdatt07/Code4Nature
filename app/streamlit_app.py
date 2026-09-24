import streamlit as st
from site_pages import about, carbon, climate_smart_rice, contact, home, insights, mrv, policy, simulator, technology

st.set_page_config(page_title="Asterisk Climos | Code4Nature", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>html,body,[data-testid="stAppViewContainer"],.stApp{background:#07120f!important;color:#edf7f2!important}[data-testid="stHeader"]{background:rgba(7,18,15,.88)!important}[data-testid="stSidebar"]{display:none!important}.block-container{max-width:1400px!important}
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
st.navigation(pages,position="top").run()
