from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.history_model import StatusHistory
from app.models.printer_model import Printer, Status
from app.schemas.filters import FilterBase
from app.schemas.status_schema import StatusSchema


async def create_status(status: StatusSchema, session: AsyncSession):
    status_db = Status(status=status.status, description=status.description)
    session.add(status_db)
    await session.commit()
    await session.refresh(status_db)
    return status_db


async def get_status(session: AsyncSession, filters: FilterBase):
    status = (await session.scalars(select(Status).limit(filters.limit).offset(filters.offset))).all()
    if not status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")
    return status


async def get_status_id(id: int, session: AsyncSession):
    status = await session.scalar(select(Status).where(Status.id == id))
    if not status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    return status


async def update_status(id: int, status: StatusSchema, session: AsyncSession):
    status_db = await session.scalar(select(Status).where(Status.id == id))
    if not status_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    status_db.status = status.status
    status_db.description = status.description

    await session.commit()
    await session.refresh(status_db)

    return status_db


async def delete_status(id: int, session: AsyncSession):
    status_db = await session.scalar(select(Status).where(Status.id == id))
    printers = (await session.scalars(select(Printer).where(Printer.status_id == id))).all()
    status_history = (await session.scalars(select(StatusHistory).where(StatusHistory.status_id == id))).all()

    if not status_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    if printers:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Status has printers")

    if status_history:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Status has status history")

    await session.delete(status_db)
    await session.commit()
    return status_db
