from datetime import datetime

from sqlalchemy import asc
from sqlmodel import select

from config.moreno import Session
from models.day_sale import DaySale


def get(id: int):
    with Session() as session:
        daySale = session.get(DaySale, id)
        return daySale


def get_all():
    with Session() as session:
        statement = select(DaySale).order_by(asc(DaySale.date))
        return session.exec(statement).unique().all()


def get_of_date(date: str):
    try:
        with Session() as session:
            date: datetime = datetime.strptime(date, '%Y-%m-%d')
            statement = select(DaySale).where(DaySale.date == date)
            day_sale = session.exec(statement).first()
            return day_sale
    except TypeError or ValueError:
        return None


def get_by_range_of_date(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(DaySale).where(DaySale.date >= start.date(), DaySale.date <= end.date()).order_by(
                asc(DaySale.date))
            day_sales = session.exec(statement).all()
            return day_sales
    except ValueError:
        return list()
