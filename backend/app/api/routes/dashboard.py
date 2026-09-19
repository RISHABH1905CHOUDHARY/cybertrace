"""Executive Dashboard API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardResponse, summary="Get combined executive dashboard overview")
async def get_dashboard_overview(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Combined endpoint delivering all data required for the main dashboard:
    - Key performance indicators
    - Categorical fraud distribution
    - Top affected districts
    - Monthly time-series trends
    - High-risk vulnerable ATM terminals
    """
    return await AnalyticsService.get_full_dashboard(db)
