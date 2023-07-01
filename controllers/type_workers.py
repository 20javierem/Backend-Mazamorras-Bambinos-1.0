from sqlmodel import select

from config.moreno import Session
from models import Worker
from models.type_worker import TypeWorker


async def get(id: int):
    with Session() as session:
        return session.get(TypeWorker, id)


async def all():
    with Session() as session:
        statement = select(TypeWorker)
        return session.exec(statement).all()


async def hasDependences(typeWorker: TypeWorker) -> bool:
    with Session() as session:
        statement = select(Worker).join(TypeWorker).where(TypeWorker.id == typeWorker.id)
        return len(session.exec(statement).unique().all()) > 0
