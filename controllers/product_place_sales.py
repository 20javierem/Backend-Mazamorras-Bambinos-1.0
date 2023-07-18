from datetime import datetime

from sqlalchemy import asc
from sqlmodel import select

from config.moreno import Session
from models import DaySale, ProductDaySale, PlaceSale
from models.product_place_sale import ProductPlaceSale


def get(id: int):
    with Session() as session:
        return session.get(ProductPlaceSale, id)


def get_by_place_sale_and_product_day_sale(place_sale_id: int, product_day_sale: int):
    with Session() as session:
        statement = select(ProductPlaceSale).where(
            ProductPlaceSale.placeSale_id == place_sale_id,
            ProductPlaceSale.productDaySale_id == product_day_sale)
        return session.exec(statement).first()



def get_by_product_and_place_and_worker(idProduct: int, idWorker: int, idPlace: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(ProductPlaceSale).join(DaySale).join(PlaceSale).join(ProductDaySale).where(
                not ProductPlaceSale.deleted,
                ProductDaySale.product_id == idProduct,
                PlaceSale.place_id == idPlace,
                PlaceSale.worker_id == idWorker,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_by_product_and_worker(idProduct: int, idWorker: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(ProductPlaceSale).join(DaySale).join(PlaceSale).join(ProductDaySale).where(
                not ProductPlaceSale.deleted,
                ProductDaySale.product_id == idProduct,
                PlaceSale.worker_id == idWorker,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_by_product_and_place(idProduct: int, idPlace: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(ProductPlaceSale).join(DaySale).join(PlaceSale).join(ProductDaySale).where(
                not ProductPlaceSale.deleted,
                ProductDaySale.product_id == idProduct,
                PlaceSale.place_id == idPlace,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_by_product(idProduct: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(ProductPlaceSale).join(DaySale).join(PlaceSale).join(ProductDaySale).where(
                not ProductPlaceSale.deleted,
                ProductDaySale.product_id == idProduct,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()
