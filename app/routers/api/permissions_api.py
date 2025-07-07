from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.permission_schema import (
    PermissionApiKeySchema,
    PermissionApiKeyUpdateSchema,
    PermissionUserSchema,
    PermissionUserUpdateSchema,
)
from app.schemas.user_schema import UsersRoleSchema
from app.services.permissions_service import (
    create_permission_api_key,
    create_permission_user,
    delete_permission_api_key,
    delete_permission_user,
    get_all_permissions_api_key,
    get_all_permissions_user,
    update_permission_api_key,
    update_permission_user,
)

permissions_router = APIRouter()


@permissions_router.get("/user")
async def api_get_all_permissions_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await get_all_permissions_user(session)
    return result


@permissions_router.get("/api_key")
async def api_get_all_permissions_api_key(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await get_all_permissions_api_key(session)
    return result


@permissions_router.post("/user")
async def api_create_permission_user(
    permission: PermissionUserSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await create_permission_user(permission, session)
    return result


@permissions_router.post("/api_key")
async def api_create_permission_api_key(
    permission: PermissionApiKeySchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await create_permission_api_key(permission, session)
    return result


@permissions_router.put("/user/{permission_id}")
async def api_update_permission_user(
    permission_id: int,
    permission: PermissionUserUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await update_permission_user(permission_id, permission, session)
    return result


@permissions_router.put("/api_key/{permission_id}")
async def api_update_permission_api_key(
    permission_id: int,
    permission: PermissionApiKeyUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await update_permission_api_key(permission_id, permission, session)
    return result


@permissions_router.delete("/user/{permission_id}")
async def api_delete_permission_user(
    permission_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await delete_permission_user(permission_id, session)
    return result


@permissions_router.delete("/api_key/{permission_id}")
async def api_delete_permission_api_key(
    permission_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    result = await delete_permission_api_key(permission_id, session)
    return result
