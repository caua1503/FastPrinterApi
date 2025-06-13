from models.input_model import InputSchema, InputSchemaDB, TipoInsumoSchema, TipoInsumoSchemaDB
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from http import HTTPStatus

async def create_input(input: InputSchema, session: Session):

    input_db = InputSchemaDB(
        nome=input.nome,
        descricao=input.descricao,
        tipo_insumo=input.tipo_insumo,
        marca=input.marca,
    )

    session.add(input_db)
    session.commit()
    session.refresh(input_db)
    return input_db

async def get_input(session: Session, limit: int, offset: int):
    inputs = session.scalars(
        select(InputSchemaDB).limit(limit).offset(offset)
    ).all()

    if not inputs:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")
    
    return inputs

async def get_input_id(id: int, session: Session):
    input = session.scalar(
        select(InputSchemaDB).where(InputSchemaDB.id == id)
    )
    if not input:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")
    
    return input

async def update_input(id: int, input: InputSchema, session: Session):
    input_db = session.scalar(
        select(InputSchemaDB).where(InputSchemaDB.id == id)
    )
    if not input_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")
    
    input_db.nome = input.nome
    input_db.descricao = input.descricao
    input_db.tipo_insumo = input.tipo_insumo
    input_db.marca = input.marca

    session.commit()
    session.refresh(input_db)
    return input_db

async def delete_input(id: int, session: Session):
    input_db = session.scalar(
        select(InputSchemaDB).where(InputSchemaDB.id == id)
    )
    if not input_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input not found")
    
    session.delete(input_db)
    session.commit()
    return input_db

async def get_input_type(session: Session):
    input_types = session.scalars(
        select(TipoInsumoSchemaDB)
    ).all()
    if not input_types:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")
    return input_types

async def create_input_type(input_type: TipoInsumoSchema, session: Session):
    input_type_db = TipoInsumoSchemaDB(
        nome=input_type.nome
    )
    session.add(input_type_db)
    session.commit()
    session.refresh(input_type_db)

    return input_type_db

async def update_input_type(id: int, input_type: TipoInsumoSchema, session: Session):
    input_type_db = session.scalar(
        select(TipoInsumoSchemaDB).where(TipoInsumoSchemaDB.id == id)
    )
    if not input_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")
    
    input_type_db.nome = input_type.nome

    session.commit()
    session.refresh(input_type_db)

    return input_type_db

async def delete_input_type(id: int, session: Session):
    input_type_db = session.scalar(
        select(TipoInsumoSchemaDB).where(TipoInsumoSchemaDB.id == id)
    )
    if not input_type_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")
    
    session.delete(input_type_db)
    session.commit()
    return input_type_db

async def get_input_type_id(id: int, session: Session):
    input_type = session.scalar(
        select(TipoInsumoSchemaDB).where(TipoInsumoSchemaDB.id == id)
    )
    
    if not input_type:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Input type not found")
    
    return input_type