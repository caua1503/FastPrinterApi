import secrets
import string
import time
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_config
from app.models.auth_model import RefreshToken
from app.models.user_model import UserApiKey

config = get_config()  # pyright: ignore

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_random_code(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    code = "".join(secrets.choice(characters) for _ in range(length))
    return code


def generate_api_key() -> str:
    api_key = f"api_key_{generate_random_code(64)}"
    return api_key


async def verify_api_key_db(session: AsyncSession, api_key: str) -> bool:
    existing_api_key = await session.scalar(select(UserApiKey).where(UserApiKey.api_key == api_key))

    if existing_api_key is None:
        return False

    return True


async def get_api_key(session: AsyncSession) -> str:
    while True:
        api_key = generate_api_key()
        existing_api_key = await verify_api_key_db(session, api_key)
        if not existing_api_key:
            return api_key


def create_access_token(data: dict) -> str:
    expires_delta: timedelta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    issued_at = time.time()
    to_encode.update({"exp": expire})
    to_encode.update({"iat": issued_at})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(session: AsyncSession):
    max_attempts = 20
    length_token = 128

    for _ in range(max_attempts):
        refresh_token = generate_random_code(length_token)
        query = select(RefreshToken).where(RefreshToken.token == refresh_token)
        result = await session.execute(query)
        refresh_token_obj = result.scalar_one_or_none()

        if not refresh_token_obj:
            return refresh_token

    raise RuntimeError("Failed to generate unique refresh token after 20 attempts")
