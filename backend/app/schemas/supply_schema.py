from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplySchema(BaseModel):
    name: str
    supply_type_id: int
    brand: str
    description: Optional[str] = None


class SupplySchemaDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    supply_type_id: int
    name: str
    brand: str
    description: Optional[str] = None


class SupplyTypeSchema(BaseModel):
    name: str


class SupplyTypeSchemaDB(SupplyTypeSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SupplyListResponse(BaseModel):
    supplys: list[SupplySchemaDB]


class SupplyTypeListResponse(BaseModel):
    supply_types: list[SupplyTypeSchemaDB]
