from pydantic import BaseModel

class InputSchema(BaseModel):
    tipo_insumo: str
    marca: str
    descricao: str

class InputSchemaDB(InputSchema):
    id: int
