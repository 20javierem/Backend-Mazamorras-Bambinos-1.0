from sqlmodel import select

from config.moreno import Session
from models.motion import Motion


def get(id: int):
    with Session() as session:
        return session.get(Motion, id)


def all():
    with Session() as session:
        statement = select(Motion)
        return session.exec(statement).all()
