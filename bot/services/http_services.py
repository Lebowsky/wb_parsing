from models.product import Product
from .wb_services import get_card_details
from .api_services import update_product


async def get_product_info(user_id: int, product_id: int) -> Product:
    wb_product = await get_card_details(product_id)
    result = await update_product(wb_product, user_id)

    return result
