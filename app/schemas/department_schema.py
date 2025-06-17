from pydantic import BaseModel

class DepartmentSchema(BaseModel):
    name: str
    description: str

class DepartmentSchemaDB(DepartmentSchema):
    id: int