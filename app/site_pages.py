import re
import streamlit as st
import streamlit.components.v1 as components

from pathlib import Path
import base64

from app.dashboard import init_state, render_economics, render_market, render_mrv, render_policy, render_farm_simulator

# Native Streamlit page objects used by homepage page links.
_PAGE_ROUTES = {}

def set_page_routes(routes):
    global _PAGE_ROUTES
    _PAGE_ROUTES = routes


def inject_site_css():
    st.markdown("""<style>
:root{
  --ink:#12251d;--forest:#0a1d16;--forest-2:#10291f;--sage:#a9cfb2;
  --mint:#cfe5d3;--cream:#f4f0e6;--paper:#fffdf7;--line:rgba(18,37,29,.13);
  --muted:#607168;--accent:#91c9a0;--blue:#8db9c8;
}
.stApp{background:var(--cream)!important;color:var(--ink)!important}
[data-testid="stHeader"]{background:rgba(244,240,230,.82)!important;backdrop-filter:blur(18px);border-bottom:1px solid rgba(18,37,29,.08)}
[data-testid="stSidebar"]{display:none!important}
.block-container{max-width:1480px!important;padding:0 3rem 4rem!important}

/* quiet Streamlit chrome */
.stAppViewContainer .main{background:var(--cream)!important}
.stMarkdownContainer h1 a,.stMarkdownContainer h2 a,.stMarkdownContainer h3 a,
.stMarkdownContainer h4 a,.stMarkdownContainer h5 a,.stMarkdownContainer h6 a,
[data-testid="stHeading"] a,.stHeadingWithActionElements a,
[data-testid="stHeaderActionElements"],[data-testid="StyledLinkIconContainer"]{
  display:none!important;visibility:hidden!important;pointer-events:none!important
}

/* shared editorial system */
.site-head{
  display:flex;justify-content:space-between;align-items:center;min-height:82px;
  border-bottom:1px solid rgba(18,37,29,.10);padding:.35rem 0 .55rem;margin-bottom:0
}
.brand{display:flex;align-items:center;gap:.65rem;font-weight:900;letter-spacing:.08em}
.brand-logo{width:82px;height:82px;object-fit:contain;display:block}
.status{font-size:.58rem;letter-spacing:.14em;color:#557064}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#4ca66a;box-shadow:0 0 10px rgba(76,166,106,.75);margin-right:.4rem}
.eyebrow{
  color:#557c61;font-size:.64rem;letter-spacing:.20em;font-weight:900;text-transform:uppercase
}
.section{padding:6.2rem 0}
.section h2{
  font-size:clamp(2.8rem,6vw,6.6rem);line-height:.90;letter-spacing:-.065em;
  margin:.7rem 0 1.2rem;color:var(--ink);font-weight:900
}
.section h2 em{color:#477a58;font-style:normal}
.section-copy{color:var(--muted);line-height:1.85;max-width:820px;font-size:1rem}
.band{
  background:var(--forest);color:#edf6ef;border-radius:28px;border:1px solid rgba(145,201,160,.14);
  padding:5rem 4rem;margin:1.5rem 0
}
.band h2{font-size:clamp(2.5rem,5.5vw,5.4rem);line-height:.92;letter-spacing:-.06em;color:#edf6ef;margin:.7rem 0 1rem}
.band .section-copy{color:#a9beb0}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:2.3rem}
.tiles.four{grid-template-columns:repeat(4,1fr)}
.tile{
  position:relative;overflow:hidden;background:rgba(255,253,247,.78);border:1px solid var(--line);
  border-radius:24px;padding:1.6rem;min-height:210px;
  box-shadow:0 8px 40px rgba(24,45,33,.045);transition:transform .45s cubic-bezier(.2,.75,.2,1),box-shadow .45s,border-color .45s
}
.tile:after{
  content:"";position:absolute;inset:auto -35% -55% auto;width:180px;height:180px;border-radius:50%;
  background:radial-gradient(circle,rgba(111,164,123,.16),transparent 68%);pointer-events:none
}
.tile:hover{transform:translateY(-8px);box-shadow:0 22px 60px rgba(24,45,33,.10);border-color:rgba(71,122,88,.30)}
.tile h3{margin:.8rem 0 .45rem;color:var(--ink);font-size:1.38rem;letter-spacing:-.025em}
.tile p{margin:0;color:#66776d;line-height:1.72;font-size:.90rem}
.num{color:#5b7f65;font-size:.64rem;font-weight:900;letter-spacing:.16em}
.muted{color:#697a70}
.footer-note{border-top:1px solid rgba(18,37,29,.13);padding-top:1.25rem;color:#718177;font-size:.72rem;line-height:1.65}

/* immersive homepage */
.c4n-experience{margin:0 -3rem -4rem;overflow:hidden;background:var(--cream);color:var(--ink)}
.c4n-experience .wrap{width:min(1240px,calc(100% - 56px));margin:0 auto}
.c4n-hero{
  min-height:calc(100vh - 42px);position:relative;overflow:hidden;display:flex;align-items:flex-end;
  background:#07150f;color:#f5f8f2
}
.c4n-hero .hero-scene{position:absolute;inset:0;width:100%;height:100%}
.c4n-hero .scene-glow{position:absolute;inset:0;background:
  radial-gradient(circle at 74% 18%,rgba(206,222,171,.22),transparent 13%),
  linear-gradient(180deg,rgba(4,15,10,.18),rgba(4,15,10,.28) 35%,rgba(4,15,10,.90) 100%),
  linear-gradient(90deg,rgba(4,15,10,.72),transparent 68%)
}
.c4n-hero .sun{animation:c4nFloat 8s ease-in-out infinite;transform-origin:center}
.c4n-hero .wind{animation:c4nWind 9s ease-in-out infinite}
.c4n-hero .scan{animation:c4nScan 5s linear infinite}
.c4n-hero .grain{opacity:.16;mix-blend-mode:screen}
@keyframes c4nFloat{0%,100%{transform:translateY(0) scale(1);opacity:.85}50%{transform:translateY(-7px) scale(1.035);opacity:1}}
@keyframes c4nWind{0%,100%{transform:translateX(-20px);opacity:.10}50%{transform:translateX(22px);opacity:.36}}
@keyframes c4nScan{0%{transform:translateX(-18%);opacity:0}18%{opacity:.45}80%{opacity:.28}100%{transform:translateX(118%);opacity:0}}
.c4n-hero .hero-copy{position:relative;z-index:3;padding-bottom:3.2rem;width:100%}
.c4n-hero .micro{
  display:flex;justify-content:space-between;gap:1rem;align-items:center;margin-bottom:1.4rem;
  color:#b6cfbb;font-size:.58rem;letter-spacing:.17em;font-weight:900;text-transform:uppercase
}
.c4n-hero h1{
  max-width:1120px;margin:0;font-size:clamp(4rem,9.3vw,10.6rem);line-height:.83;letter-spacing:-.072em;font-weight:900;
  color:#fbfcf8
}
.c4n-hero h1 span{display:block;color:#a5d3ae}
.c4n-hero .lede{max-width:680px;margin:1.6rem 0 2.2rem;color:#c9d9cc;font-size:1rem;line-height:1.75}
.hero-pills{display:flex;gap:.7rem;flex-wrap:wrap}
.hero-pill{
  border:1px solid rgba(228,243,229,.16);background:rgba(5,19,13,.42);backdrop-filter:blur(12px);
  border-radius:999px;padding:.7rem .85rem;color:#d7e5d8;font-size:.68rem;letter-spacing:.06em
}
.hero-radar{
  position:absolute;right:10%;top:18%;width:190px;height:190px;border:1px solid rgba(165,211,174,.28);
  border-radius:50%;z-index:2;box-shadow:0 0 0 36px rgba(165,211,174,.035),0 0 0 74px rgba(165,211,174,.022);
  animation:c4nRadar 4s ease-out infinite
}
.hero-radar:before{content:"";position:absolute;left:50%;top:50%;width:1px;height:74px;background:#a5d3ae;transform-origin:bottom;animation:c4nRadarArm 3s linear infinite}
.hero-radar:after{
  content:"";position:absolute;left:50%;top:50%;width:11px;height:11px;transform:translate(-50%,-50%);
  border-radius:50%;background:#c6e8c9;box-shadow:0 0 0 8px rgba(198,232,201,.10),0 0 24px rgba(198,232,201,.32)
}
@keyframes c4nRadar{0%{transform:scale(.72);opacity:.8}75%,100%{transform:scale(1.08);opacity:0}}
@keyframes c4nRadarArm{to{transform:rotate(360deg)}}
.hero-readout{
  position:absolute;right:4.5%;bottom:10%;z-index:3;padding:15px 16px;min-width:182px;
  border-radius:16px;border:1px solid rgba(196,229,201,.16);background:rgba(5,18,13,.56);backdrop-filter:blur(16px)
}
.hero-readout small{display:block;color:#91ad99;font-size:.55rem;letter-spacing:.14em;font-weight:900}
.hero-readout strong{display:block;color:#f4f9f1;margin-top:6px;font-size:1.28rem;letter-spacing:-.035em}
.hero-readout span{display:block;margin-top:4px;color:#a8bbaa;font-size:.63rem}
.c4n-scroll{
  position:absolute;right:2.2rem;bottom:2rem;z-index:4;color:#b8ccb9;font-size:.55rem;letter-spacing:.18em;
  text-transform:uppercase;writing-mode:vertical-rl;display:flex;gap:.6rem;align-items:center
}
.c4n-scroll:after{content:"";display:block;width:1px;height:54px;background:linear-gradient(#b8ccb9,transparent)}

.narrative{
  position:relative;padding:8rem 0;background:var(--paper);overflow:hidden
}
.narrative.dark{background:var(--forest);color:#edf6ef}
.narrative.olive{background:#dfe9de}
.story-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:7vw;align-items:center}
.story-grid.reverse{grid-template-columns:1.15fr .85fr}
.story-title{font-size:clamp(2.7rem,5.5vw,6rem);line-height:.90;letter-spacing:-.065em;font-weight:900;margin:.75rem 0 1.3rem;color:inherit}
.story-copy{max-width:640px;color:#63736a;font-size:1rem;line-height:1.85}
.dark .story-copy{color:#a9bdb0}
.story-index{font-size:.58rem;letter-spacing:.2em;font-weight:900;color:#63806b}
.orbit{
  position:relative;min-height:470px;border-radius:34px;overflow:hidden;background:#0c2118;
  border:1px solid rgba(18,37,29,.10);box-shadow:0 30px 90px rgba(24,45,33,.10)
}
.orbit .orbit-core{
  position:absolute;left:50%;top:50%;width:104px;height:104px;transform:translate(-50%,-50%);
  border-radius:50%;background:radial-gradient(circle at 35% 30%,#d9ecbf,#8dbd8c 38%,#477557 72%,#183b29);
  box-shadow:0 0 0 25px rgba(169,207,178,.08),0 0 0 70px rgba(169,207,178,.035)
}
.orbit .ring{position:absolute;left:50%;top:50%;border:1px solid rgba(169,207,178,.20);border-radius:50%;transform:translate(-50%,-50%);animation:c4nRing 7s linear infinite}
.orbit .r1{width:240px;height:240px}.orbit .r2{width:350px;height:350px;animation-duration:11s}.orbit .r3{width:470px;height:470px;animation-duration:17s}
.orbit .label{
  position:absolute;padding:9px 11px;border-radius:10px;background:rgba(6,20,14,.76);border:1px solid rgba(169,207,178,.15);
  color:#d7e6d8;font-size:.60rem;letter-spacing:.1em;font-weight:900
}
.orbit .l1{left:8%;top:18%}.orbit .l2{right:8%;top:28%}.orbit .l3{left:16%;bottom:14%}.orbit .l4{right:13%;bottom:20%}
@keyframes c4nRing{to{transform:translate(-50%,-50%) rotate(360deg)}}

.signal-line{
  width:1px;height:110px;background:linear-gradient(var(--accent),transparent);margin:0 auto;position:relative
}
.signal-line:before{content:"";position:absolute;top:0;left:50%;width:8px;height:8px;transform:translate(-50%,-4px);border-radius:50%;background:#76ad83;box-shadow:0 0 0 8px rgba(118,173,131,.09)}

.evidence-stage{background:#0a1d16;color:#edf6ef;padding:8rem 0}
.stage-grid{display:grid;grid-template-columns:.74fr 1.26fr;gap:4vw;align-items:center}
.metric-cinema{
  border:1px solid rgba(169,207,178,.13);border-radius:28px;padding:2rem;background:
  radial-gradient(circle at 78% 18%,rgba(141,185,200,.15),transparent 20%),rgba(255,255,255,.025)
}
.metric-cinema .eyebrow{color:#9bc4a4}
.metric-big{font-size:clamp(4rem,9vw,9rem);line-height:.8;letter-spacing:-.07em;font-weight:900;color:#f3f7ef}
.metric-big span{color:#91c9a0}
.metric-cinema p{max-width:430px;color:#9db2a5;line-height:1.7}
.data-rail{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:25px}
.data-chip{padding:17px;border:1px solid rgba(169,207,178,.10);border-radius:17px;background:rgba(255,255,255,.025)}
.data-chip strong{display:block;font-size:1.45rem;letter-spacing:-.035em;color:#eff7ef}
.data-chip small{display:block;margin-top:6px;color:#7f9589;line-height:1.4}

.tech-visual{
  min-height:470px;border-radius:34px;position:relative;overflow:hidden;background:#10271d;
  border:1px solid rgba(169,207,178,.12)
}
.tech-map{
  position:absolute;inset:12% 10%;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,1fr);gap:6px;transform:rotate(-6deg) scale(1.12)
}
.tech-map i{border-radius:6px;background:linear-gradient(145deg,rgba(169,207,178,.54),rgba(50,89,67,.23));border:1px solid rgba(255,255,255,.06)}
.tech-map i:nth-child(2n){background:linear-gradient(145deg,rgba(111,175,192,.55),rgba(44,79,88,.25))}
.tech-map i:nth-child(3n){background:linear-gradient(145deg,rgba(202,213,137,.50),rgba(76,100,66,.23))}
.tech-map i:nth-child(5n){background:linear-gradient(145deg,rgba(112,145,110,.52),rgba(48,76,57,.24))}
.tech-scan{position:absolute;left:6%;right:6%;height:2px;top:18%;background:#a5d3ae;box-shadow:0 0 22px rgba(165,211,174,.50);animation:c4nScanY 5s ease-in-out infinite}
@keyframes c4nScanY{0%,100%{transform:translateY(0);opacity:.15}50%{transform:translateY(290px);opacity:.65}}
.tech-pin{position:absolute;left:53%;top:53%;width:18px;height:18px;border-radius:50%;background:#cfe9ca;border:4px solid rgba(8,29,20,.78);box-shadow:0 0 0 9px rgba(207,233,202,.10),0 0 28px rgba(207,233,202,.30)}
.tech-label{position:absolute;left:16px;bottom:16px;padding:8px 10px;border-radius:10px;background:rgba(5,18,13,.80);border:1px solid rgba(169,207,178,.14);color:#d9e9dc;font-size:.58rem;font-weight:900;letter-spacing:.1em}

.c4n-values{background:#dfe9de;padding:8rem 0}
.value-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:5vw;align-items:end}
.value-list{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:2rem}
.value-card{padding:22px;background:rgba(255,253,247,.58);border:1px solid rgba(18,37,29,.10);border-radius:20px}
.value-card strong{display:block;font-size:2.8rem;line-height:1;letter-spacing:-.06em;color:#153224}
.value-card span{display:block;margin-top:7px;color:#566a5e;font-size:.78rem;line-height:1.45}
.value-card small{display:block;margin-top:8px;color:#7d8e84;font-size:.56rem;letter-spacing:.1em;text-transform:uppercase;font-weight:900}

.timeline{background:var(--paper);padding:8rem 0}
.timeline-list{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin-top:3.5rem;border-top:1px solid rgba(18,37,29,.12)}
.timeline-step{position:relative;padding:30px 18px 10px;border-right:1px solid rgba(18,37,29,.10);min-height:210px}
.timeline-step:last-child{border-right:0}
.timeline-dot{position:absolute;left:18px;top:-5px;width:10px;height:10px;border-radius:50%;background:#76ad83;box-shadow:0 0 0 7px rgba(118,173,131,.10)}
.timeline-step .num{color:#65806c}
.timeline-step h3{font-size:1.28rem;margin:25px 0 8px;letter-spacing:-.025em}
.timeline-step p{font-size:.80rem;line-height:1.65;color:#69786f;margin:0}

.final-cta{
  margin:0;background:#08160f;color:#f3f7ef;padding:8rem 0 7rem;position:relative;overflow:hidden
}
.final-cta:before{
  content:"";position:absolute;width:560px;height:560px;border-radius:50%;right:-170px;top:-220px;
  background:radial-gradient(circle,rgba(145,201,160,.18),transparent 68%)
}
.final-cta h2{max-width:1000px;font-size:clamp(3.4rem,7.3vw,8rem);line-height:.84;letter-spacing:-.07em;margin:.8rem 0 1.5rem;color:#f3f7ef}
.final-cta h2 span{color:#91c9a0}
.final-cta p{max-width:640px;color:#a6b9ac;line-height:1.8}
.final-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:2rem}

div.st-key-home_start button,div.st-key-home_tech button,div.st-key-home_mrv button{
  border-radius:999px!important;padding:.78rem 1.15rem!important;height:auto!important;min-height:0!important;font-weight:900!important;
}
div.st-key-home_start button{background:#91c9a0!important;border:1px solid #91c9a0!important;color:#08160f!important}
div.st-key-home_tech button,div.st-key-home_mrv button{background:transparent!important;border:1px solid rgba(243,247,239,.24)!important;color:#f3f7ef!important}
div.st-key-home_start button:hover{transform:translateY(-2px);box-shadow:0 12px 25px rgba(145,201,160,.18)!important}
div.st-key-home_tech button:hover,div.st-key-home_mrv button:hover{background:rgba(243,247,239,.06)!important}
div.st-key-home_start button p,div.st-key-home_tech button p,div.st-key-home_mrv button p{margin:0!important}

@media(max-width:1000px){
 .block-container{padding:0 1.2rem 3rem!important}
 .c4n-experience{margin:0 -1.2rem -3rem}
 .c4n-experience .wrap{width:min(100% - 32px,1240px)}
 .story-grid,.story-grid.reverse,.stage-grid,.value-grid{grid-template-columns:1fr}
 .tiles,.tiles.four{grid-template-columns:1fr 1fr}
 .timeline-list{grid-template-columns:1fr 1fr}
 .timeline-step{border-right:0;border-bottom:1px solid rgba(18,37,29,.10)}
}
@media(max-width:620px){
 .c4n-hero{min-height:760px}
 .c4n-hero h1{font-size:4.0rem}
 .hero-radar{width:130px;height:130px;right:7%;top:17%}
 .hero-readout{right:4%;bottom:13%;min-width:150px}
 .tiles,.tiles.four,.data-rail,.value-list,.timeline-list{grid-template-columns:1fr}
 .band{padding:3rem 1.4rem;border-radius:22px}
 .section,.narrative,.evidence-stage,.c4n-values,.timeline{padding:5rem 0}
 .story-title{font-size:3.2rem}
 .tech-visual,.orbit{min-height:340px}
}
</style>""", unsafe_allow_html=True)

