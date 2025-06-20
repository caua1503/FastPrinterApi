from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    password_hash: str
    code_hash: str
    api_key: str


class UserSchemaDB(UserSchema):
    id: int


class UserConfigurationSchema(BaseModel):
    username: str
    webhook_enabled: bool
    webhook_url: Optional[str]
