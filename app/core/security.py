import random
import string
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Config
from app.helpers.database_helper import get_redis_client, get_session
from app.helpers.redis_helper import (
    redis_get_value,
    # redis_set_value,
)
from app.models.user_model import (
    PermissionApiKey,
    PermissionUser,
    User,
    UserApiKey,
    UserPermission,
    UsersRoleSchema,
)

config = Config()  # pyright: ignore

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)
api_key_scheme = APIKeyHeader(name="X-Api-Key", auto_error=False)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_random_code(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(length))
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
        print(api_key)
        existing_api_key = await verify_api_key_db(session, api_key)
        if not existing_api_key:
            return api_key


async def get_jtw_code() -> str:
    redis_client = await get_redis_client()

    while True:
        jwt_code = generate_random_code(32)
        existing_jwt_code = await redis_get_value(jwt_code, redis_client)

        if not existing_jwt_code:
            # await redis_set_value(jwt_code, jwt_code, redis_client)
            return jwt_code


def create_access_token(data: dict) -> str:
    expires_delta: timedelta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def has_access(
    role: UsersRoleSchema = UsersRoleSchema.member,
    required_user_code: Optional[str] = None,
    required_api_scope: Optional[str] = None,
) -> User:
    """
    Dependency to handle user access control.
    It verifies authentication via JWT (Bearer) or API Key and then checks
    for role and specific permissions.
    - Admins bypass all role and permission checks.
    - `required_user_code` is checked for JWT authenticated sessions.
    - `required_api_scope` is checked for API Key authenticated sessions.
    """

    async def dependency(  # noqa: PLR0912
        token: Optional[str] = Depends(oauth2_scheme),
        api_key: Optional[str] = Depends(api_key_scheme),
        session: AsyncSession = Depends(get_session),
    ):
        user: Optional[User] = None
        auth_type: Optional[str] = None
        error_auth = HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="Invalid or expired token",)
        if token:
            auth_type = "bearer"
            try:
                payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
                user_id = payload.get("sub")

                if not user_id:
                    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

                result = await session.execute(select(User).where(User.id == int(user_id)))
                user = result.scalar_one_or_none()

            except jwt.DecodeError:
                raise error_auth
            except jwt.ExpiredSignatureError:
                raise error_auth

        elif api_key:
            auth_type = "apikey"
            stmt = select(User).join(User.api_keys).where(UserApiKey.api_key == api_key)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        if not auth_type:
            raise error_auth

        if not user:
            raise error_auth

        # Authorization checks
        if user.role == UsersRoleSchema.admin:
            return user  # Admins can do anything

        if user.role != role:
            raise error_auth

        # Permission checks based on authentication method
        if auth_type == "bearer" and required_user_code:
            stmt = select(PermissionUser.code).join(UserPermission).where(UserPermission.user_id == user.id)
            permissions_result = await session.execute(stmt)
            user_permissions = {code for (code,) in permissions_result}
            if required_user_code not in user_permissions:
                raise error_auth

        if auth_type == "apikey" and required_api_scope:
            stmt = select(PermissionApiKey.code).join(UserApiKey).where(UserApiKey.user_id == user.id)
            permissions_result = await session.execute(stmt)
            api_permissions = {code for (code,) in permissions_result}
            if required_api_scope not in api_permissions:
                raise error_auth

        return user

    return Depends(dependency)
