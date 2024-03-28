from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine

from fastapi import Depends

from db import tables, database
from db.tables import Base
from config import settings


class PragmaService:
    # def __init__(self, session: Session = Depends(database.get_session)):
    #     self.session: Session = session

    async def recreate_tables(self):
        engine = create_async_engine(
            settings.db_url,
            future=True,
        )

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
