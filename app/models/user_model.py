from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    code_hash: Mapped[str]
    api_key: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Permission:
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]
    permissions: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class UserConfiguration:
    __tablename__ = "user_configuration"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username: Mapped[str]
    webhook_enabled: Mapped[bool] = mapped_column(default=False)
    webhook_url: Mapped[Optional[str]] = mapped_column(default=None)
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
