from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_auth_api(user, client: TestClient):
    response = client.post("/api/v1/auth/token", data={"username": user.login, "password": user.password})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"
