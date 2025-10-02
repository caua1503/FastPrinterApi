import asyncio
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.config import Config
from app.core.security import get_password_hash
from app.models import table_registry
from app.models.department_model import Department
from app.models.printer_model import Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import PermissionApiKey, PermissionUser, User, UserConfiguration
from app.schemas.permission_schema import (
    DepartmentPermissionCatalog,
    HistoryPermissionCatalog,
    LogPermissionCatalog,
    MaintenancePermissionCatalog,
    PrinterPermissionCatalog,
    SupplyPermissionCatalog,
    UserPermissionCatalog,
    UserRoleCatalog,
)
from app.schemas.user_schema import UsersRoleSchema

engine = create_async_engine(Config().DATABASE_URL, echo=True)  # type: ignore


def get_all_permissions(catalog_classes):
    """
    Extracts all permissions defined in catalog classes and returns a list of PermissionUsers.

    Each catalog class groups together system-related packages
    (e.g., UserPermissionCatalog, PrinterPermissionCatalog).

    The function examines all attributes of these classes, verifies that the tasks are valid
    (have 'name' and 'code' fields),

    and creates a PermissionUser object for each.

    Arguments:
    catalog_classes(list): List of permission catalog classes.

    Returns:
    list: List of PermissionUsers, ready to be inserted into the database.

    Example of use:
        initial_permissions = get_all_permissions([
            UserRoleCatalog,
            UserPermissionCatalog,
            PrinterPermissionCatalog,
            ...
        ])
    """
    permissions = []
    for catalog in catalog_classes:
        for attr in dir(catalog):
            if not attr.startswith("__"):
                perm = getattr(catalog, attr)
                if hasattr(perm, "name") and hasattr(perm, "code"):
                    permissions.append(
                        PermissionUser(
                            name=perm.name,
                            code=perm.code,
                            description=perm.description,
                        )
                    )
    return permissions


def get_all_api_permissions(catalog_classes):
    """
    Extracts all permissions defined in catalog classes and returns a list of PermissionApiKey.

    Each catalog class groups together system-related packages
    (e.g., UserPermissionCatalog, PrinterPermissionCatalog).

    The function examines all attributes of these classes, verifies that the tasks are valid
    (have 'name' and 'code' fields),

    and creates a PermissionApiKey object for each.

    Arguments:
    catalog_classes(list): List of permission catalog classes.

    Returns:
    list: List of PermissionApiKey, ready to be inserted into the database.
    """
    permissions = []
    for catalog in catalog_classes:
        for attr in dir(catalog):
            if not attr.startswith("__"):
                perm = getattr(catalog, attr)
                if hasattr(perm, "name") and hasattr(perm, "code"):
                    permissions.append(
                        PermissionApiKey(
                            name=perm.name,
                            code=perm.code,
                            description=perm.description,
                        )
                    )
    return permissions


# Permissões para usuários do sistema (incluindo roles de sistema)
initial_user_permissions = get_all_permissions([
    UserRoleCatalog,
    UserPermissionCatalog,
    PrinterPermissionCatalog,
    SupplyPermissionCatalog,
    DepartmentPermissionCatalog,
    MaintenancePermissionCatalog,
    HistoryPermissionCatalog,
    LogPermissionCatalog,
])

# Permissões para API keys (excluindo roles de sistema admin/member)
initial_api_permissions = get_all_api_permissions([
    UserPermissionCatalog,
    PrinterPermissionCatalog,
    SupplyPermissionCatalog,
    DepartmentPermissionCatalog,
    MaintenancePermissionCatalog,
    HistoryPermissionCatalog,
    LogPermissionCatalog,
])

# --- English Data ---
initial_supply_types_en = [
    SupplyType(name="Toner"),
    SupplyType(name="Cartridge"),
    SupplyType(name="Ink"),
    SupplyType(name="Toner/Drum"),
]
initial_departments_en = [
    Department(name="ADM", description="HR Department"),
    Department(name="Warehouse", description="Finance Department"),
    Department(name="Sales", description="Sales Department"),
    Department(name="Stock", description="Stock Department"),
]
initial_supplies_en = [
    Supply(name="Toner", supply_type_id=1, brand="Katun", description="Toner for Kyocera printers"),
    Supply(name="Toner", supply_type_id=1, brand="D-camp", description="Toner for Kyocera printers"),
    Supply(name="Cartridge", supply_type_id=2, brand="Epson", description="Cartridge for Epson printers"),
    Supply(name="Ink", supply_type_id=3, brand="Epson", description="Ink for Epson printers"),
    Supply(name="Toner/Drum", supply_type_id=4, brand="OKI", description="Toner/Drum for OKI printer"),
]
initial_status_en = [
    Status(status="Excellent", description="Printer with Toner >= 80%"),
    Status(status="Good", description="Printer with Toner >= 50%"),
    Status(status="Fair", description="Printer with Toner >= 20%"),
    Status(status="Poor", description="Printer with Toner < 20%"),
    Status(status="Critical", description="Printer with Toner < 10%"),
    Status(status="Under Maintenance", description="Printer is under maintenance"),
    Status(status="Stopped (No Defect)", description="Printer stopped (no defect)"),
    Status(status="Stopped (With Defect)", description="Printer stopped (with defect)"),
    Status(status="Not Available", description="Status not available"),
]

