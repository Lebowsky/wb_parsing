from typing import Optional, List
from pydantic import BaseModel


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