from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import table_registry


@table_registry.mapped_as_dataclass
class SupplyType:
    __tablename__ = "supply_type"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]


@table_registry.mapped_as_dataclass
class Supply:
    __tablename__ = "supply"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]
    supply_type_id: Mapped[int] = mapped_column(ForeignKey("supply_type.id"))
    brand: Mapped[str]
    description: Mapped[Optional[str]]
