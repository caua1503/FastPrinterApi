from pydantic import BaseModel, Field
from typing import Optional

class FilterBase(BaseModel):
    limit: Optional[int] = Field(default=10, ge=1)
    offset: Optional[int] = Field(default=0, ge=0)

class FilterPrinter(FilterBase):
    printer_id: Optional[int] = Field(default=None)
    status_id: Optional[int] = Field(default=None)
    supply_id: Optional[int] = Field(default=None)
    department_id: Optional[int] = Field(default=None)

