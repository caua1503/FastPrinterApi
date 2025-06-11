from pydantic import BaseModel

class StatusSchema(BaseModel):
    status: str
    descricao: str

class StatusSchemaDB(StatusSchema):
    id: int