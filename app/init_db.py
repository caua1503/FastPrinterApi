from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models.model_db import table_registry, Insumo, Status, Tipo_Insumo
from config import DATABASE_URL

# Configure seu banco de dados
engine = create_engine(DATABASE_URL, echo=True)

# Cria todas as tabelas
table_registry.metadata.create_all(bind=engine)

# Dados iniciais
tipo_insumo_iniciais = [
    Tipo_Insumo(nome="Toner"), #id 1
    Tipo_Insumo(nome="Cartucho"), #id 2
    Tipo_Insumo(nome="Tinta"), #id 3
    Tipo_Insumo(nome="Toner/Tabor"), #id 4
]

insumos_iniciais = [
    Insumo(nome="Toner", tipo_insumo=1, marca="Katun", descricao="Toner para impressoras kyocera"), #id 1
    Insumo(nome="Toner", tipo_insumo=1, marca="D-camp", descricao="Toner para impressoras kyocera"), #id 2
    Insumo(nome="Tinta", tipo_insumo=3, marca="Epson", descricao="Tinta para impressoras epson"), #id 3
    Insumo(nome="Cartucho", tipo_insumo=2, marca="Epson", descricao="Cartucho para impressoras epson"), #id 4
    Insumo(nome="Toner/Tabor", tipo_insumo=4, marca="OKI", descricao="Toner/Tabor da impressora OKI"), #id 5
]

status_iniciais = [
    Status(status="Excelente", descricao="Impressora com Toner >= 80%"), #id 1
    Status(status="Bom", descricao="Impressora com Toner >= 50%"), #id 2
    Status(status="Regular", descricao="Impressora com Toner >= 20%"), #id 3
    Status(status="Ruim", descricao="Impressora com Toner < 20%"), #id 4
    Status(status="Péssimo", descricao="Impressora com Toner < 10%"), #id 5
    Status(status="Em manutenção", descricao="Impressora em manutenção"), #id 6
    Status(status="Parada s/ defeito", descricao="Impressora parada (sem defeito)"), #id 7
    Status(status="Parada c/ defeito", descricao="Impressora parada (com defeito)"), #id 8
    Status(status="Não Disponível", descricao="Status não disponível"), #id 9
]

with Session(engine) as session:
    if not session.execute(select(Tipo_Insumo)).first():
        session.add_all(tipo_insumo_iniciais)
        print("✅ Tipos de insumo adicionados.")
    else:
        print("ℹ️ Tipos de insumo já existem. Nenhum novo inserido.")

    if not session.execute(select(Insumo)).first():
        session.add_all(insumos_iniciais)
        print("✅ Insumos adicionados.")
    else:
        print("ℹ️ Insumos já existem. Nenhum novo inserido.")

    if not session.execute(select(Status)).first():
        session.add_all(status_iniciais)
        print("✅ Status adicionados.")
    else:
        print("ℹ️ Status já existem. Nenhum novo inserido.")

    session.commit()
    print("✅ Banco de dados inicializado com sucesso.")
