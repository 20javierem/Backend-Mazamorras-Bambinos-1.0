from datetime import datetime

from sqlmodel import select

from config.db import Session
from models.day_sale import DaySale
from models.place_sale import PlaceSale


async def get(id: int):
    with Session() as session:
        return session.get(PlaceSale, id)


async def save(placeSale: PlaceSale):
    with Session() as session:
        session.add(placeSale)
        session.commit()
        session.refresh(placeSale)
        return placeSale


async def delete(placeSale: PlaceSale):
    with Session() as session:
        session.delete(placeSale)
        session.commit()


async def all():
    with Session() as session:
        statement = select(PlaceSale)
        return session.exec(statement).unique().all()


async def getByWorkerBetween(id: int, start: str, end: str):
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


async def getByPlaceBetween(id: int, start: str, end: str):
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
