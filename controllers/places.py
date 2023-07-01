from sqlmodel import select

from config.moreno import Session
from models import PlaceSale
from models.place import Place


async def get(id: int):
    with Session() as session:
        return session.get(Place, id)


async def all():
    with Session() as session:
        statement = select(Place)
        return session.exec(statement).all()


async def hasDependences(place: Place) -> bool:
    with Session() as session:
        statement = select(PlaceSale).join(Place).where(Place.id == place.id)
        return len(session.exec(statement).unique().all()) > 0
