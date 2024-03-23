from typing import Optional
from pydantic import BaseModel


class WbProduct(BaseModel):
    id: int
    name: str
    price: float
    url: str
    image_url: Optional[str] = None


class Product(BaseModel):
    name: str
    group_id: Optional[int] = None
    user_id: int
    current_price: Optional[float] = None
    previous_price: Optional[float] = None
    url: str
    image_url: Optional[str] = None
