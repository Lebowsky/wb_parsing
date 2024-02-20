from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    title: str
    group_id: Optional[int] = None
    user_id: int
    current_price: Optional[float] = None
    previous_price: Optional[float] = None


    class Config:
        from_attributes = True


class UpdateProduct(BaseModel):
    title: Optional[str] = None
    group_id: Optional[int] = None
    price: Optional[float] = None
