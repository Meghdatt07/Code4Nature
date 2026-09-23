# Code4Nature — CarbonAWD Streamlit Application

CarbonAWD is the Code4Nature project demonstrator for rice **Alternate Wetting and Drying (AWD)**, field/SAR MRV, carbon-market scenario modelling, farm economics, and the farmer/FPO layer.

## Interface

The Streamlit dashboard now mirrors the supplied CarbonAWD HTML prototype:

- dark CarbonAWD visual theme and data-flow hero
- science/problem section
- interactive farm map
- clickable farm point and map navigation
- polygon and rectangle farm-boundary drawing
- automatic farm area calculation in hectares
- selected farm geometry passed to the live Sentinel-1 SAR request
- simulator fallback when Sentinel Hub credentials are not configured
- AWD WET / DRYING / REWETTING telemetry simulator
- 30-day water-depth chart
- global agriculture carbon-market reference
- voluntary carbon-token proxy
- USD/INR live feed with fallback
- Government ERF scenario vs live VCM proxy pricing
- methane reduction, CO2e, carbon credits, gross revenue and farmer/company shares
- policy, subsidy, FPO and India carbon-market context

## Streamlit deployment

Deploy this repository directly on Streamlit Community Cloud.

- Repository: `Meghdatt07/Code4Nature`
- Branch: `main`
- Recommended main file: `streamlit_app.py`

No FastAPI server and no `localhost:8000` dependency are required by the Streamlit dashboard.

The repository also keeps `app/streamlit_app.py` runnable for deployments that were previously configured to use that path.

## Optional live Sentinel-1 mode

Add these secrets in Streamlit Cloud:

```toml
SH_CLIENT_ID = "your-sentinel-hub-client-id"
SH_CLIENT_SECRET = "your-sentinel-hub-client-secret"
```

Do not commit credentials to GitHub.

Without these secrets the farm map, simulator, calculator and dashboard remain usable.

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

For the legacy entry path:

```bash
streamlit run app/streamlit_app.py
```

## Calculation assumptions

The supplied prototype uses 120 kg CH4 reduction per hectare per season, GWP-100 of methane = 28, 1 tCO2e represented as 1 carbon-credit unit for scenario modelling, and a Government ERF scenario price of USD 15/tCO2e. Farmer/FPO share is adjustable by the user.

These are scenario assumptions from the supplied project materials, not a guarantee of credit issuance or a guaranteed market price.

## Scientific and market caveats

- SAR output is a relative wetness proxy, not absolute soil moisture.
- Absolute soil-moisture estimation requires field calibration and validation.
- The live VCM number is a proxy and is not a guaranteed sale price for a CarbonAWD project credit.
- India VCM and the Indian compliance/CCTS market are shown separately.
- A dashboard estimate is not itself a certified carbon credit.

## Repository structure

```text
Code4Nature/
├── streamlit_app.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── client.py
│   ├── components.py
│   └── streamlit_app.py
└── engine/
    └── main.py
```

`engine/main.py` remains only as a legacy/reference FastAPI backend.


## New CarbonAWD website

A separate interactive website is available in the website directory. It is based on the supplied CarbonAWD/Asterisk Climos MVP design and includes an interactive Leaflet farm map, movable farm marker, polygon/rectangle farm boundary selection, automatic farm-area calculation, AWD telemetry simulation, Sentinel-1 SAR simulator with an optional secure backend path, live FX and carbon-market proxy feeds, farmer/FPO and MRV/company economics, and India policy/FPO/carbon-market context.

The site is deployed through GitHub Actions using .github/workflows/deploy-website.yml.

### GitHub Pages

Open Settings → Pages in the repository and set the source to GitHub Actions. After the workflow completes, GitHub Pages will publish the contents of website/.

