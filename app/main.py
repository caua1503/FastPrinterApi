import asyncio
import sys

from fastapi import FastAPI

from app.routers import api_router

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def hello():
    return {"message": "Hello World"}
