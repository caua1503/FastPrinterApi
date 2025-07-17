from typing import List, Optional

from pydantic import BaseModel


class PermissionBaseSchema(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class PermissionBaseUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionUserUpdateSchema(PermissionBaseUpdateSchema):
    pass


class PermissionApiKeyUpdateSchema(PermissionBaseUpdateSchema):
    pass


class PermissionUserSchema(PermissionBaseSchema):
    pass


class PermissionApiKeySchema(PermissionBaseSchema):
    pass


class PermissionUserSchemaDB(PermissionUserSchema):
    id: int


class PermissionApiKeySchemaDB(PermissionApiKeySchema):
    id: int


class ListPermissionUserSchema(BaseModel):
    total: int
    permissions: List[PermissionUserSchemaDB]


class ListPermissionApiKeySchema(BaseModel):
    total: int
    permissions: List[PermissionApiKeySchemaDB]
