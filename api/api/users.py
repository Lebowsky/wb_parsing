from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from models.users import User, ListUser
from services.users import UsersService

router = APIRouter(
    prefix='/users',
)


@router.get('/{user_id}', response_model=User)
async def get_user(
        user_id: int,
        service: UsersService = Depends()
):
    return await service.get(user_id)


@router.get('/', response_model=List[ListUser])
async def get_users(
        is_active: Optional[bool] = None,
        service: UsersService = Depends()
):
    return await service.get_list(
        is_active=is_active,
    )


@router.post('/', response_model=User)
async def create_user(
        user_data: User,
        service: UsersService = Depends()
):
    return await service.create(user_data)


@router.put('/', response_model=User)
async def update_user(
        user_id: int,
        user_data: User,
        service: UsersService = Depends()
):
    return await service.update(user_id, user_data)


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        service: UsersService = Depends()
):
    await service.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
