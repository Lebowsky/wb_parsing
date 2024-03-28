from models.product import Product
from .wb_services import get_card_details
from .api_services import update_product, get_products_by_user_id


async def get_product_info(user_id: int, product_id: int) -> Product:
    wb_product = await get_card_details(product_id)
    result = await update_product(wb_product, user_id)

    return result


async def get_user_products(user_id: int) -> list[Product]:
    return await get_products_by_user_id(user_id)
