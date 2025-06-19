from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import table_registry


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
    supply_type_id: Mapped[int]
    brand: Mapped[str]
    description: Mapped[Optional[str]]
