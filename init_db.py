import asyncio
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.config import Config
from app.models import table_registry
from app.models.department_model import Department
from app.models.printer_model import Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import PermissionUser

# Configure your database
engine = create_async_engine(Config().DATABASE_URL, echo=True)  # type: ignore

# Initial Permissions (Always in English)
initial_permissions = [
    # System Roles
    PermissionUser(name="Administrator", code="admin", description="Full administrative permissions."),
    PermissionUser(name="Member", code="member", description="Basic user permissions."),
    # User Permissions
    PermissionUser(name="user.create", code="user.create", description="Allows creating new users."),
    PermissionUser(name="user.read", code="user.read", description="Allows viewing user information."),
    PermissionUser(name="user.update", code="user.update", description="Allows updating user information."),
    PermissionUser(name="user.delete", code="user.delete", description="Allows deleting users."),
    # Printer Permissions
    PermissionUser(name="printer.create", code="printer.create", description="Allows adding new printers."),
    PermissionUser(name="printer.read", code="printer.read", description="Allows viewing printer information."),
    PermissionUser(name="printer.update", code="printer.update", description="Allows updating printer information."),
    PermissionUser(name="printer.delete", code="printer.delete", description="Allows deleting printers."),
    # Supply Permissions
    PermissionUser(name="supply.create", code="supply.create", description="Allows adding new supplies."),
    PermissionUser(name="supply.read", code="supply.read", description="Allows viewing supply information."),
    PermissionUser(name="supply.update", code="supply.update", description="Allows updating supply information."),
    PermissionUser(name="supply.delete", code="supply.delete", description="Allows deleting supplies."),
    # Department Permissions
    PermissionUser(name="department.create", code="department.create", description="Allows creating new departments."),
    PermissionUser(
        name="department.read", code="department.read", description="Allows viewing department information."
    ),
    PermissionUser(
        name="department.update", code="department.update", description="Allows updating department information."
    ),
    PermissionUser(name="department.delete", code="department.delete", description="Allows deleting departments."),
    # Maintenance Permissions
    PermissionUser(
        name="maintenance.create", code="maintenance.create", description="Allows creating maintenance records."
    ),
    PermissionUser(name="maintenance.read", code="maintenance.read", description="Allows viewing maintenance records."),
    PermissionUser(
        name="maintenance.update", code="maintenance.update", description="Allows updating maintenance records."
    ),
    PermissionUser(
        name="maintenance.delete", code="maintenance.delete", description="Allows deleting maintenance records."
    ),
    # History Permissions
    PermissionUser(name="history.read", code="history.read", description="Allows viewing history records."),
    # Log Permissions
    PermissionUser(name="log.read", code="log.read", description="Allows viewing system logs."),
]

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


async def insert_with_check(session: AsyncSession, model, data, name: str):
    """Helper function to insert data with verification"""
    result = await session.execute(select(model).limit(1))
    if not result.scalar_one_or_none():
        session.add_all(data)
        await session.commit()
        print(f"{name} added successfully.")
        await asyncio.sleep(0.1)  # Wait for 0.1 second after each operation
    else:
        print(f"{name} already exist. None added.")


async def initialize_database(use_portuguese: bool = False):
    # Select data based on the flag
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
        # Asynchronously create all tables
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
            print("Tables created/verified successfully.")
            await asyncio.sleep(1)  # Wait for tables to be fully created

        async with AsyncSession(engine) as session:
            # Sequential initialization with delays

            # 1. First, insert permissions
            await insert_with_check(session, PermissionUser, initial_permissions, "User permissions")

            # 2. Then, insert supply types
            await insert_with_check(session, SupplyType, initial_supply_types, "Supply types")

            # 3. After supply types are inserted, insert supplies
            await insert_with_check(session, Supply, initial_supplies, "Supplies")

            # 4. Insert status
            await insert_with_check(session, Status, initial_status, "Statuses")

            # 5. Finally, insert departments
            await insert_with_check(session, Department, initial_departments, "Departments")

        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    use_pt = "-p" in sys.argv
    asyncio.run(initialize_database(use_portuguese=use_pt))
