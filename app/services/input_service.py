from http import HTTPStatus

from fastapi import HTTPException
from models.model_db import Insumo, Tipo_Insumo
from schemas.input_schema import InputSchema, TipoInsumoSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_input(input: InputSchema, session: AsyncSession):
    input_db = Insumo(
        nome=input.nome,
        descricao=input.descricao,
        tipo_insumo=input.tipo_insumo,
        marca=input.marca,
    )

    session.add(input_db)
    await session.commit()
    await session.refresh(input_db)
    return input_db


async def get_input(session: AsyncSession, limit: int, offset: int):
    inputs = (await session.scalars(select(Insumo).limit(limit).offset(offset))).all()

    if not inputs:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")

    return inputs


async def get_input_id(id: int, session: AsyncSession):
    input = await session.scalar(select(Insumo).where(Insumo.id == id))

    if not input:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")

    return input


async def update_input(id: int, input: InputSchema, session: AsyncSession):
    input_db = await session.scalar(select(Insumo).where(Insumo.id == id))

    if not input_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")

    input_db.nome = input.nome
    input_db.descricao = input.descricao
    input_db.tipo_insumo = input.tipo_insumo
    input_db.marca = input.marca

    await session.commit()
    await session.refresh(input_db)
    return input_db


async def delete_input(id: int, session: AsyncSession):
    input_db = await session.scalar(select(Insumo).where(Insumo.id == id))

    if not input_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")

    await session.delete(input_db)
    await session.commit()
    return input_db


async def get_input_type(session: AsyncSession):
    input_types = (await session.scalars(select(Tipo_Insumo))).all()

    if not input_types:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")

    return input_types


async def create_input_type(input_type: TipoInsumoSchema, session: AsyncSession):
    input_type_db = Tipo_Insumo(nome=input_type.nome)
    session.add(input_type_db)
    await session.commit()
    await session.refresh(input_type_db)

    return input_type_db


async def update_input_type(id: int, input_type: TipoInsumoSchema, session: AsyncSession):
    input_type_db = await session.scalar(select(Tipo_Insumo).where(Tipo_Insumo.id == id))
    if not input_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")

    input_type_db.nome = input_type.nome

    await session.commit()
    await session.refresh(input_type_db)

    return input_type_db


async def delete_input_type(id: int, session: AsyncSession):
    input_type_db = await session.scalar(select(Tipo_Insumo).where(Tipo_Insumo.id == id))

    if not input_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")

    await session.delete(input_type_db)
    await session.commit()
    return input_type_db


async def get_input_type_id(id: int, session: AsyncSession):
    input_type = await session.scalar(select(Tipo_Insumo).where(Tipo_Insumo.id == id))

    if not input_type:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")

    return input_type
