from sqlmodel import select

from config.moreno import Session
from models import ProductDaySale
from models.product import Product


async def get(id: int):
    with Session() as session:
        return session.get(Product, id)


async def all():
    with Session() as session:
        statement = select(Product)
        return session.exec(statement).all()


async def hasDependences(product: Product) -> bool:
    with Session() as session:
        statement = select(ProductDaySale).join(Product).where(Product.id == product.id)
        return len(session.exec(statement).unique().all()) > 0
