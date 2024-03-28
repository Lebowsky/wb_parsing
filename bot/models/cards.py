from pydantic import BaseModel


class CardData(BaseModel):
    name: str
    current_price: float = 0.0
    previous_price: float = 0.0
    url: str = ''
    image_url: str = ''
