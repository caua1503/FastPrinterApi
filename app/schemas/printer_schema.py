from datetime import date
from typing import Optional

from pydantic import BaseModel


class PrinterSchema(BaseModel):
    name: str
    model: str
    ip: str
    brand: str


class PrinterSchemaDB(PrinterSchema):
    id: int


class FullPrinterSchema(BaseModel):
    supply_id: int
    status_id: int
    name: str
    brand: str
    model: str
    ip: str
    department_id: int
    description: Optional[str] = None
    forecast: Optional[date] = None
    last_refill: Optional[date] = None
    last_maintenance: Optional[date] = None
    last_check: Optional[date] = None


class FullPrinterSchemaDB(FullPrinterSchema):
    id: int
