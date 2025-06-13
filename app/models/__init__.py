from .history_model import (
    HistoryManutencaoSchema,
    HistoryManutencaoSchemaDB,
    HistoryRecargaSchema,
    HistoryRecargaSchemaDB,
)
from .printer_model import FullPrinterSchema, FullPrinterSchemaDB, PrinterSchemaDB

__all__ = [
    "FullPrinterSchema",
    "FullPrinterSchemaDB",
    "PrinterSchemaDB",
    "HistoryRecargaSchema",
    "HistoryRecargaSchemaDB",
    "HistoryManutencaoSchema",
    "HistoryManutencaoSchemaDB",
]
