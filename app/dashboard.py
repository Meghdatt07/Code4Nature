import math
from datetime import datetime, timedelta, timezone

import folium
import requests
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from folium.plugins import Draw
from streamlit_folium import st_folium

try:
    from .client import check_health, get_market_data, get_sar_data
except ImportError:
    from client import check_health, get_market_data, get_sar_data

DEFAULT_LAT = 23.2135
DEFAULT_LON = 72.6840
DEFAULT_HECTARES = 10.0
CH4_REDUCTION_PER_HA = 120.0
GWP_CH4 = 28.0
ERF_SCENARIO_PRICE_USD = 15.0
DEFAULT_VCM_PRICE_USD = 1.85

PRESETS = {
    "IITGN reference farm": (23.2135, 72.6840),
    "Nearby farm A": (23.2350, 72.7050),
    "Nearby farm B": (23.1850, 72.6500),
    "Nearby farm C": (23.2700, 72.7500),
}


def _inject_css():
    st.markdown(
        """
        <style>
        .stApp { background:#06110d; color:#e7f5ed; }
        [data-testid="stHeader"] { background:rgba(6,17,13,.85); }
        .block-container { max-width:1450px; padding-top:1.5rem; padding-bottom:3rem; }
        .top-nav { display:flex; justify-content:space-between; align-items:center; padding:.7rem 0 1.3rem; margin-bottom:.4rem; border-bottom:1px solid rgba(255,255,255,.06); }\n        .brand { font-weight:900; letter-spacing:.08em; font-size:1rem; }\n        .brand span { color:#6ee7b7; }\n        .brand small { margin-left:.7rem; color:#587267; font-size:.58rem; letter-spacing:.16em; }\n        .nav-status { color:#7e978c; font-size:.62rem; letter-spacing:.14em; }\n        .live-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:#34d399; box-shadow:0 0 12px #34d399; margin-right:.4rem; }\n        .hero {
            background:
              radial-gradient(circle at 12% 20%,rgba(16,185,129,.20),transparent 35%),
              radial-gradient(circle at 86% 10%,rgba(59,130,246,.18),transparent 32%),
              #06110d;
            border:1px solid rgba(110,231,183,.14);
            border-radius:28px; padding:3.5rem 2.8rem; margin-bottom:1.5rem;
        }
        .hero-kicker {
            display:inline-block; padding:.35rem .75rem;
            border:1px solid rgba(110,231,183,.2); border-radius:999px;
            color:#6ee7b7; font-size:.72rem; letter-spacing:.08em;
            font-weight:800; text-transform:uppercase;
        }
        .hero-title {
            font-size:clamp(2.5rem,6vw,5rem); line-height:.98; font-weight:900;
            letter-spacing:-.045em; margin:1rem 0;
        }
        .gradient {
            background:linear-gradient(90deg,#6ee7b7,#60a5fa);
            -webkit-background-clip:text; background-clip:text; color:transparent;
        }
        .hero-copy,.small-copy { color:#9fb5aa; line-height:1.7; }
        .flow-card,.info-card {
            background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.065);
            border-radius:18px; padding:1.2rem; height:100%;
        }
        .flow-num { color:#6ee7b7; font-weight:900; font-size:.85rem; }
        .section-kicker {
            color:#6ee7b7; font-size:.72rem; letter-spacing:.10em;
            font-weight:800; text-transform:uppercase;
        }
        .section-title { font-size:2rem; font-weight:900; letter-spacing:-.03em; margin-top:.2rem; }
        div[data-testid="stMetric"] {
            background:rgba(255,255,255,.035);
            border:1px solid rgba(255,255,255,.065);
            border-radius:18px; padding:1rem;
        }
        div[data-testid="stMetricLabel"] { color:#8ca99a; }
        .formula {
            background:rgba(0,0,0,.22); border-radius:14px; padding:1rem;
            color:#bcd0c5; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
            font-size:.85rem; line-height:1.8;
        }
        .footer { color:#789084; text-align:center; padding:2rem 0 0; font-size:.78rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def polygon_area_ha(points_latlon):
    if len(points_latlon) < 3:
        return 0.0
    radius_m = 6371008.8
    coords = [(math.radians(lat), math.radians(lon)) for lat, lon in points_latlon]
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    area = 0.0
    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i + 1]
        area += (lon2 - lon1) * (2.0 + math.sin(lat1) + math.sin(lat2))
    return abs(area) * radius_m * radius_m / 2.0 / 10000.0


def polygon_centroid(points_latlon):
    if not points_latlon:
        return DEFAULT_LAT, DEFAULT_LON
    return (
        sum(p[0] for p in points_latlon) / len(points_latlon),
        sum(p[1] for p in points_latlon) / len(points_latlon),
    )


def classify_awd(depth_cm):
    if depth_cm > 0:
        return "WET"
    if depth_cm >= -15:
        return "DRYING"
    return "REWETTING"


def init_state():
    defaults = {
        "lat": DEFAULT_LAT,
        "lon": DEFAULT_LON,
        "farm_polygon": None,
        "farm_area_ha": DEFAULT_HECTARES,
        "sar_data": None,
        "telemetry": None,
        "market_data": None,
        "current_depth": -7.0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state["telemetry"] is None:
        start = datetime.now(timezone.utc) - timedelta(days=29)
        depths = [5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7]
        rows = []
        for i, depth in enumerate(depths):
            ts = start + timedelta(days=i)
            rows.append(
                {
                    "timestamp": ts.strftime("%d %b"),
                    "AWD water depth (cm)": depth,
                    "Continuous flooding": 5.0,
                    "status": classify_awd(depth),
                }
            )
        st.session_state["telemetry"] = rows



def render_top_nav():
    st.markdown(
        """
        <div class="top-nav">
          <div class="brand"><span>CODE4</span>NATURE <small>CLIMATE INTELLIGENCE</small></div>
          <div class="nav-status"><span class="live-dot"></span> SYSTEM ONLINE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_hero():
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">CODE4NATURE / RICE CARBON INTELLIGENCE</div>
          <div class="hero-title">Turn every rice field into<br><span class="gradient">measurable climate value.</span></div>
          <div class="hero-copy" style="max-width:820px;font-size:1.08rem;">
            Code4Nature combines farm mapping, water-management intelligence, Sentinel-1 SAR evidence
            and transparent methane / CO2e modelling to connect field actions with
            farmer/FPO economics and carbon-market value.
          </div>
          <div class="small-copy" style="margin-top:1rem;">
            Demonstrator only: dashboard estimates are simulated/indicative unless
            supported by independently validated measurements and carbon-market verification.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    flow = [
        ("01","Farm telemetry","Pani Pipe / water-level evidence"),
        ("02","Sentinel-1 SAR","VV/VH → relative wetness proxy"),
        ("03","MRV engine","AWD state → methane → CO2e"),
        ("04","Economics","Carbon value → farmer + MRV share"),
    ]
    for col, (num, title, text) in zip(cols, flow):
        with col:
            st.markdown(
                f'<div class="flow-card"><div class="flow-num">{num}</div><div style="font-weight:800;font-size:1rem;margin-top:.35rem;">{title}</div><div class="small-copy" style="font-size:.8rem;margin-top:.35rem;">{text}</div></div>',
                unsafe_allow_html=True,
            )


def render_why():
    st.markdown('<div class="section-kicker">THE PROBLEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Why does this exist?</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">Continuous flooding creates anaerobic conditions that drive methane formation. AWD periodically lets the field dry before re-flooding. The practical challenge is proving that the water regime happened consistently and translating that evidence into a transparent MRV calculation.</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    cards = [
        ("💧","Water regime","Make WET, DRYING and REWETTING states visible instead of relying only on logbooks."),
        ("🛰️","Verification at scale","Use ground observations for calibration points and Sentinel-1 to extend observations across larger areas."),
        ("₹","Economic transparency","Change acreage, abatement, price and farmer share and immediately see USD and INR outcomes."),
    ]
    for col, (icon, title, body) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="info-card"><div style="font-size:1.8rem;">{icon}</div><div style="font-weight:800;font-size:1.1rem;margin-top:.5rem;">{title}</div><div class="small-copy" style="font-size:.83rem;margin-top:.4rem;">{body}</div></div>',
                unsafe_allow_html=True,
            )


