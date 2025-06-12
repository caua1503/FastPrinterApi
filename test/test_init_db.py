import os
import sys
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Adicionar o diretório raiz ao path para permitir imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
app_path = os.path.join(project_root, 'app')
sys.path.insert(1, app_path)

from app.models.model_db import table_registry, Insumo, Status
from app.config.config import DATABASE_URL

# Configure seu banco de dados
engine = create_engine(DATABASE_URL, echo=True)

# Cria todas as tabelas
table_registry.metadata.create_all(bind=engine)

# Dados iniciais
insumos_iniciais = [
    Insumo(tipo_insumo="Toner", marca="Katun", descricao="Toner para impressoras kyocera"),
    Insumo(tipo_insumo="Toner", marca="D-camp", descricao="Toner para impressoras kyocera"),
    Insumo(tipo_insumo="Cartucho", marca="Epson", descricao="Cartucho para impressoras epson"),
    Insumo(tipo_insumo="Toner/Tabor", marca="OKI", descricao="Toner/Tabor da impressora OKI"),
]

status_iniciais = [
    Status(status="Excelente", descricao="Impressora com Toner >= 80%"),
    Status(status="Bom", descricao="Impressora com Toner >= 50%"),
    Status(status="Regular", descricao="Impressora com Toner >= 20%"),
    Status(status="Ruim", descricao="Impressora com Toner < 20%"),
    Status(status="Péssimo", descricao="Impressora com Toner < 10%"),
    Status(status="Em manutenção", descricao="Impressora em manutenção"),
    Status(status="Parada s/ defeito", descricao="Impressora parada (sem defeito)"),
    Status(status="Parada c/ defeito", descricao="Impressora parada (com defeito)"),
    Status(status="Não Disponível", descricao="Status não disponível"),
]

with Session(engine) as session:
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
