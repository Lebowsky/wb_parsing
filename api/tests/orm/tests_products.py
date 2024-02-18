import unittest

from models.users import User
from services.products import ProductsService
from models.products import Product
from services.users import UsersService
from .init_tests import create_sessionmaker


class TestProductService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session_maker = await create_sessionmaker()

    async def test_crud_products(self):
        async with self.session_maker() as session:
            service = ProductsService(session=session)
            user_service = UsersService(session=session)

            await user_service.create(User(id=1, username='name1', is_active=False))
            await user_service.create(User(id=2, username='name2', is_active=False))
            product1 = Product(title='product1', user_id=1)
            product2 = Product(title='product2', user_id=1)

            product1_id = await service.create(product1)
            product2_id = await service.create(product2)

            user = await user_service.get(1)
            self.assertEqual(len(user.products), 2)

            user = await user_service.get(2)
            self.assertEqual(len(user.products), 0)

            await service.update(product2_id, product1)
            product2 = await service.get(product2_id)
            self.assertEqual(product2.title, 'product1')


