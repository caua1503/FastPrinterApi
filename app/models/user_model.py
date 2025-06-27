from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import table_registry
from app.schemas.user_schema import UsersRoleSchema


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    name: Mapped[str]
    role: Mapped[UsersRoleSchema] = mapped_column(default=UsersRoleSchema.member)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    # Relationships
    api_keys: Mapped[List["UserApiKey"]] = relationship(back_populates="user", cascade="all, delete-orphan", init=False)
    configuration: Mapped["UserConfiguration"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False, init=False
    )
    permission_of_user: Mapped[List["UserPermission"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )


@table_registry.mapped_as_dataclass
class UserApiKey:
    __tablename__ = "user_api_key"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    api_key: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="api_keys", init=False)
    permissions: Mapped[List["ApiKeyPermission"]] = relationship(
        back_populates="api_key", cascade="all, delete-orphan", init=False
    )


@table_registry.mapped_as_dataclass
class PermissionApiKey:
    """
    all api functions, sunch as: update user, update printer, read all printers e etc
    """

    __tablename__ = "permission_of_api_key"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)  # read.all_printers_info, read.printers_info, read.supply
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class PermissionUser:
    """
    all permissions of users sunch as acess to screen of system, system fuunctions e etc
    """

    __tablename__ = "permission_of_user"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)  # read.user, update.printer, read.supply
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class UserPermission:
    """
    Conecta os usuarios (user_api_key.id) as tabelas permission_of_user
    """

    __tablename__ = "user_permission"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission_of_user.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="permission_of_user", init=False)
    permission: Mapped["PermissionUser"] = relationship(init=False)


@table_registry.mapped_as_dataclass
class ApiKeyPermission:
    """
    Connect all apis keys (user_api_key.id) for tables in permission_of_api_key
    each user can have more than one api key with different permissions levels
    """

    __tablename__ = "api_key_permission"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permission_of_api_key.id"))
    api_key_id: Mapped[int] = mapped_column(ForeignKey("user_api_key.id"))
    api_key: Mapped["UserApiKey"] = relationship(back_populates="permissions", init=False)
    permission: Mapped["PermissionApiKey"] = relationship(init=False)


@table_registry.mapped_as_dataclass
class UserConfiguration:
    __tablename__ = "user_configuration"
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username: Mapped[str]
    webhook_enabled: Mapped[bool] = mapped_column(default=False)
    webhook_url: Mapped[Optional[str]] = mapped_column(default=None)
    primeiro_acesso: Mapped[bool] = mapped_column(default=True)  # logica para o usuario trocar a senha assim que entrar
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="configuration", init=False)
