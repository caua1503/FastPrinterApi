from fastapi import APIRouter

from .core_api import core_router
from .history_api import history_router
from .printers_api import printer_router
from .status_api import status_router
from .supply_api import supply_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(printer_router)
api_router.include_router(history_router)
api_router.include_router(supply_router)
api_router.include_router(status_router)
api_router.include_router(core_router)


@api_router.get("/")
async def main():
    return {"message": "Funcionando, abra o /docs"}
