import time
import streamlit as st

INTRO_STYLE = """
<style>
body { overflow-x:hidden; }
body:has(.c4n-intro-lock) .stApp { overflow:hidden; }
.c4n-intro-lock {
  position:fixed; inset:0; z-index:99999;
  background:
    radial-gradient(circle at 50% 38%, rgba(126,226,177,.11), transparent 30%),
    radial-gradient(circle at 50% 100%, rgba(102,183,215,.08), transparent 34%),
    #06110d;
  color:#edf7f2;
}
.c4n-intro-lock * { box-sizing:border-box; }
.c4n-intro-brand {
  position:absolute; left:30px; top:28px;
  font-size:13px; font-weight:900; letter-spacing:.16em;
}
.c4n-intro-brand span { color:#7ee2b1; }
.c4n-intro-scene {
  position:absolute; left:50%; top:43%;
  transform:translate(-50%,-50%);
  width:min(900px,88vw); height:min(390px,44vh);
  display:grid; grid-template-columns:1fr 1fr; gap:18px;
}
.c4n-intro-panel {
  position:relative; overflow:hidden; border-radius:28px;
  border:1px solid rgba(126,226,177,.16);
  background:linear-gradient(180deg,#123126,#07140f 78%);
  box-shadow:0 30px 80px rgba(0,0,0,.28);
}
.c4n-intro-panel.dry { background:linear-gradient(180deg,#17372b,#07140f 78%); }
.c4n-intro-tag {
  position:absolute; left:18px; top:18px; z-index:4;
  padding:7px 10px; border:1px solid rgba(126,226,177,.2);
  border-radius:999px; background:rgba(6,17,13,.72);
  color:#a9cabb; font-size:9px; font-weight:900; letter-spacing:.14em;
}
.c4n-intro-water { position:absolute; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,#66b7d7 18%,#66b7d7 82%,transparent);
  box-shadow:0 0 28px rgba(102,183,215,.2);
}
.c4n-intro-water.high { bottom:72px; }
.c4n-intro-water.low { bottom:106px; opacity:.5; }
.c4n-intro-soil { position:absolute; inset:auto 0 0; height:108px;
  background:linear-gradient(180deg,#19382b,#0a1711); }
.c4n-intro-roots { position:absolute; left:50%; bottom:38px; width:170px; height:125px;
  transform:translateX(-50%); opacity:.82; }
.c4n-intro-roots:before,.c4n-intro-roots:after { content:""; position:absolute; left:50%; bottom:0;
  width:2px; height:118px; background:#7ca591; border-radius:999px; transform-origin:bottom; }
.c4n-intro-roots:before { transform:rotate(24deg); }
.c4n-intro-roots:after { transform:rotate(-24deg); }
.c4n-intro-roots i { position:absolute; left:50%; bottom:18px; width:80px; height:2px;
  background:#6f977f; transform-origin:left center; }
.c4n-intro-roots i:nth-child(1){transform:rotate(55deg)}
.c4n-intro-roots i:nth-child(2){transform:rotate(125deg)}
.c4n-intro-roots i:nth-child(3){transform:translate(-50%,8px) rotate(90deg)}
.c4n-intro-plant { position:absolute; left:50%; bottom:94px; width:10px; height:182px;
  transform:translateX(-50%) scaleY(.08); transform-origin:bottom; opacity:0;
  background:linear-gradient(90deg,#4a8966,#a3d1b2,#467f5e); border-radius:999px;
  animation:c4n-plant-rise 2.65s cubic-bezier(.22,1,.36,1) .2s forwards; }
.c4n-intro-plant.tall { height:196px; }
.c4n-intro-plant b { position:absolute; width:76px; height:12px;
  border-radius:999px 999px 999px 0;
  background:linear-gradient(90deg,#447f5e,#9acbac); transform-origin:100% 50%; }
.c4n-intro-plant b:nth-child(1){top:24px;left:-67px;transform:rotate(-29deg)}
.c4n-intro-plant b:nth-child(2){top:59px;left:0;transform:rotate(28deg)}
.c4n-intro-plant b:nth-child(3){top:98px;left:-66px;transform:rotate(-24deg)}
.c4n-intro-plant b:nth-child(4){top:135px;left:1px;transform:rotate(28deg)}
.c4n-intro-bubbles { position:absolute; left:50%; bottom:102px; width:190px; height:230px;
  transform:translateX(-50%); }
.c4n-intro-bubbles i { position:absolute; bottom:0; width:9px; height:9px;
  border:1px solid rgba(132,183,207,.8); border-radius:50%;
  background:rgba(132,183,207,.08); animation:c4n-bubble-up 2.9s ease-in infinite; }
.c4n-intro-bubbles i:nth-child(1){left:12%;animation-delay:.2s}
.c4n-intro-bubbles i:nth-child(2){left:26%;animation-delay:.9s}
.c4n-intro-bubbles i:nth-child(3){left:40%;animation-delay:1.6s}
.c4n-intro-bubbles i:nth-child(4){left:52%;animation-delay:.55s}
.c4n-intro-bubbles i:nth-child(5){left:64%;animation-delay:1.25s}
.c4n-intro-bubbles i:nth-child(6){left:74%;animation-delay:1.85s}
.c4n-intro-bubbles i:nth-child(7){left:84%;animation-delay:.7s}
.c4n-intro-bubbles.few { opacity:.62; }
.c4n-intro-bubbles.few i:nth-child(n+3){display:none}
.c4n-plant-gif{
  position:absolute; left:50%; top:34px; bottom:46px; width:72%;
  transform:translateX(-50%); object-fit:cover; object-position:center;
  border-radius:18px; mix-blend-mode:normal; opacity:.96;
  filter:saturate(1.08) contrast(1.04);
  animation:c4n-plant-breathe 3.5s ease-in-out infinite;
}
.c4n-plant-gif.flooded{top:28px;bottom:36px}
.c4n-plant-gif.awd{top:28px;bottom:36px}
.c4n-intro-panel:after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(180deg,rgba(6,17,13,0.04),rgba(6,17,13,0.08) 62%,rgba(6,17,13,.42));
}
@keyframes c4n-plant-breathe{0%,100%{transform:translateX(-50%) scale(1)}50%{transform:translateX(-50%) scale(1.018)}}
.c4n-intro-ch4 { position:absolute; left:18px; bottom:17px;
  font-size:9px; font-weight:900; letter-spacing:.13em; color:#9cb9aa; }
.c4n-intro-copy { position:absolute; left:50%; bottom:62px; transform:translateX(-50%);
  width:min(720px,90vw); text-align:center; }
.c4n-intro-copy span { font-size:10px; font-weight:900; letter-spacing:.18em; color:#7ee2b1; }
.c4n-intro-copy h2 { margin:8px 0 0; font-size:clamp(22px,3vw,34px); letter-spacing:-.035em; }
.c4n-intro-copy p { margin:9px 0 0; color:#8ea79c; font-size:12px; }
.c4n-intro-progress { position:absolute; left:50%; bottom:29px; transform:translateX(-50%);
  width:min(700px,74vw); height:2px; background:rgba(255,255,255,.08); overflow:hidden; }
.c4n-intro-progress span { display:block; width:0; height:100%;
  background:linear-gradient(90deg,#7ee2b1,#66b7d7); animation:c4n-progress 4s linear forwards; }
.c4n-intro-status { position:absolute; right:28px; bottom:22px;
  color:#647e71; font-size:9px; letter-spacing:.12em; }
.c4n-intro-welcome {
  position:absolute; inset:0; display:grid; place-items:center;
  align-content:center; text-align:center; opacity:0; pointer-events:none;
  background:
    radial-gradient(circle at 50% 40%,rgba(126,226,177,.12),transparent 34%),
    radial-gradient(circle at 50% 100%,rgba(102,183,215,.08),transparent 30%),
    #06110d;
  transition:opacity .8s ease;
}
.c4n-intro-lock.welcome .c4n-intro-loading { opacity:0; pointer-events:none; }
.c4n-intro-lock.welcome .c4n-intro-welcome { opacity:1; pointer-events:auto; }
.c4n-intro-welcome-kicker { font-size:10px; font-weight:900; letter-spacing:.2em; color:#78988b; }
.c4n-intro-welcome-title { margin-top:18px; padding:0 20px;
  font-size:clamp(23px,4vw,46px); font-weight:300; letter-spacing:.16em; }
.c4n-intro-welcome-brand { margin-top:22px; font-size:clamp(44px,8vw,94px);
  font-weight:950; letter-spacing:-.055em; line-height:.9; }
.c4n-intro-welcome-brand span { color:#7ee2b1; }
.c4n-intro-welcome-sub { margin-top:18px; color:#7f998d; font-size:13px; }
.c4n-intro-enter-wrap { position:fixed; left:50%; bottom:54px;
  transform:translateX(-50%); z-index:100001; width:auto; }
.c4n-intro-enter-wrap [data-testid="stButton"] { width:auto; }
.c4n-intro-enter-wrap button {
  min-width:170px; padding:14px 22px; border-radius:999px!important;
  border:1px solid rgba(126,226,177,.25)!important;
  background:#7ee2b1!important; color:#07120f!important;
  font-size:12px!important; font-weight:900!important; letter-spacing:.14em!important;
  box-shadow:0 14px 40px rgba(126,226,177,.18)!important;
}
@keyframes c4n-plant-rise { 0%{opacity:0;transform:translateX(-50%) scaleY(.08)} 35%{opacity:1} 100%{opacity:1;transform:translateX(-50%) scaleY(1)} }
@keyframes c4n-bubble-up { 0%{transform:translateY(0) scale(.6);opacity:0} 15%{opacity:1} 100%{transform:translateY(-190px) translateX(10px) scale(1.12);opacity:0} }
@keyframes c4n-progress { to{width:100%} }
@media(max-width:700px){
  .c4n-intro-scene{width:94vw;height:275px;gap:10px}
  .c4n-intro-panel{border-radius:20px}
  .c4n-intro-brand{left:20px;top:20px}
  .c4n-intro-plant{height:140px;bottom:82px}.c4n-intro-plant.tall{height:152px}
  .c4n-intro-soil{height:88px}
  .c4n-intro-copy{bottom:57px;width:92vw}.c4n-intro-copy h2{font-size:19px}.c4n-intro-copy p{font-size:10px}
  .c4n-intro-status{display:none}
  .c4n-intro-welcome-title{font-size:18px;letter-spacing:.11em}
  .c4n-intro-welcome-brand{font-size:52px}
}
@media(prefers-reduced-motion:reduce){
  .c4n-intro-plant,.c4n-intro-bubbles i,.c4n-intro-progress span{animation:none!important}
  .c4n-intro-progress span{width:100%}
}
</style>
"""

