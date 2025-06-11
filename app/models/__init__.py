from .printer_model import FullPrinterSchema, FullPrinterSchemaDB, PrinterSchemaDB

from .history_model import (HistoryRecargaSchema, HistoryRecargaSchemaDB, 
                      HistoryManutencaoSchema, HistoryManutencaoSchemaDB)

__all__ = ["FullPrinterSchema", "FullPrinterSchemaDB", "PrinterSchemaDB",
           "HistoryRecargaSchema", "HistoryRecargaSchemaDB", "HistoryManutencaoSchema", "HistoryManutencaoSchemaDB"]