# Import all models to make them available when importing from models package
from app.models.base_model import table_registry
from app.models.department_model import Department
from app.models.history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
    StatusHistory,
)
from app.models.maintenance_model import PrinterMaintenanceInfo
from app.models.printer_model import Printer, Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import Permission, User, UserConfiguration

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