def build_map():
    center = [st.session_state["lat"], st.session_state["lon"]]
    m = folium.Map(location=center, zoom_start=14, tiles="OpenStreetMap", control_scale=True)
    folium.Marker(
        center,
        tooltip="Selected farm point",
        popup=f"Lat {center[0]:.4f}, Lon {center[1]:.4f}",
        icon=folium.Icon(color="green", icon="leaf", prefix="fa"),
    ).add_to(m)
    polygon = st.session_state.get("farm_polygon")
    if polygon:
        folium.Polygon(
            locations=polygon,
            color="#34d399",
            weight=3,
            fill=True,
            fill_color="#34d399",
            fill_opacity=0.18,
            tooltip=f"Selected farm • {st.session_state['farm_area_ha']:.2f} ha",
        ).add_to(m)
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "circle": False,
            "circlemarker": False,
            "marker": False,
            "rectangle": True,
            "polygon": True,
        },
        edit_options={"edit": True, "remove": True},
    ).add_to(m)
    return m


def handle_map_result(map_data):
    if not map_data:
        return
    clicked = map_data.get("last_clicked")
    if clicked and clicked.get("lat") is not None and clicked.get("lng") is not None:
        st.session_state["lat"] = float(clicked["lat"])
        st.session_state["lon"] = float(clicked["lng"])
    drawing = map_data.get("last_active_drawing")
    if not drawing:
        return
    geometry = drawing.get("geometry", {})
    if geometry.get("type") != "Polygon":
        return
    coords = geometry.get("coordinates", [])
    if not coords:
        return
    ring = coords[0]
    polygon = [(float(pair[1]), float(pair[0])) for pair in ring]
    if len(polygon) < 3:
        return
    st.session_state["farm_polygon"] = polygon
    st.session_state["farm_area_ha"] = max(0.01, polygon_area_ha(polygon))
    st.session_state["lat"], st.session_state["lon"] = polygon_centroid(polygon)


