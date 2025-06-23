from pydantic import BaseModel


class TokenSchemma(BaseModel):
    acess_token: str
    token_type: str
