from typing import List, Set

import sqlalchemy as sa

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self):
        if 'id' in self.__dict__.keys():
            return f'class={type(self).__name__} id={self.id}'
        else:
            return str(self)

    def __str__(self):
        return f'class={type(self).__name__} ' + ''.join(['{}={}'.format(k, v) for k, v in self.__dict__.items()])


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True), server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime(True),
        onupdate=sa.func.now(),
        server_default=sa.func.now()
    )


class User(TimedBaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    products: Mapped[List['Product']] = relationship(lazy='selectin', back_populates='user')


class Product(TimedBaseModel):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(nullable=True)
    current_price: Mapped[float] = mapped_column(nullable=True)
    previous_price: Mapped[float] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)
    prices: Mapped[List['Price']] = relationship(lazy='selectin', back_populates='product')
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates='products')


class Price(TimedBaseModel):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(nullable=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    product: Mapped[Product] = relationship(back_populates='prices')
