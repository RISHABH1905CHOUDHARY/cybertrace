"""Tests for Dashboard, Analytics, and Heatmap endpoints."""

from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_overview_and_kpis(client: AsyncClient, admin_token_headers: dict):
    # Insert a sample complaint
    payload = {
        "fraud_type": "UPI Fraud",
        "amount": 50000.0,
        "complaint_date": datetime.now(timezone.utc).isoformat(),
        "transaction_date": datetime.now(timezone.utc).isoformat(),
        "state": "Delhi",
        "district": "South Delhi",
        "city": "New Delhi",
        "latitude": 28.5400,
        "longitude": 77.2500,
        "status": "reported",
    }
    await client.post("/api/v1/complaints", json=payload, headers=admin_token_headers)

    # Test Dashboard Overview
    overview_res = await client.get("/api/v1/dashboard/overview", headers=admin_token_headers)
    assert overview_res.status_code == 200
    overview_data = overview_res.json()
    assert "kpis" in overview_data
    assert "fraud_distribution" in overview_data
    assert "top_districts" in overview_data
    assert overview_data["kpis"]["total_complaints"] >= 1


@pytest.mark.asyncio
async def test_heatmap_points_and_geojson(client: AsyncClient, admin_token_headers: dict):
    # Test heatmap points
    points_res = await client.get("/api/v1/heatmap/points", headers=admin_token_headers)
    assert points_res.status_code == 200
    points_data = points_res.json()
    assert isinstance(points_data, list)
    if len(points_data) > 0:
        assert "weight" in points_data[0]
        assert "latitude" in points_data[0]
        assert "longitude" in points_data[0]

    # Test GeoJSON endpoint
    geojson_res = await client.get("/api/v1/heatmap/geojson", headers=admin_token_headers)
    assert geojson_res.status_code == 200
    geojson_data = geojson_res.json()
    assert geojson_data["type"] == "FeatureCollection"
    assert "features" in geojson_data
