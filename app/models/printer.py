from typing import List, Dict
from pydantic import BaseModel

class PrinterSchema(BaseModel):
    name: str 
    model: str
    ip: str


class FullPrinterSchema(PrinterSchema):
    status: str = None
    setor: str = None
    descricao: str = None
    previsao: str = None
    ultima_recarga: str  = None
    ultima_manutencao: str = None
    ultima_verificacao: str = None

class PrinterSchemaDB(FullPrinterSchema):
    id: int