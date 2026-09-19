"""ATM Management and Spatial Query API routes."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_user, get_db, require_role
from app.models.atm import ATMStatus
from app.models.user import User, UserRole
from app.schemas.atm import ATMCreate, ATMResponse, ATMRiskProfile, ATMUpdate
from app.services.atm_service import ATMService
from app.services.risk_service import RiskService
from app.utils.pagination import PageResponse

router = APIRouter(prefix="/atms", tags=["ATMs"])


@router.get("", response_model=PageResponse[ATMResponse], summary="List and filter ATMs")
async def list_atms(
    bank_name: Optional[str] = Query(None, description="Filter by bank name"),
    status: Optional[ATMStatus] = Query(None, description="Filter by ATM status"),
    city: Optional[str] = Query(None, description="Filter by city"),
    district: Optional[str] = Query(None, description="Filter by district"),
    state: Optional[str] = Query(None, description="Filter by state"),
    search: Optional[str] = Query(None, description="Search across ATM ID, branch, address"),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve filtered, paginated list of ATMs."""
    items, total = await ATMService.list_atms(
        db=db,
        bank_name=bank_name,
        status=status,
        city=city,
        district=district,
        state=state,
        search=search,
        offset=pagination.offset,
        limit=pagination.page_size,
    )
    return PageResponse.create(items=items, total=total, page=pagination.page, page_size=pagination.page_size)


@router.post("", response_model=ATMResponse, status_code=status.HTTP_201_CREATED, summary="Register a new ATM")
async def create_atm(
    atm_in: ATMCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value])),
):
    """Register a new ATM terminal in the system."""
    existing = await ATMService.get_by_atm_id(db, atm_in.atm_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ATM with code '{atm_in.atm_id}' is already registered.",
        )
    return await ATMService.create_atm(db, atm_in, user_id=current_user.id)


@router.get("/nearby", summary="Find ATMs in proximity to coordinates")
async def get_nearby_atms(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(5.0, gt=0, le=50.0),
    bank_name: Optional[str] = None,
    status: Optional[ATMStatus] = ATMStatus.ACTIVE,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Spatial proximity search for ATMs within a radius around given latitude/longitude."""
    results = await ATMService.find_nearby(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        bank_name=bank_name,
        status=status,
    )
    return [
        {
            "atm": ATMResponse.model_validate(atm),
            "distance_km": dist,
        }
        for atm, dist in results
    ]


@router.get("/{atm_id}", response_model=ATMResponse, summary="Get ATM details by ID or code")
async def get_atm(
    atm_id: str,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve ATM record by primary key or unique code."""
    if atm_id.isdigit():
        atm = await ATMService.get_by_id(db, int(atm_id))
    else:
        atm = await ATMService.get_by_atm_id(db, atm_id)

    if not atm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ATM not found")
    return atm


@router.put("/{atm_id}", response_model=ATMResponse, summary="Update ATM record")
async def update_atm(
    atm_id: int,
    atm_update: ATMUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value])),
):
    """Update ATM details or operational status."""
    atm = await ATMService.get_by_id(db, atm_id)
    if not atm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ATM not found")
    return await ATMService.update_atm(db, atm, atm_update, user_id=current_user.id)


@router.get("/{atm_id}/risk", response_model=ATMRiskProfile, summary="Evaluate ATM cybercrime risk score")
async def get_atm_risk(
    atm_id: int,
    search_radius_km: float = Query(5.0, gt=0, le=20.0),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Calculate multi-factor risk score for an ATM based on nearby cybercrimes and historical fraud."""
    atm = await ATMService.get_by_id(db, atm_id)
    if not atm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ATM not found")

    return await RiskService.compute_atm_risk_score(db, atm, search_radius_km=search_radius_km)
