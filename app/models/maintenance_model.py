from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import table_registry


@table_registry.mapped_as_dataclass
class PrinterMaintenanceInfo:
    __tablename__ = "printer_maintenance_info"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    printer_id: Mapped[int]
    last_update: Mapped[date]
    next_refill: Mapped[Optional[date]]
    next_cleaning: Mapped[Optional[date]]
    refill_percentage: Mapped[float]
    cleaning_percentage: Mapped[float]
