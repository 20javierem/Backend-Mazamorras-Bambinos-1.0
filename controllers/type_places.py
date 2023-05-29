from sqlmodel import select

from config.db import Session
from models.type_place import TypePlace


async def get(id: int):
    with Session() as session:
        return session.get(TypePlace, id)


async def save(typePlace: TypePlace):
    with Session() as session:
        session.add(typePlace)
        session.commit()
        session.refresh(typePlace)
        return typePlace


async def delete(typePlace: TypePlace):
    with Session() as session:
        session.delete(typePlace)
        session.commit()


async def all():
    with Session() as session:
        statement = select(TypePlace)
        return session.exec(statement).all()
