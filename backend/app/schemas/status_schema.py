from pydantic import BaseModel


class StatusSchema(BaseModel):
    status: str
    description: str


class StatusSchemaDB(StatusSchema):
    id: int
