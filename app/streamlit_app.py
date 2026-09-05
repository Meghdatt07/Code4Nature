# File: streamlit_app.py
import streamlit as st
from app.api_client import check_health, get_market_data, get_sar_data
from app.components import display_market_data, display_sar_data

# Page configuration
st.set_page_config(page_title="CarbonAWD MRV", layout="wide", page_icon="🌾")

st.title("CarbonAWD — IIT Gandhinagar Rice MRV")
st.markdown("A single-page demonstrator for rice methane reduction (AWD), MRV, and carbon-credit workflows.")

# Connectivity Health Check
health = check_health()
if not health:
    st.error("Cannot connect to FastAPI backend. Please ensure you are running `uvicorn engine.main:app --host 0.0.0.0 --port 8000` in a separate terminal.")
    st.stop()

if not health.get("sentinel_hub_configured"):
    st.warning("⚠️ Sentinel Hub credentials not configured. Live Sentinel-1 queries are disabled, switching to simulator fallback.")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📡 SAR MRV Dashboard", "💰 Market & Economics", "📖 About AWD & Policy"])

with tab1:
    st.header("Farm Location & SAR Analysis")
    st.write("Input field coordinates to fetch real Sentinel-1 SAR statistics.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        lat = st.number_input("Latitude", value=23.2156, format="%.4f")
        lon = st.number_input("Longitude", value=72.6369, format="%.4f")
        
        if st.button("Fetch Satellite Data", type="primary"):
            with st.spinner("Querying Sentinel Hub API via backend..."):
                sar_data = get_sar_data(lat, lon)
                st.session_state['sar_data'] = sar_data
    
    with col2:
        if 'sar_data' in st.session_state:
            display_sar_data(st.session_state['sar_data'])
        else:
            st.info("Click 'Fetch Satellite Data' to view radar backscatter and the calculated relative wetness proxy.")

with tab2:
    st.header("Carbon Market Pricing")
    # Fetch data directly from FastAPI endpoints
    market_data = get_market_data()
    display_market_data(market_data)
    
    st.divider()
    
    st.subheader("Farmer/FPO vs MRV Company Economics Calculator")
    col_a, col_b, col_c = st.columns(3)
    hectares = col_a.number_input("Farm Size (Hectares)", min_value=0.1, value=1.0, step=0.1)
    credits_per_ha = col_b.number_input("Expected Credits/Ha/Year", value=4.0)
    split_farmer = col_c.slider("Farmer/FPO Revenue Share (%)", 0, 100, 70)
    
    total_credits = hectares * credits_per_ha
    price_usd = market_data.get('global_agriculture_median_usd', 71.40)
    fx = market_data.get('fx_usd_inr', 88.0)
    
    total_rev_usd = total_credits * price_usd
    total_rev_inr = total_rev_usd * fx
    farmer_rev_inr = total_rev_inr * (split_farmer / 100)
    company_rev_inr = total_rev_inr - farmer_rev_inr
    
    metrics_a, metrics_b, metrics_c = st.columns(3)
    metrics_a.metric("Total Generated Revenue", f"₹{total_rev_inr:,.0f}")
    metrics_b.metric("Farmer/FPO Share", f"₹{farmer_rev_inr:,.0f}")
    metrics_c.metric("Company/MRV Share", f"₹{company_rev_inr:,.0f}")

with tab3:
    st.header("India Policy, AWD & Subsidy Context")
    st.write("""
    **Alternate Wetting and Drying (AWD)** is a managed irrigation practice that reduces methane emissions from rice paddies by allowing the field to dry intermittently rather than keeping it continuously flooded.
    
    **Important Implementation Notes:**
    * **Soil Moisture Model**: The current architecture yields a relative wetness proxy derived from SAR backscatter. Absolute soil moisture calculation necessitates field calibration with physical sensors.
    * **Market Separation**: This app maintains an explicit separation between global VCM observable pricing (which operates in USD) and India's domestic CCTS/CCC market which we intentionally do not conflate.
    """)
