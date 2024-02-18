import unittest
from sqlalchemy import text, select

from .init_tests import create_sessionmaker

from models import User, Product
from services import UsersService, ProductsService


class TestPricesService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session_maker = await create_sessionmaker()

    async def test_crud_prices(self):
        async with self.session_maker() as session:
            user_service = UsersService(session)
            await user_service.create(User(id=1, username='name1'))
            await user_service.create(User(id=2, username='name2', is_active=False))
            await user_service.create(User(id=3, username='name3', is_active=True))

            product_service = ProductsService(session)
            product_id = await product_service.create(Product(title='product1', user_id=1, price=100))
            await product_service.create(Product(title='product2', user_id=1, price=200))
            await product_service.create(Product(title='product3', user_id=2, price=300))

            self.assertEqual(len((await session.scalars(text('SELECT * FROM users'))).all()), 3)
            self.assertEqual(len((await session.scalars(text('SELECT * FROM products'))).all()), 3)

            user1 = await user_service.get(1)
            self.assertEqual(user1.username, 'name1')
            self.assertEqual(len(user1.products), 2)
            self.assertEqual(len(user1.products[0].prices), 1)
            self.assertEqual(user1.products[0].prices[0].price, 100)

            await product_service.update(product_id, Product(title='product1', user_id=1, price=200))

            user1 = await user_service.get(1)
            self.assertEqual(len(user1.products), 2)
            self.assertEqual(len(user1.products[0].prices), 2)
            self.assertEqual(user1.products[0].prices[1].price, 200)

            self.assertEqual(len(await product_service.get_user_products(1)), 2)
            self.assertEqual(len(await product_service.get_user_products(2)), 1)
            self.assertEqual(len(await product_service.get_user_products(3)), 0)

            print((await product_service.get_user_products(1)))



