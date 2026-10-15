# Asterisk Climos (CarbonAWD) — Deployment Guide

Code4Nature Challenge 2026 · Final submission
License: CC-BY-NC 4.0

This guide explains how to run and deploy the Asterisk Climos rice-MRV prototype from this repository. It covers local development, a one-command Docker deployment, cloud hosting options, configuration and troubleshooting.

> **Live deployment:** https://code4nature.streamlit.app/ (Streamlit Community Cloud, deployed from this repository's `streamlit_app.py`).

> **Scientific limitation.** Every output of this prototype is a deterministic demonstration calculation on synthetic data. It must not be presented as measured agronomic results or certified carbon credits.

---

## 1. What gets deployed

The repository contains four runnable parts. Only the first three are needed for the main application.

| Component | Folder | Technology | Default port | Required |
|---|---|---|---|---|
| Web frontend | `frontend/` | Next.js 15, React 19, TypeScript, Tailwind CSS 4, Leaflet, Recharts | 3000 | Yes |
| API backend | `backend/` | Python 3.12, FastAPI, SQLAlchemy, Pydantic, Shapely, ReportLab | 8000 | Yes |
| Database | via Docker | PostgreSQL 16 + PostGIS 3.4 (SQLite fallback for local use) | 5432 | Recommended |
| Live-data service | `engine/` | FastAPI: Sentinel Hub (Sentinel-1), FX rate and carbon-price lookups | 8000 (set another port) | Optional |
| Streamlit app | `streamlit_app.py`, `app/` | Streamlit, Folium | 8501 | **Live at https://code4nature.streamlit.app/** |
| Static site | `website/` | Plain HTML/CSS/JS, published to GitHub Pages by CI | — | Optional |

```
Browser ──► Next.js frontend ──► FastAPI backend ──► PostgreSQL + PostGIS
                                     │
                                     └── provider interfaces (carbon price, FX,
                                         satellite, weather, soil) – demo values today

Optional: engine/ API or Streamlit app ──► Sentinel Hub · open.er-api.com · CoinGecko · carbon.fyi
```

---

## 2. Prerequisites

| Tool | Version | Needed for |
|---|---|---|
| Git | any recent | Cloning the repository |
| Docker + Docker Compose v2 | Docker 24+ | Option A (recommended) |
| Python | 3.12 (3.11 works for Streamlit) | Option B: backend, engine, Streamlit |
| Node.js + npm | Node 22 LTS | Option B: frontend |
| PostgreSQL + PostGIS | 16 / 3.4 | Option B with a real database (optional) |

Hardware: any machine with 2 CPU cores, 4 GB RAM and 5 GB free disk is enough for the demo.

Clone the repository:

```bash
git clone <repository-url> code4nature
cd code4nature
```

---

## 3. Configuration

Copy the example environment file and adjust the values:

```bash
cp .env.example .env
```

| Variable | Used by | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | frontend | `http://localhost:8000` | Public URL of the FastAPI backend. Baked into the frontend **at build time**. |
| `DATABASE_URL` | backend | `sqlite:///./asterisk_climos.db` | SQLAlchemy URL, for example `postgresql+psycopg://climos:climos@localhost:5432/climos`. |
| `CORS_ORIGINS` | backend | `http://localhost:3000` | Comma-separated list of origins allowed to call the API. Must include the frontend URL. |
| `SECRET_KEY` | backend | `change-me` | Reserved for future authentication. Always change it in production. |
| `DEMO_FX_USD_INR` | backend | `83` | Demo USD→INR exchange rate. |
| `SH_CLIENT_ID`, `SH_CLIENT_SECRET` | engine, Streamlit | empty | Sentinel Hub OAuth client. Without them, satellite data falls back to the simulator. |

**Security rules**

- Never commit `.env` or any real credentials.
- Keep Sentinel Hub and database credentials on the server only; never put them in `NEXT_PUBLIC_*` variables, because those are visible in the browser.
- Replace the default database password (`climos`) for any public deployment.

---

## 4. Option A — Docker Compose (recommended)

One command starts the database, the API and the website:

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Website | http://localhost:3000 |
| API | http://localhost:8000 |
| Interactive API docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |
| PostgreSQL | `localhost:5432` (user, password and database: `climos`) |

On first start the backend creates its tables and seeds demo data: three scenarios (Conservative, Base Demo, Custom), six synthetic farms across India and sample MRV records labelled `DEMO DATA`.

Useful commands:

```bash
docker compose up -d --build      # run in the background
docker compose logs -f backend    # follow backend logs
docker compose down               # stop (keeps the database volume)
docker compose down -v            # stop and delete all data
```

The PostGIS extension can be enabled explicitly with `backend/schema.sql`:

