from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import tables, database
from models.users import User


class UsersService:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session: Session = session

    async def _get(self, user_id: int) -> tables.User:
        q = select(tables.User).where(tables.User.id == user_id)
        res = await self.session.execute(q)
        user = res.scalar()

        return user

    async def get(self, user_id: int) -> tables.User:
        user = await self._get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def get_list(
            self,
            is_active: Optional[bool] = None,
    ) -> List[tables.User]:

        q = select(tables.User)
        if is_active is not None:
            q = q.where(tables.User.is_active == is_active)

        res = await self.session.execute(q)
        return res.scalars().all()

    async def create(self, user_data: User) -> tables.User:
        user = await self._get(user_data.id)

        if user:
            return user
        else:
            user = tables.User(**user_data.dict())
            self.session.add(user)
            await self.session.commit()
            return user

    async def update(self, user_id: int, user_data: User) -> tables.User:
        user = await self._get(user_id)
        if user:
            for field, value in user_data:
                setattr(user, field, value)

            await self.session.commit()
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def delete(self, user_id: int):
        user = await self._get(user_id)
        await self.session.delete(user)
        await self.session.commit()
