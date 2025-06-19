from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_all_printers_maintenance_info, get_printer_maintenance_info
from app.helpers.database_helper import get_session
from app.services.core_service import get_printer_maintenance_info_service

core_router = APIRouter()


@core_router.get("/current/info/printer/all")
async def api_current_get_all_printers_maintenance_info(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_all_printers_maintenance_info(session, limit))
    return get_all_printers_maintenance_info(session, limit)


@core_router.get("/current/info/printer/{printer_id}")
async def api_current_get_printer_maintenance_info(
    printer_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_printer_maintenance_info(printer_id, session, limit))
    return get_printer_maintenance_info(printer_id, session, limit)


@core_router.get("/info/printer/{printer_id}")
async def api_get_printer_maintenance_info(
    printer_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_printer_maintenance_info_service(printer_id, session, limit))
    return get_printer_maintenance_info_service(printer_id, session, limit)
