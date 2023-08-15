from datetime import datetime
from operator import invert

from sqlmodel import select

from config.moreno import Session
from models import PlaceSale, DaySale
from models.motion import Motion


def get(id: int):
    with Session() as session:
        return session.get(Motion, id)


def get_between(start: str, end: str):
    try:
        with Session() as session:
            start: datetime = datetime.strptime(start, '%Y-%m-%d')
            end: datetime = datetime.strptime(end, '%Y-%m-%d')
            statement = select(Motion) \
                .select_from(Motion) \
                .join(DaySale, Motion.daySale_id == DaySale.id).where(
                invert(Motion.deleted),
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
            statement = select(Motion) \
                .select_from(Motion) \
                .join(PlaceSale, Motion.placeSale_id == PlaceSale.id) \
                .select_from(PlaceSale) \
                .join(DaySale, PlaceSale.daySale_id == DaySale.id).where(
                invert(Motion.deleted),
                DaySale.date >= start.date(),
                DaySale.date <= end.date()
            )
            return session.exec(statement).unique().all()
    except ValueError:
        return list()
