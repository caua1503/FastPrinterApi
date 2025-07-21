from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import table_registry

if TYPE_CHECKING:
    from app.models.user_model import User


@table_registry.mapped_as_dataclass
class RefreshToken:
    __tablename__ = "refresh_token"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int]
    expires_at: Mapped[datetime]
    is_revoked: Mapped[bool] = mapped_column(default=False)
    ip_address: Mapped[str] = mapped_column(default="")
    user_agent: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="refresh_token", init=False)
