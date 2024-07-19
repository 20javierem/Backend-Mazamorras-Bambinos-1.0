from datetime import datetime
from operator import invert

from sqlalchemy import asc
from sqlmodel import select

from config.moreno import Session
from models import Worker
from models import Place
from models.day_sale import DaySale
from models.place_sale import PlaceSale


def get(id: int):
    with Session() as session:
        return session.get(PlaceSale, id)


def get_by_day_sale_and_worker(idDaySale: int, idWorker: int):
    with Session() as session:
        statement = select(PlaceSale).join(DaySale).join(Worker).where(
            invert(PlaceSale.deleted),
            Worker.id == idWorker,
            DaySale.id == idDaySale
        )
        return session.exec(statement).first()


def get_by_day_sale_and_place(idDaySale: int, idPlace: int):
    with Session() as session:
        statement = select(PlaceSale).join(DaySale).join(Place).where(
            invert(PlaceSale.deleted),
            Place.id == idPlace,
            DaySale.id == idDaySale
        )
        return session.exec(statement).first()


def get_by_worker_between(id: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(
                invert(PlaceSale.deleted),
                PlaceSale.worker_id == id,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_by_place_between(id: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(
                invert(PlaceSale.deleted),
                PlaceSale.place_id == id,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_between(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(
                invert(PlaceSale.deleted),
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


def get_by_place_worker_between(idWorker: int, idPlace: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(
                invert(PlaceSale.deleted),
                PlaceSale.place_id == idPlace,
                PlaceSale.worker_id == idWorker,
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            ).order_by(asc(DaySale.date))
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()
