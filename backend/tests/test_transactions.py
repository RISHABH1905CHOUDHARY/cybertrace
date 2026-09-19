"""Tests for Transactions and withdrawal management."""

from datetime import date, time
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_record_and_query_transaction(client: AsyncClient, admin_token_headers: dict):
    payload = {
        "transaction_id": "TXN-TEST-1001",
        "atm_code": "ATM-SBI-DEL01",
        "transaction_date": str(date.today()),
        "transaction_time": str(time(14, 30, 0)),
        "amount": 20000.0,
        "transaction_type": "cash_withdrawal",
        "city": "New Delhi",
        "district": "New Delhi",
        "latitude": 28.6315,
        "longitude": 77.2167,
        "is_fraud": True,
    }
    create_res = await client.post("/api/v1/transactions", json=payload, headers=admin_token_headers)
    assert create_res.status_code == 201
    txn_data = create_res.json()
    assert txn_data["transaction_id"] == "TXN-TEST-1001"
    assert txn_data["is_fraud"] is True

    # Query fraud transactions
    query_res = await client.get("/api/v1/transactions?is_fraud=true", headers=admin_token_headers)
    assert query_res.status_code == 200
    assert query_res.json()["total"] >= 1
