from typing import List, Optional
from fastapi import APIRouter, Depends, Response

from models import Product
from services import ProductsService

router = APIRouter(
    prefix='/products',
)


@router.get('/', response_model=List[Product])
async def get_user_products(
        user_id: int,
        service: ProductsService = Depends()
):
    return await service.get_user_products(user_id=user_id)
