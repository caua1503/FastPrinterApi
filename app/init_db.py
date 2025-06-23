import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.config import Config
from app.models import table_registry
from app.models.department_model import Department
from app.models.printer_model import Status
from app.models.supply_model import Supply, SupplyType
from app.models.user_model import PermissionUser

# Configure seu banco de dados
engine = create_async_engine(Config().DATABASE_URL, echo=True)

# Dados iniciais
permissoes_iniciais = [
    PermissionUser(name="Adminitradores", permissions="all"),
    PermissionUser(name="Usuarios", permissions="all"),
]
tipo_insumo_iniciais = [
    SupplyType(name="Toner"),  # id 1
    SupplyType(name="Cartucho"),  # id 2
    SupplyType(name="Tinta"),  # id 3
    SupplyType(name="Toner/Tabor"),  # id 4
]
departments_iniciais = [
    Department(name="ADM", description="Departamento de RH"),  # id 1
    Department(name="Almoxarifado", description="Departamento de Financeiro"),  # id 2
    Department(name="Vendas", description="Departamento de Vendas"),  # id 3
    Department(name="Estoque", description="Departamento de Estoque"),  # id 4
]
insumos_iniciais = [
    Supply(name="Toner", supply_type_id=1, brand="Katun", description="Toner para impressoras kyocera"),  # id 1
    Supply(name="Toner", supply_type_id=1, brand="D-camp", description="Toner para impressoras kyocera"),  # id 2
    Supply(name="Tinta", supply_type_id=3, brand="Epson", description="Tinta para impressoras epson"),  # id 3
    Supply(name="Cartucho", supply_type_id=2, brand="Epson", description="Cartucho para impressoras epson"),  # id 4
    Supply(name="Toner/Tabor", supply_type_id=4, brand="OKI", description="Toner/Tabor da impressora OKI"),  # id 5
]

status_iniciais = [
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


async def init_db():
    try:
        # Cria todas as tabelas assincronamente
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
            print("✅ Tabelas criadas/verificadas com sucesso.")

        async with AsyncSession(engine) as session:
            # Verifica e insere tipos de insumo
            result = await session.execute(select(SupplyType).limit(1))
            if not result.scalar_one_or_none():
                session.add_all(tipo_insumo_iniciais)
                await session.commit()
                print("✅ Tipos de insumo adicionados.")
            else:
                print("ℹ️ Tipos de insumo já existem. Nenhum novo inserido.")

            # Verifica e insere insumos
            result = await session.execute(select(Supply).limit(1))
            if not result.scalar_one_or_none():
                session.add_all(insumos_iniciais)
                await session.commit()
                print("✅ Insumos adicionados.")
            else:
                print("ℹ️ Insumos já existem. Nenhum novo inserido.")

            # Verifica e insere status
            result = await session.execute(select(Status).limit(1))
            if not result.scalar_one_or_none():
                session.add_all(status_iniciais)
                await session.commit()
                print("✅ Status adicionados.")
            else:
                print("ℹ️ Status já existem. Nenhum novo inserido.")

            # Verifica e insere departamentos
            result = await session.execute(select(Department).limit(1))
            if not result.scalar_one_or_none():
                session.add_all(departments_iniciais)
                await session.commit()
                print("✅ Departamentos adicionados.")
            else:
                print("ℹ️ Departamentos já existem. Nenhum novo inserido.")

        print("✅ Banco de dados inicializado com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
