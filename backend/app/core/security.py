import asyncio
import secrets
import string
import time
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Config
from app.core.task import task_create_api_key_log, task_create_system_log
from app.helpers.database_helper import get_session
from app.models.auth_model import RefreshToken
from app.models.user_model import (
    PermissionApiKey,
    PermissionUser,
    User,
    UserApiKey,
    UserPermission,
    UsersRoleSchema,
)
from app.schemas.logs_schema import ApiKeyActionSchema, ApiKeyLogSchema, LogLevelSchema, ServiceSchema, SystemLogSchema

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

    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail="Failed to generate unique refresh token after 20 attempts",
    )


async def log_api_key_usage(
    session: AsyncSession,
    api_key: str,
    user_id: int,
    request: Request,
) -> None:
    """
    Helper function to record API Key usage logs.

    Args:
        session: Database session (logs_database)
        api_key: API Key used
        user_id: User ID that used the API Key
        request: FastAPI Request object to capture the route
        action: Action performed (default: GET)
    """
    try:
        stmt_api_key = select(UserApiKey).where(UserApiKey.api_key == api_key)
        result_api_key = await session.execute(stmt_api_key)
        api_key_obj = result_api_key.scalar_one()
        http_method = request.method.upper()
        user_action = (
            ApiKeyActionSchema(http_method)
            if http_method in [action.value for action in ApiKeyActionSchema]
            else ApiKeyActionSchema.ANY
        )

        log_api_key = ApiKeyLogSchema(
            user_id=user_id,
            api_key_id=api_key_obj.id,
            action=user_action,
            route=str(request.url.path),
            timestamp=datetime.now(),
        )
        task_create_api_key_log.delay(**log_api_key.model_dump())
    except Exception as e:
        system_log = SystemLogSchema(
            message=f"Error logging API Key usage: {e}",
            service=ServiceSchema.OTHER,
            level=LogLevelSchema.ERROR,
            timestamp=datetime.now(),
        )
        task_create_system_log.delay(**system_log.model_dump())


def has_access(  # noqa: PLR0915
    role: UsersRoleSchema = UsersRoleSchema.member,
    required_user_code: Optional[str] = None,
    required_api_scope: Optional[str] = None,
    usage_bearer: bool = True,
    usage_api_key: bool = True,
) -> User:
    """
    Dependency to handle user access control.
    It verifies authentication via JWT (Bearer) or API Key and then checks
    for role and specific permissions.
    - Admins bypass all role and permission checks.
    - `required_user_code` is checked for JWT authenticated sessions.
    - `required_api_scope` is checked for API Key authenticated sessions.
    - `usage_bearer` is used to block bearer token authentication for a route.
    - `usage_api_key` is used to block API Key authentication for a route.
    """

    async def dependency(  # noqa: PLR0912, PLR0915
        request: Request,
        token: Optional[str] = Depends(oauth2_scheme),
        api_key: Optional[str] = Depends(api_key_scheme),
        session: AsyncSession = Depends(get_session),
    ):
        user: Optional[User] = None
        auth_type: Optional[str] = None
        error_auth = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid or expired token",
        )

        if token and not usage_bearer:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Bearer token authentication not allowed for this route",
            )

        if api_key and not usage_api_key:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="API Key authentication not allowed for this route",
            )

        if token:
            auth_type = "bearer"
            try:
                payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
                user_id = payload.get("sub")

                if not user_id:
                    raise error_auth

                result = await session.execute(select(User).where(User.id == int(user_id)))
                user = result.scalar_one_or_none()

            except jwt.DecodeError:
                raise error_auth
            except jwt.ExpiredSignatureError:
                raise error_auth
            except OperationalError as erro:
                from app.core.task import task_create_system_log  # noqa: PLC0415

                log = SystemLogSchema(
                    message="Error connecting to database",
                    description=str(erro),
                    level=LogLevelSchema.CRITICAL,
                    service=ServiceSchema.POSTGRES,
                    timestamp=datetime.now(),
                )
                task_create_system_log.delay(**log.model_dump())
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Error connecting to database",
                )
            except Exception:
                raise error_auth

        elif api_key:
            auth_type = "apikey"
            stmt = select(User).join(User.api_keys).where(UserApiKey.api_key == api_key)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                asyncio.create_task(log_api_key_usage(session, api_key, user.id, request))

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

            if api_key:
                asyncio.create_task(log_api_key_usage(session, api_key, user.id, request))

        return user

    return Depends(dependency)
