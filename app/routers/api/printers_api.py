from http import HTTPStatus

from fastapi import APIRouter, Depends
from helpers.db_helper import get_session
from models.printer_model import FullPrinterSchema, PrinterSchemaDB
from services.printer_service import create_printer, delete_printer, get_printer, get_printers, update_printer
from sqlalchemy.orm import Session

printer_router = APIRouter(prefix="/printers", tags=["printers"])


@printer_router.get("/", description="Get all printers")
async def api_get_printers(session: Session = Depends(get_session), limit: int = 10, offset: int = 0):
    printers = await get_printers(session, limit, offset)
    return {"printers": printers}


@printer_router.post(
    "/", response_model=PrinterSchemaDB, status_code=HTTPStatus.CREATED, description="Create a printer"
)
async def api_create_printer(printer: FullPrinterSchema, session: Session = Depends(get_session)):
    printer_db = await create_printer(printer, session)
    return printer_db


@printer_router.get("/{id}", description="Get a printer by id")
async def api_get_printer(id: int, session: Session = Depends(get_session)):
    printer = await get_printer(id, session)
    return printer


@printer_router.put("/{id}", description="Update a printer by id")
async def api_update_printer(id: int, printer: FullPrinterSchema, session: Session = Depends(get_session)):
    printer_db = await update_printer(id, printer, session)
    return printer_db


@printer_router.delete("/{id}", description="Delete a printer by id")
async def api_delete_printer(id: int, session: Session = Depends(get_session)):
    await delete_printer(id, session)
    return {"message": f"id deleted: {id}"}
