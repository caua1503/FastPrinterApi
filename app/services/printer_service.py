from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.printer_model import Printer
from app.schemas.filter_schema import FilterPrinter
from app.schemas.printer_schema import FullPrinterSchema


async def create_printer(session: AsyncSession, printer: FullPrinterSchema):
    existing_printer = await session.scalar(select(Printer).where(Printer.ip == printer.ip))

    if existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="IP already exists",
        )

    db_printer = Printer(
        supply_id=printer.supply_id,
        status_id=printer.status_id,
        name=printer.name,
        brand=printer.brand,
        model=printer.model,
        ip=printer.ip,
        department_id=printer.department_id,
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


async def get_printers(session: AsyncSession, filters: FilterPrinter):
    query = select(Printer)

    if filters.status_id:
        query = query.filter(Printer.status_id == filters.status_id)
    if filters.supply_id:
        query = query.filter(Printer.supply_id == filters.supply_id)
    if filters.department_id:
        query = query.filter(Printer.department_id == filters.department_id)

    printers = (await session.scalars(query.limit(filters.limit).offset(filters.offset))).all()

    return printers if printers else []


async def get_printer_id(session: AsyncSession, id: int):
    printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
        )

    return printer


async def delete_printer(session: AsyncSession, id: int):
    printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
        )

    await session.delete(printer)
    await session.commit()


async def update_printer(session: AsyncSession, id: int, printer: FullPrinterSchema):
    existing_printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
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
    existing_printer.brand = printer.brand
    existing_printer.department_id = printer.department_id
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
