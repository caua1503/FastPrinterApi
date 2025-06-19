from fastapi import FastAPI
from app.routers import api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def hello():
    return {"message": "Hello World"}
