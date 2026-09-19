"""Heatmap generation API routes."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import HeatmapPoint
from app.services.heatmap_service import HeatmapService

router = APIRouter(prefix="/heatmap", tags=["Heatmap & GIS Layers"])


@router.get("/points", response_model=List[HeatmapPoint], summary="Get weighted heatmap data points")
async def get_heatmap_points(
    fraud_type: Optional[str] = Query(None, description="Filter by fraud type"),
    district: Optional[str] = Query(None, description="Filter by district"),
    start_date: Optional[datetime] = Query(None, description="Filter start date"),
    end_date: Optional[datetime] = Query(None, description="Filter end date"),
    min_lat: Optional[float] = Query(None, description="Bounding box min latitude"),
    max_lat: Optional[float] = Query(None, description="Bounding box max latitude"),
    min_lon: Optional[float] = Query(None, description="Bounding box min longitude"),
    max_lon: Optional[float] = Query(None, description="Bounding box max longitude"),
    limit: int = Query(1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Generate normalized weighted coordinate points suitable for rendering
    heatmaps on map libraries (Leaflet heatLayer, Mapbox GL heatmap, Google Maps).
    """
    return await HeatmapService.get_complaint_heatmap_points(
        db=db,
        fraud_type=fraud_type,
        district=district,
        start_date=start_date,
        end_date=end_date,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        limit=limit,
    )


@router.get("/geojson", summary="Get heatmap data formatted as GeoJSON FeatureCollection")
async def get_heatmap_geojson(
    fraud_type: Optional[str] = Query(None, description="Filter by fraud type"),
    district: Optional[str] = Query(None, description="Filter by district"),
    start_date: Optional[datetime] = Query(None, description="Filter start date"),
    end_date: Optional[datetime] = Query(None, description="Filter end date"),
    limit: int = Query(1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Return complaint geospatial locations as standard GeoJSON for GIS clients."""
    return await HeatmapService.get_complaints_geojson(
        db=db,
        fraud_type=fraud_type,
        district=district,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


@router.get("/withdrawals", response_model=List[HeatmapPoint], summary="Get fraudulent cash-out heatmap points")
async def get_withdrawal_heatmap(
    district: Optional[str] = Query(None, description="Filter by district"),
    is_fraud_only: bool = Query(True, description="Only include confirmed fraudulent withdrawals"),
    limit: int = Query(1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Generate intensity points for ATM cash withdrawals and cash-out points."""
    return await HeatmapService.get_withdrawal_heatmap_points(
        db=db,
        district=district,
        is_fraud_only=is_fraud_only,
        limit=limit,
    )
