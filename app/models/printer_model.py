from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import table_registry


@table_registry.mapped_as_dataclass
class Status:
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    status: Mapped[str]
    description: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class Printer:
    __tablename__ = "printer"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    supply_id: Mapped[int] = mapped_column(ForeignKey("supply.id"))
    name: Mapped[str]
    brand: Mapped[str]
    model: Mapped[str]
    ip: Mapped[str] = mapped_column(unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    description: Mapped[Optional[str]]
    forecast: Mapped[Optional[date]]
    last_refill: Mapped[Optional[date]]
    last_maintenance: Mapped[Optional[date]]
    last_check: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
