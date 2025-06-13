from pydantic import BaseModel
from typing import Optional

class InputSchema(BaseModel):
    nome: str
    tipo_insumo: int
    marca: str
    descricao: Optional[str]

class InputSchemaDB(InputSchema):
    id: int

class TipoInsumoSchema(BaseModel):
    nome: str

class TipoInsumoSchemaDB(TipoInsumoSchema):
    id: int