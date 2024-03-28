import logging
from json import JSONDecodeError

import httpx
from httpx import HTTPStatusError, RequestError
from urllib.parse import urljoin

from config import settings
from exceptions import ApiRequestError
from models.product import Product, WbProduct, UpdateProduct

logger = logging.getLogger(__name__)


async def update_product(product: WbProduct, user_id: int) -> Product:
    try:
        result = httpx.post(
            _get_url(),
            json=UpdateProduct(
                **product.model_dump(),
                wb_id=product.id,
                user_id=user_id
            ).model_dump()
        ).raise_for_status().json()
        return Product(**result)
    except (RequestError, HTTPStatusError, JSONDecodeError) as e:
        logger.error(e)
        raise ApiRequestError


def _get_url():
    return urljoin(str(settings.server_url), 'products/')
