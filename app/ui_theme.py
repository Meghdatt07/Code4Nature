import streamlit as st

def inject_ui_theme():
    """Global Asterisk Climos visual system.

    This layer intentionally changes presentation only: typography, colour,
    spacing, navigation, cards, controls and responsive behaviour. Page copy
    and application logic remain untouched.
    """
    st.markdown(
        """
<style>
:root{
  --ac-ink:#241506;
  --ac-ink-2:#3b2817;
  --ac-cream:#f7f2e8;
  --ac-paper:#fffdf8;
  --ac-sand:#e9ddca;
  --ac-line:#d8c9b3;
  --ac-green:#27b968;
  --ac-green-dark:#15834a;
  --ac-green-soft:#dff3e7;
  --ac-moss:#78946f;
  --ac-blue:#78aeb5;
  --ac-orange:#d98b3d;
  --ac-muted:#766b5f;
  --ac-shadow:0 18px 50px rgba(45,29,12,.09);
}

/* -----------------------------------------------------------
   GLOBAL CANVAS
   ----------------------------------------------------------- */
html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.stApp{
  background:var(--ac-cream)!important;
  color:var(--ac-ink)!important;
}

[data-testid="stHeader"]{
  background:rgba(247,242,232,.88)!important;
  backdrop-filter:blur(16px)!important;
}

[data-testid="stSidebar"]{
  background:var(--ac-cream)!important;
  border-right:1px solid var(--ac-line)!important;
}

.block-container{
  max-width:1380px!important;
  padding:1.1rem 3.2rem 5rem!important;
}

p,li,span,div{
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

h1,h2,h3,h4,h5,h6{
  color:var(--ac-ink)!important;
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

/* -----------------------------------------------------------
   STREAMLIT TOP NAV — dark architectural pill
   ----------------------------------------------------------- */
div[data-testid="stNavigation"]{
  background:var(--ac-ink)!important;
  border:1px solid #3e2b19!important;
  border-radius:18px!important;
  box-shadow:0 12px 32px rgba(36,21,6,.14)!important;
  padding:.25rem!important;
  margin:.15rem 0 1.1rem!important;
}

div[data-testid="stNavigation"] a,
div[data-testid="stNavigation"] button{
  color:#eee6d8!important;
  border-radius:12px!important;
  font-size:.72rem!important;
  font-weight:750!important;
  letter-spacing:.01em!important;
}

div[data-testid="stNavigation"] a:hover,
div[data-testid="stNavigation"] button:hover{
  background:#3a2817!important;
  color:#fff!important;
}

div[data-testid="stNavigation"] a[aria-current="page"],
div[data-testid="stNavigation"] button[aria-current="page"]{
  background:var(--ac-green)!important;
  color:#092514!important;
  box-shadow:none!important;
}

/* Hide the redundant old Streamlit nav when an entrypoint uses a hidden menu. */
[data-testid="stSidebarNav"]{background:var(--ac-cream)!important}

/* -----------------------------------------------------------
   BRAND HEADER
   ----------------------------------------------------------- */
.site-head{
  min-height:76px!important;
  border-bottom:1px solid var(--ac-line)!important;
  padding:.2rem 0 .55rem!important;
  margin-bottom:1.5rem!important;
}

.brand-logo{
  width:64px!important;
  height:64px!important;
  object-fit:contain!important;
}

.status{
  color:var(--ac-moss)!important;
  font-size:.62rem!important;
  font-weight:800!important;
}

.dot{
  background:var(--ac-green)!important;
  box-shadow:0 0 12px rgba(39,185,104,.35)!important;
}

/* -----------------------------------------------------------
   HERO — warm editorial / climate-tech
   ----------------------------------------------------------- */
.hero{
  border:1px solid var(--ac-line)!important;
  border-radius:30px!important;
  padding:5.4rem 4.3rem 4.8rem!important;
  background:
    radial-gradient(circle at 78% 20%,rgba(39,185,104,.12),transparent 25%),
    radial-gradient(circle at 12% 95%,rgba(120,174,181,.13),transparent 27%),
    var(--ac-paper)!important;
  box-shadow:var(--ac-shadow)!important;
}

.eyebrow{
  color:var(--ac-green-dark)!important;
  font-size:.67rem!important;
  font-weight:900!important;
  letter-spacing:.16em!important;
}

.hero h1{
  color:var(--ac-ink)!important;
  font-size:clamp(3.5rem,7vw,7.3rem)!important;
  line-height:.88!important;
  letter-spacing:-.075em!important;
  max-width:1000px!important;
  margin:1.2rem 0 1.5rem!important;
}

.hero h1 span{
  color:var(--ac-green)!important;
}

.hero p{
  color:var(--ac-muted)!important;
  max-width:720px!important;
  font-size:1.03rem!important;
  line-height:1.75!important;
}

/* -----------------------------------------------------------
   SECTIONS / BANDS
   ----------------------------------------------------------- */
.section{
  padding:5rem 0!important;
}

.section h2,
.band h2{
  color:var(--ac-ink)!important;
  font-size:clamp(2.35rem,4.7vw,5.1rem)!important;
  line-height:.92!important;
  letter-spacing:-.065em!important;
}

.section-copy{
  color:var(--ac-muted)!important;
  max-width:790px!important;
  font-size:.98rem!important;
  line-height:1.8!important;
}

.band{
  background:var(--ac-ink)!important;
  border:0!important;
  border-radius:28px!important;
  margin:1.2rem 0!important;
  padding:4.8rem 3.2rem!important;
  box-shadow:0 20px 55px rgba(36,21,6,.12)!important;
}

.band h2{color:#f7f2e8!important}
.band .section-copy{color:#c9bdaa!important}

/* -----------------------------------------------------------
   CARDS — less SaaS, more editorial/product
   ----------------------------------------------------------- */
.card,.metric-card,.tile,.glass{
  background:var(--ac-paper)!important;
  border:1px solid var(--ac-line)!important;
  border-radius:20px!important;
  box-shadow:0 10px 30px rgba(45,29,12,.055)!important;
}

.card:hover,.tile:hover,.metric-card:hover{
  border-color:#b9a78e!important;
  transform:translateY(-2px);
  transition:transform .18s ease,border-color .18s ease;
}

.card b,.metric-card b,.tile h3{
  color:var(--ac-ink)!important;
}

.muted,.tile p,.card .muted{
  color:var(--ac-muted)!important;
}

.num{
  color:var(--ac-green-dark)!important;
  font-weight:900!important;
}

/* -----------------------------------------------------------
   BUTTONS
   ----------------------------------------------------------- */
div.stButton > button,
div[data-testid="stFormSubmitButton"] button{
  border-radius:12px!important;
  min-height:2.65rem!important;
  padding:.7rem 1rem!important;
  font-weight:850!important;
  border:1px solid var(--ac-line)!important;
  background:var(--ac-paper)!important;
  color:var(--ac-ink)!important;
  box-shadow:none!important;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] button:hover{
  border-color:var(--ac-green)!important;
  background:var(--ac-green-soft)!important;
  color:#0b351e!important;
}

div.stButton > button[kind="primary"],
div.stButton > button[data-testid="baseButton-primary"]{
  background:var(--ac-green)!important;
  border-color:var(--ac-green)!important;
  color:#082615!important;
}

div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="baseButton-primary"]:hover{
  background:#31c873!important;
}

/* -----------------------------------------------------------
   FORMS / INPUTS / SELECTS
   ----------------------------------------------------------- */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div,
[data-baseweb="multiselect"] > div{
  background:var(--ac-paper)!important;
  border-color:var(--ac-line)!important;
  border-radius:11px!important;
}

input,textarea{
  color:var(--ac-ink)!important;
}

label{
  color:var(--ac-ink-2)!important;
  font-weight:750!important;
}

/* -----------------------------------------------------------
   TABLES / DATAFRAMES / METRICS
   ----------------------------------------------------------- */
[data-testid="stMetric"]{
  background:var(--ac-paper)!important;
  border:1px solid var(--ac-line)!important;
  border-radius:18px!important;
  padding:1rem!important;
  box-shadow:0 10px 30px rgba(45,29,12,.05)!important;
}

[data-testid="stMetricLabel"]{
  color:var(--ac-muted)!important;
}

[data-testid="stMetricValue"]{
  color:var(--ac-ink)!important;
}

[data-testid="stDataFrame"]{
  border:1px solid var(--ac-line)!important;
  border-radius:16px!important;
  overflow:hidden!important;
}

/* -----------------------------------------------------------
   TABS / EXPANDERS / ALERTS
   ----------------------------------------------------------- */
button[data-baseweb="tab"]{
  color:var(--ac-muted)!important;
  font-weight:750!important;
}

button[data-baseweb="tab"][aria-selected="true"]{
  color:var(--ac-ink)!important;
}

div[data-baseweb="tab-highlight"]{
  background:var(--ac-green)!important;
}

[data-testid="stExpander"]{
  background:var(--ac-paper)!important;
  border:1px solid var(--ac-line)!important;
  border-radius:16px!important;
}

[data-testid="stAlert"]{
  border-radius:16px!important;
}

/* -----------------------------------------------------------
   INSIGHTS
   ----------------------------------------------------------- */
.insight-card{
  background:var(--ac-paper)!important;
  border-color:var(--ac-line)!important;
  border-radius:20px!important;
  box-shadow:0 12px 35px rgba(45,29,12,.06)!important;
}

.insight-card:hover{
  border-color:#b8a68d!important;
  box-shadow:0 18px 42px rgba(45,29,12,.09)!important;
}

.insight-top{
  background:linear-gradient(135deg,#edf6e9,#f8f0e4)!important;
  border-bottom-color:var(--ac-line)!important;
}

.insight-source{
  color:var(--ac-moss)!important;
}

.insight-content h3{
  color:var(--ac-ink)!important;
}

.insight-content p{
  color:var(--ac-muted)!important;
}

.insight-link{
  color:var(--ac-green-dark)!important;
}

/* -----------------------------------------------------------
   FOOTER / SMALL DETAILS
   ----------------------------------------------------------- */
.footer-note{
  border-top:1px solid var(--ac-line)!important;
  color:#87796a!important;
}

a{
  color:var(--ac-green-dark);
}

a:hover{
  color:#0c6e3b;
}

/* Keep Streamlit's automatic heading/link anchor icons invisible. */
.stMarkdownContainer h1 a,
.stMarkdownContainer h2 a,
.stMarkdownContainer h3 a,
.stMarkdownContainer h4 a,
.stMarkdownContainer h5 a,
.stMarkdownContainer h6 a,
[data-testid="stHeading"] a,
.stHeadingWithActionElements a,
[data-testid="stHeaderActionElements"],
[data-testid="StyledLinkIconContainer"]{
  display:none!important;
  visibility:hidden!important;
  pointer-events:none!important;
}

/* -----------------------------------------------------------
   RESPONSIVE
   ----------------------------------------------------------- */
@media(max-width:900px){
  .block-container{
    padding:1rem 1.15rem 3.5rem!important;
  }
  .hero{
    padding:3.4rem 1.6rem!important;
    border-radius:24px!important;
  }
  .hero h1{
    font-size:clamp(3rem,12vw,5rem)!important;
  }
  .band{
    padding:3.6rem 1.5rem!important;
    border-radius:22px!important;
  }
  .site-head{
    min-height:68px!important;
  }
  .brand-logo{
    width:56px!important;
    height:56px!important;
  }
}

@media(max-width:620px){
  .block-container{
    padding-left:.8rem!important;
    padding-right:.8rem!important;
  }
  .hero{
    padding:2.8rem 1.2rem!important;
  }
  .section{
    padding:3.5rem 0!important;
  }
  div[data-testid="stNavigation"]{
    border-radius:14px!important;
    overflow-x:auto!important;
  }
}
</style>
        """,
        unsafe_allow_html=True,
    )
