from http import HTTPStatus

from fastapi import HTTPException
from app.models.history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
)
from app.models.printer_model import Printer
from app.models.supply_model import Supply
from app.schemas.history_schema import (
    AlertHistorySchema,
    MaintenanceHistorySchema,
    PrinterTrashHistorySchema,
    RefillHistorySchema,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

"""

ROTA DE HISTORICO DE RECARGA

"""


async def create_history_recharge(history: RefillHistorySchema, session: AsyncSession):
    exist_printer = await session.scalar(select(Printer).where(Printer.id == history.printer_id))

    if not exist_printer:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Printer not found")

    exist_supply = await session.scalar(select(Supply).where(Supply.id == history.supply_id))

    if not exist_supply:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Supply not found")

    history_db = RefillHistory(
        printer_id=history.printer_id,
        date=history.date,
        event_type=history.event_type,
        supply_id=history.supply_id,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_recharge(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(RefillHistory).limit(limit).offset(offset))).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def get_history_recharge_id(id: int, session: AsyncSession):
    history = await session.scalar(select(RefillHistory).where(RefillHistory.id == id))

    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return history


async def get_history_recharge_printer_id(printer_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(RefillHistory).where(RefillHistory.printer_id == printer_id).limit(limit).offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_recharge(id: int, history: RefillHistorySchema, session: AsyncSession):
    history_db = await session.scalar(select(RefillHistory).where(RefillHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.printer_id = history.printer_id
    history_db.date = history.date
    history_db.event_type = history.event_type
    history_db.supply_id = history.supply_id
    history_db.description = history.description

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_recharge(id: int, session: AsyncSession):
    history_db = await session.scalar(select(RefillHistory).where(RefillHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()
    return True


"""
ROTA DE HISTORICO DE MANUTENÇÃO
"""


async def create_history_maintenance(history: MaintenanceHistorySchema, session: AsyncSession):
    history_db = MaintenanceHistory(
        printer_id=history.printer_id,
        date=history.date,
        event_type=history.event_type,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_maintenance(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(MaintenanceHistory).limit(limit).offset(offset))).all()
    return historys


async def get_history_maintenance_id(id: int, session: AsyncSession):
    history = await session.scalar(select(MaintenanceHistory).where(MaintenanceHistory.id == id))

    if not history:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return history


async def get_history_maintenance_printer_id(printer_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(MaintenanceHistory).where(MaintenanceHistory.printer_id == printer_id).limit(limit).offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_maintenance(id: int, history: MaintenanceHistorySchema, session: AsyncSession):
    history_db = await session.scalar(select(MaintenanceHistory).where(MaintenanceHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.printer_id = history.printer_id
    history_db.date = history.date
    history_db.event_type = history.event_type
    history_db.description = history.description

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_maintenance(id: int, session: AsyncSession):
    history_db = await session.scalar(select(MaintenanceHistory).where(MaintenanceHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True


"""
ROTA DE HISTORICO DE LIMPEZA DE LIXEIRA
"""


async def create_history_trash(history: PrinterTrashHistorySchema, session: AsyncSession):
    history_db = PrinterTrashHistory(
        printer_id=history.printer_id,
        date=history.date,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_trash(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(PrinterTrashHistory).limit(limit).offset(offset))).all()
    return historys


async def get_history_trash_printer_id(printer_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(PrinterTrashHistory).where(PrinterTrashHistory.printer_id == printer_id).limit(limit).offset(offset)
        )
    ).all()

    if not historys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    return historys


async def update_history_trash(id: int, history: PrinterTrashHistorySchema, session: AsyncSession):
    history_db = await session.scalar(select(PrinterTrashHistory).where(PrinterTrashHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.printer_id = history.printer_id
    history_db.date = history.date
    history_db.description = history.description

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_trash(id: int, session: AsyncSession):
    history_db = await session.scalar(select(PrinterTrashHistory).where(PrinterTrashHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True


"""
ROTA DE HISTORICO DE ALERTA
"""


async def create_history_alert(history: AlertHistorySchema, session: AsyncSession) -> AlertHistorySchema:
    history_db = AlertHistory(
        printer_id=history.printer_id,
        date=history.date,
        alert_type=history.alert_type,
        description=history.description,
    )

    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_alert(session: AsyncSession, limit: int, offset: int):
    historys = (await session.scalars(select(AlertHistory).limit(limit).offset(offset))).all()
    return historys


async def get_history_alert_printer_id(printer_id: int, limit: int, offset: int, session: AsyncSession):
    historys = (
        await session.scalars(
            select(AlertHistory).where(AlertHistory.printer_id == printer_id).limit(limit).offset(offset)
        )
    ).all()
    return historys


async def update_history_alert(id: int, history: AlertHistorySchema, session: AsyncSession):
    history_db = await session.scalar(select(AlertHistory).where(AlertHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.printer_id = history.printer_id
    history_db.date = history.date
    history_db.alert_type = history.alert_type
    history_db.description = history.description

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_alert(id: int, session: AsyncSession):
    history_db = await session.scalar(select(AlertHistory).where(AlertHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()

    return True
