from sqlmodel import select

from config.moreno import Session
from models.motion import Motion


async def get(id: int):
    with Session() as session:
        return session.get(Motion, id)


async def all():
    with Session() as session:
        statement = select(Motion)
        return session.exec(statement).all()
