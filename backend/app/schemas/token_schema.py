from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


class RefreshTokenSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class OAuth2PasswordAndRefreshRequestForm(OAuth2PasswordRequestForm):
    refresh: bool = False
