"""Tests for ATM endpoints and spatial searches."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_query_nearby_atms(client: AsyncClient, admin_token_headers: dict):
    # Register ATM in Connaught Place, Delhi (28.6315, 77.2167)
    atm_payload = {
        "atm_id": "ATM-TEST-DEL01",
        "bank_name": "State Bank of India",
        "branch_name": "Connaught Place Inner Circle",
        "address": "B-Block, Connaught Place",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "latitude": 28.6315,
        "longitude": 77.2167,
        "status": "active",
    }
    create_res = await client.post("/api/v1/atms", json=atm_payload, headers=admin_token_headers)
    assert create_res.status_code == 201
    atm_data = create_res.json()
    assert atm_data["atm_id"] == "ATM-TEST-DEL01"

    # Query nearby from Janpath (28.6250, 77.2180) - approx 0.7km away
    nearby_res = await client.get(
        "/api/v1/atms/nearby?latitude=28.6250&longitude=77.2180&radius_km=2.0",
        headers=admin_token_headers,
    )
    assert nearby_res.status_code == 200
    results = nearby_res.json()
    assert len(results) >= 1
    first_match = results[0]
    assert first_match["atm"]["atm_id"] == "ATM-TEST-DEL01"
    assert first_match["distance_km"] < 2.0


@pytest.mark.asyncio
async def test_atm_risk_score(client: AsyncClient, admin_token_headers: dict):
    # Register ATM
    atm_payload = {
        "atm_id": "ATM-RISK-TEST01",
        "bank_name": "HDFC Bank",
        "branch_name": "Sector 18 Branch",
        "address": "Atta Market, Sector 18",
        "city": "Noida",
        "district": "Gautam Buddha Nagar",
        "state": "Uttar Pradesh",
        "latitude": 28.5708,
        "longitude": 77.3260,
        "status": "active",
    }
    create_res = await client.post("/api/v1/atms", json=atm_payload, headers=admin_token_headers)
    atm_id = create_res.json()["id"]

    risk_res = await client.get(f"/api/v1/atms/{atm_id}/risk", headers=admin_token_headers)
    assert risk_res.status_code == 200
    risk_data = risk_res.json()
    assert "risk_score" in risk_data
    assert "risk_level" in risk_data
    assert isinstance(risk_data["factors"], list)
