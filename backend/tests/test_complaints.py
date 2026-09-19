"""Tests for Cybercrime Complaints endpoints."""

from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_complaint(client: AsyncClient, admin_token_headers: dict):
    payload = {
        "complaint_type": "Cyber Fraud",
        "fraud_type": "UPI Fraud",
        "amount": 75000.0,
        "complaint_date": datetime.now(timezone.utc).isoformat(),
        "transaction_date": datetime.now(timezone.utc).isoformat(),
        "state": "Delhi",
        "district": "South Delhi",
        "city": "New Delhi",
        "area": "Saket",
        "latitude": 28.5244,
        "longitude": 77.2100,
        "status": "reported",
        "description": "Victim scammed via fraudulent UPI payment request link.",
        "source": "National Cyber Crime Reporting Portal",
    }
    # Create complaint
    create_res = await client.post("/api/v1/complaints", json=payload, headers=admin_token_headers)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["fraud_type"] == "UPI Fraud"
    assert created_data["amount"] == 75000.0
    complaint_id = created_data["id"]

    # Retrieve complaint
    get_res = await client.get(f"/api/v1/complaints/{complaint_id}", headers=admin_token_headers)
    assert get_res.status_code == 200
    assert get_res.json()["district"] == "South Delhi"


@pytest.mark.asyncio
async def test_list_and_filter_complaints(client: AsyncClient, admin_token_headers: dict):
    # Seed one complaint
    payload = {
        "fraud_type": "ATM Fraud",
        "amount": 25000.0,
        "complaint_date": datetime.now(timezone.utc).isoformat(),
        "transaction_date": datetime.now(timezone.utc).isoformat(),
        "state": "Maharashtra",
        "district": "Mumbai City",
        "city": "Mumbai",
        "latitude": 18.9200,
        "longitude": 72.8200,
        "status": "under_investigation",
    }
    await client.post("/api/v1/complaints", json=payload, headers=admin_token_headers)

    # Filter by fraud_type
    res = await client.get("/api/v1/complaints?fraud_type=ATM Fraud", headers=admin_token_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert any(item["fraud_type"] == "ATM Fraud" for item in data["items"])


@pytest.mark.asyncio
async def test_update_complaint_status(client: AsyncClient, admin_token_headers: dict):
    payload = {
        "fraud_type": "Card Fraud",
        "amount": 50000.0,
        "complaint_date": datetime.now(timezone.utc).isoformat(),
        "transaction_date": datetime.now(timezone.utc).isoformat(),
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "city": "Bengaluru",
        "latitude": 12.9700,
        "longitude": 77.6400,
        "status": "reported",
    }
    create_res = await client.post("/api/v1/complaints", json=payload, headers=admin_token_headers)
    comp_id = create_res.json()["id"]

    patch_res = await client.patch(
        f"/api/v1/complaints/{comp_id}/status",
        json={"status": "resolved", "remarks": "Fund freeze executed successfully via 1930 nodal desk."},
        headers=admin_token_headers,
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "resolved"
