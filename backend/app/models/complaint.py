"""Cybercrime Complaint ORM Model."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import DateTime, Float, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from app.database.base import Base, TimestampMixin

# Optional GeoAlchemy2 integration
if settings.USE_POSTGIS:
    from geoalchemy2 import Geometry
    PointType = Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
else:
    PointType = None


class FraudType(str, Enum):
    ATM_FRAUD = "ATM Fraud"
    CARD_FRAUD = "Card Fraud"
    UPI_FRAUD = "UPI Fraud"
    BANKING_FRAUD = "Banking Fraud"
    PHISHING = "Phishing"
    ONLINE_SHOPPING_FRAUD = "Online Shopping Fraud"
    OTHER = "Other"


class ComplaintStatus(str, Enum):
    REPORTED = "reported"
    UNDER_INVESTIGATION = "under_investigation"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Complaint(Base, TimestampMixin):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    complaint_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    complaint_type: Mapped[str] = mapped_column(String(100), default="Cyber Fraud", nullable=False)
    fraud_type: Mapped[str] = mapped_column(String(60), index=True, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    complaint_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    state: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    area: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional PostGIS spatial geometry column
    if PointType is not None:
        location_geom: Mapped[Optional[object]] = mapped_column(PointType, nullable=True)

    status: Mapped[str] = mapped_column(String(40), default=ComplaintStatus.REPORTED.value, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(100), default="National Cyber Crime Reporting Portal", nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="complaint", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_complaints_lat_long", "latitude", "longitude"),
        Index("ix_complaints_district_fraud", "district", "fraud_type"),
    )

    def __repr__(self) -> str:
        return f"<Complaint {self.complaint_id} - {self.fraud_type} INR {self.amount}>"
