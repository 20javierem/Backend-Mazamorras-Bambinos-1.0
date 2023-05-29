from sqlmodel import select

from config.db import Session
from models.product_place_sale import ProductPlaceSale


async def get(id: int):
    with Session() as session:
        return session.get(ProductPlaceSale, id)


async def save(productPlaceSale: ProductPlaceSale):
    with Session() as session:
        session.add(productPlaceSale)
        session.commit()
        session.refresh(productPlaceSale)
        return productPlaceSale


async def delete(productPlaceSale: ProductPlaceSale):
    with Session() as session:
        session.delete(productPlaceSale)
        session.commit()


async def all():
    with Session() as session:
        statement = select(ProductPlaceSale)
        return session.exec(statement).all()
