from dataclasses import dataclass

import requests
import logging

import exceptions

logger = logging.getLogger(__name__)

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.wildberries.ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


@dataclass
class ProductModel:
    id: int
    name: str
    url: str
    image_url: str
    price: float


def get_card_details(item_id: str, **kwargs) -> ProductModel:
    params = {
        'nm': item_id,
        'curr': 'rub',
    }

    try:
        response = requests.get('https://card.wb.ru/cards/v1/detail', params=params, headers=headers)
        products = response.json()['data']['products']
    except (KeyError, requests.exceptions.JSONDecodeError, requests.exceptions.HTTPError) as e:
        logger.error(str(e))
        raise exceptions.ApiRequestError

    if products:
        return ProductModel(
            id=_parse_id(products[0]),
            name=_parse_name(products[0]),
            url=_get_product_url(products[0]),
            image_url=_get_image_url(products[0]),
            price=_parse_price(products[0])
        )
    else:
        raise exceptions.ProductNotFoundError


def _parse_id(product) -> int:
    return product['id']


def _parse_name(product) -> str:
    return product['name']


def _get_product_url(product) -> str:
    return 'https://www.wildberries.ru/catalog/{id}/detail.aspx'.format(**product)


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


if __name__ == '__main__':
    # print(ImgUrlGenerator(76280452).url())
    print(get_card_details('76280451'))
