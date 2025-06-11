from http import HTTPStatus
from sqlalchemy import select
from config import DATABASE_URL
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.model_db import Impressora
from helpers.db_helper import get_engine
from typing import List, Dict, Any, Optional
from models.printer_model import FullPrinterSchemaDB, FullPrinterSchema


async def create_printer(printer: FullPrinterSchema) -> FullPrinterSchemaDB:

    engine = await get_engine()

    with Session(engine) as session:
        # Verificar se IP já existe
        existing_printer = session.scalar(
            select(Impressora).where(Impressora.ip == printer.ip)
        )
        
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
            ultima_verificacao=printer.ultima_verificacao
        )
        
        session.add(db_printer)
        session.commit()
        session.refresh(db_printer)

        return db_printer

async def delete_printer(id: int):
    ...

async def update_printer(id: int, printer: FullPrinterSchema):
    ...

async def get_printer(id: int ) -> List[FullPrinterSchema]:
    ...
    
async def get_printers(filters: Optional[Dict[str, Any]] = None) -> List[FullPrinterSchema]:
    if filters:
        ...
    
    return database