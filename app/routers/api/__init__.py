from fastapi import APIRouter

from .auth_api import auth_router
from .core_api import core_router
from .department_api import department_router
from .history_api import history_router
from .printers_api import printer_router
from .status_api import status_router
from .supply_api import supply_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(printer_router, prefix="/printer", tags=["api - printer"])

api_router.include_router(history_router, prefix="/history", tags=["api - history"])

api_router.include_router(supply_router, prefix="/supply", tags=["api - supply"])

api_router.include_router(status_router, prefix="/status", tags=["api - status"])

api_router.include_router(department_router, prefix="/department", tags=["api - department"])

api_router.include_router(core_router, prefix="/core", tags=["api - core"])

api_router.include_router(auth_router, prefix="/auth", tags=["api - auth"])


@api_router.get("/")
async def main():
    return {"message": "Funcionando, abra o /docs"}
