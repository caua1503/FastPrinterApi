import asyncio
from http import HTTPStatus
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_config
from app.helpers.database_helper import get_redis_client, get_session
from app.helpers.redis_helper import redis_get_value_pydantic, redis_set_value_pydantic
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
    ) -> User:
        try:
            redis_client = await get_redis_client()
        except Exception:
            redis_client = None

        user: Optional[User] = None
        auth_type: Optional[str] = None
        redis_usage: bool = False

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

                if redis_client:
                    try:
                        user_redis = await redis_get_value_pydantic(
                            key=f"user_id_{user_id}",
                            model=User,
                            redis_client=redis_client,
                        )
                    except Exception:
                        user_redis = None
                else:
                    user_redis = None

                if user_redis:
                    user = user_redis
                    redis_usage = True
                else:
                    result = await session.execute(select(User).where(User.id == int(user_id)))
                    user = result.scalar_one_or_none()

            except jwt.DecodeError:
                raise error_auth
            except jwt.ExpiredSignatureError:
                raise error_auth
            except OperationalError:
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="Error connecting to database",
                )
            except Exception:
                raise error_auth

        elif api_key:
            auth_type = "apikey"

            if redis_client:
                try:
                    user_redis = await redis_get_value_pydantic(
                        key=f"user_id_api_{api_key}",
                        model=User,
                        valid_json=False,
                        redis_client=redis_client,
                    )
                except Exception:
                    user_redis = None
            else:
                user_redis = None

            if user_redis:
                user = user_redis
                redis_usage = True
            else:
                stmt = select(User).join(User.api_keys).where(UserApiKey.api_key == api_key)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

            if user:
                pass

        if not auth_type:
            raise error_auth

        if not user:
            raise error_auth

        if not redis_usage:
            # Cache para JWT token
            if auth_type == "bearer" and redis_client:
                asyncio.create_task(
                    redis_set_value_pydantic(
                        key=f"user_id_{user.id}",
                        value=user,
                        valid_json=False,
                        redis_client=redis_client,
                        ex=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Converter para segundos
                    )
                )
            # Cache para API Key
            elif auth_type == "apikey" and redis_client:
                asyncio.create_task(
                    redis_set_value_pydantic(
                        key=f"user_id_api_{api_key}",
                        value=user,
                        valid_json=False,
                        redis_client=redis_client,
                        ex=3600,  # 1 hora para API keys
                    )
                )

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
                pass

        return user

    return Depends(dependency)
