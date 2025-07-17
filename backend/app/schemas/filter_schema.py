from datetime import date, timedelta
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.logs_schema import ApiKeyActionSchema, LogLevelSchema, ServiceSchema


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class OrderByField(str, Enum):
    date = "date"


class OrderByFieldPrinter(str, Enum):
    created_at = "created_at"
    forecast = "forecast"
    last_refill = "last_refill"
    last_maintenance = "last_maintenance"
    last_check = "last_check"


class OrderByFieldLog(str, Enum):
    timestamp = "timestamp"
    created_at = "created_at"


class FilterBase(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class FilterBase2(FilterBase):
    time_start: Optional[date] = Field(default=date.today() - timedelta(days=7))
    time_end: Optional[date] = Field(default=date.today())


class FilterPrinterDefault(FilterBase):
    status_id: Optional[int] = Field(default=None)
    supply_id: Optional[int] = Field(default=None)
    department_id: Optional[int] = Field(default=None)
    order_by: Optional[OrderBy] = Field(default=OrderBy.desc)
    order_by_field: Optional[OrderByFieldPrinter] = Field(default=OrderByFieldPrinter.created_at)


class FilterPrinter(FilterPrinterDefault):
    printer_id: Optional[int] = Field(default=None)


class FilterPrinterHistory(FilterBase2):
    printer_id: Optional[int] = Field(default=None)
    order_by: Optional[OrderBy] = Field(default=OrderBy.desc)


class FilterLog(FilterBase2):
    service: Optional[ServiceSchema] = Field(default=None)
    level: Optional[LogLevelSchema] = Field(default=None)
    order_by: Optional[OrderBy] = Field(default=OrderBy.desc)
    order_by_field: Optional[OrderByFieldLog] = Field(default=OrderByFieldLog.timestamp)


class FilterLogUser(FilterLog):
    user_id: Optional[int] = Field(default=None)


class FilterLogSystem(FilterLog):
    pass


class FilterLogApiKey(FilterBase2):
    api_key_id: Optional[int] = Field(default=None)
    action: Optional[ApiKeyActionSchema] = Field(default=None)
    order_by: Optional[OrderBy] = Field(default=OrderBy.desc)
    order_by_field: Optional[OrderByFieldLog] = Field(default=OrderByFieldLog.timestamp)


class FilterLogApiKeyAdmin(FilterLogApiKey):
    user_ids: Optional[List[int]] = Field(default=None)
