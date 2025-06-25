from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LogLevelSchema(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogDescriptionSchema(str, Enum):
    DEBUG = "Details for development and debugging"
    INFO = "Normal application events"
    WARNING = "Something unexpected, but that did not prevent the application from continuing"
    ERROR = "Faults that require attention but do not crash the application"
    CRITICAL = "Serious failures (no Database, no Redis, etc)"


class LogSchema(BaseModel):
    message: str
    description: Optional[str] = None
    level: LogLevelSchema
    service: str
    timestamp: date


class UserLogSchema(LogSchema):
    user_id: int


class SystemLogSchema(LogSchema):
    service: str
