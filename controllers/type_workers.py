from sqlmodel import select

from config.moreno import Session
from models.type_worker import TypeWorker


def get(id: int):
    with Session() as session:
        return session.get(TypeWorker, id)


def all():
    with Session() as session:
        statement = select(TypeWorker)
        return session.exec(statement).all()
