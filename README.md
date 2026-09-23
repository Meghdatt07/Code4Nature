# Code4Nature — CarbonAWD / Asterisk Climos MVP

The repository now contains the full-stack Asterisk Climos MVP supplied for Code4Nature: a Next.js frontend, FastAPI simulation backend, optional PostgreSQL/PostGIS persistence, interactive farm mapping, transparent emissions/carbon calculations and demo report generation.

## Primary web application

Frontend:
\`frontend/\`

Run locally:
\`cd frontend && npm install && npm run dev\`

Open:
\`http://localhost:3000\`

Backend:
\`backend/\`

Run locally:
\`cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000\`

For deployment, configure NEXT_PUBLIC_BACKEND_URL on the frontend to point to the deployed FastAPI service.

The main website includes:
- farm-area simulation
- interactive Leaflet farm map
- water-use optimisation scenario
- methane/CO2e simulation
- potential carbon-credit quantity
- carbon price scenario
- farmer/FPO and company/MRV revenue split
- Digital MRV section
- farmer and company dashboard pages
- research/context page
- PDF demo report endpoint
- provenance and synthetic-data disclaimers

## Docker

Run:
\`docker compose up --build\`

This starts the PostgreSQL/PostGIS database, FastAPI backend and Next.js frontend.

## GitHub automation

GitHub Actions now validates the backend tests and runs the production Next.js build.

## Streamlit compatibility

The previous Streamlit implementation remains in the repository for compatibility. The Next.js application is the primary website for this uploaded MVP.

## Scientific limitation

All model outputs supplied in the MVP are deterministic demonstration equations. They should not be represented as measured agronomic results or certified carbon credits. Project-specific methodology, MRV, validation, verification and evidence are required for real credit issuance.
