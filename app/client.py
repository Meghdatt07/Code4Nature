import hashlib
import math
import os
import re
from datetime import datetime, timedelta, timezone

import requests
import streamlit as st

SH_TOKEN_URL = (
    "https://services.sentinel-hub.com/auth/realms/main/"
    "protocol/openid-connect/token"
)
SH_STATS_URL = "https://services.sentinel-hub.com/api/v1/statistics"


def _secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def check_health():
    client_id = _secret("SH_CLIENT_ID")
    client_secret = _secret("SH_CLIENT_SECRET")
    return {
        "ok": True,
        "sentinel_hub_configured": bool(client_id and client_secret),
        "mode": "live" if client_id and client_secret else "simulator",
    }


def _bbox(lat: float, lon: float, delta: float = 0.003):
    return [lon - delta, lat - delta, lon + delta, lat + delta]


@st.cache_data(ttl=300, show_spinner=False)
def _sentinel_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        SH_TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _simulate_sar(lat: float, lon: float):
    digest = hashlib.sha256(f"{lat:.6f},{lon:.6f}".encode("utf-8")).hexdigest()
    value = int(digest[:8], 16) / 0xFFFFFFFF
    vv_db = -19.0 + 7.0 * value
    vh_db = -25.0 + 6.0 * value
    moisture_proxy = max(0.0, min(100.0, 50.0 + (vv_db + 15.0) * 7.0))
    return {
        "source": "Built-in simulator",
        "moisture_proxy_percent": moisture_proxy,
        "vv_mean_db": vv_db,
        "vh_mean_db": vh_db,
        "observation_date": datetime.now(timezone.utc).date().isoformat(),
        "note": (
            "Simulator fallback. These deterministic values are demo values "
            "and are not Sentinel-1 observations."
        ),
    }


def _live_sar(lat: float, lon: float, polygon=None):
    client_id = _secret("SH_CLIENT_ID")
    client_secret = _secret("SH_CLIENT_SECRET")
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=18)

    evalscript = """//VERSION=3
function setup() {
  return {
    input: [{bands: ["VV", "VH", "dataMask"]}],
    output: [
      {id: "sar", bands: 2, sampleType: "FLOAT32"},
      {id: "dataMask", bands: 1}
    ]
  };
}
function evaluatePixel(s) {
  return {
    sar: [s.VV, s.VH],
    dataMask: [s.dataMask]
  };
}"""

    bounds = {
        "bbox": _bbox(lat, lon),
        "properties": {
            "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        },
    }

    if polygon and len(polygon) >= 3:
        ring = [[float(lon_), float(lat_)] for lat_, lon_ in polygon]
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        bounds["geometry"] = {
            "type": "Polygon",
            "coordinates": [ring],
        }

    payload = {
        "input": {
            "bounds": bounds,
            "data": [
                {
                    "type": "sentinel-1-grd",
                    "dataFilter": {"mosaickingOrder": "mostRecent"},
                    "processing": {"orthorectify": True},
                }
            ],
        },
        "aggregation": {
            "timeRange": {
                "from": start.isoformat().replace("+00:00", "Z"),
                "to": now.isoformat().replace("+00:00", "Z"),
            },
            "aggregationInterval": {"of": "P6D"},
            "evalscript": evalscript,
            "resx": 0.0001,
            "resy": 0.0001,
        },
        "calculations": {"default": {}},
    }

    token = _sentinel_token(client_id, client_secret)
    response = requests.post(
        SH_STATS_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=45,
    )
    response.raise_for_status()

    data = response.json().get("data", [])
    if not data:
        raise RuntimeError("No Sentinel-1 observations found for this AOI.")

    latest = data[-1]
    bands = latest.get("outputs", {}).get("sar", {}).get("bands", {})
    vv = bands.get("B0", {}).get("stats", {}).get("mean")
    vh = bands.get("B1", {}).get("stats", {}).get("mean")

    vv_db = 10.0 * math.log10(vv) if vv and vv > 0 else None
    vh_db = 10.0 * math.log10(vh) if vh and vh > 0 else None

    proxy = None
    if vv_db is not None:
        proxy = max(0.0, min(100.0, 50.0 + (vv_db + 15.0) * 7.0))

    return {
        "source": "Sentinel Hub / Sentinel-1 GRD",
        "moisture_proxy_percent": proxy,
        "vv_mean_db": vv_db,
        "vh_mean_db": vh_db,
        "observation_date": latest.get("interval", {}).get("to"),
        "note": (
            "Relative wetness proxy derived from SAR backscatter. "
            "Absolute soil moisture requires field calibration and model validation."
        ),
    }


def get_sar_data(lat: float, lon: float, polygon=None):
    client_id = _secret("SH_CLIENT_ID")
    client_secret = _secret("SH_CLIENT_SECRET")

    if not (client_id and client_secret):
        return _simulate_sar(lat, lon)

    try:
        return _live_sar(lat, lon, polygon=polygon)
    except Exception as exc:
        simulated = _simulate_sar(lat, lon)
        simulated["source"] = "Simulator fallback after Sentinel Hub error"
        simulated["note"] = (
            f"Live Sentinel Hub request failed: {exc}. "
            "Showing deterministic simulator values instead."
        )
        return simulated


@st.cache_data(ttl=900, show_spinner=False)
def get_market_data():
    fx = 88.0
    fx_source = "fallback value"

    try:
        response = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=10,
        )
        response.raise_for_status()
        fx = float(response.json()["rates"]["INR"])
        fx_source = "open.er-api.com"
    except Exception:
        pass

    agriculture_median = None
    updated = ""

    try:
        response = requests.get(
            "https://www.carbon.fyi/data",
            timeout=15,
        )
        response.raise_for_status()
        html = response.text
        match = re.search(
            r"Agriculture.*?\$([0-9,.]+).*?\$([0-9,.]+)",
            html,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            agriculture_median = float(match.group(2).replace(",", ""))
        updated_match = re.search(
            r"Updated\s+([^<]+)",
            html,
            re.IGNORECASE,
        )
        if updated_match:
            updated = updated_match.group(1).strip()
    except Exception:
        pass

    market_carbon_price = None
    market_source = "fallback value"

    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": "toucan-protocol-base-carbon-tonne",
                "vs_currencies": "usd",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        value = data.get("toucan-protocol-base-carbon-tonne", {}).get("usd")
        if value is not None:
            market_carbon_price = float(value)
            market_source = "CoinGecko / Toucan BCT proxy"
    except Exception:
        pass

    if agriculture_median is None:
        agriculture_median = 71.40
    if market_carbon_price is None:
        market_carbon_price = 1.85

    return {
        "global_agriculture_median_usd": agriculture_median,
        "market_carbon_price_usd": market_carbon_price,
        "fx_usd_inr": fx,
        "global_source": "Carbon.fyi public market data",
        "market_source": market_source,
        "fx_source": fx_source,
        "updated_at": updated or "latest available feed or fallback",
        "india_note": (
            "India VCM proxy = global agriculture reference converted to INR. "
            "This is not an official Indian CCTS/CCC spot price."
        ),
    }
