from http import HTTPStatus
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from helpers.db_helper import get_session
from typing import Optional, List, Dict, Any
from models.model_db import Historico_Recarga, Historico_Manutencao
from models.history_model import (HistoryRecargaSchema, HistoryRecargaSchemaDB, 
                            HistoryManutencaoSchema, HistoryManutencaoSchemaDB)
"""

ROTA DE HISTORICO DE RECARGA

"""

async def create_history_recharge(history: HistoryRecargaSchema, session: Session) -> HistoryRecargaSchema:
    history_db = Historico_Recarga(
        impressora_id=history.impressora_id,
        data=history.data,
        tipo_evento=history.tipo_evento,
        id_insumo=history.id_insumo,
        descricao=history.descricao
    )
    session.add(history_db)
    session.commit()
    session.refresh(history_db)
    return history_db

async def get_history_recharge(session: Session, limit: int, offset: int) -> HistoryRecargaSchemaDB:
    historys = session.scalars(
        select(Historico_Recarga).limit(limit).offset(offset)
        ).all()
    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    return historys

async def get_history_recharge_id(id: int, session: Session) -> HistoryRecargaSchemaDB:
    history = session.scalar(
        select(Historico_Recarga).where(Historico_Recarga.id == id)
    )
    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    return history

async def get_history_recharge_printer_id(impressora_id: int, limit: int, offset: int, session: Session) -> List[HistoryRecargaSchemaDB]:
    historys = session.scalars(
        select(Historico_Recarga)
        .where(Historico_Recarga.impressora_id == impressora_id)
        .limit(limit)
        .offset(offset)
        ).all()
    
    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    return historys

async def update_history_recharge(id: int, history: HistoryRecargaSchema, session: Session):
    history_db = session.scalar(
        select(Historico_Recarga).where(Historico_Recarga.id == id)
    )
    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.tipo_evento = history.tipo_evento
    history_db.id_insumo = history.id_insumo
    history_db.descricao = history.descricao

    session.commit()
    session.refresh(history_db)
    return history_db

async def delete_history_recharge(id: int, session: Session):
    history_db = session.scalar(
        select(Historico_Recarga).where(Historico_Recarga.id == id)
    )
    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    session.delete(history_db)
    session.commit()
    return True


"""
ROTA DE HISTORICO DE MANUTENÇÃO
"""

async def create_history_maintenance(history: HistoryManutencaoSchema, session: Session) -> HistoryManutencaoSchema:

    history_db = Historico_Manutencao(
        impressora_id=history.impressora_id,
        data=history.data,
        tipo_evento=history.tipo_evento,
        descricao=history.descricao
    )
    session.add(history_db)
    session.commit()
    session.refresh(history_db)
    return history_db


async def get_history_maintenance(session: Session, limit: int, offset: int) -> List[HistoryManutencaoSchemaDB]:
    historys = session.scalars(
        select(Historico_Manutencao).limit(limit).offset(offset)
        ).all()
    return historys

async def get_history_maintenance_id(id: int, session: Session) -> HistoryManutencaoSchemaDB:
    history = session.scalar(
        select(Historico_Manutencao).where(Historico_Manutencao.id == id)
    )
    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    return history

async def get_history_maintenance_printer_id(impressora_id: int, limit: int, offset: int, session: Session):
    historys = session.scalars(
        select(Historico_Manutencao)
        .where(Historico_Manutencao.impressora_id == impressora_id)
        .limit(limit)
        .offset(offset)
        ).all()
    
    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    return historys


async def update_history_maintenance(id: int, history: HistoryManutencaoSchema, session: Session):
    history_db = session.scalar(
        select(Historico_Manutencao).where(Historico_Manutencao.id == id)
    )
    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.tipo_evento = history.tipo_evento    
    history_db.descricao = history.descricao

    session.commit()
    session.refresh(history_db)
    return history_db

async def delete_history_maintenance(id: int, session: Session):
    history_db = session.scalar(
        select(Historico_Manutencao).where(Historico_Manutencao.id == id)
    )
    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")
    
    session.delete(history_db)
    session.commit()

    return True