```bash
docker compose exec db psql -U climos -d climos -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

---

## 5. Option B — Manual local setup

### 5.1 Backend (FastAPI)

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Optional: point at PostgreSQL instead of the SQLite default
# export DATABASE_URL=postgresql+psycopg://climos:climos@localhost:5432/climos
uvicorn app.main:app --reload --port 8000
```

Check it at http://localhost:8000/health. The expected response is `{"status":"ok","mode":"prototype","model_version":"demo-v1.0"}`.

### 5.2 Frontend (Next.js)

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local
npm run dev
```

Open http://localhost:3000. Because `next.config.ts` sets `basePath: '/Code4Nature'`, pages may be served under http://localhost:3000/Code4Nature/.

### 5.3 Optional: live-data engine

```bash
pip install fastapi uvicorn requests
export SH_CLIENT_ID=...  SH_CLIENT_SECRET=...
uvicorn engine.main:app --port 8001
```

Endpoints: `/health`, `/api/sar?lat=..&lon=..` (Sentinel-1 VV/VH and a relative wetness proxy) and `/api/market` (FX and carbon-price reference).

### 5.4 Streamlit app (the live website)

```bash
pip install -r requirements.txt     # from the repository root
streamlit run streamlit_app.py      # http://localhost:8501
```

---

## 6. Running the tests

```bash
# Backend unit tests (also run by GitHub Actions)
PYTHONPATH=backend pytest -q backend/tests

# Frontend type-check and production build
cd frontend && npm run lint && npm run build
```

The backend tests check the reference demo case: a 10 ha farm with a 6.0 tCO₂e/ha baseline and a 41.67% reduction must give 25 tCO₂e, 25 potential credits and $300 farmer revenue at $20/t with a 60/40 split. They also check share and area validation.

---

## 7. Production deployment

### 7.0 Current live deployment: Streamlit Community Cloud

The website is live at **https://code4nature.streamlit.app/**.

To redeploy it, or to deploy your own copy:

1. Push the repository to GitHub.
2. Sign in at https://share.streamlit.io with GitHub and choose **Create app → Deploy a public app from GitHub**.
3. Select the repository, the `main` branch and the main file `streamlit_app.py`. Streamlit installs the root `requirements.txt` automatically.
4. Optional: under **Advanced settings → Secrets** (or later in **App settings → Secrets**), add the Sentinel Hub credentials so the Digital MRV page uses live Sentinel-1 data instead of the simulator:

   ```toml
   SH_CLIENT_ID = "your-client-id"
   SH_CLIENT_SECRET = "your-client-secret"
   ```

5. Choose the app URL (for example `code4nature`) and click **Deploy**. Every push to `main` redeploys the app automatically.

The sections below cover deploying the full-stack version (Next.js + FastAPI + PostGIS) on your own infrastructure.

### 7.1 Frontend build mode

`frontend/next.config.ts` currently sets `output: 'export'` and `basePath: '/Code4Nature'`. That produces a **static site** in `frontend/out/`, suitable for GitHub Pages, GitLab Pages or any static host. Choose one of these:

- **Static hosting (current setting).** Build with `NEXT_PUBLIC_BACKEND_URL` set to the public API URL, then publish `frontend/out/`. Keep `basePath` matching the URL path the site is served under, or remove it when the site is served from the root of a domain.
- **Node server (Docker, Vercel, Render).** Remove `output: 'export'` from `next.config.ts` so that `npm start` (used in `frontend/Dockerfile`) can serve the app. `next start` does not serve a static export.

### 7.2 Recommended hosting combinations

| Layer | Option 1 (managed) | Option 2 (single VM) |
|---|---|---|
| Frontend | Vercel, Netlify, or GitLab/GitHub Pages (static export) | Docker container behind Nginx |
| Backend | Render, Railway or Fly.io (Docker, from `backend/Dockerfile`) | Docker container behind Nginx |
| Database | Managed PostgreSQL with PostGIS (e.g. Supabase, Neon, AWS RDS) | `postgis/postgis:16-3.4` container with a persistent volume |

Steps for any combination:

1. Create the PostgreSQL database and enable PostGIS (`CREATE EXTENSION IF NOT EXISTS postgis;`).
2. Deploy the backend with `DATABASE_URL`, `CORS_ORIGINS` (the frontend's public URL) and `SECRET_KEY` set. Confirm `/health` responds.
3. Build the frontend with `NEXT_PUBLIC_BACKEND_URL` set to the backend's public HTTPS URL, then deploy it.
4. Open the site, run a simulation and download the PDF report to confirm the full path works.

### 7.3 Single VM with Docker Compose and Nginx

On an Ubuntu 22.04+ server:

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2 nginx certbot python3-certbot-nginx
git clone <repository-url> /opt/climos && cd /opt/climos
cp .env.example .env    # set strong passwords, SECRET_KEY, public URLs
# Edit docker-compose.yml: NEXT_PUBLIC_BACKEND_URL=https://api.example.org,
# change POSTGRES_PASSWORD and add CORS_ORIGINS=https://climos.example.org to the backend
sudo docker compose up -d --build
```

