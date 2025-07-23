from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.user_schema import (
    UserApiKeySchema,
    UserCreateAdminSchema,
    UserCreateSchema,
    UserNewPasswordAdminSchema,
    UserNewPasswordSchema,
    UserPublicSchema,
    UsersRoleSchema,
    UserUpdateSchema,
)
from app.services.user_service import (
    create_api_key,
    create_user,
    delete_user,
    get_api_key_from_user_id,
    update_first_access,
    update_user,
    update_user_password,
    update_user_password_admin,
)

user_router = APIRouter()


@user_router.post("/", summary="Create a new user", response_model=UserPublicSchema, status_code=HTTPStatus.CREATED)
async def api_create_user(session: Annotated[AsyncSession, Depends(get_session)], user: UserCreateSchema):
    new_user = await create_user(session, user)
    return UserPublicSchema(
        id=new_user.id,
        login=new_user.login,
        name=new_user.name,
    )


@user_router.delete("/", summary="Delete a user", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_user(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    await delete_user(session, current_user.id)


@user_router.put("/", summary="Update a user", response_model=UserPublicSchema, status_code=HTTPStatus.OK)
async def api_update_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserUpdateSchema,
    current_user=has_access(usage_api_key=False),
):
    return await update_user(session, current_user.id, user)


@user_router.put("/change-password", summary="Update a user password", status_code=HTTPStatus.NO_CONTENT)
async def api_update_user_password(
    session: Annotated[AsyncSession, Depends(get_session)],
    password: UserNewPasswordSchema,
    current_user=has_access(usage_api_key=False),
):
    return await update_user_password(session, current_user.id, password)


@user_router.get(
    "/api-key", summary="Get all api keys of user", response_model=List[UserApiKeySchema], status_code=HTTPStatus.OK
)
async def api_get_api_key_from_user_id(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(UsersRoleSchema.member, usage_api_key=False),
):
    return await get_api_key_from_user_id(session, current_user.id)


@user_router.post(
    "/new-api-key", summary="Create a new api key", response_model=UserApiKeySchema, status_code=HTTPStatus.CREATED
)
async def api_get_api_key(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    return await create_api_key(session, current_user.id)


@user_router.post("/first-access", summary="Update first access", status_code=HTTPStatus.ACCEPTED)
async def api_update_first_access(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    return await update_first_access(session, current_user.id)


@user_router.post(
    "/admin", summary="Create a new user (admin)", response_model=UserPublicSchema, status_code=HTTPStatus.CREATED
)
async def api_create_user_admin(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserCreateAdminSchema,
    current_user=has_access(UsersRoleSchema.admin, usage_api_key=False),
):
    new_user = await create_user(session, user)
    return UserPublicSchema(
        id=new_user.id,
        login=new_user.login,
        name=new_user.name,
    )


@user_router.delete("/admin", summary="Delete a user (admin)", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_user_admin(
    id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(UsersRoleSchema.admin, usage_api_key=False),
):
    await delete_user(session, id)


@user_router.put("/admin", summary="Update a user (admin)", response_model=UserPublicSchema, status_code=HTTPStatus.OK)
async def api_update_user_admin(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserUpdateSchema,
    id: int,
    current_user=has_access(UsersRoleSchema.admin, usage_api_key=False),
):
    return await update_user(session, id, user)


@user_router.put("/admin/change-password", summary="Update a user password (admin)", status_code=HTTPStatus.NO_CONTENT)
async def api_update_user_password_admin(
    session: Annotated[AsyncSession, Depends(get_session)],
    password: UserNewPasswordAdminSchema,
    id: int,
    current_user=has_access(UsersRoleSchema.admin, usage_api_key=False),
):
    return await update_user_password_admin(session, id, password)
