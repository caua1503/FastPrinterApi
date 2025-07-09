from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SupplyIdSchema(BaseModel):
    id: int = 1
    name: str


class StatusIdSchema(BaseModel):
    id: int = 1
    name: str


class DepartmentIdSchema(BaseModel):
    id: int = 1
    name: str


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
    department_id: int = 1
    name: str
    brand: str
    model: str
    ip: str
    description: Optional[str] = None
    forecast: Optional[date] = None
    last_refill: Optional[date] = None
    last_maintenance: Optional[date] = None
    last_check: Optional[date] = None


class FullPrinterSchemaDB(BaseModel):
    # FullPrintSchemaDB was previously an extension of FullPrintSchema,
    # like this: (FullPrinterSchemaDB(FullPrinterSchema)), but for json aesthetics it was duplicated
    model_config = ConfigDict(from_attributes=True)
    id: int
    supply_id: int = 1
    status_id: int = 1
    department_id: int = 1
    name: str
    brand: str
    model: str
    ip: str
    description: Optional[str] = None
    forecast: Optional[date] = None
    last_refill: Optional[date] = None
    last_maintenance: Optional[date] = None
    last_check: Optional[date] = None


class FullPrinterPublicSchema(FullPrinterSchemaDB):
    supply_id: SupplyIdSchema  # type: ignore
    status_id: StatusIdSchema  # type: ignore
    department_id: DepartmentIdSchema  # type: ignore


class ListFullPrinterPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    printers: List[FullPrinterPublicSchema]


class FullPrinterUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supply_id: Optional[int] = None
    status_id: Optional[int] = None
    department_id: Optional[int] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    ip: Optional[str] = None
    description: Optional[str] = None
    forecast: Optional[date] = None
    last_refill: Optional[date] = None
    last_maintenance: Optional[date] = None
    last_check: Optional[date] = None
