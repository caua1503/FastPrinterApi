from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import Config

engine = create_async_engine(Config().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
