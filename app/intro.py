import base64
from pathlib import Path

import streamlit as st

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


def gif_data_uri(filename):
    try:
        data = base64.b64encode((ASSET_DIR / filename).read_bytes()).decode("ascii")
        return f"data:image/gif;base64,{data}"
    except Exception:
        return ""


INTRO_STYLE = """
<style>
html, body { overflow-x:hidden; }
.c4n-preloader-root{
  position:fixed!important;
  inset:0!important;
  z-index:999999!important;
  width:100vw!important;
  height:100vh!important;
  overflow:hidden!important;
  background:#06110d!important;
}
.c4n-preloader-root::after{
  content:"";
  position:absolute;
  inset:0;
  z-index:2;
  pointer-events:none;
  background:
    linear-gradient(180deg,rgba(2,9,6,.06),rgba(2,9,6,.20) 48%,rgba(2,9,6,.76) 100%),
    radial-gradient(circle at 50% 44%,transparent 18%,rgba(2,9,6,.12) 58%,rgba(2,9,6,.58) 100%);
}
.c4n-case{
  position:absolute;
  top:0;
  bottom:0;
  width:50%;
  overflow:hidden;
  background:#10281d;
}
.c4n-case-left{left:0;background:linear-gradient(180deg,#15392f,#07150f 74%)}
.c4n-case-right{right:0;background:linear-gradient(180deg,#1d4329,#0a1710 74%)}
.c4n-case img{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center;
  display:block;
  transform:scale(1.02);
  filter:saturate(1.08) contrast(1.03);
}
.c4n-case-left img{mix-blend-mode:screen;opacity:.93}
.c4n-case-right img{mix-blend-mode:screen;opacity:.92}
.c4n-case-left::before,
.c4n-case-right::before{
  content:"";
  position:absolute;
  inset:0;
  z-index:1;
  background:linear-gradient(180deg,rgba(3,13,9,.08),rgba(3,13,9,.12) 52%,rgba(3,13,9,.58));
}
.c4n-case-left::after{
  content:"";
  position:absolute;
  left:0;right:0;bottom:0;
  height:42%;
  z-index:1;
  background:linear-gradient(180deg,transparent,rgba(7,33,27,.34));
}
.c4n-case-right::after{
  content:"";
  position:absolute;
  left:0;right:0;bottom:0;
  height:42%;
  z-index:1;
  background:linear-gradient(180deg,transparent,rgba(25,45,20,.28));
}
.c4n-divider{
  position:absolute;
  left:50%;
  top:18%;
  bottom:18%;
  width:1px;
  transform:translateX(-50%);
  z-index:4;
  background:linear-gradient(180deg,transparent,rgba(238,250,242,.34),transparent);
}
.c4n-preloader-brand{
  position:absolute;
  left:34px;
  top:27px;
  z-index:5;
  color:#edf7f2;
  font-size:13px;
  font-weight:900;
  letter-spacing:.18em;
  text-shadow:0 2px 18px rgba(0,0,0,.56);
}
.c4n-preloader-brand span{color:#7ee2b1}
.c4n-case-label{
  position:absolute;
  top:34px;
  z-index:5;
  padding:10px 13px;
  border-radius:13px;
  border:1px solid rgba(255,255,255,.18);
  background:rgba(4,16,11,.45);
  backdrop-filter:blur(12px);
  color:#eef8f2;
  font-size:9px;
  font-weight:900;
  letter-spacing:.13em;
  text-shadow:0 1px 8px rgba(0,0,0,.5);
}
.c4n-label-left{left:28px}
.c4n-label-right{right:28px}
.c4n-preloader-copy{
  position:absolute;
  left:50%;
  top:57%;
  transform:translate(-50%,-50%);
  z-index:6;
  width:min(920px,92vw);
  text-align:center;
  color:#f4faf6;
  text-shadow:0 3px 25px rgba(0,0,0,.72);
}
.c4n-preloader-kicker{font-size:9px;font-weight:800;letter-spacing:.28em}
.c4n-preloader-title{
  margin-top:12px;
  font-size:clamp(20px,3.2vw,44px);
  font-weight:300;
  letter-spacing:.14em;
}
.c4n-preloader-brandline{
  margin-top:13px;
  font-size:clamp(46px,7.5vw,92px);
  font-weight:950;
  letter-spacing:-.06em;
  line-height:.9;
}
.c4n-preloader-brandline span{color:#7ee2b1}
.c4n-preloader-tagline{
  margin-top:13px;
  font-size:10px;
  letter-spacing:.15em;
  color:#d9e9df;
}
.c4n-preloader-progress-wrap{
  position:absolute;
  left:50%;
  bottom:27px;
  transform:translateX(-50%);
  z-index:8;
  width:min(560px,66vw);
  text-align:center;
}
.c4n-preloader-progress{
  height:3px;
  border-radius:999px;
  background:rgba(255,255,255,.16);
  overflow:hidden;
}
.c4n-preloader-progress span{
  display:block;
  width:0;
  height:100%;
  border-radius:999px;
  background:linear-gradient(90deg,#66b7d7,#7ee2b1,#a3ebc4);
  box-shadow:0 0 16px rgba(126,226,177,.45);
  animation:c4n-load 2s linear forwards;
}
.c4n-preloader-status{
  margin-top:8px;
  color:#e5f0e9;
  font-size:9px;
  letter-spacing:.17em;
}
.c4n-preloader-enter{
  position:absolute;
  left:50%;
  bottom:73px;
  transform:translate(-50%,14px) scale(.98);
  z-index:10;
  opacity:0;
  pointer-events:none;
  animation:c4n-pop .32s cubic-bezier(.22,1,.36,1) 1s forwards;
}
.c4n-preloader-enter form{margin:0}
.c4n-preloader-enter button{
  min-width:180px;
  padding:15px 25px;
  border-radius:999px;
  border:1px solid rgba(126,226,177,.44);
  background:rgba(5,22,15,.82);
  color:#f1f8f4;
  font-size:12px;
  font-weight:900;
  letter-spacing:.16em;
  box-shadow:0 12px 50px rgba(0,0,0,.34),0 0 30px rgba(126,226,177,.18);
  backdrop-filter:blur(12px);
  cursor:pointer;
}
.c4n-preloader-enter button:hover{
  background:#7ee2b1;
  color:#07120f;
  box-shadow:0 16px 56px rgba(126,226,177,.28);
}
.c4n-preloader-enter button span{font-size:16px;margin-left:7px}
@keyframes c4n-load{to{width:100%}}
@keyframes c4n-pop{
  to{
    opacity:1;
    transform:translate(-50%,0) scale(1);
    pointer-events:auto;
  }
}
@media(max-width:700px){
  .c4n-preloader-brand{left:18px;top:18px;font-size:10px}
  .c4n-case-label{top:58px;font-size:8px;padding:8px 9px}
  .c4n-label-left{left:14px}
  .c4n-label-right{right:14px}
  .c4n-preloader-copy{top:58%;width:95vw}
  .c4n-preloader-title{font-size:18px;letter-spacing:.09em}
  .c4n-preloader-brandline{font-size:48px}
  .c4n-preloader-tagline{font-size:7px;letter-spacing:.10em}
  .c4n-preloader-enter{bottom:67px}
  .c4n-preloader-progress-wrap{bottom:24px;width:82vw}
  .c4n-divider{top:16%;bottom:16%}
}
@media(prefers-reduced-motion:reduce){
  .c4n-preloader-progress span,.c4n-preloader-enter{animation:none!important}
  .c4n-preloader-progress span{width:100%}
  .c4n-preloader-enter{opacity:1;transform:translate(-50%,0) scale(1);pointer-events:auto}
}
</style>
"""


