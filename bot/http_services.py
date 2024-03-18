import logging

import httpx
from config import settings
from models import Product


async def create_product(product: Product):
    data = product.model_dump()
    logging.debug(data)
    logging.debug(type(data))
    httpx.post(_get_url(), json=data)


def _get_url():
    return f'{settings.server_url}/products/'
