from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.models.user_model import User
from app.schemas.token_schema import OAuth2PasswordAndRefreshRequestForm, RefreshTokenSchema, TokenSchema
from app.services.auth_service import get_token_jwt, logout, refresh_token

auth_router = APIRouter()


@auth_router.post("/token", summary="Get a token", response_model=RefreshTokenSchema)
async def api_get_token_jwt(
    form_data: Annotated[OAuth2PasswordAndRefreshRequestForm, Depends()],
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
):

    return await get_token_jwt(form_data, request, session)


@auth_router.post("/refresh-token", summary="Refresh a token", response_model=TokenSchema)
async def api_refresh_token(
    session: Annotated[AsyncSession, Depends(get_session)],
    refresh_token_str: Annotated[str, Body(..., embed=True)],
):
    return await refresh_token(refresh_token_str, session)


@auth_router.get("/logout", summary="Logout")
async def api_logout(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, has_access(usage_api_key=False)],
    refresh_token_str: Annotated[str, Body(..., embed=True)],
):
    return await logout(current_user.id, session, refresh_token_str)
