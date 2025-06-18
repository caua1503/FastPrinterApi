from http import HTTPStatus

from fastapi import HTTPException
from models.printer_model import Printer
from schemas.printer_schema import FullPrinterSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_printer(session: AsyncSession, printer: FullPrinterSchema):
    # Verificar se IP já existe
    existing_printer = await session.scalar(select(Printer).where(Printer.ip == printer.ip))

    if existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O IP ja esta sendo usado",
        )

    # Criar nova impressora
    db_printer = Printer(
        supply_id=printer.supply_id,
        status_id=printer.status_id,
        name=printer.name,
        brand=printer.brand,
        model=printer.model,
        ip=printer.ip,
        department_id=printer.department_id ,
        description=printer.description,
        forecast=printer.forecast,
        last_refill=printer.last_refill,
        last_maintenance=printer.last_maintenance,
        last_check=printer.last_check,
    )

    session.add(db_printer)
    await session.commit()
    await session.refresh(db_printer)

    return db_printer


async def get_printers(session: AsyncSession, limit: int, offset: int):
    printers = (await session.scalars(select(Printer).limit(limit).offset(offset))).all()
    return printers


async def get_printer_id(session: AsyncSession, id: int):
    printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    return printer


async def get_printer_department_id(session: AsyncSession, department_id: int, limit: int, offset: int):
    printer_in_department = await session.scalars(
        select(Printer).where(Printer.department_id == department_id).limit(limit).offset(offset)
    )

    if not printer_in_department:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Printer not found in department")

    return printer_in_department


async def get_printer_supply_id(session: AsyncSession, supply_id: int, limit: int, offset: int):
    printer_in_supply = await session.scalars(
        select(Printer).where(Printer.supply_id == supply_id).limit(limit).offset(offset)
    )

    if not printer_in_supply:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Printer not found in supply")

    return printer_in_supply


async def get_printer_status_id(session: AsyncSession, status_id: int, limit: int, offset: int):
    printer_in_status = await session.scalars(
        select(Printer).where(Printer.status_id == status_id).limit(limit).offset(offset)
    )

    if not printer_in_status:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Printer not found in status")

    return printer_in_status


async def delete_printer(session: AsyncSession, id: int):
    printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    await session.delete(printer)
    await session.commit()


async def update_printer(session: AsyncSession, id: int, printer: FullPrinterSchema):
    existing_printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Impressora não encontrada",
        )

    if existing_printer.ip != printer.ip:
        existing_ip_printer = await session.scalar(select(Printer).where(Printer.ip == printer.ip))

        if existing_ip_printer:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="O IP ja esta sendo usado",
            )

    existing_printer.name = printer.name
    existing_printer.model = printer.model
    existing_printer.ip = printer.ip
    existing_printer.department = printer.department
    existing_printer.description = printer.description
    existing_printer.forecast = printer.forecast
    existing_printer.last_refill = printer.last_refill
    existing_printer.last_maintenance = printer.last_maintenance
    existing_printer.last_check = printer.last_check
    existing_printer.status_id = printer.status_id
    existing_printer.supply_id = printer.supply_id

    await session.commit()
    await session.refresh(existing_printer)

    return existing_printer