Example Nginx reverse proxy (`/etc/nginx/sites-available/climos`):

```nginx
server {
    server_name climos.example.org;
    location / { proxy_pass http://127.0.0.1:3000; proxy_set_header Host $host; }
}
server {
    server_name api.example.org;
    location / { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host;
                 proxy_set_header X-Forwarded-Proto $scheme; }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/climos /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d climos.example.org -d api.example.org   # HTTPS
```

For production, do not publish port 5432 to the internet: remove `ports: ["5432:5432"]` from the `db` service.

### 7.4 GitLab CI/CD (FES GitLab)

The repository ships GitHub Actions workflows (`.github/workflows/`). An equivalent `.gitlab-ci.yml` for the FES GitLab instance:

```yaml
stages: [test, build]

backend-tests:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r backend/requirements.txt
    - PYTHONPATH=backend pytest -q backend/tests

frontend-build:
  stage: build
  image: node:22
  script:
    - cd frontend
    - npm install
    - npm run lint
    - npm run build
  artifacts:
    paths: [frontend/out]
```

To publish the static frontend with GitLab Pages, add a `pages` job that copies `frontend/out` into `public/`, and set `basePath` to the project's Pages path.

---

## 8. API reference (summary)

Full interactive documentation is served at `/docs`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service status and model version |
| GET, POST | `/api/farms` | List farms / create a farm from a GeoJSON polygon (area computed automatically) |
| GET | `/api/farms/{id}` | One farm |
| POST | `/api/simulations` | Run and store a simulation for a farm |
| GET | `/api/simulations/{id}` | Fetch a stored simulation |
| GET | `/api/scenarios` | List preset scenarios |
| POST | `/api/scenarios/calculate` | Stateless scenario calculation |
| GET | `/api/scenarios/dashboard/admin` | Portfolio totals from the synthetic farm dataset |
| GET, POST | `/api/carbon/price` | Read / set the demo carbon price and FX rate |
| GET | `/api/mrv/{farm_id}` | MRV records for a farm |
| GET | `/api/reports/simulations/{id}.pdf` | PDF simulation report (marked “not a carbon credit certificate”) |

---

## 9. Operations

- **Backups:** `docker compose exec db pg_dump -U climos climos > backup_$(date +%F).sql`
- **Restore:** `cat backup.sql | docker compose exec -T db psql -U climos -d climos`
- **Updates:** `git pull && docker compose up -d --build`
- **Logs:** `docker compose logs -f <service>`
- **Health monitoring:** poll `GET /health` from an uptime monitor.

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Website loads but simulator shows network errors | Frontend built with the wrong `NEXT_PUBLIC_BACKEND_URL`, or CORS blocks it | Rebuild the frontend with the correct URL; add the frontend origin to `CORS_ORIGINS` |
| Frontend container exits on `npm start` | `output: 'export'` is set in `next.config.ts` | Serve `frontend/out/` statically, or remove `output: 'export'` (section 7.1) |
| Pages return 404 at `/` | `basePath: '/Code4Nature'` is set | Open `/Code4Nature/`, or remove/adjust `basePath` |
| Backend cannot connect to the database | `DATABASE_URL` wrong, or db not ready yet | Check the URL; restart the backend after the db is up (`docker compose restart backend`) |
| `ModuleNotFoundError: pyproj` when creating a farm | Farm area projection uses `pyproj` | `pip install pyproj` (and add it to `backend/requirements.txt`) |
| Satellite panel says “simulator” | No Sentinel Hub credentials | Set `SH_CLIENT_ID` / `SH_CLIENT_SECRET` on the server |
| Map tiles do not load | Network blocks `tile.openstreetmap.org` | Allow outbound HTTPS to OpenStreetMap tile servers |

---

## 11. Third-party services and licences

| Service / library | Purpose | Terms |
|---|---|---|
| OpenStreetMap tiles via Leaflet | Base map | ODbL; attribution shown on the map |
| Sentinel Hub / Copernicus Sentinel-1 | SAR backscatter (optional) | Copernicus open data terms, Sentinel Hub ToS |
| open.er-api.com | USD→INR rate (optional) | Public API terms |
| CoinGecko, carbon.fyi | Illustrative carbon-price reference (optional) | Public terms of use |
| Next.js, React, FastAPI, SQLAlchemy, Leaflet, Recharts | Application stack | MIT / BSD-style open-source licences |
| PostgreSQL, PostGIS | Database | PostgreSQL License / GPL-2.0 |
