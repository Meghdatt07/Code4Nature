# Code4Nature — CarbonAWD Streamlit App

Code4Nature is a Streamlit demonstrator for rice **Alternate Wetting and Drying (AWD)**, Sentinel-1 SAR monitoring, carbon-market reference pricing, and farmer/FPO economics.

## Streamlit deployment

This repository is now structured to run **directly on Streamlit**.

### 1. Deploy on Streamlit Community Cloud

1. Open Streamlit Community Cloud.
2. Select **Deploy an app**.
3. Choose this GitHub repository.
4. Select the `main` branch.
5. Set the main file path to:
   `streamlit_app.py`
6. Deploy.

No separate FastAPI server and no `localhost:8000` connection are required.

## Optional: enable live Sentinel-1 mode

The app works without credentials by using a clearly labelled deterministic simulator.

To enable live Sentinel Hub requests, add these secrets in the Streamlit app settings:

```toml
SH_CLIENT_ID = "your-sentinel-hub-client-id"
SH_CLIENT_SECRET = "your-sentinel-hub-client-secret"
```

**Do not put credentials in GitHub source files.**

## Local run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run streamlit_app.py
```

## Important data notes

- The SAR output is a **relative wetness proxy**, not an absolute soil-moisture measurement.
- A scientifically calibrated soil-moisture model requires field observations and validation.
- The displayed global agriculture value is a market reference and the INR value is a conversion proxy.
- The app does not invent an official Indian CCTS/CCC spot price.

## Repository structure

```
Code4Nature/
├── streamlit_app.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── client.py
│   └── components.py
└── engine/
    └── main.py
```

The legacy FastAPI backend is retained in `engine/main.py` for reference, but the Streamlit application no longer depends on it.
