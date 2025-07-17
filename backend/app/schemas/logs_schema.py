from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class LogLevelSchema(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ServiceSchema(str, Enum):
    REDIS = "REDIS"
    POSTGRES = "POSTGRES"
    OTHER = "OTHER"


class ApiKeyActionSchema(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    CONNECT = "CONNECT"
    ANY = "ANY"


class LogDescriptionSchema(str, Enum):
    DEBUG = "Details for development and debugging"
    INFO = "Normal application events"
    WARNING = "Something unexpected, but that did not prevent the application from continuing"
    ERROR = "Faults that require attention but do not crash the application"
    CRITICAL = "Serious failures (no Database, no Redis, etc)"


class LogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    description: Optional[str] = None
    level: LogLevelSchema
    service: ServiceSchema
    timestamp: datetime


class UserLogSchema(LogSchema):
    model_config = ConfigDict(from_attributes=True)
    user_id: int


class SystemLogSchema(LogSchema):
    pass


class ApiKeyLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key_id: int
    user_id: int
    action: ApiKeyActionSchema
    timestamp: datetime
    route: Optional[str] = None
    description: Optional[str] = None


class ListUserLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    logs: List[UserLogSchema]


class ListSystemLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    logs: List[SystemLogSchema]


class ListApiKeyLogSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total: int
    count: int
    logs: List[ApiKeyLogSchema]
