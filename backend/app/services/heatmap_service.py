"""Heatmap generation service for GIS map visualizations."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.atm import ATM
from app.models.transaction import Transaction
from app.schemas.dashboard import HeatmapGeoJSON, HeatmapPoint
from app.utils.geo import to_geojson_feature, to_geojson_feature_collection


class HeatmapService:
    @staticmethod
    async def get_complaint_heatmap_points(
        db: AsyncSession,
        fraud_type: Optional[str] = None,
        district: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        limit: int = 1000,
    ) -> List[HeatmapPoint]:
        """Fetch weighted points representing cybercrime complaint intensities."""
        query = select(Complaint)

        if fraud_type:
            query = query.where(Complaint.fraud_type == fraud_type)
        if district:
            query = query.where(Complaint.district.ilike(f"%{district}%"))
        if start_date:
            query = query.where(Complaint.complaint_date >= start_date)
        if end_date:
            query = query.where(Complaint.complaint_date <= end_date)
        if min_lat is not None and max_lat is not None:
            query = query.where(Complaint.latitude.between(min_lat, max_lat))
        if min_lon is not None and max_lon is not None:
            query = query.where(Complaint.longitude.between(min_lon, max_lon))

        query = query.limit(limit)
        result = await db.execute(query)
        complaints = result.scalars().all()

        if not complaints:
            return []

        # Find max amount to normalize weights between 0.1 and 1.0
        amounts = [float(c.amount) for c in complaints]
        max_amt = max(amounts) if amounts and max(amounts) > 0 else 1.0

        points = []
        for c in complaints:
            amt = float(c.amount)
            # Logarithmic or linear weight scaling
            normalized_weight = round(min(1.0, 0.2 + (amt / max_amt) * 0.8), 3)
            points.append(
                HeatmapPoint(
                    latitude=c.latitude,
                    longitude=c.longitude,
                    weight=normalized_weight,
                    fraud_type=c.fraud_type,
                    amount=amt,
                    district=c.district,
                )
            )

        return points

    @staticmethod
    async def get_complaints_geojson(
        db: AsyncSession,
        fraud_type: Optional[str] = None,
        district: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 1000,
    ) -> Dict[str, Any]:
        """Generate a GeoJSON FeatureCollection of complaints for direct frontend map rendering."""
        points = await HeatmapService.get_complaint_heatmap_points(
            db=db,
            fraud_type=fraud_type,
            district=district,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )

        features = []
        for p in points:
            feature = to_geojson_feature(
                latitude=p.latitude,
                longitude=p.longitude,
                properties={
                    "weight": p.weight,
                    "fraud_type": p.fraud_type,
                    "amount": p.amount,
                    "district": p.district,
                },
            )
            features.append(feature)

        return to_geojson_feature_collection(features)

    @staticmethod
    async def get_withdrawal_heatmap_points(
        db: AsyncSession,
        district: Optional[str] = None,
        is_fraud_only: bool = True,
        limit: int = 1000,
    ) -> List[HeatmapPoint]:
        """Generate heatmap points for cash withdrawals (especially fraudulent cash-outs)."""
        query = select(Transaction)
        if is_fraud_only:
            query = query.where(Transaction.is_fraud.is_(True))
        if district:
            query = query.where(Transaction.district.ilike(f"%{district}%"))

        query = query.limit(limit)
        result = await db.execute(query)
        transactions = result.scalars().all()

        if not transactions:
            return []

        amounts = [float(t.amount) for t in transactions]
        max_amt = max(amounts) if amounts and max(amounts) > 0 else 1.0

        points = []
        for t in transactions:
            amt = float(t.amount)
            weight = round(min(1.0, 0.3 + (amt / max_amt) * 0.7), 3)
            points.append(
                HeatmapPoint(
                    latitude=t.latitude,
                    longitude=t.longitude,
                    weight=weight,
                    fraud_type="Cash Withdrawal",
                    amount=amt,
                    district=t.district,
                )
            )

        return points
