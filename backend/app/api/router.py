"""Main API v1 Router assembling all domain route modules."""

from fastapi import APIRouter
from app.api.routes import (
    analytics,
    atms,
    auth,
    complaints,
    dashboard,
    heatmap,
    locations,
    transactions,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(complaints.router)
api_router.include_router(atms.router)
api_router.include_router(transactions.router)
api_router.include_router(locations.router)
api_router.include_router(analytics.router)
api_router.include_router(heatmap.router)
api_router.include_router(dashboard.router)
