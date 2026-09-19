"""Tests for Authentication endpoints."""

import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_admin_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin_test@crimetrace.ai", "password": "AdminPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_admin_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin_test@crimetrace.ai", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_current_user_me(client: AsyncClient, admin_token_headers: dict):
    response = await client.get("/api/v1/auth/me", headers=admin_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin_test@crimetrace.ai"
    assert data["role"] == "admin"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
