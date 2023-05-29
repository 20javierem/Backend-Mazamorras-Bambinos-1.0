from sqlmodel import select

from config.db import Session
from models.product_day_sale import ProductDaySale


async def get(id: int):
    with Session() as session:
        return session.get(ProductDaySale, id)


async def save(productDaySale: ProductDaySale):
    with Session() as session:
        session.add(productDaySale)
        session.commit()
        session.refresh(productDaySale)
        return productDaySale

async def delete(productDaySale: ProductDaySale):
    with Session() as session:
        session.delete(productDaySale)
        session.commit()


async def all():
    with Session() as session:
        statement = select(ProductDaySale)
        return session.exec(statement).all()