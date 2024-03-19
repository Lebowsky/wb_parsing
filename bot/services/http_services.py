from models.product import Product
from wb_services import get_card_details
from api_services import get_product_data


async def get_product_info(product_id: int) -> Product:
    # wb_product = await get_card_details(product_id)
    api_product = await get_product_data(product_id)

    return api_product

