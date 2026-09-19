"""Geospatial management and spatial query service."""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location, LocationType, RiskLevel
from app.schemas.location import LocationCreate, LocationUpdate
from app.utils.geo import get_bounding_box, haversine_distance_km


class GeospatialService:
    @staticmethod
    async def create_location(
        db: AsyncSession,
        location_in: LocationCreate,
    ) -> Location:
        """Create a geographic point of interest (hotspot, police station, branch)."""
        loc = Location(
            name=location_in.name,
            location_type=location_in.location_type.value,
            district=location_in.district,
            state=location_in.state,
            latitude=location_in.latitude,
            longitude=location_in.longitude,
            radius_meters=location_in.radius_meters,
            risk_level=location_in.risk_level.value,
        )
        db.add(loc)
        await db.commit()
        await db.refresh(loc)
        return loc

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[Location]:
        """Fetch location by primary key."""
        result = await db.execute(select(Location).where(Location.id == id))
        return result.scalars().first()

    @staticmethod
    async def list_locations(
        db: AsyncSession,
        location_type: Optional[LocationType] = None,
        district: Optional[str] = None,
        risk_level: Optional[RiskLevel] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Location], int]:
        """List locations with filtering."""
        query = select(Location)

        if location_type:
            query = query.where(Location.location_type == location_type.value)
        if district:
            query = query.where(func.lower(Location.district) == district.lower())
        if risk_level:
            query = query.where(Location.risk_level == risk_level.value)

        count_res = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_res.scalar_one()

        items_res = await db.execute(query.order_by(Location.name.asc()).offset(offset).limit(limit))
        items = list(items_res.scalars().all())

        return items, total

    @staticmethod
    async def find_nearby_locations(
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float = 10.0,
        location_type: Optional[LocationType] = None,
    ) -> List[Tuple[Location, float]]:
        """Find locations within radius."""
        min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
        query = select(Location).where(
            Location.latitude.between(min_lat, max_lat),
            Location.longitude.between(min_lon, max_lon),
        )
        if location_type:
            query = query.where(Location.location_type == location_type.value)

        res = await db.execute(query)
        candidates = res.scalars().all()

        nearby = []
        for loc in candidates:
            dist = haversine_distance_km(latitude, longitude, loc.latitude, loc.longitude)
            if dist <= radius_km:
                nearby.append((loc, dist))

        nearby.sort(key=lambda x: x[1])
        return nearby
