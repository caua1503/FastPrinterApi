from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RefillHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    printer_id: int
    date: date
    event_type: str
    supply_id: int
    description: Optional[str]


class MaintenanceHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    printer_id: int
    date: date
    event_type: str
    description: Optional[str]


class PrinterTrashHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    printer_id: int
    date: date
    description: Optional[str]


class AlertHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    printer_id: int
    date: date
    alert_type: str
    description: Optional[str]


class StatusHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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

class ListRefillHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[RefillHistorySchemaDB]


class ListMaintenanceHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[MaintenanceHistorySchemaDB]


class ListStatusHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[StatusHistorySchemaDB]


class ListAlertHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[AlertHistorySchemaDB]


class ListPrinterTrashHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[PrinterTrashHistorySchemaDB]