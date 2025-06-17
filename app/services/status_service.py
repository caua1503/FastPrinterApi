from http import HTTPStatus

from fastapi import HTTPException
from models.model_db import Status
from schemas.status_schema import StatusSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_status(status: StatusSchema, session: AsyncSession):
    status_db = Status(status=status.status, descricao=status.descricao)
    session.add(status_db)
    await session.commit()
    await session.refresh(status_db)
    return status_db


async def get_status(session: AsyncSession):
    status = (await session.scalars(select(Status))).all()
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
    status_db.descricao = status.descricao

    await session.commit()
    await session.refresh(status_db)

    return status_db


async def delete_status(id: int, session: AsyncSession):
    status_db = await session.scalar(select(Status).where(Status.id == id))
    if not status_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    await session.delete(status_db)
    await session.commit()
    return status_db
