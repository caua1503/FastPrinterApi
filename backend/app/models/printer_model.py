from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import table_registry

if TYPE_CHECKING:
    from app.models.department_model import Department
    from app.models.supply_model import Supply


@table_registry.mapped_as_dataclass
class Status:
    __tablename__ = "status"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    status: Mapped[str]
    description: Mapped[Optional[str]]
    printers: Mapped[List["Printer"]] = relationship(back_populates="status", init=False)


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

    department: Mapped["Department"] = relationship(back_populates="printers", init=False)
    supply: Mapped["Supply"] = relationship(back_populates="printers", init=False)
    status: Mapped["Status"] = relationship(back_populates="printers", init=False)
