from http import HTTPStatus

from fastapi import HTTPException
from models.status_model import StatusSchema, StatusSchemaDB
from sqlalchemy import select
from sqlalchemy.orm import Session


async def create_status(status: StatusSchema, session: Session) -> StatusSchemaDB:
    status_db = StatusSchemaDB(status=status.status, descricao=status.descricao)
    session.add(status_db)
    session.commit()
    session.refresh(status_db)
    return status_db


async def get_status(session: Session):
    status = session.scalars(select(StatusSchemaDB)).all()
    if not status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")
    return status


async def get_status_id(id: int, session: Session):
    status = session.scalar(select(StatusSchemaDB).where(StatusSchemaDB.id == id))
    if not status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    return status


async def update_status(id: int, status: StatusSchema, session: Session):
    status_db = session.scalar(select(StatusSchemaDB).where(StatusSchemaDB.id == id))
    if not status_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    status_db.status = status.status
    status_db.descricao = status.descricao

    session.commit()
    session.refresh(status_db)

    return status_db


async def delete_status(id: int, session: Session):
    status_db = session.scalar(select(StatusSchemaDB).where(StatusSchemaDB.id == id))
    if not status_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Status not found")

    session.delete(status_db)
    session.commit()
    return status_db
