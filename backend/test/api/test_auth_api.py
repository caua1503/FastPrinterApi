from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from app.models.user_model import User


@pytest.mark.asyncio
async def test_auth_api_success(user: User, client: TestClient):
    """Testa autenticação com credenciais válidas"""
    response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    assert data["refresh_token"] is not None


@pytest.mark.asyncio
async def test_auth_api_invalid_username(client: TestClient):
    """Testa autenticação com usuário inválido"""
    response = client.post("/api/v1/auth/token", data={"username": "invalid_user", "password": "any_password"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "invalid credencials"


@pytest.mark.asyncio
async def test_auth_api_invalid_password(user: User, client: TestClient):
    """Testa autenticação com senha inválida"""
    response = client.post("/api/v1/auth/token", data={"username": user.login, "password": "wrong_password"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "invalid credencials"


@pytest.mark.asyncio
async def test_auth_api_missing_username(client: TestClient):
    """Testa autenticação sem fornecer username"""
    response = client.post("/api/v1/auth/token", data={"password": "any_password"})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_auth_api_missing_password(user: User, client: TestClient):
    """Testa autenticação sem fornecer password"""
    response = client.post("/api/v1/auth/token", data={"username": user.login})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_auth_api_with_refresh_flag(user: User, client: TestClient):
    """Testa autenticação com flag refresh ativada"""
    response = client.post(
        "/api/v1/auth/token", data={"username": user.login, "password": user.password, "refresh": True}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    assert data["refresh_token"] is not None


@pytest.mark.asyncio
async def test_refresh_token_success(user: User, client: TestClient):
    """Testa renovação de token com refresh token válido"""

    auth_response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})
    refresh_token = auth_response.json()["refresh_token"]

    response = client.post("/api/v1/auth/refresh-token", json={"refresh_token_str": refresh_token})

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    assert "refresh_token" not in data


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: TestClient):
    """Testa renovação com refresh token inválido"""
    response = client.post("/api/v1/auth/refresh-token", json={"refresh_token_str": "invalid_refresh_token"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Invalid or revoked refresh token"


@pytest.mark.asyncio
async def test_refresh_token_missing(client: TestClient):
    """Testa renovação sem fornecer refresh token"""
    response = client.post("/api/v1/auth/refresh-token", json={})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_logout_success(user: User, client: TestClient):
    """Testa logout com token válido"""
    auth_response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})
    access_token = auth_response.json()["access_token"]
    refresh_token = auth_response.json()["refresh_token"]

    response = client.request(
        "GET",
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token_str": refresh_token},
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_logout_invalid_refresh_token(user: User, client: TestClient):
    """Testa logout com refresh token inválido"""
    auth_response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})
    access_token = auth_response.json()["access_token"]

    response = client.request(
        "GET",
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token_str": "invalid_refresh_token"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Token not found"


@pytest.mark.asyncio
async def test_logout_missing_authorization(client: TestClient):
    """Testa logout sem token de autorização"""
    response = client.request("GET", "/api/v1/auth/logout", json={"refresh_token_str": "any_refresh_token"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_logout_missing_refresh_token(user: User, client: TestClient):
    """Testa logout sem fornecer refresh token"""
    auth_response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})
    access_token = auth_response.json()["access_token"]

    response = client.get("/api/v1/auth/logout", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_refresh_token_after_logout(user: User, client: TestClient):
    """Testa que refresh token não funciona após logout"""
    auth_response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})
    access_token = auth_response.json()["access_token"]
    refresh_token = auth_response.json()["refresh_token"]

    logout_response = client.request(
        "GET",
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token_str": refresh_token},
    )
    assert logout_response.status_code == HTTPStatus.OK

    response = client.post("/api/v1/auth/refresh-token", json={"refresh_token_str": refresh_token})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Invalid or revoked refresh token"


@pytest.mark.asyncio
async def test_auth_admin_user(admin_user: User, client: TestClient):
    """Testa autenticação com usuário admin"""
    response = client.post("/api/v1/auth/token", data={"username": admin_user.login, "password": admin_user.password})

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    assert data["refresh_token"] is not None