def _logo_data():
    try:
        theme_type = st.context.theme.type
    except Exception:
        theme_type = "light"

    theme_dir = Path(__file__).resolve().parent / "assets"
    logo_path = theme_dir / ("logo_dark.svg" if theme_type == "dark" else "logo_light.svg")
    svg = logo_path.read_text(encoding="utf-8")
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + encoded

def shell():
    inject_site_css()
    logo = _logo_data()
    st.markdown(
        f'''<div class="site-head">
          <div class="brand"><img class="brand-logo" src="{logo}" alt="Asterisk Climos logo"></div>
          <div class="status"><span class="dot"></span>FIELD → SIGNAL → IMPACT</div>
        </div>''',
        unsafe_allow_html=True
    )

def frame(eyebrow,title,text):
    st.markdown(
        f'''<section class="section">
          <div class="eyebrow">{eyebrow}</div>
          <h2>{title}</h2>
          <div class="section-copy">{text}</div>
        </section>''',
        unsafe_allow_html=True
    )

def tiles(items, four=False):
    cls='tiles four' if four else 'tiles'
    html=f'<div class="{cls}">'
    for num,title,body in items:
        html+=f'<div class="tile"><div class="num">{num}</div><h3>{title}</h3><p>{body}</p></div>'
    html+='</div>'
    st.markdown(html,unsafe_allow_html=True)


