from sqlmodel import select

from config.moreno import Session
from models.type_place import TypePlace


def get(id: int):
    with Session() as session:
        return session.get(TypePlace, id)


def all():
    with Session() as session:
        statement = select(TypePlace)
        return session.exec(statement).all()
