from http import HTTPStatus

from fastapi import HTTPException
from models.model_db import Impressora
from schemas.printer_schema import FullPrinterSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_printer(printer: FullPrinterSchema, session: AsyncSession):
    # Verificar se IP já existe
    existing_printer = await session.scalar(select(Impressora).where(Impressora.ip == printer.ip))

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
    await session.commit()
    await session.refresh(db_printer)

    return db_printer


async def get_printers(session: AsyncSession, limit: int, offset: int):
    printers = (await session.scalars(select(Impressora).limit(limit).offset(offset))).all()
    return printers


async def delete_printer(id: int, session: AsyncSession):
    printer = await session.scalar(select(Impressora).where(Impressora.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    await session.delete(printer)
    await session.commit()


async def update_printer(id: int, printer: FullPrinterSchema, session: AsyncSession):
    existing_printer = await session.scalar(select(Impressora).where(Impressora.id == id))

    if not existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    if existing_printer.ip != printer.ip:
        existing_ip_printer = await session.scalar(select(Impressora).where(Impressora.ip == printer.ip))

        if existing_ip_printer:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="O IP ja esta sendo usado",
            )

    existing_printer.name = printer.name
    existing_printer.model = printer.model
    existing_printer.ip = printer.ip
    existing_printer.setor = printer.setor
    existing_printer.descricao = printer.descricao
    existing_printer.previsao = printer.previsao
    existing_printer.ultima_recarga = printer.ultima_recarga
    existing_printer.ultima_manutencao = printer.ultima_manutencao
    existing_printer.ultima_verificacao = printer.ultima_verificacao
    existing_printer.id_status = printer.id_status
    existing_printer.id_insumo = printer.id_insumo

    await session.commit()
    await session.refresh(existing_printer)

    return existing_printer


async def get_printer(id: int, session: AsyncSession):
    printer = await session.scalar(select(Impressora).where(Impressora.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    return printer
