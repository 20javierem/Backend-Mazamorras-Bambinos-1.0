from sqlmodel import select

from config.db import Session
from models.expense import Expense


async def get(id: int):
    with Session() as session:
        return session.get(Expense, id)


async def save(expense: Expense):
    with Session() as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense


async def delete(expense: Expense):
    with Session() as session:
        session.delete(expense)
        session.commit()



async def all():
    with Session() as session:
        statement = select(Expense)
        return session.exec(statement).all()
