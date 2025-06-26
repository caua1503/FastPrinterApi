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
    update_user,
    update_user_password,
)

user_router = APIRouter()


@user_router.post("/", response_model=UserPublicSchema, status_code=HTTPStatus.CREATED)
async def api_create_user(session: Annotated[AsyncSession, Depends(get_session)], user: UserCreateSchema):
    return await create_user(session, user)


@user_router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_user(session: Annotated[AsyncSession, Depends(get_session)], id: int):
    await delete_user(session, id)


@user_router.put("/{id}", response_model=UserPublicSchema, status_code=HTTPStatus.OK)
async def api_update_user(session: Annotated[AsyncSession, Depends(get_session)], id: int, user: UserUpdateSchema):
    return await update_user(session, id, user)


@user_router.put("/change-password/", status_code=HTTPStatus.NO_CONTENT)
async def api_update_user_password(
    session: Annotated[AsyncSession, Depends(get_session)],
    password: UserNewPasswordSchema,
    current_user=has_access(),
):
    return await update_user_password(session, current_user.id, password)


@user_router.get("/api-key", response_model=List[UserApiKeySchema], status_code=HTTPStatus.OK)
async def api_get_api_key_from_user_id(
    session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access(UsersRoleSchema.member)
):
    return await get_api_key_from_user_id(session, current_user.id)


@user_router.get("/new-api-key/", response_model=UserApiKeySchema, status_code=HTTPStatus.OK)
async def api_get_api_key(session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()):
    return await create_api_key(session, current_user.id)
