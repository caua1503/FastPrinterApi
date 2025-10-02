from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import table_registry

if TYPE_CHECKING:
    from app.models.printer_model import Printer


@table_registry.mapped_as_dataclass
class Department:
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), onupdate=func.now())
    printers: Mapped[List["Printer"]] = relationship(back_populates="department", init=False)
