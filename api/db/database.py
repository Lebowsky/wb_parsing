from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import settings
from db.tables import Base


async def get_async_sessionmaker() -> sessionmaker:
    engine = create_async_engine(
        settings.db_url,
        future=True,
    )

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )

    return async_sessionmaker


async def get_session():
    async_sessionmaker: sessionmaker = await get_async_sessionmaker()

    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()
