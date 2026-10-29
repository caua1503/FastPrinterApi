from typing import Optional

from pydantic import BaseModel, ConfigDict


class DepartmentSchema(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentSchemaDB(DepartmentSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DepartmentListResponse(BaseModel):
    departments: list[DepartmentSchemaDB]
