"""ATM Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.atm import ATMStatus


class ATMBase(BaseModel):
    atm_id: str = Field(..., min_length=3, max_length=64)
    bank_name: str = Field(..., min_length=2, max_length=100)
    branch_name: str = Field(..., min_length=2, max_length=150)
    address: str = Field(..., min_length=5, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    status: ATMStatus = ATMStatus.ACTIVE


class ATMCreate(ATMBase):
    pass


class ATMUpdate(BaseModel):
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    status: Optional[ATMStatus] = None


class ATMResponse(ATMBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ATMProximityQuery(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    radius_km: float = Field(default=5.0, gt=0, le=100.0)
    bank_name: Optional[str] = None
    status: Optional[ATMStatus] = ATMStatus.ACTIVE


class ATMRiskProfile(BaseModel):
    atm: ATMResponse
    distance_km: Optional[float] = None
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Risk index between 0 and 100")
    risk_level: str = Field(..., description="low, medium, high, or critical")
    recent_fraud_count: int
    total_fraud_volume: float
    factors: list[str]
