from datetime import datetime

from sqlmodel import select

from config.db import Session
from models.day_sale import DaySale


async def get(id: int):
    with Session() as session:
        return session.get(DaySale, id)


async def save(daySale: DaySale):
    with Session() as session:
        session.add(daySale)
        session.commit()
        for place_sale in daySale.placeSales:
            place_sale.daySale = daySale
            session.add(place_sale)
            session.commit()
            session.refresh(place_sale)
        for product_day_sale in daySale.productDaySales:
            product_day_sale.daySale = daySale
            session.add(product_day_sale)
            session.commit()
            session.refresh(product_day_sale)
        session.refresh(daySale)
        return daySale


async def delete(daySale: DaySale):
    with Session() as session:
        session.delete(daySale)
        session.commit()


async def all():
    with Session() as session:
        statement = select(DaySale)
        return session.exec(statement).unique().all()


async def getOfDate(date: str):
    try:
        with Session() as session:
            date: datetime = datetime.strptime(date, '%Y-%m-%d')
            statement = select(DaySale).where(DaySale.date == date)
            day_sale = session.exec(statement).one()
            return day_sale
    except ValueError:
        return None


async def getByRangeOfDate(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(DaySale).where(DaySale.date >= start.date(), DaySale.date <= end.date())
            day_sales = session.exec(statement).all()
            return day_sales
    except ValueError:
        return list()
