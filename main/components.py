# File: app/components.py
import streamlit as st

def display_market_data(market_data):
    st.subheader("Global VCM & India Market Proxy")
    if "error" in market_data:
        st.error("Could not load market data.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Global Ag Median", f"${market_data.get('global_agriculture_median_usd', 0):.2f}")
    col2.metric("USD/INR FX Rate", f"₹{market_data.get('fx_usd_inr', 0):.2f}")
    
    inr_proxy = market_data.get('global_agriculture_median_usd', 0) * market_data.get('fx_usd_inr', 0)
    col3.metric("India VCM Proxy (INR)", f"₹{inr_proxy:,.2f}")
    
    st.caption(f"Source: {market_data.get('global_source')} | Updated: {market_data.get('updated_at')}")
    st.info(market_data.get('india_note'))

def display_sar_data(sar_data):
    st.subheader("Sentinel-1 SAR Moisture Proxy")
    if "error" in sar_data:
        st.error(f"Error fetching SAR data: {sar_data['error']}")
        return
    
    st.write(f"**Source:** {sar_data.get('source')}")
    
    obs_date = sar_data.get('observation_date')
    st.write(f"**Observation Date:** {obs_date if obs_date else 'Simulator Fallback'}")
    
    proxy = sar_data.get('moisture_proxy_percent')
    if proxy is not None:
        st.metric("Relative Wetness Proxy", f"{proxy:.1f}%")
        st.progress(int(proxy) / 100)
    else:
        st.warning("No moisture proxy available. The system has defaulted to the simulator fallback because backend credentials are unconfigured.")
    
    col1, col2 = st.columns(2)
    vv = sar_data.get('vv_mean_db')
    vh = sar_data.get('vh_mean_db')
    col1.metric("VV Mean (dB)", f"{vv:.2f}" if vv else "N/A")
    col2.metric("VH Mean (dB)", f"{vh:.2f}" if vh else "N/A")
    
    st.caption(sar_data.get('note'))
