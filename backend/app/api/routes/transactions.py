"""Transaction and Withdrawal API routes."""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import PaginationParams, get_current_user, get_db, require_role
from app.models.user import User, UserRole
from app.schemas.transaction import TransactionCreate, TransactionFilterParams, TransactionResponse
from app.services.complaint_service import ComplaintService
from app.services.transaction_service import TransactionService
from app.utils.pagination import PageResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=PageResponse[TransactionResponse], summary="List and filter transactions")
async def list_transactions(
    atm_id: Optional[int] = Query(None, description="Filter by internal ATM ID"),
    atm_code: Optional[str] = Query(None, description="Filter by ATM code"),
    is_fraud: Optional[bool] = Query(None, description="Filter fraud-flagged withdrawals"),
    district: Optional[str] = Query(None, description="Filter by district"),
    city: Optional[str] = Query(None, description="Filter by city"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum withdrawal amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum withdrawal amount"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Retrieve filtered, paginated list of transactions and ATM cash withdrawals."""
    filters = TransactionFilterParams(
        atm_id=atm_id,
        atm_code=atm_code,
        is_fraud=is_fraud,
        district=district,
        city=city,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
    )
    items, total = await TransactionService.list_transactions(
        db=db,
        filters=filters,
        offset=pagination.offset,
        limit=pagination.page_size,
    )
    return PageResponse.create(items=items, total=total, page=pagination.page, page_size=pagination.page_size)


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED, summary="Record a new transaction")
async def record_transaction(
    txn_in: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.ANALYST.value, UserRole.INVESTIGATOR.value])),
):
    """Record an ATM cash withdrawal or banking transaction."""
    return await TransactionService.record_transaction(db, txn_in, user_id=current_user.id)


@router.get("/{txn_id}", response_model=TransactionResponse, summary="Get transaction details by ID or code")
async def get_transaction(
    txn_id: str,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Fetch transaction record by internal PK or transaction ID string."""
    if txn_id.isdigit():
        txn = await TransactionService.get_by_id(db, int(txn_id))
    else:
        txn = await TransactionService.get_by_transaction_id(db, txn_id)

    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return txn


@router.patch("/{txn_id}/link-complaint", response_model=TransactionResponse, summary="Link withdrawal to cybercrime complaint")
async def link_transaction_complaint(
    txn_id: int,
    complaint_id: int = Query(..., description="Internal ID of cybercrime complaint"),
    mark_as_fraud: bool = Query(True, description="Flag this transaction as fraudulent"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN.value, UserRole.INVESTIGATOR.value])),
):
    """Link a specific fraudulent cash withdrawal to an investigated cybercrime complaint."""
    txn = await TransactionService.get_by_id(db, txn_id)
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    complaint = await ComplaintService.get_by_id(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

    return await TransactionService.link_to_complaint(
        db=db,
        transaction=txn,
        complaint_id=complaint_id,
        mark_as_fraud=mark_as_fraud,
        user_id=current_user.id,
    )
