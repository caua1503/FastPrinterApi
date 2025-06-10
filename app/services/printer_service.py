from typing import List, Dict, Any, Optional
from models.printer import FullPrinterSchemaDB, FullPrinterSchema, PrinterSchemaDB


database = []

async def create_printer(printer: FullPrinterSchema) -> FullPrinterSchemaDB:
    printer_db = FullPrinterSchemaDB(id=len(database) + 1, 
                                 **printer.model_dump())
    database.append(printer_db)
    return printer_db

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