from typing import Optional

from pydantic import BaseModel, validator


class User(BaseModel):
    id: int
    username: str
    is_active: Optional[bool] = False

    class Config:
        from_attributes = True


class ListUser(User):
    id: int
    username: Optional[str] = ''
    is_active: Optional[bool] = None
