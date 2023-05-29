from sqlmodel import select

from config.db import Session
from models.advance import Advance


async def get(id: int):
    with Session() as session:
        return session.get(Advance, id)


async def save(advance: Advance):
    with Session() as session:
        session.add(advance)
        session.commit()
        session.refresh(advance)
        return advance


async def delete(advance: Advance):
    with Session() as session:
        session.delete(advance)
        session.commit()


async def all():
    with Session() as session:
        statement = select(Advance)
        return session.exec(statement).all()