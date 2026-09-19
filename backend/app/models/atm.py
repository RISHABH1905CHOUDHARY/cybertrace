"""ATM Database ORM Model."""

from enum import Enum
from typing import Optional
from sqlalchemy import Float, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from app.database.base import Base, TimestampMixin

if settings.USE_POSTGIS:
    from geoalchemy2 import Geometry
    PointType = Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
else:
    PointType = None


class ATMStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class ATM(Base, TimestampMixin):
    __tablename__ = "atms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    atm_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    bank_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    branch_name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    state: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional PostGIS spatial geometry column
    if PointType is not None:
        location_geom: Mapped[Optional[object]] = mapped_column(PointType, nullable=True)

    status: Mapped[str] = mapped_column(String(30), default=ATMStatus.ACTIVE.value, index=True, nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="atm")

    __table_args__ = (
        Index("ix_atms_lat_long", "latitude", "longitude"),
        Index("ix_atms_bank_district", "bank_name", "district"),
    )

    def __repr__(self) -> str:
        return f"<ATM {self.atm_id} - {self.bank_name}, {self.branch_name}>"
