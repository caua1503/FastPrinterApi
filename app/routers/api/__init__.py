from fastapi import APIRouter
from .printers_api import printer_router
from .history_api import history_router
from .input_api import input_router
from .status_api import status_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(printer_router)
api_router.include_router(history_router)
api_router.include_router(input_router)
api_router.include_router(status_router)

@api_router.get('/')
async def main():
    return {"message": "Funcionando, abra o /docs"}