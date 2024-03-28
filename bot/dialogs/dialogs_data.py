from models.cards import CardData
from models.product import Product
from services.http_services import get_user_products


async def get_card_data(product_id: int) -> CardData:
    result = data.get(product_id)
    return CardData(**result)


async def get_products_ids(user_id: int) -> tuple:
    products_categories = await get_user_products(user_id)
    return tuple(category.keys() for category in products_categories)


async def get_products(user_id) -> tuple[dict[int, Product], dict[int, Product], dict[int, Product]]:
    products = await get_user_products(user_id)
    return (
        {item.wb_id: item for item in products},
        {item.wb_id: item for item in products if item.current_price < item.previous_price},
        {item.wb_id: item for item in products if item.current_price > item.previous_price},
    )


data = {62604402:
    {
        "wb_id": 62604402,
        "name": "Сварочный полуавтомат инверторный Smart Mig-175S",
        "group_id": 0,
        "user_id": 440206915,
        "current_price": 7200,
        "previous_price": 7200,
        "url": "https://www.wildberries.ru/catalog/62604402/detail.aspx",
        "image_url": "https://basket-04.wb.ru/vol626/part62604/62604402/images/big/1.webp"
    },
    170430455: {
        "wb_id": 170430455,
        "name": "NOTE 30 Pro 8+256GB",
        "group_id": 0,
        "user_id": 440206915,
        "current_price": 19697,
        "previous_price": 19697,
        "url": "https://www.wildberries.ru/catalog/170430455/detail.aspx",
        "image_url": "https://basket-12.wb.ru/vol1704/part170430/170430455/images/big/1.webp"
    },
    168217638: {
        "wb_id": 168217638,
        "name": "Электрический чайник",
        "group_id": None,
        "user_id": 440206915,
        "current_price": 1007,
        "previous_price": 1007,
        "url": "https://www.wildberries.ru/catalog/168217638/detail.aspx",
        "image_url": "https://basket-12.wb.ru/vol1682/part168217/168217638/images/big/1.webp"
    },
    81796140: {
        "wb_id": 81796140,
        "name": "Органайзер для хранения вещей",
        "group_id": None,
        "user_id": 440206915,
        "current_price": 415,
        "previous_price": 415,
        "url": "https://www.wildberries.ru/catalog/81796140/detail.aspx",
        "image_url": "https://basket-05.wb.ru/vol817/part81796/81796140/images/big/1.webp"
    }
}
