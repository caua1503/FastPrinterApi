from http import HTTPStatus
from fastapi import APIRouter
from typing import List, Dict, Any
from models import PrinterSchema, FullPrinterSchema, PrinterSchemaDB
from services import get_printers, create_printer

printer_router = APIRouter(prefix="/printers", tags=["printers"])

@printer_router.get("/", description="Get all printers")
async def api_get_printers():
    printers = await get_printers()
    return {"printers": printers}

@printer_router.get("/{id}", description="Get a printer by id")
async def api_get_printer(id: int):
    return {"message": f"id: {id}"}

@printer_router.post("/", response_model=PrinterSchemaDB, status_code=HTTPStatus.CREATED, description="Create a printer")
async def api_create_printer(printer: FullPrinterSchema):
    printer_db = await create_printer(printer)
    return printer_db

@printer_router.put("/{id}", description="Update a printer by id")
async def api_update_printer(id: int):
    data = None
    return {"message": f"id: {id}, data: {data}"}

@printer_router.delete("/{id}", description="Delete a printer by id")
async def api_delete_printer(id: int):
    return {"message": f"id deleted: {id}"}