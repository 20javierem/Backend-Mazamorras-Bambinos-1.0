from sqlmodel import select

from config.moreno import Session
from models import Place
from models.type_place import TypePlace


async def get(id: int):
    with Session() as session:
        return session.get(TypePlace, id)


async def all():
    with Session() as session:
        statement = select(TypePlace)
        return session.exec(statement).all()


async def hasDependences(typePlace: TypePlace) -> bool:
    with Session() as session:
        statement = select(Place).join(TypePlace).where(TypePlace.id == typePlace.id)
        return len(session.exec(statement).unique().all()) > 0
