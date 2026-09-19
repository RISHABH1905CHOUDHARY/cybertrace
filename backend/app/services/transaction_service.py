"""Transaction and withdrawal management service."""

from typing import List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.models.atm import ATM
from app.models.audit_log import AuditLog
from app.schemas.transaction import TransactionCreate, TransactionFilterParams
from app.utils.validators import generate_transaction_id


class TransactionService:
    @staticmethod
    async def record_transaction(
        db: AsyncSession,
        txn_in: TransactionCreate,
        user_id: Optional[int] = None,
    ) -> Transaction:
        """Record a new cash withdrawal or transaction."""
        transaction_id = txn_in.transaction_id or generate_transaction_id()

        # If atm_code provided but atm_id missing, resolve ATM
        resolved_atm_id = txn_in.atm_id
        if not resolved_atm_id and txn_in.atm_code:
            atm_res = await db.execute(select(ATM.id).where(ATM.atm_id == txn_in.atm_code))
            resolved_atm_id = atm_res.scalar_one_or_none()

        db_txn = Transaction(
            transaction_id=transaction_id,
            atm_id=resolved_atm_id,
            atm_code=txn_in.atm_code,
            transaction_date=txn_in.transaction_date,
            transaction_time=txn_in.transaction_time,
            amount=txn_in.amount,
            transaction_type=txn_in.transaction_type,
            city=txn_in.city,
            district=txn_in.district,
            latitude=txn_in.latitude,
            longitude=txn_in.longitude,
            is_fraud=txn_in.is_fraud,
            complaint_id=txn_in.complaint_id,
        )
        db.add(db_txn)
        await db.flush()

        if txn_in.is_fraud:
            audit = AuditLog(
                user_id=user_id,
                action="FLAG_FRAUD_TRANSACTION",
                resource_type="transaction",
                resource_id=transaction_id,
                details=f"Fraud transaction {transaction_id} INR {txn_in.amount} linked to complaint {txn_in.complaint_id}",
            )
            db.add(audit)

        await db.commit()
        await db.refresh(db_txn)
        return db_txn

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[Transaction]:
        """Fetch transaction by internal primary key."""
        result = await db.execute(select(Transaction).where(Transaction.id == id))
        return result.scalars().first()

    @staticmethod
    async def get_by_transaction_id(db: AsyncSession, txn_id: str) -> Optional[Transaction]:
        """Fetch transaction by unique transaction ID."""
        result = await db.execute(select(Transaction).where(Transaction.transaction_id == txn_id))
        return result.scalars().first()

    @staticmethod
    async def list_transactions(
        db: AsyncSession,
        filters: Optional[TransactionFilterParams] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Transaction], int]:
        """Query transactions with filtering and total count."""
        query = select(Transaction)

        if filters:
            if filters.atm_id is not None:
                query = query.where(Transaction.atm_id == filters.atm_id)
            if filters.atm_code:
                query = query.where(Transaction.atm_code == filters.atm_code)
            if filters.is_fraud is not None:
                query = query.where(Transaction.is_fraud == filters.is_fraud)
            if filters.district:
                query = query.where(func.lower(Transaction.district) == filters.district.lower())
            if filters.city:
                query = query.where(func.lower(Transaction.city) == filters.city.lower())
            if filters.min_amount is not None:
                query = query.where(Transaction.amount >= filters.min_amount)
            if filters.max_amount is not None:
                query = query.where(Transaction.amount <= filters.max_amount)
            if filters.start_date:
                query = query.where(Transaction.transaction_date >= filters.start_date)
            if filters.end_date:
                query = query.where(Transaction.transaction_date <= filters.end_date)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        items_query = query.order_by(Transaction.transaction_date.desc(), Transaction.transaction_time.desc()).offset(offset).limit(limit)
        items_result = await db.execute(items_query)
        items = list(items_result.scalars().all())

        return items, total

    @staticmethod
    async def link_to_complaint(
        db: AsyncSession,
        transaction: Transaction,
        complaint_id: int,
        mark_as_fraud: bool = True,
        user_id: Optional[int] = None,
    ) -> Transaction:
        """Link a withdrawal transaction directly to an investigated cybercrime complaint."""
        transaction.complaint_id = complaint_id
        if mark_as_fraud:
            transaction.is_fraud = True

        audit = AuditLog(
            user_id=user_id,
            action="LINK_TRANSACTION_TO_COMPLAINT",
            resource_type="transaction",
            resource_id=transaction.transaction_id,
            details=f"Linked to complaint PK {complaint_id}",
        )
        db.add(audit)
        await db.commit()
        await db.refresh(transaction)
        return transaction
