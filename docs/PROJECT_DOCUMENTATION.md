# Asterisk Climos (CarbonAWD) — Project Documentation

**Code4Nature Challenge 2026 · Final submission**
**Team:** [Team Name] · Indian Institute of Technology Gandhinagar
**Team leader:** [Name, Email] · **Members:** [Names, Roles] · **Mentor:** [Name]
**Live website:** https://code4nature.streamlit.app/
**Source code:** https://github.com/Meghdatt07/Code4Nature
**License:** Creative Commons Attribution-NonCommercial 4.0 International (CC-BY-NC 4.0)

---

## Contents

1. Executive summary
2. Problem statement
3. Objectives
4. Solution overview
5. Features
6. System architecture
7. Repository structure
8. Data model
9. Methodology and calculations
10. Data sources and provenance
11. Assumptions and limitations
12. Deviations from the inception report
13. Testing and quality assurance
14. Sustainability and adoption
15. Key learnings and insights
16. Roadmap
17. Related submission documents
18. Licensing and attribution

---

## 1. Executive summary

Rice grown under continuous flooding is one of the largest sources of agricultural methane in India. Alternate Wetting and Drying (AWD) is a well-documented practice that cuts methane and irrigation water, but smallholders, farmer producer organisations (FPOs) and institutions lack a low-cost, transparent way to show that AWD is practised and to estimate its climate and economic value.

**Asterisk Climos** (proposed in the inception report as **CarbonAWD**) is an open digital Measurement, Reporting and Verification (MRV) prototype. A user maps a rice plot, models AWD water use, estimates methane and CO₂-equivalent (CO₂e) reductions, applies a carbon-price scenario and sees the value split between the farmer/FPO and the company or MRV partner. Every number carries its source and model version, and the system never presents its outputs as certified carbon credits.

## 2. Problem statement

- Methane (CH₄) has roughly 27 times the 100-year warming potential of CO₂ (IPCC AR6), and flooded paddies are a major source.
- AWD is a proven mitigation practice, but there is no accessible way for a smallholder, FPO or academic institution to verify at low cost whether it is followed.
- Existing carbon-MRV platforms are built for large project developers and are opaque about their assumptions, calculations and pricing.
- There is a gap for a transparent, small-scale MRV tool that shows every assumption it makes.

## 3. Objectives

| # | Objective (from the inception report) | Status in the final build |
|---|---|---|
| 1 | One complete, working data path from farm to indicative carbon value | **Achieved** with synthetic data: farm boundary → water → CO₂e → value → split → PDF report |
| 2 | Reusable, documented MRV calculation module with visible assumptions | **Achieved**: versioned models (`demo-v1.0`) behind interfaces, with unit tests |
| 3 | Integration with at least one real satellite source (Sentinel-1 via Sentinel Hub) | **Partly achieved**: implemented in `engine/` and the Streamlit app; the main backend uses a mock provider |
| 4 | Dashboard usable by a non-technical reviewer | **Achieved and extended**: multi-page website with farmer and company dashboards |
| 5 | Document every assumption, dependency and licence | **Achieved**: this document, the deployment guide, the README and in-app disclaimers |

## 4. Solution overview

The core is a four-step pipeline:

1. **Map the farm.** The user draws the plot boundary on a Leaflet + OpenStreetMap map. The backend computes the area in hectares and acres from the GeoJSON polygon using an equal-area projection.
2. **Model water.** Baseline (continuous flooding) irrigation is compared with AWD irrigation in litres per acre.
3. **Estimate CO₂e.** The practice change is converted into a methane / CO₂e reduction in tonnes.
4. **Value and split.** A user-chosen carbon price converts potential credits into USD and INR, split between farmer/FPO and company/MRV partner. The split must total 100%.

Results are stored with their inputs and model version, and can be downloaded as a PDF report marked “Prototype Simulation — Not a Carbon Credit Certificate”.

## 5. Features

**Website (Next.js)**

| Page | Purpose |
|---|---|
| Home | Project story, AWD explainer videos and entry points |
| Farm Simulator | Interactive map, polygon drawing, area calculation and simulation inputs |
| Digital MRV | Monitor, report, verify: SAR wetness evidence and AWD/MRV records |
| Carbon / Rice carbon credits | Carbon calculator, price scenarios and revenue split |
| Dashboard: farmer | Plot status, water saved and farmer-share income |
| Dashboard: company/admin | Portfolio totals across farms |
| Climate-smart rice | How AWD works: wet, drying, rewet |
| Technology | Satellite, model and measurement layers |
| Research and Insights | Sourced context from World Bank, FAO, ESA Copernicus and ICAR |
| About, Industry, Partner with us, News, Contact | Organisation and outreach pages |

**Backend (FastAPI)**

