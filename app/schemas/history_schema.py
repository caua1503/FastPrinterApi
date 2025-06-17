from datetime import date
from typing import Optional

from pydantic import BaseModel


class HistoryRecargaSchema(BaseModel):
    impressora_id: int
    data: date
    tipo_evento: str
    id_insumo: int
    descricao: Optional[str]


class HistoryManutencaoSchema(BaseModel):
    impressora_id: int
    data: date
    tipo_evento: str
    descricao: Optional[str]


class HistoryLixeiraSchema(BaseModel):
    impressora_id: int
    data: date
    descricao: Optional[str]


class HistoryAlertaSchema(BaseModel):
    impressora_id: int
    data: date
    tipo_alerta: str
    descricao: Optional[str]


class HistoryRecargaSchemaDB(HistoryRecargaSchema):
    id: int


class HistoryManutencaoSchemaDB(HistoryManutencaoSchema):
    id: int


class HistoryLixeiraSchemaDB(HistoryLixeiraSchema):
    id: int


class HistoryAlertaSchemaDB(HistoryAlertaSchema):
    id: int
