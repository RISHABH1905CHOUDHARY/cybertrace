"""Tests for Risk forecasting and ML stub integration."""

from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_forecast_withdrawal_locations(client: AsyncClient, admin_token_headers: dict):
    # 1. Create ATM in New Delhi
    atm_payload = {
        "atm_id": "ATM-FORECAST-01",
        "bank_name": "State Bank of India",
        "branch_name": "CP Branch",
        "address": "Connaught Place",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "latitude": 28.6310,
        "longitude": 77.2170,
        "status": "active",
    }
    await client.post("/api/v1/atms", json=atm_payload, headers=admin_token_headers)

    # 2. Create Complaint close to the ATM (approx 0.5km away)
    complaint_payload = {
        "fraud_type": "UPI Fraud",
        "amount": 85000.0,
        "complaint_date": datetime.now(timezone.utc).isoformat(),
        "transaction_date": datetime.now(timezone.utc).isoformat(),
        "state": "Delhi",
        "district": "New Delhi",
        "city": "New Delhi",
        "latitude": 28.6340,
        "longitude": 77.2180,
        "status": "reported",
    }
    comp_res = await client.post("/api/v1/complaints", json=complaint_payload, headers=admin_token_headers)
    complaint_id = comp_res.json()["id"]

    # 3. Request forecast
    forecast_res = await client.get(
        f"/api/v1/complaints/{complaint_id}/forecast-withdrawals?radius_km=5.0&top_k=3",
        headers=admin_token_headers,
    )
    assert forecast_res.status_code == 200
    forecast_data = forecast_res.json()
    assert isinstance(forecast_data, list)
    assert len(forecast_data) >= 1

    top_atm = forecast_data[0]
    assert top_atm["atm"]["atm_id"] == "ATM-FORECAST-01"
    assert "risk_score" in top_atm
    assert top_atm["distance_km"] < 2.0
    assert len(top_atm["factors"]) > 0
