"""API routes export package."""

from app.api.routes import (
    auth,
    users,
    complaints,
    atms,
    transactions,
    locations,
    analytics,
    heatmap,
    dashboard,
)

__all__ = [
    "auth",
    "users",
    "complaints",
    "atms",
    "transactions",
    "locations",
    "analytics",
    "heatmap",
    "dashboard",
]
