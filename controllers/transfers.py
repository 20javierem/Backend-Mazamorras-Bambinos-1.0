from sqlmodel import select

from config.db import Session
from models.transfer import Transfer


async def get(id: int):
    with Session() as session:
        return session.get(Transfer, id)


async def save(transfer: Transfer):
    with Session() as session:
        session.add(transfer)
        session.commit()
        session.refresh(transfer)
        return transfer


async def delete(transfer: Transfer):
    with Session() as session:
        session.delete(transfer)
        session.commit()


async def all():
    with Session() as session:
        statement = select(Transfer)
        return session.exec(statement).all()
