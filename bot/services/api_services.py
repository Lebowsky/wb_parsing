import logging
from json import JSONDecodeError
from typing import Any, Generator

import httpx
from httpx import HTTPStatusError, RequestError
from urllib.parse import urljoin

from config import settings
from exceptions import ApiRequestError
from models.product import Product

logger = logging.getLogger(__name__)


async def create_product(product: Product):
    data = product.model_dump()
    httpx.post(_get_url(), json=data)


async def get_user_products(user_id: int) -> Generator[Product, Any, None]:
    try:
        result = httpx.get(_get_url(), params={'user_id': user_id}).raise_for_status().json()
        return (Product.model_validate(item) for item in result)
    except (RequestError, HTTPStatusError, JSONDecodeError) as e:
        logger.error(e)
        raise ApiRequestError


def _get_url():
    return urljoin(str(settings.server_url), 'products/')
