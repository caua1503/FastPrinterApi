from http import HTTPStatus
from typing import Annotated

from app.core.security import verify_password
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.helpers.database_helper import get_session
from app.models.user_model import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()


@auth_router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await session.scalar(select(User).where(User.login == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas")

    return {"message": "Login realizado com sucesso"}
