"""Risk analysis and cash-out forecasting service."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.atm import ATM, ATMStatus
from app.models.complaint import Complaint
from app.models.transaction import Transaction
from app.models.location import RiskLevel
from app.schemas.atm import ATMRiskProfile, ATMResponse
from app.utils.geo import get_bounding_box, haversine_distance_km


class RiskService:
    @staticmethod
    def categorize_risk(score: float) -> str:
        """Categorize numerical risk score into discrete risk levels."""
        if score >= settings.CRITICAL_RISK_THRESHOLD:
            return RiskLevel.CRITICAL.value
        elif score >= settings.HIGH_RISK_THRESHOLD:
            return RiskLevel.HIGH.value
        elif score >= 40.0:
            return RiskLevel.MEDIUM.value
        return RiskLevel.LOW.value

    @staticmethod
    async def compute_atm_risk_score(
        db: AsyncSession,
        atm: ATM,
        search_radius_km: float = 5.0,
    ) -> ATMRiskProfile:
        """
        Compute multi-factor heuristic risk score for a single ATM:
        1. Proximity & count of complaints within radius
        2. Count and sum of fraudulent transactions at this ATM
        3. Recency of complaints
        """
        # 1. Nearby complaints within search radius
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(atm.latitude, atm.longitude, search_radius_km)
        comp_query = select(Complaint).where(
            Complaint.latitude.between(min_lat, max_lat),
            Complaint.longitude.between(min_lon, max_lon),
        )
        comp_res = await db.execute(comp_query)
        nearby_complaints = [
            c for c in comp_res.scalars().all()
            if haversine_distance_km(atm.latitude, atm.longitude, c.latitude, c.longitude) <= search_radius_km
        ]

        # 2. Fraudulent transactions at this ATM
        txn_query = select(
            func.count(Transaction.id).label("fraud_count"),
            func.coalesce(func.sum(Transaction.amount), 0.0).label("fraud_sum"),
        ).where(
            (Transaction.atm_id == atm.id) | (Transaction.atm_code == atm.atm_id),
            Transaction.is_fraud.is_(True),
        )
        txn_res = await db.execute(txn_query)
        fraud_count, fraud_volume = txn_res.first()
        fraud_volume = float(fraud_volume)

        # 3. Factor scoring
        factors: List[str] = []
        score = 10.0  # baseline operational risk

        # Complaint density factor (up to 40 points)
        comp_count = len(nearby_complaints)
        if comp_count > 0:
            comp_pts = min(40.0, comp_count * 8.0)
            score += comp_pts
            factors.append(f"{comp_count} cybercrime complaints within {search_radius_km}km (+{comp_pts:.1f} pts)")

        # Direct fraud history factor (up to 35 points)
        if fraud_count > 0:
            fraud_pts = min(35.0, fraud_count * 12.0)
            score += fraud_pts
            factors.append(f"{fraud_count} previous fraudulent withdrawals recorded at this ATM (+{fraud_pts:.1f} pts)")

        # Financial exposure factor (up to 15 points)
        if fraud_volume > 100000:
            score += 15.0
            factors.append(f"High fraud withdrawal volume INR {fraud_volume:,.2f} (+15.0 pts)")
        elif fraud_volume > 25000:
            score += 8.0
            factors.append(f"Moderate fraud withdrawal volume INR {fraud_volume:,.2f} (+8.0 pts)")

        score = min(100.0, round(score, 1))
        risk_level = RiskService.categorize_risk(score)

        return ATMRiskProfile(
            atm=ATMResponse.model_validate(atm),
            distance_km=None,
            risk_score=score,
            risk_level=risk_level,
            recent_fraud_count=fraud_count,
            total_fraud_volume=fraud_volume,
            factors=factors or ["Standard baseline risk, no immediate cluster threats detected"],
        )

    @staticmethod
    async def forecast_withdrawal_locations(
        db: AsyncSession,
        latitude: float,
        longitude: float,
        complaint_amount: float = 50000.0,
        radius_km: float = 10.0,
        top_k: int = 5,
    ) -> List[ATMRiskProfile]:
        """
        Forecasting likely cash withdrawal locations for a cybercrime complaint.
        Evaluates candidate ATMs within the radius, scores likelihood based on:
        - Distance to fraud incident origin
        - ATM historical fraud susceptibility
        - Active ATM status
        """
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
        query = select(ATM).where(
            ATM.latitude.between(min_lat, max_lat),
            ATM.longitude.between(min_lon, max_lon),
            ATM.status == ATMStatus.ACTIVE.value,
        )
        res = await db.execute(query)
        candidates = res.scalars().all()

        profiles: List[ATMRiskProfile] = []
        for atm in candidates:
            dist = haversine_distance_km(latitude, longitude, atm.latitude, atm.longitude)
            if dist > radius_km:
                continue

            base_profile = await RiskService.compute_atm_risk_score(db, atm, search_radius_km=3.0)
            
            # Distance penalty/multiplier: closer ATMs have higher probability of withdrawal
            distance_factor = max(0.2, (radius_km - dist) / radius_km)
            forecast_score = min(100.0, round((base_profile.risk_score * 0.6) + (distance_factor * 40.0), 1))
            
            forecast_factors = list(base_profile.factors)
            forecast_factors.insert(0, f"Proximity: {dist:.2f}km from reported crime incident origin")

            profiles.append(
                ATMRiskProfile(
                    atm=base_profile.atm,
                    distance_km=dist,
                    risk_score=forecast_score,
                    risk_level=RiskService.categorize_risk(forecast_score),
                    recent_fraud_count=base_profile.recent_fraud_count,
                    total_fraud_volume=base_profile.total_fraud_volume,
                    factors=forecast_factors,
                )
            )

        # Sort by forecast risk score descending
        profiles.sort(key=lambda p: p.risk_score, reverse=True)
        return profiles[:top_k]
