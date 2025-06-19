from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.database_helper import get_session
from app.schemas.printer_schema import FullPrinterSchema
from app.services.printer_service import (
    create_printer,
    delete_printer,
    get_printer_department_id,
    get_printer_id,
    get_printer_status_id,
    get_printer_supply_id,
    get_printers,
    update_printer,
)

printer_router = APIRouter()


@printer_router.get("/", status_code=HTTPStatus.OK, description="Get all printers")
async def api_get_printers(session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0):
    printers = await get_printers(session, limit, offset)
    return {"printers": printers}


@printer_router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=FullPrinterSchema, description="Create a printer"
)
async def api_create_printer(printer: FullPrinterSchema, session: Annotated[AsyncSession, Depends(get_session)]):
    printer_db = await create_printer(session, printer)
    return printer_db


@printer_router.get("/{id}", status_code=HTTPStatus.OK, description="Get a printer by id")
async def api_get_printer(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    printer = await get_printer_id(session, id)
    return printer


@printer_router.put("/{id}", status_code=HTTPStatus.OK, description="Update a printer by id")
async def api_update_printer(
    id: int, printer: FullPrinterSchema, session: Annotated[AsyncSession, Depends(get_session)]
):
    printer_db = await update_printer(session, id, printer)
    return printer_db


@printer_router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT, description="Delete a printer by id")
async def api_delete_printer(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    await delete_printer(session, id)


@printer_router.get(
    "/department/{department_id}", status_code=HTTPStatus.OK, description="Get printers by department id"
)
async def api_get_printer_department_id(
    department_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
):
    printers = await get_printer_department_id(session, department_id, limit, offset)
    return {"printers": printers}


@printer_router.get("/supply/{supply_id}", status_code=HTTPStatus.OK, description="Get printers by supply id")
async def api_get_printer_supply_id(
    supply_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
):
    printers = await get_printer_supply_id(session, supply_id, limit, offset)
    return {"printers": printers}


@printer_router.get("/status/{status_id}", status_code=HTTPStatus.OK, description="Get printers by status id")
async def api_get_printer_status_id(
    status_id: int, session: Annotated[AsyncSession, Depends(get_session)], limit: int = 10, offset: int = 0
):
    printers = await get_printer_status_id(session, status_id, limit, offset)
    return {"printers": printers}
