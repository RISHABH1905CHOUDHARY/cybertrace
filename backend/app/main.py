"""CrimeTrace AI Backend - FastAPI Main Application Entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.router import api_router
from app.core.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown routines."""
    # Startup: initialize database tables
    try:
        await init_db()
    except Exception as e:
        print(f"Warning: Database initialization error (will retry or use migrations): {e}")

    yield

    # Shutdown routines can be added here if needed


tags_metadata = [
    {"name": "Authentication", "description": "JWT authentication, login, refresh, and profile endpoints."},
    {"name": "Complaints", "description": "Cybercrime complaint management, search, and cash-out forecasting."},
    {"name": "ATMs", "description": "ATM registry, proximity searches, and risk scoring."},
    {"name": "Transactions", "description": "Cash withdrawal tracking, fraud tagging, and complaint linkages."},
    {"name": "Heatmap & GIS Layers", "description": "Spatial intensity maps and GeoJSON feature collections."},
    {"name": "Analytics", "description": "Crime trends, categorical distribution, and district aggregations."},
    {"name": "Dashboard", "description": "Executive dashboard summary overview."},
    {"name": "Locations & GIS", "description": "Jurisdictional boundaries, police stations, and persistent hotspots."},
    {"name": "Users", "description": "User account administration and RBAC role assignment."},
]

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
**CrimeTrace AI** is a predictive analytics framework for cybercrime complaints
and forecasting likely cash withdrawal locations.

### Key Capabilities:
* **Cybercrime Complaint Management**: Multi-filter tracking across Indian districts and fraud categories.
* **ATM & Location Network**: Spatial indexing and proximity search for ATM terminals.
* **Cash-Out Forecasting Engine**: Ranks nearby ATMs by probability of fraudulent withdrawals post-incident.
* **GIS Heatmaps & GeoJSON**: Renders weighted crime densities and boundaries.
* **Role-Based Access Control**: Strict segregation for Admin, Analyst, Investigator, and Viewer.
* **Future ML Plug-and-Play**: Standardized schemas and protocols ready for machine learning model integration.
    """,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handlers
@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database conflict: duplicate unique entry or foreign key violation."},
    )


# Health & Metadata Routes
@app.get("/", tags=["System"], summary="API Root Status")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs_url": "/docs",
    }


@app.get("/health", tags=["System"], summary="Health Check")
async def health():
    return {
        "status": "healthy",
        "postgis_enabled": settings.USE_POSTGIS,
        "ml_stub_mode": settings.ML_SERVICE_STUB_MODE,
    }


# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)
