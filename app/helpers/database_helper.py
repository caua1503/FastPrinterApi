from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import Config

engine = create_async_engine(Config().DATABASE_URL)
engine_logs = create_async_engine(Config().DATABASE_LOGS_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


async def get_session_logs():
    async with AsyncSession(engine_logs) as session_logs:
        yield session_logs
