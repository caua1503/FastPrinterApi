from datetime import date, datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import table_registry_logs
from app.schemas.logs_schema import ApiKeyActionSchema, LogLevelSchema, ServiceSchema


@table_registry_logs.mapped_as_dataclass
class SystemLog:
    __tablename__ = "system_log"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    message: Mapped[str]
    level: Mapped[LogLevelSchema]
    service: Mapped[ServiceSchema]
    timestamp: Mapped[date]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=func.now())


@table_registry_logs.mapped_as_dataclass
class UserLog:
    __tablename__ = "user_log"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    message: Mapped[str]
    level: Mapped[LogLevelSchema]
    service: Mapped[ServiceSchema]
    timestamp: Mapped[date]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=func.now())


@table_registry_logs.mapped_as_dataclass
class ApiKeyLog:
    __tablename__ = "api_key_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    api_key_id: Mapped[int]
    user_id: Mapped[int]
    action: Mapped[ApiKeyActionSchema]
    route: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
