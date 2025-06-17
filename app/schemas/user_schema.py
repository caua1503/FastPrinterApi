from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    senha_hash: str
    codigo_hash: str
    api_key: str


class UserSchemaDB(UserSchema):
    id: int


class UserConfigSchema(BaseModel):
    nome_usuario: str
    webhook_enable: bool
    webhook_url: Optional[str]
