from sqlmodel import select

from config.db import Session
from models.place import Place


async def get(id: int):
    with Session() as session:
        return session.get(Place, id)


async def save(place: Place):
    with Session() as session:
        session.add(place)
        session.commit()
        session.refresh(place)
        return place


async def delete(place: Place):
    with Session() as session:
        session.delete(place)
        session.commit()


async def all():
    with Session() as session:
        statement = select(Place)
        return session.exec(statement).all()
