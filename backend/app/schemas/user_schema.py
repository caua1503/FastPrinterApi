from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UsersRoleSchema(Enum):
    admin = "admin"
    member = "member"
    guest = "guest"


class UserNewPasswordSchema(BaseModel):
    current_password: str
    new_password: str


class UserNewPasswordAdminSchema(BaseModel):
    new_password: str


class UserApiKeySchema(BaseModel):
    api_key: str


class UserCreateSchema(BaseModel):
    login: str
    password: str
    name: str


class UserCreateAdminSchema(UserCreateSchema):
    role: UsersRoleSchema = UsersRoleSchema.member


class UserUpdateSchema(BaseModel):
    login: Optional[str] = None
    name: Optional[str] = None


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    name: str


class UserSchema(UserCreateSchema):
    role: UsersRoleSchema = UsersRoleSchema.member


class UserSchemaDB(UserSchema):
    id: int


class UserConfigurationSchema(BaseModel):
    user_id: int
    username: str
    webhook_enabled: bool = False
    webhook_url: Optional[str] = None
    first_access: bool = True
