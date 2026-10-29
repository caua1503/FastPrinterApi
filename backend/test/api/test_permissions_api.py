from http import HTTPStatus

import pytest

from app.models.user_model import PermissionApiKey, PermissionUser
from app.schemas.permission_schema import (
    ListPermissionApiKeySchema,
    ListPermissionUserSchema,
    PermissionApiKeySchemaDB,
    PermissionUserSchemaDB,
)


@pytest.mark.asyncio
async def test_get_permissions_user(client, admin_token, session):
    perm = PermissionUser(name="Test Perm", code="test.perm", description="Desc")
    session.add(perm)
    await session.commit()

    response = client.get("/api/v1/permissions/user", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = ListPermissionUserSchema.model_validate(data)
    assert validated.total >= 1
    assert any(p.code == "test.perm" for p in validated.permissions)


@pytest.mark.asyncio
async def test_get_permissions_api_key(client, admin_token, session):
    perm = PermissionApiKey(name="API Key Perm", code="test.apikey", description="Desc")
    session.add(perm)
    await session.commit()

    response = client.get("/api/v1/permissions/api_key", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = ListPermissionApiKeySchema.model_validate(data)
    assert validated.total >= 1
    assert any(p.code == "test.apikey" for p in validated.permissions)


@pytest.mark.asyncio
async def test_create_permission_user(client, admin_token):
    payload = {"name": "New User Perm", "code": "new.user.perm", "description": "New Desc"}
    response = client.post(
        "/api/v1/permissions/user",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionUserSchemaDB.model_validate(data)
    assert validated.code == "new.user.perm"


@pytest.mark.asyncio
async def test_create_permission_api_key(client, admin_token):
    payload = {"name": "New Key Perm", "code": "new.key.perm", "description": "New Desc"}
    response = client.post(
        "/api/v1/permissions/api_key",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionApiKeySchemaDB.model_validate(data)
    assert validated.code == "new.key.perm"


@pytest.mark.asyncio
async def test_update_permission_user(client, admin_token, session):
    perm = PermissionUser(name="Old Name", code="update.user.perm", description="Old Desc")
    session.add(perm)
    await session.commit()
    await session.refresh(perm)

    payload = {"name": "Updated Name", "description": "Updated Desc"}
    response = client.put(
        f"/api/v1/permissions/user/{perm.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionUserSchemaDB.model_validate(data)
    assert validated.name == "Updated Name"


@pytest.mark.asyncio
async def test_update_permission_api_key(client, admin_token, session):
    perm = PermissionApiKey(name="Old Key Name", code="update.key.perm", description="Old Desc")
    session.add(perm)
    await session.commit()
    await session.refresh(perm)

    payload = {"name": "Updated Key Name", "description": "Updated Desc"}
    response = client.put(
        f"/api/v1/permissions/api_key/{perm.id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionApiKeySchemaDB.model_validate(data)
    assert validated.name == "Updated Key Name"


@pytest.mark.asyncio
async def test_delete_permission_user(client, admin_token, session):
    perm = PermissionUser(name="Del User Perm", code="del.user.perm", description="Desc")
    session.add(perm)
    await session.commit()
    await session.refresh(perm)

    response = client.delete(
        f"/api/v1/permissions/user/{perm.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionUserSchemaDB.model_validate(data)
    assert validated.id == perm.id


@pytest.mark.asyncio
async def test_delete_permission_api_key(client, admin_token, session):
    perm = PermissionApiKey(name="Del Key Perm", code="del.key.perm", description="Desc")
    session.add(perm)
    await session.commit()
    await session.refresh(perm)

    response = client.delete(
        f"/api/v1/permissions/api_key/{perm.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    validated = PermissionApiKeySchemaDB.model_validate(data)
    assert validated.id == perm.id