def render_algorithmic_mrv_simulation():
    html = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box}body{margin:0;background:#0b1425;color:#e8edf7;font-family:Arial,sans-serif}
.wrap{padding:0 0 18px}.head{display:flex;justify-content:space-between;align-items:center;padding:4px 0 18px;border-bottom:1px solid #29354a}
.title{font-size:25px;font-weight:800}.sub{font-size:15px;color:#91a0b8;margin-top:6px}.btn{background:#2864e6;color:#fff;border:0;border-radius:14px;padding:15px 23px;font-size:16px;font-weight:800;cursor:pointer}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:38px;margin-top:28px}.card{background:#101b2f;border:1px solid #2b3850;border-radius:18px;padding:28px;position:relative}.card.awd{border-color:#0a8b72}.badge{position:absolute;right:0;top:0;background:#11b98b;color:#04131a;padding:8px 16px;border-radius:0 0 0 14px;font-size:12px;font-weight:900}
.card h3{font-size:14px;color:#c0c9d8;letter-spacing:.02em;margin:0 0 15px}.awd h3{color:#28d1a6}.chartbox{height:330px}
@media(max-width:850px){.grid{grid-template-columns:1fr}.head{gap:15px;align-items:flex-start}.btn{width:100%}}
</style></head><body><div class="wrap">
<div class="head"><div><div class="title">MRV Algorithmic Simulation</div><div class="sub">Verra VM0051 Compliance View</div></div><button id="play" class="btn">▶ Execute 30-Day Model</button></div>
<div class="grid">
<div class="card"><h3>≋ &nbsp; BASELINE CONTROL (CONTINUOUS)</h3><div class="chartbox"><canvas id="baseline"></canvas></div></div>
<div class="card awd"><div class="badge">CREDITS GENERATED</div><h3>⌁ &nbsp; AWD INTERVENTION</h3><div class="chartbox"><canvas id="awd"></canvas></div></div>
</div></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const days=Array.from({length:30},(_,i)=>"T+"+(i+1));
const continuous={water:Array(30).fill(5),methane:Array(30).fill(2.4)};
const awd={water:[5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7,-11,-15,5,4,2,0,-3,-7],methane:[2.4,2.2,1.8,1,0.4,.1,0,0,1.8,1.5,1,.5,.2,0,0,0,1.5,1.2,.8,.4,.1,0,0,0,1.2,.9,.5,.2,.1,0]};
Chart.defaults.font.family="Arial";Chart.defaults.color="#95a3ba";
const opts={responsive:true,maintainAspectRatio:false,animation:false,
plugins:{legend:{position:"top",labels:{usePointStyle:true,boxWidth:6,font:{size:11}}}},
scales:{x:{grid:{color:"rgba(255,255,255,.04)"}},y:{min:-20,max:10,title:{display:true,text:"Soil Water Level (cm)",color:"#718099"},grid:{color:c=>c.tick.value===0?"rgba(59,130,246,.55)":"rgba(255,255,255,.05)",lineWidth:c=>c.tick.value===0?2:1}},y1:{min:0,max:3,position:"right",title:{display:true,text:"CH4 Emissions (kg/ha/day)",color:"#718099"},grid:{drawOnChartArea:false}}}};
function make(id,data,mColor,fillWater){
return new Chart(document.getElementById(id),{type:"line",data:{labels:days,datasets:[
{label:"Water Depth (cm)",data:[...data.water],borderColor:"#3b82f6",backgroundColor:"rgba(59,130,246,.10)",borderWidth:2,yAxisID:"y",fill:true,tension:.35,pointRadius:0},
{label:"Methane (kg/ha/day)",data:[...data.methane],borderColor:mColor,backgroundColor:"transparent",borderWidth:2,borderDash:[4,4],yAxisID:"y1",tension:.35,pointRadius:0}]},options:opts})}
let b=make("baseline",continuous,"#ff3b61"), a=make("awd",awd,"#10d39b");
document.getElementById("play").onclick=()=>{b.data.datasets.forEach(d=>d.data=[]);a.data.datasets.forEach(d=>d.data=[]);b.update();a.update();let i=0,t=setInterval(()=>{if(i>=30){clearInterval(t);return}
b.data.datasets[0].data.push(continuous.water[i]);b.data.datasets[1].data.push(continuous.methane[i]);a.data.datasets[0].data.push(awd.water[i]);a.data.datasets[1].data.push(awd.methane[i]);b.update();a.update();i++},100)}
</script></body></html>"""
    components.html(html, height=455, scrolling=False)


def render_mrv():
    st.markdown('<div class="section-kicker">LIVE FARM / SAR LAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Move the farm. Draw the boundary. Query the satellite.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">Click the map to change the farm point, or use the polygon/rectangle tools to outline the farm. The drawn geometry becomes the calculator area and is passed as the SAR AOI when live credentials are available.</p>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.65, 1])
    with left:
        map_data = st_folium(
            build_map(),
            width=None,
            height=560,
            returned_objects=["last_clicked", "last_active_drawing"],
            key="farm_map",
        )
        handle_map_result(map_data)

    with right:
        preset = st.selectbox("Farm preset", list(PRESETS.keys()))
        if st.button("Use preset", use_container_width=True):
            lat, lon = PRESETS[preset]
            st.session_state["lat"] = lat
            st.session_state["lon"] = lon
            st.session_state["farm_polygon"] = None
            st.session_state["farm_area_ha"] = DEFAULT_HECTARES
            st.rerun()

        c1, c2 = st.columns(2)
        lat = c1.number_input("Latitude", -90.0, 90.0, float(st.session_state["lat"]), step=0.0001, format="%.4f")
        lon = c2.number_input("Longitude", -180.0, 180.0, float(st.session_state["lon"]), step=0.0001, format="%.4f")
        st.session_state["lat"] = lat
        st.session_state["lon"] = lon

        area = st.number_input("Farm area (hectares)", min_value=0.01, value=float(st.session_state["farm_area_ha"]), step=0.1, format="%.2f")
        st.session_state["farm_area_ha"] = area

        if st.button("Fetch SAR for selected area", type="primary", use_container_width=True):
            with st.spinner("Querying Sentinel-1..."):
                st.session_state["sar_data"] = get_sar_data(
                    st.session_state["lat"],
                    st.session_state["lon"],
                    polygon=st.session_state.get("farm_polygon"),
                )

        sar = st.session_state.get("sar_data")
        if sar:
            st.markdown("---")
            proxy = sar.get("moisture_proxy_percent")
            st.metric("Relative wetness", "—" if proxy is None else f"{float(proxy):.1f}%")
            x1, x2 = st.columns(2)
            vv, vh = sar.get("vv_mean_db"), sar.get("vh_mean_db")
            x1.metric("VV mean", "—" if vv is None else f"{float(vv):.2f} dB")
            x2.metric("VH mean", "—" if vh is None else f"{float(vh):.2f} dB")
            st.caption(f"Source: {sar.get('source','N/A')}")
            st.caption(sar.get("note",""))

            with st.expander("Details"):
                if vv is not None:
                    vv_value = float(vv)
                    wetness_calc = max(0.0, min(100.0, 50.0 + (vv_value + 15.0) * 7.0))
                    st.markdown(
                        "**Relative wetness:** the demonstrator converts VV backscatter into a relative wetness proxy using "
                        f"**clamp(50 + (VV + 15) × 7, 0, 100)** → "
                        f"**{wetness_calc:.1f}%** for VV = **{vv_value:.2f} dB**."
                    )
                if vh is not None:
                    st.markdown(
                        f"**VH mean:** {float(vh):.2f} dB — VH is the cross-polarized SAR backscatter signal and complements VV when interpreting vegetation and surface scattering."
                    )
                st.markdown(
                    "**SAR:** Synthetic Aperture Radar, an active radar system that measures returned microwave energy.  "
                    "**VV/VH:** radar polarization channels.  "
                    "**dB:** decibel scale used to express backscatter.  "
                    "**Relative wetness:** a model-derived indicator, not an absolute soil-moisture percentage."
                )
                st.caption(
                    "This calculation is performed after you trigger the SAR query. The displayed wetness value is a demonstrator proxy and requires field calibration before use as an absolute soil-moisture measurement."
                )
        
    k1, k2, k3, k4 = st.columns(4)
    depth = float(st.session_state.get("current_depth", -7.0))
    status = classify_awd(depth)
    ch4 = st.session_state["farm_area_ha"] * CH4_REDUCTION_PER_HA
    co2e = ch4 * GWP_CH4 / 1000.0
    k1.metric("Farm area", f"{st.session_state['farm_area_ha']:.2f} ha")
    k2.metric("AWD status", status)
    k3.metric("Potential CH4 reduction", f"{ch4:,.0f} kg/season")
    k4.metric("Potential CO2e", f"{co2e:,.2f} tCO2e/season")

    st.markdown("#### 30-day AWD telemetry simulator")
    t1, t2 = st.columns([3, 1])
    with t2:
        new_depth = st.slider("New water depth (cm)", -20.0, 8.0, float(st.session_state.get("current_depth",-7.0)), 0.5)
        st.session_state["current_depth"] = new_depth
        st.info(f"Current state: **{classify_awd(new_depth)}**")
        if st.button("Add telemetry reading", use_container_width=True):
            now = datetime.now()
            st.session_state["telemetry"].append(
                {
                    "timestamp": now.strftime("%d %b %H:%M"),
                    "AWD water depth (cm)": new_depth,
                    "Continuous flooding": 5.0,
                    "status": classify_awd(new_depth),
                }
            )
            st.session_state["telemetry"] = st.session_state["telemetry"][-30:]
            st.rerun()
    with t1:
        chart_df = pd.DataFrame(st.session_state["telemetry"]).set_index("timestamp")
        st.line_chart(chart_df[["Continuous flooding","AWD water depth (cm)"]], height=320)

    st.markdown('<div class="section-kicker" style="margin-top:3rem">ALGORITHMIC MRV SIMULATION</div>', unsafe_allow_html=True)
    render_algorithmic_mrv_simulation()




def render_farm_simulator():
    st.markdown('<div class="section-kicker">FARM SIMULATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">See your rice carbon-credit opportunity in seconds.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">Enter your farm land and crop. The Farm Simulator uses the same rice methane-abatement reference standard as Digital MRV so both pages produce the same CO2e opportunity for the same area.</p>',
        unsafe_allow_html=True,
    )

    area = st.number_input(
        "Farm land (hectares)",
        min_value=0.01,
        value=10.0,
        step=0.1,
        format="%.2f",
        key="simple_farm_area",
        help="Enter the total land area where the crop is grown.",
    )
    crop = st.selectbox(
        "Crop being grown",
        ["Rice", "Other crop"],
        key="simple_crop_type",
        help="The current methane-abatement model is intended for rice cultivation.",
    )

    if st.button("Calculate carbon opportunity", type="primary", use_container_width=True, key="simple_run_sim"):
        if crop != "Rice":
            st.warning(
                "The current Code4Nature methane-abatement model is designed for rice cultivation. "
                "Choose Rice to generate the present estimate."
            )
            return

        market_data = get_market_data()
        carbon_price = float(
            market_data.get("rice_methane_price_usd") or 20.0
        )
        low = float(market_data.get("rice_methane_range_low_usd") or 15.0)
        high = float(market_data.get("rice_methane_range_high_usd") or 25.0)
        source = market_data.get(
            "rice_methane_source",
            "Current published rice-methane market reference",
        )
        source_url = market_data.get(
            "rice_methane_source_url",
            "https://indianexpress.com/article/explained/explained-economics/methane-emission-reductions-farmers-climate-change-rice-carbon-credits-10443685/",
        )

        # DIGITAL MRV REFERENCE STANDARD
        # 120 kg CH4 abatement / ha / season × GWP100 28
        # = 3.36 tCO2e / ha / season.
        ch4_reduction_per_ha = CH4_REDUCTION_PER_HA
        co2e_per_ha = ch4_reduction_per_ha * GWP_CH4 / 1000.0
        seasonal_credits = area * co2e_per_ha

        # The prototype treats one rice season as one annual opportunity
        # for the 5-year economic view.
        annual_credits = seasonal_credits

        future_years = 5
        future_credits = annual_credits * future_years
        future_value = future_credits * carbon_price

        st.session_state["simple_farm_result"] = {
            "area": area,
            "crop": crop,
            "ch4_reduction_per_ha": ch4_reduction_per_ha,
            "co2e_per_ha": co2e_per_ha,
            "carbon_price": carbon_price,
            "price_low": low,
            "price_high": high,
            "market_source": source,
            "market_source_url": source_url,
            "annual_credits": annual_credits,
            "future_credits": future_credits,
            "future_value": future_value,
        }

    result = st.session_state.get("simple_farm_result")
    if result:
        st.markdown("### Your estimated opportunity")
        st.markdown(
            f'<div class="info-card"><b>{result["area"]:.2f} hectares of {result["crop"]}</b>'
            f'<div class="small-copy" style="margin-top:.4rem;">Digital MRV standard: '
            f'{result["ch4_reduction_per_ha"]:,.0f} kg CH4/ha/season × '
            f'{GWP_CH4:.0f} GWP100 = {result["co2e_per_ha"]:.2f} tCO2e/ha/season.</div>'
            f'<div class="small-copy" style="margin-top:.4rem;">Current rice-methane reference: '
            f'USD {result["carbon_price"]:,.2f} per tCO2e '
            f'(reported range USD {result["price_low"]:,.2f}–{result["price_high"]:,.2f})</div></div>',
            unsafe_allow_html=True,
        )

        r1, r2 = st.columns(2)
        r1.metric("Estimated credits / season", f"{result['annual_credits']:,.2f} tCO2e")
        r2.metric("Next 5-year potential credits", f"{result['future_credits']:,.2f} tCO2e")

        @st.cache_data(ttl=300, show_spinner=False)
        def get_live_usd_inr():
            fallback_rate = 95.91
            try:
                response = requests.get(
                    "https://open.er-api.com/v6/latest/USD",
                    timeout=5,
                )
                response.raise_for_status()
                data = response.json()
                rate = float(data["rates"]["INR"])
                if rate <= 0:
                    raise ValueError("Invalid USD/INR rate")
                return rate, data.get("time_last_update_utc", "API update time unavailable"), "open.er-api.com"
            except (requests.RequestException, KeyError, TypeError, ValueError):
                return fallback_rate, "Fallback rate", "MSEI/RBI reference rate"

        usd_inr, fx_updated_at, fx_source = get_live_usd_inr()
        future_value_inr = result["future_value"] * usd_inr

        v1, v2 = st.columns(2)
        v1.metric("Potential value over next 5 years", f"USD {result['future_value']:,.0f}")
        v2.metric("Potential value over next 5 years", f"₹{future_value_inr:,.0f}")
        st.caption(
            f"Live FX: 1 USD = ₹{usd_inr:,.2f} • Source: {fx_source} • Updated: {fx_updated_at}. "
            "INR value is the USD scenario converted at the latest available API rate."
        )

        chart = pd.DataFrame(
            {
                "Years": [1, 2, 3, 4, 5],
                "Future potential value (USD)": [
                    result["annual_credits"] * result["carbon_price"] * year
                    for year in [1, 2, 3, 4, 5]
                ],
            }
        ).set_index("Years")
        st.markdown("#### 5-year view")
        st.line_chart(chart, height=280)

        st.markdown(
            f'<div class="small-copy">Price source: <a href="{result["market_source_url"]}" target="_blank">{result["market_source"]}</a>.</div>',
            unsafe_allow_html=True,
        )

        with st.expander("Details"):
            details = [
                "**Digital MRV standard:** 120 kg CH4 abatement per hectare per rice season.",
                "**CO2e conversion:** 120 kg CH4 × GWP100 28 ÷ 1000 = 3.36 tCO2e per hectare per season.",
                "**10-hectare reference:** 10 ha × 3.36 = 33.60 tCO2e per season.",
                "**5-year potential value:** five one-season-per-year opportunities using the current carbon-price reference.",
                "**USD → INR conversion:** the displayed INR estimate uses the latest available USD/INR rate from the live exchange-rate API.",
                "**Current rice-methane reference price:** midpoint of the currently reported USD 15–25/tCO2e rice methane credit range.",
            ]
            for line in details:
                st.markdown(line)
            st.caption(
                "The carbon price is a current market reference, not a guaranteed transaction price. "
                "Future values are not guaranteed, and the INR figure changes as the USD/INR exchange rate changes."
            )

        st.success(
            "Thank you for making an effort to save Mother Earth. "
            "Your farm data helps build the evidence base for climate-smart rice."
        )

def render_market():
    st.markdown('<div class="section-kicker">MARKET FEED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Carbon prices: global + India</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">Carbon is not one universal commodity price. This panel separates a global agriculture market reference, a voluntary carbon-token proxy, and the India VCM conversion. No fabricated Indian compliance-market spot price is shown.</p>',
        unsafe_allow_html=True,
    )
    if st.button("Refresh market feed"):
        st.session_state["market_data"] = None
    market_data = st.session_state.get("market_data")
    if market_data is None:
        with st.spinner("Refreshing market feed..."):
            market_data = get_market_data()
            st.session_state["market_data"] = market_data

    ag = float(market_data.get("global_agriculture_median_usd", 71.40))
    bct = float(market_data.get("market_carbon_price_usd", DEFAULT_VCM_PRICE_USD))
    fx = float(market_data.get("fx_usd_inr", 88.0))
    india_proxy = ag * fx

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Global agriculture median", f"USD {ag:,.2f}")
    p2.metric("VCM carbon-token proxy", f"USD {bct:,.2f}")
    p3.metric("USD / INR", f"₹{fx:,.2f}")
    p4.metric("India VCM reference proxy", f"₹{india_proxy:,.2f}")

    st.caption(
        f"Global source: {market_data.get('global_source','N/A')} | "
        f"VCM proxy: {market_data.get('market_source','N/A')} | "
        f"FX source: {market_data.get('fx_source','N/A')} | "
        f"Updated: {market_data.get('updated_at','N/A')}"
    )

    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown('<div class="info-card"><b>Global VCM</b><div class="small-copy" style="font-size:.82rem;">Observable reference data, not a guaranteed sale price for project credits.</div></div>', unsafe_allow_html=True)
    with q2:
        st.markdown('<div class="info-card"><b>India VCM proxy</b><div class="small-copy" style="font-size:.82rem;">Global agriculture reference converted using current FX for scenario modelling.</div></div>', unsafe_allow_html=True)
    with q3:
        st.markdown('<div class="info-card"><b>India ICM / CCC</b><div class="small-copy" style="font-size:.82rem;">Not displayed as a live spot price in this prototype.</div></div>', unsafe_allow_html=True)


def render_economics():
    st.markdown('<div class="section-kicker">ECONOMICS SCENARIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Economics Scenario Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">A scenario estimate, not a revenue guarantee — every assumption below is a slider you control. USD↔INR uses a live exchange rate when available.</p>',
        unsafe_allow_html=True,
    )

    html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}
body{margin:0;background:#0f172a;color:#fff;font-family:Inter,Arial,sans-serif}
.wrap{background:#0f172a;border-radius:18px;padding:30px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}
.control{margin-bottom:24px}
.row{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:8px}
.label{font-size:14px;color:#cbd5e1}
.value{font-weight:700;color:#86efac}
input[type=range]{width:100%;accent-color:#10b981}
.result{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:24px}
.result-row{display:flex;flex-direction:column;border-bottom:1px solid #334155;padding-bottom:14px;margin-bottom:14px}
.result-row:last-child{border-bottom:0;margin-bottom:0;padding-bottom:0}
.muted{color:#94a3b8;font-size:14px}
.big{font-size:24px;font-weight:700}
.green{color:#34d399}
.blue{color:#93c5fd}
.small{font-size:12px;color:#64748b}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="grid">
    <div>
      <div class="control">
        <div class="row">
          <label class="label">Farm Area</label>
          <span id="val-acres" class="value">1,000 Acres</span>
        </div>
        <input type="range" id="slider-acres" min="1" max="10000" step="1" value="1000">
      </div>

      <div class="control">
        <div class="row">
          <label class="label">Abatement (tCO2e / Acre)</label>
          <span id="val-abatement" class="value">1.2 tCO2e</span>
        </div>
        <input type="range" id="slider-abatement" min="0.5" max="2.0" step="0.1" value="1.2">
      </div>

      <div class="control">
        <div class="row">
          <label class="label">Indicative Carbon Price (USD)</label>
          <span id="val-price" class="value">$24.00</span>
        </div>
        <input type="range" id="slider-price" min="1" max="50" step="0.5" value="24">
      </div>

      <div class="control">
        <div class="row">
          <label class="label">Farmer Profit Share (%)</label>
          <span id="val-share" class="value">65%</span>
        </div>
        <input type="range" id="slider-share" min="50" max="100" step="1" value="65">
      </div>

      <button id="btn-use-live-price" style="border:0;border-radius:8px;padding:8px 12px;background:#334155;color:#fff;font-size:12px;cursor:pointer;">
        ⚡ Use current live/indicative price
      </button>
    </div>

    <div class="result">
      <div class="result-row">
        <span class="muted">Estimated Carbon Credits</span>
        <span id="res-credits" class="big">0 VCUs</span>
      </div>

      <div class="result-row">
        <span class="muted">Potential Gross Value</span>
        <div style="display:flex;align-items:baseline;gap:12px;">
          <span id="res-gross-usd" class="big">$0</span>
          <span id="res-gross-inr" class="muted">₹0</span>
        </div>
      </div>

      <div class="result-row">
        <span class="green" style="font-weight:600;font-size:14px;">Projected Farmer Share</span>
        <div style="display:flex;align-items:baseline;gap:12px;">
          <span id="res-farmers-usd" class="big green">$0</span>
          <span id="res-farmers-inr" class="muted">₹0</span>
        </div>
      </div>

      <div class="result-row">
        <span class="blue" style="font-weight:600;font-size:14px;">Platform / Company Share</span>
        <div style="display:flex;align-items:baseline;gap:12px;">
          <span id="res-platform-usd" class="big blue">$0</span>
          <span id="res-platform-inr" class="muted">₹0</span>
        </div>
      </div>

      <p id="fx-rate-note" class="small" style="margin:16px 0 0;">—</p>
      <p class="small" style="margin:8px 0 0;">Prototype estimate only — not a verified carbon credit or a price guarantee.</p>
    </div>
  </div>
</div>

<script>
const sliderAcres=document.getElementById('slider-acres');
const sliderAbatement=document.getElementById('slider-abatement');
const sliderPrice=document.getElementById('slider-price');
const sliderShare=document.getElementById('slider-share');

const formatUSD=new Intl.NumberFormat('en-US',{
  style:'currency',
  currency:'USD',
  maximumFractionDigits:0
});
const formatINR=new Intl.NumberFormat('en-IN',{
  style:'currency',
  currency:'INR',
  maximumFractionDigits:0
});

let livePrice={usd:24.0,source:'manual fallback',label:'indicative'};
let liveFx={rate:83.5,source:'static fallback'};

async function fetchLiveCarbonPrice(){
  try{
    const res=await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=toucan-protocol-base-carbon-tonne&vs_currencies=usd,inr'
    );
    if(!res.ok) throw new Error('price fetch failed');
    const data=await res.json();
    const usd=data['toucan-protocol-base-carbon-tonne']?.usd;

    if(typeof usd==='number' && usd>0){
      livePrice={
        usd,
        source:'CoinGecko (Toucan BCT, live)',
        label:'live tokenized-credit proxy — not a rice-project price'
      };
      return;
    }
    throw new Error('unexpected response shape');
  }catch(e){
    livePrice={
      usd:24.0,
      source:'manual fallback (live fetch failed)',
      label:'indicative'
    };
  }
}

async function fetchLiveFxRate(){
  try{
    const res=await fetch('https://open.er-api.com/v6/latest/USD');
    if(!res.ok) throw new Error('fx fetch failed');
    const data=await res.json();
    const rate=data?.rates?.INR;

    if(typeof rate==='number' && rate>0){
      liveFx={rate,source:'open.er-api.com (live)'};
      return;
    }
    throw new Error('unexpected response shape');
  }catch(e){
    liveFx={rate:83.5,source:'static fallback (live fetch failed)'};
  }
}

function updateEconomicsCalculator(){
  const acres=parseInt(sliderAcres.value);
  const abatement=parseFloat(sliderAbatement.value);
  const priceUSD=parseFloat(sliderPrice.value);
  const share=parseInt(sliderShare.value);
  const fx=liveFx.rate;

  document.getElementById('val-acres').textContent=
    acres.toLocaleString()+' Acres';
  document.getElementById('val-abatement').textContent=
    abatement.toFixed(1)+' tCO2e';
  document.getElementById('val-price').textContent=
    '$'+priceUSD.toFixed(2);
  document.getElementById('val-share').textContent=
    share+'%';

  const totalCredits=acres*abatement;
  const grossRevenueUSD=totalCredits*priceUSD;
  const farmerRevenueUSD=grossRevenueUSD*(share/100);
  const platformRevenueUSD=grossRevenueUSD-farmerRevenueUSD;

  document.getElementById('res-credits').textContent=
    totalCredits.toLocaleString('en-US')+' VCUs (est.)';

  document.getElementById('res-gross-usd').textContent=
    formatUSD.format(grossRevenueUSD);
  document.getElementById('res-gross-inr').textContent=
    formatINR.format(grossRevenueUSD*fx);

  document.getElementById('res-farmers-usd').textContent=
    formatUSD.format(farmerRevenueUSD);
  document.getElementById('res-farmers-inr').textContent=
    formatINR.format(farmerRevenueUSD*fx);

  document.getElementById('res-platform-usd').textContent=
    formatUSD.format(platformRevenueUSD);
  document.getElementById('res-platform-inr').textContent=
    formatINR.format(platformRevenueUSD*fx);

  document.getElementById('fx-rate-note').textContent=
    'FX: 1 USD ≈ ₹'+liveFx.rate.toFixed(2)+
    ' ('+liveFx.source+'). Price: '+livePrice.source+'.';
}

[sliderAcres,sliderAbatement,sliderPrice,sliderShare]
  .forEach(s=>s.addEventListener('input',updateEconomicsCalculator));

document.getElementById('btn-use-live-price').addEventListener('click',()=>{
  sliderPrice.value=livePrice.usd.toFixed(2);
  updateEconomicsCalculator();
});

(async function boot(){
  await Promise.all([fetchLiveCarbonPrice(),fetchLiveFxRate()]);
  sliderPrice.value=livePrice.usd.toFixed(2);
  updateEconomicsCalculator();

  setInterval(async()=>{
    await Promise.all([fetchLiveCarbonPrice(),fetchLiveFxRate()]);
    updateEconomicsCalculator();
  },120000);
})();
</script>
</body>
</html>"""
    components.html(html, height=570, scrolling=False)

def render_policy():
    st.markdown('<div class="section-kicker">INDIA ENABLEMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Government policy, subsidies & FPO layer</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="small-copy">This section is a decision aid rather than an eligibility guarantee. The supplied project prototype separates agricultural infrastructure/FPO support routes from the carbon-credit methodology itself.</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    with cols[0]:
        st.markdown(
            """
            <div class="info-card">
            <h4>Agriculture Infrastructure Fund (AIF)</h4>
            <div class="small-copy">A financing route for eligible agriculture infrastructure. Scheme terms and eligibility should be checked against current official guidance.</div>
            <hr>
            <h4>10,000 FPO ecosystem / SFAC</h4>
            <div class="small-copy">FPO formation, promotion and convergence resources can support aggregation and project coordination.</div>
            <hr>
            <h4>FPO Equity Grant</h4>
            <div class="small-copy">The supplied prototype references matching equity support for eligible Farmer Producer Companies, subject to scheme conditions and limits.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            """
            <div class="info-card">
            <h4>Indian Carbon Market / CCTS</h4>
            <div class="small-copy">Keep India's compliance framework separate from voluntary carbon-market instruments. The prototype intentionally does not invent an Indian CCC spot price.</div>
            <hr>
            <h4>Where CarbonAWD fits</h4>
            <div class="small-copy"><b>Farmer:</b> adopts AWD and supplies field evidence.<br>
            <b>FPO:</b> aggregates farms and coordinates training/MRV.<br>
            <b>CarbonAWD / MRV platform:</b> manages evidence, satellite integration and calculations.<br>
            <b>Registry / VVB / buyer:</b> remains independent from this demonstrator.</div>
            <hr>
            <h4>Methodology status</h4>
            <div class="small-copy">The supplied materials reference Verra VM0051 as a methodology reference; a dashboard estimate is not proof that a project is creditable.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def run():
    st.set_page_config(
        page_title="CarbonAWD | Rice MRV & Carbon Intelligence",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_state()
    _inject_css()
    render_top_nav()
    st.sidebar.markdown("## 🌾 Code4Nature")
    st.sidebar.caption("Rice carbon intelligence • Digital MRV")
    st.sidebar.markdown("---")
    status = check_health()
    if status.get("sentinel_hub_configured"):
        st.sidebar.success("Sentinel-1: LIVE")
    else:
        st.sidebar.info("Sentinel-1: SIMULATOR")
    st.sidebar.markdown(
        "**Prototype sections**\n\n"
        "Overview → Farm Intelligence → Carbon Economics → MRV → Policy / FPO"
    )

    page = st.radio("PRODUCT", ["Overview", "Farm Intelligence", "Carbon Economics", "MRV & Evidence", "Policy / FPO"], horizontal=True, label_visibility="collapsed")
    st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
    render_hero()
    if page == "Overview":
        render_why()
    elif page == "Farm Intelligence":
        render_mrv()
    elif page == "Carbon Economics":
        render_market()
        render_economics()
    elif page == "MRV & Evidence":
        render_mrv()
    else:
        render_policy()
    st.divider()
    st.markdown(
        """
        <div class="footer">
        CarbonAWD • Code4Nature 2026 prototype<br>
        Demonstrator only. Carbon estimates, prices and profitability are scenario values unless independently verified.
        </div>
        """,
        unsafe_allow_html=True,
    )
