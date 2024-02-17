import asyncio
import unittest

from services.users import UsersService
from models.users import User
from db import tables
from .init_tests import create_sessionmaker

from db import tables


class TestUsersORM(unittest.IsolatedAsyncioTestCase):
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def asyncSetUp(self) -> None:
        self.session_maker = await create_sessionmaker()

    async def test_crud_users(self):
        async with self.session_maker() as session:
            service = UsersService(session=session)
            test_data =[
                User(id=0, username='name1'),
                User(id=1, username='name2', is_active=False),
                User(id=2, username='name3', is_active=True)
            ]
            for _id, item in enumerate(test_data):
                user = await service.create(item)
                self.assertEqual(user.id, _id)
                
            self.assertEqual(len(await service.get_list()), 3)
            self.assertEqual(len(await service.get_list(is_active=True)), 1)
            self.assertEqual(len(await service.get_list(is_active=False)), 2)
            await service.delete(1)
            self.assertEqual(len(await service.get_list()), 2)

            update_user = User(id=0, username='new_name', is_active=True)
            user = await service.update(0, update_user)
            self.assertIsInstance(user, tables.User)
            
            user = await service.get(0)
            self.assertEqual(user.username, 'new_name')
            
