from pydantic import BaseModel, ConfigDict


class StatusSchema(BaseModel):
    status: str
    description: str


class StatusSchemaDB(StatusSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StatusListResponse(BaseModel):
    status: list[StatusSchemaDB]
