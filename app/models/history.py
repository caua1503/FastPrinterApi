from pydantic import BaseModel

class HistoryRecargaSchema(BaseModel):
    impressora_id:int
    data:str
    tipo_evento:str
    id_insumo: int
class HistoryManutencaoSchema(BaseModel):
    impressora_id:int
    data:str
    tipo_evento:str
    descricao:str

class HistoryRecargaSchemaDB(HistoryRecargaSchema):
    id:int

class HistoryManutencaoSchemaDB(HistoryManutencaoSchema):
    id:int