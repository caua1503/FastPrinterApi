from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import create_access_token, verify_password
from app.models.user_model import User
from app.schemas.token_schema import TokenSchema


async def get_token_jwt(form_data: OAuth2PasswordRequestForm, session: AsyncSession):
    user = await session.scalar(
        select(User).options(selectinload(User.configuration)).where(User.login == form_data.username)
    )

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invalid credencials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invalid credencials")

    data = {
        "sub": str(user.id),
        "first_access": user.configuration.first_access,
    }

    token = TokenSchema(
        access_token=create_access_token(data),
        token_type="bearer",
    )

    return token


async def refresh_token(current_user: User):
    data = {
        "sub": str(current_user.id),
        "first_access": current_user.configuration.first_access,
    }

    token = TokenSchema(
        access_token=create_access_token(data),
        token_type="bearer",
    )

    return token