def render_intro():
    try:
        if st.query_params.get("c4n_enter") == "1":
            st.session_state["c4n_intro_complete"] = True
            st.query_params.clear()
    except Exception:
        pass

    if st.session_state.get("c4n_intro_complete"):
        return

    flooded = gif_data_uri("flooded-rice-plant.gif")
    awd = gif_data_uri("awd-rice-plant.gif")

    st.markdown(INTRO_STYLE, unsafe_allow_html=True)
    st.markdown(
        f'''
        <div class="c4n-preloader-root">
          <div class="c4n-case c4n-case-left">
            <img src="{flooded}" alt="" aria-hidden="true">
          </div>
          <div class="c4n-case c4n-case-right">
            <img src="{awd}" alt="" aria-hidden="true">
          </div>
          <div class="c4n-divider"></div>

          <div class="c4n-preloader-brand">CODE<span>4</span>NATURE</div>

          <div class="c4n-case-label c4n-label-left">FLOODED FIELD · HIGHER CH₄</div>
          <div class="c4n-case-label c4n-label-right">AWD / DRY-DOWN · LOWER CH₄</div>

          <div class="c4n-preloader-copy">
            <div class="c4n-preloader-kicker">CLIMATE INTELLIGENCE</div>
            <div class="c4n-preloader-title">WELCOME TO THE WORLD OF OPPORTUNITIES</div>
            <div class="c4n-preloader-brandline">ASTERISK <span>CLIMOS</span></div>
            <div class="c4n-preloader-tagline">MEASURE · OPTIMIZE · REDUCE · CREATE VALUE</div>
          </div>

          <div class="c4n-preloader-enter">
            <form method="get" action="" target="_self">
              <input type="hidden" name="c4n_enter" value="1">
              <button type="submit">LET'S GO <span>↗</span></button>
            </form>
          </div>

          <div class="c4n-preloader-progress-wrap">
            <div class="c4n-preloader-progress"><span></span></div>
            <div class="c4n-preloader-status">LOADING CLIMATE INTELLIGENCE · 0 → 100%</div>
          </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.stop()
