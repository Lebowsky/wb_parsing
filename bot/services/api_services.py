import logging
from json import JSONDecodeError

import httpx
from httpx import HTTPError

from config import settings
from models.product import Product

logger = logging.getLogger(__name__)


async def create_product(product: Product):
    data = product.model_dump()
    httpx.post(_get_url(), json=data)


async def get_product_data(user_id, product_id: int) -> Product:
    try:
        result = httpx.get(_get_url(), params={'user_id': user_id, 'product_id': product_id})
        return result.json()
    except (HTTPError, JSONDecodeError) as e:
        logger.error(e)


def _get_url():
    return f'{settings.server_url}/products/'