def home():
    shell(); init_state()
    cells = "".join("<i></i>" for _ in range(35))
    st.markdown(f"""
    <div class="c4n-experience">
      <section class="c4n-hero">
        <svg class="hero-scene" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
          <defs>
            <linearGradient id="c4sky" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#0c2a20"/><stop offset="58%" stop-color="#214f38"/><stop offset="100%" stop-color="#0a2117"/></linearGradient>
            <linearGradient id="c4field" x1="0" x2="1" y1="0" y2="1"><stop offset="0%" stop-color="#4d835b"/><stop offset="48%" stop-color="#244f36"/><stop offset="100%" stop-color="#0e2a1c"/></linearGradient>
            <radialGradient id="c4sun"><stop offset="0%" stop-color="#f1e9bd" stop-opacity=".98"/><stop offset="32%" stop-color="#e7d98c" stop-opacity=".48"/><stop offset="100%" stop-color="#e7d98c" stop-opacity="0"/></radialGradient>
            <pattern id="c4rows" width="150" height="44" patternUnits="userSpaceOnUse" patternTransform="skewX(-22)">
              <path d="M0 3 H150 M0 30 H150" stroke="#b6d29c" stroke-opacity=".18" stroke-width="2"/>
              <path d="M20 0 V44 M86 0 V44" stroke="#b6d29c" stroke-opacity=".10"/>
            </pattern>
            <filter id="c4blur"><feGaussianBlur stdDeviation="30"/></filter>
          </defs>
          <rect width="1600" height="900" fill="url(#c4sky)"/>
          <circle class="sun" cx="1180" cy="170" r="170" fill="url(#c4sun)"/>
          <g class="wind" filter="url(#c4blur)" fill="none" stroke="#d3e5be" stroke-opacity=".16" stroke-width="5">
            <path d="M110 470 C430 370 620 520 890 420 S1310 310 1550 430"/>
            <path d="M40 530 C380 420 650 610 1010 480 S1390 410 1620 500"/>
          </g>
          <path d="M0 492 C260 420 540 470 770 400 C1040 319 1320 392 1600 310 V900 H0 Z" fill="url(#c4field)"/>
          <path d="M0 520 C330 430 550 500 800 430 C1090 347 1380 415 1600 345 V900 H0 Z" fill="url(#c4rows)" opacity=".95"/>
          <path d="M0 625 C260 548 530 610 800 545 C1040 484 1350 530 1600 462 V900 H0 Z" fill="url(#c4rows)" opacity=".55"/>
          <g opacity=".28" stroke="#e6f0d8" stroke-width="2"><path d="M0 705 C290 610 520 735 820 650 S1330 600 1600 555"/><path d="M0 770 C300 680 560 790 850 725 S1320 690 1600 650"/></g>
          <g class="grain"><circle cx="90" cy="160" r="2" fill="#fff"/><circle cx="270" cy="240" r="2" fill="#fff"/><circle cx="470" cy="130" r="2" fill="#fff"/><circle cx="740" cy="200" r="2" fill="#fff"/><circle cx="970" cy="100" r="2" fill="#fff"/><circle cx="1360" cy="250" r="2" fill="#fff"/></g>
          <g class="scan"><rect x="-120" y="115" width="3" height="670" fill="#c5e8c8" opacity=".34"/></g>
        </svg>
        <div class="scene-glow"></div>
        <div class="wrap">
          <div class="hero-radar"></div>
          <div class="hero-readout"><small>FIELD SIGNAL / PROTOTYPE</small><strong>31.8% wetness</strong><span>VV −17.60 dB · VH −23.80 dB</span></div>
          <div class="c4n-scroll">Scroll to enter the field</div>
          <div class="hero-copy">
            <div class="micro"><span>ASTERISK CLIMOS / CODE4NATURE</span><span>RICE · WATER · CLIMATE INTELLIGENCE</span></div>
            <h1>Every field<br><span>leaves a signal.</span></h1>
            <p class="lede">We connect what happens in the rice field with what a satellite can see—and turn that evidence into a transparent climate-impact story.</p>
            <div class="hero-pills"><span class="hero-pill">ALTERNATE WETTING & DRYING</span><span class="hero-pill">SENTINEL‑1 SAR</span><span class="hero-pill">DIGITAL MRV</span><span class="hero-pill">CARBON ECONOMICS</span></div>
          </div>
        </div>
      </section>

      <section class="narrative"><div class="wrap"><div class="story-grid">
        <div><div class="story-index">01 / THE FIELD</div><div class="story-title">Water changes<br>the story<br>beneath the crop.</div><div class="story-copy">Rice production depends on water, but prolonged flooding creates conditions that can increase methane emissions. Alternate Wetting and Drying introduces deliberate dry-down periods between irrigation events.</div></div>
        <div class="orbit"><div class="orbit-core"></div><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="label l1">FLOODED</div><div class="label l2">DRYING</div><div class="label l3">REWETTING</div><div class="label l4">OBSERVATION</div></div>
      </div></div></section>

      <div class="signal-line"></div>

      <section class="narrative olive"><div class="wrap"><div class="story-grid reverse">
        <div class="tech-visual"><div class="tech-map">{cells}</div><div class="tech-scan"></div><div class="tech-pin"></div><div class="tech-label">SENTINEL‑1 / RELATIVE WETNESS PROXY</div></div>
        <div><div class="story-index">02 / THE SIGNAL</div><div class="story-title">The field cannot always be visited.<br><em>So we observe from above.</em></div><div class="story-copy">Synthetic Aperture Radar (SAR) can repeatedly observe the land surface. In the prototype, Sentinel‑1 VV and VH backscatter are evidence inputs to a relative wetness layer—not a direct “moisture = −VV” conversion.</div>
          <div class="tiles" style="grid-template-columns:1fr 1fr;margin-top:2rem"><div class="tile"><div class="num">VV</div><h3>−17.60 dB</h3><p>Example prototype signal.</p></div><div class="tile"><div class="num">VH</div><h3>−23.80 dB</h3><p>Example prototype signal.</p></div></div>
        </div>
      </div></div></section>

      <section class="evidence-stage"><div class="wrap"><div class="stage-grid">
        <div><div class="eyebrow">03 / DIGITAL MRV</div><div class="story-title">Evidence should be<br><span style="color:#91c9a0">traceable.</span></div><div class="story-copy" style="color:#a9bdb0">A digital MRV layer ties a field boundary, farmer observations, satellite signals, timestamps and assumptions together. The goal is not a black-box number—it is an inspectable evidence chain.</div>
          <div class="data-rail"><div class="data-chip"><strong>FIELD</strong><small>Boundary + water observations</small></div><div class="data-chip"><strong>SAR</strong><small>VV + VH evidence</small></div><div class="data-chip"><strong>MODEL</strong><small>Methane → CO₂e scenario</small></div><div class="data-chip"><strong>MRV</strong><small>Provenance + verification path</small></div></div>
        </div>
        <div class="metric-cinema"><div class="eyebrow">FROM SIGNAL TO SCENARIO</div><div class="metric-big">31.8<span>%</span></div><p>Relative wetness in the prototype demonstration. It is an illustrative model input, not a direct field measurement or a carbon-credit verification result.</p><div class="data-rail"><div class="data-chip"><strong>WET</strong><small>Water regime state</small></div><div class="data-chip"><strong>AWD</strong><small>Practice context</small></div></div></div>
      </div></div></section>

      <section class="narrative"><div class="wrap"><div class="story-grid">
        <div><div class="story-index">04 / THE SCIENCE</div><div class="story-title">Measure the gas.<br>Calibrate the model.<br><em>Then scale the signal.</em></div><div class="story-copy">Satellite observations and models can support monitoring at scale, while chambers and laboratory gas chromatography provide direct methane evidence for calibration and validation. Code4Nature keeps these layers conceptually distinct.</div></div>
        <div><div class="tiles" style="grid-template-columns:1fr;margin-top:0"><div class="tile"><div class="num">01 / FIELD MEASUREMENT</div><h3>Chamber sampling</h3><p>Capture gas from a defined plot at controlled intervals.</p></div><div class="tile"><div class="num">02 / LAB</div><h3>Gas chromatography</h3><p>Quantify methane concentration in collected samples.</p></div><div class="tile"><div class="num">03 / DIGITAL</div><h3>Calibration + validation</h3><p>Use measured evidence to test and improve remote-sensing and model assumptions.</p></div></div></div>
      </div></div></section>

      <section class="c4n-values"><div class="wrap"><div class="value-grid">
        <div><div class="story-index">05 / FROM IMPACT TO VALUE</div><div class="story-title">A climate outcome becomes useful when the economics are visible.</div><div class="story-copy">The platform can translate an illustrative methane-abatement scenario into CO₂e and carbon-value scenarios, while keeping farmer/FPO share and assumptions explicit.</div>
          <div class="value-list"><div class="value-card"><strong>28×</strong><span>Global-warming-potential factor used in the prototype conversion.</span><small>Illustrative model assumption</small></div><div class="value-card"><strong>65%</strong><span>Example farmer/FPO share in the current economics prototype.</span><small>Configurable scenario</small></div></div>
        </div>
        <div class="value-card" style="padding:34px;background:#123124;border-color:rgba(145,201,160,.12)"><div class="num" style="color:#9bc7a5">CARBON ECONOMICS</div><strong style="font-size:clamp(3.2rem,7vw,7rem);color:#eff7ee">$15–20</strong><span style="color:#b5c6b9">Example carbon-price range used for project scenarios; market prices vary and actual credit value depends on methodology, verification and market conditions.</span><small style="color:#8fa699">Scenario range · USD / tCO₂e</small></div>
      </div></div></section>

      <section class="timeline"><div class="wrap"><div class="eyebrow">06 / ONE CONTINUOUS STORY</div><div class="story-title">From the paddy field<br>to measurable impact.</div>
        <div class="timeline-list">
          <div class="timeline-step"><div class="timeline-dot"></div><div class="num">01 / PRACTICE</div><h3>AWD</h3><p>Controlled flooding and dry-down create the intervention context.</p></div>
          <div class="timeline-step"><div class="timeline-dot"></div><div class="num">02 / OBSERVE</div><h3>FIELD DATA</h3><p>Boundary, water level and crop-stage observations anchor the story.</p></div>
          <div class="timeline-step"><div class="timeline-dot"></div><div class="num">03 / SEE</div><h3>SAR</h3><p>VV/VH signals add repeatable Earth-observation evidence.</p></div>
          <div class="timeline-step"><div class="timeline-dot"></div><div class="num">04 / VERIFY</div><h3>MRV</h3><p>Measured and modelled evidence are connected with provenance.</p></div>
          <div class="timeline-step"><div class="timeline-dot"></div><div class="num">05 / VALUE</div><h3>CO₂e + CARBON</h3><p>Scenario outputs become transparent climate and economics indicators.</p></div>
        </div>
      </section>

      <section class="final-cta"><div class="wrap" style="position:relative;z-index:2"><div class="eyebrow" style="color:#9bc7a5">CODE4NATURE / NEXT STEP</div><h2>Make the field<br><span>measurable.</span></h2><p>Explore a rice-field scenario, inspect the technology stack, or open the Digital MRV workflow.</p></div></section>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns([1.1, 1.1, 1.1, 4.7])
    with cols[0]:
        if st.button("Start simulator →", key="home_start", type="primary"):
            st.switch_page(_PAGE_ROUTES["simulator"])
    with cols[1]:
        if st.button("Technology", key="home_tech"):
            st.switch_page(_PAGE_ROUTES["technology"])
    with cols[2]:
        if st.button("Digital MRV", key="home_mrv"):
            st.switch_page(_PAGE_ROUTES.get("mrv", _PAGE_ROUTES["technology"]))
    st.markdown('<div style="margin-top:1.5rem;padding:0 0 1rem;color:#6f7f76;font-size:.68rem;line-height:1.65">Prototype demonstration only. Water states, wetness values, methane reductions, CO₂e, carbon quantities, prices and financial outcomes are illustrative unless independently measured and verified.</div>', unsafe_allow_html=True)

def climate_smart_rice():
    shell()
    frame("CLIMATE-SMART RICE","The farming practice is the climate intervention.","Alternate Wetting and Drying (AWD) introduces controlled dry-down periods between irrigations. The prototype focuses on making that field process observable and explainable.")
    tiles([("01","WET","Flooded state and irrigation event."),("02","DRYING","Controlled drawdown toward the target threshold."),("03","REWET","Reflood when the field reaches the operating threshold.")])
    st.markdown('<div class="band"><div class="eyebrow">FARMER-FIRST</div><h2>Make the field measurable.</h2><div class="section-copy">Farmers supply the practice, FPOs help aggregate and coordinate, and the MRV layer organises evidence for the project team.</div></div>',unsafe_allow_html=True)

def technology():
    shell()
    frame("OUR TECHNOLOGY","Soil to sky. One evidence chain.","Field observations, satellite signals, methane measurement and transparent modelling are combined into one workflow for rice climate projects.")
    tiles([
        ("01","GROUND DATA","Water level, irrigation and crop-stage observations."),
        ("02","SENTINEL-1","SAR-derived relative wetness proxy for field-scale monitoring."),
        ("03","MODELLING","Scenario equations connect water regime with methane and CO₂e outcomes."),
        ("04","PROVENANCE","Keep field, signal, sample, method, model and timestamp attached to every result."),
    ],True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">FIELD VALIDATION</div>
      <h2>Measure methane at the source.</h2>
      <div class="section-copy">
        Satellite and model outputs help us monitor fields at scale, but the project also needs
        direct greenhouse-gas measurements to establish what is happening at the field.
      </div>
      <div style="display:grid;grid-template-columns:1.15fr .85fr;gap:1rem;margin-top:2rem;align-items:stretch;">
        <div class="tile" style="min-height:0;">
          <div class="num">01 / CHAMBER SAMPLING</div>
          <h3>Capture the gas released by the rice field.</h3>
          <p>
            Closed chambers are placed over defined areas of a rice plot. Air samples are collected
            from the chamber headspace at set time intervals so the change in methane concentration
            can be measured.
          </p>
          <div class="num" style="margin-top:1.2rem;">02 / GAS CHROMATOGRAPHY</div>
          <h3>Turn a gas sample into a methane concentration.</h3>
          <p>
            Gas chromatography is the laboratory measurement layer used to quantify methane in the
            collected samples. The concentration measured across time is then used to estimate the
            methane flux from the field.
          </p>
          <div class="num" style="margin-top:1.2rem;">03 / DIGITAL MRV</div>
          <h3>Connect measured data with the digital evidence chain.</h3>
          <p>
            The resulting location-specific measurements can be used as field evidence for calibration,
            validation and transparent MRV alongside satellite observations and modelled scenarios.
          </p>
        </div>
        <div class="tile" style="padding:0;overflow:hidden;display:flex;flex-direction:column;">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/cd/GCMS_Instrument.jpg" alt="Gas chromatograph laboratory instrument" style="width:100%;height:320px;object-fit:contain;display:block;background:#06110d;" />
          <div style="padding:1.2rem;">
            <div class="num">GAS CHROMATOGRAPHY</div>
          </div>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">FIELD EVIDENCE / PRESS REPORT</div>
      <h2>Why this matters for Code4Nature.</h2>
      <div class="section-copy">
        A recent field report on rice methane highlighted the same measurement pathway that matters
        for our platform: reducing prolonged flooding through Alternate Wetting and Drying (AWD),
        measuring emissions from individual fields, and using laboratory gas chromatography to turn
        collected gas samples into location-specific methane data.
      </div>
      <div class="tiles" style="margin-top:2rem;">
        <div class="tile">
          <div class="num">AWD</div>
          <h3>Reduce prolonged flooding.</h3>
          <p>Periodic dry-downs interrupt the continuously flooded conditions that support methane-producing processes in rice soils.</p>
        </div>
        <div class="tile">
          <div class="num">MEASUREMENT</div>
          <h3>Use chambers + gas chromatography.</h3>
          <p>Field chambers capture gas samples; laboratory gas chromatography quantifies methane concentration so field flux can be estimated from the concentration change over time.</p>
        </div>
        <div class="tile">
          <div class="num">CARBON MRV</div>
          <h3>Build evidence that can be traced.</h3>
          <p>Real, verified, location-specific measurements strengthen the evidence chain needed to connect farm practice, modeled impact and carbon-credit MRV.</p>
        </div>
      </div>
      <div class="footer-note" style="margin-top:1.5rem;">
        Source context: supplied newspaper clipping about rice methane and farmer economics. The report describes AWD,
        field chambers and gas-chromatography analysis; project-specific measurements and verification are still required.
      </div>
    </section>
    """, unsafe_allow_html=True)


