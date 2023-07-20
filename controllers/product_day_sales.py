from datetime import datetime
from operator import invert

from sqlalchemy import asc
from sqlmodel import select

from config.moreno import Session
from models import DaySale
from models.product_day_sale import ProductDaySale


def get(id: int):
    with Session() as session:
        return session.get(ProductDaySale, id)


def get_by_product_between(idProduct: int, start: str, end: str):
    try:
        start: datetime = datetime.strptime(start, '%Y-%m-%d')
        end: datetime = datetime.strptime(end, '%Y-%m-%d')
        with Session() as session:
            statement = select(ProductDaySale).join(DaySale).where(
                invert(ProductDaySale.deleted),
                ProductDaySale.product_id == idProduct,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()
