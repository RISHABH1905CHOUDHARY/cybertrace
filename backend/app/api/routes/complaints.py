"""Cybercrime Complaints API routes."""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_user, get_db, require_role
from app.models.complaint import ComplaintStatus, FraudType
from app.models.user import User, UserRole
from app.schemas.atm import ATMRiskProfile
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintFilterParams,
    ComplaintResponse,
    ComplaintStatusUpdate,
    ComplaintUpdate,
)
from app.services.complaint_service import ComplaintService
from app.services.risk_service import RiskService
from app.utils.pagination import PageResponse

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.get("", response_model=PageResponse[ComplaintResponse], summary="List and filter complaints")
async def list_complaints(
    fraud_type: Optional[FraudType] = Query(None, description="Filter by fraud category"),
    status: Optional[ComplaintStatus] = Query(None, description="Filter by complaint status"),
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum defrauded amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum defrauded amount"),
    start_date: Optional[datetime] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date (ISO format)"),
    search: Optional[str] = Query(None, description="Search query across ID, description, area"),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve filtered, paginated list of cybercrime complaints."""
    filters = ComplaintFilterParams(
        fraud_type=fraud_type,
        status=status,
        state=state,
        district=district,
        city=city,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )
    items, total = await ComplaintService.list_complaints(
        db=db,
        filters=filters,
        offset=pagination.offset,
        limit=pagination.page_size,
    )
    return PageResponse.create(items=items, total=total, page=pagination.page, page_size=pagination.page_size)


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED, summary="File a new cybercrime complaint")
async def create_complaint(
    complaint_in: ComplaintCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value, UserRole.INVESTIGATOR.value])),
):
    """Register a new complaint. Allowed for Admin, Analyst, and Investigator roles."""
    return await ComplaintService.create_complaint(db, complaint_in, user_id=current_user.id)


@router.get("/nearby", summary="Find complaints near coordinates")
async def get_nearby_complaints(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    radius_km: float = Query(10.0, gt=0, le=100.0),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Locate complaints occurring within a radius of given coordinates."""
    results = await ComplaintService.find_nearby(db, latitude, longitude, radius_km)
    return [
        {
            "complaint": ComplaintResponse.model_validate(c),
            "distance_km": dist,
        }
        for c, dist in results
    ]


@router.get("/{complaint_id}", response_model=ComplaintResponse, summary="Get complaint by ID or code")
async def get_complaint(
    complaint_id: str,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve full details of a specific complaint by primary key or unique code."""
    if complaint_id.isdigit():
        complaint = await ComplaintService.get_by_id(db, int(complaint_id))
    else:
        complaint = await ComplaintService.get_by_complaint_id(db, complaint_id)

    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse, summary="Update complaint details")
async def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value, UserRole.INVESTIGATOR.value])),
):
    """Update editable fields of a cybercrime complaint."""
    complaint = await ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return await ComplaintService.update_complaint(db, complaint, complaint_update, user_id=current_user.id)


@router.patch("/{complaint_id}/status", response_model=ComplaintResponse, summary="Update complaint investigation status")
async def update_complaint_status(
    complaint_id: int,
    status_update: ComplaintStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.INVESTIGATOR.value])),
):
    """Update complaint status (reported -> under_investigation -> resolved/closed)."""
    complaint = await ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return await ComplaintService.update_status(
        db=db,
        complaint=complaint,
        new_status=status_update.status,
        remarks=status_update.remarks,
        user_id=current_user.id,
    )


@router.get("/{complaint_id}/forecast-withdrawals", response_model=List[ATMRiskProfile], summary="Forecast likely ATM withdrawal locations")
async def forecast_complaint_withdrawals(
    complaint_id: int,
    radius_km: float = Query(10.0, gt=0, le=50.0, description="Search radius around complaint origin"),
    top_k: int = Query(5, ge=1, le=20, description="Top K ranked ATMs to return"),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """
    Forecasting Engine: Ranks nearby ATMs by probability of fraudulent cash withdrawal
    based on geographical proximity, ATM historical fraud volume, and density.
    """
    complaint = await ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

    predictions = await RiskService.forecast_withdrawal_locations(
        db=db,
        latitude=complaint.latitude,
        longitude=complaint.longitude,
        complaint_amount=float(complaint.amount),
        radius_km=radius_km,
        top_k=top_k,
    )
    return predictions
