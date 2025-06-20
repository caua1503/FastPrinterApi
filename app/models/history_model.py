from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import table_registry


@table_registry.mapped_as_dataclass
class PrinterTrashHistory:
    __tablename__ = "printer_trash_history"  # history of printer trash cleaning
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int] = mapped_column(ForeignKey("printer.id"))
    date: Mapped[date]
    description: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class StatusHistory:  # history of printer status, in maintenance, refills, when it reached critical etc
    __tablename__ = "status_history"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int] = mapped_column(ForeignKey("printer.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    date: Mapped[date]
    description: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class MaintenanceHistory:
    __tablename__ = "maintenance_history"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int] = mapped_column(ForeignKey("printer.id"))
    date: Mapped[date]
    event_type: Mapped[str]  # preventive, cleaning, part replacement, repair, supply change
    description: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class RefillHistory:
    __tablename__ = "refill_history"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int] = mapped_column(ForeignKey("printer.id"))
    date: Mapped[date]
    event_type: Mapped[str]  # Refill, Supply Change
    supply_id: Mapped[int]
    description: Mapped[Optional[str]]


@table_registry.mapped_as_dataclass
class AlertHistory:
    __tablename__ = "alert_history"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int] = mapped_column(ForeignKey("printer.id"))
    date: Mapped[date]
    alert_type: Mapped[str]
    description: Mapped[Optional[str]]
