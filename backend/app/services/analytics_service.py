"""Analytics and Dashboard aggregation service."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.atm import ATM, ATMStatus
from app.models.complaint import Complaint, ComplaintStatus
from app.models.transaction import Transaction
from app.schemas.dashboard import (
    ATMHotspotItem,
    DashboardResponse,
    DashboardSummaryKPIs,
    DistrictLossItem,
    FraudDistributionItem,
    TimeSeriesDataPoint,
)
from app.services.risk_service import RiskService


class AnalyticsService:
    @staticmethod
    async def get_dashboard_kpis(db: AsyncSession) -> DashboardSummaryKPIs:
        """Compute key aggregate performance and crime indicators."""
        # 1. Complaints aggregate
        comp_res = await db.execute(
            select(
                func.count(Complaint.id).label("total_complaints"),
                func.coalesce(func.sum(Complaint.amount), 0.0).label("total_defrauded"),
                func.count(
                    case((Complaint.status == ComplaintStatus.UNDER_INVESTIGATION.value, 1))
                ).label("under_investigation"),
                func.count(
                    case((Complaint.status == ComplaintStatus.RESOLVED.value, 1))
                ).label("resolved"),
            )
        )
        total_comp, total_amount, under_invest, resolved = comp_res.first()
        total_amount = float(total_amount)
        res_rate = round((resolved / total_comp * 100.0), 2) if total_comp > 0 else 0.0

        # 2. ATMs aggregate
        atm_count_res = await db.execute(select(func.count(ATM.id)))
        total_atms = atm_count_res.scalar_one()

        # 3. Fraudulent transactions aggregate
        txn_res = await db.execute(
            select(
                func.count(Transaction.id).label("fraud_txns"),
                func.coalesce(func.sum(Transaction.amount), 0.0).label("fraud_txn_volume"),
            ).where(Transaction.is_fraud.is_(True))
        )
        fraud_txns_count, fraud_txn_volume = txn_res.first()

        # 4. Approximate high risk ATMs count (having fraud transactions or many complaints)
        high_risk_res = await db.execute(
            select(func.count(func.distinct(Transaction.atm_id))).where(Transaction.is_fraud.is_(True))
        )
        high_risk_atms = high_risk_res.scalar_one() or 0

        return DashboardSummaryKPIs(
            total_complaints=total_comp,
            total_defrauded_amount=total_amount,
            total_atms_monitored=total_atms,
            high_risk_atms_count=high_risk_atms,
            under_investigation_count=under_invest,
            resolved_complaints_count=resolved,
            resolution_rate_percentage=res_rate,
            fraudulent_withdrawals_count=fraud_txns_count,
            total_fraudulent_cash_withdrawn=float(fraud_txn_volume),
        )

    @staticmethod
    async def get_fraud_distribution(db: AsyncSession) -> List[FraudDistributionItem]:
        """Aggregate breakdown of cybercrime by fraud type."""
        total_res = await db.execute(select(func.count(Complaint.id)))
        total_count = total_res.scalar_one()

        query = (
            select(
                Complaint.fraud_type,
                func.count(Complaint.id).label("type_count"),
                func.coalesce(func.sum(Complaint.amount), 0.0).label("type_amount"),
            )
            .group_by(Complaint.fraud_type)
            .order_by(func.count(Complaint.id).desc())
        )
        result = await db.execute(query)
        rows = result.all()

        items: List[FraudDistributionItem] = []
        for fraud_type, count, amt in rows:
            pct = round((count / total_count * 100.0), 2) if total_count > 0 else 0.0
            items.append(
                FraudDistributionItem(
                    fraud_type=fraud_type,
                    count=count,
                    percentage=pct,
                    total_amount=float(amt),
                )
            )
        return items

    @staticmethod
    async def get_top_affected_districts(db: AsyncSession, limit: int = 10) -> List[DistrictLossItem]:
        """Aggregate top districts by complaint volume and total financial loss."""
        query = (
            select(
                Complaint.district,
                Complaint.state,
                func.count(Complaint.id).label("c_count"),
                func.coalesce(func.sum(Complaint.amount), 0.0).label("total_loss"),
            )
            .group_by(Complaint.district, Complaint.state)
            .order_by(func.sum(Complaint.amount).desc())
            .limit(limit)
        )
        result = await db.execute(query)
        rows = result.all()

        districts: List[DistrictLossItem] = []
        for dist, state, count, loss in rows:
            loss_float = float(loss)
            risk = "critical" if loss_float > 1000000 else "high" if loss_float > 300000 else "medium"
            districts.append(
                DistrictLossItem(
                    district=dist,
                    state=state,
                    complaint_count=count,
                    total_amount=loss_float,
                    risk_level=risk,
                )
            )
        return districts

    @staticmethod
    async def get_monthly_trend(db: AsyncSession, limit: int = 12) -> List[TimeSeriesDataPoint]:
        """Time-series trend of cybercrime complaints."""
        query = (
            select(
                Complaint.complaint_date,
                Complaint.amount,
            )
            .order_by(Complaint.complaint_date.asc())
        )
        res = await db.execute(query)
        rows = res.all()

        # Group by Year-Month in python for dialect-neutral portability (PostgreSQL + SQLite)
        buckets = {}
        for c_date, amount in rows:
            month_key = c_date.strftime("%Y-%m")
            if month_key not in buckets:
                buckets[month_key] = {"count": 0, "amount": 0.0}
            buckets[month_key]["count"] += 1
            buckets[month_key]["amount"] += float(amount)

        points = [
            TimeSeriesDataPoint(
                period=month,
                complaint_count=data["count"],
                total_amount=round(data["amount"], 2),
                fraud_transactions_count=0,
            )
            for month, data in sorted(buckets.items())
        ]
        return points[-limit:]

    @staticmethod
    async def get_top_vulnerable_atms(db: AsyncSession, limit: int = 5) -> List[ATMHotspotItem]:
        """Fetch ATMs with highest recorded fraud history and risk."""
        atm_query = select(ATM).where(ATM.status == ATMStatus.ACTIVE.value).limit(20)
        atm_res = await db.execute(atm_query)
        atms = atm_res.scalars().all()

        scored_atms = []
        for atm in atms:
            profile = await RiskService.compute_atm_risk_score(db, atm)
            scored_atms.append(profile)

        scored_atms.sort(key=lambda x: x.risk_score, reverse=True)

        hotspots: List[ATMHotspotItem] = []
        for p in scored_atms[:limit]:
            hotspots.append(
                ATMHotspotItem(
                    atm_id=p.atm.atm_id,
                    bank_name=p.atm.bank_name,
                    branch_name=p.atm.branch_name,
                    city=p.atm.city,
                    district=p.atm.district,
                    latitude=p.atm.latitude,
                    longitude=p.atm.longitude,
                    risk_score=p.risk_score,
                    risk_level=p.risk_level,
                    fraud_incidents_nearby=p.recent_fraud_count,
                )
            )
        return hotspots

    @staticmethod
    async def get_full_dashboard(db: AsyncSession) -> DashboardResponse:
        """Fetch complete dashboard payload."""
        kpis = await AnalyticsService.get_dashboard_kpis(db)
        distribution = await AnalyticsService.get_fraud_distribution(db)
        top_districts = await AnalyticsService.get_top_affected_districts(db)
        trend = await AnalyticsService.get_monthly_trend(db)
        vulnerable_atms = await AnalyticsService.get_top_vulnerable_atms(db)

        return DashboardResponse(
            kpis=kpis,
            fraud_distribution=distribution,
            top_districts=top_districts,
            monthly_trend=trend,
            top_vulnerable_atms=vulnerable_atms,
        )
