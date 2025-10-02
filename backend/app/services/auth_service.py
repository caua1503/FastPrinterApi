from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_config
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.auth_model import RefreshToken
from app.models.user_model import User
from app.schemas.token_schema import OAuth2PasswordAndRefreshRequestForm, RefreshTokenSchema, TokenSchema

config = get_config()


async def get_token_jwt(form_data: OAuth2PasswordAndRefreshRequestForm, request: Request, session: AsyncSession):
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

    if form_data.refresh:
        expires_at = datetime.now(timezone.utc) + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        expires_at = datetime.now(timezone.utc) + timedelta(days=1)

    access_token = create_access_token(data)
    refresh_token = await create_refresh_token(session)

    ip_address = request.client.host
    user_agent = request.headers.get("User-Agent")

    refresh_token_obj = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
        is_revoked=False,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    session.add(refresh_token_obj)
    await session.commit()
    await session.refresh(refresh_token_obj)

    return RefreshTokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def refresh_token(refresh_token_str: str, session: AsyncSession):
    """Valida e gera um novo access token a partir de um refresh token válido."""

    token_obj = await session.scalar(select(RefreshToken).where(RefreshToken.token == refresh_token_str))

    if not token_obj or token_obj.is_revoked:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid or revoked refresh token")

    expires_at = token_obj.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid or revoked refresh token")

    user = await session.scalar(
        select(User).options(selectinload(User.configuration)).where(User.id == token_obj.user_id)
    )

    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid or revoked refresh token")

    data = {
        "sub": str(user.id),
        "first_access": user.configuration.first_access,
    }
    access_token = create_access_token(data)

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )


async def logout(user_id: int, session: AsyncSession, refresh_token_str: str):
    exist_refresh_token = await session.scalar(
        select(RefreshToken).where(RefreshToken.user_id == user_id).where(RefreshToken.token == refresh_token_str)
    )

    if not exist_refresh_token:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Token not found")

    exist_refresh_token.is_revoked = True

    await session.commit()
    await session.refresh(exist_refresh_token)
