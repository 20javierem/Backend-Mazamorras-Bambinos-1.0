from sqlmodel import select

from config.moreno import Session
from models.place import Place


def get(id: int):
    with Session() as session:
        return session.get(Place, id)


def all():
    with Session() as session:
        statement = select(Place)
        return session.exec(statement).all()
