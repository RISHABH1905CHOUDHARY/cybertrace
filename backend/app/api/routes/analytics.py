"""Analytics and statistical aggregation API routes."""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import (
    ATMHotspotItem,
    DashboardSummaryKPIs,
    DistrictLossItem,
    FraudDistributionItem,
    TimeSeriesDataPoint,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/kpis", response_model=DashboardSummaryKPIs, summary="Get summary analytics KPIs")
async def get_kpis(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve key metrics: total complaints, financial loss, monitored ATMs, resolution rates."""
    return await AnalyticsService.get_dashboard_kpis(db)


@router.get("/fraud-distribution", response_model=List[FraudDistributionItem], summary="Get cybercrime distribution by fraud category")
async def get_fraud_distribution(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Analyze proportional incidence and financial impact per fraud category."""
    return await AnalyticsService.get_fraud_distribution(db)


@router.get("/districts", response_model=List[DistrictLossItem], summary="Get district crime and financial loss statistics")
async def get_district_stats(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve top affected districts ranked by cumulative monetary losses."""
    return await AnalyticsService.get_top_affected_districts(db, limit=limit)


@router.get("/trends", response_model=List[TimeSeriesDataPoint], summary="Get monthly cybercrime trend time series")
async def get_trends(
    limit: int = Query(12, ge=1, le=36),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve historical monthly complaint counts and financial volumes."""
    return await AnalyticsService.get_monthly_trend(db, limit=limit)


@router.get("/vulnerable-atms", response_model=List[ATMHotspotItem], summary="Get top vulnerable ATM hotspots")
async def get_vulnerable_atms(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve high-risk ATM terminals prone to illicit cash-out operations."""
    return await AnalyticsService.get_top_vulnerable_atms(db, limit=limit)
