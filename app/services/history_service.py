from typing import Optional, List, Dict, Any
from models.history_model import (HistoryRecargaSchema, HistoryRecargaSchemaDB, 
                            HistoryManutencaoSchema, HistoryManutencaoSchemaDB)
    

"""
ROTA DE HISTORICO DE RECARGA
"""

async def create_history_recharge(history: HistoryRecargaSchema) -> HistoryRecargaSchema:
    ...

async def get_history_recharge(filters: Optional[Dict[str, Any]] = None) -> List[HistoryRecargaSchemaDB]:
    if filters:
        ...
    ...

async def update_history_recharge(id: int, history: HistoryRecargaSchema):
    ...

async def delete_history_recharge(id: int):
    ...

"""
ROTA DE HISTORICO DE MANUTENÇÃO
"""

async def create_history_maintenance(history: HistoryManutencaoSchema) -> HistoryManutencaoSchema:
    ...


async def get_history_maintenance(filters: Optional[Dict[str, Any]] = None) -> List[HistoryManutencaoSchemaDB]:
    if filters:
        ...
    ...

async def update_history_maintenance(id: int, history: HistoryManutencaoSchema):
    ...


async def delete_history_maintenance(id: int):
    ...