from sqlmodel import select

from config.moreno import Session
from models.advance import Advance


def get(id: int):
    with Session() as session:
        return session.get(Advance, id)


def all():
    with Session() as session:
        statement = select(Advance)
        return session.exec(statement).all()
