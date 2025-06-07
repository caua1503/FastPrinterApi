from fastapi import APIRouter
from .printers import printer_router

api_router = APIRouter(prefix="/api", tags=["api"])
api_router.include_router(printer_router)

@api_router.get('/')
async def main():
    return {"message": "Funcionando, abra o /docs"}