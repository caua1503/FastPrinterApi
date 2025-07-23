from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_all_printers_maintenance_info, get_printer_maintenance_info
from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.filter_schema import FilterBase
from app.schemas.maintenance_schema import ListPrinterMaintenanceInfoSchema
from app.schemas.user_schema import UsersRoleSchema
from app.services.core_service import get_printer_maintenance_info_service

core_router = APIRouter()


@core_router.get("/current/info/printer", summary="Get all printers maintenance info")
async def api_current_get_all_printers_maintenance_info(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterBase, Query()],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    # return await asyncio.to_thread(get_all_printers_maintenance_info(session, limit))
    return await get_all_printers_maintenance_info(session, filters)


@core_router.get("/current/info/printer/{printer_id}", summary="Get a printer maintenance info")
async def api_current_get_printer_maintenance_info(
    printer_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterBase, Query()],
    current_user=has_access(role=UsersRoleSchema.admin),
):
    # return await asyncio.to_thread(get_printer_maintenance_info(printer_id, session, limit))
    return await get_printer_maintenance_info(printer_id, session, filters)


@core_router.get(
    "/info/printer", summary="Get all printers maintenance info", response_model=ListPrinterMaintenanceInfoSchema
)
async def api_get_all_printer_maintenance_info(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterBase, Query()],
    current_user=has_access(),
): ...


@core_router.get("/info/printer/{printer_id}", summary="Get a printer maintenance info")
async def api_get_printer_maintenance_info(
    printer_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterBase, Query()],
    current_user=has_access(),
):
    # return await asyncio.to_thread(get_printer_maintenance_info_service(printer_id, session, limit))
    return await get_printer_maintenance_info_service(printer_id, session, filters)
