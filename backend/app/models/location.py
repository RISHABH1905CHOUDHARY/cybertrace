"""Geographical Location and Hotspot ORM Model."""

from enum import Enum
from sqlalchemy import Float, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin


class LocationType(str, Enum):
    HOTSPOT = "hotspot"
    POLICE_STATION = "police_station"
    BANK_BRANCH = "bank_branch"
    JURISDICTIONAL_BOUNDARY = "jurisdictional_boundary"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Location(Base, TimestampMixin):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), default=LocationType.HOTSPOT.value, index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    state: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    radius_meters: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(30), default=RiskLevel.MEDIUM.value, index=True, nullable=False)

    __table_args__ = (
        Index("ix_locations_lat_long", "latitude", "longitude"),
    )

    def __repr__(self) -> str:
        return f"<Location {self.name} ({self.location_type}) - Risk: {self.risk_level}>"
