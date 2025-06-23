from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.history_model import (
    AlertHistory,
    MaintenanceHistory,
    PrinterTrashHistory,
    RefillHistory,
    StatusHistory,
)
from app.models.printer_model import Printer
from app.models.supply_model import Supply
from app.schemas.filter_schema import FilterPrinter
from app.schemas.history_schema import (
    AlertHistorySchema,
    MaintenanceHistorySchema,
    PrinterTrashHistorySchema,
    RefillHistorySchema,
    StatusHistorySchema,
)

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


async def get_history_recharge(session: AsyncSession, filters: FilterPrinter):
    query = select(RefillHistory)

    if filters.printer_id:
        query = query.filter(RefillHistory.printer_id == filters.printer_id)

    historys = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()

    return historys if historys else []


async def get_history_recharge_id(id: int, session: AsyncSession):
    history = await session.scalar(select(RefillHistory).where(RefillHistory.id == id))
    return history


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


async def get_history_maintenance(session: AsyncSession, filters: FilterPrinter):
    query = select(MaintenanceHistory)

    if filters.printer_id:
        query = query.filter(MaintenanceHistory.printer_id == filters.printer_id)

    historys = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()

    return historys if historys else []


async def get_history_maintenance_id(id: int, session: AsyncSession):
    history = await session.scalar(select(MaintenanceHistory).where(MaintenanceHistory.id == id))

    return history


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


async def get_history_trash(session: AsyncSession, filters: FilterPrinter):
    query = select(PrinterTrashHistory)

    if filters.printer_id:
        query = query.filter(PrinterTrashHistory.printer_id == filters.printer_id)

    historys = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()
    return historys if historys else []


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

    return AlertHistorySchema(
        printer_id=history_db.printer_id,
        date=history_db.date,
        alert_type=history_db.alert_type,
        description=history_db.description,
    )


async def get_history_alerts(session: AsyncSession, filters: FilterPrinter):
    query = select(AlertHistory)

    if filters.printer_id:
        query = query.filter(AlertHistory.printer_id == filters.printer_id)

    historys = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()
    return historys if historys else []


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


"""
ROTA DE HISTORICO DE STATUS
"""


async def create_history_status(history: StatusHistorySchema, session: AsyncSession):
    history_db = StatusHistory(
        printer_id=history.printer_id, status_id=history.status_id, date=history.date, description=history.description
    )
    session.add(history_db)
    await session.commit()
    await session.refresh(history_db)
    return history_db


async def get_history_status(session: AsyncSession, filters: FilterPrinter):
    query = select(StatusHistory)

    if filters.printer_id:
        query = query.filter(StatusHistory.printer_id == filters.printer_id)

    historys = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()
    return historys if historys else []


async def get_history_status_id(id: int, session: AsyncSession):
    history = await session.scalar(select(StatusHistory).where(StatusHistory.id == id))
    return history


async def update_history_status(id: int, history: StatusHistorySchema, session: AsyncSession):
    history_db = await session.scalar(select(StatusHistory).where(StatusHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    history_db.status_id = history.status_id
    history_db.date = history.date
    history_db.description = history.description

    await session.commit()
    await session.refresh(history_db)
    return history_db


async def delete_history_status(id: int, session: AsyncSession):
    history_db = await session.scalar(select(StatusHistory).where(StatusHistory.id == id))

    if not history_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="History not found")

    await session.delete(history_db)
    await session.commit()
