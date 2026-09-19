"""Geographic Location POI and Hotspot API routes."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_user, get_db, require_role
from app.models.location import LocationType, RiskLevel
from app.models.user import User, UserRole
from app.schemas.location import LocationCreate, LocationResponse
from app.services.geospatial_service import GeospatialService
from app.utils.pagination import PageResponse

router = APIRouter(prefix="/locations", tags=["Locations & GIS"])


@router.get("", response_model=PageResponse[LocationResponse], summary="List GIS locations and hotspots")
async def list_locations(
    location_type: Optional[LocationType] = Query(None, description="Filter by location classification"),
    district: Optional[str] = Query(None, description="Filter by district"),
    risk_level: Optional[RiskLevel] = Query(None, description="Filter by risk severity"),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve indexed geographic points of interest, police boundaries, and crime hotspots."""
    items, total = await GeospatialService.list_locations(
        db=db,
        location_type=location_type,
        district=district,
        risk_level=risk_level,
        offset=pagination.offset,
        limit=pagination.page_size,
    )
    return PageResponse.create(items=items, total=total, page=pagination.page, page_size=pagination.page_size)


@router.post("", response_model=LocationResponse, status_code=status.HTTP_201_CREATED, summary="Create a GIS location or hotspot")
async def create_location(
    location_in: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value])),
):
    """Create a new geographic hotspot, jurisdictional boundary, or police station record."""
    return await GeospatialService.create_location(db, location_in)


@router.get("/nearby", summary="Find locations near coordinates")
async def get_nearby_locations(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(10.0, gt=0, le=50.0),
    location_type: Optional[LocationType] = None,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Find GIS locations within specified radius of coordinates."""
    results = await GeospatialService.find_nearby_locations(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        location_type=location_type,
    )
    return [
        {
            "location": LocationResponse.model_validate(loc),
            "distance_km": dist,
        }
        for loc, dist in results
    ]


@router.get("/{location_id}", response_model=LocationResponse, summary="Get location by ID")
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Fetch location details by ID."""
    loc = await GeospatialService.get_by_id(db, location_id)
    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return loc
