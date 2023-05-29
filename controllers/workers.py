from sqlmodel import select

from config.db import Session, get_password_hash
from models.worker import Worker


async def get(id: int):
    with Session() as session:
        return session.get(Worker, id)


async def save(worker: Worker):
    with Session() as session:
        if worker.password is None:
            worker.password = get_password_hash(worker.dni)
        session.add(worker)
        session.commit()
        session.refresh(worker)
        return worker


async def delete(worker: Worker):
    with Session() as session:
        session.delete(worker)
        session.commit()


async def all():
    with Session() as session:
        statement = select(Worker)
        return session.exec(statement).all()


async def actives():
    with Session() as session:
        statement = select(Worker).where(Worker.active)
        return session.exec(statement).all()


async def getByDni(dni: str):
    with Session() as session:
        statement = select(Worker).where(Worker.dni == dni)
        return session.exec(statement).first()

