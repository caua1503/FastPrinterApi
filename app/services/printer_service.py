from http import HTTPStatus

from fastapi import HTTPException
from models.model_db import Impressora
from models.printer_model import FullPrinterSchema, FullPrinterSchemaDB
from sqlalchemy import select
from sqlalchemy.orm import Session


async def create_printer(printer: FullPrinterSchema, session: Session) -> FullPrinterSchemaDB:
    # Verificar se IP já existe
    existing_printer = session.scalar(select(Impressora).where(Impressora.ip == printer.ip))

    if existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O IP ja esta sendo usado",
        )

    # Criar nova impressora
    db_printer = Impressora(
        id_insumo=printer.id_insumo,
        id_status=printer.id_status,
        name=printer.name,
        marca=printer.marca,
        model=printer.model,
        ip=printer.ip,
        setor=printer.setor,
        descricao=printer.descricao,
        previsao=printer.previsao,
        ultima_recarga=printer.ultima_recarga,
        ultima_manutencao=printer.ultima_manutencao,
        ultima_verificacao=printer.ultima_verificacao,
    )

    session.add(db_printer)
    session.commit()
    session.refresh(db_printer)

    return db_printer


async def get_printers(session: Session, limit: int, offset: int):
    printers = session.scalars(select(Impressora).limit(limit).offset(offset)).all()

    return printers


async def delete_printer(id: int, session: Session):
    printer = session.scalar(select(Impressora).where(Impressora.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    session.delete(printer)
    session.commit()


async def update_printer(id: int, printer: FullPrinterSchema, session: Session):
    printer_db = session.scalar(select(Impressora).where(Impressora.id == id))

    if not printer_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    printer_db.name = printer.name
    printer_db.model = printer.model
    printer_db.ip = printer.ip
    printer_db.setor = printer.setor
    printer_db.descricao = printer.descricao
    printer_db.previsao = printer.previsao
    printer_db.ultima_recarga = printer.ultima_recarga
    printer_db.ultima_manutencao = printer.ultima_manutencao
    printer_db.ultima_verificacao = printer.ultima_verificacao
    printer_db.id_status = printer.id_status
    printer_db.id_insumo = printer.id_insumo

    session.commit()
    session.refresh(printer_db)

    return printer_db


async def get_printer(id: int, session: Session) -> FullPrinterSchemaDB:
    printer = session.scalar(select(Impressora).where(Impressora.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    return printer
