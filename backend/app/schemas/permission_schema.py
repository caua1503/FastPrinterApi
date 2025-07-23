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


class UserRoleCatalog:
    admin = PermissionBaseSchema(name="admin", code="admin", description="Full administrative permissions.")
    member = PermissionBaseSchema(name="member", code="member", description="Basic user permissions.")


class UserPermissionCatalog:
    user_create = PermissionBaseSchema(name="user.create", code="user.create", description="Allows creating new users.")
    user_update = PermissionBaseSchema(
        name="user.update", code="user.update", description="Allows updating user information."
    )
    user_delete = PermissionBaseSchema(name="user.delete", code="user.delete", description="Allows deleting users.")
    user_read = PermissionBaseSchema(name="user.read", code="user.read", description="Allows viewing user information.")


class PrinterPermissionCatalog:
    printer_create = PermissionBaseSchema(
        name="printer.create", code="printer.create", description="Allows adding new printers."
    )
    printer_update = PermissionBaseSchema(
        name="printer.update", code="printer.update", description="Allows updating printer information."
    )
    printer_delete = PermissionBaseSchema(
        name="printer.delete", code="printer.delete", description="Allows deleting printers."
    )
    printer_read = PermissionBaseSchema(
        name="printer.read", code="printer.read", description="Allows viewing printer information."
    )


class SupplyPermissionCatalog:
    supply_create = PermissionBaseSchema(
        name="supply.create", code="supply.create", description="Allows adding new supplies."
    )
    supply_delete = PermissionBaseSchema(
        name="supply.delete", code="supply.delete", description="Allows deleting supplies."
    )
    supply_update = PermissionBaseSchema(
        name="supply.update", code="supply.update", description="Allows updating supply information."
    )
    supply_read = PermissionBaseSchema(
        name="supply.read", code="supply.read", description="Allows viewing supply information."
    )


class DepartmentPermissionCatalog:
    department_create = PermissionBaseSchema(
        name="department.create", code="department.create", description="Allows creating new departments."
    )
    department_delete = PermissionBaseSchema(
        name="department.delete", code="department.delete", description="Allows deleting departments."
    )
    department_update = PermissionBaseSchema(
        name="department.update", code="department.update", description="Allows updating department information."
    )
    department_read = PermissionBaseSchema(
        name="department.read", code="department.read", description="Allows viewing department information."
    )


class MaintenancePermissionCatalog:
    maintenance_create = PermissionBaseSchema(
        name="maintenance.create", code="maintenance.create", description="Allows creating new maintenance."
    )
    maintenance_delete = PermissionBaseSchema(
        name="maintenance.delete", code="maintenance.delete", description="Allows deleting maintenance."
    )
    maintenance_update = PermissionBaseSchema(
        name="maintenance.update", code="maintenance.update", description="Allows updating maintenance information."
    )
    maintenance_read = PermissionBaseSchema(
        name="maintenance.read", code="maintenance.read", description="Allows viewing maintenance information."
    )


class HistoryPermissionCatalog:
    history_create = PermissionBaseSchema(
        name="history.create", code="history.create", description="Allows creating new history."
    )
    history_delete = PermissionBaseSchema(
        name="history.delete", code="history.delete", description="Allows deleting history."
    )
    history_update = PermissionBaseSchema(
        name="history.update", code="history.update", description="Allows updating history information."
    )
    history_read = PermissionBaseSchema(
        name="history.read", code="history.read", description="Allows viewing history information."
    )


class LogPermissionCatalog:
    log_delete = PermissionBaseSchema(name="log.delete", code="log.delete", description="Allows deleting logs.")
    log_update = PermissionBaseSchema(
        name="log.update", code="log.update", description="Allows updating log information."
    )
    log_read = PermissionBaseSchema(name="log.read", code="log.read", description="Allows viewing log information.")
