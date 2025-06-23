from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.database_helper import get_session
from app.schemas.user_schema import (
    UserCreateSchema,
    UserPasswordSchema,
    UserPublicSchema,
    UserUpdateSchema,
)
from app.services.user_service import (
    create_user,
    delete_user,
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


@user_router.put("/password/{id}", status_code=HTTPStatus.NO_CONTENT)
async def api_update_user_password(
    session: Annotated[AsyncSession, Depends(get_session)], id: int, password: UserPasswordSchema
):
    return await update_user_password(session, id, password)


# @user_router.put("/new-api-key/{id}", response_model=UserApiKey, status_code=HTTPStatus.OK)
# async def api_update_api_key(session: Annotated[AsyncSession, Depends(get_session)], id: int):
#     return await update_api_key(session, id)
