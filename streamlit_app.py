import streamlit as st
from app.client import check_health, get_market_data, get_sar_data
from app.components import display_market_data, display_sar_data

st.set_page_config(
    page_title="CarbonAWD MRV",
    page_icon="🌾",
    layout="wide",
)

st.title("🌾 CarbonAWD — Rice AWD & Carbon MRV")
st.markdown(
    "A Streamlit demonstrator for Alternate Wetting and Drying (AWD), "
    "Sentinel-1 SAR monitoring, carbon-market reference pricing, and farm economics."
)

status = check_health()
if status["sentinel_hub_configured"]:
    st.success("Live Sentinel-1 mode is enabled.")
else:
    st.info(
        "Sentinel Hub credentials are not configured, so the SAR panel is using "
        "the built-in simulator. The app can still be deployed and used normally."
    )

tab1, tab2, tab3 = st.tabs(
    ["📡 SAR MRV Dashboard", "💰 Market & Economics", "📖 AWD & Policy"]
)

with tab1:
    st.header("Farm Location & SAR Analysis")
    st.write(
        "Enter a farm location and request Sentinel-1 SAR data. "
        "With credentials configured, the app queries Sentinel Hub directly. "
        "Otherwise it provides deterministic simulator values."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        lat = st.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=23.2156,
            step=0.0001,
            format="%.4f",
        )
        lon = st.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=72.6369,
            step=0.0001,
            format="%.4f",
        )

        if st.button("Fetch Satellite Data", type="primary", use_container_width=True):
            with st.spinner("Fetching SAR data..."):
                st.session_state["sar_data"] = get_sar_data(lat, lon)

    with col2:
        if "sar_data" in st.session_state:
            display_sar_data(st.session_state["sar_data"])
        else:
            st.info(
                "Click 'Fetch Satellite Data' to view radar backscatter and "
                "the relative wetness proxy."
            )

with tab2:
    st.header("Carbon Market Pricing")
    market_data = get_market_data()
    display_market_data(market_data)

    st.divider()
    st.subheader("Farmer/FPO vs MRV Company Economics Calculator")

    col_a, col_b, col_c = st.columns(3)

    hectares = col_a.number_input(
        "Farm Size (Hectares)",
        min_value=0.1,
        value=1.0,
        step=0.1,
    )
    credits_per_ha = col_b.number_input(
        "Expected Credits / Ha / Year",
        min_value=0.0,
        value=4.0,
        step=0.5,
    )
    split_farmer = col_c.slider(
        "Farmer/FPO Revenue Share (%)",
        min_value=0,
        max_value=100,
        value=70,
    )

    total_credits = hectares * credits_per_ha
    price_usd = float(market_data.get("global_agriculture_median_usd", 71.40))
    fx = float(market_data.get("fx_usd_inr", 88.0))

    total_rev_usd = total_credits * price_usd
    total_rev_inr = total_rev_usd * fx
    farmer_rev_inr = total_rev_inr * split_farmer / 100
    company_rev_inr = total_rev_inr - farmer_rev_inr

    metrics_a, metrics_b, metrics_c = st.columns(3)
    metrics_a.metric("Total Revenue", f"₹{total_rev_inr:,.0f}")
    metrics_b.metric("Farmer/FPO Share", f"₹{farmer_rev_inr:,.0f}")
    metrics_c.metric("MRV/Company Share", f"₹{company_rev_inr:,.0f}")

    st.caption(
        f"Estimated credits: {total_credits:,.2f} | "
        f"Reference price: ${price_usd:,.2f}/credit | "
        f"FX: ₹{fx:,.2f}/USD"
    )

with tab3:
    st.header("Alternate Wetting & Drying (AWD)")
    st.markdown(
        """
**Alternate Wetting and Drying (AWD)** is a rice irrigation practice in
which the field is periodically allowed to dry instead of remaining
continuously flooded.

### MRV notes

- **SAR moisture result:** the app displays a relative wetness proxy derived
  from Sentinel-1 backscatter.
- **Not absolute soil moisture:** scientific calibration requires field
  observations and validation data.
- **Simulator:** when Sentinel Hub credentials are absent, deterministic
  demonstration values are generated locally so the Streamlit deployment
  remains usable.
- **Carbon pricing:** the app displays a global agriculture reference value
  and separately labels the India conversion as a reference proxy. It does
  not fabricate an Indian domestic CCTS/CCC spot price.
"""
    )

st.sidebar.header("Deployment")
st.sidebar.write("Run this repository as a single Streamlit application.")
st.sidebar.code("streamlit run streamlit_app.py")
st.sidebar.caption(
    "Optional live SAR mode requires SH_CLIENT_ID and SH_CLIENT_SECRET "
    "in Streamlit secrets."
)