- REST API for farms, simulations, scenarios, carbon price, MRV records and PDF reports
- Automatic seeding of three scenarios, six synthetic farms and sample MRV records
- Interactive API documentation at `/docs`

**Transparency built in**

- Every response is labelled with `data_source` (for example `synthetic_demo`), `data_type` (`simulated`) and `model_version`.
- MRV records carry a `verification_status` of `DEMO DATA`.
- Disclaimers on pages and in the PDF report state that outputs are illustrative.

## 6. System architecture

```
                ┌──────────────────────────────┐
  Farmer / FPO  │  Next.js 15 · React 19 · TS  │
  Company / MRV │  Tailwind 4 · Leaflet + OSM  │
  Reviewer ───► │  Recharts · Framer Motion    │
                └──────────────┬───────────────┘
                               │ HTTPS / JSON
                ┌──────────────▼───────────────┐
                │  FastAPI backend             │
                │  farms · simulations ·       │
                │  scenarios · carbon · mrv ·  │
                │  reports (ReportLab PDF)     │
                │  Pydantic · SQLAlchemy ·     │
                │  Shapely                     │
                └───────┬──────────────┬───────┘
                        │              │
        ┌───────────────▼──┐   ┌───────▼──────────────────────┐
        │ PostgreSQL 16 +  │   │ Provider interfaces           │
        │ PostGIS 3.4      │   │ CarbonPrice · FX · Satellite ·│
        │ (SQLite fallback)│   │ Weather · Soil (demo today)   │
        └──────────────────┘   └───────────────────────────────┘

  Optional live-data layer: engine/ (FastAPI) and the Streamlit app
  → Sentinel Hub Statistics API (Sentinel-1 VV/VH) · open.er-api.com · CoinGecko · carbon.fyi
```

**Design principles**

- **Modular providers.** Carbon price, FX, satellite, weather and soil data are reached through abstract provider classes (`backend/app/services/providers.py`), so a demo source can be replaced by a live or licensed feed without changing the rest of the system.
- **Pluggable models.** Water, emission, carbon and revenue models implement base classes (`backend/app/services/models.py`), so a calibrated model can replace a demo model.
- **Server-side secrets.** Satellite and database credentials stay on the server and are never embedded in frontend code.

## 7. Repository structure

```
code4nature/
├── frontend/              Next.js web application (primary website)
│   ├── app/               Pages (simulator, mrv, dashboard, carbon, research, …)
│   ├── components/        Farm map, charts, calculators, shared UI
│   └── lib/               API client, calculation helpers, video catalogue
├── backend/               FastAPI service
│   ├── app/api/           Routers: farms, simulations, scenarios, carbon, mrv, reports
│   ├── app/services/      Water, emission, carbon and revenue models; providers
│   ├── app/models/        SQLAlchemy database models
│   ├── app/schemas/       Pydantic request/response schemas
│   ├── data/              synthetic_farms.csv, demo_parameters.json
│   ├── tests/             pytest unit tests
│   └── schema.sql         PostGIS extension setup
├── engine/                Optional live-data API (Sentinel Hub, FX, carbon price)
├── app/ + streamlit_app.py  Earlier Streamlit implementation (kept for compatibility)
├── website/               Static HTML site (GitHub Pages)
├── docs/                  Deployment guide and this document
├── docker-compose.yml     Database + backend + frontend
└── .github/workflows/     CI (tests and build) and Pages deployment
```

## 8. Data model

| Table | Key fields | Purpose |
|---|---|---|
| `farms` | name, geometry_geojson, latitude, longitude, area_hectares, area_acres, soil_type, season, crop_type | Rice plots and their boundaries |
| `simulations` | farm_id, model_version, baseline/project water and emission, emission_reduction, potential_credits, carbon_price, gross_value, farmer_share, company_share, input_json, output_json | Every simulation run with its full inputs and outputs |
| `scenarios` | name, baseline/project emission and water, carbon_price, shares | Presets: Conservative, Base Demo, Custom |
| `mrv_records` | farm_id, measurement_type, value, unit, source, timestamp, verification_status | Field evidence: water level, soil moisture, irrigation volume, methane |
| `farm_measurements` | water_level, soil_moisture, rainfall, irrigation_volume, methane_measurement, measurement_source | Time-series measurements for future sensors |
| `users` | name, email, role | Reserved for farmer/company/admin access control |

## 9. Methodology and calculations

All constants are named and adjustable. The reference model version is `demo-v1.0`.