def render_intro():
    # Use a query-param CTA so the "LET'S GO" control is a real browser link,
    # not a Streamlit widget that can get trapped behind a fixed overlay.
    try:
        if st.query_params.get("c4n_intro") == "enter":
            st.session_state["c4n_intro_complete"] = True
            st.session_state["c4n_intro_phase"] = "entered"
            st.query_params.clear()
    except Exception:
        pass

    if st.session_state.get("c4n_intro_complete"):
        return

    phase = st.session_state.get("c4n_intro_phase", "loading")

    if phase == "loading":
        st.markdown(INTRO_STYLE, unsafe_allow_html=True)
        st.markdown(
            '''<div class="c4n-intro-lock">
              <div class="c4n-intro-loading">
                <div class="c4n-intro-brand">CODE<span>4</span>NATURE</div>
                <div class="c4n-intro-scene">
                  <div class="c4n-intro-panel">
                    <div class="c4n-intro-tag">FLOODED SOIL</div>
                    <div class="c4n-intro-water high"></div>
                    <div class="c4n-intro-soil"></div>
                    <img class="c4n-plant-gif flooded" src="assets/flooded-rice-plant.gif" alt="" aria-hidden="true">
                    <div class="c4n-intro-ch4">MORE CH₄ POTENTIAL</div>
                  </div>
                  <div class="c4n-intro-panel dry">
                    <div class="c4n-intro-tag">AWD / DRY-DOWN</div>
                    <div class="c4n-intro-water low"></div>
                    <div class="c4n-intro-soil"></div>
                    <img class="c4n-plant-gif awd" src="assets/awd-rice-plant.gif" alt="" aria-hidden="true">
                    <div class="c4n-intro-ch4">LOWER CH₄ POTENTIAL</div>
                  </div>
                </div>
                <div class="c4n-intro-copy">
                  <span>FIELD INTELLIGENCE</span>
                  <h2>Water changes the story beneath the crop.</h2>
                  <p>Visualising the methane pathway from flooded conditions to controlled dry-down.</p>
                </div>
                <div class="c4n-intro-progress"><span></span></div>
                <div class="c4n-intro-status">CALIBRATING WATER · METHANE · EVIDENCE…</div>
              </div>
            </div>''',
            unsafe_allow_html=True,
        )
        time.sleep(4)
        st.session_state["c4n_intro_phase"] = "welcome"
        st.rerun()

    st.markdown(INTRO_STYLE, unsafe_allow_html=True)
    st.markdown(
        '''<div class="c4n-intro-lock welcome">
          <div class="c4n-intro-welcome">
            <div>
              <div class="c4n-intro-welcome-kicker">CODE4NATURE PRESENTS</div>
              <div class="c4n-intro-welcome-title">WELCOME TO THE WORLD OF OPPORTUNITIES</div>
              <div class="c4n-intro-welcome-brand">ASTERISK <span>CLIMOS</span></div>
              <div class="c4n-intro-welcome-sub">Climate intelligence for measurable rice-field impact.</div>
            </div>
          </div>
          <a class="c4n-intro-enter-link" href="?c4n_intro=enter" aria-label="Enter Asterisk Climos">
            LET'S GO <span>↗</span>
          </a>
        </div>''',
        unsafe_allow_html=True,
    )
    st.stop()
