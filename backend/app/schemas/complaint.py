"""Complaint Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.complaint import ComplaintStatus, FraudType


class ComplaintBase(BaseModel):
    complaint_type: str = Field(default="Cyber Fraud", max_length=100)
    fraud_type: FraudType
    amount: float = Field(..., gt=0, description="Amount defrauded in INR")
    complaint_date: datetime
    transaction_date: datetime
    state: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    area: Optional[str] = Field(None, max_length=150)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    status: ComplaintStatus = ComplaintStatus.REPORTED
    description: Optional[str] = None
    source: str = Field(default="National Cyber Crime Reporting Portal", max_length=100)


class ComplaintCreate(ComplaintBase):
    complaint_id: Optional[str] = Field(None, description="Custom complaint ID, auto-generated if omitted")


class ComplaintUpdate(BaseModel):
    complaint_type: Optional[str] = None
    fraud_type: Optional[FraudType] = None
    amount: Optional[float] = Field(None, gt=0)
    complaint_date: Optional[datetime] = None
    transaction_date: Optional[datetime] = None
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    status: Optional[ComplaintStatus] = None
    description: Optional[str] = None
    source: Optional[str] = None


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    remarks: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    id: int
    complaint_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplaintFilterParams(BaseModel):
    fraud_type: Optional[FraudType] = None
    status: Optional[ComplaintStatus] = None
    state: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search: Optional[str] = None
