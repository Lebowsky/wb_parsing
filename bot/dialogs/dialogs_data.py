from models.cards import CardData
from models.product import Product
from services.http_services import get_user_products, get_product_info


async def get_card_data(user_id: int, product_id: int) -> CardData:
    result = await get_product_info(user_id, product_id)
    return CardData(**result.model_dump())


async def get_products_ids(user_id: int) -> tuple:
    products_categories = await get_products(user_id)
    return tuple(category.keys() for category in products_categories)


async def get_products(user_id) -> tuple[dict[int, Product], dict[int, Product], dict[int, Product]]:
    products = await get_user_products(user_id)
    return (
        {item.wb_id: item for item in products},
        {item.wb_id: item for item in products if item.current_price < item.previous_price},
        {item.wb_id: item for item in products if item.current_price > item.previous_price},
    )
