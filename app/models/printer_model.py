from pydantic import BaseModel
from datetime import date
from typing import Optional

class PrinterSchema(BaseModel):
    name: str 
    model: str
    ip: str
    marca: str

class PrinterSchemaDB(PrinterSchema):
    id: int

class FullPrinterSchema(BaseModel):
    id_insumo: int
    id_status: int
    name: str 
    marca: str
    model: str
    ip: str
    setor: str
    descricao: Optional[str] = None
    previsao: Optional[date] = None
    ultima_recarga: Optional[date] = None
    ultima_manutencao: Optional[date] = None
    ultima_verificacao: Optional[date] = None

class FullPrinterSchemaDB(FullPrinterSchema):
    id: int
