from sqlmodel import select

from config.db import Session
from models.type_worker import TypeWorker


async def save(type_worker: TypeWorker):
    with Session() as session:
        session.add(type_worker)
        session.commit()
        session.refresh(type_worker)
        return type_worker


async def delete(type_worker: TypeWorker):
    with Session() as session:
        session.delete(type_worker)
        session.commit()


async def get(id: int):
    with Session() as session:
        return session.get(TypeWorker, id)


async def all():
    with Session() as session:
        statement = select(TypeWorker)
        return session.exec(statement).all()
