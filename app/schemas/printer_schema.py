from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PrinterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    model: str
    ip: str
    brand: str


class PrinterSchemaDB(PrinterSchema):
    id: int


class FullPrinterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    supply_id: int = 1
    status_id: int = 1
    name: str
    brand: str
    model: str
    ip: str
    department_id: int = 1
    description: Optional[str] = None
    forecast: Optional[date] = None
    last_refill: Optional[date] = None
    last_maintenance: Optional[date] = None
    last_check: Optional[date] = None


class FullPrinterSchemaDB(FullPrinterSchema):
    id: int


class ListFullPrinterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    printers: List[FullPrinterSchemaDB]
