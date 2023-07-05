from sqlmodel import select

from config.moreno import Session
from models import PlaceSale
from models.product_place_sale import ProductPlaceSale


async def get(id: int):
    with Session() as session:
        return session.get(ProductPlaceSale, id)


async def get_by_place_sale_and_product_day_sale(place_sale_id: int, product_day_sale: int):
    with Session() as session:
        statement = select(ProductPlaceSale).where(
            ProductPlaceSale.placeSale_id == place_sale_id,
            ProductPlaceSale.productDaySale_id == product_day_sale)
        return session.exec(statement).first()


async def all():
    with Session() as session:
        statement = select(ProductPlaceSale)
        return session.exec(statement).all()
