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


class PrinterRefSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


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


class RefillHistoryListItemSchema(RefillHistorySchemaDB):
    printer: PrinterRefSchema


class MaintenanceHistoryListItemSchema(MaintenanceHistorySchemaDB):
    printer: PrinterRefSchema


class AlertHistoryListItemSchema(AlertHistorySchemaDB):
    printer: PrinterRefSchema


class ListRefillHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[RefillHistoryListItemSchema]


class ListMaintenanceHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[MaintenanceHistoryListItemSchema]


class ListStatusHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[StatusHistorySchemaDB]


class ListAlertHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[AlertHistoryListItemSchema]


class ListPrinterTrashHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    historys: List[PrinterTrashHistorySchemaDB]
