from exceptions import ProductNotFoundError
from models.product import Product
from .wb_services import get_card_details
from .api_services import get_user_products


async def get_product_info(user_id: int, product_id: int) -> Product:
    # user_products = await get_user_products(user_id)

    # try:
        # db_product = next(product for product in user_products if product.id == product_id)
    # except StopIteration:
    #     raise ProductNotFoundError

    wb_product = await get_card_details(product_id)

    return Product(**wb_product.model_dump(), user_id=user_id)

