# Import all models to make them available when importing from models package
from app.models.base_model import table_registry, table_registry_logs
from app.models.department_model import Department
from app.models.history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
    StatusHistory,
)
from app.models.logs_model import SystemLog, UserLog
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer, Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import (
    ApiKeyPermission,
    PermissionApiKey,
    PermissionUser,
    User,
    UserApiKey,
    UserConfiguration,
    UserPermission,
    UsersRoleSchema,
)

# Make all models available at package level
__all__ = [
    # Base
    "table_registry",
    "table_registry_logs",
    # Department models
    "Department",
    # Printer models
    "Status",
    "Printer",
    # Supply models
    "SupplyType",
    "Supply",
    # History models
    "PrinterTrashHistory",
    "StatusHistory",
    "MaintenanceHistory",
    "RefillHistory",
    "AlertHistory",
    # User models
    "User",
    "PermissionUser",
    "UserConfiguration",
    "UserApiKey",
    "UserPermission",
    "UsersRoleSchema",
    "PermissionApiKey",
    "ApiKeyPermission",
    # Maintenance models
    "PrinterMaintenanceInfo",
    # Logs models
    "SystemLog",
    "UserLog",
]
