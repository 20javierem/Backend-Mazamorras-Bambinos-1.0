from sqlmodel import select

from config.moreno import Session
from models.product import Product


def get(id: int):
    with Session() as session:
        return session.get(Product, id)


def all():
    with Session() as session:
        statement = select(Product)
        return session.exec(statement).all()
