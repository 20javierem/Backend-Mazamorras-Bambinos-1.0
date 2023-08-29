from operator import invert

from sqlalchemy.exc import OperationalError
from sqlmodel import select
from config.moreno import Session
from models.user import User


def get(id):
    with Session() as session:
        return session.get(User, id)


def all():
    with Session() as session:
        statement = select(User)
        return session.exec(statement).all()


def getByUsername(username: str):
    try:
        with Session() as session:
            statement = select(User).where(User.username == username, invert(User.deleted))
            return session.exec(statement).first()
    except OperationalError:
        return getByUsername(username)
