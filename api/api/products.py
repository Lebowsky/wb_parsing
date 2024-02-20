from typing import List, Optional
from fastapi import APIRouter, Depends, Response

from models import Product
from models.products import UpdateProduct
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


@router.post('/')
async def create_product(
        product_data: Product,
        service: ProductsService = Depends()
):
    return await service.create(product_data)


@router.put('/')
async def update_product(
        product_id: int,
        product_data: UpdateProduct,
        service: ProductsService = Depends()
):
    return await service.update(product_id, product_data)
