from sqlmodel import select

from config.moreno import Session
from config.encryption import encrypt
from models import PlaceSale
from models.worker import Worker


async def get(id: int):
    with Session() as session:
        return session.get(Worker, id)

async def all():
    with Session() as session:
        statement = select(Worker)
        return session.exec(statement).all()


async def actives():
    with Session() as session:
        statement = select(Worker).where(Worker.active)
        return session.exec(statement).all()


async def hasDependences(worker: Worker) -> bool:
    with Session() as session:
        statement = select(PlaceSale).join(Worker).where(Worker.id == worker.id)
        return len(session.exec(statement).unique().all()) > 0


async def getByDni(dni: str):
    with Session() as session:
        statement = select(Worker).where(Worker.dni == dni)
        return session.exec(statement).first()
