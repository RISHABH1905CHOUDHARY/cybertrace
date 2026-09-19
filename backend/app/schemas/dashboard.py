"""Dashboard and Analytics Pydantic schemas."""

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DashboardSummaryKPIs(BaseModel):
    total_complaints: int
    total_defrauded_amount: float
    total_atms_monitored: int
    high_risk_atms_count: int
    under_investigation_count: int
    resolved_complaints_count: int
    resolution_rate_percentage: float
    fraudulent_withdrawals_count: int
    total_fraudulent_cash_withdrawn: float


class TimeSeriesDataPoint(BaseModel):
    period: str  # e.g. "2026-01", "2026-09-15"
    complaint_count: int
    total_amount: float
    fraud_transactions_count: int = 0


class FraudDistributionItem(BaseModel):
    fraud_type: str
    count: int
    percentage: float
    total_amount: float


class DistrictLossItem(BaseModel):
    district: str
    state: str
    complaint_count: int
    total_amount: float
    risk_level: str


class ATMHotspotItem(BaseModel):
    atm_id: str
    bank_name: str
    branch_name: str
    city: str
    district: str
    latitude: float
    longitude: float
    risk_score: float
    risk_level: str
    fraud_incidents_nearby: int


class DashboardResponse(BaseModel):
    kpis: DashboardSummaryKPIs
    fraud_distribution: List[FraudDistributionItem]
    top_districts: List[DistrictLossItem]
    monthly_trend: List[TimeSeriesDataPoint]
    top_vulnerable_atms: List[ATMHotspotItem]


# Heatmap Specific Schemas
class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    weight: float = Field(..., description="Normalized intensity from 0.0 to 1.0 or weighted amount")
    fraud_type: Optional[str] = None
    amount: Optional[float] = None
    district: Optional[str] = None


class HeatmapGeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]


class HeatmapGeoJSON(BaseModel):
    type: str = "FeatureCollection"
    features: List[HeatmapGeoJSONFeature]
