import httpx
import logging

from json import JSONDecodeError
from httpx import HTTPError

import exceptions
from constants import WB_HEADERS, WB_API_URL_GET_CARD, WB_URL_DETAIL
from models.product import WbProduct

logger = logging.getLogger(__name__)


async def get_card_details(item_id: int) -> WbProduct:
    params = {
        'nm': item_id,
        'curr': 'rub',
    }

    try:
        response = httpx.get(WB_API_URL_GET_CARD, params=params, headers=WB_HEADERS).raise_for_status().json()
        products = response['data']['products']
    except (KeyError, JSONDecodeError, HTTPError) as e:
        logger.error(str(e))
        raise exceptions.ApiRequestError

    if products:
        return WbProduct(
            id=_parse_id(products[0]),
            name=_parse_name(products[0]),
            price=_parse_price(products[0]),
            url=_get_product_url(products[0]),
            image_url=_get_image_url(products[0]),
        )
    else:
        logger.debug('Not found product with id=%s', item_id)
        raise exceptions.ProductNotFoundError


def _parse_id(product) -> int:
    return product['id']


def _parse_name(product) -> str:
    return product['name']


def _get_product_url(product) -> str:
    return WB_URL_DETAIL.format(**product)


def _get_image_url(product) -> str:
    return ImgUrlGenerator(product['id']).url()


def _parse_price(product) -> float:
    return product['salePriceU'] / 100


class ImgUrlGenerator:
    def __init__(self, nm_id, photo_size='big', photo_number=1, format_='webp'):
        self.nm_id = nm_id
        self.size = photo_size
        self.number = photo_number
        self.format_ = format_  # 'jpg'

    def get_host(self, vol):
        url_parts = [
            {'range': [0, 143], 'url': "//basket-01.wb.ru"},
            {'range': [144, 287], 'url': "//basket-02.wb.ru"},
            {'range': [288, 431], 'url': "//basket-03.wb.ru"},
            {'range': [432, 719], 'url': "//basket-04.wb.ru"},
            {'range': [720, 1007], 'url': "//basket-05.wb.ru"},
            {'range': [1008, 1061], 'url': "//basket-06.wb.ru"},
            {'range': [1062, 1115], 'url': "//basket-07.wb.ru"},
            {'range': [1116, 1169], 'url': "//basket-08.wb.ru"},
            {'range': [1170, 1313], 'url': "//basket-09.wb.ru"},
            {'range': [1314, 1601], 'url': "//basket-10.wb.ru"},
            {'range': [1602, 1655], 'url': "//basket-11.wb.ru"},
            {'range': [1656, 1919], 'url': "//basket-12.wb.ru"},
            {'range': [1920, 2045], 'url': "//basket-13.wb.ru"},
            {'range': [2046, 999999999], 'url': "//basket-14.wb.ru"},
        ]

        url = [part['url'] for part in url_parts if (part['range'][0] <= vol <= part['range'][1])][0]

        return url

    def url(self):
        vol = int(self.nm_id // 1e5)
        part = int(self.nm_id // 1e3)

        return f'https:{self.get_host(vol)}/vol{vol}/part{part}/{self.nm_id}/images/{self.size}/{self.number}.{self.format_}'

