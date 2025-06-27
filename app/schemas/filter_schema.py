from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field
from app.schemas.logs_schema import LogLevelSchema, ServiceSchema


class FilterBase(BaseModel):
    limit: int = Field(default=10, ge=1)
    offset: int = Field(default=0, ge=0)


class FilterPrinter(FilterBase):
    printer_id: Optional[int] = Field(default=None)
    status_id: Optional[int] = Field(default=None)
    supply_id: Optional[int] = Field(default=None)
    department_id: Optional[int] = Field(default=None)

class FilterLog(FilterBase):
    service: Optional[ServiceSchema] = Field(default=None)
    level: Optional[LogLevelSchema] = Field(default=None)
    time_start: Optional[datetime] = Field(default=datetime.now() - timedelta(days=30))
    time_end: Optional[datetime] = Field(default=datetime.now())

class FilterLogUser(FilterLog):
    user_id: Optional[int] = Field(default=None)

class FilterLogSystem(FilterLog):
    pass