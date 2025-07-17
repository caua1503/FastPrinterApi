from datetime import date
from typing import Optional

from pydantic import BaseModel


class PrinterMaintenanceInfoSchema(BaseModel):
    printer_id: int
    last_update: date
    next_refill: Optional[date] = None
    next_cleaning: Optional[date] = None
    refill_percentage: float
    cleaning_percentage: float


class PrinterMaintenanceInfoSchemaDB(PrinterMaintenanceInfoSchema):
    id: int


class ListPrinterMaintenanceInfoSchema(BaseModel):
    total: int
    count: int
    list: list[PrinterMaintenanceInfoSchemaDB]
