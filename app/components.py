import streamlit as st


def display_market_data(market_data):
    st.subheader("Global Carbon Market Reference")

    if "error" in market_data:
        st.error("Could not load market data.")
        return

    price_usd = float(market_data.get("global_agriculture_median_usd", 0.0))
    fx = float(market_data.get("fx_usd_inr", 0.0))
    inr_proxy = price_usd * fx

    col1, col2, col3 = st.columns(3)
    col1.metric("Agriculture Reference", f"${price_usd:,.2f}")
    col2.metric("USD / INR", f"₹{fx:,.2f}")
    col3.metric("India INR Reference Proxy", f"₹{inr_proxy:,.2f}")

    st.caption(
        f"Source: {market_data.get('global_source', 'N/A')} | "
        f"FX: {market_data.get('fx_source', 'N/A')} | "
        f"Updated: {market_data.get('updated_at', 'N/A')}"
    )
    st.info(market_data.get("india_note", ""))


def display_sar_data(sar_data):
    st.subheader("Sentinel-1 SAR Moisture Proxy")

    if "error" in sar_data:
        st.error(f"Error: {sar_data['error']}")
        return

    st.write(f"**Source:** {sar_data.get('source', 'N/A')}")

    observation_date = sar_data.get("observation_date")
    st.write(
        f"**Observation Date:** "
        f"{observation_date if observation_date else 'N/A'}"
    )

    proxy = sar_data.get("moisture_proxy_percent")
    if proxy is not None:
        proxy = float(proxy)
        st.metric("Relative Wetness Proxy", f"{proxy:.1f}%")
        st.progress(min(100, max(0, int(proxy))))
    else:
        st.warning("No moisture proxy is available for this observation.")

    col1, col2 = st.columns(2)
    vv = sar_data.get("vv_mean_db")
    vh = sar_data.get("vh_mean_db")

    col1.metric(
        "VV Mean (dB)",
        f"{float(vv):.2f}" if vv is not None else "N/A",
    )
    col2.metric(
        "VH Mean (dB)",
        f"{float(vh):.2f}" if vh is not None else "N/A",
    )

    note = sar_data.get("note")
    if note:
        st.caption(note)
