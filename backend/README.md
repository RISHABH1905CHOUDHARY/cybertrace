# CrimeTrace AI — Backend

> **Predictive Analytics Framework for Cybercrime Complaints and Forecasting Likely Cash Withdrawal Locations**

CrimeTrace AI is a high-performance, modular backend built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL / PostGIS**, and **Pydantic v2**. It bridges cybercrime intelligence reported through national portals/desks with predictive spatial forecasting to identify high-probability ATM terminals targeted for illicit cash withdrawals.

---

## 1. Key Capabilities

* **Cybercrime Complaint Management**: End-to-end complaint lifecycle tracking across Indian states/districts with multi-dimensional filtering (fraud type, date intervals, financial impact).
* **ATM Spatial Network**: Geospatial indexing, radius queries, and proximity detection using PostGIS and Haversine spatial calculations.
* **Cash-Out Forecasting Engine**: Heuristic and probabilistic ranking of nearby ATM terminals prone to cash withdrawals post-incident.
* **GIS Heatmap & GeoJSON Services**: Ready-to-render weighted intensity points and standard GeoJSON FeatureCollections for frontend mapping (Leaflet, Mapbox GL, OpenLayers).
* **Role-Based Access Control (RBAC)**: JWT authentication with tiered roles:
  * `admin`: Complete system administration and user management.
  * `analyst`: Data exploration, complaint ingestion, and spatial analytics.
  * `investigator`: Complaint status progression and transaction audit linking.
  * `viewer`: Read-only reporting and KPI dashboard access.
* **ML Plug-and-Play Foundation**: Abstract predictor interfaces (`BasePredictor`) and schemas enabling data scientists to plug in trained models (CatBoost, XGBoost, PyTorch) without modifying route logic.

---

## 2. Technology Stack

* **Language**: Python 3.12+ (tested up to 3.13)
* **Framework**: FastAPI, Uvicorn
* **ORM & Database**: SQLAlchemy 2.0 Async, PostgreSQL with PostGIS, asyncpg / psycopg2
* **Migrations**: Alembic
* **Validation & Settings**: Pydantic v2, Pydantic Settings
* **Security & Auth**: PyJWT, Bcrypt
* **Spatial & GIS**: GeoAlchemy2, Shapely
* **Testing**: Pytest, Pytest-Asyncio, HTTPX

---

## 3. Project Architecture

```
backend/
├── app/
│   ├── main.py                 # FastAPI application factory & lifespan
│   │
│   ├── core/
│   ├── config.py           # Pydantic Settings & environment variables
│   ├── security.py         # Bcrypt password hashing & JWT tokens
│   └── dependencies.py     # DB session injection & RBAC role checkers
│   │
│   ├── database/
│   ├── base.py             # Declarative Base & timestamp mixins
│   ├── database.py         # Async engine & session factory
│   └── session.py          # Session dependency & table initialization
│   │
│   ├── models/                 # SQLAlchemy ORM Models
│   ├── user.py             # User & RBAC roles
│   ├── complaint.py        # Cybercrime complaints
│   ├── atm.py              # ATM terminals & spatial coordinates
│   ├── transaction.py      # Cash withdrawals & fraud linkages
│   ├── location.py         # Hotspots & jurisdictional boundaries
│   └── audit_log.py        # Immutable security audit trail
│   │
│   ├── schemas/                # Pydantic v2 Data Transfer Objects (DTOs)
│   ├── auth.py, user.py, complaint.py, atm.py, transaction.py, location.py, dashboard.py
│   │
│   ├── api/                    # API Route Handlers
│   ├── router.py           # Central API v1 router aggregator
│   └── routes/
│       ├── auth.py, users.py, complaints.py, atms.py, transactions.py,
│       ├── locations.py, analytics.py, heatmap.py, dashboard.py
│   │
│   ├── services/               # Business Logic & Algorithms
│   ├── complaint_service.py
│   ├── atm_service.py
│   ├── transaction_service.py
│   ├── geospatial_service.py
│   ├── heatmap_service.py
│   ├── risk_service.py     # Multi-factor ATM risk & withdrawal forecasting
│   └── analytics_service.py
│   │
│   ├── utils/                  # Reusable Helpers
│   ├── geo.py              # Haversine formula, bounding boxes, GeoJSON
│   ├── pagination.py       # Standard PageResponse generic wrapper
│   └── validators.py       # ID generators & PII data masking
│   │
│   └── ml/                     # Machine Learning Contracts
│       ├── base.py             # BasePredictor protocol interface
│       ├── schemas.py          # ML feature vectors & inference response schemas
│       ├── stub_predictor.py   # Heuristic baseline predictor
│       └── README.md           # Model deployment instructions
│
├── alembic/                    # Database migrations
├── scripts/
│   └── seed_database.py        # Realistic database seeder
├── tests/                      # Pytest asynchronous test suite
├── .env.example                # Environment configuration template
├── Dockerfile                  # Multi-stage container build
├── docker-compose.yml          # PostGIS + Backend services orchestration
└── requirements.txt
```

