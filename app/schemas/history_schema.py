from datetime import date
from typing import Optional

from pydantic import BaseModel


class RefillHistorySchema(BaseModel):
    printer_id: int
    date: date
    event_type: str
    supply_id: int
    description: Optional[str]


class MaintenanceHistorySchema(BaseModel):
    printer_id: int
    date: date
    event_type: str
    description: Optional[str]


class PrinterTrashHistorySchema(BaseModel):
    printer_id: int
    date: date
    description: Optional[str]


class AlertHistorySchema(BaseModel):
    printer_id: int
    date: date
    alert_type: str
    description: Optional[str]


class StatusHistorySchema(BaseModel):
    printer_id: int
    status_id: int
    date: date
    description: Optional[str] = None


class RefillHistorySchemaDB(RefillHistorySchema):
    id: int


class MaintenanceHistorySchemaDB(MaintenanceHistorySchema):
    id: int


class PrinterTrashHistorySchemaDB(PrinterTrashHistorySchema):
    id: int


class AlertHistorySchemaDB(AlertHistorySchema):
    id: int


class StatusHistorySchemaDB(StatusHistorySchema):
    id: int
