from typing import Optional

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentSchemaDB(DepartmentSchema):
    id: int
