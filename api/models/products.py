from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    wb_id: int
    name: str
    group_id: Optional[int] = None
    user_id: int
    current_price: Optional[float] = None
    previous_price: Optional[float] = None
    url: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateProduct(BaseModel):
    wb_id: int
    user_id: int
    name: Optional[str] = None
    group_id: Optional[int] = None
    price: Optional[float] = None
    url: str
    image_url: Optional[str] = None
