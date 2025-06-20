from pydantic import BaseModel, Field


class FilterBase(BaseModel):
    limit: int | None = Field(default=10, ge=1, le=100)
    offset: int | None = Field(default=0, ge=0)




