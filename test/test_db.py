import os
import sys
from sqlalchemy import select

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
app_path = os.path.join(project_root, 'app')
sys.path.insert(1, app_path)

from app.models.model_db import Impressora

def test_create_printer_db(session):
    printer = Impressora(name="teste", 
                    model="teste", 
                    ip="192.168.1.1", 
                    marca="teste",
                    setor="teste",
                    id_status="teste",
                    descricao="teste",
                    previsao="teste",
                    id_insumo="teste",
                    ultima_recarga="teste",
                    ultima_manutencao="teste",
                    ultima_verificacao="teste")

    session.add(printer)
    session.commit()
    result= session.scalar(
        select(Impressora).where(Impressora.ip ==  "192.168.1.1")
    )

    assert result.ip == "192.168.1.1"