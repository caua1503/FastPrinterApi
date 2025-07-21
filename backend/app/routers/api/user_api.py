from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.user_schema import (
    UserApiKeySchema,
    UserCreateSchema,
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
)

user_router = APIRouter()


@user_router.post("/", response_model=UserPublicSchema, status_code=HTTPStatus.CREATED)
async def api_create_user(session: Annotated[AsyncSession, Depends(get_session)], user: UserCreateSchema):
    new_user = await create_user(session, user)
    return UserPublicSchema(
        id=new_user.id,
        login=new_user.login,
        name=new_user.name,
    )


@user_router.delete("/", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_user(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    await delete_user(session, current_user.id)


@user_router.put("/", response_model=UserPublicSchema, status_code=HTTPStatus.OK)
async def api_update_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserUpdateSchema,
    current_user=has_access(usage_api_key=False),
):
    return await update_user(session, current_user.id, user)


@user_router.put("/change-password", status_code=HTTPStatus.NO_CONTENT)
async def api_update_user_password(
    session: Annotated[AsyncSession, Depends(get_session)],
    password: UserNewPasswordSchema,
    current_user=has_access(usage_api_key=False),
):
    return await update_user_password(session, current_user.id, password)


@user_router.get("/api-key", response_model=List[UserApiKeySchema], status_code=HTTPStatus.OK)
async def api_get_api_key_from_user_id(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(UsersRoleSchema.member, usage_api_key=False),
):
    return await get_api_key_from_user_id(session, current_user.id)


@user_router.post("/new-api-key", response_model=UserApiKeySchema, status_code=HTTPStatus.CREATED)
async def api_get_api_key(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    return await create_api_key(session, current_user.id)


@user_router.post("/first-access", status_code=HTTPStatus.ACCEPTED)
async def api_update_first_access(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(usage_api_key=False)
):
    return await update_first_access(session, current_user.id)