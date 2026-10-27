from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_config
from app.helpers.database_helper import get_session
from app.models.user_model import (
    PermissionApiKey,
    PermissionUser,
    User,
    UserApiKey,
    UserPermission,
    UsersRoleSchema,
)

config = get_config()  # pyright: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)
api_key_scheme = APIKeyHeader(name="X-Api-Key", auto_error=False)


async def _user_from_bearer(token: str, session: AsyncSession) -> User | None:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        parsed_user_id = int(user_id)
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    try:
        result = await session.execute(select(User).where(User.id == parsed_user_id))
        return result.scalar_one_or_none()
    except OperationalError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error connecting to database",
        )


async def _user_from_api_key(api_key: str, session: AsyncSession) -> User | None:
    try:
        stmt = select(User).join(User.api_keys).where(UserApiKey.api_key == api_key)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except OperationalError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error connecting to database",
        )


def has_access(
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

    async def dependency(
        token: Optional[str] = Depends(oauth2_scheme),
        api_key: Optional[str] = Depends(api_key_scheme),
        session: AsyncSession = Depends(get_session),
    ) -> User:
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
            user = await _user_from_bearer(token, session)
        elif api_key:
            auth_type = "apikey"
            user = await _user_from_api_key(api_key, session)
        else:
            raise error_auth

        if not user:
            raise error_auth

        error_forbidden = HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions",
        )

        if user.role == UsersRoleSchema.admin:
            return user

        if user.role != role:
            raise error_forbidden

        if auth_type == "bearer" and required_user_code:
            stmt = select(PermissionUser.code).join(UserPermission).where(UserPermission.user_id == user.id)
            permissions_result = await session.execute(stmt)
            user_permissions = {code for (code,) in permissions_result}
            if required_user_code not in user_permissions:
                raise error_forbidden

        if auth_type == "apikey" and required_api_scope:
            stmt = select(PermissionApiKey.code).join(UserApiKey).where(UserApiKey.user_id == user.id)
            permissions_result = await session.execute(stmt)
            api_permissions = {code for (code,) in permissions_result}
            if required_api_scope not in api_permissions:
                raise error_forbidden

        return user

    return Depends(dependency)