def simulator():
    shell(); init_state()
    frame("FARM SIMULATOR","Explore a rice-field scenario.","Use this page for scenario modelling. Map your farm and change assumptions without running satellite/MRV retrieval.")
    render_farm_simulator()

def carbon():
    st.set_page_config(page_title="Carbon Economics | Asterisk Climos", layout="wide"); shell(); init_state()
    frame("CARBON ECONOMICS","See the economics behind the scenario.","Change the area, abatement, carbon price and farmer/FPO share to inspect illustrative USD and INR outcomes.")
    render_market(); render_economics()

def mrv():
    shell(); init_state()
    frame("DIGITAL MRV","Field evidence and satellite intelligence.","Use this page for SAR retrieval, relative wetness, VV/VH backscatter and AWD telemetry/MRV evidence.")
    render_mrv()

def policy():
    shell()
    frame("POLICY / FPO","Connect implementation with the enablement layer.","Keep agricultural support, FPO aggregation and carbon-market methodology as distinct pieces of the project architecture.")
    render_policy()

def about():
    shell()

    frame(
        "ABOUT / OUR DIRECTION",
        "Building climate intelligence for rice, water and measurable impact.",
        "Asterisk Climos is a student-driven initiative at IIT Gandhinagar bringing together Earth Science, computer science, data science, remote sensing, machine learning and sustainability."
    )

    st.markdown("""
    <section class="section" style="padding-top:0;">
      <div class="eyebrow">OUR APPROACH</div>
      <h2>One problem. Multiple layers. One measurable impact.</h2>
      <div class="section-copy">
        Climate-smart rice requires more than a single technology. Our approach connects
        farmers and field observations with Earth observation, scientific measurement,
        data-driven modelling, digital MRV and transparent carbon economics.
        The aim is to create an evidence chain from what happens on the farm to
        measurable environmental and economic outcomes.
      </div>
    </section>

    <div class="tiles">
      <div class="tile">
        <div class="num">01 / FIELD</div>
        <h3>Farmers & implementation</h3>
        <p>Understand farming practices, water management and field conditions while keeping the needs of farmers and local partners at the centre.</p>
      </div>
      <div class="tile">
        <div class="num">02 / EARTH OBSERVATION</div>
        <h3>Satellite + GeoAI</h3>
        <p>Use radar and other Earth-observation data with data science and AI to understand field conditions at scale.</p>
      </div>
      <div class="tile">
        <div class="num">03 / SCIENCE</div>
        <h3>dMRV & measurement</h3>
        <p>Combine ground observations, field measurements, laboratory evidence and scientific models to make environmental outcomes traceable.</p>
      </div>
      <div class="tile">
        <div class="num">04 / VALUE</div>
        <h3>Carbon + farmer economics</h3>
        <p>Explore how credible methane reductions and climate-smart practices can connect to transparent carbon and farmer-value pathways.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">OUR IIT GANDHINAGAR MISSION</div>
      <h2>We are students. We can build, test and learn in the field.</h2>
      <div class="section-copy">
        Asterisk Climos is our student-driven attempt to apply science and technology
        to a practical climate problem. We are bringing together Earth Science,
        computer science, data science, remote sensing, machine learning and
        sustainability to build a working prototype—not just a presentation.
      </div>

      <div class="band" style="margin-top:2rem;">
        <div class="eyebrow">OUR MOTTO</div>
        <h2>Learn from the field.<br>Measure with science.<br>Build with technology.<br>Create impact.</h2>
        <div class="section-copy">
          As students of IIT Gandhinagar, our goal is to turn what we learn in classrooms
          and laboratories into useful tools for farmers, researchers, FPOs and climate
          practitioners. We start small, validate our assumptions, stay transparent
          about uncertainty, and improve the system with evidence.
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    tiles([
        ("01","OBSERVE","Understand the field before building the model."),
        ("02","MEASURE","Use Earth observation, field data and scientific methods."),
        ("03","MODEL","Turn observations into transparent, explainable scenarios."),
        ("04","ACT","Design tools that can support climate-smart decisions."),
        ("05","LEARN","Test, validate, document limitations and iterate."),
        ("06","IMPACT","Keep farmers, water, climate and measurable outcomes at the centre.")
    ], True)

    st.markdown("""
    <section class="section">
      <div class="eyebrow">OUR DIFFERENCE</div>
      <h2>Student-built does not mean science-light.</h2>
      <div class="section-copy">
        We are building an educational and research-oriented platform around open data,
        documented assumptions and reproducible methods. The project is designed to
        learn through experimentation, field validation and continuous improvement,
        while clearly separating prototype results from independently measured or
        verified outcomes.
      </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-note">Asterisk Climos is an independent IIT Gandhinagar student initiative focused on climate-smart rice, Earth observation, digital MRV and transparent carbon economics.</div>',
        unsafe_allow_html=True
    )

