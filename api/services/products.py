from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import tables, database
from models.products import Product, UpdateProduct


class ProductsService:
    def __init__(self, session: Session = Depends(database.get_session)):
        self.session: Session = session

    async def _get(self, product_id: int) -> tables.Product:
        q = select(tables.Product).where(tables.Product.id == product_id)
        res = await self.session.execute(q)
        product = res.scalar()

        return product

    async def get(self, product_id: int) -> tables.Product:
        product = await self._get(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return product

    async def get_user_products(self, user_id: int) -> List[tables.Product]:
        q = select(tables.Product).where(tables.Product.user_id == user_id)
        res = await self.session.execute(q)
        products = res.scalars().all()
        return products

    async def create(self, product_data: Product) -> int:
        product_data = product_data.dict()
        price = product_data.pop('price', None)
        product = tables.Product(**product_data)
        self.session.add(product)
        if price:
            product.prices.append(tables.Price(price=price))
            product.current_price = price
            product.previous_price = price
        await self.session.commit()
        return product.id

    async def update(self, product_id: int, product_data: UpdateProduct) -> tables.Product:
        product = await self._get(product_id)
        if product:
            product_data = product_data.model_dump()
            price = product_data.pop('price', None)

            for field, value in product_data.items():
                if value is not None:
                    setattr(product, field, value)

            if price:
                product.prices.append(tables.Price(price=price))
                product.previous_price = product.current_price
                product.current_price = price

            await self.session.commit()
            return product.id
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def update_or_create(self, product_data: UpdateProduct) -> tables.Product:
        q = select(tables.Product).where(
            tables.Product.wb_id == product_data.wb_id,
            tables.Product.user_id == product_data.user_id
        )
        res = await self.session.execute(q)
        product = res.scalar()

        product_data = product_data.model_dump()
        price = product_data.pop('price', None)

        if not product:
            product = tables.Product()
            self.session.add(product)

        for field, value in product_data.items():
            if value is not None:
                setattr(product, field, value)

        if price:
            # product.prices.append(tables.Price(price=price))
            product.previous_price = product.current_price or price
            product.current_price = price

        await self.session.commit()
        return product

    async def delete(self, product_id: int):
        product = await self._get(product_id)
        await self.session.delete(product)
        await self.session.commit()
