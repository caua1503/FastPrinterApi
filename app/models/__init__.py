# Import all models to make them available when importing from models package
from .base_model import table_registry
from .department_model import Department
from .history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
    StatusHistory,
)
from .maintenance_model import PrinterMaintenanceInfo
from .printer_model import Printer, Status
from .supply_model import Supply, SupplyType
from .user_model import Permission, User, UserConfiguration

# Make all models available at package level
__all__ = [
    # Base
    "table_registry",
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
    "Permission",
    "UserConfiguration",
    # Maintenance models
    "PrinterMaintenanceInfo",
]