def insights():
    shell()
    frame(
        "INSIGHTS / CLIMATE INTELLIGENCE",
        "Rice. Water. Methane. Earth observation.",
        "Research, field evidence and emerging technologies shaping climate-smart rice and digital MRV. These insights are sourced from scientific literature and public institutions rather than company marketing."
    )

    articles = [
        ("01","Mar 19, 2026","India's water security is becoming an agricultural priority",
         "India has 18% of the world's population but only 4% of its water resources. Agriculture consumes roughly 80–90% of India's water, making efficient irrigation, groundwater monitoring and digital water intelligence central to climate-resilient rice.",
         "WORLD BANK / WATER FOR FOOD",
         "https://www.worldbank.org/en/brief/2026/03/19/how-india-is-addressing-its-water-needs"),
        ("02","2026","Optimized rice water management could cut global rice GHG emissions by 39.17%",
         "A global study using 15,458 field observations and machine-learning scenario simulations estimated that optimized water management could reduce rice greenhouse-gas emissions by 39.17% (340.46 Mt CO₂e) while increasing simulated yields by 3.55%. This is a modeled potential, not a guaranteed field outcome.",
         "RESEARCH / GLOBAL RICE",
         "https://agris.fao.org/search/en/providers/122413/records/699588e4e6c33ba92ad5780d"),
        ("03","2026","Smart irrigation is moving toward real-time field monitoring",
         "Recent Indian agricultural-engineering research is combining automated Alternate Wetting and Drying with sensors, controllers and digital monitoring. Reported water savings are experimental results, so field performance still depends on soil, climate, crop and irrigation conditions.",
         "FIELD STUDY / TECHNOLOGY",
         "https://agris.fao.org/search/en/providers/124598/records/69959e8ce6c33ba92ad640e7"),
        ("04","2026","Sentinel-1 can help us see rice-field water conditions through clouds",
         "Sentinel-1 radar provides repeat observations independent of daylight and can support monitoring of waterlogged ground, soil moisture and crop structure. For Asterisk Climos, SAR is an observation layer that complements—not replaces—field measurements and methane MRV.",
         "EARTH OBSERVATION / ESA",
         "https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/10_ways_Sentinel-1_data_lets_us_see_our_world"),
        ("05","Apr 2026","Indian rice research is pushing genetic and ecosystem-level innovation",
         "ICAR-CRRI's 61st Annual Rice Group Meetings highlighted genetic gain, pre-breeding and genome-editing research across rainfed and irrigated ecosystems. Climate-smart rice therefore extends beyond irrigation: varieties, agronomy and ecosystem adaptation matter too.",
         "INDIA / ICAR",
         "https://www.icar.gov.in/en/61st-annual-rice-group-meetings-inaugurated-icar-crri-cuttack"),
        ("06","Mar 2026","AI, drones and digital advisory are entering rice agriculture",
         "ICAR-CRRI has highlighted AI-based precision agriculture, drone applications, digital advisory through RiceXpert, methane-reduction research and nitrogen-efficient technologies. The direction is clear: farm decisions are increasingly supported by connected data and field intelligence.",
         "TECHNOLOGY / ICAR",
         "https://www.icar.gov.in/en/journalists-uttarakhand-visits-icar-crri-cuttack-understand-research-and-development-initiatives"),
        ("07","2026","AWD is powerful—but methane MRV needs more than a dry/wet label",
         "Field research shows that methane response to AWD can vary with timing, crop-residue management and other conditions, while nitrous oxide can also change. A credible MRV system therefore needs water regime, crop stage, residues, weather, nutrients and measured evidence—not a single proxy.",
         "MRV / FIELD EVIDENCE",
         "https://agris.fao.org/search/en/providers/122535/records/65df83da4c5aef494fe31e25"),
        ("08","Jun 11, 2026","Direct-seeded rice is part of India's water-efficiency transition",
         "A World Bank feature on Uttar Pradesh describes direct-seeded rice as a pathway being used to reduce water use, emissions and production costs. It reinforces a broader point for climate-smart rice: practice change has to work agronomically and economically at farm scale.",
         "INDIA / WATER EFFICIENCY",
         "https://www.worldbank.org/en/news/feature/2026/06/11/farming-is-building-a-stronger-rural-economy-in-uttar-pradesh-india"),
    ]

    cards = '<div class="insight-grid">'
    for num, date, title, body, source, url in articles:
        cards += f'''<article class="insight-card">
          <div class="insight-top">
            <div class="num">{num} / {date}</div>
            <div class="insight-source">{source}</div>
          </div>
          <div class="insight-content">
            <h3>{title}</h3>
            <p>{body}</p>
            <a class="insight-link" href="{url}" target="_blank" rel="noopener noreferrer">Read source →</a>
          </div>
        </article>'''
    cards += "</div>"

    st.markdown("""
    <style>
      .insight-grid{
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:1rem;
        margin:0 0 3rem;
      }
      .insight-card{
        overflow:hidden;
        border:1px solid rgba(126,226,177,.13);
        border-radius:20px;
        background:rgba(255,255,255,.035);
        transition:transform .18s ease,border-color .18s ease;
        min-height:300px;
        display:flex;
        flex-direction:column;
      }
      .insight-card:hover{
        transform:translateY(-3px);
        border-color:rgba(126,226,177,.38);
      }
      .insight-top{
        min-height:82px;
        padding:1.15rem 1.25rem;
        background:linear-gradient(135deg,rgba(126,226,177,.10),rgba(102,183,215,.07));
        border-bottom:1px solid rgba(126,226,177,.10);
        display:flex;
        justify-content:space-between;
        gap:1rem;
        align-items:flex-start;
      }
      .insight-source{
        color:#7d998c;
        font-size:.58rem;
        line-height:1.35;
        letter-spacing:.10em;
        font-weight:900;
        text-align:right;
        max-width:48%;
      }
      .insight-content{
        padding:1.25rem;
        display:flex;
        flex-direction:column;
        flex:1;
      }
      .insight-content h3{
        margin:.2rem 0 .7rem;
        color:#edf7f2;
        font-size:1.08rem;
        line-height:1.28;
      }
      .insight-content p{
        margin:0;
        color:#91aa9e;
        line-height:1.65;
        font-size:.86rem;
      }
      .insight-link{
        display:inline-block;
        margin-top:auto;
        padding-top:1.1rem;
        color:#7ee2b1;
        font-size:.78rem;
        font-weight:800;
        text-decoration:none;
      }
      .insight-link:hover{text-decoration:underline;}
      @media(max-width:1000px){.insight-grid{grid-template-columns:1fr 1fr;}}
      @media(max-width:620px){
        .insight-grid{grid-template-columns:1fr;}
        .insight-card{min-height:0;}
        .insight-top{min-height:74px;}
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(cards, unsafe_allow_html=True)

    st.markdown(
        '<div class="band"><div class="eyebrow">THE ASTERISK CLIMOS EVIDENCE CHAIN</div><h2>Practice → observation → measurement → MRV → value.</h2><div class="section-copy">Climate-smart rice is not one number. We connect farmer practice, Earth observation, field measurement, transparent modelling and carbon economics while keeping assumptions and uncertainty visible.</div></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="footer-note">Sources: World Bank, FAO AGRIS-indexed research, ESA Copernicus/Sentinel-1 and ICAR. All insight summaries are paraphrased from the linked sources. Modeled or experimental results are presented as study findings, not universal guarantees.</div>',
        unsafe_allow_html=True
    )

def contact():
    shell()
    frame(
        "PARTNER WITH US",
        "Build the evidence chain with us.",
        "Tell us who you are, what you want to contribute and how we can work together."
    )

    # Submit from the visitor's browser to FormSubmit's AJAX endpoint.
    # This avoids the Streamlit server acting as a bot-like relay and keeps
    # the recipient address out of the visible success message.
    partner_form_html = """
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Inter, Arial, sans-serif;
        background: transparent;
        color: #edf7f2;
      }
      .wrap {
        max-width: 900px;
        margin: 0 auto;
        padding: 8px 0 18px;
      }
      .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
      }
      .field { margin-bottom: 14px; }
      .full { grid-column: 1 / -1; }
      label {
        display: block;
        margin: 0 0 7px;
        font-size: 13px;
        font-weight: 700;
        color: #b9cec3;
      }
      input, select, textarea {
        width: 100%;
        border: 1px solid #29483c;
        border-radius: 10px;
        padding: 12px 13px;
        background: #0d1d18;
        color: #edf7f2;
        font: inherit;
        outline: none;
      }
      input:focus, select:focus, textarea:focus {
        border-color: #7ee2b1;
        box-shadow: 0 0 0 2px rgba(126,226,177,.12);
      }
      textarea { min-height: 150px; resize: vertical; }
      .other { display: none; }
      button {
        border: 0;
        border-radius: 11px;
        padding: 12px 18px;
        background: #7ee2b1;
        color: #07120f;
        font-weight: 900;
        cursor: pointer;
      }
      button:disabled { opacity: .65; cursor: wait; }
      .status {
        margin-top: 14px;
        padding: 12px 14px;
        border-radius: 10px;
        display: none;
        line-height: 1.5;
        font-size: 14px;
      }
      .success { display: block; background: rgba(72,227,154,.10); border: 1px solid rgba(72,227,154,.28); color: #bdf4d8; }
      .error { display: block; background: rgba(240,90,90,.10); border: 1px solid rgba(240,90,90,.30); color: #ffd0d0; }
      @media(max-width: 700px) {
        .grid { grid-template-columns: 1fr; }
        .full { grid-column: auto; }
      }
    </style>

    <div class="wrap">
      <form id="partner-form">
        <div class="grid">
          <div class="field">
            <label for="name">Name *</label>
            <input id="name" name="name" required placeholder="Your name">
          </div>

          <div class="field">
            <label for="email">Email *</label>
            <input id="email" name="email" type="email" required placeholder="you@example.com">
          </div>

          <div class="field">
            <label for="partner_type">I am interested in partnering as *</label>
            <select id="partner_type" name="partner_type" required>
              <option value="Farmers">Farmers</option>
              <option value="FPOs">FPOs</option>
              <option value="Research teams">Research teams</option>
              <option value="Carbon-market organisations">Carbon-market organisations</option>
              <option value="Technology partners">Technology partners</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="field other" id="other-wrap">
            <label for="other_type">Please define your partner type *</label>
            <input id="other_type" name="other_type" placeholder="e.g. NGO, investor, government body">
          </div>

          <div class="field">
            <label for="organisation">Organisation / Farm / Institution</label>
            <input id="organisation" name="organisation" placeholder="Optional">
          </div>

          <div class="field">
            <label for="phone">Phone / WhatsApp</label>
            <input id="phone" name="phone" placeholder="Optional">
          </div>

          <div class="field full">
            <label for="message">Tell us about the partnership *</label>
            <textarea id="message" name="message" required placeholder="What do you want to collaborate on, and how can we work together?"></textarea>
          </div>
        </div>

        <input type="hidden" name="_subject" value="New Code4Nature partnership request">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_replyto" id="_replyto">

        <button id="submit-btn" type="submit">Send partnership request</button>
        <div id="status" class="status"></div>
      </form>
    </div>

    <script>
      const form = document.getElementById("partner-form");
      const typeSelect = document.getElementById("partner_type");
      const otherWrap = document.getElementById("other-wrap");
      const otherInput = document.getElementById("other_type");
      const emailInput = document.getElementById("email");
      const replyTo = document.getElementById("_replyto");
      const button = document.getElementById("submit-btn");
      const status = document.getElementById("status");

      function toggleOther() {
        const isOther = typeSelect.value === "Other";
        otherWrap.style.display = isOther ? "block" : "none";
        otherInput.required = isOther;
      }

      typeSelect.addEventListener("change", toggleOther);
      toggleOther();

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        status.className = "status";
        status.textContent = "";
        replyTo.value = emailInput.value.trim();
        button.disabled = true;
        button.textContent = "Sending...";

        const data = Object.fromEntries(new FormData(form).entries());
        if (data.partner_type === "Other") {
          data.partner_type = data.other_type || "Other";
        }
        delete data.other_type;

        try {
          const response = await fetch("https://formsubmit.co/ajax/meghdatt712@gmail.com", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify(data)
          });

          let result = {};
          try {
            result = await response.json();
          } catch (_) {}

          if (!response.ok || result.success === false) {
            throw new Error(result.message || ("Email service returned HTTP " + response.status));
          }

          status.className = "status success";
          status.textContent = "Thanks! Your partnership request has been submitted.";
          form.reset();
          toggleOther();
        } catch (error) {
          status.className = "status error";
          status.textContent = "We couldn't submit the request right now. Please try again in a moment.";
          console.error("Partner form submission error:", error);
        } finally {
          button.disabled = false;
          button.textContent = "Send partnership request";
        }
      });
    </script>
    """

    components.html(partner_form_html, height=610, scrolling=False)

    st.markdown(
        '<div class="footer-note">Your information is used only to respond to the partnership request.</div>',
        unsafe_allow_html=True,
    )

