"""ATM management and proximity search service."""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.atm import ATM, ATMStatus
from app.models.audit_log import AuditLog
from app.schemas.atm import ATMCreate, ATMUpdate
from app.utils.geo import get_bounding_box, haversine_distance_km


class ATMService:
    @staticmethod
    async def create_atm(
        db: AsyncSession,
        atm_in: ATMCreate,
        user_id: Optional[int] = None,
    ) -> ATM:
        """Register a new ATM."""
        db_atm = ATM(
            atm_id=atm_in.atm_id,
            bank_name=atm_in.bank_name,
            branch_name=atm_in.branch_name,
            address=atm_in.address,
            city=atm_in.city,
            district=atm_in.district,
            state=atm_in.state,
            latitude=atm_in.latitude,
            longitude=atm_in.longitude,
            status=atm_in.status.value,
        )
        db.add(db_atm)
        await db.flush()

        audit = AuditLog(
            user_id=user_id,
            action="CREATE_ATM",
            resource_type="atm",
            resource_id=atm_in.atm_id,
            details=f"Registered ATM {atm_in.atm_id} - {atm_in.bank_name}, {atm_in.branch_name}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(db_atm)
        return db_atm

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[ATM]:
        """Fetch ATM by internal primary key."""
        result = await db.execute(select(ATM).where(ATM.id == id))
        return result.scalars().first()

    @staticmethod
    async def get_by_atm_id(db: AsyncSession, atm_id: str) -> Optional[ATM]:
        """Fetch ATM by public unique ATM ID."""
        result = await db.execute(select(ATM).where(ATM.atm_id == atm_id))
        return result.scalars().first()

    @staticmethod
    async def list_atms(
        db: AsyncSession,
        bank_name: Optional[str] = None,
        status: Optional[ATMStatus] = None,
        city: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        search: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[ATM], int]:
        """List ATMs with filters and pagination."""
        query = select(ATM)

        if bank_name:
            query = query.where(func.lower(ATM.bank_name) == bank_name.lower())
        if status:
            query = query.where(ATM.status == status.value)
        if city:
            query = query.where(func.lower(ATM.city) == city.lower())
        if district:
            query = query.where(func.lower(ATM.district) == district.lower())
        if state:
            query = query.where(func.lower(ATM.state) == state.lower())
        if search:
            pattern = f"%{search}%"
            query = query.where(
                (ATM.atm_id.ilike(pattern))
                | (ATM.bank_name.ilike(pattern))
                | (ATM.branch_name.ilike(pattern))
                | (ATM.address.ilike(pattern))
            )

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        items_query = query.order_by(ATM.bank_name.asc(), ATM.branch_name.asc()).offset(offset).limit(limit)
        items_result = await db.execute(items_query)
        items = list(items_result.scalars().all())

        return items, total

    @staticmethod
    async def update_atm(
        db: AsyncSession,
        atm: ATM,
        atm_update: ATMUpdate,
        user_id: Optional[int] = None,
    ) -> ATM:
        """Update ATM information."""
        update_data = atm_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(value, "value"):
                setattr(atm, field, value.value)
            else:
                setattr(atm, field, value)

        audit = AuditLog(
            user_id=user_id,
            action="UPDATE_ATM",
            resource_type="atm",
            resource_id=atm.atm_id,
            details=f"Updated ATM fields: {list(update_data.keys())}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(atm)
        return atm

    @staticmethod
    async def find_nearby(
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        bank_name: Optional[str] = None,
        status: Optional[ATMStatus] = None,
    ) -> List[Tuple[ATM, float]]:
        """
        Find ATMs within specified radius of a coordinate using bounding box indexing and Haversine formula.
        Returns sorted list of (ATM, distance_km).
        """
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
        query = select(ATM).where(
            ATM.latitude.between(min_lat, max_lat),
            ATM.longitude.between(min_lon, max_lon),
        )
        if bank_name:
            query = query.where(func.lower(ATM.bank_name) == bank_name.lower())
        if status:
            query = query.where(ATM.status == status.value)

        result = await db.execute(query)
        candidates = result.scalars().all()

        nearby: List[Tuple[ATM, float]] = []
        for atm in candidates:
            dist = haversine_distance_km(latitude, longitude, atm.latitude, atm.longitude)
            if dist <= radius_km:
                nearby.append((atm, dist))

        nearby.sort(key=lambda x: x[1])
        return nearby
