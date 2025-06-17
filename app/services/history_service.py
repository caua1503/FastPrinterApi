from http import HTTPStatus

from fastapi import HTTPException
from models.model_db import Historico_Alerta, Historico_Lixeira_Impressora, Historico_Manutencao, Historico_Recarga
from schemas.history_schema import (
    HistoryAlertaSchema,
    HistoryLixeiraSchema,
    HistoryManutencaoSchema,
    HistoryRecargaSchema,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

"""

ROTA DE HISTORICO DE RECARGA

"""


async def create_history_recharge(history: HistoryRecargaSchema, session: AsyncSession):
    history_db = Historico_Recarga(
        impressora_id=history.impressora_id,
        data=history.data,
        tipo_evento=history.tipo_evento,
        id_insumo=history.id_insumo,
        descricao=history.descricao,
    )

    await session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_recharge(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(Historico_Recarga).limit(limit).offset(offset))).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def get_history_recharge_id(id: int, session: AsyncSession):
    history = await session.scalar(select(Historico_Recarga).where(Historico_Recarga.id == id))

    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return history


async def get_history_recharge_printer_id(impressora_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(Historico_Recarga)
            .where(Historico_Recarga.impressora_id == impressora_id)
            .limit(limit)
            .offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_recharge(id: int, history: HistoryRecargaSchema, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Recarga).where(Historico_Recarga.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.tipo_evento = history.tipo_evento
    history_db.id_insumo = history.id_insumo
    history_db.descricao = history.descricao

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_recharge(id: int, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Recarga).where(Historico_Recarga.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()
    return True


"""
ROTA DE HISTORICO DE MANUTENÇÃO
"""


async def create_history_maintenance(history: HistoryManutencaoSchema, session: AsyncSession):
    history_db = Historico_Manutencao(
        impressora_id=history.impressora_id,
        data=history.data,
        tipo_evento=history.tipo_evento,
        descricao=history.descricao,
    )

    await session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_maintenance(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(Historico_Manutencao).limit(limit).offset(offset))).all()
    return historys


async def get_history_maintenance_id(id: int, session: AsyncSession):
    history = await session.scalar(select(Historico_Manutencao).where(Historico_Manutencao.id == id))

    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return history


async def get_history_maintenance_printer_id(impressora_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(Historico_Manutencao)
            .where(Historico_Manutencao.impressora_id == impressora_id)
            .limit(limit)
            .offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_maintenance(id: int, history: HistoryManutencaoSchema, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Manutencao).where(Historico_Manutencao.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.tipo_evento = history.tipo_evento
    history_db.descricao = history.descricao

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_maintenance(id: int, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Manutencao).where(Historico_Manutencao.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True


"""
ROTA DE HISTORICO DE LIMPEZA DE LIXEIRA
"""


async def create_history_trash(history: HistoryLixeiraSchema, session: AsyncSession):
    history_db = Historico_Lixeira_Impressora(
        impressora_id=history.impressora_id,
        data=history.data,
        descricao=history.descricao,
    )

    await session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_trash(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(Historico_Lixeira_Impressora).limit(limit).offset(offset))).all()
    return historys


async def get_history_trash_printer_id(impressora_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(Historico_Lixeira_Impressora)
            .where(Historico_Lixeira_Impressora.impressora_id == impressora_id)
            .limit(limit)
            .offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_trash(id: int, history: HistoryLixeiraSchema, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Lixeira_Impressora).where(Historico_Lixeira_Impressora.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.descricao = history.descricao

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_trash(id: int, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Lixeira_Impressora).where(Historico_Lixeira_Impressora.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True


"""
ROTA DE HISTORICO DE ALERTA
"""


async def create_history_alert(history: HistoryAlertaSchema, session: AsyncSession) -> HistoryAlertaSchema:
    history_db = Historico_Alerta(
        impressora_id=history.impressora_id,
        data=history.data,
        tipo_alerta=history.tipo_alerta,
        descricao=history.descricao,
    )

    await session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_alert(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(Historico_Alerta).limit(limit).offset(offset))).all()
    return historys


async def get_history_alert_printer_id(impressora_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(Historico_Alerta).where(Historico_Alerta.impressora_id == impressora_id).limit(limit).offset(offset)
        )
    ).all()
    return historys


async def update_history_alert(id: int, history: HistoryAlertaSchema, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Alerta).where(Historico_Alerta.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.impressora_id = history.impressora_id
    history_db.data = history.data
    history_db.tipo_alerta = history.tipo_alerta
    history_db.descricao = history.descricao

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_alert(id: int, session: AsyncSession):
    history_db = await session.scalar(select(Historico_Alerta).where(Historico_Alerta.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True
