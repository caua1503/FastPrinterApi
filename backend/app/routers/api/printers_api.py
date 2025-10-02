from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import has_access
from app.helpers.database_helper import get_session
from app.schemas.filter_schema import FilterPrinterDefault
from app.schemas.printer_schema import FullPrinterSchema, FullPrinterUpdateSchema, ListFullPrinterPublicSchema
from app.services.printer_service import (
    create_printer,
    delete_printer,
    get_printer_id,
    get_printers,
    update_printer,
)

printer_router = APIRouter()


@printer_router.get(
    "/", summary="Get all printers", status_code=HTTPStatus.OK, response_model=ListFullPrinterPublicSchema
)
async def api_get_printers(
    session: Annotated[AsyncSession, Depends(get_session)],
    filters: Annotated[FilterPrinterDefault, Query()],
    current_user=has_access(),
):
    printers = await get_printers(session, filters)
    return printers


@printer_router.post("/", summary="Create a printer", status_code=HTTPStatus.CREATED, response_model=FullPrinterSchema)
async def api_create_printer(
    printer: FullPrinterSchema, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    printer_db = await create_printer(session, printer)
    return printer_db


@printer_router.get("/{id}", summary="Get a printer by id", status_code=HTTPStatus.OK)
async def api_get_printer(id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()):
    printer = await get_printer_id(session, id)
    return printer


@printer_router.put("/{id}", summary="Update a printer by id", status_code=HTTPStatus.OK)
async def api_update_printer(
    id: int,
    printer: FullPrinterUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user=has_access(),
):
    printer_db = await update_printer(session, id, printer)
    return printer_db


@printer_router.delete("/{id}", summary="Delete a printer by id", status_code=HTTPStatus.NO_CONTENT)
async def api_delete_printer(
    id: int, session: Annotated[AsyncSession, Depends(get_session)], current_user=has_access()
):
    await delete_printer(session, id)