# --- Portuguese Data ---
initial_supply_types_pt = [
    SupplyType(name="Toner"),  # id 1
    SupplyType(name="Cartucho"),  # id 2
    SupplyType(name="Tinta"),  # id 3
    SupplyType(name="Toner/Tabor"),  # id 4
]
initial_departments_pt = [
    Department(name="ADM", description="Departamento de RH"),  # id 1
    Department(name="Almoxarifado", description="Departamento de Financeiro"),  # id 2
    Department(name="Vendas", description="Departamento de Vendas"),  # id 3
    Department(name="Estoque", description="Departamento de Estoque"),  # id 4
]
initial_supplies_pt = [
    Supply(name="Toner", supply_type_id=1, brand="Katun", description="Toner para impressoras kyocera"),
    Supply(name="Toner", supply_type_id=1, brand="D-camp", description="Toner para impressoras kyocera"),
    Supply(name="Cartucho", supply_type_id=2, brand="Epson", description="Cartucho para impressoras epson"),
    Supply(name="Tinta", supply_type_id=3, brand="Epson", description="Tinta para impressoras epson"),
    Supply(name="Toner/Tabor", supply_type_id=4, brand="OKI", description="Toner/Tabor da impressora OKI"),
]
initial_status_pt = [
    Status(status="Excelente", description="Impressora com Toner >= 80%"),  # id 1
    Status(status="Bom", description="Impressora com Toner >= 50%"),  # id 2
    Status(status="Regular", description="Impressora com Toner >= 20%"),  # id 3
    Status(status="Ruim", description="Impressora com Toner < 20%"),  # id 4
    Status(status="Péssimo", description="Impressora com Toner < 10%"),  # id 5
    Status(status="Em manutenção", description="Impressora em manutenção"),  # id 6
    Status(status="Parada s/ defeito", description="Impressora parada (sem defeito)"),  # id 7
    Status(status="Parada c/ defeito", description="Impressora parada (com defeito)"),  # id 8
    Status(status="Não Disponível", description="Status não disponível"),  # id 9
]


async def create_super_user(session: AsyncSession):
    """Creates the super user and its configuration if it doesn't exist."""
    super_user_login = "fastprinter_admin"

    # Check if super user already exists
    result = await session.execute(select(User).where(User.login == super_user_login))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        print("Super Admin user already exists. Skipping creation.")
        return

    # Create super user
    print("Creating Super Admin user...")
    super_user = User(
        login=super_user_login,
        name="Super Admin",
        role=UsersRoleSchema.admin,
        password_hash=get_password_hash("123456"),
    )
    session.add(super_user)
    await session.flush()

    print("Creating Super Admin user configuration...")
    user_config = UserConfiguration(
        user_id=super_user.id,
        username=super_user_login,
        webhook_enabled=False,
        webhook_url=None,
        first_access=False,
    )
    session.add(user_config)
    await session.commit()
    print("Super Admin user and configuration created successfully.")


async def insert_with_check(session: AsyncSession, model, data, name: str):
    """Helper function to insert data with verification"""
    result = await session.execute(select(model).limit(1))
    if not result.scalar_one_or_none():
        session.add_all(data)
        await session.commit()
        print(f"{name} added successfully.")
    else:
        print(f"{name} already exist. None added.")


async def initialize_database(use_portuguese: bool = False):
    if use_portuguese:
        initial_supply_types = initial_supply_types_pt
        initial_supplies = initial_supplies_pt
        initial_status = initial_status_pt
        initial_departments = initial_departments_pt
        print("Iniciando o banco de dados em Português...")
    else:
        initial_supply_types = initial_supply_types_en
        initial_supplies = initial_supplies_en
        initial_status = initial_status_en
        initial_departments = initial_departments_en
        print("Initializing database in English...")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
            print("Tables created/verified successfully.")

        async with AsyncSession(engine) as session:
            await insert_with_check(session, PermissionUser, initial_user_permissions, "User permissions")

            await insert_with_check(session, PermissionApiKey, initial_api_permissions, "Api key permissions")

            await insert_with_check(session, SupplyType, initial_supply_types, "Supply types")

            await insert_with_check(session, Supply, initial_supplies, "Supplies")

            await insert_with_check(session, Status, initial_status, "Statuses")

            await insert_with_check(session, Department, initial_departments, "Departments")

            await create_super_user(session)

        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    use_pt = "-p" in sys.argv
    asyncio.run(initialize_database(use_portuguese=use_pt))