| Step | Equation | Base demo value |
|---|---|---|
| Area | polygon area (equal-area projection) ÷ 10,000 m² | ha; acres = ha × 2.47105 |
| Water | saved = acres × (baseline − AWD) L/acre | 4,960,000 → 3,140,000 L/acre (−36.7%) |
| Emissions | reduction = ha × baseline tCO₂e/ha × reduction % | 6.0 → 3.5 tCO₂e/ha (−41.7%) |
| Credits | potential credits = max(0, reduction tCO₂e) | 1 credit = 1 tCO₂e (illustrative) |
| Value | gross = credits × price; INR = USD × FX | $20/t; FX 83 |
| Split | farmer = gross × farmer %; company = remainder; shares must total 100% | 60% / 40% |

**Safeguards in code:** water reduction is capped at 90%, emission reduction at 70%; farm area must be above zero; prices and baselines cannot be negative.

**Digital MRV reference:** the frontend's Digital MRV page uses 120 kg CH₄ abated per hectare per season × a GWP-100 of 28 = 3.36 tCO₂e per hectare per season.

**AWD field states** (Streamlit dashboard classifier, by water depth relative to the soil surface):

| State | Rule |
|---|---|
| WET | depth > 0 cm |
| DRYING | 0 cm ≥ depth ≥ −15 cm |
| REWETTING | depth < −15 cm (field has reached the re-irrigation threshold) |

**Satellite evidence** (`engine/` and Streamlit app): the Sentinel Hub Statistics API returns mean Sentinel-1 VV and VH backscatter for a small box around the plot over the last 18 days. VV in dB is converted to a 0–100 **relative wetness proxy**. This is not absolute soil moisture; that requires field calibration.

### Worked example: base demo, 10 ha, one season

| Output | Value |
|---|---|
| Baseline emissions | 60 tCO₂e |
| Project emissions | 35 tCO₂e |
| Reduction / potential credits | 25 tCO₂e / 25 |
| Water saved | 36.7% (about 45 million litres) |
| Gross value at $20/t | $500 (₹41,500) |
| Farmer/FPO share (60%) | $300 (₹24,900) |
| Company/MRV share (40%) | $200 (₹16,600) |

## 10. Data sources and provenance

| Data | Source | Status |
|---|---|---|
| Farm boundaries | User-drawn on OpenStreetMap; six seeded synthetic farms (Telangana, West Bengal, Punjab, Haryana, Odisha) | Synthetic / user input |
| Water and emission baselines | `backend/data/demo_parameters.json`, `synthetic_farms.csv` | Synthetic demo |
| MRV records | Seeded rows labelled `DEMO DATA` | Synthetic demo |
| Carbon price | User-set scenario ($15 conservative, $20 base); optional CoinGecko / carbon.fyi reference in `engine/` and Streamlit | Indicative, not a market quote |
| USD→INR | 83 by default; optional live rate from open.er-api.com | Demo / live (optional) |
| Satellite | Sentinel-1 GRD via Sentinel Hub (optional; simulator fallback) | Live when credentials are set |
| Research context | World Bank, FAO AGRIS, ESA Copernicus, ICAR (linked on the Insights page) | Paraphrased, cited |

## 11. Assumptions and limitations

- All model outputs are deterministic demonstration equations on synthetic inputs, not measured agronomic results.
- Potential credits are **not** certified credits. Real issuance needs a recognised methodology, project-specific baselines, field measurement, validation and third-party verification.
- The emission reduction is a fixed percentage of a baseline; it does not yet respond to soil, season, rainfall or measured water levels.
- The satellite wetness proxy is relative and uncalibrated.
- Two methane conventions are present (GWP 27 in the inception report, 28 in the code) and should be harmonised.
- There is no user authentication or access control yet; the `users` table and `SECRET_KEY` are reserved for it.
- No hardware sensors are connected; the database schema is ready for them.

## 12. Deviations from the inception report

