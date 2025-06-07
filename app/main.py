from fastapi import FastAPI
import asyncio
from routers import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
async def hello():
    return {"message": "Hello World"}