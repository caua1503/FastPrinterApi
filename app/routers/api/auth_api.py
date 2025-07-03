from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.token_schema import TokenSchema
from app.services.auth_service import get_token_jwt, refresh_token

auth_router = APIRouter()


@auth_router.post("/token", response_model=TokenSchema)
async def api_get_token_jwt(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await get_token_jwt(form_data, session)


@auth_router.get("/refresh-token", response_model=TokenSchema)
async def api_refresh_token(current_user=has_access()):
    return await refresh_token(current_user)
