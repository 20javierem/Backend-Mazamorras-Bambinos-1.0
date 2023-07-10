from sqlmodel import select

from config.moreno import Session
from models.transfer import Transfer


def get(id: int):
    with Session() as session:
        return session.get(Transfer, id)


def all():
    with Session() as session:
        statement = select(Transfer)
        return session.exec(statement).all()