---

## 4. Quick Start Guide

### Prerequisites
* Python 3.12+
* Docker & Docker Compose (optional for local containerized run)

### Option A: Local Run (Zero-Configuration SQLite Fallback)

1. Clone or navigate to the backend workspace:
   ```bash
   cd crimetrace_ai/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Populate realistic seed data (users, ATMs, complaints, withdrawals):
   ```bash
   python scripts/seed_database.py
   ```

5. Start the API server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. Open interactive API docs:
   * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   * ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Docker Compose (PostgreSQL + PostGIS)

Run the full stack with PostGIS 16 and geospatial extensions:

```bash
docker compose up --build
```

The database container includes the `postgis/postgis:16-3.4` image with spatial indexing enabled.

---

## 5. Default Credentials

The seed script creates initial accounts for testing:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@crimetrace.ai` | `Admin@123456` |
| **Analyst** | `analyst@crimetrace.ai` | `Analyst@123456` |
| **Investigator** | `investigator@crimetrace.ai` | `Invest@123456` |
| **Viewer** | `viewer@crimetrace.ai` | `Viewer@123456` |

---

## 6. Core API Endpoints

### Authentication & Users
* `POST /api/v1/auth/login` — Authenticate and receive JWT Bearer tokens
* `POST /api/v1/auth/refresh` — Refresh expired access tokens
* `GET /api/v1/auth/me` — Retrieve profile of authenticated user
* `GET /api/v1/users` — Paginated user directory (Admin only)

### Cybercrime Complaints
* `GET /api/v1/complaints` — Filter complaints by fraud type, status, state, district, amount range
* `POST /api/v1/complaints` — File a new cybercrime incident
* `GET /api/v1/complaints/{id}` — Retrieve complaint details
* `PATCH /api/v1/complaints/{id}/status` — Progress investigation status
* `GET /api/v1/complaints/{id}/forecast-withdrawals` — **Forecast likely cash withdrawal ATMs**

### ATMs & Spatial Monitoring
* `GET /api/v1/atms` — List and filter ATM terminals
* `POST /api/v1/atms` — Register an ATM terminal
* `GET /api/v1/atms/nearby` — Proximity search within radius `radius_km`
* `GET /api/v1/atms/{id}/risk` — Calculate multi-factor cybercrime risk score

### Transactions & Cash Withdrawals
* `GET /api/v1/transactions` — Ingested withdrawal records (filter by `is_fraud`)
* `POST /api/v1/transactions` — Record new withdrawal
* `PATCH /api/v1/transactions/{id}/link-complaint` — Link withdrawal to investigated complaint

### GIS Heatmaps & Visualizations
* `GET /api/v1/heatmap/points` — Weighted coordinate intensity points for heat layers
* `GET /api/v1/heatmap/geojson` — Standard GeoJSON FeatureCollection
* `GET /api/v1/heatmap/withdrawals` — Fraudulent cash-out cluster points

### Executive Dashboard & Analytics
* `GET /api/v1/dashboard/overview` — Aggregated KPIs, trend series, top districts, and hotspots
* `GET /api/v1/analytics/kpis` — Real-time performance metrics
* `GET /api/v1/analytics/fraud-distribution` — Relative incidence per fraud type
* `GET /api/v1/analytics/districts` — Financial losses aggregated by district

---

## 7. Running Tests

Execute the automated test suite covering authentication, RBAC, spatial proximity, analytics, and risk forecasting:

```bash
pytest -v
```
