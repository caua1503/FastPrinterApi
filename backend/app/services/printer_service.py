from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.printer_model import Printer
from app.schemas.filter_schema import FilterPrinterDefault, OrderBy, OrderByFieldPrinter
from app.schemas.printer_schema import (
    DepartmentIdSchema,
    FullPrinterPublicSchema,
    FullPrinterSchema,
    FullPrinterSchemaDB,
    FullPrinterUpdateSchema,
    ListFullPrinterPublicSchema,
    StatusIdSchema,
    SupplyIdSchema,
)


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

    return FullPrinterSchemaDB.model_validate(db_printer)


async def get_printers(session: AsyncSession, filters: FilterPrinterDefault):
    query = select(Printer)
    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    if not total:
        return ListFullPrinterPublicSchema(total=0, count=0, printers=[])

    if filters.status_id:
        query = query.filter(Printer.status_id == filters.status_id)
    if filters.supply_id:
        query = query.filter(Printer.supply_id == filters.supply_id)
    if filters.department_id:
        query = query.filter(Printer.department_id == filters.department_id)

    if filters.order_by_field:
        order_by_mapping = {
            OrderByFieldPrinter.created_at: Printer.created_at,
            OrderByFieldPrinter.forecast: Printer.forecast,
            OrderByFieldPrinter.last_refill: Printer.last_refill,
            OrderByFieldPrinter.last_maintenance: Printer.last_maintenance,
            OrderByFieldPrinter.last_check: Printer.last_check,
        }
        column = order_by_mapping[filters.order_by_field]
        query = query.order_by(column.desc() if filters.order_by == OrderBy.desc else column.asc())
    else:
        query = query.order_by(
            Printer.created_at.desc() if filters.order_by == OrderBy.desc else Printer.created_at.asc()
        )

    query = (
        query.options(
            selectinload(Printer.supply),
            selectinload(Printer.status),
            selectinload(Printer.department),
        )
        .limit(filters.limit)
        .offset(filters.offset)
    )

    printers = (await session.scalars(query)).all()

    printers_public = [
        FullPrinterPublicSchema(
            id=printer.id,
            supply_id=SupplyIdSchema(id=printer.supply.id, name=printer.supply.name),  # type: ignore
            status_id=StatusIdSchema(id=printer.status.id, name=printer.status.status),  # type: ignore
            department_id=DepartmentIdSchema(id=printer.department.id, name=printer.department.name),  # type: ignore
            name=printer.name,
            brand=printer.brand,
            model=printer.model,
            ip=printer.ip,
            description=printer.description,
            forecast=printer.forecast,
            last_refill=printer.last_refill,
            last_maintenance=printer.last_maintenance,
            last_check=printer.last_check,
        )
        for printer in printers
    ]

    return ListFullPrinterPublicSchema(total=total, count=len(printers), printers=printers_public)  # type: ignore


async def get_printer_id(session: AsyncSession, id: int):
    query = (
        select(Printer)
        .where(Printer.id == id)
        .options(
            selectinload(Printer.supply),
            selectinload(Printer.status),
            selectinload(Printer.department),
        )
    )
    printer = await session.scalar(query)

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
        )
    result = FullPrinterPublicSchema(
        supply_id=SupplyIdSchema(id=printer.supply.id, name=printer.supply.name),  # type: ignore
        status_id=StatusIdSchema(id=printer.status.id, name=printer.status.status),  # type: ignore
        department_id=DepartmentIdSchema(id=printer.department.id, name=printer.department.name),  # type: ignore
        id=printer.id,
        name=printer.name,
        brand=printer.brand,
        model=printer.model,
        ip=printer.ip,
        description=printer.description,
        forecast=printer.forecast,
        last_refill=printer.last_refill,
        last_maintenance=printer.last_maintenance,
        last_check=printer.last_check,
    )
    return result


async def delete_printer(session: AsyncSession, id: int):
    printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
        )

    await session.delete(printer)
    await session.commit()


async def update_printer(session: AsyncSession, id: int, printer: FullPrinterUpdateSchema):
    existing_printer = await session.scalar(select(Printer).where(Printer.id == id))

    if not existing_printer:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="printer not found",
        )

    if printer.ip and existing_printer.ip != printer.ip:
        existing_ip_printer = await session.scalar(select(Printer).where(Printer.ip == printer.ip))

        if existing_ip_printer:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="The IP is already in use",
            )

    # an update model (FullPrinterUpdateSchema) is used to send only the part that needs to be modified

    existing_printer.name = printer.name if printer.name else existing_printer.name
    existing_printer.model = printer.model if printer.model else existing_printer.model
    existing_printer.ip = printer.ip if printer.ip else existing_printer.ip
    existing_printer.brand = printer.brand if printer.brand else existing_printer.brand
    existing_printer.department_id = printer.department_id if printer.department_id else existing_printer.department_id
    existing_printer.description = printer.description if printer.description else existing_printer.description
    existing_printer.forecast = printer.forecast if printer.forecast else existing_printer.forecast
    existing_printer.last_refill = printer.last_refill if printer.last_refill else existing_printer.last_refill
    existing_printer.last_maintenance = (
        printer.last_maintenance if printer.last_maintenance else existing_printer.last_maintenance
    )
    existing_printer.last_check = printer.last_check if printer.last_check else existing_printer.last_check
    existing_printer.status_id = printer.status_id if printer.status_id else existing_printer.status_id
    existing_printer.supply_id = printer.supply_id if printer.supply_id else existing_printer.supply_id

    await session.commit()
    await session.refresh(existing_printer)
    result_schema = FullPrinterSchemaDB.model_validate(existing_printer)

    return result_schema
