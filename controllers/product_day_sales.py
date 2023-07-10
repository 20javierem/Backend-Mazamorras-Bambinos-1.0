from sqlmodel import select

from config.moreno import Session
from models.product_day_sale import ProductDaySale


def get(id: int):
    with Session() as session:
        return session.get(ProductDaySale, id)


def all():
    with Session() as session:
        statement = select(ProductDaySale)
        return session.exec(statement).all()
