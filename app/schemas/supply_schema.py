from typing import Optional

from pydantic import BaseModel


class SupplySchema(BaseModel):
    name: str
    supply_type_id: int
    brand: str
    description: Optional[str] = None


class SupplySchemaDB(SupplySchema):
    id: int


class SupplyTypeSchema(BaseModel):
    name: str


class SupplyTypeSchemaDB(SupplyTypeSchema):
    id: int
