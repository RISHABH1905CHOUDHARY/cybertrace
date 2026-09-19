"""Pydantic schemas and DTOs for ML feature pipelines and model inference."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class MLFeatureVector(BaseModel):
    complaint_amount: float
    fraud_type_encoded: int
    hour_of_day: int
    day_of_week: int
    latitude: float
    longitude: float
    distance_to_atm_km: float
    atm_historical_fraud_count: int
    atm_historical_fraud_volume: float
    district_risk_index: float


class ATMPredictionScore(BaseModel):
    atm_id: str
    bank_name: str
    branch_name: str
    latitude: float
    longitude: float
    distance_km: float
    withdrawal_probability: float = Field(..., ge=0.0, le=1.0, description="Model probability 0.0 - 1.0")
    predicted_rank: int
    estimated_time_window_hours: str = "1 to 6 hours"
    feature_importances: Dict[str, float] = {}


class MLPredictionResponse(BaseModel):
    complaint_id: Optional[str] = None
    model_version: str = "v0.1-stub"
    prediction_timestamp: datetime
    top_candidate_atms: List[ATMPredictionScore]
    summary_insight: str
