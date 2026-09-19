"""Transaction and Withdrawal ORM Model."""

from datetime import date, time
from typing import Optional
from sqlalchemy import Boolean, Date, Float, ForeignKey, Index, Numeric, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    
    # ATM linkage
    atm_id: Mapped[Optional[int]] = mapped_column(ForeignKey("atms.id", ondelete="SET NULL"), nullable=True, index=True)
    atm_code: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)

    transaction_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    transaction_time: Mapped[time] = mapped_column(Time, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), default="cash_withdrawal", nullable=False)
    
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    
    is_fraud: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    complaint_id: Mapped[Optional[int]] = mapped_column(ForeignKey("complaints.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    atm = relationship("ATM", back_populates="transactions")
    complaint = relationship("Complaint", back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_date_fraud", "transaction_date", "is_fraud"),
        Index("ix_transactions_district_date", "district", "transaction_date"),
    )

    def __repr__(self) -> str:
        return f"<Transaction {self.transaction_id} INR {self.amount} is_fraud={self.is_fraud}>"
