from http import HTTPStatus

import pytest

from app.models.user_model import UserApiKey, UsersRoleSchema
from app.services.user_service import get_api_key_from_user_id


@pytest.mark.asyncio
async def test_api_key_immediate_revocation(client, admin_user, session):
    key = "test_api_key_revocation_123"
    api_key_obj = UserApiKey(user_id=admin_user.id, api_key=key)
    session.add(api_key_obj)
    await session.commit()

    resp = client.get("/api/v1/core/current/info/printer", headers={"X-Api-Key": key})
    assert resp.status_code == HTTPStatus.OK

    await session.delete(api_key_obj)
    await session.commit()

    resp = client.get("/api/v1/core/current/info/printer", headers={"X-Api-Key": key})
    assert resp.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_role_downgrade_immediate(client, admin_user, admin_token, session):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/core/current/info/printer", headers=headers)
    assert resp.status_code == HTTPStatus.OK

    admin_user.role = UsersRoleSchema.guest
    session.add(admin_user)
    await session.commit()

    resp = client.get("/api/v1/core/current/info/printer", headers=headers)
    assert resp.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_get_api_key_reflects_new_key(member_user, session):
    key1 = UserApiKey(user_id=member_user.id, api_key="key_1")
    session.add(key1)
    await session.commit()

    keys = await get_api_key_from_user_id(session, member_user.id)
    assert len(keys) == 1
    assert keys[0].api_key == "key_1"

    key2 = UserApiKey(user_id=member_user.id, api_key="key_2")
    session.add(key2)
    await session.commit()

    keys = await get_api_key_from_user_id(session, member_user.id)
    expected_keys_count = 2
    assert len(keys) == expected_keys_count