| Area | Inception report | Final build | Reason |
|---|---|---|---|
| Name | CarbonAWD | Asterisk Climos | Broader platform identity for farmers and companies |
| Frontend | HTML, Tailwind, Chart.js, Leaflet, Font Awesome | Next.js 15, React 19, TypeScript, Tailwind 4, Recharts, lucide-react, Leaflet | Component framework needed to grow from one dashboard into a multi-page platform |
| Backend | Python, FastAPI, SQLAlchemy | Same core, plus Pydantic schemas, Shapely and ReportLab PDF reports | Typed API, geometry handling and downloadable reports |
| Database | SQLite, then Supabase/PostgreSQL | PostgreSQL 16 + PostGIS, SQLite fallback | Native storage of farm boundaries |
| Satellite | Sentinel Hub Process API | Sentinel Hub Statistics API in `engine/` and Streamlit; mock provider in main backend | Statistics API returns field-level means directly; main-backend integration still pending |
| Telemetry | Sensor simulator, ESP32 device later | MRV records table with labelled demo rows; no hardware | Prioritised one working software path |
| MRV logic | Per-reading WET/DRYING/REWETTING drives CH₄ reduction | Versioned scenario models; classifier kept in Streamlit | Scenario models are simpler to audit and test |
| Methane factor | GWP-100 = 27 (AR6) | GWP-100 = 28 | To be harmonised |
| Prices | CoinGecko token proxy, open.er-api FX | User-set price scenarios; live feeds optional | Free “live” carbon prices were unreliable proxies |
| Delivery | Not specified | Live on Streamlit Community Cloud (https://code4nature.streamlit.app/); Docker Compose, GitHub Actions CI, GitHub Pages | Free public hosting plus reproducible self-hosting |

## 13. Testing and quality assurance

- **Backend unit tests** (`backend/tests/test_models.py`): the base demo case (60 → 35 tCO₂e, 25 credits, $300 farmer revenue), rejection of shares that do not total 100%, and rejection of zero farm area.
- **Continuous integration** (`.github/workflows/ci.yml`): on every push and pull request to `main`, runs the backend tests, the frontend TypeScript check and the production Next.js build.
- **Input validation:** Pydantic schemas bound every simulation input (for example crop duration 60–240 days, reduction 0–70%, shares 0–100%).

## 14. Sustainability and adoption

- **Open licence:** CC-BY-NC 4.0 lets FES, India Observatory and other institutions host, adapt and extend the tool.
- **One-command deployment:** `docker compose up --build` starts the full stack (see `docs/DEPLOYMENT_GUIDE.md`).
- **Swappable components:** price, FX, satellite, weather and soil providers, and the models, sit behind interfaces, so production-grade sources replace demo ones without a rewrite.
- **Reproducibility:** every simulation stores its inputs, outputs and model version.
- **Adoption path for FPOs:** map member plots → record AWD practice → generate reports for MRV partners → add sensors and satellite checks as they mature.
- **Hardware path:** the `mrv_records` and `farm_measurements` tables already hold water level, soil moisture, rainfall and irrigation volume for future ESP32 water-level sensors.
- **Documentation for successors:** README, this document and the deployment guide are written for a team that did not build the prototype.

## 15. Key learnings and insights

*[Team to review and personalise.]*

**Learnings**

1. **Trust is a design problem.** Labelling the source of every number took as much work as the maths.
2. **Satellites give evidence, not answers.** SAR backscatter shows relative wetness; absolute moisture needs field calibration.
3. **Carbon prices are hard to source.** With no clean free API, proxies can mislead; an explicit price scenario is more honest.
4. **Constants carry real weight.** The GWP value, baselines and caps change the credit count, so each must be stated.
5. **Interfaces first, data later.** Provider classes let us ship a working demo while live integrations matured.
6. **Full-stack, end to end.** Next.js, FastAPI, PostGIS, Docker and CI, learned by shipping them together.

**Insights**

- AWD is powerful, but methane MRV needs more than a wet/dry label: emissions depend on soil, season, baseline and how consistently the practice is followed.
- Scale sets the value: a 10 ha farm earns about $500 a season at $20/t, so aggregation through FPOs is essential.
- Water sells the practice: farmers see water and pumping savings first; methane value is the market's story.
- Layered evidence wins: field records, satellite wetness and a transparent model each cover gaps in the others.

## 16. Roadmap

| Phase | Work |
|---|---|
| Next | Move Sentinel-1 into the main backend's satellite provider; adopt one GWP value and one emission method across frontend and backend; add login and role-based access control |
| Then | ESP32 water-level sensor with an ingest API; pilot on real plots with an FPO; calibrate water and emission models on field data |
| Later | Align with a recognised rice-methane methodology; third-party verification; licensed carbon-price feed; multi-season farm history |

## 17. Related submission documents

| Item | Location |
|---|---|
| Live website | https://code4nature.streamlit.app/ |
| Presentation | Final presentation deck (link / exported PDF or PPTX in the submission) |
| Source code | This repository |
| Deployment guide | `docs/DEPLOYMENT_GUIDE.md` |
| Inception report | `CarbonAWD_Inception_Report.docx` (Phase 1 submission) |
| Project documentation | `docs/PROJECT_DOCUMENTATION.md` (this file) |

## 18. Licensing and attribution

This project, including source code, documentation and original datasets, is released under the Creative Commons Attribution-NonCommercial 4.0 International License (CC-BY-NC 4.0).

Third-party components: Next.js, React, FastAPI, SQLAlchemy, Pydantic, Leaflet, Recharts, Tailwind CSS (MIT or similar permissive licences); PostgreSQL (PostgreSQL License); PostGIS (GPL-2.0); OpenStreetMap data (ODbL, attributed on the map); Copernicus Sentinel-1 data via Sentinel Hub (Copernicus open-data terms). No proprietary code is included.
