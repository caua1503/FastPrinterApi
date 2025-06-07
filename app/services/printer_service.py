from typing import List, Dict, Any
from models import PrinterSchema, FullPrinterSchema, PrinterSchemaDB

database = []

async def create_printer(printer: PrinterSchema) -> PrinterSchemaDB:
    printer_db = PrinterSchemaDB(id=len(database) + 1, 
                                 **printer.model_dump())
    database.append(printer_db)
    return printer_db

async def delete_printer(id: int):
    ...

async def update_printer(id: int, printer: FullPrinterSchema):
    ...

async def get_printer(id: int ) -> List[FullPrinterSchema]:
    ...
    
async def get_printers(name: str = None, 
                      model: str = None, 
                      ip: str = None):
    #filters
    if name is None and model is None and ip is None:
        test_list = []
        for printer in database:
            id_printer = printer.id
            test = {id_printer: printer}
            test_list.append(test)
        return test_list #temporario
    
    if name is not None:
        return await get_printers_by_name(name)
    
    if model is not None:
        return await get_printers_by_model(model)
    
    if ip is not None:
        return await get_printers_by_ip(ip)

async def get_printers_by_name(name: str) -> List[Dict[str, FullPrinterSchema]]:
    ...

async def get_printers_by_model(model: str) -> List[Dict[str, FullPrinterSchema]]:
    ...

async def get_printers_by_ip(ip: str) -> List[Dict[str, FullPrinterSchema]]:
    ...