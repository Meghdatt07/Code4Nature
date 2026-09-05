# File: app/api_client.py
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

@st.cache_data(ttl=300)
def check_health():
    """Checks if the FastAPI backend is running and credentials are set."""
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return r.json()
    except Exception:
        return None

@st.cache_data(ttl=3600)
def get_market_data():
    """Fetches live USD/INR and carbon market data from backend."""
    try:
        r = requests.get(f"{API_BASE_URL}/api/market", timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_sar_data(lat, lon):
    """Fetches Sentinel-1 GRD data for the specified coordinates."""
    try:
        r = requests.get(f"{API_BASE_URL}/api/sar", params={"lat": lat, "lon": lon}, timeout=45)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
