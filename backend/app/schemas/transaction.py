"""Transaction and Withdrawal Pydantic schemas."""

from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    transaction_id: str = Field(..., min_length=3, max_length=64)
    atm_id: Optional[int] = None
    atm_code: Optional[str] = None
    transaction_date: date
    transaction_time: time
    amount: float = Field(..., gt=0, description="Amount in INR")
    transaction_type: str = Field(default="cash_withdrawal", max_length=50)
    city: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    is_fraud: bool = False
    complaint_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionFilterParams(BaseModel):
    atm_id: Optional[int] = None
    atm_code: Optional[str] = None
    is_fraud: Optional[bool] = None
    district: Optional[str] = None
    city: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
