from sqlmodel import select

from config.moreno import Session
from models.worker import Worker


def get(id: int):
    with Session() as session:
        return session.get(Worker, id)


def all():
    with Session() as session:
        statement = select(Worker)
        return session.exec(statement).all()


def actives():
    with Session() as session:
        statement = select(Worker).where(Worker.active)
        return session.exec(statement).all()


def getByDni(dni: str):
    with Session() as session:
        statement = select(Worker).where(Worker.dni == dni)
        return session.exec(statement).first()
