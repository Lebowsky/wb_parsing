from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    title: str
    group_id: Optional[int] = None
    user_id: int
    price: Optional[float] = None
