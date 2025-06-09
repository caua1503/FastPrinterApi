from typing import List, Dict
from pydantic import BaseModel

class PrinterSchema(BaseModel):
    name: str 
    model: str
    ip: str
    marca: str

class PrinterSchemaDB(PrinterSchema):
    id: int

class FullPrinterSchema(BaseModel):
    name: str 
    marca: str = None
    model: str
    ip: str
    status: str = None
    setor: str = None
    descricao: str = None
    previsao: str = None
    insumo: str = None
    ultima_recarga: str  = None
    ultima_manutencao: str = None
    ultima_verificacao: str = None

class FullPrinterSchemaDB(FullPrinterSchema):
    id: int
