from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.tables import Base


async def create_sessionmaker():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        # 'sqlite+aiosqlite:///database.db',
        future=True,
        # echo=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_sessionmaker
