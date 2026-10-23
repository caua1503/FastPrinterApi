from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.maintenance_helper import (  # noqa: F401
    _positive_intervals,
    calculate_next_recharge,
    calculate_recharge_percentage,
    calculate_trash_cleaning_next_time,
    calculate_trash_cleaning_percentage,
)
from app.models.history_model import AlertHistory, PrinterTrashHistory, RefillHistory
from app.schemas.filter_schema import FilterBase
from app.schemas.history_schema import AlertHistorySchema


async def create_history_alert_core(history: AlertHistorySchema, session: AsyncSession) -> AlertHistorySchema:
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


async def extract_dates_recharge(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_recharge = (
        await session.scalars(
            select(RefillHistory)
            .where(RefillHistory.printer_id == printer_id)
            .order_by(RefillHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_recharge:
        return [recharge.date for recharge in history_recharge]
    else:
        return []


async def extract_trash_dates(printer_id: int, session: AsyncSession, filters: FilterBase) -> List:
    history_trash = (
        await session.scalars(
            select(PrinterTrashHistory)
            .where(PrinterTrashHistory.printer_id == printer_id)
            .order_by(PrinterTrashHistory.date.desc())
            .limit(filters.limit)
        )
    ).all()
    if history_trash:
        return [trash.date for trash in history_trash]
    else:
        return []
