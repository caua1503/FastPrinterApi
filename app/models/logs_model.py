from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.logs_schema import LogLevel
from app.models.base_model import table_registry_logs


@table_registry_logs.mapped_as_dataclass
class SystemLog:
    __tablename__ = "system_log"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    message: Mapped[str]
    level: Mapped[LogLevel]
    service: Mapped[str]
    timestamp: Mapped[date]
    description: Mapped[Optional[str]]


@table_registry_logs.mapped_as_dataclass
class UserLog:
    __tablename__ = "user_log"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    message: Mapped[str]
    level: Mapped[LogLevel]
    service: Mapped[str]
    timestamp: Mapped[date]
    description: Mapped[Optional[str]]

