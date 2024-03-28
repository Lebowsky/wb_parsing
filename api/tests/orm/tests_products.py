import unittest

from models.products import UpdateProduct
from services import ProductsService

from .init_tests import create_sessionmaker


class TestProductsService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session_maker = await create_sessionmaker()

    async def test_update_or_create_product(self):
        async with self.session_maker() as session:
            service = ProductsService(session=session)

            test_product = UpdateProduct(
                wb_id=1,
                name='product1',
                user_id=123,
                price=100,
                url='http://',
                image_url='http://'
            )

            result = await service.update_or_create(test_product)

            self.assertIsNotNone(result)
            self.assertTrue(await service.get(result.id))

            self.assertEqual(result.previous_price, 100)
            self.assertEqual(result.current_price, 100)

            test_product.price = 200

            result = await service.update_or_create(test_product)
            self.assertEqual(result.previous_price, 100)
            self.assertEqual(result.current_price, 200)
