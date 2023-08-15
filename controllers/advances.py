from sqlmodel import select

from config.moreno import Session
from models import DaySale, PlaceSale
from models.advance import Advance
from datetime import datetime
from operator import invert


def get(id: int):
    with Session() as session:
        return session.get(Advance, id)


def get_between(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(Advance) \
                .select_from(Advance) \
                .join(DaySale, Advance.daySale_id == DaySale.id).where(
                invert(Advance.deleted),
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            )
            return session.exec(statement).unique().all()
    except ValueError:
        return list()


def get_between2(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(Advance) \
                .select_from(Advance) \
                .join(PlaceSale, Advance.placeSale_id == PlaceSale.id) \
                .select_from(PlaceSale) \
                .join(DaySale, PlaceSale.daySale_id == DaySale.id).where(
                invert(Advance.deleted),
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            )
            return session.exec(statement).unique().all()
    except ValueError:
        return list()
