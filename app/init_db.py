import asyncio

from config import Config
from models.model_db import Insumo, Status, Tipo_Insumo, table_registry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Configure seu banco de dados
engine = create_async_engine(Config().DATABASE_URL, echo=True)

# Dados iniciais
tipo_insumo_iniciais = [
    Tipo_Insumo(nome="Toner"),  # id 1
    Tipo_Insumo(nome="Cartucho"),  # id 2
    Tipo_Insumo(nome="Tinta"),  # id 3
    Tipo_Insumo(nome="Toner/Tabor"),  # id 4
]

insumos_iniciais = [
    Insumo(nome="Toner", tipo_insumo=1, marca="Katun", descricao="Toner para impressoras kyocera"),  # id 1
    Insumo(nome="Toner", tipo_insumo=1, marca="D-camp", descricao="Toner para impressoras kyocera"),  # id 2
    Insumo(nome="Tinta", tipo_insumo=3, marca="Epson", descricao="Tinta para impressoras epson"),  # id 3
    Insumo(nome="Cartucho", tipo_insumo=2, marca="Epson", descricao="Cartucho para impressoras epson"),  # id 4
    Insumo(nome="Toner/Tabor", tipo_insumo=4, marca="OKI", descricao="Toner/Tabor da impressora OKI"),  # id 5
]

status_iniciais = [
    Status(status="Excelente", descricao="Impressora com Toner >= 80%"),  # id 1
    Status(status="Bom", descricao="Impressora com Toner >= 50%"),  # id 2
    Status(status="Regular", descricao="Impressora com Toner >= 20%"),  # id 3
    Status(status="Ruim", descricao="Impressora com Toner < 20%"),  # id 4
    Status(status="Péssimo", descricao="Impressora com Toner < 10%"),  # id 5
    Status(status="Em manutenção", descricao="Impressora em manutenção"),  # id 6
    Status(status="Parada s/ defeito", descricao="Impressora parada (sem defeito)"),  # id 7
    Status(status="Parada c/ defeito", descricao="Impressora parada (com defeito)"),  # id 8
    Status(status="Não Disponível", descricao="Status não disponível"),  # id 9
]


async def init_db():
    try:
        # Cria todas as tabelas assincronamente
        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.create_all)
            print("✅ Tabelas criadas/verificadas com sucesso.")

        async with AsyncSession(engine) as session:
            # Verifica e insere tipos de insumo
            result = await session.execute(select(Tipo_Insumo).limit(1))
            if not result.scalar_one_or_none():
                session.add_all(tipo_insumo_iniciais)
                await session.commit()
                print("✅ Tipos de insumo adicionados.")
            else:
                print("ℹ️ Tipos de insumo já existem. Nenhum novo inserido.")

            # Verifica e insere insumos
            result = await session.execute(select(Insumo).limit(1))
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

        print("✅ Banco de dados inicializado com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
