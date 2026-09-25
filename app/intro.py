import base64
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent

def scene_data_uri():
    try:
        return "data:image/jpeg;base64," + base64.b64encode(
            (REPO_ROOT / "assets" / "preloader-scene.jpg").read_bytes()
        ).decode("ascii")
    except Exception:
        return ""

INTRO_STYLE = """
<style>
.c4n-preloader-root{position:fixed!important;inset:0!important;z-index:999999!important;width:100vw!important;height:100vh!important;overflow:hidden!important;background:#06110d!important}
.c4n-preloader-root::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(2,10,7,.08),rgba(2,10,7,.28) 50%,rgba(2,10,7,.78)),radial-gradient(circle at 50% 44%,transparent 15%,rgba(2,10,7,.2) 64%,rgba(2,10,7,.58) 100%)}
.c4n-preloader-scene{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(1.03) contrast(1.04)}
.c4n-preloader-brand{position:absolute;left:34px;top:28px;z-index:5;color:#eff8f3;font-size:13px;font-weight:900;letter-spacing:.17em;text-shadow:0 2px 18px rgba(0,0,0,.52)}
.c4n-preloader-brand span{color:#7ee2b1}
.c4n-preloader-copy{position:absolute;left:50%;top:59%;transform:translate(-50%,-50%);z-index:5;width:min(900px,92vw);text-align:center;color:#f4faf6;text-shadow:0 3px 24px rgba(0,0,0,.65)}
.c4n-preloader-kicker{font-size:9px;font-weight:800;letter-spacing:.29em}
.c4n-preloader-title{margin-top:13px;font-size:clamp(21px,3.4vw,46px);font-weight:300;letter-spacing:.14em}
.c4n-preloader-brandline{margin-top:13px;font-size:clamp(44px,7.4vw,88px);font-weight:950;letter-spacing:-.06em;line-height:.9}
.c4n-preloader-brandline span{color:#7ee2b1}
.c4n-preloader-tagline{margin-top:13px;font-size:10px;letter-spacing:.15em;color:#d4e6dc}
.c4n-preloader-progress-wrap{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);z-index:6;width:min(560px,66vw);text-align:center}
.c4n-preloader-progress{height:3px;border-radius:999px;background:rgba(255,255,255,.16);overflow:hidden;box-shadow:0 0 18px rgba(126,226,177,.12)}
.c4n-preloader-progress span{display:block;width:0;height:100%;border-radius:999px;background:linear-gradient(90deg,#66b7d7,#7ee2b1,#9ae8c0);box-shadow:0 0 16px rgba(126,226,177,.42);animation:c4n-load 2s linear forwards}
.c4n-preloader-status{margin-top:8px;color:#e4efe9;font-size:9px;letter-spacing:.17em}
.c4n-preloader-enter{position:absolute;left:50%;bottom:74px;transform:translate(-50%,18px) scale(.98);z-index:7;opacity:0;pointer-events:none;animation:c4n-pop .35s cubic-bezier(.22,1,.36,1) 1s forwards}
.c4n-preloader-enter a{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-width:180px;padding:15px 25px;border-radius:999px;border:1px solid rgba(126,226,177,.44);background:rgba(5,22,15,.82);color:#f1f8f4;text-decoration:none;font-size:12px;font-weight:900;letter-spacing:.16em;box-shadow:0 12px 50px rgba(0,0,0,.34),0 0 30px rgba(126,226,177,.18);backdrop-filter:blur(12px);transition:.2s ease}
.c4n-preloader-enter a:hover{transform:translateY(-2px);background:#7ee2b1;color:#07120f;box-shadow:0 16px 56px rgba(126,226,177,.28)}
.c4n-preloader-enter a span{font-size:16px}
@keyframes c4n-load{to{width:100%}}
@keyframes c4n-pop{to{opacity:1;transform:translate(-50%,0) scale(1);pointer-events:auto}}
@media(max-width:700px){
  .c4n-preloader-brand{left:20px;top:20px;font-size:10px}
  .c4n-preloader-copy{top:57%}
  .c4n-preloader-title{font-size:18px;letter-spacing:.1em}
  .c4n-preloader-brandline{font-size:50px}
  .c4n-preloader-tagline{font-size:8px}
  .c4n-preloader-enter{bottom:70px}
  .c4n-preloader-progress-wrap{width:80vw;bottom:25px}
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

    scene = scene_data_uri()
    st.markdown(INTRO_STYLE, unsafe_allow_html=True)
    st.markdown(
        f'''
        <div class="c4n-preloader-root">
          <img class="c4n-preloader-scene" src="{scene}" alt="" aria-hidden="true">
          <div class="c4n-preloader-brand">CODE<span>4</span>NATURE</div>

          <div class="c4n-preloader-copy">
            <div class="c4n-preloader-kicker">CLIMATE INTELLIGENCE</div>
            <div class="c4n-preloader-title">WELCOME TO THE WORLD OF OPPORTUNITIES</div>
            <div class="c4n-preloader-brandline">ASTERISK <span>CLIMOS</span></div>
            <div class="c4n-preloader-tagline">MEASURE · OPTIMIZE · REDUCE · CREATE VALUE</div>
          </div>

          <div class="c4n-preloader-enter">
            <a href="?c4n_enter=1" aria-label="Enter Asterisk Climos">LET'S GO <span>↗</span></a>
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
