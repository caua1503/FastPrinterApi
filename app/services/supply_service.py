from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.printer_model import Printer
from app.models.supply_model import Supply, SupplyType
from app.schemas.filter_schema import FilterBase
from app.schemas.supply_schema import SupplySchema, SupplyTypeSchema


async def create_supply(supply: SupplySchema, session: AsyncSession):
    supply_db = Supply(
        name=supply.name,
        description=supply.description,
        supply_type_id=supply.supply_type_id,
        brand=supply.brand,
    )

    session.add(supply_db)
    await session.commit()
    await session.refresh(supply_db)
    return supply_db


async def get_supply(session: AsyncSession, filters: FilterBase):
    supplys = (await session.scalars(select(Supply).limit(filters.limit).offset(filters.offset))).all()

    if not supplys:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply not found")

    return supplys


async def get_supply_id(id: int, session: AsyncSession):
    supply = await session.scalar(select(Supply).where(Supply.id == id))

    if not supply:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply not found")

    return supply


async def update_supply(id: int, supply: SupplySchema, session: AsyncSession):
    supply_db = await session.scalar(select(Supply).where(Supply.id == id))

    if not supply_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply not found")

    supply_db.name = supply.name
    supply_db.description = supply.description
    supply_db.supply_type_id = supply.supply_type_id
    supply_db.brand = supply.brand

    await session.commit()
    await session.refresh(supply_db)
    return supply_db


async def delete_supply(id: int, session: AsyncSession):
    supply_db = await session.scalar(select(Supply).where(Supply.id == id))
    printers = await session.scalars(select(Printer).where(Printer.supply_id == id))

    if not supply_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply not found")

    if printers:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Supply has printers")

    await session.delete(supply_db)
    await session.commit()
    return supply_db


async def get_supply_type(session: AsyncSession):
    supply_types = (await session.scalars(select(SupplyType))).all()

    if not supply_types:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply type not found")

    return supply_types


async def create_supply_type(supply_type: SupplyTypeSchema, session: AsyncSession):
    supply_type_db = SupplyType(name=supply_type.name)
    session.add(supply_type_db)
    await session.commit()
    await session.refresh(supply_type_db)

    return supply_type_db


async def update_supply_type(id: int, supply_type: SupplyTypeSchema, session: AsyncSession):
    supply_type_db = await session.scalar(select(SupplyType).where(SupplyType.id == id))
    if not supply_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply type not found")

    supply_type_db.nome = supply_type.nome

    await session.commit()
    await session.refresh(supply_type_db)

    return supply_type_db


async def delete_supply_type(id: int, session: AsyncSession):
    supply_type_db = await session.scalar(select(SupplyType).where(SupplyType.id == id))
    supplys = await session.scalars(select(Supply).where(Supply.supply_type_id == id))

    if not supply_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply type not found")

    if supplys:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Supply type has supplies")

    await session.delete(supply_type_db)
    await session.commit()
    return supply_type_db


async def get_supply_type_id(id: int, session: AsyncSession):
    supply_type = await session.scalar(select(SupplyType).where(SupplyType.id == id))

    if not supply_type:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="supply type not found")

    return supply_type
