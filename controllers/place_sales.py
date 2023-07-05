from datetime import datetime

from sqlmodel import select

from config.moreno import Session
from models import Place, Worker
from models.day_sale import DaySale
from models.place_sale import PlaceSale


async def get(id: int):
    with Session() as session:
        return session.get(PlaceSale, id)


async def all():
    with Session() as session:
        statement = select(PlaceSale)
        return session.exec(statement).unique().all()


async def get_by_worker_between(id: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(PlaceSale.worker_id == id, DaySale.date >= start.date(),
                                                              DaySale.date <= end.date())
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


async def get_by_place_between(id: int, start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(PlaceSale).join(DaySale).where(PlaceSale.place_id == id, DaySale.date >= start.date(),
                                                              DaySale.date <= end.date())
            day_sales = session.exec(statement).unique().all()
            return day_sales
    except ValueError:
        return list()


async def get_by_day_sale_and_worker(idDaySale: int, idWorker: int):
    with Session() as session:
        statement = select(PlaceSale).join(DaySale).join(Worker).where(Worker.id == idWorker, DaySale.id == idDaySale)
        return session.exec(statement).first()
