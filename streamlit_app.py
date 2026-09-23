import streamlit as st

from app.site_pages import (
    about,
    carbon,
    climate_smart_rice,
    contact,
    home,
    insights,
    mrv,
    policy,
    simulator,
    technology,
)

st.set_page_config(
    page_title="Code4Nature — Rice Climate Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pages = [
    st.Page(home, title="Home", icon=":material/home:", url_path="", default=True),
    st.Page(carbon, title="Rice carbon credits", icon=":material/eco:", url_path="rice-carbon-credits"),
    st.Page(climate_smart_rice, title="Climate-smart rice", icon=":material/water_drop:", url_path="climate-smart-rice"),
    st.Page(technology, title="Our technology", icon=":material/satellite_alt:", url_path="technology"),
    st.Page(simulator, title="Farm simulator", icon=":material/map:", url_path="simulator"),
    st.Page(mrv, title="Digital MRV", icon=":material/fact_check:", url_path="mrv"),
    st.Page(policy, title="Policy / FPO", icon=":material/account_balance:", url_path="policy"),
    st.Page(insights, title="Insights", icon=":material/auto_stories:", url_path="insights"),
    st.Page(about, title="About", icon=":material/info:", url_path="about"),
    st.Page(contact, title="Partner with us", icon=":material/handshake:", url_path="contact"),
]

pg = st.navigation(pages, position="top")
pg.run()
