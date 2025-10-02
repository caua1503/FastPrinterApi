from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session_logs
from app.schemas.filter_schema import FilterLogApiKey, FilterLogApiKeyAdmin, FilterLogSystem, FilterLogUser
from app.schemas.logs_schema import (
    ListApiKeyLogSchema,
    ListSystemLogSchema,
    ListUserLogSchema,
)
from app.schemas.user_schema import UsersRoleSchema
from app.services.logs_service import get_api_key_logs, get_system_logs, get_user_logs

log_router = APIRouter()


@log_router.get("/system", summary="Get all historys of system", response_model=ListSystemLogSchema)
async def api_get_system_log(
    session: Annotated[AsyncSession, Depends(get_session_logs)],
    filters: Annotated[FilterLogSystem, Query()],
    current_user=has_access(UsersRoleSchema.admin),
):
    return await get_system_logs(session, filters)


@log_router.get("/user", summary="Get all historys of user", response_model=ListUserLogSchema)
async def api_get_user_log(
    session: Annotated[AsyncSession, Depends(get_session_logs)],
    filters: Annotated[FilterLogUser, Query()],
    current_user=has_access(UsersRoleSchema.admin),
):
    return await get_user_logs(session, filters)


@log_router.get("/api", summary="Get all historys of api", response_model=ListApiKeyLogSchema)
async def api_get_api_log(
    session: Annotated[AsyncSession, Depends(get_session_logs)],
    filters: Annotated[FilterLogApiKey, Query()],
    current_user=has_access(),
):
    return await get_api_key_logs(session, filters, current_user.id)


@log_router.get("/api/admin", summary="Get all historys of api (admin)", response_model=ListApiKeyLogSchema)
async def api_get_api_log_admin(
    session: Annotated[AsyncSession, Depends(get_session_logs)],
    filters: Annotated[FilterLogApiKeyAdmin, Query()],
    current_user=has_access(UsersRoleSchema.admin),
):
    return await get_api_key_logs(session, filters)
