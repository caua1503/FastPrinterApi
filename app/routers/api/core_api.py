from typing import Annotated, List

from core import get_all_printers_maintenance_info, get_printer_maintenance_info
from fastapi import APIRouter, Depends
from helpers.db_helper import get_session
from schemas.core_schema import InfoPrinterAll
from services.core_service import get_printer_maintenance_info_service
from sqlalchemy.ext.asyncio import AsyncSession

core_router = APIRouter(prefix="/core", tags=["api - core"])


@core_router.get("/current/info/printer/all", response_model=List[InfoPrinterAll])
async def api_current_get_all_printers_maintenance_info(
    session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_all_printers_maintenance_info(session, limit))
    return get_all_printers_maintenance_info(session, limit)


@core_router.get("/current/info/printer/{impresora_id}")
async def api_current_get_printer_maintenance_info(
    impresora_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_printer_maintenance_info(impresora_id, session, limit))
    return get_printer_maintenance_info(impresora_id, session, limit)


@core_router.get("/info/printer/{impressora_id}")
async def api_get_printer_maintenance_info(
    impressora_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 6
):
    # return await asyncio.to_thread(get_printer_maintenance_info_service(impressora_id, session, limit))
    return get_printer_maintenance_info_service(impressora_id, session, limit)
