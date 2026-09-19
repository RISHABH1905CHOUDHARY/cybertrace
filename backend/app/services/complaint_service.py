"""Complaint management business logic service."""

from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint, ComplaintStatus, FraudType
from app.models.audit_log import AuditLog
from app.schemas.complaint import ComplaintCreate, ComplaintFilterParams, ComplaintUpdate
from app.utils.geo import get_bounding_box, haversine_distance_km
from app.utils.validators import generate_complaint_id


class ComplaintService:
    @staticmethod
    async def create_complaint(
        db: AsyncSession,
        complaint_in: ComplaintCreate,
        user_id: Optional[int] = None,
    ) -> Complaint:
        """Register a new cybercrime complaint and log audit trail."""
        complaint_id = complaint_in.complaint_id or generate_complaint_id()
        
        db_complaint = Complaint(
            complaint_id=complaint_id,
            complaint_type=complaint_in.complaint_type,
            fraud_type=complaint_in.fraud_type.value,
            amount=complaint_in.amount,
            complaint_date=complaint_in.complaint_date,
            transaction_date=complaint_in.transaction_date,
            state=complaint_in.state,
            district=complaint_in.district,
            city=complaint_in.city,
            area=complaint_in.area,
            latitude=complaint_in.latitude,
            longitude=complaint_in.longitude,
            status=complaint_in.status.value,
            description=complaint_in.description,
            source=complaint_in.source,
        )
        db.add(db_complaint)
        await db.flush()

        # Record audit log
        audit = AuditLog(
            user_id=user_id,
            action="CREATE_COMPLAINT",
            resource_type="complaint",
            resource_id=complaint_id,
            details=f"Created complaint {complaint_id} of type {complaint_in.fraud_type} for INR {complaint_in.amount}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(db_complaint)
        return db_complaint

    @staticmethod
    async def get_by_id(db: AsyncSession, complaint_id: int) -> Optional[Complaint]:
        """Fetch complaint by internal primary key."""
        result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_complaint_id(db: AsyncSession, complaint_id_str: str) -> Optional[Complaint]:
        """Fetch complaint by public complaint code."""
        result = await db.execute(select(Complaint).where(Complaint.complaint_id == complaint_id_str))
        return result.scalars().first()

    @staticmethod
    async def list_complaints(
        db: AsyncSession,
        filters: Optional[ComplaintFilterParams] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Complaint], int]:
        """Query complaints with dynamic filtering and total count."""
        query = select(Complaint)

        if filters:
            if filters.fraud_type:
                query = query.where(Complaint.fraud_type == filters.fraud_type.value)
            if filters.status:
                query = query.where(Complaint.status == filters.status.value)
            if filters.state:
                query = query.where(func.lower(Complaint.state) == filters.state.lower())
            if filters.district:
                query = query.where(func.lower(Complaint.district) == filters.district.lower())
            if filters.city:
                query = query.where(func.lower(Complaint.city) == filters.city.lower())
            if filters.min_amount is not None:
                query = query.where(Complaint.amount >= filters.min_amount)
            if filters.max_amount is not None:
                query = query.where(Complaint.amount <= filters.max_amount)
            if filters.start_date:
                query = query.where(Complaint.complaint_date >= filters.start_date)
            if filters.end_date:
                query = query.where(Complaint.complaint_date <= filters.end_date)
            if filters.search:
                pattern = f"%{filters.search}%"
                query = query.where(
                    (Complaint.complaint_id.ilike(pattern))
                    | (Complaint.description.ilike(pattern))
                    | (Complaint.area.ilike(pattern))
                )

        # Count total matching records
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        # Paginated results ordered by newest complaint date
        items_query = query.order_by(Complaint.complaint_date.desc()).offset(offset).limit(limit)
        items_result = await db.execute(items_query)
        items = list(items_result.scalars().all())

        return items, total

    @staticmethod
    async def update_complaint(
        db: AsyncSession,
        complaint: Complaint,
        complaint_update: ComplaintUpdate,
        user_id: Optional[int] = None,
    ) -> Complaint:
        """Update complaint details."""
        update_data = complaint_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(value, "value"):
                setattr(complaint, field, value.value)
            else:
                setattr(complaint, field, value)

        audit = AuditLog(
            user_id=user_id,
            action="UPDATE_COMPLAINT",
            resource_type="complaint",
            resource_id=complaint.complaint_id,
            details=f"Updated fields: {list(update_data.keys())}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(complaint)
        return complaint

    @staticmethod
    async def update_status(
        db: AsyncSession,
        complaint: Complaint,
        new_status: ComplaintStatus,
        remarks: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Complaint:
        """Update complaint investigation/resolution status."""
        old_status = complaint.status
        complaint.status = new_status.value

        audit = AuditLog(
            user_id=user_id,
            action="UPDATE_STATUS",
            resource_type="complaint",
            resource_id=complaint.complaint_id,
            details=f"Status changed from {old_status} to {new_status.value}. Remarks: {remarks or 'None'}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(complaint)
        return complaint

    @staticmethod
    async def find_nearby(
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float = 10.0,
    ) -> List[Tuple[Complaint, float]]:
        """Find complaints within a geographic radius using spatial bounding box + haversine."""
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
        query = select(Complaint).where(
            Complaint.latitude.between(min_lat, max_lat),
            Complaint.longitude.between(min_lon, max_lon),
        )
        result = await db.execute(query)
        candidates = result.scalars().all()

        nearby_complaints: List[Tuple[Complaint, float]] = []
        for c in candidates:
            dist = haversine_distance_km(latitude, longitude, c.latitude, c.longitude)
            if dist <= radius_km:
                nearby_complaints.append((c, dist))

        nearby_complaints.sort(key=lambda x: x[1])
        return nearby_complaints
