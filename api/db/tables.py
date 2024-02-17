from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


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

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=False)
    username = sa.Column(sa.String(50), nullable=True)
    is_active = sa.Column(sa.Boolean)
